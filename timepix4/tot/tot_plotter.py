import pandas as pd
import matplotlib.pyplot as plt


def ToTPlotter(filepath: str, COL: int = 228, ROW: int = 230) -> None:
    df = pd.read_csv(filepath)
    df = df[(df["col"] == COL) & (df["row"] == ROW)]

    plt.figure(figsize=(12, 8))
    plt.hist(df["tot"], bins=100, color="blue", alpha=0.7)
    plt.xlabel("ToT [25 ns]")
    plt.ylabel("Counts")
    plt.title(f"ToT Histogram for Pixel ({COL}, {ROW})")
    plt.xlim(0, 200)
    plt.xticks(range(0, 201, 20))
    plt.tight_layout()
    plt.savefig("ToTHistogram.png", dpi=600)
    plt.show()
