import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


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

        # PlotZoomedLinearity(lookuptable, [dfH1, dfH2, dfH3], Pixel)
        # PlotLinearity(lookuptable, [dfH1, dfH2, dfH3], Pixel, "High")
        # PlotLinearity(lookuptable, [dfL1, dfL2, dfL3], Pixel, "Low")
        GainComparison(lookuptable, dfH1, dfL1, Pixel)
        # PlotHits(dfH1, dfL1, lookuptable)

def fit_function(x, a, b):
    return a * x + b


def PlotZoomedLinearity(
    lookuptable: pd.DataFrame, dfs: list[pd.DataFrame], Pixel: str
) -> None:
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.plot(
        np.arange(0, 700, 1),
        np.arange(0, 700, 1),
        linestyle="dashdot",
        color="black",
        label="Expected Response",
    )
    plt.xlabel("Injected Charge [ke]")
    plt.ylabel("Measured Charge [ke]")
    plt.xlim(0, 105)
    plt.ylim(0, 105)
    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(0, 101, 25))
    ax.set_xticks(np.arange(0, 101, 5), minor=True)
    ax.set_yticks(np.arange(0, 101, 25))
    ax.set_yticks(np.arange(0, 101, 5), minor=True)

    # Prepare color cycle so data and fit share the same color
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for i, df in enumerate(dfs):
        if len(df) < len(lookuptable):
            lut = lookuptable.iloc[: len(df)]
        else:
            lut = lookuptable

        if i == 0:
            label = "1-pixel"
        elif i == 1:
            label = "2-pixel"
        else:
            label = "4-pixel"

        color = colors[i % len(colors)]
        plt.errorbar(
            lut["Charge"],
            df["Mean clCharge Calibrated"],
            yerr=df["Std clCharge Calibrated"],
            fmt="o",
            markersize=8,
            linestyle="none",
            # label=label,
            # capsize=3,
            color=color,
        )
        # Remove any NaN or infinite values and restrict charge range to [10, 400]
        xdata = lut["Charge"].values
        ydata = df["Mean clCharge Calibrated"].values
        yerrors = df["Std clCharge Calibrated"].values
        mask = np.isfinite(xdata) & np.isfinite(ydata) & (xdata >= 10) & (xdata <= 100)
        popt, pcov = curve_fit(
            fit_function,
            xdata[mask],
            ydata[mask],
            sigma=yerrors[mask],
            p0=[1, 0],
        )
        x_fit = np.linspace(0, 700, 100)
        y_fit = fit_function(x_fit, *popt)
        plt.plot(
            x_fit,
            y_fit,
            linestyle="-",
            label=f"{label}; Fit: a = {popt[0]:.2g}, b = {popt[1]:.2g}",
            color=color,
        )
    plt.grid()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
    ax.legend(
        loc="upper left",  # or whatever corner you like
        bbox_to_anchor=(0.03, 0.98),  # move it just outside the axes
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
    plt.savefig("HighZoomed.png", dpi=300)
    plt.show()


def PlotLinearity(
    lookuptable: pd.DataFrame, dfs: list[pd.DataFrame], Pixel: str, Gain: str
) -> None:
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.plot(
        np.arange(0, 700, 1),
        np.arange(0, 700, 1),
        linestyle="dashdot",
        color="black",
        label="Expected Response",
    )
    plt.xlabel("Injected Charge [ke]")
    plt.ylabel("Measured Charge [ke]")
    plt.xlim(0, 690)
    plt.ylim(0, 690)
    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")
    ax.set_xticks(np.arange(0, 601, 150))
    ax.set_xticks(np.arange(0, 661, 30), minor=True)
    ax.set_yticks(np.arange(0, 601, 150))
    ax.set_yticks(np.arange(0, 661, 30), minor=True)

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for i, df in enumerate(dfs):
        if len(df) < len(lookuptable):
            lut = lookuptable.iloc[: len(df)]
        else:
            lut = lookuptable

        if i == 0:
            label = "1-pixel"
        elif i == 1:
            label = "2-pixel"
        else:
            label = "4-pixel"

        color = colors[i % len(colors)]
        plt.errorbar(
            lut["Charge"],
            df["Mean clCharge Calibrated"],
            yerr=df["Std clCharge Calibrated"],
            fmt="o",
            markersize=8,
            linestyle="none",
            # label=label,
            # capsize=3,
            color=color,
        )
        # Remove any NaN or infinite values and restrict charge range to [10, 400]
        xdata = lut["Charge"].values
        ydata = df["Mean clCharge Calibrated"].values
        yerrors = df["Std clCharge Calibrated"].values
        mask = np.isfinite(xdata) & np.isfinite(ydata) & (xdata >= 10) & (xdata <= 100)
        popt, pcov = curve_fit(
            fit_function,
            xdata[mask],
            ydata[mask],
            sigma=yerrors[mask],
            p0=[1, 0],
        )
        x_fit = np.linspace(0, 700, 100)
        y_fit = fit_function(x_fit, *popt)
        plt.plot(
            x_fit,
            y_fit,
            linestyle="-",
            label=f"{label}; Fit: a = {popt[0]:.2g}, b = {popt[1]:.2g}",
            color=color,
        )
    plt.grid()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
    ax.legend(
        loc="upper left",  # or whatever corner you like
        bbox_to_anchor=(0.03, 0.98),  # move it just outside the axes
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
    plt.savefig(f"{Gain}{Pixel}clCharge Calibrated_vs_InjectedCharge.png", dpi=300)
    plt.show()


def GainComparison(lookuptable: pd.DataFrame, dfH1, dfL1, Pixel: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.xlabel("Injected Charge [ke]")
    plt.ylabel("ToT [25 ns]")
    plt.xlim(0, 690)
    plt.ylim(0, 2100)
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
            markersize=8,
            linestyle="none",
            label=label,
            # capsize=3,
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
        plt.xlim(0, 690)
        plt.ylim(1000, 100000)

        ax.tick_params(
            axis="both", which="major", length=12, width=witdh, direction="in"
        )
        ax.tick_params(
            axis="both", which="minor", length=6, width=witdh, direction="in"
        )
        ax.set_xticks(np.arange(0, 690, 150))
        ax.set_xticks(np.arange(0, 690, 30), minor=True)

        plt.grid()
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
        plt.tight_layout()
        if i == 0:
            plt.savefig(f"HighAttenuationVoltage_vs_nhits.png", dpi=300)
        else:
            plt.savefig(f"LowAttenuationVoltage_vs_nhits.png", dpi=300)
        plt.show()
