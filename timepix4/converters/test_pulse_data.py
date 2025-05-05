import pandas as pd
import uproot


def ConvertTestPulseData(
    root_file_path: str | None = None,
    charge_file_path: str | None = None,
    output_path_data: str | None = None,
    output_path_results: str | None = None,
) -> None:
    if root_file_path:
        sensor = root_file_path.split("/")[-1].split("-")[0]
        _FitDataUnwrap(root_file_path, sensor, output_path_data)
    if charge_file_path:
        sensor = charge_file_path.split("/")[-1].split("_")[0]
        _FitResultsUnwrap(charge_file_path, sensor, output_path_results)


def _FitDataUnwrap(file_path: str, sensor: str, output_path: str | None) -> None:
    file = uproot.open(file_path)
    tree_data = file["fitData"]
    arrays_data = tree_data.arrays()

    df_data = pd.DataFrame(
        {
            "col": arrays_data["col"].to_numpy(),
            "row": arrays_data["row"].to_numpy(),
            "charge": arrays_data["charge"].to_numpy(),
            "meanTot": arrays_data["meanTot"].to_numpy(),
            "stdvTot": arrays_data["stdvTot"].to_numpy(),
            "nhits": arrays_data["nhits"].to_numpy(),
        }
    )
    if output_path is not None:
        df_data.to_csv(f"{output_path}/{sensor}-TestPulseData.csv", index=False)
    else:
        df_data.to_csv(f"Data/Test Pulse Data/{sensor}-TestPulseData.csv", index=False)


def _FitResultsUnwrap(file_path, sensor: str, output_path: str | None) -> None:
    df = pd.read_csv(file_path, sep="\s+", header=None, skiprows=15)
    df.columns = [
        "Col",
        "Row",
        "p0",
        "p1",
        "p2",
        "p3",
        "p0_err",
        "p1_err",
        "p2_err",
        "p3_err",
        "red_chi2",
        "valid",
    ]
    if output_path:
        df.to_csv(f"{output_path}/{sensor}-TestPulseResults.csv", index=False)
    else:
        df.to_csv(f"Data/Test Pulse Data/{sensor}-TestPulseResults.csv", index=False)
