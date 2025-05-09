import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ToTChargePlotter(FilePath: str) -> None:
    df = pd.read_csv(FilePath)
    df_copy = df.copy()
    # df = df[(df["Mean Charge Raw"] < 100)]
    lookuptable = pd.read_csv("lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.errorbar(
        df["Mean Charge Raw"],
        df["Mean Tot"],
        xerr=df["Std Charge Raw"],
        fmt="o",
        markersize=4,
        linestyle="none",
        # color="blue",
        label="Test Pulse",
    )
    plt.plot(
        df["Mean Charge Raw"],
        df["Mean Tot"],
        linestyle="-",
        # color="red",
    )
    plt.errorbar(
        df["Mean clCharge"],
        df["Mean Tot"],
        xerr=df["Std clCharge"],
        fmt="o",
        markersize=4,
        linestyle="none",
        # color="cyan",
        label="Test Pulse clcharge",
    )
    plt.plot(
        df["Mean clCharge"],
        df["Mean Tot"],
        linestyle="-",
        # color="green",
    )
    plt.errorbar(
        df["Mean Charge Calibrated"],
        df["Mean Tot"],
        xerr=df["Std Charge Calibrated"],
        fmt="o",
        markersize=4,
        linestyle="none",
        # color="yellow",
        label="Manual calibrated",
    )
    plt.plot(
        df["Mean Charge Calibrated"],
        df["Mean Tot"],
        linestyle="-",
        # color="pink",
    )
    # plt.errorbar(
    #     df["Mean clCharge"],
    #     df["Mean Tot"],
    #     xerr=df["Std clCharge"],
    #     fmt="o",
    #     markersize=4,
    #     linestyle="none",
    #     color="green",
    #     label="Test Pulse clcharge",
    # )
    # plt.plot(
    #     df["Mean clCharge"],
    #     df["Mean Tot"],
    #     linestyle="-",
    #     color="orange",
    # )

    plt.plot(
        lookuptable["Charge"],
        df_copy["Mean Tot"],
        marker="o",
        markersize=4,
        linestyle="-",
        # color="black",
        label="Laser Calibration",
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
