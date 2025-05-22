import pandas as pd
import matplotlib.pyplot as plt


def PlotLaserStability(filepath: str) -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 22,
            "axes.labelsize": 18,
            "xtick.labelsize": 16,
            "ytick.labelsize": 16,
            "figure.titlesize": 22,
        }
    )
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

    plt.figure(figsize=(10, 8))
    plt.errorbar(
        range(0, 61),
        means,
        yerr=std,
        fmt="o",
        markersize=4,
        capsize=4,
        linestyle="-",
    )
    plt.xlabel("Time [min]")
    plt.ylabel("ToT [25 ns]")
    # plt.ylabel("Charge [ke]")
    # plt.title("Laser Stability")
    plt.xlim(0, 60)
    plt.ylim(0, 70)
    # plt.ylim(15, 20)
    plt.grid()
    plt.tight_layout()
    plt.savefig("LaserStabilityToT.png", dpi=300)
    # plt.savefig("LaserStabilityCharge.png", dpi=300)
    plt.show()
