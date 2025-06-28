import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def DirectRelativePower(filepath: str, V_ref: float) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 20,
            "axes.labelsize": 20,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "figure.titlesize": 20,
        }
    )
    df = pd.read_csv(filepath)
    reference_value = df.loc[df["V"] == V_ref, "power"].iloc[0]
    df["relative_power"] = df["power"] / reference_value
    V = df["V"].to_numpy()
    relative_power = df["relative_power"].to_numpy()
    dataframe = pd.DataFrame({"voltage": V, "relative_factor": relative_power})
    dataframe.to_csv("lookup_table.csv", index=False)
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.scatter(
        V, relative_power, marker="o", s=60, color="b", label="Pixel (228, 230)"
    )
    plt.axhline(y=1, color="r", linestyle="--", label="Relative Power = 1")
    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Relative Power [a.u.]")
    plt.xlim(2.9, 4.00)
    plt.ylim(0, 40)

    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(3.0, 4.05, 0.20))
    ax.set_xticks(np.arange(2.9, 4.05, 0.05), minor=True)
    ax.set_yticks(np.arange(0, 41, 10))
    ax.set_yticks(np.arange(0, 41, 2.5), minor=True)
    plt.yticks(np.arange(0, 41, 10))
    plt.grid()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
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
    plt.tight_layout()
    plt.savefig("relative_power_plot.png", dpi=300)
    plt.show()

    # plt.figure(figsize=(10, 8))
    # plt.scatter(df["V"].to_numpy(), df["power"].to_numpy(), marker="o", color="b")
    # plt.xlabel("Attenuation Voltage [V]")
    # plt.ylabel("Power [$\mu$W]")
    # plt.xlim(2.8, 4.0)
    # plt.ylim(0, 14)
    # # plt.yticks(np.arange(0, 16, 3))
    # plt.grid()
    # plt.tight_layout()
    # plt.savefig("PowerVsVoltage.png", dpi=300)
    # plt.show()
