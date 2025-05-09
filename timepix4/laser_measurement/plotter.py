import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ToTChargePlotter(FilePath: str) -> None:
    df = pd.read_csv(FilePath)
    lookuptable = pd.read_csv("lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(
        df["Mean Charge Raw"],
        df["Mean Tot"],
        marker="o",
        linestyle="--",
        color="b",
        label="ToT vs Test Pulse Charge",
    )
    # plt.plot(
    #     df["Mean Charge"],
    #     df["Mean Tot"],
    #     marker="o",
    #     linestyle="--",
    #     color="r",
    #     label="ToT vs Test Pulse clCharge",
    # )
    plt.plot(
        lookuptable["Charge"],
        df["Mean Tot"],
        marker="o",
        linestyle="--",
        color="g",
        label="ToT vs Charge Laser Calibration",
    )
    # Set labels and title
    ax.set_xlabel("Charge [ke]")
    ax.set_ylabel("ToT [25ns]")
    ax.set_title("ToT vs Charge")
    ax.set_xlim(0, 150)
    # ax.set_ylim(0, 200)
    ax.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("ToT_Charge.png", dpi=600)
    plt.show()