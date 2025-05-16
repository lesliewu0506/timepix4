import pandas as pd
import uproot, os


def Processor(FolderPath: str) -> None:
    AttenuationVoltage = FolderPath.split("/")[-1].replace("_", ".")
    RootFilePaths = sorted(
        [
            os.path.join(FolderPath, Folder, File)
            for Folder in os.listdir(FolderPath)
            for File in os.listdir(os.path.join(FolderPath, Folder))
            if File.endswith(".root")
        ]
    )
    results = []
    for FilePath in RootFilePaths:
        col, row = _RetrievePixel(FilePath)
        result = _ProcessFile(FilePath, col, row)
        results.append(result)
    df_results = pd.DataFrame(
        results,
        columns=[
            "col",
            "row",
            "mean_tot",
            "std_tot",
        ],
    )
    df_results = df_results.sort_values(by=["row", "col"])
    df_results.to_csv(f"Data/Laser Calibration/{AttenuationVoltage} V.csv", index=False)


def _ProcessFile(FilePath: str, col: int, row: int) -> list[tuple[float, ...]]:

    File = uproot.open(FilePath)
    tree = File["clusterTree"]

    arrays = tree.arrays(["col", "row", "tot", "nhits"], library="pd")
    dfData = pd.DataFrame(
        {
            "col": arrays["col"].tolist(),
            "row": arrays["row"].tolist(),
            "tot": arrays["tot"].tolist(),
            "nhits": arrays["nhits"].tolist(),
        }
    )
    results = _FilterAndUnwrap(dfData, col, row)
    return results


def _FilterAndUnwrap(df: pd.DataFrame, col: int, row: int) -> tuple:

    df_filtered = df[df["nhits"] == 1].copy()
    df_filtered = df_filtered.map(
        lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) == 1 else x
    )
    df_filtered = df_filtered[(df_filtered["col"] == col) & (df_filtered["row"] == row)]
    if df_filtered.empty:
        return (0, 0, 0, 0)
    mean_tot = df_filtered["tot"].mean()
    std_tot = df_filtered["tot"].std()
    col = df_filtered["col"].iloc[0]
    row = df_filtered["row"].iloc[0]
    return (col, row, mean_tot, std_tot)


def _RetrievePixel(Filepath: str) -> tuple[int, int]:
    coordinates = Filepath.split("/")[-2]
    x = int(coordinates.split("y")[0].split("_")[1].split("_")[0])
    y = int(coordinates.split("y")[1].split("_")[-1])
    diff_row = (x - 210) / 55
    diff_col = (y - 380) / 55
    row = 230 - diff_row
    col = 228 + diff_col
    return (col, row)
