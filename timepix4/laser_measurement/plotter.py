import pandas as pd
import matplotlib.pyplot as plt


def ToTChargePlotter(FilePaths: list[str]) -> None:
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))

    for FilePath in FilePaths:
        pixels = FilePath.split("/")[-1].split(".")[0]
        pixel = pixels.split("s")[-1]
        df = pd.read_csv(FilePath)

        lookuptable = pd.read_csv(f"{pixels[0]}lookup_table.csv")
        lookuptable = lookuptable.sort_values("voltage", ascending=True)
        lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)

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
    if len(FilePaths) == 1:
        ax[0].errorbar(
            df["Mean Charge Calibrated"],
            df["Mean clTot"],
            xerr=df["Std Charge Calibrated"],
            fmt="o",
            markersize=4,
            linestyle="-",
            label="Manual Calibration",
        )

    # Set labels and title
    ax[0].set_xlabel("Charge [ke]")
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

    ax[1].set_xlabel("Charge [ke]")
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
