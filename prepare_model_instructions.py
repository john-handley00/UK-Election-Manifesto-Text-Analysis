import pandas as pd
from functools import reduce
import openai
import json

with open("APIkey.txt") as f:
    openai.api_key = f.read().strip()

# Load manifesto
manifesto = pd.read_csv('manifestos/51320_201912.csv')
# Filter header and non-content lines
manifesto = manifesto[(manifesto['cmp_code']!='H') & (~manifesto['cmp_code'].isna())]

# Get list of all sentence fragments
sentence_fragments = manifesto['text'].tolist()

# Join sentence fragments into complete sentences
def join_sentences(left, right):
    if left and left[-1][-1] not in ['.', '?', '!']:
        left[-1] = left[-1] + ' ' + right
    else:
        left.append(right)
    return left

sentences = reduce(join_sentences,sentence_fragments,[])

# Create rolling window of 3 sentences, with a target sentence wrapped in asterisks
first_entry = ['*' + sentences[0] + '*'] + sentences[1:3]
last_entry = sentences[-2:] + ['*' + sentences[len(sentences)-1] + '*']

rolling_window = [first_entry] + [[sentences[i-1],'*' + sentences[i] + '*',sentences[i+1]] for i in range(1,len(sentences)-1)] + [last_entry]
inputs = [' '.join(sentences) for sentences in rolling_window]


# Load instructions from text file
with open('instructions.txt','r') as f:
    instructions = f.read()


api_params = [{'model':'gpt-3.5-turbo',
               'max_tokens': 20,
               'messages': [{'role':'system','content':instructions},
                            {'role':'user','content':text}]} for text in inputs]


with open('api_inputs/api_params.jsonl','w') as f:
    for item in api_params:
        f.write(json.dumps(item) + "\n")