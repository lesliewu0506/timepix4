import pandas as pd
import matplotlib.pyplot as plt
import ast, re
import numpy as np
from scipy.special import erf, erfc
from scipy.optimize import curve_fit


def LoadCSV(filepath):
    df = pd.read_csv(filepath, converters={"pixel": parse_tuple})
    df_filtered = df[df["pixel"].apply(lambda t: all(x % 10 == 0 for x in t))]
    return df_filtered


def parse_tuple(s):
    tup = ast.literal_eval(s)
    return tuple(int(x) for x in tup)


def PlotOnePixel(filepath):

    df_filtered = LoadCSV(filepath)

    row_data = df_filtered[df_filtered["pixel"] == (0, 0)].iloc[0]
    threshold_cols = [col for col in df_filtered.columns if col.startswith("threshold")]

    x_values = [
        int(col.split()[1]) if " " in col else int(col.replace("threshold", ""))
        for col in threshold_cols
    ]
    y_values = row_data[threshold_cols].values
    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values, marker="o", linestyle="-")
    plt.axhline(y=500, color="red", linestyle="--")
    plt.xlabel("Threshold")
    plt.ylabel("Counts for pixel (0, 0)")
    plt.title("Counts for pixel (0, 0) vs Threshold")
    plt.xticks(x_values)  # Ensure x-ticks are set on the exact thresholds
    plt.savefig("Pixel_0_0.png", dpi=600)
    plt.show()


def PlotAveragePixels(filepaths: list[str]) -> None:
    if not filepaths:
        print("No filepaths provided.")
        return

    plt.figure(figsize=(12, 8))
    legend_labels = []

    df_first = LoadCSV(filepaths[0])
    threshold_cols = [col for col in df_first.columns if col.startswith("threshold")]
    x_values = [
        int(col.split()[1]) if " " in col else int(col.replace("threshold", ""))
        for col in threshold_cols
    ]

    # Optional: A list of colors. If more files than colors, matplotlib will cycle through.
    colors = ["blue", "red", "green", "purple"]

    for index, filepath in enumerate(filepaths):
        sensor = filepath.split("/")[-2]
        df = LoadCSV(filepath)
        y_values = df[threshold_cols].mean().values
        plt.plot(
            x_values,
            y_values,
            marker="o",
            linestyle="-",
            color=colors[index % len(colors)],
        )
        legend_labels.append(sensor)

    plt.axhline(
        y=500, color="black", linestyle="--"
    )  # Common horizontal line for reference
    plt.xlabel("Threshold")
    plt.ylabel("Average Counts across all pixels")
    plt.title("Average Counts vs Threshold for Multiple Sensors")
    plt.xticks(x_values)
    plt.legend(legend_labels)
    # You can adjust the filename as needed:
    plt.savefig("Multiple_Sensors_Average_Pixels.png", dpi=600)
    plt.show()


