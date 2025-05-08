import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ToTChargePlotter(FilePath: str) -> None:
    df = pd.read_csv(FilePath)
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(
        df["Mean Charge Raw"],
        df["Mean Tot"],
        marker="o",
        linestyle="--",
        color="b",
        label="ToT vs Charge Raw",
    )
    plt.plot(
        df["Mean Charge"],
        df["Mean Tot"],
        marker="o",
        linestyle="--",
        color="r",
        label="ToT vs clCharge",
    )
    # Set labels and title
    ax.set_xlabel("Charge [ke]")
    ax.set_ylabel("ToT [25ns]")
    ax.set_title("ToT vs Charge")
    # ax.set_xlim(0, 20)
    # ax.set_ylim(0, 200)
    ax.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()