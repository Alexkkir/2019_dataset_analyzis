import pandas as pd

df = pd.read_csv('final_results/raw.csv')

# df['Name'] = df['Distorted'].apply(lambda x : (m := x.split('/')[3], m.replace('_x265', ''))[-1])
df['Reference'] = df['Reference'].apply(lambda x : str(x).split('/')[-1])
df['Distorted'] = df['Distorted'].apply(lambda x : str(x).split('/')[-1].split('.')[0])

df.to_csv('final_results/pp.csv', index=False)