import pandas as pd
import matplotlib.pyplot as plt
import ast


def PlotManualCalibratedCharge(filepath: str) -> None:
    sensor = filepath.split("/")[-1].split("-")[0]
    CorrectionFactors = _LoadCorrectionFactors()
    df = _LoadCSV(filepath)
    df["charge"] = df.apply(
        lambda row: row["tot"] * CorrectionFactors.get(row["pixel"], 1), axis=1
    )
    df.hist(
        column="charge",
        bins=7500,
        grid=False,
        figsize=(10, 7),
        color="blue",
        alpha=0.7,
        density=True,
    )

    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    plt.xlim(0, 25)

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
    plt.title(f"{sensor} Manual Calibrated Charge Distribution With Am-241 Source")
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(f"{sensor}_Charge_Distribution_Manual.png", dpi=600)
    plt.show()


def _LoadCorrectionFactors() -> dict[tuple[int, int], float]:
    df = pd.read_csv(
        f"Data/Filtered Calibration Data/N116-250408-123554-CorrectionFactors.csv"
    )
    df["pixel"] = df["pixel"].apply(lambda x: ast.literal_eval(str(x)))
    df["correction"] = df["correction"].astype(float)

    charge_dict = {
        pixel: correction for pixel, correction in zip(df["pixel"], df["correction"])
    }
    return charge_dict


def _LoadCSV(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, usecols=["col", "row", "tot"])
    df["pixel"] = list(zip(df["col"], df["row"]))
    return df
