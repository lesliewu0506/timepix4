import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

THRESHOLDS = list(range(1000, 16001, 200))


def CreateDataFrame(filepath):
    df = pd.read_csv(filepath, sep=",", on_bad_lines="skip", encoding="utf-8")
    df.columns = ["Col", "Row", "Charge", "meanTot", "stdvTot", "nhits"]
    df["meanTot"] = df["meanTot"] / 128
    df["stdvTot"] = df["stdvTot"] / 128
    return df


def HelperDFDropper(df):
    for Charge in THRESHOLDS:
        df = df.replace([np.inf, -np.inf], np.nan).dropna(
            subset=[f"col {Charge}", f"row {Charge}", f"Charge {Charge}"]
        )
        df[f"col {Charge}"] = df[f"col {Charge}"].astype(int)
        df[f"row {Charge}"] = df[f"row {Charge}"].astype(int)
    return df


def HelperCreateSortedDataFrames(df):
    sorted_blocks = []
    for Charge in THRESHOLDS:

        df = df.replace([np.inf, -np.inf], np.nan).dropna(
            subset=[f"col {Charge}", f"row {Charge}", f"Charge {Charge}"]
        )

        subset = df[[f"col {Charge}", f"row {Charge}", f"Charge {Charge}"]].copy()
        subset.columns = [f"col {Charge}", f"row {Charge}", f"Charge {Charge}"]
        subset = subset.sort_values(by=[f"col {Charge}", f"row {Charge}"]).reset_index(
            drop=True
        )
        sorted_blocks.append(subset)
    sorted_df = pd.concat(sorted_blocks, axis=1)
    sorted_df = HelperDFDropper(sorted_df)

    return sorted_df


def CreatePixelDataFramesFromSorted(sorted_df):
    pixel_dataframes = {}
    for _, row in sorted_df.iterrows():
        pixel = (row["col 1000"], row["row 1000"])
        # Build a dictionary for the charge values for each threshold
        charge_data = {}
        for threshold in THRESHOLDS:
            charge_data[f"Charge {threshold}"] = row[f"Charge {threshold}"]
        # Append the charge data to the list for this pixel
        if pixel not in pixel_dataframes:
            pixel_dataframes[pixel] = []
        pixel_dataframes[pixel].append(charge_data)

    pixels_to_remove = []
    for pixel, data_list in pixel_dataframes.items():
        df = pd.DataFrame(data_list)

        if len(df) < 400:
            pixels_to_remove.append(pixel)
        else:
            pixel_dataframes[pixel] = df

    for pixel in pixels_to_remove:
        del pixel_dataframes[pixel]

    return pixel_dataframes


def CreatePixelDataFrames(filepaths) -> dict[str, pd.DataFrame]:
    pixel_dataframes = {}

    for filepath in filepaths:

        df = pd.read_csv(f"Data/Single Pixel Data/Filtered/{filepath}")
        sorted_df = HelperCreateSortedDataFrames(df)
        # pixel_dataframes = CreatePixelDataFramesFromSorted(sorted_df)
        pixel_dataframes.update(CreatePixelDataFramesFromSorted(sorted_df))
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
    col, row = pixel
    # Determine the orientation based on sensor dimensions
    if col < 224 and row < 256:
        orientation = "TL"
    elif col >= 224 and row < 256:
        orientation = "TR"
    elif col < 224 and row >= 256:
        orientation = "BL"
    else:
        orientation = "BR"
    # Define sector colors
    sector_colors = {"TL": "red", "TR": "green", "BL": "blue", "BR": "orange"}
    color = sector_colors[orientation]

    # plt.errorbar(
    #     np.arange(1, 16.2, 0.2),
    #     means_threshold,
    #     yerr=std_thresholds,
    #     fmt=".",
    #     color=color,
    #     ecolor=color,
    #     capsize=4,
    #     label=f"Threshold Test Pixel ({col}, {row}, {orientation})",
    # )
    plt.scatter(
        np.arange(1, 16.2, 0.2),
        means_threshold,
        marker="o",
        color=color,
        label=f"Threshold Test Pixel ({col}, {row}, {orientation})",
    )


