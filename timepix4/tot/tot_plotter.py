import pandas as pd
import matplotlib.pyplot as plt


def ToTPlotter(filepath: str, COL: int = 228, ROW: int = 230) -> None:
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
    df = pd.read_csv(filepath)
    df = df[(df["col"] == COL) & (df["row"] == ROW)]
    df = df[df["tot"] > 0]
    # df = df[((df["Charge"] < 18) & (df["Charge"] > 0))]
    # mean = df[df["tot"] > 150]["tot"].mean()
    # mean = df["Charge"].mean()
    plt.figure(figsize=(12, 8))
    plt.hist(
        # df["tot"],
        df["tot"] * 0.10437223461349657,
        # df["Charge"],
        bins=180,
        color="blue",
        alpha=0.7,
        # label=f"Pixel ({COL}, {ROW}); Mean above threshold: {mean:.2f} [25 ns]",
    )
    # plt.xlabel("ToT [25 ns]")
    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    # plt.title(f"ToT Histogram for Pixel ({COL}, {ROW})")
    # plt.xlim(0, 200)
    # plt.ylim(0, 70)
    # plt.xticks(range(0, 201, 20))
    plt.xlim(0, 18)
    plt.ylim(0, 40)
    plt.xticks(range(0, 19, 2))
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
    plt.legend(loc = "best", fontsize = 16)
    plt.tight_layout()
    plt.savefig("ToTHistogram.png", dpi=300)
    plt.show()
