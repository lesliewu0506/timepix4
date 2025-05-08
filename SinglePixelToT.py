import pandas as pd
import matplotlib.pyplot as plt


def ToTChargePlotter(FilePath: str) -> None:
    df = pd.read_csv(FilePath)
    df_filtered = df[(df["row"] == 230) & (df["col"] == 228)]
    fig, ax = plt.subplots(figsize=(12, 8))

    plt.hist(df_filtered["charge"], bins=100, alpha=0.5, label="Charge")
    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    plt.tight_layout()
    plt.savefig("tot.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    ToTChargePlotter(
        "Data/Filtered Calibration Data/N116-250408-123554-Charge-Data.csv"
    )
