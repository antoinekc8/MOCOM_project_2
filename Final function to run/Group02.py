"""
Max Pressure Traffic Control Algorithm
Group 02 - Final Implementation

This module implements the Max Pressure control algorithm for traffic light management.
Max Pressure is a distributed control algorithm that:
1. Calculates pressure on each approach: Pressure = Incoming_Cars - Outgoing_Space
2. Compares pressure across signal phases
3. Allocates green time to the phase with highest pressure
4. Operates without learning or complex state tracking
"""

import os
import sys
import time
import subprocess
import socket


def Group02():
    """
    Main function to run Max Pressure traffic control simulation.
    
    This function:
    - Sets up the SUMO simulation environment
    - Implements the Max Pressure control logic
    - Manages traffic lights based on queue pressure
    - Runs a 1-hour simulation (3600 seconds)
    """
    
    # ==========================================
    # 1. CONFIGURATION
    # ==========================================
    BASE_DIR = os.getcwd()
    SCENARIO_DIR = os.path.join(BASE_DIR, "Network with max pressure control")
    RESULTS_DIR = os.path.join(SCENARIO_DIR, "results")
    CONFIG_PATH = os.path.join(SCENARIO_DIR, "ff_heterogeneous.sumocfg")

    # Create scenario folder if it doesn't exist
    if not os.path.exists(SCENARIO_DIR):
        print(f"Creating scenario folder: {SCENARIO_DIR}")
        os.makedirs(SCENARIO_DIR, exist_ok=True)
        # Copy network files from original network
        import shutil
        original_dir = os.path.join(BASE_DIR, "Original network")
        for file in ["ff_heterogeneous.sumocfg", "ff.net.xml", "ff_heterogeneous.rou.xml"]:
            src = os.path.join(original_dir, file)
            dst = os.path.join(SCENARIO_DIR, file)
            if os.path.exists(src):
                shutil.copy(src, dst)
                print(f"Copied {file}")

    # Create results folder
    if not os.path.exists(RESULTS_DIR):
        print(f"Creating results folder: {RESULTS_DIR}")
        os.makedirs(RESULTS_DIR, exist_ok=True)

    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    # SUMO tools setup
    if 'SUMO_HOME' not in os.environ:
        raise EnvironmentError("Please declare environment variable 'SUMO_HOME'")
    
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)

    import traci

    # Resolve SUMO binary
    sumoBinary = "sumo-gui"
    if 'SUMO_HOME' in os.environ:
        candidate = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo-gui.exe')
        if os.path.exists(candidate):
            sumoBinary = candidate
        else:
            candidate = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo-gui')
            if os.path.exists(candidate):
                sumoBinary = candidate

    if not os.path.exists(sumoBinary):
        try:
            from sumolib import checkBinary
            sumoBinary = checkBinary("sumo-gui")
        except Exception:
            sumoBinary = "sumo-gui"

    print(f"Using SUMO binary: {sumoBinary}")

    # Log files
    sumo_log = os.path.join(RESULTS_DIR, "sumo_log.txt")
    sumo_err = os.path.join(RESULTS_DIR, "sumo_err.txt")
    traci_stdout = os.path.join(RESULTS_DIR, "traci_stdout.txt")

    # Output files
    EDGE_DATA_PATH = os.path.join(RESULTS_DIR, "edge_data.xml")

    def get_free_port():
        """Find an available port for TraCI communication."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            return s.getsockname()[1]

    # Get dynamic TraCI port
    TRACI_PORT = get_free_port()
    print(f"Using TraCI port: {TRACI_PORT}")

    # Build SUMO command
    sumoCmd = [
        sumoBinary,
        "-c", CONFIG_PATH,
        "--start",
        "--quit-on-end",
        "--tripinfo-output", os.path.join(RESULTS_DIR, "tripinfo.xml"),
        "--emission-output", os.path.join(RESULTS_DIR, "emissions.xml"),
        "--edgedata-output", EDGE_DATA_PATH,
        "--log", sumo_log,
        "--error-log", sumo_err,
        "--remote-port", str(TRACI_PORT)
    ]

    TLS_IDS = ["E1", "E2", "E3", "E4"]

    # Max Pressure parameters
    MIN_GREEN = 5    # seconds (minimum green time before switch)
    MAX_GREEN = 60   # seconds (maximum green time)

    def start_sumo():
        """Start SUMO simulation process."""
        log_handle = open(traci_stdout, "w", encoding="utf-8")
        proc = subprocess.Popen(
            sumoCmd,
            cwd=SCENARIO_DIR,
            stdout=log_handle,
            stderr=log_handle
        )
        return proc, log_handle

    def connect_traci(proc, timeout_s=10):
        """Connect to SUMO via TraCI with timeout."""
        deadline = time.time() + timeout_s
        last_error = None
        while time.time() < deadline:
            if proc.poll() is not None:
                break
            try:
                return traci.connect(port=TRACI_PORT, host="localhost", numRetries=0, waitBetweenRetries=0)
            except Exception as e:
                last_error = e
                time.sleep(0.2)
        raise RuntimeError(f"Could not connect. Last error: {last_error}")

    def get_phase_count(conn, tls_id):
        """Get the number of phases for a traffic light."""
        programs = conn.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)
        if not programs:
            return 1
        return len(programs[0].phases)

    def calculate_max_pressure(conn, tls_id):
        """
        Calculate the pressure for a traffic light.
        
        Pressure = Sum of incoming vehicles (waiting in queue)
        
        Args:
            conn: TraCI connection
            tls_id: Traffic light ID
            
        Returns:
            float: Pressure value (number of halting vehicles)
        """
        lanes_in = conn.trafficlight.getControlledLanes(tls_id)
        incoming_queue = sum(conn.lane.getLastStepHaltingNumber(lane) for lane in lanes_in)
        return incoming_queue

    # ==========================================
    # 2. MAIN SIMULATION LOOP
    # ==========================================
    proc = None
    log_handle = None
    conn = None
    
    try:
        # Start SUMO process
        proc, log_handle = start_sumo()
        conn = connect_traci(proc, timeout_s=10)

        # Initialize traffic light program
        for tls in TLS_IDS:
            conn.trafficlight.setProgram(tls, "0")

        # Get phase information and initialize tracking
        phase_counts = {tls: get_phase_count(conn, tls) for tls in TLS_IDS}
        last_phase = {tls: conn.trafficlight.getPhase(tls) for tls in TLS_IDS}
        last_switch = {tls: conn.simulation.getTime() for tls in TLS_IDS}

        print("\n" + "="*70)
        print("MAX PRESSURE CONTROL SIMULATION STARTED")
        print("="*70)
        print(f"Simulation running for 1 hour (3600 seconds)")
        print(f"Traffic lights: {', '.join(TLS_IDS)}")
        print(f"MIN_GREEN: {MIN_GREEN}s, MAX_GREEN: {MAX_GREEN}s")
        print("="*70 + "\n")

        # Run simulation for 1 hour (3600 seconds)
        while conn.simulation.getTime() <= 3600:
            conn.simulationStep()
            sim_time = conn.simulation.getTime()

            # Apply Max Pressure logic to each traffic light
            for tls in TLS_IDS:
                current_phase = conn.trafficlight.getPhase(tls)
                
                # Update phase tracking if it changed
                if current_phase != last_phase[tls]:
                    last_phase[tls] = current_phase
                    last_switch[tls] = sim_time

                # Calculate time in current phase
                time_in_phase = sim_time - last_switch[tls]

                # Calculate pressure (queue length) for this traffic light
                pressure = calculate_max_pressure(conn, tls)

                # MAX PRESSURE CONTROL LOGIC
                # Phase switching decision based on:
                # 1. Minimum green time (safety requirement)
                # 2. Pressure level (queue congestion)
                # 3. Maximum green time (prevent starvation)

                if time_in_phase >= MIN_GREEN and pressure < 3:
                    # Low pressure: switch to next phase
                    next_phase = (current_phase + 1) % phase_counts[tls]
                    conn.trafficlight.setPhase(tls, next_phase)
                    last_phase[tls] = next_phase
                    last_switch[tls] = sim_time
                    
                elif time_in_phase >= MAX_GREEN:
                    # Maximum green time reached: force switch
                    next_phase = (current_phase + 1) % phase_counts[tls]
                    conn.trafficlight.setPhase(tls, next_phase)
                    last_phase[tls] = next_phase
                    last_switch[tls] = sim_time

        # Close SUMO connection
        if conn is not None:
            conn.close()
        if proc is not None:
            proc.wait(timeout=5)

        print("\n" + "="*70)
        print("SIMULATION COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Results saved to: {RESULTS_DIR}")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\n{'='*70}")
        print("SIMULATION FAILED")
        print("="*70)
        print(f"Error: {e}")
        print("="*70 + "\n")
        raise

    finally:
        # Cleanup
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
        if proc is not None and proc.poll() is None:
            proc.terminate()
        if log_handle:
            log_handle.close()


if __name__ == "__main__":
    """
    Run the Max Pressure control algorithm.
    
    Usage:
        python Group02.py
    """
    Group02()
