import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def ScalingFactors(filepath: str) -> None:
    df = pd.read_csv(filepath)
    df_filtered = df[df["Charge"] > 11.0]
    mean_charges = (
        df_filtered.groupby(["col", "row"])["Charge"]
        .mean()
        .reset_index(name="mean_charge")
    )
    mean_charges["scalingfactor"] = 16.5 / mean_charges["mean_charge"]
    scaling_df = mean_charges[["col", "row", "scalingfactor"]]
    scaling_df.to_csv("scaling_factors.csv", index=False)

def ScalingDistribution(filepath: str) -> None:
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
    df = pd.read_csv(filepath)
    fig, ax = plt.subplots(figsize=(12, 10))

    ax.hist(df["scalingfactor"], bins=160, color="blue", alpha=0.7)
    ax.set_xlabel("Scaling Factor")
    ax.set_ylabel("Counts")

    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 15000)

    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")
    ax.set_xticks(np.arange(0, 1.81, 0.4))
    ax.set_xticks(np.arange(0, 1.81, 0.1), minor=True)
    ax.set_yticks(np.arange(0, 16001, 4000))
    ax.set_yticks(np.arange(0, 16001, 1000), minor=True)
    plt.tight_layout()  
    plt.savefig("scaling_distribution1.png")
    plt.show()