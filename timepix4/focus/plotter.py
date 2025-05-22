import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf


class ScanPlotter:
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
        plt.rcParams.update(
            {
                "font.size": 20,
                "axes.titlesize": 22,
                "axes.labelsize": 18,
                "xtick.labelsize": 16,
                "ytick.labelsize": 16,
                "figure.titlesize": 22,
            }
        )
        _, ax = plt.subplots(figsize=(14, 8))
        ax2 = ax.twinx()

        # Plot Cluster ToT
        ax.errorbar(
            self.df["Position"],
            self.df["mean_cltot"],
            yerr=self.df["std_cltot"],
            marker="o",
            # linestyle="-",
            linestyle="None",
            capsize=3,
            label="Mean clToT",
            markersize=4,
        )

        # Plot Cluster Size
        ax2.errorbar(
            self.df["Position"],
            self.df["mean_clustersize"],
            yerr=self.df["std_clustersize"],
            marker="s",
            linestyle="None",
            capsize=3,
            color="green",
            label="Mean cluster size",
            markersize=4,
        )

        # Plot ToT
        ax.errorbar(
            self.df["Position"],
            self.df["mean_tot"],
            yerr=self.df["std_tot"],
            marker="o",
            # linestyle="None",
            linestyle="-",
            capsize=3,
            label=f"Mean ToT ({self.COL}, {self.ROW})",
            markersize=4,
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
                capsize=3,
                label=label_prev,
                markersize=4,
            )
                    # Plot ToT
            ax.errorbar(
                self.df["Position"],
                self.df["mean_tot"],
                yerr=self.df["std_tot"],
                marker="o",
                # linestyle="None",
                linestyle="-",
                capsize=3,
                label=f"Mean ToT ({self.COL}, {self.ROW})",
                markersize=4,
            )
            ax.errorbar(
                self.df["Position"],
                self.df["mean_tot_next"],
                yerr=self.df["std_tot_next"],
                marker="o",
                linestyle="-",
                capsize=3,
                label=label_next,
                markersize=4,
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
        ax.set_ylabel("ToT [25 ns]")
        ax2.set_ylabel("Cluster size [pixels]")
        plt.xlim(38.5, 41)
        # ax.set_title(
        #     f"{self.direction.capitalize()} Scan ToT: Pixel ({self.COL}, {self.ROW})"
        # )
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc="best", fontsize=14)
        ax.grid(True)
        plt.tight_layout()
        plt.savefig(
            f"{self.direction.capitalize()}ScanPlot{self.AttenuationVoltage}.png",
            dpi=300,
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
