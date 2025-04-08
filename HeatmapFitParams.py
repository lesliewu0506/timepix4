import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def LoadCSV(filepath):
    df = pd.read_csv(filepath, delim_whitespace=True, header=None, skiprows=15)
    df.columns = ["Col", "Row", "p0", "p1", "p2", "p3", "p0_err", "p1_err", "p2_err", "p3_err", "red_chi2", "valid"]
    return df

def PlotChargeCalibrationsAll(filepath: str, parameters: list):
    df = LoadCSV(filepath)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    fig.suptitle("Heatmaps of p0 t/m p3 per pixel for N116", fontsize=18)
    for i, param in enumerate(parameters):
        heatmap_data = df.pivot(index="Row", columns="Col", values=param)
        sns.heatmap(
            heatmap_data,
            cmap="viridis",
            cbar_kws={"label": f"{param}"},
            ax=axes[i],
            square=True
        )
        axes[i].set_title(f"{param} per pixel")
        axes[i].set_xticks([])
        axes[i].set_yticks([])
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

    plt.tight_layout()
    plt.savefig("All_Calibration_Heatmaps.png", dpi=600)
    plt.show()

if __name__ == "__main__":
    filepath = "Charge Calibrations/N116_charge.txt"
    parameters = ["p0", "p1", "p2", "p3"]
    PlotChargeCalibrationsAll(filepath, parameters)