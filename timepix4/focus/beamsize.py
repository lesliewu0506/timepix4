import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf


def fit_func(x, mean1, sigma1, mean2, sigma2, A):
    return A * (erf((x - mean1) / (sigma1)) - erf((x - mean2) / (sigma2)))


def FitBeamSize(Filepath: str) -> None:
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
    df = pd.read_csv(Filepath)
    # df = df[df["mean_tot"] > 0]
    first_pos = df["Position"].iloc[0]
    df["RelativePosition"] = (df["Position"] - first_pos) * 1000 - 60

    popt, pcov = curve_fit(
        fit_func,
        df["RelativePosition"],
        df["mean_tot"],
        p0=[10, 3, 60, 3, 265],
        sigma=df["std_tot"],
        absolute_sigma=True,
    )
    print(f"Fit parameters: {popt}")
    plt.figure(figsize=(12, 10))
    plt.errorbar(
        df["RelativePosition"],
        df["mean_tot"],
        yerr=df["std_tot"],
        marker="o",
        linestyle="None",
        capsize=3,
        label="Mean ToT",
        markersize=4,
        color = "red",
    )
    x_fit = np.linspace(
        df["RelativePosition"].min(), df["RelativePosition"].max(), 300
    )
    plt.plot(
        x_fit,
        fit_func(x_fit, *popt),
        linestyle="-",
        color="blue",
        label=f"Fit: $\mu_{1}$={popt[0]:.2f}, $\sigma_{1}$={popt[1]:.2f}, $\mu_{2}$={popt[2]:.2f}, $\sigma_{2}$={popt[3]:.2f}",
    )
    plt.xlim(0, 70)
    plt.ylim(-10, 600)
    plt.xlabel("relative x position [$\mu$m]")
    plt.ylabel("mean ToT [ns]")
    plt.legend(loc = "best", fontsize=14)
    plt.grid()
    plt.tight_layout()
    plt.savefig("YBeamSizeFit.png", dpi=300)
    plt.show()
