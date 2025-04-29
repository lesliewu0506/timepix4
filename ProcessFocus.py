import os, uproot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from HelperFunctions import parse_list

AttenuationVoltage = 3.5
ROW = 230
COL = 228
LIMIT = 1000


def FilterAndUnwrap(df: pd.DataFrame) -> pd.DataFrame:
    for c in ["col", "row", "tot", "cltot", "nhits"]:
        df[c] = df[c].apply(parse_list)

    df["combined"] = df.apply(
        lambda r: list(zip(r["row"], r["col"], r["tot"], r["cltot"], r["nhits"])),
        axis=1,
    )
    df_exploded = df.explode("combined")

    df_exploded[["row", "col", "tot", "cltot", "nhits"]] = pd.DataFrame(
        df_exploded["combined"].tolist(), index=df_exploded.index
    )
    df_exploded = df_exploded.drop(columns=["combined"])

    return df_exploded


def process_folder(folder_path: str, r: str):
    basename = os.path.basename(folder_path)
    height_str = basename.split("_", 1)[1]
    height_num = height_str.replace("p", "_")
    height_num2 = height_str.replace("p", ".")

    root_files = [f for f in os.listdir(folder_path) if f.endswith(".root")]
    if not root_files:
        print(f"No root file in {folder_path}, skipping")
        return
    root_file = os.path.join(folder_path, root_files[0])

    file = uproot.open(root_file)
    tree = file["clusterTree"]

    arrays = tree.arrays(["col", "row", "tot", "cltot", "nhits"], library="pd")
    df_data = pd.DataFrame(
        {
            "col": arrays["col"].tolist(),
            "row": arrays["row"].tolist(),
            "tot": arrays["tot"].tolist(),
            "cltot": arrays["cltot"].tolist(),
            "nhits": arrays["nhits"].tolist(),
        }
    )
    df_exp = FilterAndUnwrap(df_data)
    df_filtered = df_exp[(df_exp["row"] == ROW) & (df_exp["col"] == COL)].copy()

    if r == "x":
        # Include the target pixel and its immediate neighbors in the row direction
        mask = (
            df_exp["row"].isin([ROW, ROW + 1, ROW - 1])
        ) & (df_exp["col"] == COL)
        df_filtered_cl_cs = df_exp[mask].copy()
    elif r == "y":
        # Include the target pixel and its immediate neighbors in the column direction
        mask = (
            df_exp["col"].isin([COL, COL + 1, COL - 1])
        ) & (df_exp["row"] == ROW)
        df_filtered_cl_cs = df_exp[mask].copy()
    else:
        df_filtered_cl_cs = df_filtered.copy()

    df_cl_under_limit = df_filtered_cl_cs[df_filtered_cl_cs["cltot"] < LIMIT]
    mean_cl = df_cl_under_limit["cltot"].mean()
    std_cl = df_cl_under_limit["cltot"].std()

    # Compute average cluster size per event
    sizes = df_filtered_cl_cs["nhits"]
    std_cs = sizes.std()
    mean_cs = sizes.mean()

    # Filter out any ToT values above the limit, then compute mean per pixel
    df_under_limit = df_filtered[df_filtered["tot"] < LIMIT]
    df_in_limit = df_under_limit[df_under_limit["tot"] > 0]
    df_mean = df_in_limit.groupby(["row", "col"]).mean().reset_index()
    # Sort by ToT descending if desired
    df_mean = df_mean.sort_values("tot", ascending=False)

    df_mean.to_csv(
        f"Data/{r.capitalize()}Focus/ProcessedFocus {AttenuationVoltage} V/tot_{height_num}.csv",
        index=False,
    )
    # Determine max_tot for target pixel, or NaN if not present
    if not df_filtered.empty:
        max_tot = df_mean["tot"].iloc[0]
    else:
        max_tot = 0

    ref_tot_series = df_filtered["tot"]
    std_tot = ref_tot_series.std()
    return height_num2, mean_cl, std_cl, max_tot, std_tot, mean_cs, std_cs


def ZScanPlot(r: str):
    df = pd.read_csv(
        f"Data/{r.capitalize()}Focus/ProcessedFocus {AttenuationVoltage} V/Results.csv"
    )

    fig, ax = plt.subplots(figsize=(12, 8))
    ax2 = ax.twinx()

    # Plot mean_cltot and max_tot vs height
    ax.errorbar(
        df["height"],
        df["mean_cltot"],
        yerr=df["std_cltot"],
        marker="o",
        linestyle="-",
        capsize=5,
        label="Mean cltot",
    )
    ax.errorbar(
        df["height"],
        df["max_tot"],
        yerr=df["std_tottarget"],
        marker="o",
        linestyle="-",
        capsize=5,
        label="Mean tot",
    )
    ax2.errorbar(
        df["height"],
        df["mean_clustersize"],
        yerr=df["std_clustersize"],
        marker="s",
        linestyle="None",
        capsize=5,
        color="green",
        label="Mean cluster size",
    )
    ax2.set_ylabel("Mean cluster size [pixels]")

    # Highlight global maximum of max_tot
    # max_idx = df["max_tot"].idxmax()
    # max_height = df.loc[max_idx, "height"]
    # max_value = df.loc[max_idx, "max_tot"]
    # ax.scatter(
    #     max_height,
    #     max_value,
    #     marker="o",
    #     color="red",
    #     s=100,
    #     label=f"Max ToT at {r} = {max_height} mm",
    #     zorder=3,
    # )
    ax.set_xlabel(f"{r.capitalize()} Position Stage [mm]")
    ax.set_ylabel("ToT [25ns]")
    ax.set_title(
        f"Mean clToT and ToT vs {r.capitalize()} Position (Attenuation Voltage = {AttenuationVoltage} V; Pixel ({COL}, {ROW}))"
    )
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc="upper center")
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(f"{r.capitalize()}ScanPlot{AttenuationVoltage}.png", dpi=600)
    plt.show()


def ProcessFiles(r: str):
    data_root = f"Data/{r.capitalize()}Focus/Focus {AttenuationVoltage} V"
    results = []
    for d in os.listdir(data_root):
        if d.startswith("focus_"):
            result = process_folder(os.path.join(data_root, d), r)
            if result:
                results.append(result)
    # Write the aggregate cltot means for all heights
    df_results = pd.DataFrame(
        results,
        columns=[
            "height",
            "mean_cltot",
            "std_cltot",
            "max_tot",
            "std_tottarget",
            "mean_clustersize",
            "std_clustersize",
        ],
    )
    df_results = df_results.sort_values("height")
    df_results.to_csv(
        f"Data/{r.capitalize()}Focus/ProcessedFocus {AttenuationVoltage} V/Results.csv",
        index=False,
    )


if __name__ == "__main__":
    ProcessFiles("z")
    ZScanPlot("z")