def PlotSectorAverages(filepaths: list[str]) -> None:
    if not filepaths:
        print("No filepaths provided.")
        return

    df_first = LoadCSV(filepaths[0])
    threshold_cols = [col for col in df_first.columns if col.startswith("threshold")]
    x_values = [
        int(col.split()[1]) if " " in col else int(col.replace("threshold", ""))
        for col in threshold_cols
    ]

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs = axs.flatten()

    sector_titles = {0: "Top Left", 1: "Top Right", 2: "Bottom Left", 3: "Bottom Right"}

    for filepath in filepaths:
        sensor = filepath.split("/")[-2]
        df = LoadCSV(filepath)

        top_left = df[df["pixel"].apply(lambda p: p[0] < 224 and p[1] < 256)]
        top_right = df[df["pixel"].apply(lambda p: p[0] >= 224 and p[1] < 256)]
        bottom_left = df[df["pixel"].apply(lambda p: p[0] < 224 and p[1] >= 256)]
        bottom_right = df[df["pixel"].apply(lambda p: p[0] >= 224 and p[1] >= 256)]

        avg_top_left = [top_left[col].mean() for col in threshold_cols]
        avg_top_right = [top_right[col].mean() for col in threshold_cols]
        avg_bottom_left = [bottom_left[col].mean() for col in threshold_cols]
        avg_bottom_right = [bottom_right[col].mean() for col in threshold_cols]

        axs[0].plot(x_values, avg_top_left, marker="o", linestyle="-", label=sensor)
        axs[1].plot(x_values, avg_top_right, marker="o", linestyle="-", label=sensor)
        axs[2].plot(x_values, avg_bottom_left, marker="o", linestyle="-", label=sensor)
        axs[3].plot(x_values, avg_bottom_right, marker="o", linestyle="-", label=sensor)

    for i, ax in enumerate(axs):
        ax.set_title(sector_titles[i])
        ax.set_xlabel("Threshold")
        ax.set_ylabel("Average Hits")
        ax.axhline(y=500, color="red", linestyle="--")
        ax.legend()

    plt.suptitle("Sector Averages vs Threshold for Multiple Sensors")
    plt.tight_layout()
    plt.savefig("Multiple_Sensors_Sector_Averages.png", dpi=600)
    plt.show()


def ExtrapolateThreshold(row):
    target = 500
    x1 = None
    y1 = None
    x2 = None
    y2 = None

    for col in threshold_columns:
        thr_num = int(re.findall(r"\d+", col)[0])
        val = row[col]

        if val >= target:
            x1, y1 = thr_num, val

        elif val < target:
            x2, y2 = thr_num, val

            if x2 is not None:
                break
    if x1 is None or x2 is None:
        return None
    return x1 + (target - y1) * (x2 - x1) / (y2 - y1)


def ExtrapolateThresholds(df: pd.DataFrame):
    global threshold_columns
    threshold_columns = [col for col in df.columns if col.startswith("threshold")]
    threshold_columns.sort(key=lambda x: int(re.findall(r"\d+", x)[0]))
    df["extrapolated_threshold"] = df.apply(ExtrapolateThreshold, axis=1)
    return df["extrapolated_threshold"]


def PlotThresholdDistribution(filepath):
    sensor = filepath.split("/")[-2]
    df = LoadCSV(filepath)
    df_thresholds = ExtrapolateThresholds(df)

    plt.figure(figsize=(12, 8))
    plt.hist(df_thresholds, bins=26, color="blue", alpha=0.7, range=(4000, 5300))
    plt.xlabel("Extrapolated Threshold")
    plt.ylabel("Frequency")
    plt.title(f"{sensor} Distribution of Extrapolated Thresholds")
    plt.show()


def PlotThresholdSector(filepath):
    sensor = filepath.split("/")[-2]

    df = LoadCSV(filepath)
    sectors = {
        "Top Left": df[df["pixel"].apply(lambda p: p[0] < 224 and p[1] < 256)],
        "Top Right": df[df["pixel"].apply(lambda p: p[0] >= 224 and p[1] < 256)],
        "Bottom Left": df[df["pixel"].apply(lambda p: p[0] < 224 and p[1] >= 256)],
        "Bottom Right": df[df["pixel"].apply(lambda p: p[0] >= 224 and p[1] >= 256)],
    }

    # Create a 2x2 subplot figure
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs = axs.flatten()

    for ax, (name, sector_df) in zip(axs, sectors.items()):
        df_thresholds = ExtrapolateThresholds(sector_df)

        ax.hist(df_thresholds, bins=13, color="blue", alpha=0.7, range=(4000, 5300))
        ax.set_title(f"Distribution of Extrapolated Thresholds - {name}")
        ax.set_xlabel("Extrapolated Threshold")
        ax.set_ylabel("Frequency")
    plt.suptitle(f"{sensor} Distribution of Extrapolated Thresholds by Sector")
    plt.tight_layout()
    plt.savefig(f"{sensor}_ThresholdSectors_Subplots.png", dpi=600)
    plt.show()


