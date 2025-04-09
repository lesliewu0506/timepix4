import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def PlotHistogram(df:pd.DataFrame = None, filepath:str = None):
    if filepath is not None:
        df = pd.read_csv(filepath)

    df.loc[df['charge'] > 25, 'charge'] = np.nan

    ax = df.hist(column = "charge", bins = 240, grid = False, figsize = (10, 7), color = "blue", alpha = 0.7)

    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    plt.xlim(0, 20)

    vlines = [
        {"x": 2.225, "color": "red",    "label": "8.01 keV"},
        {"x": 3.861, "color": "green",  "label": "13.9 keV"},
        {"x": 4.917, "color": "blue",   "label": "17.7 keV"},
        {"x": 5.75,  "color": "magenta","label": "20.7 keV"},
        {"x": 7.306, "color": "cyan",   "label": "26.3 keV"},
        {"x": 16.5,  "color": "orange", "label": "59.5 keV"},
    ]
    for line in vlines:
        plt.axvline(x=line["x"], color=line["color"], linestyle='--', label=line["label"])
    
    plt.legend()
    plt.title("N116 Manual Calibrated Charge Distribution")
    plt.grid(False)
    plt.savefig("N116_Charge_Distribution_Manual.png", dpi = 600)
    plt.show()

def PlotCompare(filepath_raw, filepath_manual):
    df_auto = pd.read_csv(f"Raw Charge Data/{filepath_raw}-Raw-Charge.csv")
    data_auto = df_auto["charge"].dropna()

    df_manual = pd.read_csv(f"Calibration Data/{filepath_manual}-Filtered.csv")
    
    df_manual.loc[df_manual["charge"] > 25, "charge"] = np.nan
    data_manual = df_manual["charge"].dropna()
    
    plt.hist(data_auto, bins=1600, alpha=0.6, label="Test Pulse Calibration", color="blue", density=True)
    plt.hist(data_manual, bins=160, alpha=0.6, label="Manual Calibration", color="orange", density=True)

    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    plt.xlim(0, 20)

    vlines = [
        {"x": 2.225, "color": "red",    "label": "8.01 keV"},
        {"x": 3.861, "color": "green",  "label": "13.9 keV"},
        {"x": 4.917, "color": "blue",   "label": "17.7 keV"},
        {"x": 5.75,  "color": "magenta","label": "20.7 keV"},
        {"x": 7.306, "color": "cyan",   "label": "26.3 keV"},
        {"x": 16.5,  "color": "orange", "label": "59.5 keV"},
    ]
    for line in vlines:
        plt.axvline(x=line["x"], color=line["color"], linestyle='--', label=line["label"])
    
    plt.title("Charge Distribution N10")
    plt.grid(False)
    plt.legend()
    plt.savefig("N10_Charge_Distribution_ManualvsAuto.png", dpi = 600)
    plt.show()

if __name__ == "__main__":
    # filepath = "N116-250403-150114-filtered.csv" 
    # filepath = "N116-250408-123554.csv"

    PlotCompare("N10-250409-113850", "N10-250409-113850")
