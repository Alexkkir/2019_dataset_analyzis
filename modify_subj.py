import pandas as pd


subj = pd.read_csv('subjective_scores.csv')
print(subj)
        
subj['video_name'] = subj.apply(lambda row: 
                                f'enc_res_{row.codec}_{row.preset}_{row.sequence}_{row.crf}' ,
                                axis=1)
print(subj.head(5).to_string())
print(subj)

subj.to_csv('subjective_scores.csv', index=False)