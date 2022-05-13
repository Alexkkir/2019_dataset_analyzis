import pandas as pd

dirr = 'ugc_results'
df1 = pd.read_csv(f'{dirr}/corr_by_video_pearson.csv')
df2 = pd.read_csv(f'{dirr}/corr_by_video_spearman.csv')
df = pd.merge(df1, df2, on=['Metric', 'Mask', 'Sequence'])
df.to_csv(f'{dirr}/corr_by_video.csv', index=False)
df.to_excel(f'{dirr}/corr_by_video.xlsx')


df1 = pd.read_csv(f'{dirr}/corr_by_metric_pearson.csv')
df2 = pd.read_csv(f'{dirr}/corr_by_metric_spearman.csv')
df = pd.merge(df1, df2, on=['Metric', 'Mask'])
df.to_csv(f'{dirr}/corr_by_metric.csv', index=False)
df.to_excel(f'{dirr}/corr_by_metric.xlsx')
