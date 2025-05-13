import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def LaserToTPlotter(file1, file2, file3) -> None:
    lookuptable = pd.read_csv(f"1lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    fig, ax = plt.subplots(figsize=(12, 8))
    df = pd.read_csv(file1)
    # plt.errorbar(
    #     df["Mean clCharge"],
    #     df["Mean clTot"],
    #     xerr=df["Std clCharge"],
    #     fmt="o",
    #     markersize=4,
    #     linestyle="-",
    #     label="Test Pulse Calibration",
    # )

    # plt.errorbar(
    #     df["Mean Charge Calibrated"],
    #     df["Mean clTot"],
    #     xerr=df["Std Charge Calibrated"],
    #     fmt="o",
    #     markersize=4,
    #     linestyle="-",
    #     label="Manual Calibration",
    # )

    plt.plot(
        lookuptable["Charge"],
        df["Mean clTot"],
        marker="o",
        markersize=4,
        linestyle="-",
        label="Laser Calibration",
    )

    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    lut = []
    ori = []
    div2 = []
    div4 = []

    for V in np.arange(3.05, 4.01, 0.025):
        V = V.round(3)
        lutfiltered = lookuptable[lookuptable["voltage"] == V]
        df1_filtered = df[df["AttenuationVoltage"] == V]
        df2_filtered = df2[df2["AttenuationVoltage"] == V]
        df3_filtered = df3[df3["AttenuationVoltage"] == V]
        if lutfiltered.empty or df1_filtered.empty or df2_filtered.empty or df3_filtered.empty:
            continue
        lut.append(lutfiltered["Charge"].iloc[0])
        ori.append(df1_filtered["Mean clTot"].iloc[0])
        div2.append(df2_filtered["Mean clTot"].iloc[0])
        div4.append(df3_filtered["Mean clTot"].iloc[0])
    plt.plot(
        lut, ori, "o", markersize=4, label="Original Charge Calibration"
        )
    plt.plot(
        np.array(lut) / 2, np.array(div2) / 2, "o", markersize=4, label="Laser Calibration / 2"
        )
    plt.plot(
        np.array(lut) / 4, np.array(div4) / 4, "o", markersize=4, label="Laser Calibration / 4"
        )

    # V = 3.3
    # lutfiltered = lookuptable[lookuptable["voltage"] == V]
    # df1 = df[df["AttenuationVoltage"] == V]
    # df2 = pd.read_csv(file2)
    # df2 = df2[df2["AttenuationVoltage"] == V]
    # df3 = pd.read_csv(file3)
    # df3 = df3[df3["AttenuationVoltage"] == V]
    # plt.plot(
    #     lutfiltered["Charge"] / 1, df1["Mean clTot"], "o", markersize=4, label="Point 1"
    # )

    # plt.plot(
    #     lutfiltered["Charge"] / 2, df2["Mean clTot"] / 2, "o", markersize=4, label="Point 2"
    # )

    # plt.plot(
    #     lutfiltered["Charge"] / 4, df3["Mean clTot"] / 4, "o", markersize=4, label="Point 4"
    # )

    plt.xlabel("Injected Charge [ke]")
    plt.ylabel("ToT [25ns]")
    plt.xlim(0, 200)
    plt.ylim(0, 2000)
    plt.title("ToT vs Charge")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("ToT_Charge_2.png", dpi=600)
    plt.show()


def ToTChargePlotter(FilePaths: list[str]) -> None:
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    lookuptable = pd.read_csv(f"1lookup_table.csv")
    lookuptable = lookuptable.sort_values("voltage", ascending=True)
    lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
    for FilePath in FilePaths:
        pixels = FilePath.split("/")[-1].split(".")[0]
        df = pd.read_csv(FilePath)
        df["Mean Tot"] = df["Mean Tot"] / int(FilePath.split("/")[-1][0])
        ax[0].errorbar(
            df["Mean clCharge"],
            df["Mean Tot"],
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

        ax[1].plot(
            lut["Charge"],
            df["Mean Tot"],
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
    ax[1].set_title("Laser Calibration ToT vs clCharge")

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


# def ToTChargePlotter(FilePaths: list[str]) -> None:
#     fig, ax = plt.subplots(1, 2, figsize=(16, 8))
#     lookuptable = pd.read_csv(f"1lookup_table.csv")
#     lookuptable = lookuptable.sort_values("voltage", ascending=True)
#     lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
#     for FilePath in FilePaths:
#         pixels = FilePath.split("/")[-1].split(".")[0]
#         df = pd.read_csv(FilePath)
#         # if pixels[0] == "1":
#         #     lookuptable = pd.read_csv(f"{pixels[0]}lookup_table.csv")
#         #     lookuptable = lookuptable.sort_values("voltage", ascending=True)
#         #     lookuptable["Charge"] = lookuptable["relative_factor"].apply(lambda x: x * 16.5)
#         df["Mean clTot"] = df["Mean clTot"] / int(FilePath.split("/")[-1][0])
#         ax[0].errorbar(
#             df["Mean clCharge"],
#             df["Mean clTot"],
#             xerr=df["Std clCharge"],
#             fmt="o",
#             markersize=4,
#             linestyle="-",
#             label=f"{pixels[0]} Pixels",
#         )

#         if len(df) < len(lookuptable):
#             lut = lookuptable.iloc[: len(df)]
#         else:
#             lut = lookuptable

#         # if pixels[0] == "1":
#         #     ax[0].plot(
#         #         lut["Charge"],
#         #         df["Mean clTot"],
#         #         marker="o",
#         #         markersize=4,
#         #         linestyle="-",
#         #         label="Laser Calibration",
#         #     )
#         # else:
#         ax[1].plot(
#             lut["Charge"],
#             df["Mean clTot"],
#             marker="o",
#             markersize=4,
#             linestyle="-",
#             label=f"{pixels[0]} Pixels",
#         )
#     # if len(FilePaths) == 1:
#     #     ax[0].errorbar(
#     #         df["Mean Charge Calibrated"],
#     #         df["Mean clTot"],
#     #         xerr=df["Std Charge Calibrated"],
#     #         fmt="o",
#     #         markersize=4,
#     #         linestyle="-",
#     #         label="Manual Calibration",
#     #     )

#     # Set labels and title
#     ax[0].set_xlabel("Injected Charge [ke]")
#     ax[0].set_ylabel("ToT [25ns]")
#     ax[0].set_title("Test Pulse Calibration clToT vs clCharge")

#     ax[0].set_xlim(0, 200)
#     ax[0].set_ylim(0, 2000)

#     # ax[0].set_xlim(0, 20)
#     # ax[0].set_ylim(0, 200)
#     # ax[0].set_xticks(range(0, 21, 2))
#     # ax[0].set_yticks(range(0, 201, 20))
#     ax[0].legend()
#     ax[0].grid()

#     ax[1].set_xlabel("Injected Charge [ke]")
#     ax[1].set_ylabel("ToT [25ns]")
#     ax[1].set_title("Laser Calibration clToT vs clCharge")

#     ax[1].set_xlim(0, 200)
#     ax[1].set_ylim(0, 2000)

#     # ax[1].set_xlim(0, 20)
#     # ax[1].set_ylim(0, 200)
#     # ax[1].set_xticks(range(0, 21, 2))
#     # ax[1].set_yticks(range(0, 201, 20))
#     ax[1].legend()
#     ax[1].grid()

#     plt.tight_layout()
#     plt.savefig("ToT_Charge.png", dpi=600)
#     plt.show()
