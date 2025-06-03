import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf


def fit_func(x, mean1, sigma1, mean2, sigma2, A):
    return A * (erf((x - mean1) / (sigma1)) - erf((x - mean2) / (sigma2)))


def FitBeamSize(Filepath: str) -> None:
    df = pd.read_csv(Filepath)
    first_pos = df["Position"].iloc[0]
    df["RelativePosition"] = (df["Position"] - first_pos) * 1000

    # popt, pcov = curve_fit(
    #     fit_func,
    #     df["RelativePosition"],
    #     df["mean_tot"],
    #     p0=[10, 6, 60, 6, 1],
    # )
    plt.errorbar(
        df["RelativePosition"],
        df["mean_tot"],
        yerr=df["std_tot"],
        marker="o",
        linestyle="None",
        capsize=3,
        label="Mean ToT",
        markersize=4,
    )
    plt.xlabel("relative x position [$\mu$m]")
    plt.ylabel("mean ToT [ns]")
    plt.grid()
    plt.tight_layout()
    plt.show()