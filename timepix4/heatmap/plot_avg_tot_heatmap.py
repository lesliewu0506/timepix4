from timepix4.utils import createdicts
import uproot, ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def VisualizeToT(filepath: str) -> None:
    CorrectionFactors = createdicts()
    # Increase font sizes for readability
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 22,
            "axes.labelsize": 20,
            "xtick.labelsize": 18,
            "ytick.labelsize": 18,
            "figure.titlesize": 22,
        }
    )
    letters = ["a", "b", "c", "d", "e", "f"]

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
        std_tots = df_filtered.groupby(["row", "col"])["tot"].std().reset_index()

        center_row, center_col = 230, 228
        row_min, row_max = center_row - 3, center_row + 3
        col_min, col_max = center_col - 3, center_col + 3

        mean_tots = mean_tots[
            mean_tots["row"].between(row_min, row_max)
            & mean_tots["col"].between(col_min, col_max)
        ]
        std_tots = std_tots[
            std_tots["row"].between(row_min, row_max)
            & std_tots["col"].between(col_min, col_max)
        ]
        mean_tots["charge_manual"] = mean_tots.apply(
            lambda r: r["tot"] * CorrectionFactors.get((r["col"], r["row"]), 0.10),
            axis=1,
        )

        std_tots["charge_manual"] = std_tots.apply(
            lambda r: r["tot"] * CorrectionFactors.get((r["col"], r["row"]), 0.10),
            axis=1,
        )

        heatmap_tot = mean_tots.pivot(index="row", columns="col", values="tot")
        rows = list(range(row_min, row_max + 1))
        cols = list(range(col_min, col_max + 1))
        heatmap_tot = heatmap_tot.reindex(index=rows, columns=cols, fill_value=np.nan)

        std_heatmap_tot = std_tots.pivot(
            index="row", columns="col", values="tot"
        ).reindex(index=rows, columns=cols, fill_value=np.nan)
        if i == 0:
            annot_tot = heatmap_tot.combine(
                std_heatmap_tot,
                lambda m_col, s_col: (
                    m_col.map(lambda v: f"{v:.0f}")
                    + "\n±"
                    + s_col.map(lambda v: f"{v:.1g}")
                ),
            )
        else:
            annot_tot = heatmap_tot.combine(
                std_heatmap_tot,
                lambda m_col, s_col: (
                    m_col.map(lambda v: f"{v:.3g}")
                    + "\n±"
                    + s_col.map(lambda v: f"{v:.1g}")
                ),
            )

        total_mean_tot = mean_tots["tot"].sum()
        total_std_tot = np.sqrt((std_tots["tot"] ** 2).sum())
        heatmap_tot = heatmap_tot.reindex(index=rows, columns=cols, fill_value=np.nan)
        sns.heatmap(
            heatmap_tot,
            cmap="viridis",
            cbar_kws={"label": "ToT [25 ns]", "shrink": 0.85, "pad": 0.02},
            square=True,
            annot=annot_tot,
            fmt="",
            annot_kws={"size": 20},
            ax=axes[i],
            vmax=600,
            vmin=0,
        )
        axes[i].set_title(
            f"({letters[i]}) Total ToT = {total_mean_tot:.3g} ± {round(total_std_tot)} [25 ns]"
        )
        for spine in axes[i].spines.values():
            spine.set_visible(True)
            spine.set_linewidth(1)

        heatmap_charge = mean_tots.pivot(
            index="row", columns="col", values="charge_manual"
        )
        heatmap_charge = heatmap_charge.reindex(
            index=rows, columns=cols, fill_value=np.nan
        )
        # Pivot std charge and prepare annotation DataFrame
        std_heatmap_charge = std_tots.pivot(
            index="row", columns="col", values="charge_manual"
        ).reindex(index=rows, columns=cols, fill_value=np.nan)

        annot_charge = heatmap_charge.combine(
            std_heatmap_charge,
            lambda m_col, s_col: (
                m_col.map(lambda v: f"{v:.1f}")
                + "\n±"
                + s_col.map(lambda v: f"{v:.1g}")
            ),
        )
        # Compute total charge mean and std
        total_mean_charge = mean_tots["charge_manual"].sum()
        total_std_charge = np.sqrt((std_tots["charge_manual"] ** 2).sum())
        sns.heatmap(
            heatmap_charge,
            cmap="viridis",
            cbar_kws={"label": "Charge [ke]", "shrink": 0.85, "pad": 0.02},
            square=True,
            annot=annot_charge,
            fmt="",
            annot_kws={"size": 20},
            ax=axes[i + 3],
            vmax=60,
            vmin=0,
        )
        axes[i + 3].set_title(
            f"({letters[i + 3]}) Total Charge = {total_mean_charge:.2g} ± {round(total_std_charge)} [ke]"
        )
        for spine in axes[i + 3].spines.values():
            spine.set_visible(True)
            spine.set_linewidth(1)

    plt.tight_layout()
    plt.subplots_adjust(
        left=0.03,
        right=0.97,
        top=0.93,
        bottom=0.03,
        hspace=0.15,
        wspace=0.15,
    )
    plt.savefig(f"Heatmap6.png", dpi=300)
    plt.show()


def VisualizeToT_single(filepath: str) -> None:
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

    fig, ax = plt.subplots(figsize=(10, 8))

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

    center_row, center_col = 230, 228
    row_min, row_max = center_row - 3, center_row + 3
    col_min, col_max = center_col - 3, center_col + 3

    mean_tots = mean_tots[
        mean_tots["row"].between(row_min, row_max)
        & mean_tots["col"].between(col_min, col_max)
    ]

    rows = list(range(row_min, row_max + 1))
    cols = list(range(col_min, col_max + 1))

    heatmap_tot = mean_tots.pivot(index="row", columns="col", values="tot")
    heatmap_tot = heatmap_tot.reindex(index=rows, columns=cols, fill_value=np.nan)
    sns.heatmap(
        heatmap_tot,
        cmap="viridis",
        cbar_kws={"label": "ToT [25 ns]"},
        square=True,
        annot=True,
        fmt=".3g",
        annot_kws={"size": 16},
    )
    ax.set_title(f"Total ToT = {round(mean_tots['tot'].sum())} [25 ns]")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)

    plt.tight_layout()
    plt.savefig("Heatmap_four.png", dpi=600)
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
