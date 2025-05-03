import uproot, os, ast
import pandas as pd
import numpy as np

# =========================Calculating factors===================
THRESHOLDTOT = 150


def FindHighestToT(df, target_col, target_row):
    # Filter for pixel
    pixel_df = df[(df["col"] == target_col) & (df["row"] == target_row)]

    if pixel_df.empty:
        return None
    mask = pixel_df["tot"] > THRESHOLDTOT
    filtered_tot = pixel_df.loc[mask, "tot"]
    if filtered_tot.empty:
        return None
    return filtered_tot.mean()
    # counts, bin_edges = np.histogram(pixel_df["tot"], bins=3011=)

    # bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # # Can be higher than 100
    # mask = bin_centers > THRESHOLDTOT
    # filtered_counts = counts[mask]
    # filtered_bins = bin_centers[mask]

    # if len(filtered_bins) == 0:
    #     return None

    # # Find Dominant Bin
    # max_index = np.argmax(filtered_counts)
    # dominant_bin_value = filtered_bins[max_index]

    # return dominant_bin_value


def GetCalibrationFactors(df: pd.DataFrame):
    groups = df.groupby("pixel")

    global CorrectionFactors

    CorrectionFactors = {
        pixel: 16.5 / FindHighestToT(group, group["col"].iloc[0], group["row"].iloc[0])
        for pixel, group in groups
        if FindHighestToT(group, group["col"].iloc[0], group["row"].iloc[0]) is not None
    }


def CalculateCharge(df: pd.DataFrame):
    GetCalibrationFactors(df)
    df["correction"] = df["pixel"].apply(
        lambda pixel: CorrectionFactors.get(pixel, np.nan)
    )
    df["charge"] = df["tot"] * df["correction"]

    return df


# =========================Calculating factors===================


def FilterAndUnwrap(df: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df[df["nhits"] == 1].copy()
    df_filtered = df_filtered.map(
        lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) == 1 else x
    )
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
    df_data = pd.DataFrame(
        {
            "col": arrays_data["col"].to_numpy(),
            "row": arrays_data["row"].to_numpy(),
            "tot": arrays_data["tot"].to_numpy(),
            "nhits": arrays_data["nhits"].to_numpy(),
            "Raw Charge": arrays_data["charge"].to_numpy(),
        }
    )

    df_filtered = FilterAndUnwrap(df_data)
    df_filtered.to_csv(
        f"Data/Filtered Calibration Data/{filename}-Charge-Data.csv",)
    # df_transformed = TransformDataFrame(df_filtered)
    # df_transformed["correction"] = df_transformed["pixel"].apply(
    #     lambda pixel: CorrectionFactors.get(pixel, np.nan)
    # )
    # df_correction = pd.DataFrame(list(CorrectionFactors.items()), columns=["pixel", "correction"])

    # df_correction.to_csv(f"Data/Filtered Calibration Data/{filename}-CorrectionFactors.csv", index=False)
    # df_transformed.to_csv(
    #     f"Data/Filtered Calibration Data/{filename}-Charge-Data.csv", index=False
    # )


def ConvertToT4Sector(filepath: str) -> None:
    filename = filepath.split(".")[0]
    file = uproot.open(f"Data/Am-241 Runs/{filepath}")
    tree = file["clusterTree"]

    arrays_data = tree.arrays(["col", "row", "charge", "nhits"], library="pd")
    df_data = pd.DataFrame(
        {
            "col": arrays_data["col"].to_numpy(),
            "row": arrays_data["row"].to_numpy(),
            "charge": arrays_data["charge"].to_numpy(),
            "nhits": arrays_data["nhits"].to_numpy(),
        }
    )
    df_filtered = df_data[df_data["nhits"] == 1]
    df_filtered = df_filtered.map(
        lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) == 1 else x
    )

    df_filtered["Top Left"] = (
        df_filtered.loc[
            (df_filtered["col"] < 224) & (df_filtered["row"] < 256), "charge"
        ]
        / 1000
    )
    df_filtered["Bottom Left"] = (
        df_filtered.loc[
            (df_filtered["col"] < 224) & (df_filtered["row"] >= 256), "charge"
        ]
        / 1000
    )
    df_filtered["Top Right"] = (
        df_filtered.loc[
            (df_filtered["col"] >= 224) & (df_filtered["row"] < 256), "charge"
        ]
        / 1000
    )
    df_filtered["Bottom Right"] = (
        df_filtered.loc[
            (df_filtered["col"] >= 224) & (df_filtered["row"] >= 256), "charge"
        ]
        / 1000
    )
    df_filtered.to_csv(
        f"Data/4Sector Data/{filename}-Charge4Sector.csv",
        index=False,
        columns=["Top Left", "Bottom Left", "Top Right", "Bottom Right"],
    )


def to_scalar(x):
    # If x has a tolist() method, convert it to a list
    if hasattr(x, "tolist"):
        x = x.tolist()
    # If x is a list or tuple of length 1, recursively extract the element
    if isinstance(x, (list, tuple)) and len(x) == 1:
        return to_scalar(x[0])
    # If x is a numpy scalar, convert to Python scalar
    if isinstance(x, np.generic):
        return x.item()
    return x


