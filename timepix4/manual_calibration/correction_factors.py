import pandas as pd

THRESHOLDTOT = 150


def GetCalibrationFactors(filepath: str) -> None:
    sensor = filepath.split("/")[-1].split("-")[0]
    df = _LoadCSV(filepath)
    groups = df.groupby("pixel")

    CorrectionFactors = {}
    for pixel, group in groups:
        tot = _FindHighestToT(group, group["col"].iloc[0], group["row"].iloc[0])
        if tot is None:
            CorrectionFactors[pixel] = 0.10
        else:
            CorrectionFactors[pixel] = 16.5 / tot

    cf_df = pd.DataFrame(
        list(CorrectionFactors.items()), columns=["pixel", "correction"]
    )
    cf_df.to_csv(f"{sensor}-CorrectionFactors.csv", index=False)


def _LoadCSV(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df["pixel"] = list(zip(df["col"], df["row"]))
    return df


def _FindHighestToT(df: pd.DataFrame, target_col: int, target_row: int):
    pixel_df = df[(df["col"] == target_col) & (df["row"] == target_row)]

    if pixel_df.empty:
        return None
    mask = pixel_df["tot"] > THRESHOLDTOT
    filtered_tot = pixel_df.loc[mask, "tot"]
    if filtered_tot.empty:
        return None
    return filtered_tot.mean()
