import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def DirectRelativePower(filepath: str, V_ref: float) -> None:
    plt.rcParams.update(
        {
            "font.size": 18,
            "axes.titlesize": 18,
            "axes.labelsize": 18,
            "xtick.labelsize": 18,
            "ytick.labelsize": 18,
            "figure.titlesize": 20,
        }
    )
    df = pd.read_csv(filepath)
    reference_value = df.loc[df["V"] == V_ref, "power"].iloc[0]
    df["relative_power"] = df["power"] / reference_value
    V = df["V"].to_numpy()
    relative_power = df["relative_power"].to_numpy()
    dataframe = pd.DataFrame({"voltage": V, "relative_factor": relative_power})
    dataframe.to_csv("lookup_table.csv", index=False)
    plt.figure(figsize=(10, 8))
    plt.scatter(V, relative_power, marker="o", color="b", label="Pixel (228, 230)")
    plt.axhline(y=1, color="r", linestyle="--", label="Relative Power = 1")
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Relative Power [a.u.]")
    # plt.title("Relative Power vs Attenuation Voltage")
    plt.xlim(2.8, 4.0)
    plt.ylim(0, 40)
    plt.yticks(np.arange(0, 41, 10))
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig("relative_power_plot.png", dpi = 300)
    plt.show()

    plt.figure(figsize=(10, 8))
    plt.scatter(df["V"].to_numpy(), df["power"].to_numpy(), marker="o", color="b")
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Power [$\mu$W]")
    plt.xlim(2.8, 4.0)
    plt.ylim(0, 14)
    # plt.yticks(np.arange(0, 16, 3))
    plt.grid()
    plt.tight_layout()
    plt.savefig("PowerVsVoltage.png", dpi=300)
    plt.show()