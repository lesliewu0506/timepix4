from timepix4.focus import FocusProcessor, ScanPlotter, HitmapVisualizer


def main():
    # focus = FocusProcessor(AttenuationVoltage=3.5, direction="y")
    # focus.ProcessAll()
    plotter = ScanPlotter(direction="y", AttenuationVoltage=3.5, ROW=230, COL=228)
    plotter.Plot_ToT()
    # plotter.Plot_Charge()
    # visualizer = HitmapVisualizer(
    #     "Data/Focus/Z/ZFocus 3.5 V/focus_39p500/N116-250502-152529.root"
    # )
    # visualizer.CreateHitmap()


if __name__ == "__main__":
    main()
