import pandas as pd
import matplotlib.pyplot as plt


def CreateDataframe(filepath):
    df = pd.read_csv(f"Data/Voltage Scans/{filepath}.txt", sep=" ", header=None)

    df.columns = ["Voltage", "Current", "Std"]
    df["Current"] = df["Current"] * ((10**6))

    return df


def PlotIV(filepath: str):
    df = CreateDataframe(filepath)
    # Plot Current vs Voltage
    plt.figure(figsize=(14,8))
    plt.plot(df["Voltage"], df["Current"], marker="o", markersize=5)
    plt.xlabel("Absolute Voltage [V]")
    plt.xlim(0, 200)
    plt.ylim(0, 10)
    plt.ylabel("Leakage Current [$\mu$A]")
    # plt.gca().invert_xaxis()
    plt.title(f"IV-Curve N146")
    plt.tight_layout()

    plt.savefig(f"IV_curve_N146.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    # files = [f"{pre}N10_voltage_scan.txt", f"{pre}N116_voltage_scan.txt"]
    files = ["N146_Voltage_Scan"]
    for file in files:
        PlotIV(file)
