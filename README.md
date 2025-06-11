# timepix4

Main Repository for Timepix4 Detector Data Analysis

---

## Overview

This repository contains a suite of Python scripts and a helper module for processing, analyzing, and visualizing data acquired with the Timepix4 pixel detector.  You’ll find tools for:

- Converting ROOT files into CSV format for further analysis
- Calibrating and measuring laser scans 
- Generating heatmaps and ToT distributions

---

## Repository Structure
```python
├── Convert.py               # Convert ROOT to CSV
├── Focus.py                 # Analyze focus scans
├── Heatmaps.py              # Generate pixel heatmaps
├── LaserMeasurements.py     # Analyze data from laser measurements
├── LaserPower.py            # Analyze laser power
├── LeakageCurrent.py        # Plot leakage current vs. bias voltage
├── ManualCalibration.py     # Manually fit calibration parameters
├── TestPulseAnalysis.py     # Analyze test-pulse response
├── ToTPlotter.py            # Plot ToT distributions
└── timepix4/                # Shared Python module (loader, utilities, classes)
```