def PlotThresholdSector16(filepath):
    sensor = filepath.split("/")[-2]
    df = LoadCSV(filepath)
    x_boundaries = [0, 112, 224, 336, 448]
    y_boundaries = [0, 128, 256, 384, 512]

    sectors = {}
    for i in range(4):
        for j in range(4):
            sector_name = f"Sector (Column: {x_boundaries[j]}-{x_boundaries[j+1]}, Row: {y_boundaries[i]}-{y_boundaries[i+1]})"
            sector_df = df[
                df["pixel"].apply(
                    lambda p: p[0] >= x_boundaries[j]
                    and p[0] < x_boundaries[j + 1]
                    and p[1] >= y_boundaries[i]
                    and p[1] < y_boundaries[i + 1]
                )
            ]
            sectors[sector_name] = sector_df

    # Create a 4x4 subplot figure for histograms
    fig, axs = plt.subplots(4, 4, figsize=(16, 16))
    axs = axs.flatten()

    # Iterate through each sector and plot its histogram of extrapolated thresholds
    for ax, (name, sector_df) in zip(axs, sectors.items()):
        df_thresholds = ExtrapolateThresholds(sector_df)
        ax.hist(df_thresholds, bins=13, color="blue", alpha=0.7, range=(4000, 5300))
        ax.set_title(f"{name}")
        ax.set_xlabel("Extrapolated Threshold")
        ax.set_ylabel("Frequency")

    plt.suptitle(f"{sensor} Distribution of Extrapolated Thresholds by Sector")
    plt.tight_layout()
    plt.savefig(f"{sensor}_ThresholdSectors_Subplots.png", dpi=600)
    plt.show()


def PlotThresholdDistributionMultiple(filepaths: list[str]) -> None:
    if not filepaths:
        print("No filepaths provided.")
        return

    # Prepare lists to accumulate the sensor data and labels
    sensor_data = []
    sensor_labels = []
    colors = [
        "lightblue",
        "lightgreen",
        "lightpink",
        "lightyellow",
        "lavender",
        "lightcoral",
        "wheat",
        "plum",
    ]

    for index, filepath in enumerate(filepaths):
        sensor = filepath.split("/")[-2]
        sensor_labels.append(sensor)
        df = LoadCSV(filepath)
        # Compute extrapolated thresholds and drop NaNs
        df_thresholds = ExtrapolateThresholds(df).dropna().values
        sensor_data.append(df_thresholds)

    plt.figure(figsize=(12, 8))
    bp = plt.boxplot(sensor_data, labels=sensor_labels, patch_artist=True)
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(colors[i % len(colors)])
    plt.xlabel("Sensor")
    plt.ylabel("Extrapolated Threshold")
    plt.title("Distribution of Extrapolated Thresholds for Multiple Sensors")
    plt.tight_layout()
    plt.savefig("Multiple_Sensors_Threshold_Distribution_BoxPlot.png", dpi=600)
    plt.show()


