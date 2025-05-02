import os, uproot, ast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Focus:
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

    def _ComputeNeighbourStats(self) -> None:
        Positions = self._NeighbourPositions()
        if Positions is not None:
            PrevPosition, NextPosition = Positions

            # ============ Next Pixel Stats ============
            dfNextPixel = self.dfExp[
                (self.dfExp["row"] == NextPosition[0])
                & (self.dfExp["col"] == NextPosition[1])
            ].copy()
            # Next ToT Stats
            MeanToTNext = dfNextPixel["tot"].mean() or 0
            StdToTNext = dfNextPixel["tot"].std() or 0
            self.PositionResults.append(MeanToTNext)
            self.PositionResults.append(StdToTNext)

            # Next Charge Stats
            MeanChargeNext = dfNextPixel["charge"].mean() or 0
            StdChargeNext = dfNextPixel["charge"].std() or 0
            self.PositionResults.append(MeanChargeNext)
            self.PositionResults.append(StdChargeNext)

            # ============ Prev Pixel Stats ============
            dfPrevPixel = self.dfExp[
                (self.dfExp["row"] == PrevPosition[0])
                & (self.dfExp["col"] == PrevPosition[1])
            ].copy()
            # Prev ToT Stats
            MeanToTPrev = dfPrevPixel["tot"].mean() or 0
            StdToTPrev = dfPrevPixel["tot"].std() or 0
            self.PositionResults.append(MeanToTPrev)
            self.PositionResults.append(StdToTPrev)

            # Prev Charge Stats
            MeanChargePrev = dfPrevPixel["charge"].mean() or 0
            StdChargePrev = dfPrevPixel["charge"].std() or 0
            self.PositionResults.append(MeanChargePrev)
            self.PositionResults.append(StdChargePrev)
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

    def _ComputeTargetPixelStats(self) -> None:
        # ToT Stats
        MeanToT = self.dfTargetPixel["tot"].mean() or 0
        StdToT = self.dfTargetPixel["tot"].std() or 0
        self.PositionResults.append(MeanToT)
        self.PositionResults.append(StdToT)

        # Charge Stats
        MeanCharge = self.dfTargetPixel["charge"].mean() or 0
        StdCharge = self.dfTargetPixel["charge"].std() or 0
        self.PositionResults.append(MeanCharge)
        self.PositionResults.append(StdCharge)

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

        df["combined"] = df_charge.apply(
            lambda r: list(
                zip(
                    r["row"],
                    r["col"],
                    r["tot"],
                    r["cltot"],
                    r["nhits"],
                    r["charge"],
                    r["clcharge"],
                )
            ),
            axis=1,
        )
        df_exploded = df.explode("combined")

        df_exploded[["row", "col", "tot", "cltot", "nhits", "charge", "clcharge"]] = (
            pd.DataFrame(df_exploded["combined"].tolist(), index=df_exploded.index)
        )
        df_exploded = df_exploded.drop(columns=["combined"])

        df_exploded = df_exploded[
            (df_exploded["tot"] < self.ToTLimit) & (df_exploded["tot"] >= 0)
        ]
        df_exploded = df_exploded[
            (df_exploded["cltot"] < self.ToTLimit) & (df_exploded["cltot"] >= 0)
        ]
        return df_exploded


