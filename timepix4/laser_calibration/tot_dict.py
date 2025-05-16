import pandas as pd
import ast


def LoadCorrectionFactors() -> dict[tuple[int, int], float]:
    df = pd.read_csv(
        f"Data/Filtered Calibration Data/N116-250408-123554-CorrectionFactors.csv"
    )
    df["pixel"] = df["pixel"].apply(lambda x: ast.literal_eval(str(x)))
    df["correction"] = df["correction"].astype(float)
    df["row"] = df["pixel"].apply(lambda p: p[1])
    df["col"] = df["pixel"].apply(lambda p: p[0])
    df = df[
        ((df["row"] > 219) & (df["row"] < 231) & (df["col"] > 227) & (df["col"] < 239))
    ]
    df["ToT"] = 16.5 / df["correction"]
    df = df.drop(columns=["pixel", "correction"])
    df.to_csv("LaserCalToT.csv", index=False)
