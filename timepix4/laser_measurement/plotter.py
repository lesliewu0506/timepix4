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
        label="ToT vs Charge",
    )
    # plt.plot(
    #     df["Mean Charge"],
    #     df["Mean Tot"],
    #     marker="o",
    #     linestyle="--",
    #     color="r",
    #     label="ToT vs Charge Raw",
    # )
    # Set labels and title
    ax.set_xlabel("Charge [ke]")
    ax.set_ylabel("ToT [25ns]")
    ax.set_title("ToT vs Charge")
    ax.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()