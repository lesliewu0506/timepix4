import pandas as pd
import matplotlib.pyplot as plt


def STDHistogramComparison(filepaths: list[str]):
    plt.figure(figsize=(12, 10))

    for filepath, color in zip(filepaths, ["blue", "orange", "green", "red"]):
        sensor = filepath.split("/")[-1].split("-")[0]
        df = _LoadCSV(filepath)
        df["stdvTot"] = df["stdvTot"] / df["meanTot"] * 100
        plt.hist(df["stdvTot"], bins=100, alpha=0.3, label=sensor, color=color)

    plt.xlabel("std ToT [%]")
    plt.ylabel("Frequency")
    plt.title("std ToT Histogram Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig("stdTot_Histogram_Comparison.png", dpi=600)
    plt.show()


def _LoadCSV(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df
