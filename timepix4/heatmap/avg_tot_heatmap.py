import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def PlotAvgToTHeatmap(filepath: str) -> None:
    sensor = filepath.split("/")[-1].split("-")[0]
    df = _LoadCSV(filepath)
    avg_tot_per_pixel = _CalulcateAvgToTPerPixel(df)
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


def PlotAvgToTAndFitHeatmaps(
    tot_data_path: str, fit_data_path: str, parameter: str = "p1"
) -> None:
    sensor = tot_data_path.split("/")[-1].split("-")[0]

    tot_df = _LoadCSV(tot_data_path)
    avg_tot = _CalulcateAvgToTPerPixel(tot_df)
    fit_df = LoadFitCSV(fit_data_path, parameter)

    heatmap_data_ToT = avg_tot.pivot(index="row", columns="col", values="tot")
    heatmap_data_fit_param = fit_df.pivot(index="Row", columns="Col", values=parameter)

    divided = heatmap_data_ToT / heatmap_data_fit_param
    divided = divided.fillna(0)
    divided = divided.replace([float("inf"), -float("inf")], 0)

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        divided,
        cmap="viridis",
        cbar_kws={"label": f"Avg ToT / Fit {parameter}"},
        vmin=20,
        vmax=30,
    )
    plt.title(f"Avg ToT / Fit {parameter} per Pixel", fontsize=16)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(f"{sensor}_AvgToT_Fit_{parameter}_Heatmap.png", dpi=600)
    plt.show()


def _LoadCSV(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, usecols=["col", "row", "tot"])
    df["pixel"] = list(zip(df["col"], df["row"]))
    return df


def LoadFitCSV(filepath: str, parameter: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, usecols=["Col", "Row", parameter])
    return df


def _CalulcateAvgToTPerPixel(df: pd.DataFrame) -> pd.DataFrame:
    avg_tot_per_pixel = df.groupby("pixel")["tot"].mean().reset_index()
    avg_tot_per_pixel["col"] = avg_tot_per_pixel["pixel"].apply(lambda x: x[0])
    avg_tot_per_pixel["row"] = avg_tot_per_pixel["pixel"].apply(lambda x: x[1])
    avg_tot_per_pixel.drop(columns=["pixel"], inplace=True)
    return avg_tot_per_pixel
