# RL Traffic Control Simulation - Evaluation Function

## Overview

This folder contains a standalone function `run_rl_traffic_control()` that runs RL-based traffic control simulation using SUMO. The function performs **evaluation only** (no training) and assumes you already have a trained model (`final_model.pth`).

## Files

- **`run_rl_simulation.py`**: Main module with the `run_rl_traffic_control()` function
- **`examples_run_rl_simulation.py`**: Usage examples demonstrating different use cases
- **`README.md`**: This file

## Function Signature

```python
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
        List of traffic light IDs to control 
        (default: ["E1", "E2", "E3"])
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
    """
```

## Quick Start

### 1. Basic Usage

```python
from run_rl_simulation import Group2

results = Group2(
    config_path="Network with RL control/ff_heterogeneous.sumocfg",
    model_path="Network with RL control/models/final_model.pth",
    results_dir="Network with RL control/results"
)

print(f"Simulation success: {results['success']}")
print(f"Total reward: {results['total_reward']:.2f}")
```

### 2. Command-Line Usage

```bash
python run_rl_simulation.py \
    --config "Network with RL control/ff_heterogeneous.sumocfg" \
    --model "Network with RL control/models/final_model.pth" \
    --results "Network with RL control/results" \
    --duration 3600 \
    --yellow 3 \
    --min-green 10
```

### 3. Run Examples

```bash
# Example 1: Basic usage
python examples_run_rl_simulation.py 1

# Example 2: Custom duration (30 minutes)
python examples_run_rl_simulation.py 2

# Example 3: Custom traffic light IDs
python examples_run_rl_simulation.py 3

# Example 4: Custom signal timing
python examples_run_rl_simulation.py 4

# Example 5: Full reproducibility (all parameters explicit)
python examples_run_rl_simulation.py 5
```

## Key Features

### ✓ No Training Required
- Assumes `final_model.pth` already exists
- Only performs evaluation/inference
- Much faster than the full notebook (just runs simulation)

### ✓ All Paths as Arguments
- Every file path is a function parameter
- No hardcoded paths
- Easy to run on different datasets or scenarios
- Full reproducibility

### ✓ Customizable Parameters
- **Simulation duration**: Control how long the simulation runs
- **Traffic light IDs**: Specify which traffic lights to control
- **Signal timing**: Customize yellow phase and minimum green times

### ✓ Output Files
- `tripinfo_eval_ep999.xml`: Trip information for all vehicles
- `edge_data_eval_ep999.xml`: Edge data (speed, waiting times, etc.)

## Input Requirements

Before running the function, ensure you have:

1. **SUMO Configuration File** (`.sumocfg`)
   - Contains network, route, and simulation settings
   - Must point to valid network (`.net.xml`) and routes (`.rou.xml`)

2. **Pre-trained Model** (`final_model.pth`)
   - PyTorch model file from training phase
   - Must be in the location specified by `model_path`

3. **SUMO Installation**
   - `SUMO_HOME` environment variable must be set
   - `sumo` executable must be in `$SUMO_HOME/bin/`

## Output Files

### Tripinfo (`tripinfo_eval_ep999.xml`)
Contains trip information for each vehicle:
- ID, departure time, arrival time
- Route taken, distance traveled
- Waiting time, speed, duration

### Edge Data (`edge_data_eval_ep999.xml`)
Contains aggregate edge statistics:
- Average speed per edge
- Total waiting time per edge
- Vehicle density per edge

## For Reproducibility

To ensure results can be reproduced:

1. **Document all parameters**:
   ```python
   params = {
       'config_path': '/absolute/path/to/config.sumocfg',
       'model_path': '/absolute/path/to/final_model.pth',
       'results_dir': '/absolute/path/to/results',
       'scenario_duration': 3600,
       'tls_ids': ["E1", "E2", "E3"],
       'yellow_duration': 3,
       'min_green': 10
   }
   ```

2. **Use absolute paths**:
   ```python
   import os
   config_path = os.path.abspath('path/to/config.sumocfg')
   ```

3. **Save parameter documentation**:
   ```python
   import json
   with open('simulation_params.json', 'w') as f:
       json.dump(params, f, indent=2)
   ```

## Excluded Features

The following components from the original notebook are NOT included:

- ❌ **Training Phase**: Function assumes model is already trained
- ❌ **KPI Computation & Analysis**: No vehicle statistics or performance metrics
- ❌ **Visualization**: No plots or dashboard generation

These can be applied to the output XML files separately if needed.

## Error Handling

The function returns a dictionary with `success` flag:

```python
results = run_rl_traffic_control(...)

if not results['success']:
    print(f"Simulation failed: {results['error']}")
else:
    print(f"Simulation succeeded!")
    print(f"Results: {results['tripinfo_file']}")
```

Common errors:

| Error | Solution |
|-------|----------|
| `SUMO_HOME not set` | Set `SUMO_HOME` environment variable |
| `Config file not found` | Verify `config_path` points to valid `.sumocfg` file |
| `Model file not found` | Verify `model_path` points to trained `final_model.pth` |
| `Traffic light not found` | Verify `tls_ids` match network definition |

## Dependencies

```python
torch            # PyTorch for neural network
numpy            # Numerical computing
traci            # SUMO TraCI Python API (installed with SUMO)
```

## Example: Full Reproducibility Script

```python
import os
import json
from run_rl_simulation import Group2

# Define all parameters explicitly
BASE_DIR = os.path.abspath('.')
SCENARIO = "Network with RL control"

params = {
    'config_path': os.path.join(BASE_DIR, SCENARIO, "ff_heterogeneous.sumocfg"),
    'model_path': os.path.join(BASE_DIR, SCENARIO, "models", "final_model.pth"),
    'results_dir': os.path.join(BASE_DIR, SCENARIO, "results"),
    'scenario_duration': 3600,
    'tls_ids': ["E1", "E2", "E3"],
    'yellow_duration': 3,
    'min_green': 10,
    'verbose': True
}

# Run simulation
results = Group2(**params)

# Save parameters for reproducibility
with open('simulation_config.json', 'w') as f:
    json.dump(params, f, indent=2)

# Print results
print(f"Success: {results['success']}")
print(f"Reward: {results['total_reward']:.2f}")
print(f"Tripinfo: {results['tripinfo_file']}")
```

## Notes

- The function is **not** designed for training - use the original notebook for that
- The function **does not** compute KPIs - use the original notebook's KPI section for analysis
- All output files are saved to `results_dir` with names following the pattern: `*_eval_ep999.xml`
- Simulation progress is printed if `verbose=True`

## Support

For issues or questions:
1. Check that all input files exist
2. Verify SUMO installation with `sumo --version`
3. Review the examples in `examples_run_rl_simulation.py`
4. Check the original notebook for network configuration details
