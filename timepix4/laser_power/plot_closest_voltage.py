import pandas as pd
import matplotlib.pyplot as plt


def PlotClosestVoltage(filepath: str, tot_ref: float) -> None:
    df = pd.read_csv(filepath)
    plt.figure(figsize=(12, 8))
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
    plt.scatter(df["AttenuationVoltage"], df["Mean Tot"], marker="o", color="b")
    plt.axhline(
        tot_ref,
        color="red",
        linestyle="--",
        label=f"Reference ToT: {tot_ref:.2f} [25 ns]",
    )
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Mean ToT [25 ns]")
    # plt.title("Mean ToT vs Attenuation Voltage")
    plt.xlim(3.6, 4)
    plt.ylim(0, 400)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("ClosestVoltage.png", dpi=300)
    plt.show()
