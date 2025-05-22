import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def PlotRelativePower(FilePath: str) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 22,
            "axes.labelsize": 18,
            "xtick.labelsize": 16,
            "ytick.labelsize": 16,
            "figure.titlesize": 22,
        }
    )
    df = pd.read_csv(FilePath)
    plt.figure(figsize=(12, 8))
    plt.plot(
        df["voltage"],
        df["relative_factor"],
        marker="o",
        linestyle="none",
        color="b",
        label="Pixel (228, 230)",
    )
    plt.axhline(y=1, color="r", linestyle="--", label="Relative Power = 1")
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Relative Power")
    # plt.title("Relative Power vs Attenuation Voltage")
    plt.xlim(3, 4)
    plt.ylim(0, 25)
    plt.xticks(np.arange(3.0, 4.05, 0.20))
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig("RelativePower.png", dpi=600)
    plt.show()