class FocusPlotter:
    def __init__(
        self, direction: str, AttenuationVoltage: float, ROW: int, COL: int
    ) -> None:
        self.direction = direction
        self.AttenuationVoltage = AttenuationVoltage
        self.ROW = ROW
        self.COL = COL
        self.df = pd.read_csv(
            f"Data/Focus/{self.direction.capitalize()}/ProcessedFocus {self.AttenuationVoltage} V/Results.csv"
        )

    def Plot_ToT(self) -> None:
        _, ax = plt.subplots(figsize=(12, 8))
        ax2 = ax.twinx()

        # Plot Cluster ToT
        ax.errorbar(
            self.df["Position"],
            self.df["mean_cltot"],
            yerr=self.df["std_cltot"],
            marker="o",
            linestyle="-",
            capsize=5,
            label="Mean clToT",
        )

        # Plot Cluster Size
        ax2.errorbar(
            self.df["Position"],
            self.df["mean_clustersize"],
            yerr=self.df["std_clustersize"],
            marker="s",
            linestyle="None",
            capsize=5,
            color="green",
            label="Mean cluster size",
        )

        # Plot ToT
        ax.errorbar(
            self.df["Position"],
            self.df["mean_tot"],
            yerr=self.df["std_tot"],
            marker="o",
            linestyle="-",
            capsize=5,
            label=f"Mean ToT ({self.COL}, {self.ROW})",
        )

        if self.direction != "z":
            if self.direction == "x":
                label_prev = f"Mean ToT ({self.COL}, {self.ROW - 1})"
                label_next = f"Mean ToT ({self.COL}, {self.ROW + 1})"
            elif self.direction == "y":
                label_prev = f"Mean ToT ({self.COL - 1}, {self.ROW})"
                label_next = f"Mean ToT ({self.COL + 1}, {self.ROW})"

            # Plot previous and next ToT
            ax.errorbar(
                self.df["Position"],
                self.df["mean_tot_prev"],
                yerr=self.df["std_tot_prev"],
                marker="o",
                linestyle="-",
                capsize=5,
                label=label_prev,
            )

            ax.errorbar(
                self.df["Position"],
                self.df["mean_tot_next"],
                yerr=self.df["std_tot_next"],
                marker="o",
                linestyle="-",
                capsize=5,
                label=label_next,
            )

        # Plot Attributes
        max_cs = np.ceil(self.df["mean_clustersize"].max() / 5) * 5
        if max_cs < 10:
            max_cs = 10

        ax2.set_ylim(0, max_cs)
        num_ticks = len(ax2.get_yticks())
        all_tot = np.hstack(
            [
                self.df["mean_cltot"].values,
                self.df["mean_tot"].values,
                self.df["mean_tot_prev"].values,
                self.df["mean_tot_next"].values,
            ]
        )
        all_tot = all_tot[~np.isnan(all_tot)]

        min_lim = np.floor(all_tot.min() / 100) * 100
        max_lim = np.ceil(all_tot.max() / 100) * 100

        left_ticks = np.linspace(min_lim, max_lim, num_ticks)
        ax.set_ylim(min_lim, max_lim)
        ax.set_yticks(left_ticks)
        ax2.set_yticks(np.linspace(0, max_cs, num_ticks))

        ax.set_xlabel(f"{self.direction.capitalize()} Position Stage [mm]")
        ax.set_ylabel("ToT [25ns]")
        ax2.set_ylabel("Mean cluster size [pixels]")

        ax.set_title(
            f"{self.direction.capitalize()} Scan ToT: Pixel ({self.COL}, {self.ROW})"
        )
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc="best")
        ax.grid(True)
        plt.tight_layout()
        plt.savefig(
            f"{self.direction.capitalize()}ScanPlot{self.AttenuationVoltage}.png",
            dpi=600,
        )
        plt.show()

    def Plot_Charge(self) -> None:
        _, ax = plt.subplots(figsize=(12, 8))
        ax2 = ax.twinx()

        # Plot Cluster Charge
        ax.errorbar(
            self.df["Position"],
            self.df["mean_clcharge"],
            yerr=self.df["std_clcharge"],
            marker="o",
            linestyle="-",
            capsize=5,
            label=f"Mean clCharge",
        )

        # Plot Cluster Size
        ax2.errorbar(
            self.df["Position"],
            self.df["mean_clustersize"],
            yerr=self.df["std_clustersize"],
            marker="s",
            linestyle="None",
            capsize=5,
            color="green",
            label="Mean cluster size",
        )

        # Plot Charge
        ax.errorbar(
            self.df["Position"],
            self.df["mean_charge"],
            yerr=self.df["std_charge"],
            marker="o",
            linestyle="-",
            capsize=5,
            label=f"Mean Charge ({self.COL}, {self.ROW})",
        )
        if self.direction != "z":
            if self.direction == "x":
                label_prev = f"Mean Charge ({self.COL}, {self.ROW - 1})"
                label_next = f"Mean Charge ({self.COL}, {self.ROW + 1})"
            elif self.direction == "y":
                label_prev = f"Mean Charge ({self.COL - 1}, {self.ROW})"
                label_next = f"Mean Charge ({self.COL + 1}, {self.ROW})"

            # Plot previous and next Charge
            ax.errorbar(
                self.df["Position"],
                self.df["mean_charge_prev"],
                yerr=self.df["std_charge_prev"],
                marker="o",
                linestyle="-",
                capsize=5,
                label=label_prev,
            )

            ax.errorbar(
                self.df["Position"],
                self.df["mean_charge_next"],
                yerr=self.df["std_charge_next"],
                marker="o",
                linestyle="-",
                capsize=5,
                label=label_next,
            )

        # Plot Attributes
        max_cs = np.ceil(self.df["mean_clustersize"].max() / 5) * 5
        if max_cs < 10:
            max_cs = 10

        ax2.set_ylim(0, max_cs)
        num_ticks = len(ax2.get_yticks())
        all_charge = np.hstack(
            [
                self.df["mean_clcharge"].values,
                self.df["mean_charge"].values,
                self.df["mean_charge_prev"].values,
                self.df["mean_charge_next"].values,
            ]
        )
        all_charge = all_charge[~np.isnan(all_charge)]

        min_lim = np.floor(all_charge.min() / 5) * 5
        max_lim = np.ceil(all_charge.max() / 5) * 5 + 5

        left_ticks = np.linspace(min_lim, max_lim, num_ticks)
        ax.set_ylim(min_lim, max_lim)
        ax.set_yticks(left_ticks)
        ax2.set_yticks(np.linspace(0, max_cs, num_ticks))

        ax.set_xlabel(f"{self.direction.capitalize()} Position Stage [mm]")
        ax.set_ylabel("Charge [ke]")
        ax.set_title(
            f"{self.direction.capitalize()} Scan Charge: Pixel ({self.COL}, {self.ROW})"
        )
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc="best")
        ax.grid(True)
        plt.tight_layout()
        plt.savefig(
            f"{self.direction.capitalize()}ScanPlotCharge{self.AttenuationVoltage}.png",
            dpi=600,
        )
        plt.show()


