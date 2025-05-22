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
    mean = df[df["tot"] > 150]["tot"].mean()
    plt.figure(figsize=(12, 8))
    plt.hist(df["tot"], bins=100, color="blue", alpha=0.7, label = f"Pixel ({COL}, {ROW}); Mean above threshold: {mean:.2f} [25 ns]")
    plt.axvline(150, color="red", linestyle="--", label="Threshold")
    plt.xlabel("ToT [25 ns]")
    plt.ylabel("Counts")
    # plt.title(f"ToT Histogram for Pixel ({COL}, {ROW})")
    plt.xlim(0, 200)
    plt.xticks(range(0, 201, 20))
    plt.legend(loc = "upper right", fontsize = 16)
    plt.tight_layout()
    plt.savefig("ToTHistogram.png", dpi=600)
    plt.show()
