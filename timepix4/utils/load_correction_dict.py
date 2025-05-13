import pandas as pd
import ast


def createdicts():
    df = pd.read_csv(
        f"Data/Filtered Calibration Data/N116-250408-123554-CorrectionFactors.csv"
    )
    df["pixel"] = df["pixel"].apply(lambda x: ast.literal_eval(str(x)))
    df["correction"] = df["correction"].astype(float)

    charge_dict = {
        pixel: correction for pixel, correction in zip(df["pixel"], df["correction"])
    }
    return charge_dict