class FocusVisualizer:
    def __init__(self, RootFilePath: str) -> None:
        self.RootFilePath = RootFilePath

    def CreateHitmap(self) -> None:
        file = uproot.open(self.RootFilePath)
        tree = file["clusterTree"]

        arrays_data = tree.arrays(["col", "row", "tot"], library="pd")

        df_data = pd.DataFrame(
            {
                "col": arrays_data["col"].to_list(),
                "row": arrays_data["row"].to_list(),
                "tot": arrays_data["tot"].to_list(),
            }
        )

        df_filtered = self._FilterAndUnwrap(df_data)
        mean_tots = df_filtered.groupby(["row", "col"])["tot"].mean().reset_index()

        # Determine center pixel (highest mean ToT)
        center = mean_tots.loc[mean_tots["tot"].idxmax()]
        center_row, center_col = int(center["row"]), int(center["col"])

        # Define 5x5 neighborhood bounds
        row_min, row_max = center_row - 3, center_row + 3
        col_min, col_max = center_col - 3, center_col + 3

        # Filter for the 5×5 area around center
        mean_tots = mean_tots[
            mean_tots["row"].between(row_min, row_max)
            & mean_tots["col"].between(col_min, col_max)
        ]

        # Pivot only the 5×5 region
        heatmap_data = mean_tots.pivot(index="row", columns="col", values="tot")
        # Ensure a complete 5×5 grid and fill missing pixels with zero
        rows = list(range(row_min, row_max + 1))
        cols = list(range(col_min, col_max + 1))
        heatmap_data = heatmap_data.reindex(index=rows, columns=cols, fill_value=np.nan)
        plt.figure(figsize=(10, 8))
        ax = sns.heatmap(
            heatmap_data,
            cmap="viridis",
            cbar_kws={"label": "ToT [25ns]"},
            square=True,
            annot=True,
            annot_kws={"size": 18},
            fmt=".2f",
        )
        # Draw a black border around the heatmap frame
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(1)
            spine.set_color('black')
        ax.set_title(f"ToT per pixel")
        plt.tight_layout()
        plt.savefig(f"Focus at ({center_col}, {center_row}).png", dpi=600)
        plt.show()

    def _FilterAndUnwrap(self, df: pd.DataFrame) -> pd.DataFrame:
        # Parse each cell into a list
        for c in ["col", "row", "tot"]:
            df[c] = df[c].apply(self._ParseList)

        # Zip the three lists together so they explode in parallel
        df["combined"] = df.apply(
            lambda r: list(zip(r["row"], r["col"], r["tot"])), axis=1
        )
        df_exploded = df.explode("combined")

        # Unpack the tuples back into separate columns
        df_exploded[["row", "col", "tot"]] = pd.DataFrame(
            df_exploded["combined"].tolist(), index=df_exploded.index
        )
        df_exploded = df_exploded.drop(columns=["combined"])
        return df_exploded

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


if __name__ == "__main__":
    # focus = Focus(AttenuationVoltage=3.5, direction="y")
    # focus.ProcessAll()
    # plotter = FocusPlotter(direction="y", AttenuationVoltage=3.5, ROW=230, COL=228)
    # plotter.Plot_ToT()
    # plotter.Plot_Charge()
    visualizer = FocusVisualizer(
        "Data/Focus/Z/ZFocus 3.5 V/focus_39p500/N116-250502-152529.root"
    )
    visualizer.CreateHitmap()
