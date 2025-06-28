import pandas as pd
import numpy as np

def RefactoredDistribution(filepath: str) -> None:
    df = pd.read_csv(filepath)
    scaling_df = pd.read_csv('scaling_factors.csv')
    df = df.merge(scaling_df, on=['col', 'row'], how='left')
    df['Charge'] = df['Charge'] * df['scalingfactor']
    df = df.drop(columns=['scalingfactor'])
    df.to_csv('scaled_raw_data.csv', index=False)
    