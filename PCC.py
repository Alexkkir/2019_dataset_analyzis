import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

data = pd.read_csv('final_results/merged.csv')
names = sorted([*{*data['Name']}])[:]
metrics = ['psnr', 'ssim', 'vmaf', 'niqe']

tables_str = {metric: dict() for metric in metrics}
tables_val = {metric: {False: [], True: []} for metric in metrics}


for metric in metrics:
    for name in names:
        tables_str[metric][name] = dict()
        for mask in [False, True]:
            vid = data[(data['Name'] == name) & (data['Mask'] == mask) & (data['Metric'] == metric)][['Subjective', 'Metric_val']]
            vid = np.array(vid)
        
            rho = np.corrcoef(vid.T)
            rho = rho[0][1]
            tables_val[metric][mask].append(rho)
            tables_str[metric][name][f'Mask={mask}'] = round(rho, 3)

means = {met: {f'Mask={mask}': round(np.mean(c), 3) for mask, c in by_mask.items()} for met, by_mask in
         tables_val.items()}

with open('final_results/PCC.txt', 'w') as f:
    sys.stdout = f
    print(pd.DataFrame(means))
    print()
    print()

    for m, df in tables_str.items():
        print(f'Metric={m}:')
        print(pd.DataFrame(df).to_string())
        print()
        print()
