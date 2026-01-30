"""
Example usage of the RL traffic control simulation function.

This script demonstrates how to use Group2() for reproducibility
with all file paths specified as arguments.
"""

import os
from groupe2 import Group2


def example_1_basic_usage():
    """
    Example 1: Basic usage with default parameters.
    
    Assumes you're running from the project root directory and have the standard
    folder structure:
    - Network with RL control/ff_heterogeneous.sumocfg
    - Network with RL control/models/final_model.pth
    - Network with RL control/results/
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage")
    print("="*70)
    
    # Get current directory
    base_dir = os.getcwd()
    
    # Define all paths explicitly
    config_path = os.path.join(
        base_dir, 
        "Network with RL control", 
        "ff_heterogeneous.sumocfg"
    )
    model_path = os.path.join(
        base_dir,
        "Network with RL control",
        "models",
        "final_model.pth"
    )
    results_dir = os.path.join(
        base_dir,
        "Network with RL control",
        "results"
    )
    
    # Run simulation with all paths specified
    results = Group2(
        config_path=config_path,
        model_path=model_path,
        results_dir=results_dir,
        scenario_duration=3600,  # 1 hour
        verbose=True
    )
    
    return results


def example_2_custom_duration():
    """
    Example 2: Run with custom simulation duration (e.g., 30 minutes).
    
    Useful for quick testing before running full 1-hour simulation.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Custom Duration (30 minutes)")
    print("="*70)
    
    base_dir = os.getcwd()
    config_path = os.path.join(base_dir, "Network with RL control", "ff_heterogeneous.sumocfg")
    model_path = os.path.join(base_dir, "Network with RL control", "models", "final_model.pth")
    results_dir = os.path.join(base_dir, "Network with RL control", "results")
    
    results = Group2(
        config_path=config_path,
        model_path=model_path,
        results_dir=results_dir,
        scenario_duration=1800,  # 30 minutes
        verbose=True
    )
    
    return results


def example_3_custom_traffic_lights():
    """
    Example 3: Control only specific traffic lights.
    
    Useful if your network has different TLS IDs or you want to control a subset.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Traffic Light IDs")
    print("="*70)
    
    base_dir = os.getcwd()
    config_path = os.path.join(base_dir, "Network with RL control", "ff_heterogeneous.sumocfg")
    model_path = os.path.join(base_dir, "Network with RL control", "models", "final_model.pth")
    results_dir = os.path.join(base_dir, "Network with RL control", "results")
    
    results = Group2(
        config_path=config_path,
        model_path=model_path,
        results_dir=results_dir,
        tls_ids=["E1", "E2"],  # Control only E1 and E2
        scenario_duration=3600,
        verbose=True
    )
    
    return results


def example_4_custom_timing():
    """
    Example 4: Customize yellow phase and minimum green times.
    
    Useful for testing different traffic signal timing parameters.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom Signal Timing")
    print("="*70)
    
    base_dir = os.getcwd()
    config_path = os.path.join(base_dir, "Network with RL control", "ff_heterogeneous.sumocfg")
    model_path = os.path.join(base_dir, "Network with RL control", "models", "final_model.pth")
    results_dir = os.path.join(base_dir, "Network with RL control", "results")
    
    results = Group2(
        config_path=config_path,
        model_path=model_path,
        results_dir=results_dir,
        scenario_duration=3600,
        yellow_duration=4,  # 4 seconds yellow instead of 3
        min_green=15,       # 15 seconds minimum green instead of 10
        verbose=True
    )
    
    return results


def example_5_full_reproducibility():
    """
    Example 5: Full reproducibility with all parameters explicitly set.
    
    This is the recommended pattern for publication/sharing of results.
    Every parameter is explicitly specified, so someone else can reproduce
    your exact simulation.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Full Reproducibility - All Parameters Explicit")
    print("="*70)
    
    # Define all parameters explicitly for maximum reproducibility
    BASE_DIR = os.getcwd()
    SCENARIO_NAME = "Network with RL control"
    
    # All paths specified as absolute paths
    config_path = os.path.abspath(
        os.path.join(BASE_DIR, SCENARIO_NAME, "ff_heterogeneous.sumocfg")
    )
    model_path = os.path.abspath(
        os.path.join(BASE_DIR, SCENARIO_NAME, "models", "final_model.pth")
    )
    results_dir = os.path.abspath(
        os.path.join(BASE_DIR, SCENARIO_NAME, "results")
    )
    
    # All simulation parameters explicit
    simulation_params = {
        'config_path': config_path,
        'model_path': model_path,
        'results_dir': results_dir,
        'scenario_duration': 3600,      # 1 hour
        'tls_ids': ["E1", "E2", "E3"],
        'yellow_duration': 3,
        'min_green': 10,
        'verbose': True
    }
    
    # Document the parameters used
    print("Simulation Parameters:")
    print("-" * 70)
    for key, value in simulation_params.items():
        print(f"  {key:.<40} {value}")
    print("-" * 70)
    
    # Run simulation
    results = Group2(**simulation_params)
    
    # Document the results
    print("\nResults:")
    print("-" * 70)
    for key, value in results.items():
        print(f"  {key:.<40} {value}")
    print("-" * 70)
    
    return results, simulation_params


if __name__ == "__main__":
    import sys
    
    # Run examples based on command-line argument
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
    else:
        example_num = "1"
    
    print("\n")
    print("*" * 70)
    print("RL Traffic Control Simulation - Usage Examples")
    print("*" * 70)
    
    if example_num == "1":
        example_1_basic_usage()
    elif example_num == "2":
        example_2_custom_duration()
    elif example_num == "3":
        example_3_custom_traffic_lights()
    elif example_num == "4":
        example_4_custom_timing()
    elif example_num == "5":
        example_5_full_reproducibility()
    else:
        print(f"\nExample {example_num} not found.")
        print("Available examples: 1, 2, 3, 4, 5")
        print("\nUsage: python examples_run_rl_simulation.py [1-5]")
