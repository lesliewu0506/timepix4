import uproot, os, ast
import pandas as pd
import numpy as np


class Processor:
    def __init__(
        self,
        FolderPath: str,
        ROW=230,
        COL=228,
    ) -> None:
        self.FolderPath: str = FolderPath
        self.ROW: int = ROW
        self.COL: int = COL
        self.CorrectionFactors: dict[tuple[int, int], float] = (
            self._LoadCorrectionFactors()
        )

        self.results: list[tuple[float, ...]] = []

    def ProcessFolder(self) -> None:
        RootFilePaths = [
            os.path.join(self.FolderPath, File)
            for File in os.listdir(self.FolderPath)
            if File.endswith(".root")
        ]
        for RootFile in RootFilePaths:
            self._ProcessFile(RootFile)

        df_results = pd.DataFrame(
            self.results,
            columns=[
                "AttenuationVoltage",
                "Mean Tot",
                "Mean Charge Raw",
                "Mean Charge",
            ],
        )
        df_results = df_results.sort_values("AttenuationVoltage")
        df_results.to_csv(
            f"{self.FolderPath}/Results.csv",
            index=False,
        )

    def _ProcessFile(self, FilePath: str) -> None:
        self.AttenuationVoltageResults = []
        self.AttenuationVoltage = (
            FilePath.split("/")[-1].split(".")[0].replace("_", ".")
        )

        File = uproot.open(FilePath)
        tree = File["clusterTree"]

        arrays = tree.arrays(["col", "row", "tot", "nhits", "clCharge"], library="pd")
        dfData = pd.DataFrame(
            {
                "col": arrays["col"].tolist(),
                "row": arrays["row"].tolist(),
                "tot": arrays["tot"].tolist(),
                "nhits": arrays["nhits"].tolist(),
                "raw charge": arrays["clCharge"].tolist(),
            }
        )
        self.dfExp = self._FilterAndUnwrap(dfData)
        self._ComputeStats()

        self.results.extend(self.AttenuationVoltageResults)

    def _ComputeStats(self) -> None:
        self.dfTargetPixel = self.dfExp[
            (self.dfExp["row"] == self.ROW) & (self.dfExp["col"] == self.COL)
        ].copy()
        self._ComputeTargetPixelStats()

    def _ComputeTargetPixelStats(self) -> None:
        self.dfTargetPixel["raw charge"] = self.dfTargetPixel["raw charge"].astype(
            float
        )

        self.dfTargetPixel["charge"] = self.dfTargetPixel["charge"].astype(float)
        self.dfTargetPixel["tot"] = self.dfTargetPixel["tot"].astype(float)
        self.dfTargetPixel["nhits"] = self.dfTargetPixel["nhits"].astype(float)

        mean_tot = self.dfTargetPixel["tot"].mean()
        # mean_charge_raw = self.dfTargetPixel["raw charge"].mean() / 1000
        mean_charge = self.dfTargetPixel["charge"].mean()
        self.dfTargetPixel["Charge"] = self.dfTargetPixel["tot"].apply(
            self._ToTConverter
        )
        mean_charge_raw = self.dfTargetPixel["Charge"].mean()
        self.AttenuationVoltageResults.append(
            (
                float(self.AttenuationVoltage),
                float(mean_tot),
                float(mean_charge_raw),
                float(mean_charge),
            )
        )

    def _ToTConverter(self, ToT: float) -> float:
        # a = 61.5472
        # b = 1.683213
        # c = 970420.8
        # t = 353.9627
        # -7.782196,1.704267,1295264.0,61.11348
        b = -7.782196
        a = 1.704267
        c = 1295264.0
        t = 61.11348

        # 65.03894,2.135082,1119591.0,328.8884
        # a = 65.03894
        # b = 2.135082
        # c = 1119591.0
        # t = 328.8884
        return (ToT + a * t - b + np.sqrt(4 * a * c + np.square(b + a * t - ToT))) / (
            2 * a
        )

    def _ParseList(self, x: str | list | tuple) -> list:
        if isinstance(x, str):
            parsed = ast.literal_eval(x)
            if isinstance(parsed, (list, tuple)):
                return list(parsed)
            else:
                return [parsed]
        elif isinstance(x, (list, tuple)):
            return list(x)
        else:
            return [x]

    def _ToTToCharge(
        self, ToTList: list[float], RowList: list[int], ColList: list[int]
    ) -> list[float]:
        pix_charges = []
        for tot, r, c in zip(ToTList, RowList, ColList):

            factor = self.CorrectionFactors.get((c, r), 0.10)
            pix_charges.append(tot * factor)

        return pix_charges

    def _FilterAndUnwrap(self, df: pd.DataFrame) -> pd.DataFrame:
        for c in ["col", "row", "tot", "nhits", "raw charge"]:
            df[c] = df[c].apply(self._ParseList)
        df_charge = df.copy()

        df_charge["charge"] = df_charge.apply(
            lambda r: self._ToTToCharge(
                r["tot"],
                r["row"],
                r["col"],
            ),
            axis=1,
        )
        df_charge = df_charge[
            ["row", "col", "tot", "nhits", "raw charge", "charge"]
        ].reset_index(drop=True)
        df["combined"] = df_charge.apply(
            lambda r: list(
                zip(
                    r["row"],
                    r["col"],
                    r["tot"],
                    r["nhits"],
                    r["raw charge"],
                    r["charge"],
                )
            ),
            axis=1,
        )
        df_exploded = df.explode("combined")

        df_exploded[["row", "col", "tot", "nhits", "raw charge", "charge"]] = (
            pd.DataFrame(df_exploded["combined"].tolist(), index=df_exploded.index)
        )
        df_exploded = df_exploded.drop(columns=["combined"])
        return df_exploded

    def _LoadCorrectionFactors(self) -> dict[tuple[int, int], float]:
        df = pd.read_csv(
            f"Data/Filtered Calibration Data/N116-250408-123554-CorrectionFactors.csv"
        )
        df["pixel"] = df["pixel"].apply(lambda x: ast.literal_eval(str(x)))
        df["correction"] = df["correction"].astype(float)

        charge_dict = {
            pixel: correction
            for pixel, correction in zip(df["pixel"], df["correction"])
        }
        return charge_dict
