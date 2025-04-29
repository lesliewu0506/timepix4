import os, uproot, ast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

AttenuationVoltage = 3.5
ROW = 230
COL = 228


def parse_list(x):
    if isinstance(x, str):
        parsed = ast.literal_eval(x)
        if isinstance(parsed, (list, tuple)):
            return list(parsed)
        else:
            return [parsed]
    elif isinstance(x, (list, tuple)):
        return list(x)
    else:
        return [x]


def FilterAndUnwrap(df: pd.DataFrame) -> pd.DataFrame:
    for c in ["col", "row", "tot"]:
        df[c] = df[c].apply(parse_list)
    df["combined"] = df.apply(lambda r: list(zip(r["row"], r["col"], r["tot"])), axis=1)
    df_exploded = df.explode("combined")

    df_exploded[["row", "col", "tot"]] = pd.DataFrame(
        df_exploded["combined"].tolist(), index=df_exploded.index
    )
    df_exploded = df_exploded.drop(columns=["combined"])
    return df_exploded

def FilterAndUnwrap2(df: pd.DataFrame) -> pd.DataFrame:
    for c in ["col", "row", "cltot"]:
        df[c] = df[c].apply(parse_list)
    df["combined"] = df.apply(lambda r: list(zip(r["row"], r["col"], r["cltot"])), axis=1)
    df_exploded = df.explode("combined")

    df_exploded[["row", "col", "cltot"]] = pd.DataFrame(
        df_exploded["combined"].tolist(), index=df_exploded.index
    )
    df_exploded = df_exploded.drop(columns=["combined"])
    return df_exploded

def process_folder(folder_path: str):
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

    arrays_1 = tree.arrays(["col", "row", "cltot"], library="pd")
    print(arrays_1)
    df = pd.DataFrame(
        {
            "col": arrays_1["col"].tolist(),
            "row": arrays_1["row"].tolist(),
            "cltot": arrays_1["cltot"].tolist(),
        }
    )
    df_cl_exp = FilterAndUnwrap2(df)
    df_cl = df_cl_exp[(df_cl_exp["row"] == ROW) & (df_cl_exp["col"] == COL)]

    mean_cl = df_cl["cltot"].mean()
    std_cl = df_cl["cltot"].std()

    arrays = tree.arrays(["col", "row", "tot"], library="pd")
    # df_data = pd.DataFrame(
    #     {
    #         "col": arrays["col"].to_numpy(),
    #         "row": arrays["row"].to_numpy(),
    #         "tot": arrays["tot"].to_numpy(),
    #     }
    # )
    df_data = pd.DataFrame(
        {
            "col": arrays["col"].tolist(),
            "row": arrays["row"].tolist(),
            "tot": arrays["tot"].tolist(),
        }
    )

    # Compute average cluster size per event
    sizes = arrays["col"].apply(lambda x: len(x))
    std_cs = sizes.std()
    mean_cs = sizes.mean()

    df_exp = FilterAndUnwrap(df_data)
    df_mean = df_exp.groupby(["row", "col"])["tot"].mean().reset_index()
    df_mean = df_mean.sort_values("tot", ascending=False)

    df_mean.to_csv(
        f"Data/ZFocus/ProcessedFocus {AttenuationVoltage} V/tot_{height_num}.csv",
        index=False,
    )
    # Determine max_tot for target pixel, or NaN if not present
    filtered = df_mean[(df_mean["row"] == ROW) & (df_mean["col"] == COL)]
    if not filtered.empty:
        max_tot = filtered["tot"].iloc[0]
    else:
        max_tot = np.nan
    ref_tot_series = df_exp[(df_exp["row"] == ROW) & (df_exp["col"] == COL)]["tot"]
    std_tot = ref_tot_series.std()
    return height_num2, mean_cl, std_cl, max_tot, std_tot, mean_cs, std_cs


def ZScanPlot():
    df = pd.read_csv(f"Data/ZFocus/ProcessedFocus {AttenuationVoltage} V/Results.csv")

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
    max_idx = df["max_tot"].idxmax()
    max_height = df.loc[max_idx, "height"]
    max_value = df.loc[max_idx, "max_tot"]
    ax.scatter(
        max_height,
        max_value,
        marker="o",
        color="red",
        s=100,
        label=f"Max ToT at z = {max_height} mm",
        zorder=3,
    )
    ax.set_xlabel("Z Position Stage [mm]")
    ax.set_ylabel("ToT [25ns]")
    ax.set_title(
        f"Mean clToT and ToT vs Z Position (Attenuation Voltage = {AttenuationVoltage} V; Pixel ({COL}, {ROW}))"
    )
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc="upper center")
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(f"ZScanPlot{AttenuationVoltage}.png", dpi=600)
    plt.show()


def ProcessFiles():
    data_root = f"Data/ZFocus/Focus {AttenuationVoltage} V"
    results = []
    for d in os.listdir(data_root):
        if d.startswith("focus_"):
            result = process_folder(os.path.join(data_root, d))
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
        f"Data/ZFocus/ProcessedFocus {AttenuationVoltage} V/Results.csv", index=False
    )

if __name__ == "__main__":
    ProcessFiles()
    ZScanPlot()
