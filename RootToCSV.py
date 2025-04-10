import uproot
import pandas as pd
import numpy as np

def ConvertFitData(root_file_path, csv_file_path):
    file = uproot.open(root_file_path)
    ### ----------- FIT DATA -------------
    tree_data = file["fitData"]
    arrays_data = tree_data.arrays()

    # Convert to DataFrame
    df_data = pd.DataFrame({
        "col": arrays_data["col"].to_numpy(),
        "row": arrays_data["row"].to_numpy(),
        "charge": arrays_data["charge"].to_numpy(),
        "meanTot": arrays_data["meanTot"].to_numpy(),
        "stdvTot": arrays_data["stdvTot"].to_numpy(),
        "nhits": arrays_data["nhits"].to_numpy(),
    })

    # Save to CSV
    df_data.to_csv(csv_file_path, index=False)

# =========================Calculating factors===================
THRESHOLDTOT = 150

def FindHighestToT(df, target_col, target_row):
    # Filter for pixel
    pixel_df = df[(df['col'] == target_col) & (df['row'] == target_row)]

    if pixel_df.empty:
        return None

    counts, bin_edges = np.histogram(pixel_df['tot'], bins=301)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Can be higher than 100
    mask = bin_centers > THRESHOLDTOT
    filtered_counts = counts[mask]
    filtered_bins = bin_centers[mask]

    if len(filtered_bins) == 0:
        return None

    # Find Dominant Bin
    max_index = np.argmax(filtered_counts)
    dominant_bin_value = filtered_bins[max_index]

    return dominant_bin_value

def GetCalibrationFactors(df: pd.DataFrame):
    groups = df.groupby("pixel")

    global CorrectionFactors

    CorrectionFactors = {
        pixel: 16.5 / FindHighestToT(group, group["col"].iloc[0], group["row"].iloc[0])
        for pixel, group in groups
        if FindHighestToT(group, group["col"].iloc[0], group["row"].iloc[0]) is not None
    }

def CalculateCharge(df:pd.DataFrame):
    GetCalibrationFactors(df)
    df["correction"] = df["pixel"].apply(lambda pixel: CorrectionFactors.get(pixel, np.nan))
    df["charge"] = df["tot"] * df["correction"]

    return df

# =========================Calculating factors===================

def FilterAndUnwrap(df: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df[df["nhits"] == 1].copy()
    df_filtered = df_filtered.map(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) == 1 else x)
    df_filtered["Raw Charge"] = df_filtered["Raw Charge"].astype(float) / 1000
    return df_filtered

def TransformDataFrame(df_filtered: pd.DataFrame) -> pd.DataFrame:
    df_filtered["pixel"] = list(zip(df_filtered["col"], df_filtered["row"]))
    df_transformed = CalculateCharge(df_filtered)
    return df_transformed.dropna(subset=["charge"])

def ConvertClusterData(filepath: str) -> None:
    filename = filepath.split(".")[0]
    file = uproot.open(f"Data/Am-241 Runs/{filepath}")
    tree = file["clusterTree"]
    
    arrays_data = tree.arrays(["col", "row", "tot", "nhits", "charge"], library="pd")
    df_data = pd.DataFrame({
        "col": arrays_data["col"].to_numpy(),
        "row": arrays_data["row"].to_numpy(),
        "tot": arrays_data["tot"].to_numpy(),
        "nhits": arrays_data["nhits"].to_numpy(),
        "Raw Charge": arrays_data["charge"].to_numpy()
    })

    df_filtered = FilterAndUnwrap(df_data)
    df_transformed = TransformDataFrame(df_filtered)
    df_transformed.to_csv(f"Data/Filtered Calibration Data/{filename}-Charge-Data.csv", index=False, columns = ["charge", "Raw Charge"])

def ConvertToT4Sector(filepath: str) -> None:
    filename = filepath.split(".")[0]
    file = uproot.open(f"Data/Am-241 Runs/{filepath}")
    tree = file["clusterTree"]

    arrays_data = tree.arrays(["col", "row", "tot", "nhits"], library="pd")
    df_data = pd.DataFrame({
        "col": arrays_data["col"].to_numpy(),
        "row": arrays_data["row"].to_numpy(),
        "tot": arrays_data["tot"].to_numpy(),
        "nhits": arrays_data["nhits"].to_numpy()
    })
    df_filtered = df_data[df_data["nhits"] == 1]
    df_filtered = df_filtered.map(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) == 1 else x)

    df_filtered["Top Left"] = df_filtered.loc[(df_filtered["col"] < 224) & (df_filtered["row"] < 256), "tot"]
    df_filtered["Bottom Left"] = df_filtered.loc[(df_filtered["col"] < 224) & (df_filtered["row"] >= 256), "tot"]
    df_filtered["Top Right"] = df_filtered.loc[(df_filtered["col"] >= 224) & (df_filtered["row"] < 256), "tot"]
    df_filtered["Bottom Right"] = df_filtered.loc[(df_filtered["col"] >= 224) & (df_filtered["row"] >= 256), "tot"]
    df_filtered.to_csv(f"Data/4Sector Data/{filename}-ToT4Sector.csv", index=False, columns = ["Top Left", "Bottom Left", "Top Right", "Bottom Right"])

if __name__ == "__main__":

    # for root_file_path in ["N10-250409-113850.root"]:
    #     ConvertClusterData(root_file_path)
    ConvertToT4Sector("N116-250408-123554.root")
    # ConvertToT4Sector("N116-250408-105332.root")