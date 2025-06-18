import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def LaserPlotter(folder: list[list[str]], value: str = "Tot") -> None:
    lookuptable = pd.read_csv("lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 20,
            "axes.labelsize": 20,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "figure.titlesize": 20,
        }
    )

    for pixel in folder:
        High1 = pixel[0].replace("x", "High")
        High2 = pixel[1].replace("x", "High")
        High3 = pixel[2].replace("x", "High")
        Low1 = pixel[0].replace("x", "Low")
        Low2 = pixel[1].replace("x", "Low")
        Low3 = pixel[2].replace("x", "Low")

        Pixel = High1.split("/")[-2].split("1")[-1].split(" ", 1)[-1]
        fig, ax = plt.subplots(figsize=(12, 10))
        dfH1 = pd.read_csv(High1)
        dfH2 = pd.read_csv(High2)
        dfH3 = pd.read_csv(High3)
        dfL1 = pd.read_csv(Low1)
        dfL2 = pd.read_csv(Low2)
        dfL3 = pd.read_csv(Low3)

        if value == "Tot" or value == "clTot":
            plt.xlim(0, 400)
            plt.ylim(0, 2000)
            plt.xlabel("Injected Charge [ke]", fontsize=16)
            plt.ylabel("ToT [25 ns]", fontsize=16)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
        elif (
            value == "clCharge"
            or value == "Charge Raw"
            or value == "clCharge Calibrated"
        ):
            plt.xlim(0, 700)
            plt.ylim(0, 2250)
            # plt.xlim(0, 700)
            # plt.ylim(0, 700)
            plt.xlabel("Injected Charge [ke]")
            plt.ylabel("Measured Charge [ke]")
            plt.ylabel("ToT [25 ns]")
            # plt.xticks(fontsize=12)
            # plt.yticks(fontsize=12)

        for High, Low, pixels in zip([dfH1, dfH2, dfH3], [dfL1, dfL2, dfL3], [1, 2, 4]):
            for i, df in zip([1, 2], [High, Low]):
                if len(df) < len(lookuptable):
                    lut = lookuptable.iloc[: len(df)]
                else:
                    lut = lookuptable

                if i == 1:
                    label = f"{pixels} Pixels (High)"
                else:
                    label = f"{pixels} Pixels (Low)"
                plt.errorbar(
                    lut["Charge"],
                    # df[f"Mean {value}"],
                    df["Mean Tot"],
                    # yerr=df[f"Std {value}"],
                    yerr=df["Std Tot"],
                    fmt="o",
                    markersize=4,
                    linestyle="-",
                    # label = f"{pixels} Pixel Injection",
                    # label = f"{pixels} Pixels (Low)"
                    label=label,
                    capsize=3,
                )
            break

        # plt.plot(
        #     np.arange(0, 700, 1),
        #     np.arange(0, 700, 1),
        #     linestyle="dashdot",
        #     color="black",
        #     label="Expected Response",
        # )
        # ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
        # ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))
        ax.tick_params(axis="both", which="minor", length=5)
        ax.tick_params(axis="both", which="minor", direction="in", labelbottom=False)

        plt.legend(fontsize=18)
        plt.grid()
        plt.tight_layout()
        # plt.savefig(f"{Pixel}{value}_vs_InjectedCharge.png", dpi=300)
        plt.savefig(f"{Pixel}_High_vs_Low.png", dpi=600)
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
