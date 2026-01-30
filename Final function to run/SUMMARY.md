# RL Traffic Control - Function Summary

## What Was Created

A standalone, reproducible function for running RL-based traffic control simulation without training or KPI analysis.

## Files in This Folder

### 1. `run_rl_simulation.py` (Main Module)
**Purpose**: Core function for RL simulation evaluation

**Main Function**: `Group2()`
- **Type**: Evaluation only (no training)
- **Input**: 
  - `config_path`: SUMO configuration file
  - `model_path`: Pre-trained model (final_model.pth)
  - `results_dir`: Output directory
  - `scenario_duration`: Simulation time in seconds
  - `tls_ids`: Traffic light IDs to control
  - `yellow_duration`: Yellow phase duration
  - `min_green`: Minimum green phase duration
- **Output**: Dictionary with results (success, reward, steps, file paths)

**Features**:
- No hardcoded paths - all configurable as arguments
- PyTorch neural network for inference
- SUMO integration via TraCI
- Error handling with detailed messages
- Command-line interface support

**Command-line Usage**:
```bash
python run_rl_simulation.py \
    --config "path/to/config.sumocfg" \
    --model "path/to/final_model.pth" \
    --results "path/to/results" \
    --duration 3600
```

### 2. `examples_run_rl_simulation.py` (Usage Examples)
**Purpose**: Demonstrate different ways to use the function

**Contains 5 Examples**:
1. Basic usage with defaults
2. Custom simulation duration (30 minutes)
3. Custom traffic light IDs
4. Custom signal timing parameters
5. Full reproducibility (all parameters explicit)

**Run Examples**:
```bash
python examples_run_rl_simulation.py 1    # Run example 1
python examples_run_rl_simulation.py 5    # Run example 5 (recommended)
```

### 3. `README.md` (Documentation)
**Purpose**: Complete documentation and usage guide

**Covers**:
- Function signature and parameters
- Quick start examples
- Command-line usage
- All features and capabilities
- Input requirements
- Output file descriptions
- Reproducibility best practices
- Error handling
- Dependencies

## Key Differences from Original Notebook

| Aspect | Original Notebook | This Function |
|--------|-------------------|---------------|
| Training | ✓ Included | ❌ Excluded |
| Evaluation | ✓ Included | ✓ Included |
| KPI Analysis | ✓ Included | ❌ Excluded |
| Visualization | ✓ Included | ❌ Excluded |
| Configurable Paths | ❌ Hardcoded | ✓ Function arguments |
| Reproducibility | Medium | ✓ High (all params explicit) |
| Ease of Use | Complex (full notebook) | ✓ Simple (single function) |

## What Is Included

✓ Load pre-trained model (final_model.pth)  
✓ Initialize SUMO network from config file  
✓ Run 1-hour (or custom duration) simulation  
✓ Apply RL agent control to traffic lights  
✓ Generate tripinfo XML output  
✓ Generate edge data XML output  
✓ Track cumulative reward  
✓ Error handling and validation  

## What Is NOT Included

❌ Training phase (assumes model is pre-trained)  
❌ KPI computation and statistics  
❌ Vehicle classification and filtering  
❌ Visualization and plotting  
❌ Performance analysis  

(Use original notebook or separate analysis script for these)

## Usage Pattern

### For Quick Testing
```python
from run_rl_simulation import Group2

results = Group2(
    config_path="Network with RL control/ff_heterogeneous.sumocfg",
    model_path="Network with RL control/models/final_model.pth",
    results_dir="Network with RL control/results",
    scenario_duration=1800  # 30 minutes for testing
)
```

### For Production/Reproducibility
```python
import os
import json
from run_rl_simulation import Group2

# Define all parameters explicitly
BASE_DIR = os.path.abspath('.')
params = {
    'config_path': os.path.join(BASE_DIR, "Network with RL control", "ff_heterogeneous.sumocfg"),
    'model_path': os.path.join(BASE_DIR, "Network with RL control", "models", "final_model.pth"),
    'results_dir': os.path.join(BASE_DIR, "Network with RL control", "results"),
    'scenario_duration': 3600,
    'tls_ids': ["E1", "E2", "E3"],
    'yellow_duration': 3,
    'min_green': 10
}

# Run and save configuration
results = Group2(**params)
with open('simulation_config.json', 'w') as f:
    json.dump(params, f, indent=2)
```

## Requirements

**Software**:
- Python 3.7+
- PyTorch (CPU or GPU)
- SUMO simulation software
- SUMO_HOME environment variable set

**Files**:
- SUMO config file (.sumocfg)
- Pre-trained model (final_model.pth)
- Network files (referenced by config)
- Route files (referenced by config)

## Output

Each simulation run produces:

1. **tripinfo_eval_ep999.xml**
   - Trip information for all vehicles
   - Can be analyzed for KPIs separately

2. **edge_data_eval_ep999.xml**
   - Edge statistics (speed, waiting, density)
   - Can be used for network analysis

3. **Console Output** (if verbose=True)
   - Simulation progress
   - Confirmation of model loading
   - Results summary

## For Reproducibility

To share/reproduce your simulation:

1. Document all parameters in JSON:
   ```json
   {
     "config_path": "/absolute/path/to/config.sumocfg",
     "model_path": "/absolute/path/to/final_model.pth",
     "results_dir": "/path/to/results",
     "scenario_duration": 3600,
     "tls_ids": ["E1", "E2", "E3"],
     "yellow_duration": 3,
     "min_green": 10
   }
   ```

2. Share:
   - This parameter file
   - The network files (config, .net.xml, .rou.xml)
   - The trained model (final_model.pth)

3. Recipient runs:
   ```bash
   python run_rl_simulation.py \
     --config /path/to/config.sumocfg \
     --model /path/to/final_model.pth \
     --results /path/to/results
   ```

## Next Steps

After running the simulation, you can:

1. **Analyze Results**
   - Use original notebook's KPI section on the output XML files
   - Extract vehicle-level statistics from tripinfo_eval_ep999.xml
   - Compare with baseline scenarios

2. **Compare Scenarios**
   - Run function multiple times with different parameters
   - Use output XML files in scenario comparison notebook

3. **Visualize**
   - Create custom plots from tripinfo_eval_ep999.xml
   - Generate performance reports

## Support

Refer to:
- `README.md` for detailed documentation
- `examples_run_rl_simulation.py` for usage patterns
- Original notebook for network configuration details
- Original notebook's KPI section for analysis of XML outputs
