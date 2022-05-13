import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# TABLE = 'results_ssim_subj.csv'
# TABLE = 'results_vmaf_l2_subj.csv'
corr = 'Pearson'
dirr = 'ugc_results'
data = pd.read_csv(f'{dirr}/merged.csv')
by_seq = pd.read_csv(f'{dirr}/corr_by_video.csv')
by_metr = pd.read_csv(f'{dirr}/corr_by_metric.csv')

names = sorted(set(data['Sequence']))

for metric in ['psnr', 'ssim', 'vmaf', 'niqe']:
    fig, ax = plt.subplots(figsize=(8, 7))

    for mask in [False, True]:
        for name in names:
            df = data[(data['Sequence'] == name) & (data['Mask'] == mask) & (data['Metric'] == metric)]

            met = np.array(df['Metric_val'])
            subj = np.array(df['Subjective'])
            r = float(by_seq[(by_seq['Sequence'] == name) & (by_seq['Mask'] == mask) & (by_seq['Metric'] == metric)][corr])

            ax.scatter(subj, met, label=f'{name}_{mask}, PCC=%.3f' % (r))
        ro_total = float(by_metr[(by_metr['Mask'] == mask) & (by_metr['Metric'] == metric)][corr])
        ax.set_title(f'metric={metric}, mask={mask}, PCC=%.3f' % (ro_total))
        ax.set_xlabel('Subjective')
        ax.set_ylabel('Metric')
        ax.legend(loc='lower right')
        fig.show()

        fig.savefig(f'{dirr}/metric={metric}_mask={mask}.jpg')

        xlims, ylims = ax.get_xlim(), ax.get_ylim()
        ax.clear()
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
