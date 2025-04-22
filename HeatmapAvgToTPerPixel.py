import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def LoadCSV(filepath):
    df = pd.read_csv(filepath, usecols=["nhits", "col", "row", "tot"])
    df_filtered = df[df["nhits"] == 1].copy()

    df_filtered["col"] = df_filtered["col"].str.strip("[]").astype(int)
    df_filtered["row"] = df_filtered["row"].str.strip("[]").astype(int)
    df_filtered["tot"] = df_filtered["tot"].str.strip("[]").astype(float)
    df_filtered["pixel"] = list(zip(df_filtered["col"], df_filtered["row"]))
    return df_filtered


def LoadFitCSV(filepath):
    df = pd.read_csv(
        f"Data/Charge Calibrations/{filepath}_charge.txt",
        delim_whitespace=True,
        header=None,
        skiprows=15,
    )
    df.columns = [
        "Col",
        "Row",
        "p0",
        "p1",
        "p2",
        "p3",
        "p0_err",
        "p1_err",
        "p2_err",
        "p3_err",
        "red_chi2",
        "valid",
    ]
    return df


def LoadCleanCSV(filepath):

    df = pd.read_csv(filepath, usecols=["col", "row", "tot"])
    df["pixel"] = list(zip(df["col"], df["row"]))
    return df


def CalulcateAvgToTPerPixel(df: pd.DataFrame):
    avg_tot_per_pixel = df.groupby("pixel")["tot"].mean().reset_index()
    avg_tot_per_pixel["col"] = avg_tot_per_pixel["pixel"].apply(lambda x: x[0])
    avg_tot_per_pixel["row"] = avg_tot_per_pixel["pixel"].apply(lambda x: x[1])
    avg_tot_per_pixel.drop(columns=["pixel"], inplace=True)
    return avg_tot_per_pixel


def PlotAvgToTHeatmap(filepath):
    sensor = filepath.split("-")[0]
    df = LoadCleanCSV(f"Data/Filtered Calibration Data/{filepath}-Charge-Data.csv")
    avg_tot_per_pixel = CalulcateAvgToTPerPixel(df)
    heatmap_data = avg_tot_per_pixel.pivot(index="row", columns="col", values="tot")
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        heatmap_data,
        cmap="viridis",
        cbar_kws={"label": "Average ToT"},
        vmin=15,
        vmax=60,
    )
    plt.title(f"{sensor} Average ToT per Pixel", fontsize=16)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(f"{sensor}_AvgToT_Heatmap.png", dpi=600)
    plt.show()


def PlotAvgToTAndFitHeatmaps(filepath):
    sensor = filepath.split("-")[0]

    tot_df = LoadCleanCSV(f"Data/Filtered Calibration Data/{filepath}-Filtered.csv")
    # tot_df = LoadCleanCSV(f"Data/Filtered Calibration Data/{filepath}-Charge-Data.csv")
    fit_df = LoadFitCSV(sensor)
    avg_tot = CalulcateAvgToTPerPixel(tot_df)

    heatmap_data_ToT = avg_tot.pivot(index="row", columns="col", values="tot")
    heatmap_data_p1 = fit_df.pivot(index="Row", columns="Col", values="p1")
    # (
    #     fig,
    #     axes,
    # ) = plt.subplots(1, 2, figsize=(24, 10))
    # axes.flatten()

    # fig.suptitle(f"{sensor} Average ToT and Fit p1 per Pixel", fontsize=18)

    # sns.heatmap(
    #     heatmap_data_ToT,
    #     cmap="viridis",
    #     cbar_kws={"label": "Average ToT"},
    #     # vmin=15,
    #     # vmax=60,
    #     ax=axes[0],
    # )
    # sns.heatmap(
    #     heatmap_data_p1,
    #     cmap="viridis",
    #     cbar_kws={"label": "p1"},
    #     # vmin=0.65,
    #     # vmax=2.5,
    #     ax=axes[1],
    # )

    # axes[0].set_title("Average ToT per Pixel", fontsize=16)
    # axes[0].set_xlabel("")
    # axes[0].set_ylabel("")
    # axes[0].set_xticks([])
    # axes[0].set_yticks([])

    # axes[1].set_title("Fit p1 per Pixel", fontsize=16)
    # axes[1].set_xlabel("")
    # axes[1].set_ylabel("")
    # axes[1].set_xticks([])
    # axes[1].set_yticks([])

    # plt.tight_layout()
    # # plt.savefig(f"{sensor}_AvgToT_Fit_p1_Heatmaps.png", dpi=600)
    # plt.show()

    divided = heatmap_data_ToT/ heatmap_data_p1
    divided = divided.fillna(0)
    divided = divided.replace([float("inf"), -float("inf")], 0)
    # Select subregion from row 60 to 70 and col 350 to 360
    # divided = divided.loc[360:370, 70:80]
    sns.heatmap(
        divided,
        cmap="viridis",
        cbar_kws={"label": "Avg ToT / Fit p1"},
        vmin=20,
        vmax=30,
        # robust=True,
    )
    plt.title(f"Avg ToT / Fit p1 perx§ Pixel", fontsize=16)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(f"{sensor}_AvgToT_Fit_p1_divided_Heatmap.png", dpi=600)
    plt.show()

if __name__ == "__main__":
    # filepath = "N116-250403-150114-Filtered.csv"
    # filepath = "N10-250404-143700-Filtered.csv"
    # df = LoadCleanCSV(f"Data/Filtered Calibration Data/{filepath}")
    # avg_tot_per_pixel = CalulcateAvgToTPerPixel(df)
    # PlotAvgToTHeatmap(avg_tot_per_pixel)
    # PlotAvgToTAndFitHeatmaps(filepath, "Charge Calibrations/N116_charge.txt")
    # filepaths = ["N10-250404-143700", "N116-250403-150114"]
    # filepath2 = ["N112-250411-101613", "N113-250408-100406"]
    # for filepath in filepath2:
    #     # PlotAvgToTAndFitHeatmaps(filepath)
    #     PlotAvgToTHeatmap(filepath)
    PlotAvgToTAndFitHeatmaps("N116")
    # PlotAvgToTAndFitHeatmaps("N116-250403-150114")