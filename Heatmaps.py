from timepix4.heatmap import *


def main():
    # filepath = "Data/Filtered Calibration Data/N116-250403-150114-Charge-Data.csv"
    # # PlotAvgToTHeatmap(filepath)
    # filefit = "Data/Test Pulse Data/N116-TestPulseResults.csv"
    # PlotAvgToTAndFitHeatmaps(filepath, filefit)
    # VisualizeToT("Data/Laser Measurements/High/Laser Measurements x (228, 230)/3_500.root")
    # VisualizeToT_single("Data/Laser Measurements/Laser Measurements 4/3_500.root")
    SourceHitMap("Data/Filtered Calibration Data/N116-250408-123554-Filtered.csv")


if __name__ == "__main__":
    main()
