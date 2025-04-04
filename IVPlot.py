import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def CreateDataframe(filepath):
    # Read the file, no header, space-separated, and each row becomes a row in the DataFrame
    df = pd.read_csv(filepath, sep=' ', header=None)
    
    # Rename the columns to appropriate labels
    df.columns = ['Voltage', 'Current', 'Std']
    df['Current'] = df['Current'] * (-10 ** 6)
    
    return df

def PlotIV(filepath: str):
    # Extract the file name without extension
    FileName = filepath.split('_')[0]
    df = CreateDataframe(filepath)
    # Plot Current vs Voltage
    plt.figure()
    plt.plot(df['Voltage'], df['Current'], marker='o', markersize = 5)
    plt.xlabel('Voltage [V]')
    plt.ylim(0, 10)
    plt.ylabel('Current [$\mu$A]')
    plt.gca().invert_xaxis()
    plt.title(f'I-V Curve {FileName}')
    plt.tight_layout()
    
    plt.savefig(f'IV_curve_{FileName}.png', dpi=600)
    plt.show()

if __name__ == "__main__":
    files = ["N10_voltage_scan.txt", "N116_voltage_scan.txt"]
    for file in files:
        PlotIV(file)