import pandas as pd
import matplotlib.pyplot as plt

def CreateDataframe(filepath):
    df = pd.read_csv(f"Voltage Scans/{filepath}.txt", sep=' ', header=None)

    df.columns = ['Voltage', 'Current', 'Std']
    df['Current'] = df['Current'] * (-10 ** 6)
    
    return df

def PlotIV(filepath: str):
    FileName = filepath.split('_')[0]
    df = CreateDataframe(filepath)
    # Plot Current vs Voltage
    plt.figure()
    plt.plot(df['Voltage'], df['Current'], marker='o', markersize = 5)
    plt.xlabel('Voltage [V]')
    plt.ylim(0, 2)
    plt.ylabel('Current [$\mu$A]')
    plt.gca().invert_xaxis()
    plt.title(f'I-V Curve N10 with Tape')
    plt.tight_layout()
    
    plt.savefig(f'IV_curve_N10_with_Tape.png', dpi=600)
    plt.show()

if __name__ == "__main__":
    # files = [f"{pre}N10_voltage_scan.txt", f"{pre}N116_voltage_scan.txt"]
    files = ["N10_voltage_scan_Tape"]
    for file in files:
        PlotIV(file)