def Threshold(folder_path: str) -> None:
    # List all files in the directory
    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".root")])

    # Define threshold values from 4000 to 5300 in steps of 100 (14 values total)
    thresholds = list(range(4000, 5301, 50))
    if len(file_list) != len(thresholds):
        print(
            "Warning: Number of files does not match the expected number of threshold values."
        )

    merged_df = None

    for file_name, threshold_val in zip(file_list, thresholds):
        print(f"Start processing file: {file_name} with threshold: {threshold_val}")

        full_path = os.path.join(folder_path, file_name)
        file = uproot.open(full_path)
        tree = file["clusterTree"]

        arrays_data = tree.arrays(["col", "row", "nhits"], library="pd")

        col_list = [to_scalar(item) for item in arrays_data["col"]]
        row_list = [to_scalar(item) for item in arrays_data["row"]]
        nhits_list = [to_scalar(item) for item in arrays_data["nhits"]]

        df_data = pd.DataFrame({"col": col_list, "row": row_list, "nhits": nhits_list})

        # Filter rows where nhits equals 1
        df_filtered = df_data[df_data["nhits"] == 1]

        # Group by 'col' and 'row' and sum the nhits
        df_grouped = df_filtered.groupby(["col", "row"], as_index=False)["nhits"].sum()

        # Create a 'pixel' column as a tuple of (col, row)
        df_grouped["pixel"] = list(zip(df_grouped["col"], df_grouped["row"]))

        # Retain only the 'pixel' and the summed 'nhits'
        df_grouped = df_grouped[["pixel", "nhits"]]

        # Rename the 'nhits' column to include the threshold value (e.g., 'threshold4000')
        threshold_col_name = f"threshold {threshold_val}"
        df_grouped = df_grouped.rename(columns={"nhits": threshold_col_name})

        # Merge the current file's dataframe with the accumulated merged dataframe
        if merged_df is None:
            merged_df = df_grouped
        else:
            merged_df = pd.merge(merged_df, df_grouped, on="pixel", how="outer")
    # Replace missing values with 0
    merged_df = merged_df.fillna(0)

    # Remove pixels that have 0 hits across all threshold columns
    threshold_columns = [f"threshold {val}" for val in thresholds]
    merged_df = merged_df[merged_df[threshold_columns].sum(axis=1) > 0]
    # Write the final merged dataframe to a CSV file
    merged_df.to_csv(f"{folder_path}FinalHits.csv", index=False)


def parse_tuple(s):
    tup = ast.literal_eval(s)
    return tuple(int(x) for x in tup)


def FilterThreshold(filepath):
    df = pd.read_csv(filepath, converters={"pixel": parse_tuple})
    df_filtered = df[df["pixel"].apply(lambda t: all(x % 10 == 0 for x in t))]
    df_filtered.to_csv("Data/Threshold Test Data/FinalHitsFiltered.csv", index=False)


def SinglePixel(folder):
    file_list = sorted(os.listdir(folder))
    merged_df = None
    ChargeList = list(range(1000, 16200, 200))

    for file_name, Charge in zip(file_list, ChargeList):
        if not file_name.endswith(".root"):
            continue
        full_path = os.path.join(folder, file_name)
        file = uproot.open(full_path)
        tree = file["clusterTree"]

        arrays_data = tree.arrays(["tot", "nhits", "row", "col"], library="pd")
        tot_list = [to_scalar(item) for item in arrays_data["tot"]]
        nhits_list = [to_scalar(item) for item in arrays_data["nhits"]]
        col_list = [to_scalar(item) for item in arrays_data["col"]]
        row_list = [to_scalar(item) for item in arrays_data["row"]]

        df = pd.DataFrame(
            {f"col {Charge}" : col_list, f"row {Charge}" : row_list, "tot": tot_list, "nhits": nhits_list}
        )
        df_filtered = df[df["nhits"] == 1]
        df_filtered = df_filtered.rename(columns={"tot": f"Charge {Charge}"})
        df_filtered = df_filtered.drop(columns=["nhits"])
        if merged_df is None:
            merged_df = df_filtered
        else:
            merged_df = pd.concat([merged_df, df_filtered], axis=1)
    merged_df.to_csv("Data/Single Pixel Data/Filtered/BR.csv", index=False)


if __name__ == "__main__":
    filepaths = [
        "N10-250404-143700.root",
        "N112-250411-101613.root",
        "N113-250408-100406.root",
        "N116-250403-150114.root",
    ]
    # for filepath in filepaths:
    # ConvertClusterData(filepath)
    # ConvertToT4Sector(filepath)
    for root_file_path in ["N116-250408-123554.root"]:
    # root_file_path = "N10-250409-113326.root"
        ConvertClusterData(root_file_path)
    # ConvertToT4Sector("N116-250408-123554.root")
    # ConvertToT4Sector("N116-250408-105332.root")
    # Threshold("Data/Threshold Test Data/")
    # FilterThreshold("Data/Threshold Test Data/FinalHits.csv")
    # Threshold("Data/Threshold Test Data/N113/")
    # ConvertToT4Sector("N112-250411-101613.root")
    # ConvertFitData("Data/Test Pulse Data/N116-250417-093801.root", "Data/Test Pulse Data/fitData_N116_3.csv")
    # Threshold("Data/Threshold Test Data/N116_2/")
    # SinglePixel(f"Data/Single Pixel Data/Sectors/Multiple/BR/")
