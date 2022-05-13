import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

MODE = ['pearson', 'spearman']
dirr = 'final_results'
data = pd.read_csv(f'{dirr}/merged.csv')
metrics = ['psnr', 'ssim', 'vmaf', 'niqe']
presets = sorted(set(data['Preset']))

def calc_corr(x, mode):
    return np.array(x.corr(mode))[0, 1]

tables_str = {metric: dict() for metric in metrics}
tables_val = {metric: {False: [], True: []} for metric in metrics}

corr = data.copy()
corr = corr.groupby(['Metric', 'Mask', 'Sequence', 'Preset'], group_keys=True)\
    .apply(lambda x : pd.Series(
        [calc_corr(x[['Metric_val', 'Subjective']], MODE[0]), calc_corr(x[['Metric_val', 'Subjective']], MODE[1]), len(x)], 
        index=[MODE[0], MODE[1], 'Sample_size']
))

def print_f(f):
    return '%.5f' % (f,)

def DescrStatsW(col, weights):
    total = weights.sum()
    col *= weights / total * len(col)
    return col

def weigh_func(col, weights, mode='mean'):
    st = DescrStatsW(col, weights=weights)
    return st.mean()

def average_rho(corrs: pd.Series, weights: pd.Series):
    corrs = pd.DataFrame(corrs)
    d = corrs.apply(lambda x: np.arctanh(x)).replace([np.inf, -np.inf], [np.arctanh(0.99), np.arctanh(-0.99)]) \
               .apply(lambda x: weigh_func(x, weights, 'mean')) \
               .apply(lambda x: np.tanh(x)).abs().replace([0.99], [1])
    return float(d)

corr_by_video = corr.groupby(['Metric', 'Sequence', 'Mask']).apply(lambda row : \
    pd.Series([
        print_f(average_rho(row[MODE[0]], row['Sample_size'])), 
        print_f(average_rho(row[MODE[1]], row['Sample_size']))], 
    index=[MODE[0].capitalize(), MODE[1].capitalize()]))
corr_by_metric = corr.groupby(['Metric', 'Mask']).apply(lambda row : \
    pd.Series([
        print_f(average_rho(row[MODE[0]], row['Sample_size'])), 
        print_f(average_rho(row[MODE[1]], row['Sample_size']))], 
    index=[MODE[0].capitalize(), MODE[1].capitalize()]))

print(corr_by_video)
print(corr_by_metric)

corr_by_video.to_excel(f'{dirr}/corr_by_video.xlsx')
corr_by_metric.to_excel(f'{dirr}/corr_by_metric.xlsx')

corr_by_video.reset_index().to_csv(f'{dirr}/corr_by_video.csv', index=False)
corr_by_metric.reset_index().to_csv(f'{dirr}/corr_by_metric.csv', index=False)
