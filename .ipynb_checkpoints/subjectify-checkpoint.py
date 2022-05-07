import matplotlib.pyplot as plt
from time import time
import csv

from tqdm import tqdm
import pandas as pd

df = pd.read_csv('final_results/pp.csv')
subj = pd.read_csv('subjective_scores.csv')

result = pd.merge(df, subj, left_on = 'Distorted', right_on = 'Video_name')
result.to_csv('final_results/merged.csv', index=False)

