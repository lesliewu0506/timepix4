import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf
import matplotlib.ticker as ticker


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
                "axes.labelsize": 20,
                "xtick.labelsize": 20,
                "ytick.labelsize": 20,
                "figure.titlesize": 22,
            }
        )
        _, ax = plt.subplots(figsize=(12, 10))
        ax2 = ax.twinx()

        # Plot Cluster ToT
        ax.errorbar(
            self.df["Position"],
            self.df["mean_cltot"],
            yerr=self.df["std_cltot"],
            marker="o",
            # linestyle="-",
            linestyle="None",
            # capsize=3,
            label="Mean clToT",
            markersize=5,
        )

        # Plot Cluster Size
        ax2.errorbar(
            self.df["Position"],
            self.df["mean_clustersize"],
            yerr=self.df["std_clustersize"],
            marker="s",
            linestyle="None",
            # capsize=3,
            color="green",
            label="Mean cluster size",
            markersize=5,
        )

        # Plot ToT
        # ax.errorbar(
        #     self.df["Position"],
        #     self.df["mean_tot"],
        #     yerr=self.df["std_tot"],
        #     marker="o",
        #     linestyle="None",
        #     # linestyle="-",
        #     # capsize=3,
        #     label=f"Mean ToT ({self.COL}, {self.ROW})",
        #     markersize=5,
        # )

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
                # linestyle="None",
                # capsize=3,
                label=label_prev,
                markersize=5,
            )
            # Plot ToT
            ax.errorbar(
                self.df["Position"],
                self.df["mean_tot"],
                yerr=self.df["std_tot"],
                marker="o",
                # linestyle="None",
                linestyle="-",
                # capsize=3,
                label=f"Mean ToT ({self.COL}, {self.ROW})",
                markersize=5,
            )
            ax.errorbar(
                self.df["Position"],
                self.df["mean_tot_next"],
                yerr=self.df["std_tot_next"],
                marker="o",
                linestyle="-",
                # linestyle="None",
                # capsize=3,
                label=label_next,
                markersize=5,
            )

        # ax.set_xlim(38.5, 41)
        # ax.set_ylim(0, 600)
        # ax2.set_ylim(0, 20)

        # ax.set_xlim(18.125, 18.325)
        ax.set_xlim(42.275, 42.475)

        ax.set_ylim(0, 750)
        ax2.set_ylim(0, 10)
        

        witdh = 2
        ax.tick_params(axis="y", which="major", length=12, width=witdh, direction="in")
        ax.tick_params(axis="y", which="minor", length=6, width=witdh, direction="in")
        ax2.tick_params(axis="y", which="major", length=12, width=witdh, direction="in")
        ax2.tick_params(axis="y", which="minor", length=6, width=witdh, direction="in")
        ax.tick_params(axis="x", which="major", length=12, width=witdh, direction="in")
        ax.tick_params(axis="x", which="minor", length=6, width=witdh, direction="in")

        # ax.set_xticks(np.arange(38.5, 41.1, 0.5))
        # ax.set_xticks(np.arange(38.5, 41, 0.1), minor=True)
        # ax.set_yticks(np.arange(0, 601, 150))
        # ax.set_yticks(np.arange(0, 601, 30), minor=True)
        # ax2.set_yticks(np.arange(0, 21, 5))
        # ax2.set_yticks(np.arange(0, 21, 1), minor=True)

        # ax.set_xticks(np.arange(18.125, 18.326, 0.05))
        # ax.set_xticks(np.arange(18.125, 18.326, 0.01), minor=True)

        ax.set_xticks(np.arange(42.275, 42.476, 0.05))
        ax.set_xticks(np.arange(42.275, 42.476, 0.01), minor=True)

        ax.set_yticks(np.arange(0, 751, 150))
        ax.set_yticks(np.arange(0, 751, 30), minor=True)
        ax2.set_yticks(np.arange(0, 10.1, 2))
        ax2.set_yticks(np.arange(0, 10.1, 0.4), minor=True)

        ax.set_xlabel(f"{self.direction}-position [mm]")
        ax.set_ylabel("ToT [25 ns]")
        ax2.set_ylabel("Cluster size [pixels]")
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        # ax.legend(
        #     lines + lines2,
        #     labels + labels2,
        #     loc="lower right",  # or whatever corner you like
        #     bbox_to_anchor=(0.87, 0.02),  # move it just outside the axes
        #     borderaxespad=0.5,  # padding between axes and legend
        #     frameon=True,  # draw a frame
        #     fancybox=False,  # straight corners (disable rounded box)
        #     edgecolor="black",  # color of the border
        #     framealpha=1.0,  # fully opaque
        #     labelspacing=0.3,  # vertical space between entries
        #     handlelength=2.5,  # length of the legend lines
        #     handletextpad=0.5,  # space between line and label
        #     borderpad=0.4,  # padding inside the legend box
        #     fontsize=17,
        # )
        # ax.legend(
        #     lines + lines2,
        #     labels + labels2,
        #     loc="upper left",  # or whatever corner you like
        #     bbox_to_anchor=(0.02, 0.98),  # move it just outside the axes
        #     borderaxespad=0.5,  # padding between axes and legend
        #     frameon=True,  # draw a frame
        #     fancybox=False,  # straight corners (disable rounded box)
        #     edgecolor="black",  # color of the border
        #     framealpha=1.0,  # fully opaque
        #     labelspacing=0.3,  # vertical space between entries
        #     handlelength=2.5,  # length of the legend lines
        #     handletextpad=0.5,  # space between line and label
        #     borderpad=0.4,  # padding inside the legend box
        #     fontsize=17,
        # )
        ax.legend(
            lines + lines2,
            labels + labels2,
            loc="upper right",  # or whatever corner you like
            bbox_to_anchor=(0.98, 0.98),  # move it just outside the axes
            borderaxespad=0.5,  # padding between axes and legend
            frameon=True,  # draw a frame
            fancybox=False,  # straight corners (disable rounded box)
            edgecolor="black",  # color of the border
            framealpha=1.0,  # fully opaque
            labelspacing=0.3,  # vertical space between entries
            handlelength=2.5,  # length of the legend lines
            handletextpad=0.5,  # space between line and label
            borderpad=0.4,  # padding inside the legend box
            fontsize=17,
        )
        ax.grid(True)
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
        plt.tight_layout()
        plt.savefig(
            f"{self.direction.capitalize()}ScanPlot{self.AttenuationVoltage}.png",
            dpi=300,
        )
        plt.show()

    def Plot_Charge(self) -> None:
        plt.rcParams.update(
            {
                "font.size": 20,
                "axes.titlesize": 22,
                "axes.labelsize": 20,
                "xtick.labelsize": 20,
                "ytick.labelsize": 20,
                "figure.titlesize": 22,
            }
        )
        _, ax = plt.subplots(figsize=(12, 10))
        ax2 = ax.twinx()

        # Plot Cluster Charge
        ax.errorbar(
            self.df["Position"],
            self.df["mean_clcharge"],
            yerr=self.df["std_clcharge"],
            marker="o",
            linestyle="None",
            # capsize=3,
            label=f"Mean clCharge",
            markersize=5,
        )

        # Plot Cluster Size
        ax2.errorbar(
            self.df["Position"],
            self.df["mean_clustersize"],
            yerr=self.df["std_clustersize"],
            marker="s",
            linestyle="None",
            # capsize=3,
            color="green",
            label="Mean cluster size",
            markersize=5,
        )

        # Plot Charge
        # ax.errorbar(
        #     self.df["Position"],
        #     self.df["mean_charge"],
        #     yerr=self.df["std_charge"],
        #     marker="o",
        #     linestyle="None",
        #     capsize=3,
        #     label=f"Mean Charge ({self.COL}, {self.ROW})",
        #     markersize=4,
        # )
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
                # capsize=3,
                label=label_prev,
                markersize=5,
            )
            # Plot Charge
            ax.errorbar(
                self.df["Position"],
                self.df["mean_charge"],
                yerr=self.df["std_charge"],
                marker="o",
                linestyle="-",
                # capsize=3,
                label=f"Mean Charge ({self.COL}, {self.ROW})",
                markersize=5,
            )
            ax.errorbar(
                self.df["Position"],
                self.df["mean_charge_next"],
                yerr=self.df["std_charge_next"],
                marker="o",
                linestyle="-",
                # capsize=3,
                label=label_next,
                markersize=5,
            )

        # ax.set_xlim(18.125, 18.325)
        # ax.set_xlim(42.275, 42.475)
        ax.set_ylim(0, 75)
        ax2.set_ylim(0, 10)

        witdh = 2
        ax.tick_params(axis="y", which="major", length=12, width=witdh, direction="in")
        ax.tick_params(axis="y", which="minor", length=6, width=witdh, direction="in")
        ax2.tick_params(axis="y", which="major", length=12, width=witdh, direction="in")
        ax2.tick_params(axis="y", which="minor", length=6, width=witdh, direction="in")
        ax.tick_params(axis="x", which="major", length=12, width=witdh, direction="in")
        ax.tick_params(axis="x", which="minor", length=6, width=witdh, direction="in")

        # ax.set_xticks(np.arange(18.125, 18.326, 0.050))
        # ax.set_xticks(np.arange(18.125, 18.330, 0.010), minor=True)
        ax.set_xticks(np.arange(42.275, 42.476, 0.050))
        ax.set_xticks(np.arange(42.275, 42.476, 0.010), minor=True)

        ax.set_yticks(np.arange(0, 76, 15))
        ax.set_yticks(np.arange(0, 76, 3), minor=True)
        ax2.set_yticks(np.arange(0, 11, 2))
        ax2.set_yticks(np.arange(0, 10, 0.4), minor=True)

        # left_ticks = np.linspace(min_lim, max_lim, num_ticks)
        # ax.set_ylim(min_lim, max_lim)
        # ax.set_yticks(left_ticks)
        # ax.set_yticks(np.arange(0, 76, 15))
        # ax2.set_yticks(np.linspace(0, max_cs, num_ticks))
        # ax.set_xticks(np.arange(42.275, 42.501, 0.050))

        ax.set_xlabel(f"{self.direction}-position [mm]")
        ax.set_ylabel("Charge [ke]")
        ax2.set_ylabel("Cluster size [pixels]")

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        # ax.legend(lines + lines2, labels + labels2, loc="center right", fontsize=12)
        ax.legend(
            lines + lines2,
            labels + labels2,
            loc="upper right",  # or whatever corner you like
            bbox_to_anchor=(0.99, 0.99),  # move it just outside the axes
            borderaxespad=0.5,  # padding between axes and legend
            frameon=True,  # draw a frame
            fancybox=False,  # straight corners (disable rounded box)
            edgecolor="black",  # color of the border
            framealpha=1.0,  # fully opaque
            labelspacing=0.3,  # vertical space between entries
            handlelength=2.5,  # length of the legend lines
            handletextpad=0.5,  # space between line and label
            borderpad=0.4,  # padding inside the legend box
            fontsize=17,
        )
        ax.grid(True)
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
        # plt.xlim(42.275, 42.475)
        # plt.xlim(18.125, 18.325)
        # plt.xlim(38.5, 41)
        plt.tight_layout()

        plt.savefig(
            f"{self.direction.capitalize()}ScanPlotCharge{self.AttenuationVoltage}.png",
            dpi=300,
        )
        plt.show()
