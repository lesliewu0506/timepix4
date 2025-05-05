import uproot
import pandas as pd


def ConvertClusterData(filepath: str) -> None:
    sensor = filepath.split("/")[-1].split("-")[0]
    file = uproot.open(filepath)
    tree = file["clusterTree"]

    arrays_data = tree.arrays(["col", "row", "tot", "nhits", "charge"], library="pd")
    df_data = pd.DataFrame(
        {
            "col": arrays_data["col"].to_list(),
            "row": arrays_data["row"].to_list(),
            "tot": arrays_data["tot"].to_list(),
            "nhits": arrays_data["nhits"].to_list(),
            "Raw Charge": arrays_data["charge"].to_list(),
        }
    )

    df_filtered = _FilterAndUnwrap(df_data)
    df_filtered.to_csv(
        f"{sensor}-Charge-Data.csv",
    )


def _FilterAndUnwrap(df: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df[df["nhits"] == 1].copy()
    df_filtered = df_filtered.map(
        lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) == 1 else x
    )
    df_filtered["Raw Charge"] = df_filtered["Raw Charge"].astype(float) / 1000
    return df_filtered
