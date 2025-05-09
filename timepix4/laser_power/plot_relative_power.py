import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def PlotRelativePower(FilePath: str) -> None:
    df = pd.read_csv(FilePath)
    plt.figure(figsize=(12, 8))
    plt.plot(
        df["voltage"],
        df["relative_factor"],
        marker="o",
        linestyle="--",
        color="b",
        label="Relative Power vs Attenuation Voltage",
    )
    plt.axhline(y=1, color="r", linestyle="--", label="Relative Power = 1")
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Relative Power")
    plt.title("Relative Power vs Attenuation Voltage")

    plt.xticks(np.arange(3.0, 4.05, 0.05))
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig("RelativePower.png", dpi=600)
    plt.show()
