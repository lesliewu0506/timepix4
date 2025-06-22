import os, ast
import uproot
import pandas as pd


class FocusProcessor:
    def __init__(
        self,
        AttenuationVoltage,
        direction,
        ROW=230,
        COL=228,
        ToTLimit=1000,
        ChargeLimit=100,
    ) -> None:
        self.AttenuationVoltage: float = AttenuationVoltage
        self.direction: str = direction
        self.ROW: int = ROW
        self.COL: int = COL
        self.ToTLimit: int = ToTLimit
        self.ChargeLimit: int = ChargeLimit
        self.CorrectionFactors: dict[tuple[int, int], float] = (
            self._LoadCorrectionFactors()
        )

        self.results: list[tuple[float, ...]] = []

    def ProcessAll(self) -> None:
        DataDir = f"Data/focus/{self.direction.capitalize()}/{self.direction.capitalize()}Focus {self.AttenuationVoltage} V"
        OutputDir = f"Data/Focus/{self.direction.capitalize()}/ProcessedFocus {self.AttenuationVoltage} V"
        os.makedirs(OutputDir, exist_ok=True)
        for directory in os.listdir(DataDir):
            if directory.startswith("focus_"):
                self._ProcessFile(os.path.join(DataDir, directory))

        df_results = pd.DataFrame(
            self.results,
            columns=[
                "Position",
                "mean_tot",
                "std_tot",
                "mean_charge",
                "std_charge",
                "mean_cltot",
                "std_cltot",
                "mean_clcharge",
                "std_clcharge",
                "mean_clustersize",
                "std_clustersize",
                "mean_tot_next",
                "std_tot_next",
                "mean_charge_next",
                "std_charge_next",
                "mean_tot_prev",
                "std_tot_prev",
                "mean_charge_prev",
                "std_charge_prev",
            ],
        )
        df_results = df_results.sort_values("Position")
        df_results.fillna(0, inplace=True)
        df_results.to_csv(
            f"{OutputDir}/Results.csv",
            index=False,
        )

    def _ProcessFile(self, FolderPath: str) -> None:

        BaseName = os.path.basename(FolderPath)
        PositionStr = BaseName.split("_", 1)[1]
        self.PositionFloatStr = PositionStr.replace("p", ".")

        RootFilePaths = [
            File for File in os.listdir(FolderPath) if File.endswith(".root")
        ]
        if not RootFilePaths:
            print(f"No root file in {FolderPath}, skipping...")
            return
        RootFile = os.path.join(FolderPath, RootFilePaths[0])
        File = uproot.open(RootFile)
        tree = File["clusterTree"]

        arrays = tree.arrays(["col", "row", "tot", "cltot", "nhits"], library="pd")
        dfData = pd.DataFrame(
            {
                "col": arrays["col"].tolist(),
                "row": arrays["row"].tolist(),
                "tot": arrays["tot"].tolist(),
                "cltot": arrays["cltot"].tolist(),
                "nhits": arrays["nhits"].tolist(),
            }
        )
        self.dfExp = self._FilterAndUnwrap(dfData)
        self._ComputeStats()

    def _ComputeStats(self) -> None:
        self.PositionResults = []
        self.PositionResults.append(self.PositionFloatStr)

        # ============ Target Pixel Stats ============
        self.dfTargetPixel = self.dfExp[
            (self.dfExp["row"] == self.ROW) & (self.dfExp["col"] == self.COL)
        ].copy()
        self._ComputeTargetPixelStats()

        # ============ Cluster Stats ============
        self.dfCluster = self._GetClusterDataFrame()
        self._ComputeClusterStats()

        # ============ Neighbour Pixel Stats ============
        self._ComputeNeighbourStats()

        # ============ Save Results ============
        self.results.append(self.PositionResults)

    def _ComputePixelStats(
        self, df_pixel: pd.DataFrame
    ) -> tuple[float, float, float, float]:
        return (
            float(df_pixel["tot"].mean() or 0),
            float(df_pixel["tot"].std() or 0),
            float(df_pixel["charge"].mean() or 0),
            float(df_pixel["charge"].std() or 0),
        )

    def _ComputeTargetPixelStats(self) -> None:
        MeanToT, StdToT, MeanCharge, StdCharge = self._ComputePixelStats(
            self.dfTargetPixel
        )
        self.PositionResults.extend([MeanToT, StdToT, MeanCharge, StdCharge])

    def _ComputeClusterStats(self) -> None:
        # Cluster ToT Stats
        MeanclToT = self.dfCluster["cltot"].mean() or 0
        StdclToT = self.dfCluster["cltot"].std() or 0
        self.PositionResults.append(MeanclToT)
        self.PositionResults.append(StdclToT)

        # Cluster Charge Stats
        MeanclCharge = self.dfCluster["clcharge"].mean() or 0
        StdclCharge = self.dfCluster["clcharge"].std() or 0
        self.PositionResults.append(MeanclCharge)
        self.PositionResults.append(StdclCharge)

        # Cluster Size Stats
        MeanclSize = self.dfCluster["nhits"].mean() or 0
        StdclSize = self.dfCluster["nhits"].std() or 0
        self.PositionResults.append(MeanclSize)
        self.PositionResults.append(StdclSize)

    def _ComputeNeighbourStats(self) -> None:
        Positions = self._NeighbourPositions()
        if Positions is not None:
            PrevPosition, NextPosition = Positions

            # ============ Next Pixel Stats ============
            dfNextPixel = self.dfExp[
                (self.dfExp["row"] == NextPosition[0])
                & (self.dfExp["col"] == NextPosition[1])
            ].copy()

            MeanToTNext, StdToTNext, MeanChargeNext, StdChargeNext = (
                self._ComputePixelStats(dfNextPixel)
            )
            self.PositionResults.extend(
                [MeanToTNext, StdToTNext, MeanChargeNext, StdChargeNext]
            )

            # ============ Prev Pixel Stats ============
            dfPrevPixel = self.dfExp[
                (self.dfExp["row"] == PrevPosition[0])
                & (self.dfExp["col"] == PrevPosition[1])
            ].copy()

            MeanToTPrev, StdToTPrev, MeanChargePrev, StdChargePrev = (
                self._ComputePixelStats(dfPrevPixel)
            )
            self.PositionResults.extend(
                [MeanToTPrev, StdToTPrev, MeanChargePrev, StdChargePrev]
            )
        else:
            for _ in range(8):
                self.PositionResults.append(0)

    def _GetClusterDataFrame(self) -> pd.DataFrame:
        if self.direction == "x":
            mask = (
                self.dfExp["row"].isin(
                    [self.ROW, self.ROW + 1, self.ROW - 1, self.ROW - 2, self.ROW + 2]
                )
            ) & (self.dfExp["col"] == self.COL)
            return self.dfExp[mask].copy()

        elif self.direction == "y":
            mask = (
                self.dfExp["col"].isin(
                    [self.COL, self.COL + 1, self.COL - 1, self.COL - 2, self.COL + 2]
                )
            ) & (self.dfExp["row"] == self.ROW)
            return self.dfExp[mask].copy()

        else:
            return self.dfTargetPixel

    def _NeighbourPositions(self) -> list[tuple[int, int]] | None:
        if self.direction == "x":
            return [(self.ROW - 1, self.COL), (self.ROW + 1, self.COL)]
        elif self.direction == "y":
            return [(self.ROW, self.COL - 1), (self.ROW, self.COL + 1)]
        else:
            return None

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
        clcharge = sum(pix_charges)

        return pix_charges, [clcharge]

    def _FilterAndUnwrap(self, df: pd.DataFrame) -> pd.DataFrame:
        for c in ["col", "row", "tot", "cltot", "nhits"]:
            df[c] = df[c].apply(self._ParseList)
        df_charge = df.copy()

        df_charge[["charge", "clcharge"]] = df_charge.apply(
            lambda r: pd.Series(
                self._ToTToCharge(r["tot"], r["row"], r["col"]),
                index=["charge", "clcharge"],
            ),
            axis=1,
        )
        df_charge = df_charge[
            ["row", "col", "tot", "cltot", "nhits", "charge", "clcharge"]
        ].reset_index(drop=True)

        df_exploded = df_charge.explode(["row", "col", "tot", "charge"]).reset_index(
            drop=True
        )
        for c in ["col", "row", "tot", "charge", "cltot", "nhits", "clcharge"]:
            df_exploded[c] = df_exploded[c].apply(self._ParsefromList)

        df_exploded = df_exploded[
            (df_exploded["tot"] < self.ToTLimit) & (df_exploded["tot"] >= 0)
        ]
        df_exploded = df_exploded[
            (df_exploded["cltot"] < self.ToTLimit) & (df_exploded["cltot"] >= 0)
        ]
        return df_exploded

    def _ParsefromList(self, x: list | float | int) -> float:
        if isinstance(x, list):
            return float(x[0])
        elif isinstance(x, (int, float)):
            return float(x)
        else:
            print(x)
            raise ValueError(f"Expected a list with at least one element, got {x}")
