import os, uproot, ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

    df_cl = pd.DataFrame(
        {"cltot": tree.arrays(["cltot"], library="pd")["cltot"].to_numpy()}
    )
    mean_cl = df_cl["cltot"].mean()

    arrays = tree.arrays(["col", "row", "tot"], library="pd")
    df_data = pd.DataFrame(
        {
            "col": arrays["col"].to_numpy(),
            "row": arrays["row"].to_numpy(),
            "tot": arrays["tot"].to_numpy(),
        }
    )
    df_exp = FilterAndUnwrap(df_data)
    df_mean = df_exp.groupby(["row", "col"])["tot"].mean().reset_index()
    df_mean = df_mean.sort_values("tot", ascending=False)

    df_mean.to_csv(
        f"Data/Focus/ProcessedFocus {AttenuationVoltage} V/tot_{height_num}.csv",
        index=False,
    )
    max_tot = df_mean[(df_mean["row"] == ROW) & (df_mean["col"] == COL)]["tot"].iloc[0]
    return height_num2, mean_cl, max_tot


def ZScanPlot():
    df = pd.read_csv(f"Data/Focus/ProcessedFocus {AttenuationVoltage} V/Results.csv")

    # Plot mean_cltot and max_tot vs height
    plt.figure(figsize=(10, 6))
    plt.plot(df["height"], df["mean_cltot"], marker="o", label="Mean cltot")
    plt.plot(df["height"], df["max_tot"], marker="o", label="Mean tot")
    # Highlight global maximum of max_tot
    max_idx = df["max_tot"].idxmax()
    max_height = df.loc[max_idx, "height"]
    max_value = df.loc[max_idx, "max_tot"]
    plt.scatter(
        max_height,
        max_value,
        marker="o",
        color="red",
        s=100,
        label=f"Max ToT at z = {max_height} mm",
        zorder=3,
    )
    plt.xlabel("Z Position Stage [mm]")
    plt.ylabel("ToT [25ns]")
    plt.title(
        f"Mean clToT and ToT vs Z Position (Attenuation Voltage = {AttenuationVoltage} V; Pixel ({COL}, {ROW}))"
    )
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"ZScanPlot{AttenuationVoltage}.png", dpi=600)
    plt.show()


def ProcessFiles():
    data_root = f"Data/Focus/Focus {AttenuationVoltage} V"
    results = []
    for d in os.listdir(data_root):
        if d.startswith("focus_"):
            result = process_folder(os.path.join(data_root, d))
            if result:
                results.append(result)
    # Write the aggregate cltot means for all heights
    df_results = pd.DataFrame(results, columns=["height", "mean_cltot", "max_tot"])
    df_results = df_results.sort_values("height")
    df_results.to_csv(
        f"Data/Focus/ProcessedFocus {AttenuationVoltage} V/Results.csv", index=False
    )


# def Hitmap():
#     # Determine center pixel (highest mean ToT)
#     center = mean_tots.loc[mean_tots["tot"].idxmax()]
#     center_row, center_col = int(center["row"]), int(center["col"])

#     # Define 5x5 neighborhood bounds
#     row_min, row_max = center_row - 3, center_row + 3
#     col_min, col_max = center_col - 3, center_col + 3

#     # Filter for the 5×5 area around center
#     mean_tots = mean_tots[
#         mean_tots["row"].between(row_min, row_max)
#         & mean_tots["col"].between(col_min, col_max)
#     ]
#     # Pivot only the 5×5 region
#     heatmap_data = mean_tots.pivot(index="row", columns="col", values="tot")
#     # Ensure a complete 5×5 grid and fill missing pixels with zero
#     rows = list(range(row_min, row_max + 1))
#     cols = list(range(col_min, col_max + 1))
#     heatmap_data = heatmap_data.reindex(index=rows, columns=cols, fill_value=np.nan)
#     plt.figure(figsize=(10, 8))
#     ax = sns.heatmap(
#         heatmap_data,
#         cmap="viridis",
#         cbar_kws={"label": "Charge [ke]"},
#         square=True,
#         annot=True,
#         annot_kws={"size": 18},
#         fmt=".2f",
#     )
#     ax.set_title(f"Charge [ke] per pixel with stage at (27.610/23.52/42.{z})")
#     plt.tight_layout()
#     plt.savefig(f"Focus at ({center_col}, {center_row}) 42.{z}.png", dpi=300)
#     plt.show()


if __name__ == "__main__":
    ProcessFiles()
    ZScanPlot()
