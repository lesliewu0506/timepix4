import pandas as pd
import matplotlib.pyplot as plt
import ast, re

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
    
    x_values = [int(col.split()[1]) if " " in col else int(col.replace("threshold", "")) for col in threshold_cols]
    y_values = row_data[threshold_cols].values
    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values, marker="o", linestyle="-")
    plt.axhline(y=500, color='red', linestyle='--')
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
    x_values = [int(col.split()[1]) if " " in col else int(col.replace("threshold", "")) for col in threshold_cols]

    # Optional: A list of colors. If more files than colors, matplotlib will cycle through.
    colors = ['blue', 'red', 'green', 'purple']
    
    for index, filepath in enumerate(filepaths):
        sensor = filepath.split("/")[-2]
        df = LoadCSV(filepath)
        y_values = df[threshold_cols].mean().values
        plt.plot(x_values, y_values, marker="o", linestyle="-", color=colors[index % len(colors)])
        legend_labels.append(sensor)
        
    plt.axhline(y=500, color='black', linestyle='--')  # Common horizontal line for reference
    plt.xlabel("Threshold")
    plt.ylabel("Average Counts across all pixels")
    plt.title("Average Counts vs Threshold for Multiple Sensors")
    plt.xticks(x_values)
    plt.legend(legend_labels)
    # You can adjust the filename as needed:
    plt.savefig("Multiple_Sensors_Average_Pixels.png", dpi=600)
    plt.show()

def PlotSectorAverages(filepath):
    sensor = filepath.split("/")[-2]
    df = LoadCSV(filepath)
    # Identify threshold columns (assumes columns named like 'threshold 4000', etc.)
    threshold_columns = [col for col in df.columns if col.startswith("threshold")]
    
    # Extract x-axis values from threshold column names
    x_values = [int(col.split()[1]) if " " in col else int(col.replace("threshold", "")) for col in threshold_columns]
    
    # Define sector filters based on the 'pixel' column
    top_left = df[df["pixel"].apply(lambda p: p[0] < 224 and p[1] < 256)]
    top_right = df[df["pixel"].apply(lambda p: p[0] >= 224 and p[1] < 256)]
    bottom_left = df[df["pixel"].apply(lambda p: p[0] < 224 and p[1] >= 256)]
    bottom_right = df[df["pixel"].apply(lambda p: p[0] > 224 and p[1] >= 256)]
    
    # Function to compute averages for each threshold column in a given DataFrame
    def compute_average(sector_df):
        return [sector_df[col].mean() for col in threshold_columns]
    
    avg_top_left = compute_average(top_left)
    avg_top_right = compute_average(top_right)
    avg_bottom_left = compute_average(bottom_left)
    avg_bottom_right = compute_average(bottom_right)
    
    # Create a 2x2 subplot figure to plot each sector
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    axs[0, 0].plot(x_values, avg_top_left, marker='o', linestyle='-')
    axs[0, 0].set_title("Top Left")
    axs[0, 0].set_xlabel("Threshold")
    axs[0, 0].set_ylabel("Average Hits")
    axs[0, 0].axhline(y=500, color='red', linestyle='--')
    
    axs[0, 1].plot(x_values, avg_top_right, marker='o', linestyle='-')
    axs[0, 1].set_title("Top Right")
    axs[0, 1].set_xlabel("Threshold")
    axs[0, 1].set_ylabel("Average Hits")
    axs[0, 1].axhline(y=500, color='red', linestyle='--')
    
    axs[1, 0].plot(x_values, avg_bottom_left, marker='o', linestyle='-')
    axs[1, 0].set_title("Bottom Left")
    axs[1, 0].set_xlabel("Threshold")
    axs[1, 0].set_ylabel("Average Hits")
    axs[1, 0].axhline(y=500, color='red', linestyle='--')
    
    axs[1, 1].plot(x_values, avg_bottom_right, marker='o', linestyle='-')
    axs[1, 1].set_title("Bottom Right")
    axs[1, 1].set_xlabel("Threshold")
    axs[1, 1].set_ylabel("Average Hits")
    axs[1, 1].axhline(y=500, color='red', linestyle='--')
    plt.suptitle(f"{sensor} Sector Averages vs Threshold")
    plt.tight_layout()
    plt.savefig(f"{sensor}_Sector_Averages.png", dpi=600)
    plt.show()

def ExtrapolateThreshold(row):
    target = 500
    x1 = None
    y1 = None
    x2 = None
    y2 = None

    for col in threshold_columns:
        thr_num = int(re.findall(r'\d+', col)[0])
        val = row[col]
        
        if val >= target:
            x1, y1 = thr_num, val

        elif val < target:
            x2, y2 = thr_num, val

            if x2 is not None:
                break
    if x1 is None or x2 is None:
        return None
    return (x1 + (target - y1) * (x2 - x1) / (y2 - y1))

def ExtrapolateThresholds(df: pd.DataFrame):
    global threshold_columns
    threshold_columns = [col for col in df.columns if col.startswith("threshold")]
    threshold_columns.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    df["extrapolated_threshold"] = df.apply(ExtrapolateThreshold, axis=1)
    return df["extrapolated_threshold"]

def PlotThresholdDistribution(filepath):
    sensor = filepath.split("/")[-2]
    df = LoadCSV(filepath)
    df_thresholds = ExtrapolateThresholds(df)

    plt.figure(figsize=(12, 8))
    plt.hist(df_thresholds, bins=26, color='blue', alpha=0.7, range = (4000, 5300))
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
        "Bottom Right": df[df["pixel"].apply(lambda p: p[0] >= 224 and p[1] >= 256)]
    }
    
    # Create a 2x2 subplot figure
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs = axs.flatten()
    
    for ax, (name, sector_df) in zip(axs, sectors.items()):
        df_thresholds = ExtrapolateThresholds(sector_df)
        
        ax.hist(df_thresholds, bins=13, color='blue', alpha=0.7, range=(4000, 5300))
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
            sector_df = df[df["pixel"].apply(lambda p: p[0] >= x_boundaries[j] and p[0] < x_boundaries[j+1] and p[1] >= y_boundaries[i] and p[1] < y_boundaries[i+1])]
            sectors[sector_name] = sector_df

    # Create a 4x4 subplot figure for histograms
    fig, axs = plt.subplots(4, 4, figsize=(16, 16))
    axs = axs.flatten()
    
    # Iterate through each sector and plot its histogram of extrapolated thresholds
    for ax, (name, sector_df) in zip(axs, sectors.items()):
        df_thresholds = ExtrapolateThresholds(sector_df)
        ax.hist(df_thresholds, bins=13, color='blue', alpha=0.7, range=(4000, 5300))
        ax.set_title(f"{name}")
        ax.set_xlabel("Extrapolated Threshold")
        ax.set_ylabel("Frequency")

    plt.suptitle(f"{sensor} Distribution of Extrapolated Thresholds by Sector")
    plt.tight_layout()
    plt.savefig(f"{sensor}_Threshold16Sectors_Subplots.png", dpi=600)
    plt.show()

if __name__ == "__main__":
    filepath = "Data/Threshold Test Data/N116/FinalHits.csv"
    filepath2 = "Data/Threshold Test Data/N112/FinalHits.csv"
    # PlotOnePixel(filepath)
    # PlotThresholdDistribution(filepath)

    PlotAveragePixels([filepath, filepath2])
    # PlotSectorAverages(filepath)
    # PlotThresholdSector(filepath)
    # PlotThresholdSector16(filepath)