import pandas as pd
import matplotlib.pyplot as plt


def LaserToTPlotter(file1, file2, file3) -> None:
    lookuptable = pd.read_csv(f"1lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    fig, ax = plt.subplots(figsize=(12, 8))
    df = pd.read_csv(file1)
    plt.errorbar(
        df["Mean clCharge"],
        df["Mean clTot"],
        xerr=df["Std clCharge"],
        fmt="o",
        markersize=4,
        linestyle="-",
        label="Test Pulse Calibration",
    )

    plt.errorbar(
        df["Mean Charge Calibrated"],
        df["Mean clTot"],
        xerr=df["Std Charge Calibrated"],
        fmt="o",
        markersize=4,
        linestyle="-",
        label="Manual Calibration",
    )

    plt.plot(
        lookuptable["Charge"],
        df["Mean clTot"],
        marker="o",
        markersize=4,
        linestyle="-",
        label="Laser Calibration",
    )

    lutfiltered = lookuptable[lookuptable["voltage"] == 3.3]
    df1 = df[df["AttenuationVoltage"] == 3.3]
    plt.plot(
        lutfiltered["Charge"] / 1, df1["Mean clTot"], "o", markersize=4, label="Point 1"
    )
    df2 = pd.read_csv(file2)
    df2 = df2[df2["AttenuationVoltage"] == 3.3]

    plt.plot(
        lutfiltered["Charge"] / 2, df2["Mean Tot"], "o", markersize=4, label="Point 2"
    )
    df3 = pd.read_csv(file3)
    df3 = df3[df3["AttenuationVoltage"] == 3.3]
    plt.plot(
        lutfiltered["Charge"] / 4, df3["Mean Tot"], "o", markersize=4, label="Point 4"
    )

    plt.xlabel("Injected Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.xlim(0, 200)
    plt.ylim(0, 2000)
    plt.title("clToT vs clCharge")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def ToTChargePlotter(FilePaths: list[str]) -> None:
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    lookuptable = pd.read_csv(f"1lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    for FilePath in FilePaths:
        pixels = FilePath.split("/")[-1].split(".")[0]
        df = pd.read_csv(FilePath)
        # if pixels[0] == "1":
        #     lookuptable = pd.read_csv(f"{pixels[0]}lookup_table.csv")
        #     lookuptable = lookuptable.sort_values("voltage", ascending=True)
        #     lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
        df["Mean clTot"] = df["Mean clTot"] / int(FilePath.split("/")[-1][0])
        ax[0].errorbar(
            df["Mean clCharge"],
            df["Mean clTot"],
            xerr=df["Std clCharge"],
            fmt="o",
            markersize=4,
            linestyle="-",
            label=f"{pixels[0]} Pixels",
        )

        if len(df) < len(lookuptable):
            lut = lookuptable.iloc[: len(df)]
        else:
            lut = lookuptable

        # if pixels[0] == "1":
        #     ax[0].plot(
        #         lut["Charge"],
        #         df["Mean clTot"],
        #         marker="o",
        #         markersize=4,
        #         linestyle="-",
        #         label="Laser Calibration",
        #     )
        # else:
        ax[1].plot(
            lut["Charge"],
            df["Mean clTot"],
            marker="o",
            markersize=4,
            linestyle="-",
            label=f"{pixels[0]} Pixels",
        )
    # if len(FilePaths) == 1:
    #     ax[0].errorbar(
    #         df["Mean Charge Calibrated"],
    #         df["Mean clTot"],
    #         xerr=df["Std Charge Calibrated"],
    #         fmt="o",
    #         markersize=4,
    #         linestyle="-",
    #         label="Manual Calibration",
    #     )

    # Set labels and title
    ax[0].set_xlabel("Injected Charge [ke]")
    ax[0].set_ylabel("ToT [25ns]")
    ax[0].set_title("Test Pulse Calibration clToT vs clCharge")

    ax[0].set_xlim(0, 200)
    ax[0].set_ylim(0, 2000)

    # ax[0].set_xlim(0, 20)
    # ax[0].set_ylim(0, 200)
    # ax[0].set_xticks(range(0, 21, 2))
    # ax[0].set_yticks(range(0, 201, 20))
    ax[0].legend()
    ax[0].grid()

    ax[1].set_xlabel("Injected Charge [ke]")
    ax[1].set_ylabel("ToT [25ns]")
    ax[1].set_title("Laser Calibration clToT vs clCharge")

    ax[1].set_xlim(0, 200)
    ax[1].set_ylim(0, 2000)

    # ax[1].set_xlim(0, 20)
    # ax[1].set_ylim(0, 200)
    # ax[1].set_xticks(range(0, 21, 2))
    # ax[1].set_yticks(range(0, 201, 20))
    ax[1].legend()
    ax[1].grid()

    plt.tight_layout()
    plt.savefig("ToT_Charge.png", dpi=600)
    plt.show()
