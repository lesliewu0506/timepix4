import pandas as pd
import matplotlib.pyplot as plt

def PowerVoltagePlot(filepath: str) -> None:
    df = pd.read_csv(filepath)
    plt.figure(figsize=(12, 8))
    plt.plot(df["V"], df["power"], linestyle="-", marker="o", color="blue", label="Power")

    plt.xlabel("Attenuation Voltage [V]")
    plt.ylabel("Power [$\mu$W]")
    plt.title("Power vs Voltage")
    plt.grid()
    plt.tight_layout()
    plt.savefig("PowerVsVoltage.png")
    plt.show()