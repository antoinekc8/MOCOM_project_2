"""
RL Traffic Control Simulation - Evaluation Phase Only

This module runs a SUMO simulation using a pre-trained RL agent for traffic control.
It skips the training phase and assumes final_model.pth already exists.
All file paths are configurable as function arguments for reproducibility.

Usage:
    from run_rl_simulation import run_rl_traffic_control
    
    results = run_rl_traffic_control(
        config_path="path/to/ff_heterogeneous.sumocfg",
        model_path="path/to/final_model.pth",
        results_dir="path/to/results",
        scenario_duration=3600  # seconds
    )
"""

import os
import sys
import torch
import torch.nn as nn
import numpy as np
from collections import deque
from pathlib import Path


# ==========================================
# 1. NEURAL NETWORK (DQN)
# ==========================================
class DQN(nn.Module):
    """Simple DQN for traffic light control."""
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, output_size)
        )

    def forward(self, x):
        return self.fc(x)


# ==========================================
# 2. RL AGENT
# ==========================================
class DQNAgent:
    """DQN Agent for inference (evaluation mode)."""
    
    def __init__(self, state_size, action_size, device):
        self.state_size = state_size
        self.action_size = action_size
        self.device = device
        
        self.policy_net = DQN(state_size, action_size).to(device)
        self.policy_net.eval()

    def act_inference(self, state):
        """Inference mode: select action with highest Q-value."""
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.policy_net(state_tensor)
        return torch.argmax(q_values).item()

    def load(self, path):
        """Load pre-trained model weights."""
        if not os.path.exists(path):
            return False
        try:
            self.policy_net.load_state_dict(torch.load(path, map_location=self.device))
            self.policy_net.eval()
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False


# ==========================================
# 3. SUMO ENVIRONMENT FUNCTIONS
# ==========================================
def setup_sumo():
    """Configure SUMO environment and return tools path."""
    if 'SUMO_HOME' not in os.environ:
        raise RuntimeError(
            "SUMO_HOME environment variable is not set. "
            "Please install SUMO and set SUMO_HOME to the installation directory."
        )
    
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    if tools not in sys.path:
        sys.path.append(tools)
    
    return tools


def get_sumo_binary():
    """Get path to SUMO executable."""
    sumo_home = os.environ.get('SUMO_HOME')
    if not sumo_home:
        raise RuntimeError("SUMO_HOME not set")
    return os.path.join(sumo_home, 'bin', 'sumo')


def get_state(tls_id):
    """
    Extract state from traffic light.
    
    State (Size 3):
    1. Total Queue Length (Normalized)
    2. Max Queue Length (Normalized)  
    3. Current Phase Index (Normalized)
    """
    import traci
    
    lanes = traci.trafficlight.getControlledLanes(tls_id)
    halting = [traci.lane.getLastStepHaltingNumber(lane) for lane in lanes]
    
    total_queue = sum(halting) / 50.0
    max_queue = max(halting) / 20.0
    phase = traci.trafficlight.getPhase(tls_id) / 4.0
    
    return np.array([total_queue, max_queue, phase], dtype=np.float32)


def get_reward(tls_id, waiting_time_prev):
    """
    Calculate reward signal (for monitoring only, not used for training).
    
    Reward = (Waiting Time Reduction) - (Queue Penalty)
    """
    import traci
    
    lanes = traci.trafficlight.getControlledLanes(tls_id)
    current_wait = sum([traci.lane.getWaitingTime(lane) for lane in lanes])
    current_queue = sum([traci.lane.getLastStepHaltingNumber(lane) for lane in lanes])
    
    diff = waiting_time_prev - current_wait
    reward = (diff * 0.2) - (current_queue * 0.05)
    reward = max(min(reward, 5.0), -5.0)
    
    return reward, current_wait


