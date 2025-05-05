import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def CreateDataFrame(filepath):
    df = pd.read_csv(filepath, sep=",", on_bad_lines="skip", encoding="utf-8")
    df.columns = ["Col", "Row", "Charge", "meanTot", "stdvTot", "nhits"]
    df["meanTot"] = df["meanTot"] / 128
    df["stdvTot"] = df["stdvTot"] / 128
    return df


def FitFunction(Q, a, b, c, t):
    return a * Q + b + (c / (Q - t))


def PlotTotCharge(filepath):
    filename = filepath.split("/")[-1]
    filename = filename[1].split(".")[0]
    df = CreateDataFrame(filepath)
    df_plot = pd.DataFrame(columns=["Charge", "meanTot", "stdvTot"])

    for charge in range(1000, 16200, 200):
        filtered_df = df[(np.isclose(df["Charge"], charge, atol=100))]
        mean_tot = filtered_df["meanTot"].mean()
        mean_tot_std = filtered_df["stdvTot"].mean()

        new_row = pd.DataFrame(
            [{"Charge": charge, "meanTot": mean_tot, "stdvTot": mean_tot_std}]
        )

        df_plot = pd.concat([df_plot, new_row], ignore_index=True)

    # Plotting
    # Fit the data
    popt, pcov = curve_fit(
        FitFunction, df_plot["Charge"] / 1000, df_plot["meanTot"], p0=[0.001, 0, 1, 100]
    )  # p0 is the initial guess for [a, b, c, t]

    # Generate fitted curve
    Q_fit = np.linspace(
        df_plot["Charge"].min() / 1000, df_plot["Charge"].max() / 1000, 2
    )
    Tot_fit = FitFunction(Q_fit, *popt)

    # Plot the data points and fitted curve
    plt.scatter(
        df_plot["Charge"] / 1000, df_plot["meanTot"], color="blue", label="Mean ToT"
    )
    plt.plot(Q_fit, Tot_fit, color="red", label="Fit")
    plt.xlabel("Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.legend()
    plt.title("ToT vs Charge with Fit N112")
    # plt.savefig("Tot_vs_Charge_N112.png", dpi = 600)
    plt.show()

    # Print the fitted parameters
    print("Fitted parameters: a=%.6f, b=%.6f, c=%.6f, t=%.6f" % tuple(popt))


def PlotTotChargeSingle(sensor, TestCol, TestRow):
    df = CreateDataFrame(f"Data/Test Pulse Data/fitData_{sensor}.csv")
    df_plot = pd.DataFrame(columns=["Charge", "meanTot", "stdvTot"])

    for charge in range(1000, 16200, 200):
        filtered_df = df[
            (df["Col"] == TestCol)
            & (df["Row"] == TestRow)
            & (np.isclose(df["Charge"], charge, atol=100))
        ]
        mean_tot = filtered_df["meanTot"].mean()
        mean_tot_std = filtered_df["stdvTot"].mean()

        if not np.isnan(mean_tot) and not np.isnan(mean_tot_std):
            new_row = pd.DataFrame(
                [{"Charge": charge, "meanTot": mean_tot, "stdvTot": mean_tot_std}]
            )

            df_plot = pd.concat([df_plot, new_row], ignore_index=True)

    # Plotting
    popt, pcov = curve_fit(
        FitFunction, df_plot["Charge"] / 1000, df_plot["meanTot"], p0=[0.001, 0, 1, 100]
    )  # p0 is the initial guess for [a, b, c, t]

    Q_fit = np.linspace(
        df_plot["Charge"].min() / 1000, df_plot["Charge"].max() / 1000, 2
    )
    Tot_fit = FitFunction(Q_fit, *popt)
    plt.scatter(
        df_plot["Charge"] / 1000, df_plot["meanTot"], color="blue", label="Mean ToT"
    )
    plt.plot(Q_fit, Tot_fit, color="red", label="Fit")
    plt.xlabel("Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.legend()
    plt.title(f"ToT vs Charge with Fit {sensor}({TestCol} x {TestRow})")
    # plt.savefig(f"Tot_vs_Charge_{sensor}_{TestCol}x{TestRow}.png", dpi = 600)
    plt.show()
    return df_plot


def VisualizeMultipleToTChargeSingle(filepath1, filepath2):
    figs, axs = plt.subplots(4, 4, figsize=(20, 20), sharex=False)
    j = 0
    for i, pixel in enumerate(range(50, 450, 50)):
        k = i
        if i > 3:
            j = 1
            k = i - 4

        df1 = PlotTotChargeSingle(filepath1, pixel, pixel)
        df2 = PlotTotChargeSingle(filepath2, pixel, pixel)

        axs[j, k].scatter(
            df1["Charge"] / 1000, df1["meanTot"], color="blue", label="Mean ToT N10"
        )
        # axs[j, k].plot(Q_fit1, Tot_fit1, color = "red", label = "Fit N10")
        axs[j, k].set_xlabel("Charge [ke]")
        axs[j, k].set_ylabel("ToT [25ns]")
        axs[j, k].legend()
        axs[j, k].set_title(f"ToT vs Charge with Fit N10 ({pixel} x {pixel})")
        axs[j + 2, k].scatter(
            df2["Charge"] / 1000, df2["meanTot"], color="blue", label="Mean ToT N116"
        )
        # axs[j + 2, k].plot(Q_fit2, Tot_fit2, color = "red", label = "Fit N116")
        axs[j + 2, k].set_xlabel("Charge [ke]")
        axs[j + 2, k].set_ylabel("ToT [25ns]")
        axs[j + 2, k].legend()
        axs[j + 2, k].set_title(f"ToT vs Charge with Fit N116 ({pixel} x {pixel})")

    plt.savefig("Tot_vs_Charge.png", dpi=600)
    plt.show()
    # print("Fitted parameters: a=%.6f, b=%.6f, c=%.6f, t=%.6f" % tuple(popt))


if __name__ == "__main__":
    # VisualizeMultipleToTChargeSingle("fitData_N10.csv", "fitData_N116.csv")
    # PlotTotCharge(f"{pre}fitData_N113.csv")
    # PlotTotChargeSingle("N116", 240, 240)
    PlotTotCharge("Data/Test Pulse Data/fitData_N116.csv")
