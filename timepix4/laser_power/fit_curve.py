import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from .plot_relative_power import PlotRelativePower


def CreateLookupTable(filepath: str, V_ref: float) -> None:
    df = pd.read_csv(filepath)
    fit_curve(df, V_ref)


def fit_func(V, A, k, C):
    return A * np.exp(-k * V) + C


def fit_curve(df: pd.DataFrame, V_ref: float):
    plt.rcParams.update({
        'font.size': 18,
        'axes.titlesize': 18,
        'axes.labelsize': 18,
        'xtick.labelsize': 18,
        'ytick.labelsize': 18,
        'figure.titlesize': 20
    })
    df_copy = df.copy()
    df = df[((df["V"] >= 2.8) & (df["V"] <= 4.0))]
    P = df["power"].to_numpy()
    V = df["V"].to_numpy()

    popt, pcov = curve_fit(
        fit_func,
        V,
        P,
        p0=[50, 1.0 / (np.ptp(V)), 0.01],
    )

    # plot
    Vfine = np.linspace(2.8, 4.0, 200)
    plt.figure(figsize=(12, 8))
    plt.scatter(df_copy["V"].to_numpy(), df_copy["power"].to_numpy(), marker="o", color="b")
    plt.plot(Vfine, fit_func(Vfine, *popt), linestyle="-", color="orange", label=f"Fit parameters: A = {popt[0]:.0f}, k = {popt[1]:.2f}, C ={popt[2]:.2f}")
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Power [$\mu$W]")
    plt.xlim(2.8, 4)
    plt.ylim(0, 30)
    plt.legend()
    # plt.title("Power vs Voltage")
    plt.grid()
    plt.tight_layout()
    plt.savefig("PowerVsVoltage.png", dpi=300)
    plt.show()

    # P_ref = fit_func(V_ref, *popt)
    # # voltages from 4.000 down to 3.050 in steps of 0.025
    # Vs = np.linspace(4.0, 3.05, int(round((4.0 - 3.05) / 0.025)) + 1)
    # Vs = np.round(Vs, 3)
    # factors = fit_func(Vs, *popt) / P_ref
    # lut = pd.DataFrame({"voltage": Vs, "relative_factor": factors})
    # lut.to_csv("lookup_table.csv", index=False)

    # PlotRelativePower("lookup_table.csv")
