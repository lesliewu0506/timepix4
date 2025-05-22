import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def LaserPlotter(file1, file2, file3, value: str = "Tot") -> None:
    pixel = file1.split("/")[-1].split(".")[0].split("s")[-1]
    # lookuptable = pd.read_csv(f"lookup_table{pixel}.csv")
    lookuptable = pd.read_csv(f"lookup_table(230, 228).csv")
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
        plt.ylabel("ToT [25 ns]", fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        # plt.title(f"{value} vs Injected Charge (Pixel (228, 230))", fontsize=18)
    elif value == "clCharge" or value == "Charge Raw" or value == "clCharge Calibrated":
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        # plt.xlim(0, 400)
        # plt.ylim(0, 400)
        plt.xlabel("Injected Charge [ke]", fontsize=16)
        plt.ylabel("Measured Charge [ke]", fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        # plt.title(f"clCharge Manually Calibrated vs Injected Charge (Pixel ({pixel}))", fontsize=18)

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
            capsize=3,
        )

    plt.plot(
        np.arange(0, 400, 1),
        np.arange(0, 400, 1),
        linestyle="dashdot",
        color="black",
        label="Ideal Response",
    )
    plt.legend(fontsize=16)
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"Zoomed{value}_vs_InjectedCharge.png", dpi=300)
    plt.show()


def LaserPlotterMultiple(file1, file2: str, file3: str, value: str) -> None:
    lookuptable = pd.read_csv(f"lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    ax1.set_xlim(0, 400)
    ax1.set_ylim(0, 400)
    ax1.set_xlabel("Injected Charge [ke]", fontsize=18)
    ax1.set_ylabel("Measured Charge [ke]", fontsize=18)
    ax1.set_xticks(ax1.get_xticks())
    ax1.tick_params(labelsize=14)
    ax1.set_yticks(ax1.get_yticks())
    ax1.tick_params(labelsize=14)
    ax1.set_title(f"clCharge vs Injected Charge", fontsize=20)

    # Zoomed-in view on ax2 (adjust limits as needed)
    ax2.set_xlim(0, 150)
    ax2.set_ylim(0, 150)
    ax2.set_xlabel("Injected Charge [ke]", fontsize=18)
    ax2.set_ylabel("Measured Charge [ke]", fontsize=18)
    ax2.set_xticks(ax2.get_xticks())
    ax2.tick_params(labelsize=14)
    ax2.set_yticks(ax2.get_yticks())
    ax2.tick_params(labelsize=14)
    ax2.set_title(f"Zoomed clCharge vs Injected Charge", fontsize=20)

    for df, pixels in zip([df1, df2, df3], [1, 2, 4]):
        if len(df) < len(lookuptable):
            lut = lookuptable.iloc[: len(df)]
        else:
            lut = lookuptable

        for ax in (ax1, ax2):
            ax.errorbar(
                lut["Charge"],
                df[f"Mean {value}"],
                yerr=df[f"Std {value}"],
                fmt="o",
                markersize=4,
                linestyle="-",
                label=f"{pixels} Pixels (Manually Calibrated)",
            )

    for df, pixels in zip([df1, df2, df3], [1, 2, 4]):
        if len(df) < len(lookuptable):
            lut = lookuptable.iloc[: len(df)]
        else:
            lut = lookuptable
        for ax in (ax1, ax2):
            ax.errorbar(
                lut["Charge"],
                df["Mean clCharge"],
                yerr=df["Std clCharge"],
                fmt="o",
                markersize=4,
                linestyle="--",
                label=f"{pixels} Pixels (Test Pulse Calibrated)",
            )
    for ax in (ax1, ax2):
        ax.plot(
            np.arange(0, 400, 1),
            np.arange(0, 400, 1),
            linestyle="dashdot",
            color="black",
            label="Ideal Response",
        )
    ax1.legend(fontsize=16)
    ax2.legend(fontsize=16)
    ax1.grid()
    ax2.grid()
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
