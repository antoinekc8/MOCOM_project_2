# Final RL Traffic Control Function

## 📋 Quick Navigation

| File | Purpose | Start Here? |
|------|---------|------------|
| **`quickstart.py`** | Fastest way to run a simulation | ✅ YES |
| **`run_rl_simulation.py`** | Main function & CLI | Core module |
| **`examples_run_rl_simulation.py`** | 5 usage examples | Learn patterns |
| **`README.md`** | Complete documentation | Full reference |
| **`SUMMARY.md`** | Overview & features | Understand what's included |

---

## 🚀 Get Started in 30 Seconds

### 1. Edit `quickstart.py`
Open `quickstart.py` and update these three paths to match your setup:
```python
CONFIG_PATH = "path/to/ff_heterogeneous.sumocfg"
MODEL_PATH = "path/to/final_model.pth"
RESULTS_DIR = "path/to/results"
```

### 2. Run It
```bash
python quickstart.py
```

That's it! The simulation will run and output results.

---

## 📚 Learning Path

### Beginner: Just Run a Simulation
1. Use `quickstart.py`
2. Update the paths
3. Run it

### Intermediate: Customize Parameters
1. Read `SUMMARY.md` for overview
2. Run `examples_run_rl_simulation.py`
3. Adapt an example for your needs

### Advanced: Full Reproducibility
1. Read `README.md` completely
2. Study `examples_run_rl_simulation.py` (Example 5)
3. Document all parameters
4. Share your configuration

---

## 🔧 Main Function

```python
from run_rl_simulation import Group2

results = Group2(
    config_path="path/to/config.sumocfg",
    model_path="path/to/final_model.pth",
    results_dir="path/to/results",
    scenario_duration=3600  # 1 hour
)
```

### Returns
- `success`: bool - Whether simulation completed
- `total_reward`: float - Cumulative reward score
- `steps`: int - Number of simulation steps
- `tripinfo_file`: str - Path to vehicle data output
- `edgedata_file`: str - Path to edge statistics output

---

## 📋 What This Does

✅ Runs RL-based traffic control simulation  
✅ Uses pre-trained model (no training)  
✅ All paths are configurable (reproducible)  
✅ Outputs trip and edge data  
✅ Error handling and validation  

❌ Does NOT train the model  
❌ Does NOT compute KPIs  
❌ Does NOT create visualizations  

---

## ⚡ Command Line Usage

```bash
python run_rl_simulation.py \
    --config Network/config.sumocfg \
    --model Network/models/final_model.pth \
    --results Network/results \
    --duration 3600 \
    --yellow 3 \
    --min-green 10
```

---

## 📊 Output Files

After running, you get:
- `tripinfo_eval_ep999.xml` - Vehicle trip data
- `edge_data_eval_ep999.xml` - Network edge statistics

Use these with the original notebook's KPI analysis section for detailed performance metrics.

---

## ❓ FAQ

**Q: I don't have a trained model**  
A: Run the training phase in the original notebook first (3. Network with RL traffic control.ipynb)

**Q: I want to change traffic light timing**  
A: Use `yellow_duration` and `min_green` parameters

**Q: How do I share my results?**  
A: Save your parameters to JSON and share with the output XML files

**Q: Can I run this multiple times?**  
A: Yes! Each run produces new results (appends to XML or overwrites)

---

## 📖 Documentation Files

- **README.md**: Complete reference with all details
- **SUMMARY.md**: Overview of features and differences
- **This file (INDEX.md)**: Quick navigation
- **quickstart.py**: Working example to copy
- **examples_run_rl_simulation.py**: 5 different usage patterns

---

## 🎯 Typical Workflow

```
1. Train model (original notebook) → final_model.pth
   ↓
2. Run evaluation (this function) → tripinfo_eval_ep999.xml
   ↓
3. Analyze results (original notebook KPI section)
   ↓
4. Compare scenarios (4. Scenario comparison.ipynb)
```

This folder provides step 2: evaluation without training or analysis.

---

## Need Help?

1. **Quick question?** → Check SUMMARY.md
2. **Usage example?** → Look at examples_run_rl_simulation.py
3. **Detailed reference?** → Read README.md
4. **Just want to run it?** → Use quickstart.py

---

**Version**: 1.0  
**Created**: January 2026  
**Status**: Ready for use  
