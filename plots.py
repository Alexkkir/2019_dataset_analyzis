import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# TABLE = 'results_ssim_subj.csv'
# TABLE = 'results_vmaf_l2_subj.csv'
TABLE = 'final_results/merged.csv'

df_orig = pd.read_csv(TABLE)
names = sorted([*{*df_orig['Name']}])

for metric in ['psnr', 'ssim', 'vmaf', 'niqe']:
    fig, ax = plt.subplots(figsize=(8, 7))
    ro_total = {True: 0, False: 0}

    for mask in [False, True]:
        for name in names:
            df = df_orig[(df_orig['Name'] == name) & (df_orig['Mask'] == mask) & (df_orig['Metric'] == metric)]

            met = np.array(df['Metric_val'])
            subj = np.array(df['Subjective'])
            r = np.corrcoef(met, subj)[0][1]
            ro_total[mask] += r
            print(r)

            ax.scatter(subj, met, label=f'{name}_{mask}, PCC=%.3f' % (r))
        ro_total[mask] /= len(names)
        ax.set_title(f'metric={metric}, mask={mask}, PCC=%.3f' % (ro_total[mask]))
        ax.set_xlabel('Subjective')
        ax.set_ylabel('Metric')
        ax.legend(loc='lower right')
        fig.show()

        fig.savefig(f'final_results/metric={metric}_mask={mask}.jpg')

        xlims, ylims = ax.get_xlim(), ax.get_ylim()
        ax.clear()
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
    print(False, ro_total[False])
    print(True, ro_total[True])
