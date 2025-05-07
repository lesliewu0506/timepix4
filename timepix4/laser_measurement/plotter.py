import pandas as pd
import matplotlib.pyplot as plt

def ToTChargePlotter(FilePath: str) -> None:
    df = pd.read_csv(FilePath)
    fig, ax = plt.subplots(figsize=(12, 8))

   
    plt.plot(df["Mean Charge"] / 1000, df["Mean Tot"], marker="o", linestyle="--", color="b", label="ToT vs Charge")
    # Set labels and title
    ax.set_xlabel("Charge [ke]")
    ax.set_ylabel("ToT [25ns]")
    ax.set_title("ToT vs Charge")
    ax.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
