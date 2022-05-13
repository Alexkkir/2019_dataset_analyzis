import pandas as pd


subj = pd.read_csv('subjective_scores_ugc.csv', sep=';')
print(subj)
        
subj['video_name'] = subj.apply(lambda row: 
                                f'enc_res_{row.codec}_{row.preset}_{row.sequence}_{row.crf}' ,
                                axis=1)
subj.columns = [x.replace(' ', '_').capitalize() for x in subj.columns]

print(subj.head(5).to_string())
print(subj)

subj.to_csv('subjective_scores_ugc.csv', index=False)