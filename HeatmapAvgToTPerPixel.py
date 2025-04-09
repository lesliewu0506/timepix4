import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def LoadCSV(filepath):
    df = pd.read_csv(filepath, usecols=["nhits", "col", "row", "tot"])
    df_filtered = df[df["nhits"] == 1].copy()

    df_filtered["col"] = df_filtered["col"].str.strip("[]").astype(int)
    df_filtered["row"] = df_filtered["row"].str.strip("[]").astype(int)
    df_filtered["tot"] = df_filtered["tot"].str.strip("[]").astype(float)
    df_filtered["pixel"] = list(zip(df_filtered["col"], df_filtered["row"]))
    return df_filtered

def LoadFitCSV(filepath):
    df = pd.read_csv(filepath, delim_whitespace=True, header=None, skiprows=15)
    df.columns = ["Col", "Row", "p0", "p1", "p2", "p3", "p0_err", "p1_err", "p2_err", "p3_err", "red_chi2", "valid"]
    return df

def LoadCleanCSV(filepath):
    df = pd.read_csv(filepath, usecols=["nhits", "col", "row", "tot"])
    df["pixel"] = list(zip(df["col"], df["row"]))
    return df

def CalulcateAvgToTPerPixel(df: pd.DataFrame):
    avg_tot_per_pixel = df.groupby("pixel")["tot"].mean().reset_index()
    avg_tot_per_pixel["col"] = avg_tot_per_pixel["pixel"].apply(lambda x: x[0])
    avg_tot_per_pixel["row"] = avg_tot_per_pixel["pixel"].apply(lambda x: x[1])
    avg_tot_per_pixel.drop(columns=["pixel"], inplace=True)
    return avg_tot_per_pixel

def PlotAvgToTHeatmap(df: pd.DataFrame):
    heatmap_data = df.pivot(index="row", columns="col", values="tot")
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, cmap="viridis", cbar_kws={"label": "Average ToT"}, vmax = 60)
    plt.title("Average ToT per Pixel", fontsize=16)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()

def PlotAvgToTAndFitHeatmaps(avg_tot_filepath, fit_filepath):
    tot_df = LoadCleanCSV(avg_tot_filepath)
    fit_df = LoadFitCSV(fit_filepath)
    avg_tot = CalulcateAvgToTPerPixel(tot_df)

    heatmap_data_ToT = avg_tot.pivot(index="row", columns="col", values="tot")
    heatmap_data_p1 = fit_df.pivot(index="Row", columns="Col", values="p1")
    fig, axes, = plt.subplots(1, 2, figsize=(24, 10))
    axes.flatten()

    fig.suptitle("N116 Average ToT and Fit p1 per Pixel", fontsize=18)

    sns.heatmap(heatmap_data_ToT, cmap="viridis", cbar_kws={"label": "Average ToT"}, vmin = 15, vmax = 60, ax = axes[0])
    sns.heatmap(heatmap_data_p1, cmap="viridis", cbar_kws={"label": "p1"}, vmin = 0.65, vmax = 2.5, ax = axes[1])

    axes[0].set_title("Average ToT per Pixel", fontsize=16)
    axes[0].set_xlabel("")
    axes[0].set_ylabel("")
    axes[0].set_xticks([])
    axes[0].set_yticks([])

    axes[1].set_title("Fit p1 per Pixel", fontsize=16)
    axes[1].set_xlabel("")
    axes[1].set_ylabel("")
    axes[1].set_xticks([])
    axes[1].set_yticks([])

    plt.tight_layout()
    plt.savefig("N116_AvgToT_Fit_p1_Heatmaps.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    filepath = "N116-filtered.csv"
    # df = LoadCleanCSV(filepath)
    # avg_tot_per_pixel = CalulcateAvgToTPerPixel(df)
    # PlotAvgToTHeatmap(avg_tot_per_pixel)
    PlotAvgToTAndFitHeatmaps(filepath, "Charge Calibrations/N116_charge.txt")