def PlotToTvsCharge(testpulse_list, dict_pixels):
    # Start Plot
    plt.figure(figsize=(18, 12))

    # for key, df_pixels in dict_pixels.items():
    #     means_chargecal, std_thresholds = iqr_filtered_stats(df_pixels)
    #     HelperPlotToTvsCharge(key, means_chargecal, std_thresholds)
    colors = {"N116_1": "red", "N116_2": "green", "N116_3": "blue"}
    for keys, df in testpulse_list.items():
        plt.scatter(
            np.arange(1, 16.2, 0.2),
            df["meanTot"],
            marker="o",
            color=colors[keys],
            label=f"Test Pulse {keys}",
        )
    # plt.scatter(
    #     df_testpulse["Charge"] / 1000,
    #     df_testpulse["meanTot"],
    #     color="magenta",  # Use a distinct color for test pulse
    #     label="Test Pulse standard",
    #     s=40,
    #     zorder=10,
    # )
    plt.title("ToT vs Charge for N116")
    plt.xlabel("Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"ToT_vs_Charge_N116_differentFits.png", dpi=600)
    plt.show()


def HelperPlotErrors(pixel, relative_errors_threshold):
    col, row = pixel
    # Determine the orientation based on sensor dimensions
    if col < 224 and row < 256:
        orientation = "TL"
    elif col >= 224 and row < 256:
        orientation = "TR"
    elif col < 224 and row >= 256:
        orientation = "BL"
    else:
        orientation = "BR"
    # Define sector colors
    sector_colors = {"TL": "red", "TR": "green", "BL": "blue", "BR": "orange"}
    color = sector_colors[orientation]

    plt.scatter(
        np.arange(1, 16.2, 0.2),
        relative_errors_threshold,
        marker="o",
        color=color,
        label=f"4 Pixel Test Pulse Injection ({col}, {row}, {orientation})",
    )


def PlotErrors(df_testpulse):
    colors = {"N116_1": "red", "N116_2": "green", "N116_3": "blue"}
    plt.figure(figsize=(18, 12))
    # for key, df_pixels in dict_pixels.items():
    #     means_chargecal, std_thresholds = iqr_filtered_stats(df_pixels)
    #     relative_errors_threshold = [
    #         s / m if m != 0 else np.nan for m, s in zip(means_chargecal, std_thresholds)
    #     ]
    #     HelperPlotErrors(key, relative_errors_threshold)

    # Plot test pulse data on top
    for keys, df in df_testpulse.items():
        relative_errors_testpulse = df["stdvTot"] / df["meanTot"]
        plt.scatter(
            np.arange(1, 16.2, 0.2),
            relative_errors_testpulse,
            marker="o",
            color=colors[keys],  # Distinct color for test pulse
            label=f"Test Pulse {keys}",
            zorder=10,
        )

    plt.title("Relative Error vs Charge for N116")
    plt.xlabel("Charge [ke]")
    plt.ylim(0, 0.1)
    plt.ylabel("Relative Error")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"Relative_Error_N116.png", dpi=600)
    plt.show()


def PlotToTHistogram(df):
    plt.figure(figsize=(14, 8))
    plt.hist(df["Charge 13000"], bins=100, color="blue", alpha=0.7)
    plt.xlabel("ToT [25ns]")
    plt.ylabel("Counts")
    plt.title("ToT (319, 280) Charge 13000")

    plt.tight_layout()
    plt.savefig(f"ToT_Histogram13_2.png", dpi=600)
    plt.show()


def Difference(dict_pixels: dict[tuple[int, int], pd.DataFrame]):
    df_testpulse: pd.DataFrame = CreateDataFrame(
        f"Data/Test Pulse Data/fitData_N116_2.csv"
    )
    diff_list = []

    for (col, row), df_pixels in dict_pixels.items():
        means_chargecal, std_thresholds = iqr_filtered_stats(df_pixels)

        filtered_row_testpulse = df_testpulse[
            (df_testpulse["Col"] == col)
            & (df_testpulse["Row"] == row)
            & np.isclose(df_testpulse["Charge"], 16000, atol=100)
        ]

        diff = means_chargecal[-1] - filtered_row_testpulse["meanTot"].values[0]
        diff_list.append(diff)

    plt.figure(figsize=(14, 8))
    plt.hist(diff_list, bins=100, color="blue", alpha=0.7)
    plt.xlabel("Difference")
    plt.ylabel("Counts")
    plt.title("Difference between Charge 16000 and Test Pulse")
    plt.tight_layout()
    plt.savefig(f"Difference_Histogram.png", dpi=600)
    plt.show()


def PlotMultipleToTCharge(dict_pixels):
    df_testpulse: pd.DataFrame = CreateDataFrame(
        f"Data/Test Pulse Data/fitData_N116_2.csv"
    )

    for (col, row), df_pixels in dict_pixels.items():

        filtered_row_testpulse = df_testpulse[
            (df_testpulse["Col"] == col) & (df_testpulse["Row"] == row)
        ]
        means_chargecal, std_thresholds = iqr_filtered_stats(df_pixels)
        plt.figure(figsize=(14, 8))
        HelperPlotToTvsCharge((col, row), means_chargecal, std_thresholds)

        plt.scatter(
            filtered_row_testpulse["Charge"] / 1000,
            filtered_row_testpulse["meanTot"],
            color="magenta",  # Use a distinct color for test pulse
            label="Test Pulse",
            s=40,
            zorder=10,
        )
        plt.title("ToT vs Charge for N116")
        plt.xlabel("Charge [ke]")
        plt.ylabel("ToT [25ns]")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        # plt.savefig(f"ToT_vs_Charge_N116.png", dpi=600)
        plt.show()


def Main(filepaths):
    # dict_pixels: dict = CreatePixelDataFrames(filepaths)

    df_testpulse = CreateTestPulseDF("N116_1")
    df_testpulse_2 = CreateTestPulseDF("N116_2")
    df_testpulse_3 = CreateTestPulseDF("N116_3")
    testpulse_list = {"N116_1" : df_testpulse, "N116_2" : df_testpulse_2, "N116_3" : df_testpulse_3}
    # print(df_testpulse)
    # PlotToTHistogram(dict_pixels[(319, 280)])
    # PlotToTvsCharge(testpulse_list, dict_pixels = None)

    PlotErrors(testpulse_list)
    # Difference(dict_pixels)
    # PlotMultipleToTCharge(dict_pixels)


if __name__ == "__main__":
    filepaths = ["BL.csv", "BR.csv", "TL.csv", "TR.csv"]
    # Main(["TL.csv"])
    Main(filepaths)
