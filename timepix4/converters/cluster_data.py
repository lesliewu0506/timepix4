import uproot, os, ast
import pandas as pd
import numpy as np


def ConvertClusterData(filepath: str) -> None:
    sensor = filepath.split("/")[-1].split("-")[0]
    file = uproot.open(filepath)
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
        f"Data/Filtered Calibration Data/{sensor}-Charge-Data.csv",
    )
    # df_transformed = TransformDataFrame(df_filtered)
    # df_transformed["correction"] = df_transformed["pixel"].apply(
    #     lambda pixel: CorrectionFactors.get(pixel, np.nan)
    # )
    # df_correction = pd.DataFrame(list(CorrectionFactors.items()), columns=["pixel", "correction"])

    # df_correction.to_csv(f"Data/Filtered Calibration Data/{filename}-CorrectionFactors.csv", index=False)
    # df_transformed.to_csv(
    #     f"Data/Filtered Calibration Data/{filename}-Charge-Data.csv", index=False
    # )


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