# ==========================================
# 4. MAIN SIMULATION FUNCTION
# ==========================================
def Group2(
    config_path,
    model_path,
    results_dir,
    scenario_duration=3600,
    tls_ids=None,
    yellow_duration=3,
    min_green=10,
    verbose=True
):
    """
    Run RL-based traffic control simulation on SUMO network.
    
    This function performs evaluation ONLY - no training.
    Assumes the model file (final_model.pth) already exists.
    
    Parameters
    ----------
    config_path : str
        Path to SUMO configuration file (.sumocfg)
    model_path : str
        Path to pre-trained model file (final_model.pth)
    results_dir : str
        Directory where simulation results will be saved
    scenario_duration : int, optional
        Simulation duration in seconds (default: 3600 = 1 hour)
    tls_ids : list, optional
        List of traffic light IDs to control (default: ["E1", "E2", "E3"])
    yellow_duration : int, optional
        Duration of yellow phase in seconds (default: 3)
    min_green : int, optional
        Minimum green phase duration in seconds (default: 10)
    verbose : bool, optional
        Print progress information (default: True)
    
    Returns
    -------
    dict
        Simulation results containing:
        - 'success': bool, whether simulation completed
        - 'total_reward': float, cumulative reward
        - 'steps': int, simulation steps executed
        - 'tripinfo_file': str, path to tripinfo output
        - 'edgedata_file': str, path to edge data output
    
    Raises
    ------
    RuntimeError
        If SUMO_HOME not set or model file not found
    FileNotFoundError
        If config_path or model_path doesn't exist
    
    Example
    -------
    >>> results = run_rl_traffic_control(
    ...     config_path="Network with RL control/ff_heterogeneous.sumocfg",
    ...     model_path="Network with RL control/models/final_model.pth",
    ...     results_dir="Network with RL control/results"
    ... )
    >>> print(f"Simulation completed: {results['success']}")
    >>> print(f"Total reward: {results['total_reward']:.2f}")
    """
    
    # Set defaults
    if tls_ids is None:
        tls_ids = ["E1", "E2", "E3"]
    
    # Validate inputs
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Create results directory
    os.makedirs(results_dir, exist_ok=True)
    
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if verbose:
        print(f"Device: {device}")
    
    # Setup SUMO
    try:
        setup_sumo()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return {
            'success': False,
            'error': str(e),
            'total_reward': 0,
            'steps': 0
        }
    
    # Import traci after setting up path
    import traci
    
    # Load agent
    agent = DQNAgent(state_size=3, action_size=2, device=device)
    if not agent.load(model_path):
        return {
            'success': False,
            'error': f"Failed to load model from {model_path}",
            'total_reward': 0,
            'steps': 0
        }
    
    if verbose:
        print(f"✓ Model loaded from {model_path}")
    
    sumo_bin = get_sumo_binary()
    
    # Output files
    tripinfo_output = os.path.join(results_dir, "tripinfo_eval_ep999.xml")
    edgedata_output = os.path.join(results_dir, "edge_data_eval_ep999.xml")
    
    try:
        if verbose:
            print("Starting SUMO simulation...")
        
        # Build SUMO command
        sumo_cmd = [
            sumo_bin,
            "-c", config_path,
            "--quit-on-end",
            "--no-step-log",
            "--waiting-time-memory", "1000",
            "--tripinfo-output", tripinfo_output,
            "--edgedata-output", edgedata_output
        ]
        
        # Start SUMO
        traci.start(sumo_cmd)
        
        # Initialize traffic lights
        for tls in tls_ids:
            try:
                traci.trafficlight.setProgram(tls, "0")
            except traci.exceptions.TraCIException:
                if verbose:
                    print(f"Warning: Traffic light {tls} not found in network")
        
        # Initialize tracking data
        tls_data = {t: {"prev_wait": 0, "phase_time": 0} for t in tls_ids}
        total_reward = 0
        step_count = 0
        
        if verbose:
            print(f"Running evaluation for {scenario_duration} seconds...")
        
        # Main simulation loop
        while traci.simulation.getTime() < scenario_duration:
            traci.simulationStep()
            step_count += 1
            
            # Make decisions every 5 seconds
            if step_count % 5 == 0:
                for tls in tls_ids:
                    try:
                        # Get state and select action
                        state = get_state(tls)
                        action = agent.act_inference(state)
                        
                        # Apply action logic
                        current_phase = traci.trafficlight.getPhase(tls)
                        
                        if current_phase == 1 or current_phase == 3:
                            # Yellow phase: wait for it to complete
                            tls_data[tls]["phase_time"] += 5
                            if tls_data[tls]["phase_time"] >= yellow_duration:
                                next_phase = 2 if current_phase == 1 else 0
                                traci.trafficlight.setPhase(tls, next_phase)
                                tls_data[tls]["phase_time"] = 0
                        else:
                            # Green phase: apply RL decision
                            target_phase = 0 if action == 0 else 2
                            
                            if current_phase != target_phase:
                                if tls_data[tls]["phase_time"] >= min_green:
                                    traci.trafficlight.setPhase(tls, current_phase + 1)
                                    tls_data[tls]["phase_time"] = 0
                                else:
                                    tls_data[tls]["phase_time"] += 5
                            else:
                                tls_data[tls]["phase_time"] += 5
                        
                        # Calculate and accumulate reward
                        reward, new_wait = get_reward(tls, tls_data[tls]["prev_wait"])
                        tls_data[tls]["prev_wait"] = new_wait
                        total_reward += reward
                    
                    except traci.exceptions.TraCIException:
                        # Traffic light not in network, skip
                        pass
        
        traci.close()
        
        if verbose:
            print(f"✓ Simulation completed successfully!")
            print(f"  Total reward: {total_reward:.2f}")
            print(f"  Simulation steps: {step_count}")
            print(f"  Results saved to: {results_dir}")
        
        return {
            'success': True,
            'total_reward': total_reward,
            'steps': step_count,
            'tripinfo_file': tripinfo_output,
            'edgedata_file': edgedata_output
        }
    
    except Exception as e:
        if verbose:
            print(f"✗ Simulation failed: {e}")
            import traceback
            traceback.print_exc()
        
        try:
            if traci.isLoaded():
                traci.close()
        except:
            pass
        
        return {
            'success': False,
            'error': str(e),
            'total_reward': 0,
            'steps': step_count if 'step_count' in locals() else 0
        }


