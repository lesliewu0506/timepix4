import pandas as pd
import matplotlib.pyplot as plt


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
    plt.rcParams.update({
        'font.size': 18,
        'axes.titlesize': 18,
        'axes.labelsize': 18,
        'xtick.labelsize': 18,
        'ytick.labelsize': 18,
        'figure.titlesize': 20
    })
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(df["Voltage"], df["Current"], marker="o", markersize=5)
    # Automatically invert axes and set limits for negative-valued data
    x_min, x_max = df["Voltage"].min(), df["Voltage"].max()
    y_min, y_max = df["Current"].min(), df["Current"].max()
    ax.set_xlim(x_max, -200)
    ax.set_ylim(y_max, -2.0)
    plt.xlabel("Voltage [V]")
    plt.ylabel("Leakage Current [$\mu$A]")
    plt.grid(True)
    # plt.title(f"IV-Curve {sensor}")
    plt.tight_layout()

    plt.savefig(f"IV_curve_{sensor}.png", dpi=300)
    plt.show()
