import ast
import pandas as pd


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


def parse_list(x):
    if isinstance(x, str):
        parsed = ast.literal_eval(x)
        if isinstance(parsed, (list, tuple)):
            return list(parsed)
        else:
            return [parsed]
    elif isinstance(x, (list, tuple)):
        return list(x)
    else:
        return [x]
