import uproot
import pandas as pd


def ConvertClusterData(filepath: str) -> None:
    sensor = filepath.split("/")[-1].split("-")[0]
    file = uproot.open(filepath)
    tree = file["clusterTree"]

    arrays_data = tree.arrays(["col", "row", "tot", "cltot", "nhits", "charge", "clCharge"], library="pd")
    df_data = pd.DataFrame(
        {
            "col": arrays_data["col"].to_list(),
            "row": arrays_data["row"].to_list(),
            "tot": arrays_data["tot"].to_list(),
            "cltot": arrays_data["cltot"].to_list(),
            "nhits": arrays_data["nhits"].to_list(),
            "Charge": arrays_data["charge"].to_list(),
            "clCharge": arrays_data["clCharge"].to_list(),
        }
    )

    df_filtered = _FilterAndUnwrap(df_data)
    df_filtered.to_csv(
        f"{sensor}-Charge-Data.csv",
        index=False,
    )


def _FilterAndUnwrap(df: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df[df["nhits"] == 1].copy()
    df_filtered = df_filtered.map(
        lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) == 1 else x
    )
    df_filtered["Charge"] = df_filtered["Charge"].astype(float) / 1000
    df_filtered["clCharge"] = df_filtered["clCharge"].astype(float) / 1000
    return df_filtered
