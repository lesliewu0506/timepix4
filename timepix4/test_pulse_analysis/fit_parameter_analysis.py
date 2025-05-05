import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def ParameterComparison(filepath1: str, filepath2: str):
    Sensor1 = filepath1.split("/")[-1].split("-")[0]
    df1 = _LoadData(filepath1)

    Sensor2 = filepath2.split("/")[-1].split("-")[0]
    df2 = _LoadData(filepath2)

    plt.figure(figsize=(12, 8))
    plt.hist(df1["p0"], bins=50, alpha=0.5, label=Sensor1, density=True)
    plt.hist(df2["p0"], bins=50, alpha=0.5, label=Sensor2, density=True)
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(f"Histogram of p0 Values {Sensor1} vs {Sensor2}.png", dpi=600)
    plt.show()


def HeatmapFitParam(filepaths: list[str], parameter: str = "p1") -> None:
    sensors = [filepath.split("/")[-1].split("-")[0] for filepath in filepaths]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(
        f"Heatmaps of {parameter} per pixel for different sensors", fontsize=18
    )
    axes = axes.flatten()

    for i, filepath in enumerate(filepaths):
        df = _LoadData(filepath)
        heatmap_data = df.pivot(index="Row", columns="Col", values=parameter)
        sns.heatmap(
            heatmap_data,
            cmap="viridis",
            cbar_kws={"label": "p1"},
            ax=axes[i],
            square=True,
            vmin=0.65,
            vmax=2.5,
        )
        axes[i].set_title(sensors[i])
        axes[i].set_xticks([])
        axes[i].set_yticks([])
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

    plt.tight_layout()
    plt.savefig(f"MultipleSensors_Heatmaps_param_{parameter}.png", dpi=600)
    plt.show()


def _LoadData(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df
