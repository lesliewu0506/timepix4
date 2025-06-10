from timepix4.focus import *


def main():
    # focus = FocusProcessor(AttenuationVoltage=3.5, direction="z")
    # focus.ProcessAll()
    plotter = ScanPlotter(direction="y", AttenuationVoltage=3.5, ROW=230, COL=228)
    plotter.Plot_ToT()
    plotter.Plot_Charge()
    # visualizer = HitmapVisualizer(
    #     "Data/Focus/Z/ZFocus 3.5 V/focus_39p500/N116-250502-152529.root"
    # )
    # visualizer.CreateHitmap()
    # FitBeamSize("Data/Focus/Y/ProcessedFocus 3.5 V/Results.csv")


if __name__ == "__main__":
    main()
