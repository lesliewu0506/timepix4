import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main_plot(filepath):
    df = pd.read_csv(filepath)
    # plt.figure(figsize=(14, 8))
    plt.plot(df["V"], df["power"], linestyle="-", marker="o", color="blue", label="Power")
    # plt.xticks(np.arange(0, 5, 1))
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Power [$\mu$W]")
    # plt.title("Power vs Voltage")
    plt.grid()
    plt.tight_layout()
    plt.savefig("PowerVsVoltage.png")
    plt.show()


if __name__ == "__main__":
    filepath = "Data/Power.csv"
    main_plot(filepath)