def PlotThresholdSectorMultiple(filepaths: list[str]) -> None:
    if not filepaths:
        print("No filepaths provided.")
        return

    # Define sector conditions
    sector_titles = {
        "Top Left": lambda p: p[0] < 224 and p[1] < 256,
        "Top Right": lambda p: p[0] >= 224 and p[1] < 256,
        "Bottom Left": lambda p: p[0] < 224 and p[1] >= 256,
        "Bottom Right": lambda p: p[0] >= 224 and p[1] >= 256,
    }

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs = axs.flatten()

    # Dictionary to accumulate thresholds per sensor for each sector
    sector_data = {sector: {} for sector in sector_titles.keys()}

    for filepath in filepaths:
        sensor = filepath.split("/")[-2]
        df = LoadCSV(filepath)
        for sector_name, condition in sector_titles.items():
            sector_df = df[df["pixel"].apply(condition)]
            # Compute extrapolated thresholds and drop NaNs
            df_thresholds = ExtrapolateThresholds(sector_df).dropna().values
            if sensor in sector_data[sector_name]:
                # Concatenate new values with existing array
                sector_data[sector_name][sensor] = np.concatenate(
                    (sector_data[sector_name][sensor], df_thresholds)
                )
            else:
                sector_data[sector_name][sensor] = df_thresholds

    for ax_index, (sector_name, sensors_data) in enumerate(sector_data.items()):
        data_to_plot = [sensors_data[sensor] for sensor in sensors_data]
        labels = list(sensors_data.keys())
        bp = axs[ax_index].boxplot(data_to_plot, labels=labels, patch_artist=True)
        # Define a list of colors to assign to boxes, cycling if necessary
        box_colors = [
            "lightblue",
            "lightgreen",
            "lightpink",
            "lightyellow",
            "lavender",
            "lightcoral",
            "wheat",
            "plum",
        ]
        for i, patch in enumerate(bp["boxes"]):
            patch.set_facecolor(box_colors[i % len(box_colors)])
        axs[ax_index].set_title(f"Extrapolated Thresholds - {sector_name}")
        axs[ax_index].set_xlabel("Sensor")
        axs[ax_index].set_ylabel("Extrapolated Threshold")

    plt.suptitle(
        "Distribution of Extrapolated Thresholds by Sector for Multiple Sensors"
    )
    plt.tight_layout()
    plt.savefig("Multiple_Sensors_ThresholdSectors_BoxPlots.png", dpi=600)
    plt.show()


def PlotThresholdSector16Multiple(filepaths: list[str]) -> None:
    if not filepaths:
        print("No filepaths provided.")
        return

    x_boundaries = [0, 112, 224, 336, 448]
    y_boundaries = [0, 128, 256, 384, 512]

    # Create a dictionary for 16 sectors with corresponding lambda conditions
    sectors = {}
    for i in range(4):
        for j in range(4):
            sector_name = f"Sector (Col: {x_boundaries[j]}-{x_boundaries[j+1]}, Row: {y_boundaries[i]}-{y_boundaries[i+1]})"
            sectors[sector_name] = (
                lambda p, xb=x_boundaries[j], xb_next=x_boundaries[
                    j + 1
                ], yb=y_boundaries[i], yb_next=y_boundaries[i + 1]: (
                    p[0] >= xb and p[0] < xb_next and p[1] >= yb and p[1] < yb_next
                )
            )

    # Dictionary to accumulate thresholds per sensor for each sector
    sector_data = {sector: {} for sector in sectors.keys()}

    for filepath in filepaths:
        sensor = filepath.split("/")[-2]
        df = LoadCSV(filepath)
        for sector_name, condition in sectors.items():
            sector_df = df[df["pixel"].apply(condition)]
            df_thresholds = ExtrapolateThresholds(sector_df).dropna().values
            if sensor in sector_data[sector_name]:
                sector_data[sector_name][sensor] = np.concatenate(
                    (sector_data[sector_name][sensor], df_thresholds)
                )
            else:
                sector_data[sector_name][sensor] = df_thresholds

    # Create a 4x4 subplot figure for box plots
    fig, axs = plt.subplots(4, 4, figsize=(16, 16))
    axs = axs.flatten()

    for ax_index, (sector_name, sensors_data) in enumerate(sector_data.items()):
        data_to_plot = [sensors_data[sensor] for sensor in sensors_data]
        labels = list(sensors_data.keys())
        bp = axs[ax_index].boxplot(data_to_plot, labels=labels, patch_artist=True)
        # Define a list of colors to assign to boxes, cycling if necessary
        box_colors = [
            "lightblue",
            "lightgreen",
            "lightpink",
            "lightyellow",
            "lavender",
            "lightcoral",
            "wheat",
            "plum",
        ]
        for i, patch in enumerate(bp["boxes"]):
            patch.set_facecolor(box_colors[i % len(box_colors)])
        axs[ax_index].set_title(sector_name)
        axs[ax_index].set_xlabel("Sensor")
        axs[ax_index].set_ylabel("Extrapolated Threshold")

    plt.suptitle(
        "Distribution of Extrapolated Thresholds by 16 Sectors for Multiple Sensors"
    )
    plt.tight_layout()
    plt.savefig("Multiple_Sensors_Threshold16Sectors_BoxPlots.png", dpi=600)
    plt.show()


