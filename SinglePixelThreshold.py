import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def CreateDataFrame(filepath):
    df = pd.read_csv(filepath, sep=",", on_bad_lines="skip", encoding="utf-8")
    df.columns = ["Col", "Row", "Charge", "meanTot", "stdvTot", "nhits"]
    df["meanTot"] = df["meanTot"] / 128
    df["stdvTot"] = df["stdvTot"] / 128
    return df


def CreatePixelDataFrames(filepath) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(filepath)
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["col", "row"])

    df["col"] = df["col"].astype(int)
    df["row"] = df["row"].astype(int)
    # Sort the DataFrame by pixel column and row.
    df.sort_values(by=["col", "row"], inplace=True)

    pixel_dataframes = {}
    # Group by 'col' and 'row' and then remove those columns from each pixel DataFrame.
    for (col, row), group in df.groupby(["col", "row"]):
        # Only keep groups with 500 or more counts
        if group.shape[0] < 500:
            continue
        filtered_group = group.drop(columns=["row", "col"])
        pixel_dataframes[(col, row)] = filtered_group.reset_index(drop=True)
    return pixel_dataframes


def CreateTestPulseDF(sensor: str) -> pd.DataFrame:
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


def HelperPlotTotChargeSingle(sensor, TestCol, TestRow):
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


def HelperPlotToTvsCharge(pixel, means_threshold, std_thresholds):
    col_val, row_val = pixel
    plt.errorbar(
        np.arange(1, 16.2, 0.2),
        means_threshold,
        yerr=std_thresholds,
        fmt=".",
        color="red",
        ecolor="darkred",
        capsize=4,
        label=f"Threshold Test Pixel ({col_val}, {row_val})",
    )


def PlotToTvsCharge(df_testpulse, dict_pixels):
    # Start Plot
    plt.figure(figsize=(14, 8))
    plt.scatter(
        df_testpulse["Charge"] / 1000,
        df_testpulse["meanTot"],
        color="blue",
        label="Test Pulse",
        s=10,
    )
    for keys, df_pixels in dict_pixels.items():
        means_chargecal, std_thresholds = iqr_filtered_stats(df_pixels)
        HelperPlotToTvsCharge(keys, means_chargecal, std_thresholds)

    plt.title("ToT vs Charge for N116")
    plt.xlabel("Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    # plt.savefig(f"ToT_vs_Charge_N116.png", dpi=600)
    plt.show()


def HelperPlotErrors(pixel, relative_errors_threshold):

    col_val, row_val = pixel

    plt.scatter(
        np.arange(1, 16.2, 0.2),
        relative_errors_threshold,
        marker="o",
        color="green",
        label=f"Threshold Test Pixel ({col_val}, {row_val})",
    )


def PlotErrors(df_testpulse, dict_pixels):
    relative_errors_testpulse = df_testpulse["stdvTot"] / df_testpulse["meanTot"]

    plt.figure(figsize=(14, 6))
    plt.scatter(
        np.arange(1, 16.2, 0.2),
        relative_errors_testpulse,
        marker="o",
        color="blue",
        label="Test Pulse",
    )
    for keys, df_pixels in dict_pixels.items():
        means_chargecal, std_thresholds = iqr_filtered_stats(df_pixels)
        relative_errors_threshold = [
            s / m if m != 0 else np.nan for m, s in zip(means_chargecal, std_thresholds)
        ]
        HelperPlotErrors(keys, relative_errors_threshold)

    plt.title("Relative Error vs Charge for N116")
    plt.xlabel("Charge [ke]")
    plt.ylim(0, 0.1)
    plt.ylabel("Relative Error")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    # plt.savefig(f"Relative_Error_N116.png", dpi=600)
    plt.show()


def Main(filepath):
    dict_pixels: dict = CreatePixelDataFrames(
        f"Data/Single Pixel Data/Filtered/{filepath}"
    )

    df_testpulse = CreateTestPulseDF("N116")

    # PlotToTvsCharge(df_testpulse, dict_pixels)

    PlotErrors(df_testpulse, dict_pixels)


if __name__ == "__main__":
    Main("SinglePixel.csv")
