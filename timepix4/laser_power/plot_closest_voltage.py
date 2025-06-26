import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def PlotClosestVoltage(filepath: str, tot_ref: float) -> None:
    df = pd.read_csv(filepath)
    df = df[df["AttenuationVoltage"] > 3.575]
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
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.errorbar(
        df["AttenuationVoltage"],
        df["Mean Tot"],
        yerr=df["Std Tot"],
        fmt="o",
        markersize=3,
        linestyle="None",
        capsize=3,
        color="b",
        label="Mean ToT",
    )
    plt.axhline(
        tot_ref,
        color="red",
        linestyle="--",
        label=f"Reference ToT: {tot_ref:.3g} [25 ns]",
    )
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("ToT [25 ns]")

    plt.xlim(3.6, 4)
    plt.ylim(0, 400)

    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(3.6, 4.1, 0.1))
    ax.set_xticks(np.arange(3.6, 4.01, 0.025), minor=True)
    ax.set_yticks(np.arange(0, 401, 100))
    ax.set_yticks(np.arange(0, 401, 25), minor=True)

    ax.legend(
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
        fontsize=20,
    )
    plt.grid()
    ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    plt.savefig("ClosestVoltage.png", dpi=300)
    plt.show()
