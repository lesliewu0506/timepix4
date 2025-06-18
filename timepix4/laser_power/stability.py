import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def PlotLaserStability(filepath: str) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 22,
            "axes.labelsize": 18,
            "xtick.labelsize": 16,
            "ytick.labelsize": 16,
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
        # means.append(filtered["Charge"].mean())
        # std.append(filtered["Charge"].std())

    plt.figure(figsize=(10, 8))
    plt.errorbar(
        range(0, 61),
        means,
        yerr=std,
        fmt="o",
        markersize=4,
        capsize=4,
        linestyle="none",
    )
    plt.xlabel("Time [min]")
    plt.ylabel("ToT [25 ns]")
    # plt.ylabel("Charge [ke]")
    # plt.title("Laser Stability")
    plt.xlim(0, 60)
    plt.ylim(240, 260)
    # plt.ylim(15, 20)
    plt.grid()
    plt.tight_layout()
    plt.savefig("LaserStabilityToT.png", dpi=300)
    # plt.savefig("LaserStabilityCharge.png", dpi=300)
    plt.show()

    plt.figure(figsize=(10, 8))
    # plt.hist(df_filtered["tot"], bins=100)

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
    )

    # Define Gaussian function
    def gaussian(x, amp, mu, sigma):
        return amp * np.exp(-((x - mu) ** 2) / (2 * sigma**2))

    # Initial guesses: amplitude, mean, std
    p0 = [counts.max(), data.mean(), data.std()]
    # Fit Gaussian
    popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
    # Plot fitted Gaussian
    x_fit = np.linspace(bin_centers.min(), bin_centers.max(), 500)
    plt.plot(
        x_fit,
        gaussian(x_fit, *popt),
        color="red",
        linestyle="-",
        label=f"Fit: μ={popt[1]:.2f}, σ={popt[2]:.2f}",
    )
    plt.xlim(230, 270)
    plt.ylim(0, 160000)
    plt.xlabel("ToT [25 ns]")
    plt.ylabel("Counts")
    # plt.grid()
    plt.legend(loc="best", fontsize=18)
    plt.tight_layout()
    plt.savefig("LaserStabilityToTHistogram.png", dpi=300)
    plt.show()
