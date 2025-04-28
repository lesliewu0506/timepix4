import uproot, ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from LoadCorrectionDict import createdicts
import os

z = 890


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
    # Parse each cell into a list
    for c in ["col", "row", "tot"]:
        df[c] = df[c].apply(parse_list)

    # Zip the three lists together so they explode in parallel
    df["combined"] = df.apply(lambda r: list(zip(r["row"], r["col"], r["tot"])), axis=1)
    df_exploded = df.explode("combined")

    # Unpack the tuples back into separate columns
    df_exploded[["row", "col", "tot"]] = pd.DataFrame(
        df_exploded["combined"].tolist(), index=df_exploded.index
    )
    df_exploded = df_exploded.drop(columns=["combined"])

    df_exploded.to_csv(f"Data/Focus/cluster42_{z}.csv", index=False)
    return df_exploded


def ConvertClusterData(filepath: str) -> None:
    # filename = filepath.split(".")[0]
    file = uproot.open(f"Data/Focus/{filepath}")
    tree = file["clusterTree"]

    arrays_data = tree.arrays(["col", "row", "tot"], library="pd")

    df_data = pd.DataFrame(
        {
            "col": arrays_data["col"].to_numpy(),
            "row": arrays_data["row"].to_numpy(),
            "tot": arrays_data["tot"].to_numpy(),
        }
    )

    df_filtered = FilterAndUnwrap(df_data)
    mean_tots = df_filtered.groupby(["row", "col"])["tot"].mean().reset_index()
    mean_tots["tot"] = mean_tots["tot"].astype(float) * 0.10437223461349657

    # Determine center pixel (highest mean ToT)
    center = mean_tots.loc[mean_tots["tot"].idxmax()]
    center_row, center_col = int(center["row"]), int(center["col"])

    # Define 5x5 neighborhood bounds
    row_min, row_max = center_row - 3, center_row + 3
    col_min, col_max = center_col - 3, center_col + 3

    # Filter for the 5×5 area around center
    mean_tots = mean_tots[
        mean_tots["row"].between(row_min, row_max)
        & mean_tots["col"].between(col_min, col_max)
    ]

    # Pivot only the 5×5 region
    heatmap_data = mean_tots.pivot(index="row", columns="col", values="tot")
    # Ensure a complete 5×5 grid and fill missing pixels with zero
    rows = list(range(row_min, row_max + 1))
    cols = list(range(col_min, col_max + 1))
    heatmap_data = heatmap_data.reindex(index=rows, columns=cols, fill_value=np.nan)
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(
        heatmap_data,
        cmap="viridis",
        cbar_kws={"label": "Charge [ke]"},
        square=True,
        annot=True,
        annot_kws={"size": 18},
        fmt=".2f",
    )
    ax.set_title(f"Charge [ke] per pixel with stage at (27.610/23.52/42.{z})")
    plt.tight_layout()
    plt.savefig(f"Focus at ({center_col}, {center_row}) 42.{z}.png", dpi=300)
    plt.show()


def ZScanPlot():
    # Automatically gather and sort all .root files in Data/Focus
    filepaths = sorted(
        [f for f in os.listdir("Data/Focus") if f.endswith(".root")]
    )
    CorrectionFactors = createdicts()
    tot_list = []
    cltot_list = []

    for filepath in filepaths:
        file = uproot.open(f"Data/Focus/{filepath}")
        tree = file["clusterTree"]

        arrays_data = tree.arrays(["cltot"], library="pd")

        df_cltot = pd.DataFrame(
            {
                "cltot": arrays_data["cltot"].to_numpy(),
            }
        )

        arrays_data_2 = tree.arrays(["col", "row", "tot"], library="pd")

        df_data = pd.DataFrame(
            {
                "col": arrays_data_2["col"].to_numpy(),
                "row": arrays_data_2["row"].to_numpy(),
                "tot": arrays_data_2["tot"].to_numpy(),
            }
        )

        df_filtered = FilterAndUnwrap(df_data)
        mean_tots = df_filtered.groupby(["row", "col"])["tot"].mean().reset_index()

        # Determine center pixel (highest mean ToT)
        center = mean_tots.loc[mean_tots["tot"].idxmax()]
        center_row, center_col = int(center["row"]), int(center["col"])

        df_cltot["cltot"] = (
            df_cltot["cltot"].astype(float)
            * CorrectionFactors[(center_col, center_row)]
        )
        mean_cltot = df_cltot["cltot"].mean()
        mean_tots["tot"] = (
            mean_tots["tot"].astype(float) * CorrectionFactors[(center_col, center_row)]
        )
        mean_tot = mean_tots["tot"].max()

        tot_list.append(mean_tot)
        cltot_list.append(mean_cltot)
    z_list = list(np.arange(42.340, 42.591, 0.025))
    z_list.extend([42.790, 42.190, 42.290, 42.890, 43.290])
    # Sort z positions together with their corresponding ToT lists
    combined = sorted(zip(z_list, tot_list, cltot_list))
    z_list, tot_list, cltot_list = map(list, zip(*combined))

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(z_list, tot_list, label="Charge", marker="o")
    plt.plot(z_list, cltot_list, label="Cluster Charge", marker="o")
    plt.xlabel("Z Position Stage [mm]")
    plt.ylabel("Charge [ke]")
    # plt.xticks(np.arange(42.165, 42.891, 0.05))
    plt.title("Z Scan Plot")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("ZScanPlot.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    # ConvertClusterData("N116-250425-111418.root")
    # ConvertClusterData("N116-250425-142003.root")
    # ConvertClusterData("N116-250425-153231.root")
    filepaths = [
        "N116-250425-4.root",
        "N116-250425-142003.root",
        "N116-250425-143945.root",
    ]
    # ZScanPlot("N116-250425-143945.root")
    ZScanPlot()