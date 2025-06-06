import pandas as pd
import matplotlib.pyplot as plt


def PlotCompare(filepath):
    vlines = [
        {"x": 2.225, "color": "red", "label": "8.01 keV"},
        {"x": 3.861, "color": "green", "label": "13.9 keV"},
        {"x": 4.917, "color": "blue", "label": "17.7 keV"},
        {"x": 5.75, "color": "magenta", "label": "20.7 keV"},
        {"x": 7.306, "color": "cyan", "label": "26.3 keV"},
        {"x": 16.5, "color": "orange", "label": "59.5 keV"},
    ]

    filename = filepath.split("-")[0]
    df = pd.read_csv(f"Data/4Sector Data/{filepath}-Charge4Sector.csv")
    df = df[["Top Left", "Top Right", "Bottom Left", "Bottom Right"]]
    # Combine all values into one array
    # all_values = df.values.flatten()

    # # Create a single histogram
    # plt.figure(figsize=(10, 6))
    # plt.hist(all_values, bins=1600, alpha=0.6, color="blue", label="Raw Charge")
    # plt.hist(
    #     all_values * 1.1424,
    #     bins=1600,
    #     alpha=0.6,
    #     color="orange",
    #     label="Corrected Charge (Factor = 1.1424)",
    # )
    # plt.xlim(0, 20)
    # plt.xlabel("Charge [ke]")
    # plt.ylabel("Counts")
    # for line in vlines:
    #     plt.axvline(
    #         x=line["x"], color=line["color"], linestyle="--", label=line["label"]
    #     )
    # plt.legend(loc="best")
    # plt.title(f"{filename} Combined Charge Distribution (All Sectors)")
    # plt.tight_layout()
    # plt.savefig(f"{filename}_Combined_Charge_Distribution.png", dpi=600)
    # plt.show()
    # # Create histogram and get axes
    # axarr = df.hist(layout=(2, 2), bins=1600, alpha=0.5, figsize=(20, 20), grid=False)

    # axes = axarr.flatten()

    # for ax, column in zip(axes, df.columns):
    #     for line in vlines:
    #         ax.axvline(
    #             x=line["x"], color=line["color"], linestyle="--", label=line["label"]
    #         )

    #     # Add legend with the column name + vline labels
    #     ax.legend(loc="best")
    #     ax.set_xlim(0, 20)
    #     ax.set_xlabel("Charge [ke]")
    #     ax.set_ylabel("Counts")
    #     ax.set_title(f"{column}")

    # plt.suptitle(f"{filename} ToT Distribution Per Sector", fontsize=16)
    # # plt.tight_layout(rect=[0, 0, 1, 0.96])
    # plt.tight_layout()
    # plt.savefig(f"{filename}_Charge_Distribution_4Sector.png", dpi=600)
    # plt.show()

    # Create a single plot for all histograms with distinct colors
    fig, ax = plt.subplots(figsize=(14, 6))
    # Define a list of distinct colors for each sector
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

    # Plot each sector histogram on the same axes with a specific color
    for idx, column in enumerate(df.columns):
        ax.hist(df[column], bins=1600, alpha=0.5, color=colors[idx], label=column)

    # Draw the vertical lines for each energy reference
    for line in vlines:
        ax.axvline(
            x=line["x"], color=line["color"], linestyle="--", label=line["label"]
        )

    ax.set_xlim(0, 20)
    ax.set_xlabel("Charge [ke]")
    ax.set_ylabel("Counts")
    ax.set_title(f"{filename} Charge Distribution by Sectors")
    ax.legend(loc="best")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{filename}_Combined_Charge_Distribution.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    # filepath1 = ["N10-250404-143700", "N116-250403-150114"]
    # filepath2 = ["N112-250411-101613", "N113-250408-100406"]
    filepaths = ["N10-250409-113326", "N116-250408-123554"]
    for filepath in filepaths:
        PlotCompare(filepath)
