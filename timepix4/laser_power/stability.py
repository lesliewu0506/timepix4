import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def PlotLaserStability(filepath: str) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 22,
            "axes.labelsize": 20,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "figure.titlesize": 22,
        }
    )
    means = []
    std = []
    df = pd.read_csv(filepath)
    df_filtered = df[((df["row"] == 230) & (df["col"] == 228))]
    for i in range(0, 61):
        filtered = df_filtered.iloc[i * 60000 : i * 60000 + 60000]
        means.append(filtered["tot"].mean())
        std.append(filtered["tot"].std() / np.sqrt(60000))
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.errorbar(
        range(0, 61),
        means,
        yerr=std,
        fmt="o",
        markersize=9,
        # capsize=3,
        linestyle="none",
        color="b",
    )
    plt.xlabel("Time [min]")
    plt.ylabel("ToT [25 ns]")
    plt.xlim(0, 60)
    plt.ylim(240, 260)

    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(0, 61, 15))
    ax.set_xticks(np.arange(0, 61, 3), minor=True)
    ax.set_yticks(np.arange(240, 261, 5))
    ax.set_yticks(np.arange(240, 260.5, 1), minor=True)

    plt.grid()
    ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    plt.savefig("LaserStabilityToT.png", dpi=300)
    plt.show()

    fig, ax = plt.subplots(figsize=(12, 10))

    data = df_filtered["tot"]
    # Compute histogram
    counts, bins = np.histogram(data, bins=100)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    # Plot histogram as bar chart
    plt.bar(
        bin_centers,
        counts,
        width=(bins[1] - bins[0]),
        color="blue",
        alpha=0.7,
        label="Data",
        zorder = 2
    )

    # Define Gaussian function
    def gaussian(x, amp, mu, sigma):
        return amp * np.exp(-((x - mu) ** 2) / (2 * sigma**2))

    # Initial guesses: amplitude, mean, std
    p0 = [counts.max(), data.mean(), data.std()]
    # Fit Gaussian
    popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
    # Plot fitted Gaussian
    x_fit = np.linspace(225, 275, 1000)
    plt.plot(
        x_fit,
        gaussian(x_fit, *popt),
        color="red",
        linestyle="-",
        label=f"Fit: μ={popt[1]:.2f}, σ={popt[2]:.2f}",
        zorder = 2
    )
    plt.xlim(230, 270)
    plt.ylim(0, 160000)
    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(230, 271, 10))
    ax.set_xticks(np.arange(230, 271, 2.5), minor=True)
    ax.set_yticks(np.arange(0, 160001, 40000))
    ax.set_yticks(np.arange(0, 160001, 10000), minor=True)

    plt.xlabel("ToT [25 ns]")
    plt.ylabel("Counts")
    # plt.grid(zorder = 3)  
    # ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5, zorder = 3)
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
    plt.savefig("LaserStabilityToTHistogram.png", dpi=300)
    plt.show()
