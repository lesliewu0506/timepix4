import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def SourceHitMap(file: str) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 20,
            "axes.labelsize": 20,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "figure.titlesize": 20,
        }
    )

    df = pd.read_csv(file)
    counts = df.groupby(["row", "col"]).size().reset_index(name="count")
    heatmap_data = counts.pivot(index="row", columns="col", values="count").fillna(0)

    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        heatmap_data,
        cmap="viridis",
        cbar_kws={"label": "counts/pixel"},
        vmax=900,
        vmin=0,
    )
    ax.invert_yaxis()
    major_xticks = np.arange(0, heatmap_data.shape[1], 100)
    major_yticks = np.arange(0, heatmap_data.shape[0], 100)
    minor_xticks = np.arange(0, heatmap_data.shape[1], 20)
    minor_yticks = np.arange(0, heatmap_data.shape[0], 20)
    ax.set_xticks(major_xticks)
    ax.set_yticks(major_yticks)
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(minor_yticks, minor=True)

    ax.set_xticklabels(major_xticks, rotation="horizontal")
    ax.set_yticklabels(major_yticks)

    ax.tick_params(which="major", direction="in", length=8, width=1.5)
    ax.tick_params(which="minor", direction="in", length=4, width=1)
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(which="major", direction="in", length=12, width=1)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.5)
        spine.set_color("black")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.tight_layout()
    plt.savefig("SourceHitMap.png", dpi=300)
    plt.show()
