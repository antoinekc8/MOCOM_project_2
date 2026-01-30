#!/usr/bin/env python3
"""
QUICK START - RL Traffic Control Simulation

This is the fastest way to get started with running RL traffic control simulations.
Copy this file and customize the paths to your scenario.
"""

import os
import sys
from run_rl_simulation import Group2


def main():
    """
    Run RL traffic control simulation with explicit paths.
    
    ⚠️ CUSTOMIZE THESE PATHS FOR YOUR SETUP:
    """
    
    # ===== CUSTOMIZE THESE PATHS =====
    BASE_DIR = os.getcwd()  # Your project directory
    
    CONFIG_PATH = os.path.join(
        BASE_DIR,
        "Network with RL control",
        "ff_heterogeneous.sumocfg"
    )
    
    MODEL_PATH = os.path.join(
        BASE_DIR,
        "Network with RL control",
        "models",
        "final_model.pth"
    )
    
    RESULTS_DIR = os.path.join(
        BASE_DIR,
        "Network with RL control",
        "results"
    )
    
    # ===== SIMULATION PARAMETERS =====
    SCENARIO_DURATION = 3600        # seconds (1 hour)
    TLS_IDS = ["E1", "E2", "E3"]  # Traffic light IDs
    YELLOW_DURATION = 3             # seconds
    MIN_GREEN = 10                  # seconds
    
    # ===== VALIDATE FILES =====
    print("=" * 70)
    print("RL TRAFFIC CONTROL - QUICK START")
    print("=" * 70)
    
    print("\nChecking files...")
    if not os.path.exists(CONFIG_PATH):
        print(f"✗ Config file not found: {CONFIG_PATH}")
        return False
    print(f"✓ Config: {CONFIG_PATH}")
    
    if not os.path.exists(MODEL_PATH):
        print(f"✗ Model file not found: {MODEL_PATH}")
        return False
    print(f"✓ Model:  {MODEL_PATH}")
    
    print(f"✓ Results dir: {RESULTS_DIR}")
    
    # ===== PRINT CONFIGURATION =====
    print("\nSimulation Configuration:")
    print("-" * 70)
    print(f"  Duration:        {SCENARIO_DURATION} seconds ({SCENARIO_DURATION//60} minutes)")
    print(f"  Traffic Lights:  {', '.join(TLS_IDS)}")
    print(f"  Yellow Phase:    {YELLOW_DURATION} seconds")
    print(f"  Min Green:       {MIN_GREEN} seconds")
    print("-" * 70)
    
    # ===== RUN SIMULATION =====
    print("\nStarting simulation...\n")
    
    results = Group2(
        config_path=CONFIG_PATH,
        model_path=MODEL_PATH,
        results_dir=RESULTS_DIR,
        scenario_duration=SCENARIO_DURATION,
        tls_ids=TLS_IDS,
        yellow_duration=YELLOW_DURATION,
        min_green=MIN_GREEN,
        verbose=True
    )
    
    # ===== PRINT RESULTS =====
    print("\n" + "=" * 70)
    print("SIMULATION RESULTS")
    print("=" * 70)
    
    if results['success']:
        print(f"✓ Status:         SUCCESS")
        print(f"  Total Reward:   {results['total_reward']:.2f}")
        print(f"  Steps:          {results['steps']}")
        print(f"  Tripinfo:       {results['tripinfo_file']}")
        print(f"  Edge Data:      {results['edgedata_file']}")
        print("\n✓ Simulation completed successfully!")
        print("  Output files saved to:", RESULTS_DIR)
        return True
    else:
        print(f"✗ Status:  FAILED")
        print(f"  Error:   {results.get('error', 'Unknown error')}")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
