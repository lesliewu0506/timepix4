import pandas as pd
import matplotlib.pyplot as plt

def PlotCompare(filepath):
    vlines = [
        {"x": 2.225, "color": "red",    "label": "8.01 keV"},
        {"x": 3.861, "color": "green",  "label": "13.9 keV"},
        {"x": 4.917, "color": "blue",   "label": "17.7 keV"},
        {"x": 5.75,  "color": "magenta","label": "20.7 keV"},
        {"x": 7.306, "color": "cyan",   "label": "26.3 keV"},
        {"x": 16.5,  "color": "orange", "label": "59.5 keV"},
    ]

    filename = filepath.split("-")[0]
    df = pd.read_csv(f"Data/4Sector Data/{filepath}-Charge4Sector.csv")
    df = df[["Top Left", "Top Right", "Bottom Left", "Bottom Right"]]
    # Combine all values into one array
    all_values = df.values.flatten() * 1.1424

    # Create a single histogram
    plt.figure(figsize=(10, 6))
    plt.hist(all_values, bins=1600, alpha=0.6)
    plt.xlim(0, 20)
    plt.xlabel("Charge [ke]")
    plt.ylabel("Counts")
    for line in vlines:
        plt.axvline(x=line["x"], color=line["color"], linestyle='--', label=line["label"])
    plt.legend(loc = "best")
    plt.title(f"{filename} Corrected Combined Charge Distribution (All Sectors) (Factor 1.1424)")
    plt.tight_layout()
    plt.savefig(f"{filename}_Corrected_Combined_Charge_Distribution.png", dpi=600)
    plt.show()
    # # Create histogram and get axes
    # axarr = df.hist(layout=(2, 2), bins=1600, alpha=0.5, figsize=(20, 20), grid = False)

    # axes = axarr.flatten()
    
    # for ax, column in zip(axes, df.columns):
    #     for line in vlines:
    #         ax.axvline(x=line["x"], color=line["color"], linestyle='--', label=line["label"])
        
    #     # Add legend with the column name + vline labels
    #     ax.legend(loc = "best")
    #     ax.set_xlim(0, 20)
    #     ax.set_xlabel("Charge [ke]")
    #     ax.set_ylabel("Counts")
    #     ax.set_title(f"{column}")

    # plt.suptitle(f"{filename} ToT Distribution Per Sector", fontsize=16)
    # # plt.tight_layout(rect=[0, 0, 1, 0.96])
    # plt.savefig(f"{filename}_Charge_Distribution_4Sector.png", dpi=600)
    # plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    filepath = "N112-250411-101613"
    # filepath = "N116-250408-105332"
    PlotCompare(filepath)