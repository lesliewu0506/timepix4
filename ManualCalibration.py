import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def LoadCSV(filepath):
    df = pd.read_csv(filepath, usecols=["nhits", "col", "row", "tot"])
    df_filtered = df[df["nhits"] == 1].copy()

    df_filtered["col"] = df_filtered["col"].str.strip("[]").astype(int)
    df_filtered["row"] = df_filtered["row"].str.strip("[]").astype(int)
    df_filtered["tot"] = df_filtered["tot"].str.strip("[]").astype(float)
    df_filtered["pixel"] = list(zip(df_filtered["col"], df_filtered["row"]))
    return df_filtered

def FindHighestToT(df, target_col, target_row):
    # Filter for pixel
    pixel_df = df[(df['col'] == target_col) & (df['row'] == target_row)]

    if pixel_df.empty:
        return None

    counts, bin_edges = np.histogram(pixel_df['tot'], bins=301)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Can be higher than 100
    mask = bin_centers > 100
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
        df.to_csv("N10-filtered.csv", index = False)
    
    return df

def PlotHistogram(df:pd.DataFrame = None, filepath:str = None):
    if filepath is not None:
        df = pd.read_csv(filepath)

    df.loc[df['charge'] > 25, 'charge'] = np.nan

    ax = df.hist(column = "charge", bins = 80, grid = False, figsize = (10, 7), color = "blue", alpha = 0.7)
    plt.xlabel("Charge (ke)")
    plt.ylabel("Counts")
    plt.xlim(0, 20)
    plt.title("Charge Distribution")
    plt.grid(False)
    # plt.savefig("charge_histogram.png")
    plt.show()

def main(filepath):
    df = LoadCSV(filepath)
    GetCalibrationFactors(df)
    df = CalculateCharge(df, save = True)
    PlotHistogram(df = df)

if __name__ == "__main__":
    # filepath = "N116-250403-150114-filtered.csv" 
    filepath = "N10-filtered.csv"
    # main(filepath)
    PlotHistogram(filepath=filepath)
