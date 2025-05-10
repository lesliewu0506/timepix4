import pandas as pd
import matplotlib.pyplot as plt


def ToTChargePlotter(FilePath: str) -> None:
    df = pd.read_csv(FilePath)
    df_copy = df.copy()
    # df = df[(df["Mean Charge Raw"] < 100)]
    lookuptable = pd.read_csv("lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    fig, ax = plt.subplots(figsize=(12, 8))
    # plt.errorbar(
    #     df["Mean Charge Raw"],
    #     df["Mean clTot"],
    #     xerr=df["Std Charge Raw"],
    #     fmt="o",
    #     markersize=4,
    #     linestyle="none",
    #     # color="blue",
    #     label="Test Pulse",
    # )
    # plt.plot(
    #     df["Mean Charge Raw"],
    #     df["Mean clTot"],
    #     linestyle="-",
    #     # color="red",
    # )
    plt.errorbar(
        df["Mean clCharge"],
        df["Mean clTot"],
        xerr=df["Std clCharge"],
        fmt="o",
        markersize=4,
        linestyle="none",
        # color="cyan",
        label="Test Pulse Calibration",
    )
    plt.plot(
        df["Mean clCharge"],
        df["Mean clTot"],
        linestyle="-",
        # color="green",
    )
    plt.errorbar(
        df["Mean Charge Calibrated"],
        df["Mean clTot"],
        xerr=df["Std Charge Calibrated"],
        fmt="o",
        markersize=4,
        linestyle="none",
        # color="yellow",
        label="Manual Calibration",
    )
    plt.plot(
        df["Mean Charge Calibrated"],
        df["Mean clTot"],
        linestyle="-",
        # color="pink",
    )

    plt.plot(
        lookuptable["Charge"],
        df_copy["Mean clTot"],
        marker="o",
        markersize=4,
        linestyle="-",
        color="black",
        label="Laser Calibration",
    )
    # Set labels and title
    ax.set_xlabel("Charge [ke]")
    ax.set_ylabel("ToT [25ns]")
    ax.set_title("clToT vs clCharge")
    # ax.set_xlim(0, 150)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 200)
    ax.set_yticks(range(0, 201, 20))
    ax.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("ToT_Charge.png", dpi=600)
    plt.show()
