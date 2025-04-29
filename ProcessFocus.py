import os, uproot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from HelperFunctions import parse_list

AttenuationVoltage = 3.6
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
        mask = (df_exp["row"].isin([ROW, ROW + 1, ROW - 1, ROW - 2, ROW + 2])) & (
            df_exp["col"] == COL
        )
        df_filtered_cl_cs = df_exp[mask].copy()
        df_row_next = df_exp[(df_exp["row"] == ROW + 1) & (df_exp["col"] == COL)].copy()
        df_row_prev = df_exp[(df_exp["row"] == ROW - 1) & (df_exp["col"] == COL)].copy()
        df_mean_next_under = df_row_next[df_row_next["tot"] < LIMIT]
        df_mean_next_in = df_mean_next_under[df_mean_next_under["tot"] > 0]
        df_mean_next = df_mean_next_in.groupby(["row", "col"]).mean().reset_index()
        df_mean_next = df_mean_next.sort_values("tot", ascending=False)

        df_mean_prev_under = df_row_prev[df_row_prev["tot"] < LIMIT]
        df_mean_prev_in = df_mean_prev_under[df_mean_prev_under["tot"] > 0]
        df_mean_prev = df_mean_prev_in.groupby(["row", "col"]).mean().reset_index()
        df_mean_prev = df_mean_prev.sort_values("tot", ascending=False)

        std_tot_next = df_row_next["tot"].std()
        std_tot_prev = df_row_prev["tot"].std()

        if not df_mean_next.empty:
            max_tot_next = df_mean_next["tot"].iloc[0]
        else:
            max_tot_next = 0
        if not df_mean_prev.empty:
            max_tot_prev = df_mean_prev["tot"].iloc[0]
        else:
            max_tot_prev = 0

    elif r == "y":
        # Include the target pixel and its immediate neighbors in the column direction
        mask = (df_exp["col"].isin([COL, COL + 1, COL - 1, COL - 2, COL + 2])) & (
            df_exp["row"] == ROW
        )
        df_filtered_cl_cs = df_exp[mask].copy()
        df_col_next = df_exp[(df_exp["row"] == ROW) & (df_exp["col"] == COL + 1)].copy()
        df_col_prev = df_exp[(df_exp["row"] == ROW) & (df_exp["col"] == COL - 1)].copy()
        df_mean_next_under = df_col_next[df_col_next["tot"] < LIMIT]
        df_mean_next_in = df_mean_next_under[df_mean_next_under["tot"] > 0]
        df_mean_next = df_mean_next_in.groupby(["row", "col"]).mean().reset_index()
        df_mean_next = df_mean_next.sort_values("tot", ascending=False)
        df_mean_prev_under = df_col_prev[df_col_prev["tot"] < LIMIT]
        df_mean_prev_in = df_mean_prev_under[df_mean_prev_under["tot"] > 0]
        df_mean_prev = df_mean_prev_in.groupby(["row", "col"]).mean().reset_index()
        df_mean_prev = df_mean_prev.sort_values("tot", ascending=False)

        std_tot_next = df_col_next["tot"].std()
        std_tot_prev = df_col_prev["tot"].std()
        if not df_mean_next.empty:
            max_tot_next = df_mean_next["tot"].iloc[0]
        else:
            max_tot_next = 0

        if not df_mean_prev.empty:
            max_tot_prev = df_mean_prev["tot"].iloc[0]
        else:
            max_tot_prev = 0

    else:
        df_filtered_cl_cs = df_filtered.copy()
        max_tot_next = 0
        max_tot_prev = 0
        std_tot_next = 0
        std_tot_prev = 0

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
    df_mean = df_mean.sort_values("tot", ascending=False)

    df_mean.to_csv(
        f"Data/Focus/{r.capitalize()}/ProcessedFocus {AttenuationVoltage} V/tot_{height_num}.csv",
        index=False,
    )
    # Determine max_tot for target pixel, or NaN if not present
    if not df_filtered.empty and not df_mean.empty:
        max_tot = df_mean["tot"].iloc[0]
    else:
        max_tot = 0

    ref_tot_series = df_filtered["tot"]
    std_tot = ref_tot_series.std()
    return (
        height_num2,
        mean_cl,
        std_cl,
        max_tot,
        std_tot,
        mean_cs,
        std_cs,
        max_tot_next,
        max_tot_prev,
        std_tot_next,
        std_tot_prev,
    )


