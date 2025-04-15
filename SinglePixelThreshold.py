import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def CreateDataFrame(filepath):
    df = pd.read_csv(filepath, sep=",", on_bad_lines="skip", encoding="utf-8")
    df.columns = ["Col", "Row", "Charge", "meanTot", "stdvTot", "nhits"]
    df["meanTot"] = df["meanTot"] / 128
    df["stdvTot"] = df["stdvTot"] / 128
    return df


def PlotTotCharge(sensor):
    df = CreateDataFrame(f"Data/Test Pulse Data/fitData_{sensor}.csv")

    df_plot = pd.DataFrame(columns=["Charge", "meanTot", "stdvTot"])

    for charge in range(1000, 16200, 200):
        filtered_df = df[(np.isclose(df["Charge"], charge, atol=100))]
        mean_tot = filtered_df["meanTot"].mean()
        mean_tot_std = filtered_df["stdvTot"].mean()

        new_row = pd.DataFrame(
            [{"Charge": charge, "meanTot": mean_tot, "stdvTot": mean_tot_std}]
        )

        df_plot = pd.concat([df_plot, new_row], ignore_index=True)

    return df_plot


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

    return df_plot


def iqr_filtered_stats(df: pd.DataFrame):
    means = []
    stds = []

    for col in df.columns:
        data = df[col].dropna()

        # Calculate IQR
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1

        # Filter values within IQR range
        filtered = data[(data >= q1 - 1.5 * iqr) & (data <= q3 + 1.5 * iqr)]

        # Compute mean and std of filtered data
        means.append(filtered.mean())
        stds.append(filtered.std())

    return means, stds


def Main(filepath):
    df = pd.read_csv(f"Data/Single Pixel Data/Filtered/{filepath}")

    means_chargecal = PlotTotChargeSingle("N116", 240, 240)
    means_chargecal = PlotTotCharge("N116")
    relative_errors_testpulse = means_chargecal["stdvTot"] / means_chargecal["meanTot"]
    means_threshold, std_thresholds = iqr_filtered_stats(df)
    # means_threshold = df.mean().tolist()
    # std_thresholds = df.std().tolist()

    charges = list(np.arange(1, 16.2, 0.2))
    # plt.figure(figsize=(14, 6))
    # plt.scatter(
    #     means_chargecal["Charge"] / 1000,
    #     means_chargecal["meanTot"],
    #     color="blue",
    #     label="Test Pulse",
    #     s=10,
    # )

    # plt.errorbar(
    #     charges,
    #     means_threshold,
    #     yerr=std_thresholds,
    #     fmt=".",
    #     color="red",
    #     ecolor="darkred",
    #     capsize=4,
    #     label="Threshold Test",
    # )
    # plt.title(f"ToT vs Charge for N116")
    # plt.xlabel("Charge [ke]")
    # plt.ylabel("ToT [25ns]")
    # plt.legend()
    # # plt.savefig(f"ToT_vs_Charge_N116.png", dpi=600)
    # plt.show()

    relative_errors_threshold = [
        s / m if m != 0 else np.nan for m, s in zip(means_threshold, std_thresholds)
    ]
    # Plot relative errors
    plt.figure(figsize=(14, 6))
    plt.scatter(
        charges,
        relative_errors_threshold,
        marker="o",
        color="green",
        label="Threshold Test",
    )
    plt.scatter(
        means_chargecal["Charge"] / 1000,
        relative_errors_testpulse,
        marker="o",
        color="blue",
        label="Test Pulse",
    )
    plt.title("Relative Error vs Charge for N116")
    plt.xlabel("Charge [ke]")
    plt.ylim(0, 0.1)
    plt.ylabel("Relative Error")
    plt.grid(True)
    plt.legend()
    # plt.savefig("Relative_Error_vs_Charge_N116.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    Main("SinglePixel.csv")
