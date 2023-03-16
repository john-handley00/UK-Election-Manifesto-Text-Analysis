import json
import pandas as pd

with open('api_inputs/api_params_results.jsonl','r') as json_file:
    json_list = list(json_file)


prompts = [json.loads(item)[0]['messages'][1]['content'] for item in json_list]
results = [json.loads(item)[1]['choices'][0]['message']['content'] for item in json_list]

social_policy = [1 if 'social policy' in result.lower() else 0 for result in results]
econ_policy = [1 if 'economic policy' in result.lower() else 0 for result in results]
left = [1 if 'left' in result.lower() or 'liberal' in result.lower() else 0 for result in results]
right = [1 if 'right' in result.lower() or 'conservative' in result.lower() else 0 for result in results]

data = pd.DataFrame({'Social': social_policy,
                     'Economic': econ_policy,
                     'Left': left,
                     'Right': right,
                     'Prompt': prompts})

data['Left_only'] = (data['Left']==1) & (data['Right']==0)
data['Left_only'] = data['Left_only'].map({True:1,False:0})

data['Right_only'] = (data['Right']==1) & (data['Left']==0)
data['Right_only'] = data['Right_only'].map({True:1,False:0})

data['Centre'] = 1 - data['Right_only'] - data['Left_only']

data['Policy'] = 'Other'
data.loc[(data['Economic']==1)&(data['Social']==0),'Policy'] = 'Economic'
data.loc[(data['Economic']==0)&(data['Social']==1),'Policy'] = 'Social'

data['Position'] = 'Neither'
data.loc[data['Left_only']==1,'Position'] = 'Left/liberal'
data.loc[data['Right_only']==1,'Position'] = 'Right/conservative'

data = data[['Prompt','Policy','Position']]