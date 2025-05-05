import pandas as pd
import matplotlib.pyplot as plt


def ParameterComparison(filepath1: str, filepath2: str):
    Sensor1 = filepath1.split("/")[-1].split("-")[0]
    df1 = _LoadData(filepath1)

    Sensor2 = filepath2.split("/")[-1].split("-")[0]
    df2 = _LoadData(filepath2)

    plt.figure(figsize=(12, 8))
    plt.hist(df1["p0"], bins=50, alpha=0.5, label=Sensor1, density=True)
    plt.hist(df2["p0"], bins=50, alpha=0.5, label=Sensor2, density=True)
    plt.legend(loc = "best")
    plt.tight_layout()
    plt.savefig(f"Histogram of p0 Values {Sensor1} vs {Sensor2}.png", dpi=600)
    plt.show()


def _LoadData(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df
