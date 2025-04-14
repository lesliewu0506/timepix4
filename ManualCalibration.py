import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def PlotHistogram(df: pd.DataFrame = None, filepath: str = None):
    if filepath is not None:
        df = pd.read_csv(filepath)

    df.loc[df["charge"] > 25, "charge"] = np.nan

    ax = df.hist(
        column="charge", bins=240, grid=False, figsize=(10, 7), color="blue", alpha=0.7
    )

    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    plt.xlim(0, 20)

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

    plt.legend()
    plt.title("N116 Manual Calibrated Charge Distribution")
    plt.grid(False)
    plt.savefig("N116_Charge_Distribution_Manual.png", dpi=600)
    plt.show()


def PlotCharge(filepaths: list[str]):
    plt.figure(figsize=(16, 10))

    colors = ["blue", "orange", "green", "red", "purple", "brown"]
    histogram_info = []  # List to store tuples of (data, label, color)
    color_index = 0

    for filepath in filepaths:
        df = pd.read_csv(f"Data/Filtered Calibration Data/{filepath}-Charge-Data.csv")

        df.loc[df["Raw Charge"] > 25, "Raw Charge"] = np.nan

        data_test_pulse = df["Raw Charge"].dropna()

        file_label = filepath.split("-")[0]
        label_test = file_label

        histogram_info.append(
            (data_test_pulse, label_test, colors[color_index % len(colors)])
        )
        color_index += 1

    for data, label, color in histogram_info:
        plt.hist(data, bins=200, alpha=0.6, label=label, color=color, density=True)

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
    plt.ylabel("Counts (Normalized)")
    plt.xlim(0, 20)
    plt.title("N112 vs N113 Charge Distribution Calibrated")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Charge_Distribution_N112_N113.png", dpi=600)
    plt.show()


def PlotCompare(filepath):
    filename = filepath.split("-")[0]
    df = pd.read_csv(f"Data/Filtered Calibration Data/{filepath}-Charge-Data.csv")

    df.loc[df["charge"] > 25, "charge"] = np.nan
    df.loc[df["Raw Charge"] > 25, "Raw Charge"] = np.nan
    data_test_pulse = df["Raw Charge"].dropna()
    data_manual = df["charge"].dropna()

    plt.figure(figsize=(12, 6))
    plt.hist(
        data_test_pulse,
        bins=400,
        alpha=0.6,
        label="Test Pulse Calibration",
        color="blue",
        density=True,
    )
    plt.hist(
        data_manual,
        bins=400,
        alpha=0.6,
        label="Manual Calibration",
        color="orange",
        density=True,
    )

    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    plt.xlim(0, 20)

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

    plt.title(f"Charge Distribution {filename}")
    plt.grid(False)
    plt.legend()
    plt.savefig(f"{filename}_Charge_Distribution_ManualvsTestPulse.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    # filepath = "N116-250403-150114-filtered.csv"
    # filepath = "N116-250408-123554.csv"
    filepaths = ["N10-250404-143700", "N116-250403-150114"]
    filepath2 = ["N112-250411-101613", "N113-250408-100406"]
    # PlotCompare("N10-250409-113850")
    # PlotCharge(filepaths)
    PlotCharge(filepath2)
