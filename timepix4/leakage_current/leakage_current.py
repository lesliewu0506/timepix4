import pandas as pd
import matplotlib.pyplot as plt


def PlotIV(filepath: str, MaxVoltage: int = 200, MaxCurrent: int = 10) -> None:
    sensor = filepath.split("/")[-1].split("_")[0]

    df = _ProcessData(filepath)
    _PlotData(df, sensor, max_voltage=MaxVoltage, max_current=MaxCurrent)


def _ProcessData(filepath: str) -> None:
    df = pd.read_csv(filepath, sep=" ", header=None)

    df.columns = ["Voltage", "Current", "Std"]
    df["Voltage"] = df["Voltage"].abs()
    df["Current"] = df["Current"].abs() * ((10**6))

    return df


def _PlotData(
    df: pd.DataFrame, sensor: str, max_voltage: int, max_current: int
) -> None:
    plt.figure(figsize=(14, 8))
    plt.plot(df["Voltage"], df["Current"], marker="o", markersize=5)
    plt.xlim(0, max_voltage)
    plt.ylim(0, max_current)

    plt.xlabel("Absolute Voltage [V]")
    plt.ylabel("Leakage Current [$\mu$A]")
    plt.grid(True)
    plt.title(f"IV-Curve {sensor}")
    plt.tight_layout()

    plt.savefig(f"IV_curve_{sensor}.png", dpi=600)
    plt.show()