def ZScanPlot(r: str):
    df = pd.read_csv(
        f"Data/Focus/{r.capitalize()}/ProcessedFocus {AttenuationVoltage} V/Results.csv"
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
        label="Mean clToT",
    )
    ax.errorbar(
        df["height"],
        df["max_tot"],
        yerr=df["std_tottarget"],
        marker="o",
        linestyle="-",
        capsize=5,
        label=f"Mean ToT ({COL}, {ROW})",
    )
    if r == "x":
        ax.errorbar(
            df["height"],
            df["max_tot_prev"],
            yerr=df["std_tot_prev"],
            marker="o",
            linestyle="-",
            capsize=5,
            label=f"Mean ToT ({COL}, {ROW - 1})",
        )
        ax.errorbar(
            df["height"],
            df["max_tot_next"],
            yerr=df["std_tot_next"],
            marker="o",
            linestyle="-",
            capsize=5,
            label=f"Mean ToT ({COL}, {ROW + 1})",
        )
    elif r == "y":
        ax.errorbar(
            df["height"],
            df["max_tot_prev"],
            yerr=df["std_tot_prev"],
            marker="o",
            linestyle="-",
            capsize=5,
            label=f"Mean ToT ({COL - 1}, {ROW})",
        )
        ax.errorbar(
            df["height"],
            df["max_tot_next"],
            yerr=df["std_tot_next"],
            marker="o",
            linestyle="-",
            capsize=5,
            label=f"Mean ToT ({COL + 1}, {ROW})",
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
    # fix right axis limits and align tick count with dynamic left ToT limits
    ax2.set_ylim(0, 8)
    if r == "z":
        ax2.set_ylim(0, 8)
        # determine number of ticks on cluster size axis
        num_ticks = len(ax2.get_yticks())
        # dynamic ToT axis limits rounded to nearest 100
        all_tot = np.hstack([df["mean_cltot"].values, df["max_tot"].values])
        min_lim = np.floor(all_tot.min() / 100) * 100
        max_lim = np.ceil(all_tot.max() / 100) * 100
        # generate matching tick positions
        left_ticks = np.linspace(min_lim, max_lim, num_ticks)
        ax.set_ylim(min_lim, max_lim)
        ax.set_yticks(left_ticks)
        ax2.set_yticks(np.linspace(1, 9, num_ticks))
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
        f"{r.capitalize()} Scan: Attenuation Voltage = {AttenuationVoltage} V; Pixel ({COL}, {ROW})"
    )
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc="best")
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(f"{r.capitalize()}ScanPlot{AttenuationVoltage}.png", dpi=600)
    plt.show()


def ProcessFiles(r: str):
    data_root = (
        f"Data/Focus/{r.capitalize()}/{r.capitalize()}Focus {AttenuationVoltage} V"
    )
    results = []
    output_dir = f"Data/Focus/{r.capitalize()}/ProcessedFocus {AttenuationVoltage} V"
    os.makedirs(output_dir, exist_ok=True)
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
            "max_tot_next",
            "max_tot_prev",
            "std_tot_next",
            "std_tot_prev",
        ],
    )
    df_results = df_results.sort_values("height")
    df_results.to_csv(
        f"Data/Focus/{r.capitalize()}/ProcessedFocus {AttenuationVoltage} V/Results.csv",
        index=False,
    )


if __name__ == "__main__":
    ProcessFiles("z")
    ZScanPlot("z")
