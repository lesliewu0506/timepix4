import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def FourToTPlotter(filepath: str) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 22,
            "axes.labelsize": 20,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "figure.titlesize": 20,
        }
    )
    df = pd.read_csv(filepath)
    df = df[(df["col"] >= 224) & (df["row"] >= 256)]
    df = df[((df["Charge"] < 20) & (df["Charge"] > 0))]
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.hist(
        # df["tot"],
        df["Charge"], 
        bins=150,
        color="blue",
        alpha=0.7,
    )
    plt.xlim(0, 18)
    plt.ylim(0, 2500000)
    # plt.ylim(0, 4000000)
    ax.tick_params(axis="both", which="major", length=12, width=2, direction="in")
    ax.tick_params(axis="both", which="minor", length=6, width=2, direction="in")

    ax.set_xticks(np.arange(0, 18, 4))
    ax.set_xticks(np.arange(0, 18.1, 1), minor=True)
    ax.set_yticks(np.arange(0, 2500001, 500000))
    ax.set_yticks(np.arange(0, 2500001, 125000), minor=True)
    # ax.set_yticks(np.arange(0, 4100000, 1000000))
    # ax.set_yticks(np.arange(0, 4100000, 200000), minor=True)

    vlines = [
        {"x": 2.225, "color": "red", "label": "8.01 keV"},
        {"x": 3.861, "color": "green", "label": "13.9 keV"},
        {"x": 4.917, "color": "blue", "label": "17.7 keV"},
        {"x": 5.75, "color": "magenta", "label": "20.7 keV"},
        {"x": 7.306, "color": "cyan", "label": "26.3 keV"},
        {"x": 16.5, "color": "orange", "label": "59.5 keV"},
    ]
    for line in vlines:
        plt.axvline(
            x=line["x"], color=line["color"], linestyle="--", label=line["label"]
        )

    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    ax.legend(
        loc="upper center",  # or whatever corner you like
        bbox_to_anchor=(0.58, 0.98),  # move it just outside the axes
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
    # plt.savefig("TestPulseHistogram(228,230).png", dpi=300)
    # plt.savefig("RawToTHistogram.png", dpi=300)
    # plt.savefig("ChargeHistogram.png", dpi=300)
    # plt.savefig("ToTHistogram(228, 230).png", dpi=300)
    # plt.savefig("TestCalibratedChargeHistogram.png", dpi=300)
    # plt.savefig("TestPulseRefactored2.png", dpi=300)
    # plt.savefig("TestPulseRefactoredChargeHistogramOne.png", dpi=300)
    plt.savefig("TR", dpi= 300)
    plt.show()