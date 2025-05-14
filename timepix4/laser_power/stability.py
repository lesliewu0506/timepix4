import pandas as pd
import matplotlib.pyplot as plt


def PlotLaserStability(filepath: str) -> None:
    means = []
    std = []
    df = pd.read_csv(filepath)
    df_filtered = df[((df["row"] == 230) & (df["col"] == 228))]
    for i in range(0, 61):
        filtered = df_filtered.iloc[i * 60000 : i * 60000 + 60000]
        means.append(filtered["tot"].mean())
        std.append(filtered["tot"].std())
        # means.append(filtered["Charge"].mean())
        # std.append(filtered["Charge"].std())

    plt.figure(figsize=(14, 8))
    plt.errorbar(
        range(0, 61),
        means,
        yerr=std,
        fmt="o",
        markersize=4,
        capsize=4,
        linestyle="-",
    )
    plt.xlabel("Time [min]", fontsize=16)
    plt.ylabel("ToT [25 ns]", fontsize=16)
    # plt.ylabel("Charge [ke]", fontsize=16)
    plt.title("Laser Stability", fontsize=16)
    plt.ylim(0, 300)
    # plt.ylim(0, 20)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid()
    plt.tight_layout()
    plt.savefig("LaserStabilityToT.png", dpi=600)
    # plt.savefig("LaserStabilityCharge.png", dpi=600)
    plt.show()
