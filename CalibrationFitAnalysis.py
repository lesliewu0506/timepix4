import pandas as pd
import matplotlib.pyplot as plt

def CreateDataframe(filepath):
    df = pd.read_csv(filepath, delim_whitespace=True, header = None, skiprows = 15)
    df.columns = ["Col", "Row", "p0", "p1", "p2", "p3", "p0_err", "p1_err", "p2_err", "p3_err", "red_chi2", "valid"]
    return df

# def PlotDataTogether(filepath1, filepath2):
#     FileName1 = filepath1.split('_')[0]
#     df1 = CreateDataframe(filepath1)
    
#     FileName2 = filepath2.split('_')[0]
#     df2 = CreateDataframe(filepath2)

#     fig, axs = plt.subplots(2, 2, figsize=(14, 12), sharex=False)

#     for i, param in enumerate(['p0', 'p1', 'p2', 'p3']):
#         row = i // 2
#         col = i % 2
#         data1 = df1[param]
#         data2 = df2[param]
#         axs[row, col].hist(data1, bins=50, alpha=0.5, label=f'{FileName1} - {param}')
#         axs[row, col].hist(data2, bins=50, alpha=0.5, label=f'{FileName2} - {param}')
#         axs[row, col].set_title(f'{param} Comparison')
#         axs[row, col].legend()
#         axs[row, col].set_xlim(min(data1.min(), data2.min()), max(data1.max(), data2.max()))

#     axs[0, 0].set_ylabel('Frequency')
#     axs[1, 0].set_ylabel('Frequency')
#     axs[1, 0].set_xlabel('p2 Value')
#     axs[1, 1].set_xlabel('p3 Value')

#     plt.tight_layout()
#     plt.savefig(f'Histogram of p0-p3 Values {FileName1}_{FileName2}.png', dpi=600)
#     plt.show()

def PlotData(filepath1, filepath2):
    FileName1 = filepath1.split('_')[0]
    df1 = CreateDataframe(filepath1)
    df1["p2"] = df1["p2"] / (10**6)

    FileName2 = filepath2.split('_')[0]
    df2 = CreateDataframe(filepath2)
    df2["p2"] = df2["p2"] / (10**6)

    fig, axs = plt.subplots(2, 1, figsize=(8, 10), sharex=True)

    axs[0].hist(df1['p0'], bins=100, alpha=0.5, label='p0')
    # axs[0].set_xlim(-5, 10)
    axs[0].set_ylabel('Frequency')
    axs[0].set_title(f'Histogram of p0 Values {FileName1}')

    axs[1].hist(df2['p0'], bins=100, alpha=0.5, label='p0')
    # axs[1].set_xlim(-5, 10)
    axs[1].set_xlabel('p0 Value')
    axs[1].set_ylabel('Frequency')
    axs[1].set_title(f'Histogram of p0 Values {FileName2}')

    plt.tight_layout()
    plt.savefig(f'Histogram of p0 Values {FileName1}_{FileName2}.png', dpi=600)
    plt.show()
    return 

if __name__ == "__main__":
    PlotData("N10_charge.txt", "N116_charge.txt")