# ==========================================
# 5. COMMAND-LINE INTERFACE
# ==========================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run RL traffic control simulation using SUMO"
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to SUMO configuration file (.sumocfg)"
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Path to pre-trained model file (final_model.pth)"
    )
    parser.add_argument(
        "--results",
        required=True,
        help="Output directory for simulation results"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=3600,
        help="Simulation duration in seconds (default: 3600)"
    )
    parser.add_argument(
        "--tls",
        nargs="+",
        default=["E1", "E2", "E3"],
        help="Traffic light IDs to control (default: E1 E2 E3)"
    )
    parser.add_argument(
        "--yellow",
        type=int,
        default=3,
        help="Yellow phase duration in seconds (default: 3)"
    )
    parser.add_argument(
        "--min-green",
        type=int,
        default=10,
        help="Minimum green phase duration in seconds (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Convert to absolute paths
    config_path = os.path.abspath(args.config)
    model_path = os.path.abspath(args.model)
    results_dir = os.path.abspath(args.results)
    
    # Run simulation
    results = Group2(
        config_path=config_path,
        model_path=model_path,
        results_dir=results_dir,
        scenario_duration=args.duration,
        tls_ids=args.tls,
        yellow_duration=args.yellow,
        min_green=args.min_green,
        verbose=True
    )
    
    # Print results
    print("\n" + "="*70)
    print("SIMULATION RESULTS")
    print("="*70)
    if results['success']:
        print(f"Status:         SUCCESS")
        print(f"Total Reward:   {results['total_reward']:.2f}")
        print(f"Steps:          {results['steps']}")
        print(f"Tripinfo:       {results['tripinfo_file']}")
        print(f"Edge Data:      {results['edgedata_file']}")
    else:
        print(f"Status:         FAILED")
        print(f"Error:          {results.get('error', 'Unknown error')}")
    print("="*70)
