import pandas as pd
import matplotlib.pyplot as plt
import ast, re
import numpy as np


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


if __name__ == "__main__":
    N116 = "Data/Threshold Test Data/N116/FinalHits.csv"
    N112 = "Data/Threshold Test Data/N112/FinalHits.csv"
    N10 = "Data/Threshold Test Data/N10/FinalHits.csv"
    N113 = "Data/Threshold Test Data/N113/FinalHits.csv"
    filepaths = [N10, N112, N113, N116]

    # PlotAveragePixels(filepaths)
    # PlotSectorAverages(filepaths)
    # PlotThresholdDistributionMultiple(filepaths)
    # PlotThresholdSectorMultiple(filepaths)
    PlotThresholdSector16Multiple(filepaths)
