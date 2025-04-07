import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def CreateDataFrame(filepath):
    df = pd.read_csv(filepath, sep = ",", on_bad_lines="skip", encoding="utf-8")
    df.columns = ["Col", "Row","Charge","meanTot","stdvTot","nhits"]
    df["meanTot"] = df["meanTot"] / 128
    df["stdvTot"] = df["stdvTot"] / 128
    return df

def FitFunction(Q, a, b, c ,t):
    return a * Q + b + (c / (Q - t))

def PlotTotCharge(filepath):
    df = CreateDataFrame(filepath)
    df_plot = pd.DataFrame(columns = ["Charge","meanTot","stdvTot"])

    for charge in range(1000, 16200, 200):
        filtered_df = df[(np.isclose(df["Charge"], charge, atol = 100))]
        mean_tot = filtered_df["meanTot"].mean()
        mean_tot_std = filtered_df["stdvTot"].mean()

        new_row = pd.DataFrame([{
            "Charge": charge,
            "meanTot": mean_tot,
            "stdvTot": mean_tot_std
        }])

        df_plot = pd.concat([df_plot, new_row], ignore_index=True)

    # Plotting
    # Fit the data
    popt, pcov = curve_fit(FitFunction, df_plot["Charge"] / 1000, df_plot["meanTot"],
                           p0=[0.001, 0, 1, 100])  # p0 is the initial guess for [a, b, c, t]

    # Generate fitted curve
    Q_fit = np.linspace(df_plot["Charge"].min() / 1000, df_plot["Charge"].max() / 1000, 2)
    Tot_fit = FitFunction(Q_fit, *popt)

    # Plot the data points and fitted curve
    plt.scatter(df_plot["Charge"] / 1000, df_plot["meanTot"], color="blue", label="Mean ToT")
    plt.plot(Q_fit, Tot_fit, color="red", label="Fit")
    plt.xlabel("Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.legend()
    plt.title("ToT vs Charge with Fit N10")
    plt.savefig("Tot_vs_Charge_N10.png", dpi = 600)
    plt.show()

    # Print the fitted parameters
    print("Fitted parameters: a=%.6f, b=%.6f, c=%.6f, t=%.6f" % tuple(popt))

def PlotTotChargeSingle(filepath, TestCol, TestRow):
    df = CreateDataFrame(filepath)
    df_plot = pd.DataFrame(columns = ["Charge","meanTot","stdvTot"])

    for charge in range(1000, 16200, 200):
        filtered_df = df[(df["Col"] == TestCol)
                         & (df["Row"] == TestRow)
                         & (np.isclose(df["Charge"], charge, atol = 100))]
        mean_tot = filtered_df["meanTot"].mean()
        mean_tot_std = filtered_df["stdvTot"].mean()

        if not np.isnan(mean_tot) and not np.isnan(mean_tot_std):
            new_row = pd.DataFrame([{
                                    "Charge": charge,
                                    "meanTot": mean_tot,
                                    "stdvTot": mean_tot_std
                                    }])

            df_plot = pd.concat([df_plot, new_row], ignore_index=True)

    # Plotting
    popt, pcov = curve_fit(FitFunction, df_plot["Charge"] / 1000, df_plot["meanTot"],
                           p0=[0.001, 0, 1, 100])  # p0 is the initial guess for [a, b, c, t]

    # Generate fitted curve
    Q_fit = np.linspace(df_plot["Charge"].min() / 1000, df_plot["Charge"].max() / 1000, 2)
    Tot_fit = FitFunction(Q_fit, *popt)

    # Plot the data points and fitted curve
    plt.scatter(df_plot["Charge"] / 1000, df_plot["meanTot"], color="blue", label="Mean ToT")
    plt.plot(Q_fit, Tot_fit, color="red", label="Fit")
    plt.xlabel("Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.legend()
    plt.title("ToT vs Charge with Fit N116")
    # plt.savefig("Tot_vs_Charge_N10.png", dpi = 600)
    plt.show()

    # Print the fitted parameters
    print("Fitted parameters: a=%.6f, b=%.6f, c=%.6f, t=%.6f" % tuple(popt))

def STDHistogram(filepath1, filepath2):
    plt.figure(figsize=(8, 6))

    for filepath, color in zip([filepath1, filepath2], ['blue', 'orange']):
        df = CreateDataFrame(filepath)
        df["stdvTot"] = df["stdvTot"] / df["meanTot"] * 100
        plt.hist(df["stdvTot"], bins=100, alpha=0.5, label=f"{filepath}", color=color)

    plt.xlabel("std ToT [%]")
    plt.ylabel("Frequency")
    plt.title("std ToT Histogram Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig("stdTot_Histogram_Comparison.png", dpi=600)
    plt.show()

if __name__ == "__main__":
    for i in range(100, 450, 50):
        PlotTotChargeSingle("fitData_N116.csv", i, i)
    # STDHistogram("fitData_N10.csv", "fitData_N116.csv")