def error_func(x, mu, sigma):
    return 500 * (erf((mu - x) / (np.sqrt(2) * sigma))) + 500


def error_func_no_C(x, A, mu, sigma, y0):
    return y0 + 0.5 * A * erfc((x - mu) / (sigma * np.sqrt(2)))


def SingleErrorFit(filepaths: list[str]) -> None:
    all_sigmas = []
    sensors = []
    for filepath in filepaths:
        sensor = filepath.split("/")[-2]
        sensors.append(sensor)
        df = LoadCSV(filepath)
        threshold_columns = [col for col in df.columns if col.startswith("threshold")]
        threshold_vals = [int(c.split()[1]) for c in threshold_columns]
        sigma_list = []
        for index, row in df.iterrows():
            pixel = row["pixel"]

            ydata = row[threshold_columns].values.astype(float)
            xdata = threshold_vals
            xdata_2 = np.arange(4000, 5301, 5)
            try:
                popt, _ = curve_fit(
                    error_func_no_C,
                    xdata,
                    ydata,
                    p0=[1000, 4600, 75, 1000],
                    maxfev=20000,
                )
                # Create a legend label with fitted parameters
                fit_label = f"Fit: sigma={popt[2]:.2f}"
                sigma = popt[2]
                sigma_list.append(sigma)
                df_2 = df[(df["pixel"] == (pixel))].iloc[0]
                y_values = df_2.drop(["pixel"]).values.astype(float)
                plt.figure(figsize=(12, 8))
                plt.plot(xdata, y_values, marker="o", linestyle="-")
                plt.plot(
                    xdata_2,
                    error_func_no_C(xdata_2, *popt),
                    color="red",
                    label=fit_label,
                )
                plt.xlabel("Threshold")
                plt.ylabel("Counts")
                plt.title(f"Counts vs Threshold for pixel {pixel}")

                plt.legend()
                # plt.savefig(f"Counts_vs_Threshold_{sensor}_{pixel}.png", dpi=600)
                plt.show()
            except (RuntimeError, ValueError):
                pass
        all_sigmas.append(sigma_list)

    # Now plot a 2×2 grid of histograms
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    axs = axs.flatten()
    for ax, sigmas, sensor in zip(axs, all_sigmas, sensors):
        if sensor == "N116_2":
            ax.hist(sigmas, bins=15, alpha=0.7)
        else:
            ax.hist(sigmas, bins=451, alpha=0.7)
        ax.set_xlim(0, 150)
        ax.set_ylim(0, 800)
        ax.set_xlabel("Sigma")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Sigma Distribution for {sensor}")
    plt.tight_layout()
    plt.savefig("Sigma_Distribution_Grid.png", dpi=600)
    plt.show()


