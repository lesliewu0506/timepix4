import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def Plotter(FolderPath: str) -> None:
    global ref_map
    ref_map = _LoadDict()

    CSVFilePaths = sorted(
        [
            os.path.join(FolderPath, File)
            for File in os.listdir(FolderPath)
            if File.endswith(".csv")
        ]
    )

    dfs = []
    for Filepath in CSVFilePaths:
        voltage = float(Filepath.split("/")[-1].split(" ")[0])
        df = pd.read_csv(Filepath)
        df["voltage"] = voltage
        dfs.append(df)

    pixel_sets = [set(df.set_index(["col", "row"]).index) for df in dfs]
    common_pixels = pixel_sets[-2].intersection(*pixel_sets[1:])
    common_pixels = common_pixels.intersection(ref_map.keys())
    common_pixels.discard((0, 0))
    all_data = pd.concat(dfs, ignore_index=True)
    all_data = all_data[
        all_data.apply(lambda r: (r.col, r.row) in common_pixels, axis=1)
    ]
    all_data["ref_tot"] = all_data.apply(_lookup_ref, axis=1)
    all_data["diff"] = (all_data["mean_tot"] - all_data["ref_tot"]).abs()

    idx = all_data.groupby(["col", "row"])["diff"].idxmin()
    winners = all_data.loc[idx]
    counts = winners["voltage"].value_counts().sort_index()

    voltage_levels = [3.650, 3.675, 3.700, 3.725, 3.750]
    for voltage in voltage_levels:
        if voltage not in counts.index:
            counts[voltage] = 0
    counts = counts.sort_index()
    # _PlotSinglePixel(all_data)
    plt.figure(figsize=(12, 8))
    voltages = counts.index.to_numpy()
    if len(voltages) > 1:
        spacing = voltages[1] - voltages[0]
    else:
        spacing = 0.025
    width = spacing * 0.8

    plt.bar(voltages, counts.values, width=width)
    plt.xlabel("Attenuation Voltage [V]", fontsize=18)
    plt.ylabel("Number of Pixels", fontsize=18)
    plt.xticks(np.arange(3.650, 3.750, 0.025),fontsize=16)
    plt.yticks(fontsize=16)
    plt.title(
        "Pixels with Minimal ToT Difference from Reference vs Attenuation Voltage",
        fontsize=20,
    )
    plt.tight_layout()
    plt.savefig(
        "plotter.png",
        dpi=600,
    )
    plt.show()


def _PlotSinglePixel(df: pd.DataFrame) -> None:
    _, ax = plt.subplots(figsize=(12, 8))
    df = df[(df["col"] == 228) & (df["row"] == 230)]
    ax.axhline(
        y=df["ref_tot"].mean(), color="red", linestyle="--", label="Reference ToT"
    )
    ax.errorbar(
        df["voltage"],
        df["mean_tot"],
        yerr=df["std_tot"],
        fmt="o",
        label="Mean ToT",
        color="blue",
        capsize=3,
    )
    ax.set_xlabel("Attenuation Voltage [V]", fontsize=18)
    ax.set_ylabel("ToT [25 ns]", fontsize=18)
    plt.xlim(3.640, 3.760)
    plt.ylim(120, 260)
    plt.xticks(np.arange(3.650, 3.750, 0.025),fontsize=16)
    plt.yticks(fontsize=16)
    plt.title(
        "Mean ToT vs Attenuation Voltage for Pixel (228, 230)",
        fontsize=20,
    )
    plt.legend(fontsize=16)
    plt.grid()
    plt.tight_layout()

    plt.savefig(
        "plotter_single_pixel.png",
        dpi=600,
    )
    plt.show()


def _LoadDict() -> dict[tuple[int, int], float]:
    df = pd.read_csv("timepix4/laser_calibration/LaserCalToT.csv")
    return df.set_index(["col", "row"])["ToT"].to_dict()


def _lookup_ref(row):
    return ref_map.get((row.col, row.row), pd.NA)
