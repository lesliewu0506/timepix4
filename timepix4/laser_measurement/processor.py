import uproot, os, ast
import pandas as pd
import numpy as np


class Processor:
    def __init__(
        self,
        FolderPath: str,
        ROW=230,
        COL=228,
        ROW_Next=0,
        COL_Next=0,
    ) -> None:
        self.FolderPath: str = FolderPath
        self.ROW: int = ROW
        self.COL: int = COL
        self.CorrectionFactors: dict[tuple[int, int], float] = (
            self._LoadCorrectionFactors()
        )
        self.Pixels: list[tuple[int, int]] = [
            (self.ROW + i, self.COL + j)
            for i in range(min(0, ROW_Next), max(1, ROW_Next + 1))
            for j in range(min(0, COL_Next), max(1, COL_Next + 1))
        ]
        self.results: list[tuple[float, ...]] = []

    def ProcessFolder(self) -> None:
        RootFilePaths = [
            os.path.join(self.FolderPath, File)
            for File in os.listdir(self.FolderPath)
            if File.endswith(".root")
        ]
        # if self.ROW_Next != 0 or self.COL_Next != 0:
        All_Results = []
        for RootFile in RootFilePaths:
            All_Results.append(self._ProcessFile(RootFile))

        for i, pixel in enumerate(self.Pixels):
            Results = []
            for Result in All_Results:
                Results.append(Result[i])
            df_results = pd.DataFrame(
                Results,
                columns=[
                    "AttenuationVoltage",
                    "Mean Tot",
                    "Std Tot",
                    "Mean clTot",
                    "Std clTot",
                    "Mean Charge Raw",
                    "Std Charge Raw",
                    "Mean clCharge",
                    "Std clCharge",
                    "Mean Charge Calibrated",
                    "Std Charge Calibrated",
                    "Mean clCharge Calibrated",
                    "Std clCharge Calibrated",
                ],
            )
            df_results = df_results.sort_values("AttenuationVoltage")
            df_results.to_csv(
                f"{self.FolderPath}/{len(self.Pixels)}Results{pixel}.csv",
                index=False,
            )

    def _ProcessFile(self, FilePath: str) -> list[tuple[float, ...]]:
        self.AttenuationVoltageResults = []
        self.AttenuationVoltage = (
            FilePath.split("/")[-1].split(".")[0].replace("_", ".")
        )

        File = uproot.open(FilePath)
        tree = File["clusterTree"]

        arrays = tree.arrays(
            ["col", "row", "tot", "cltot", "nhits", "charge", "clCharge"], library="pd"
        )
        dfData = pd.DataFrame(
            {
                "col": arrays["col"].tolist(),
                "row": arrays["row"].tolist(),
                "tot": arrays["tot"].tolist(),
                "cltot": arrays["cltot"].tolist(),
                "nhits": arrays["nhits"].tolist(),
                "raw charge": arrays["charge"].tolist(),
                "clcharge": arrays["clCharge"].tolist(),
            }
        )
        # self.FilterAndUnwrap(dfData)
        self.dfExp = self._FilterAndUnwrap(dfData)
        for pixel in self.Pixels:
            self._ComputeStats(pixel)

        return self.AttenuationVoltageResults

    def _ComputeStats(self, pixel: tuple[int, int]) -> None:
        self.dfTargetPixel = self.dfExp[
            (self.dfExp["row"] == pixel[0]) & (self.dfExp["col"] == pixel[1])
        ].copy()
        self._ComputeTargetPixelStats()
        if self.AttenuationVoltage == "4.000" and pixel[0] == 230 and pixel[1] == 228:
            print(self.dfTargetPixel["clCharge Calibrated"].describe())
            print(self.dfTargetPixel[self.dfTargetPixel["clCharge Calibrated"] > 10])

    def _ComputeTargetPixelStats(self) -> None:
        self.dfTargetPixel["cltot"] = self.dfTargetPixel["cltot"].astype(float)
        self.dfTargetPixel["tot"] = self.dfTargetPixel["tot"].astype(float)
        self.dfTargetPixel["raw charge"] = self.dfTargetPixel["raw charge"].astype(
            float
        )
        self.dfTargetPixel["clcharge"] = self.dfTargetPixel["clcharge"].astype(float)
        self.dfTargetPixel["Charge Calibrated"] = self.dfTargetPixel[
            "Charge Calibrated"
        ].astype(float)
        self.dfTargetPixel["clCharge Calibrated"] = self.dfTargetPixel[
            "clCharge Calibrated"
        ].astype(float)
        mean_tot = self.dfTargetPixel["tot"].mean()
        std_tot = self.dfTargetPixel["tot"].std()
        mean_cltot = self.dfTargetPixel["cltot"].mean()
        std_cltot = self.dfTargetPixel["cltot"].std()
        mean_charge_raw = self.dfTargetPixel["raw charge"].mean() / 1000
        std_charge_raw = self.dfTargetPixel["raw charge"].std() / 1000
        mean_charge = self.dfTargetPixel["clcharge"].mean() / 1000
        std_charge = self.dfTargetPixel["clcharge"].std() / 1000
        mean_charge_calibrated = self.dfTargetPixel["Charge Calibrated"].mean()
        std_charge_calibrated = self.dfTargetPixel["Charge Calibrated"].std()
        mean_clcharge_calibrated = self.dfTargetPixel["clCharge Calibrated"].mean()
        std_clcharge_calibrated = self.dfTargetPixel["clCharge Calibrated"].std()
        self.AttenuationVoltageResults.append(
            (
                float(self.AttenuationVoltage),
                float(mean_tot),
                float(std_tot),
                float(mean_cltot),
                float(std_cltot),
                float(mean_charge_raw),
                float(std_charge_raw),
                float(mean_charge),
                float(std_charge),
                float(mean_charge_calibrated),
                float(std_charge_calibrated),
                float(mean_clcharge_calibrated),
                float(std_clcharge_calibrated),
            )
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
    ) -> tuple[list[float], list[float]]:
        pix_charges = []
        for tot, r, c in zip(ToTList, RowList, ColList):
            factor = self.CorrectionFactors.get((c, r), 0.10)
            pix_charges.append(tot * factor)
        total_charge = np.sum(pix_charges)
        return pix_charges, [total_charge]

    def _FilterAndUnwrap(self, df: pd.DataFrame) -> pd.DataFrame:

        for c in ["col", "row", "tot", "cltot", "nhits", "raw charge", "clcharge"]:
            df[c] = df[c].apply(self._ParseList)
        df_charge = df.copy()

        # Apply ToTToCharge and expand its tuple result into two columns
        df_charge[["Charge Calibrated", "clCharge Calibrated"]] = df_charge.apply(
            lambda r: pd.Series(
                self._ToTToCharge(r["tot"], r["row"], r["col"]),
                index=["pix_charges", "total_charge"],
            ),
            axis=1,
        )
        df_charge = df_charge[
            [
                "row",
                "col",
                "tot",
                "cltot",
                "nhits",
                "raw charge",
                "clcharge",
                "Charge Calibrated",
                "clCharge Calibrated",
            ]
        ].reset_index(drop=True)
        df["combined"] = df_charge.apply(
            lambda r: list(
                zip(
                    r["row"],
                    r["col"],
                    r["tot"],
                    r["cltot"],
                    r["nhits"],
                    r["raw charge"],
                    r["clcharge"],
                    r["Charge Calibrated"],
                    r["clCharge Calibrated"],
                )
            ),
            axis=1,
        )
        df_exploded = df.explode("combined")

        df_exploded[
            [
                "row",
                "col",
                "tot",
                "cltot",
                "nhits",
                "raw charge",
                "clcharge",
                "Charge Calibrated",
                "clCharge Calibrated",
            ]
        ] = pd.DataFrame(df_exploded["combined"].tolist(), index=df_exploded.index)
        df_exploded = df_exploded.drop(columns=["combined"])
        df_exploded = df_exploded[(df_exploded["tot"] > 0)]
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
