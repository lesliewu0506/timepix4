import uproot, ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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

    df_exploded.to_csv("Data/Focus/cluster2.csv", index=False)
    return df_exploded


def VisualizeToT(filepath: str) -> None:
    # filename = filepath.split(".")[0]
    file = uproot.open(filepath)
    tree = file["clusterTree"]

    arrays_data = tree.arrays(["col", "row", "tot"], library="pd")
    df_data = pd.DataFrame(
        {
            "col": arrays_data["col"].to_list(),
            "row": arrays_data["row"].to_list(),
            "tot": arrays_data["tot"].to_list(),
        }
    )

    df_filtered = FilterAndUnwrap(df_data)
    mean_tots = df_filtered.groupby(["row", "col"])["tot"].mean().reset_index()

    # Determine center pixel (highest mean ToT)
    center = mean_tots.loc[mean_tots["tot"].idxmax()]
    # center_row, center_col = int(center["row"]), int(center["col"])
    center_row, center_col = 230, 228
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
        cbar_kws={"label": "ToT [25 ns]"},
        square=True,
        annot=True,
        fmt=".0f",
        annot_kws={"size": 16},
    )
    # Add border only on the outside edges
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)
    ax.set_title("Average ToT Per Pixel (150ke)")
    plt.tight_layout()
    plt.savefig(f"Heatmap(150ke)1.png", dpi=600)
    plt.show()
