import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import seaborn as sns
from umap import UMAP

# Load manifesto sentences
df = pd.read_csv('data/manifestos.csv',parse_dates=['edate'])
df.loc[df['partyname']=='Liberal Party','partyname'] = 'Liberal Democrats'
df['sentence'] = df['text'].str.split('\. ')
df = df.explode('sentence')
df.pop('text')
df = df.reset_index(drop=True)

# Load embedding model
model = SentenceTransformer('all-distilroberta-v1')
embeddings = model.encode(df['sentence'].tolist(),
                          show_progress_bar=True,
                          convert_to_numpy=True)


umap = UMAP(n_components=2,metric='cosine')
dims = umap.fit_transform(embeddings,df['partyname'].map({'Labour Party': 0, 'Conservative Party': 1, 'Liberal Democrats': 2}))

df[['dim1','dim2']] = dims