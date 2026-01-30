# MOCOM Project 2

## Overview
This repository contains the scripts and notebooks used to analyse and compare four traffic signal control strategies in SUMO: the baseline scenario, actuated control, and max-pressure control, plus a reinforcement learning agent. The quantitative analyses and simulations generate reports and key indicators stored inside the folders of each scenario.

## Available notebooks
- 0. Original network analysis.ipynb: runs the baseline simulation with fixed signal timings and produces KPIs and visualisations under Original network/results.
- 1. Network with actuated traffic control.ipynb: configures and launches the actuated-control simulation, saving logs in Network with actuated control/results.
- 2. Network with Max Pressure traffic control.ipynb: implements the max-pressure algorithm, writes outputs to Network with max pressure control/results, and documents how pressures per phase are computed.
- 3. Network with RL traffic control.ipynb: trains and evaluates a PyTorch-based RL agent (DQN-style policy) that switches between two signal phases, saving models in Network with RL control/models and metrics in Network with RL control/results.
- 4. Scenario comparison.ipynb: aggregates the measurements of all four scenarios, compares directional KPIs on speed, waiting time, and travel duration, and exports tables and rankings in Scenario comparison results.

## Scenario folder structure
Each SUMO scenario follows the same base layout to ensure reproducible runs:

- Original network/: provides the reference intersection files (ff_heterogeneous.sumocfg, ff.net.xml, ff_heterogeneous.rou.xml) plus the results/ folder with baseline traces (edge_data.xml, tripinfo.xml).
- Network with actuated control/: stores a copy of the SUMO network files, optionally created by notebook 1, and a results/ folder that captures TraCI and SUMO logs for the actuated control.
- Network with max pressure control/: mirrors the same organisation, with notebook 2 generating results/ and saving the max-pressure reports.
- Network with RL control/: bundles the network files, a results/ directory for evaluation metrics, and models/ for PyTorch checkpoints (for example final_model.pth).
- Scenario comparison results/: holds the final output of notebook 4 with CSV summaries and directional rankings.

To add a new scenario, replicate the layout: create a folder named Network with <control name>/, include the three SUMO files (sumocfg, net.xml, rou.xml), add an empty results/ subfolder, and, if needed, a models/ subfolder for agent weights. The notebooks resolve paths through `BASE_DIR` and expect each scenario folder at the project root.

## Quick start
1. Install SUMO and set the `SUMO_HOME` environment variable to the SUMO installation directory.
2. Open the desired notebook, verify the paths inside the configuration cells, and execute the sections in the recommended order.
3. After the simulation, review outputs in Scenario comparison results/ or the reports stored in the respective results/ folders to compare performance.

## Supporting scripts
The Final function to run/ folder offers ready-to-use scripts (run_rl_simulation.py, quickstart.py, START_HERE.py) for running the simulations without notebooks while keeping the same scenario-folder conventions.