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
        dfH1 = pd.read_csv(High1)
        dfH2 = pd.read_csv(High2)
        dfH3 = pd.read_csv(High3)
        dfL1 = pd.read_csv(Low1)
        dfL2 = pd.read_csv(Low2)
        dfL3 = pd.read_csv(Low3)

        # PlotHits(dfH1, dfL1, lookuptable)
        GainComparison(lookuptable, dfH1, dfL1, Pixel)

        # plt.xlim(0, 100)
        # plt.ylim(0, 100)
        # plt.ylabel("Measured Charge [ke]")

        # for High, Low, pixels in zip([dfH1, dfH2, dfH3], [dfL1, dfL2, dfL3], [1, 2, 4]):
        #     for i, df in enumerate([High]):
        #         if len(df) < len(lookuptable):
        #             lut = lookuptable.iloc[: len(df)]
        #         else:
        #             lut = lookuptable

        #         if i == 1:
        #             label = f"{pixels} Pixels (High)"
        #         else:
        #             label = f"{pixels} Pixels (Low)"
        #         plt.errorbar(
        #             lut["Charge"],
        #             df[f"Mean {value}"],
        #             # df["Mean Tot"],
        #             yerr=df[f"Std {value}"],
        #             # yerr=df["Std Tot"],
        #             fmt="o",
        #             markersize=4,
        #             linestyle="-",
        #             label=f"{pixels} Pixels Injection",
        #             # label = f"{pixels} Pixels (Low)"
        #             # label=label,
        #             capsize=3,
        #         )
        #     # break

        # plt.plot(
        #     np.arange(0, 700, 1),
        #     np.arange(0, 700, 1),
        #     linestyle="dashdot",
        #     color="black",
        #     label="Expected Response",
        # )
        # # ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
        # # ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))
        # ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
        # ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
        # ax.tick_params(axis="both", which="minor", length=5)
        # ax.tick_params(axis="both", which="minor", direction="in", labelbottom=False)

        # plt.legend(fontsize=18)
        # plt.grid()
        # plt.tight_layout()
        # # plt.savefig(f"Low{Pixel}{value}_vs_InjectedCharge.png", dpi=300)
        # # plt.savefig(f"{Pixel}_High_vs_Low.png", dpi=300)
        # plt.savefig("HighZoomed.png", dpi=300)
        # plt.show()


# def LaserPlotter(folder: list[list[str]], value: str = "Tot") -> None:
#     lookuptable = pd.read_csv("lookup_table.csv")
#     lookuptable = lookuptable.sort_values("voltage", ascending=True)
#     lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
#     plt.rcParams.update(
#         {
#             "font.size": 20,
#             "axes.titlesize": 20,
#             "axes.labelsize": 20,
#             "xtick.labelsize": 20,
#             "ytick.labelsize": 20,
#             "figure.titlesize": 20,
#         }
#     )

#     for pixel in folder:
#         High1 = pixel[0].replace("x", "High")
#         High2 = pixel[1].replace("x", "High")
#         High3 = pixel[2].replace("x", "High")
#         Low1 = pixel[0].replace("x", "Low")
#         Low2 = pixel[1].replace("x", "Low")
#         Low3 = pixel[2].replace("x", "Low")

#         Pixel = High1.split("/")[-2].split("1")[-1].split(" ", 1)[-1]
#         fig, ax = plt.subplots(figsize=(12, 10))
#         dfH1 = pd.read_csv(High1)
#         dfH2 = pd.read_csv(High2)
#         dfH3 = pd.read_csv(High3)
#         dfL1 = pd.read_csv(Low1)
#         dfL2 = pd.read_csv(Low2)
#         dfL3 = pd.read_csv(Low3)

#         if value == "Tot" or value == "clTot":
#             plt.xlim(0, 400)
#             plt.ylim(0, 2000)
#             plt.xlabel("Injected Charge [ke]", fontsize=16)
#             plt.ylabel("ToT [25 ns]", fontsize=16)
#             plt.xticks(fontsize=12)
#             plt.yticks(fontsize=12)
#         elif (
#             value == "clCharge"
#             or value == "Charge Raw"
#             or value == "clCharge Calibrated"
#         ):
#             plt.xlim(0, 700)
#             plt.ylim(0, 2250)
#             # plt.ylim(0, 700)
#             plt.xlabel("Injected Charge [ke]")
#             plt.ylabel("Measured Charge [ke]")
#             plt.ylabel("ToT [25 ns]")
#             # plt.xticks(fontsize=12)
#             # plt.yticks(fontsize=12)

