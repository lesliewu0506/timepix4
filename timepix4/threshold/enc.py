import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf, erfc


def LoadCSV(filepath):
    df = pd.read_csv(filepath, converters={"pixel": parse_tuple})
    df_filtered = df[df["pixel"].apply(lambda t: all(x % 10 == 0 for x in t))]
    return df_filtered


def parse_tuple(s):
    tup = ast.literal_eval(s)
    return tuple(int(x) for x in tup)


def error_func(x, mu, sigma):
    return 500 * (erf((mu - x) / (np.sqrt(2) * sigma))) + 500


def error_func_no_C(x, A, mu, sigma, y0):
    return y0 + 0.5 * A * erfc((x - mu) / (sigma * np.sqrt(2)))


def PlotENC(filepath: str) -> None:
    df = LoadCSV(filepath)
    threshold_columns = [col for col in df.columns if col.startswith("threshold")]
    threshold_vals = [int(c.split()[1]) for c in threshold_columns]
    sigma_list = []

    for index, row in df.iterrows():
        ydata = row[threshold_columns].values.astype(float)
        xdata = threshold_vals
        try:
            popt, _ = curve_fit(
                error_func_no_C,
                xdata,
                ydata,
                p0=[1000, 4600, 75, 1000],
                maxfev=20000,
            )
            sigma = popt[2]
            sigma_list.append(sigma)
        except (RuntimeError, ValueError):
            pass

    plt.figure(figsize=(14, 8))
    plt.hist(
        sigma_list,
        color="blue",
        bins=30,
        alpha=0.7,
    )
    plt.xlim(0, 150)
    plt.ylim(0, 800)
    plt.xlabel("Sigma")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("Sigma_Distribution_Grid.png", dpi=600)
    plt.show()
