import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def CreateLookupTable(filepath: str) -> None:
    df = pd.read_csv(filepath)
    fit_curve(df)


def fit_func(V, A, k, C):
    return A * np.exp(-k * V) + C

def fit_curve(df: pd.DataFrame):
    P = df["power"].to_numpy()
    V = df["V"].to_numpy()
    popt, pcov = curve_fit(
        fit_func, V, P, p0=[P.max(), 1.0/(np.ptp(V)), P.min()]
    ) 

    # plot
    # Vfine = np.linspace(2.8, 4.6, 200)
    # plt.plot(V, P, "o", label="data")
    # plt.plot(Vfine, fit_func(Vfine, *popt), "-", label="fit")
    # plt.xlabel("Voltage [V]")
    # plt.ylabel("Power [uW]")
    # plt.legend()
    # plt.show()

    # generate lookup table from fit (relative to V=3.700)
    V_ref = 3.700
    P_ref = fit_func(V_ref, *popt)
    # voltages from 4.000 down to 3.050 in steps of 0.025
    Vs = np.linspace(4.0, 3.05, int(round((4.0 - 3.05) / 0.025)) + 1)
    Vs = np.round(Vs, 3)
    factors = fit_func(Vs, *popt) / P_ref
    lut = pd.DataFrame({
        "voltage": Vs,
        "relative_factor": factors
    })
    lut.to_csv("lookup_table.csv", index=False)
    print("Lookup table saved to lookup_table.csv")