#         for High, Low, pixels in zip([dfH1, dfH2, dfH3], [dfL1, dfL2, dfL3], [1, 2, 4]):
#             for i, df in zip([1, 2], [High, Low]):
#                 if len(df) < len(lookuptable):
#                     lut = lookuptable.iloc[: len(df)]
#                 else:
#                     lut = lookuptable

#                 if i == 1:
#                     label = f"{pixels} Pixels (High)"
#                 else:
#                     label = f"{pixels} Pixels (Low)"
#                 plt.errorbar(
#                     lut["Charge"],
#                     # df[f"Mean {value}"],
#                     df["Mean Tot"],
#                     # yerr=df[f"Std {value}"],
#                     yerr=df["Std Tot"],
#                     fmt="o",
#                     markersize=4,
#                     linestyle="-",
#                     # label = f"{pixels} Pixels Injection",
#                     # label = f"{pixels} Pixels (Low)"
#                     label=label,
#                     capsize=3,
#                 )
#             break

#         # plt.plot(
#         #     np.arange(0, 700, 1),
#         #     np.arange(0, 700, 1),
#         #     linestyle="dashdot",
#         #     color="black",
#         #     label="Expected Response",
#         # )
#         # ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
#         # ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))
#         ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
#         ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))
#         ax.tick_params(axis="both", which="minor", length=5)
#         ax.tick_params(axis="both", which="minor", direction="in", labelbottom=False)

#         plt.legend(fontsize=18)
#         plt.grid()
#         plt.tight_layout()
#         # plt.savefig(f"Low{Pixel}{value}_vs_InjectedCharge.png", dpi=300)
#         plt.savefig(f"{Pixel}_High_vs_Low.png", dpi=300)
#         plt.show()

def PlotLinearity(lookuptable: pd.DataFrame, dfs: list[pd.DataFrame]) -> None:
    pass
def GainComparison(lookuptable: pd.DataFrame, dfH1, dfL1, Pixel: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.xlabel("Injected Charge [ke]")
    plt.ylabel("ToT [25 ns]")
    plt.xlim(-30, 690)
    plt.ylim(-100, 2100)
    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(0, 601, 150))
    ax.set_xticks(np.arange(0, 661, 30), minor=True)

    ax.set_yticks(np.arange(0, 2101, 500))
    ax.set_yticks(np.arange(0, 2101, 100), minor=True)

    for i, df in enumerate([dfH1, dfL1]):
        if len(df) < len(lookuptable):
            lut = lookuptable.iloc[: len(df)]
        else:
            lut = lookuptable

        if i == 0:
            label = "High Gain Mode"
        else:
            label = "Low Gain Mode"
        plt.errorbar(
            lut["Charge"],
            df["Mean Tot"],
            yerr=df["Std Tot"],
            fmt="o",
            markersize=4,
            linestyle="-",
            label=label,
            capsize=3,
        )
    plt.grid()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
    ax.legend(
    loc="upper right",  # or whatever corner you like
    bbox_to_anchor=(0.98, 0.98),  # move it just outside the axes
    borderaxespad=0.5,  # padding between axes and legend
    frameon=True,  # draw a frame
    fancybox=False,  # straight corners (disable rounded box)
    edgecolor="black",  # color of the border
    framealpha=1.0,  # fully opaque
    labelspacing=0.3,  # vertical space between entries
    handlelength=2.5,  # length of the legend lines
    handletextpad=0.5,  # space between line and label
    borderpad=0.4,  # padding inside the legend box
    fontsize=20,
    )
    plt.tight_layout()
    plt.savefig(f"{Pixel}_High_vs_Low.png", dpi=300)
    plt.show()


def PlotHits(dfH1, dfL1, lookuptable) -> None:
    for i, df in enumerate([dfH1, dfL1]):
        fig, ax = plt.subplots(figsize=(12, 10))
        plt.yscale("log")
        plt.plot(
            lookuptable["relative_factor"] * 16.5,
            df["nhits"],
            marker="o",
            markersize=12,
            color="blue",
            alpha=0.7,
            linestyle="none",
        )
        witdh = 2

        plt.xlabel("Injected Charge [ke]")
        plt.ylabel("Number of Hits")
        plt.xlim(-20, 720)
        plt.ylim(900.05, 120000)

        ax.tick_params(
            axis="both", which="major", length=12, width=witdh, direction="in"
        )
        ax.tick_params(
            axis="both", which="minor", length=6, width=witdh, direction="in"
        )
        ax.set_xticks(np.arange(0, 701, 100))
        ax.set_xticks(np.arange(0, 701, 20), minor=True)

        plt.grid()
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
        plt.tight_layout()
        if i == 0:
            plt.savefig(f"HighAttenuationVoltage_vs_nhits.png", dpi=300)
        else:
            plt.savefig(f"LowAttenuationVoltage_vs_nhits.png", dpi=300)
        plt.show()
