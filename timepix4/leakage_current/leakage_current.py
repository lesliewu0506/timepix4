import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def PlotIV(filepath: str, MaxVoltage: int = 200, MaxCurrent: int = 10) -> None:
    sensor = filepath.split("/")[-1].split("_")[0]

    df = _ProcessData(filepath)
    _PlotData(df, sensor, max_voltage=MaxVoltage, max_current=MaxCurrent)


def _ProcessData(filepath: str) -> None:
    df = pd.read_csv(filepath, sep=" ", header=None)

    df.columns = ["Voltage", "Current", "Std"]
    df["Voltage"] = df["Voltage"]
    df["Current"] = df["Current"] * ((10**6))

    return df


def _PlotData(
    df: pd.DataFrame, sensor: str, max_voltage: int, max_current: int
) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 18,
            "axes.labelsize": 20,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "figure.titlesize": 20,
        }
    )
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.plot(df["Voltage"], df["Current"], marker="o", markersize=5)
    # Automatically invert axes and set limits for negative-valued data
    x_min, x_max = df["Voltage"].min(), df["Voltage"].max()
    y_min, y_max = df["Current"].min(), df["Current"].max()
    ax.set_xlim(10, -210)
    ax.set_ylim(0.1, -2.1)

    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(-200, 1, 50))
    ax.set_xticks(np.arange(-200, 1, 10), minor=True)
    ax.set_yticks(np.arange(-2.0, 0.1, 0.5))
    ax.set_yticks(np.arange(-2.0, 0.01, 0.1), minor=True)


    plt.xlabel("Voltage [V]")
    plt.ylabel("Leakage Current [$\mu$A]")
    plt.grid(True)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5, zorder = 3)
    plt.tight_layout()
    plt.savefig(f"IV_curve_{sensor}.png", dpi=300)
    plt.show()
