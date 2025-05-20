from timepix4.utils import createdicts
import uproot, ast
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import numpy as np


def VisualizeToT(filepath: str) -> None:
    CorrectionFactors = createdicts()
    # Increase font sizes for readability
    plt.rcParams.update(
        {
            "font.size": 16,
            "axes.titlesize": 18,
            "axes.labelsize": 16,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "figure.titlesize": 20,
        }
    )

    fig, ax = plt.subplots(2, 3, figsize=(24, 16))
    axes = ax.flatten()
    for i, c in enumerate(["1", "2", "4"]):
        filename = filepath.replace("x", c)
        file = uproot.open(filename)
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

        center_row, center_col = 230, 228
        row_min, row_max = center_row - 3, center_row + 3
        col_min, col_max = center_col - 3, center_col + 3

        mean_tots = mean_tots[
            mean_tots["row"].between(row_min, row_max)
            & mean_tots["col"].between(col_min, col_max)
        ]

        mean_tots["charge_manual"] = mean_tots.apply(
            lambda r: r["tot"] * CorrectionFactors.get((r["col"], r["row"]), 0.10),
            axis=1,
        )
        heatmap_tot = mean_tots.pivot(index="row", columns="col", values="tot")
        rows = list(range(row_min, row_max + 1))
        cols = list(range(col_min, col_max + 1))
        heatmap_tot = heatmap_tot.reindex(index=rows, columns=cols, fill_value=np.nan)
        sns.heatmap(
            heatmap_tot,
            cmap="viridis",
            cbar_kws={"label": "ToT [25 ns]"},
            square=True,
            annot=True,
            fmt=".0f",
            annot_kws={"size": 16},
            ax=axes[i],
        )
        axes[i].set_title(f"Total ToT = {round(mean_tots["tot"].sum())} [25ns]")
        for spine in axes[i].spines.values():
            spine.set_visible(True)
            spine.set_linewidth(1)

        heatmap_charge = mean_tots.pivot(
            index="row", columns="col", values="charge_manual"
        )
        heatmap_charge = heatmap_charge.reindex(
            index=rows, columns=cols, fill_value=np.nan
        )
        sns.heatmap(
            heatmap_charge,
            cmap="viridis",
            cbar_kws={"label": "Charge [ke]"},
            square=True,
            annot=True,
            fmt=".0f",
            annot_kws={"size": 16},
            ax=axes[i + 3],
        )
        axes[i + 3].set_title(
            f"Total Charge = {round(mean_tots["charge_manual"].sum())} [ke]"
        )
        for spine in axes[i + 3].spines.values():
            spine.set_visible(True)
            spine.set_linewidth(1)

    plt.suptitle("Injected Charge = 50ke", fontweight="bold")
    plt.tight_layout()

    line = Line2D(
        [0, 1], [0.485, 0.485], transform=fig.transFigure, color="black", linewidth=2
    )
    fig.add_artist(line)
    plt.savefig(f"Heatmap(50ke).png", dpi=600)
    plt.show()


def VisualizeToT_single(filepath: str) -> None:
    plt.rcParams.update(
        {
            'font.size': 16,
            'axes.titlesize': 18,
            'axes.labelsize': 16,
            'xtick.labelsize': 14,
            'ytick.labelsize': 14,
            'figure.titlesize': 20,
        }
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    file = uproot.open(filepath)
    tree = file['clusterTree']

    arrays_data = tree.arrays(['col', 'row', 'tot'], library='pd')
    df_data = pd.DataFrame(
        {
            'col': arrays_data['col'].to_list(),
            'row': arrays_data['row'].to_list(),
            'tot': arrays_data['tot'].to_list(),
        }
    )

    df_filtered = FilterAndUnwrap(df_data)
    mean_tots = df_filtered.groupby(['row', 'col'])['tot'].mean().reset_index()

    center_row, center_col = 230, 228
    row_min, row_max = center_row - 3, center_row + 3
    col_min, col_max = center_col - 3, center_col + 3

    mean_tots = mean_tots[
        mean_tots['row'].between(row_min, row_max)
        & mean_tots['col'].between(col_min, col_max)
    ]

    rows = list(range(row_min, row_max + 1))
    cols = list(range(col_min, col_max + 1))

    heatmap_tot = mean_tots.pivot(index='row', columns='col', values='tot')
    heatmap_tot = heatmap_tot.reindex(index=rows, columns=cols, fill_value=np.nan)
    sns.heatmap(
        heatmap_tot,
        cmap='viridis',
        cbar_kws={'label': 'ToT [25 ns]'},
        square=True,
        annot=True,
        fmt='.0f',
        annot_kws={'size': 16},
    )
    ax.set_title(f"Total ToT = {round(mean_tots['tot'].sum())} [25 ns]")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)

    plt.tight_layout()
    plt.savefig('Heatmap_single.png', dpi=600)
    plt.show()


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
