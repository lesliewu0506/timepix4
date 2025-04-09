import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

THRESHOLDTOT = 150

def LoadCSV(filepath):
    df = pd.read_csv(filepath, usecols=["nhits", "col", "row", "tot"])
 

def FindHighestToT(df, target_col, target_row):
    # Filter for pixel
    pixel_df = df[(df['col'] == target_col) & (df['row'] == target_row)]

    if pixel_df.empty:
        return None

    counts, bin_edges = np.histogram(pixel_df['tot'], bins=301)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Can be higher than 100
    mask = bin_centers > THRESHOLDTOT
    filtered_counts = counts[mask]
    filtered_bins = bin_centers[mask]

    if len(filtered_bins) == 0:
        return None

    # Find Dominant Bin
    max_index = np.argmax(filtered_counts)
    dominant_bin_value = filtered_bins[max_index]

    return dominant_bin_value

def GetCalibrationFactors(df: pd.DataFrame):
    groups = df.groupby("pixel")

    global CorrectionFactors

    CorrectionFactors = {
        pixel: 16.5 / FindHighestToT(group, group["col"].iloc[0], group["row"].iloc[0])
        for pixel, group in groups
        if FindHighestToT(group, group["col"].iloc[0], group["row"].iloc[0]) is not None
    }

def CalculateCharge(df:pd.DataFrame, save: bool = False):
    df["correction"] = df["pixel"].apply(lambda pixel: CorrectionFactors.get(pixel, np.nan))
    df["charge"] = df["tot"] * df["correction"]
    
    if save:
        df.to_csv("N116-filtered.csv", index = False)
    
    return df

def PlotHistogram(df:pd.DataFrame = None, filepath:str = None):
    if filepath is not None:
        df = pd.read_csv(filepath)

    df.loc[df['charge'] > 25, 'charge'] = np.nan

    ax = df.hist(column = "charge", bins = 240, grid = False, figsize = (10, 7), color = "blue", alpha = 0.7)

    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    plt.xlim(0, 20)
    plt.title("N116 Manual Calibrated Charge Distribution")
    plt.grid(False)
    plt.savefig("N116_Charge_Distribution_Manual.png")
    plt.show()

def FilterNormalData(filepath):
    df = pd.read_csv(filepath, usecols = ["nhits", "charge"])
    df_filtered = df[df["nhits"] == 1].copy()

    df_filtered["charge"] = df_filtered["charge"].str.strip("[]").astype(float) / 1000

    return df_filtered

def PlotTwoToT(filepath1, filepath2):
    df_auto = FilterNormalData(filepath1)
    df_manual = pd.read_csv(filepath2)
    df_manual.loc[df_manual["charge"] > 25, "charge"] = np.nan
    data_auto = df_auto["charge"].dropna()
    data_manual = df_manual["charge"].dropna()
    
    # Plot beide in één histogram
    plt.hist(data_auto, bins=1600, alpha=0.6, label="Auto Calibration", color="blue", density=True)
    plt.hist(data_manual, bins=80, alpha=0.6, label="Manual Calibration", color="orange", density=True)

    plt.xlabel("Charge (ke)")
    plt.ylabel("Counts")
    plt.xlim(0, 20)
    plt.title("Charge Distribution N10")
    plt.grid(False)
    plt.legend()
    plt.savefig("N10_Charge_Distribution_ManualvsAuto.png", dpi = 600)
    plt.show()

def main(filepath):
    df = LoadCSV(filepath)
    GetCalibrationFactors(df)
    df = CalculateCharge(df, save = True)
    PlotHistogram(df = df)

if __name__ == "__main__":
    # filepath = "N116-250403-150114-filtered.csv" 
    # filepath = "N116-250408-123554.csv"
    # main(filepath)
    PlotHistogram(filepath = "N116-filtered.csv")
    # PlotTwoToT("N10-250404-143700_normal.csv", "N10-filtered.csv")
