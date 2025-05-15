import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def AttenuationPlotter(filepaths: list[str]) -> None:
    plt.figure(figsize=(12, 8))
    for filepath in filepaths:
        df = pd.read_csv(filepath)
        # df["Mean clTot"] = df["Mean clTot"] / int(filepath.split("/")[-1][0])
        # plt.plot(
        #     df["AttenuationVoltage"],
        #     df["Mean clTot"],
        #     marker="o",
        #     markersize=4,
        #     linestyle="-",
        #     label=f"{filepath.split('/')[-1][0]} Pixels",
        # )
        plt.errorbar(
            df["AttenuationVoltage"],
            df["Mean clTot"],
            yerr=df["Std clTot"],
            fmt="o",
            markersize=4,
            linestyle="-",
            label=f"{filepath.split('/')[-1][0]} Pixels",
        )
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Mean ToT [25 ns]")
    plt.xticks(np.arange(3, 4, 0.05))
    plt.xlim(3, 4)
    plt.ylim(bottom=0)
    plt.gca().invert_xaxis()

    plt.legend()
    plt.grid()
    plt.title("Mean clToT vs Attenuation Voltage")
    plt.tight_layout()
    plt.savefig("MeanToTvsAttenuationVoltage.png", dpi=600)
    plt.show()