def MultipleErrorFit(filepaths: list[str]) -> None:
    all_sigmas = []
    sensors = []
    filepath_n10 = filepaths[0]
    filepath_n116 = filepaths[1]
    sensor_n10 = filepath_n10.split("/")[-2]
    sensor_n116 = filepath_n116.split("/")[-2]

    sensors.append(sensor_n10)
    sensors.append(sensor_n116)
    df_n116 = LoadCSV(filepath_n116)
    df_n10 = LoadCSV(filepath_n10)
    threshold_columns_n10 = [col for col in df_n10.columns if col.startswith("threshold")]
    threshold_columns_n116 = [col for col in df_n116.columns if col.startswith("threshold")]
    threshold_vals_n10 = [int(c.split()[1]) for c in threshold_columns_n10]
    threshold_vals_n116 = [int(c.split()[1]) for c in threshold_columns_n116]
    sigma_list_n10 = []
    sigma_list_n116 = []

    for (index10, row10), (index116, row116) in zip(df_n10.iterrows(), df_n116.iterrows()):
        pixel_n10 = row10["pixel"]
        pixel_n116 = row116["pixel"]
        ydata_n10 = row10[threshold_columns_n10].values.astype(float)
        ydata_n116 = row116[threshold_columns_n116].values.astype(float)
        xdata_n10 = threshold_vals_n10
        xdata_n116 = threshold_vals_n116
        xdata_2_n10 = np.arange(4000, 5301, 5)
        xdata_2_n116 = np.arange(4000, 5301, 5)
        plt.figure(figsize=(12, 8))
        try:
            popt, _ = curve_fit(
                error_func_no_C,
                xdata_n10,
                ydata_n10,
                p0=[1000, 4600, 75, 1000],
                maxfev=20000,
            )
            # Create a legend label with fitted parameters
            fit_label = f"Fit: sigma={popt[2]:.2f}"
            sigma = popt[2]
            sigma_list_n10.append(sigma)
            df_2 = df_n10[(df_n10["pixel"] == (pixel_n10))].iloc[0]
            y_values = df_2.drop(["pixel"]).values.astype(float)
            plt.plot(xdata_n10, y_values, marker="o", linestyle="-", label = "N10")
            plt.plot(
                xdata_2_n10,
                error_func_no_C(xdata_2_n10, *popt),
                color="red",
                label=fit_label,
            )
            plt.xlabel("Threshold")
            plt.ylabel("Counts")

            plt.legend()

        except (RuntimeError, ValueError):
            pass

        try:
            popt, _ = curve_fit(
                error_func_no_C,
                xdata_n116,
                ydata_n116,
                p0=[1000, 4600, 75, 1000],
                maxfev=20000,
            )
            # Create a legend label with fitted parameters
            fit_label = f"Fit: sigma={popt[2]:.2f}"
            sigma = popt[2]
            sigma_list_n116.append(sigma)
            df_2 = df_n116[(df_n116["pixel"] == (pixel_n116))].iloc[0]
            y_values = df_2.drop(["pixel"]).values.astype(float)
            plt.plot(xdata_n116, y_values, marker="o", linestyle="-", label = "N116")
            plt.plot(
                xdata_2_n116,
                error_func_no_C(xdata_2_n116, *popt),
                color="green",
                label=fit_label,
            )
            plt.xlabel("Threshold")
            plt.ylabel("Counts")

            plt.legend()
        except (RuntimeError, ValueError):
            pass
        plt.show()

if __name__ == "__main__":
    # N116 = "Data/Threshold Test Data/N116/FinalHits.csv"
    N112 = "Data/Threshold Test Data/N112/FinalHits.csv"
    N10 = "Data/Threshold Test Data/N10/FinalHits.csv"
    N113 = "Data/Threshold Test Data/N113/FinalHits.csv"
    N116 = "Data/Threshold Test Data/N116_2/FinalHits.csv"
    # filepaths = [N10, N112, N113, N116]
    # filepaths = [N116]
    filepaths = [N10, N116]

    # PlotAveragePixels(filepaths)
    # PlotSectorAverages(filepaths)
    # PlotThresholdDistributionMultiple(filepaths)
    # PlotThresholdSectorMultiple(filepaths)
    # PlotThresholdSector16Multiple(filepaths)
    # SingleErrorFit(filepaths)
    MultipleErrorFit(filepaths)
