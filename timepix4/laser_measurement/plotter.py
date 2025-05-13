import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def LaserPlotter(file1, file2, file3, value: str = "Tot") -> None:
    lookuptable = pd.read_csv(f"lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    plt.subplots(figsize=(14, 8))
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    if value == "Tot" or value == "clTot":
        plt.xlim(0, 400)
        plt.ylim(0, 2000)
        plt.xlabel("Injected Charge [ke]", fontsize=16)
        plt.ylabel("ToT [25ns]", fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.title(f"{value} vs Injected Charge", fontsize=18)
    elif value == "clCharge" or value == "Charge Raw":
        plt.xlim(0, 400)
        plt.ylim(0, 150)
        plt.xlabel("Injected Charge [ke]", fontsize=16)
        plt.ylabel("Charge [ke]", fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.title(f"{value} vs Injected Charge", fontsize=18)

    for df, pixels in zip([df1, df2, df3], [1, 2, 4]):
        if len(df) < len(lookuptable):
            lut = lookuptable.iloc[: len(df)]
        else:
            lut = lookuptable

        plt.errorbar(
            lut["Charge"],
            df[f"Mean {value}"],
            yerr=df[f"Std {value}"],
            fmt="o",
            markersize=4,
            linestyle="-",
            label=f"{pixels} Pixels",
        )
    plt.legend(fontsize=16)
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{value}_vs_InjectedCharge.png", dpi=600)
    plt.show()


def CompareMethodsPlotter(filepath: str) -> None:
    lookuptable = pd.read_csv(f"lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    plt.subplots(figsize=(14, 8))
    df = pd.read_csv(filepath)
    if len(df) < len(lookuptable):
        lut = lookuptable.iloc[: len(df)]
    else:
        lut = lookuptable

    plt.errorbar(
        lut["Charge"],
        lut["Charge"],
        fmt="o",
        markersize=4,
        linestyle="-",
        label="Method: Laser Calibration",
    )
    plt.errorbar(
        lut["Charge"],
        df["Mean Charge Calibrated"],
        xerr=df["Std Charge Calibrated"],
        fmt="o",
        markersize=4,
        linestyle="-",
        label="Method: Manual Calibration",
    )
    plt.errorbar(
        lut["Charge"],
        df["Mean clCharge"],
        xerr=df["Std clCharge"],
        fmt="o",
        markersize=4,
        linestyle="-",
        label="Method: Test Pulse Calibration",
    )

    plt.xlabel("Injected Charge [ke]", fontsize=16)
    plt.ylabel("Measured Charge [ke]", fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.title("Comparison of Calibration Methods", fontsize=18)
    plt.xlim(0, 400)
    plt.ylim(0, 400)
    plt.legend(fontsize=16)
    plt.grid()
    plt.tight_layout()
    plt.savefig("Comparison_Methods.png", dpi=600)
    plt.show()
