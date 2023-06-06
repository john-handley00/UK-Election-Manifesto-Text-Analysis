import pandas as pd
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/manifestos.csv',parse_dates=['edate'])
df.loc[df['partyname']=='Liberal Party','partyname'] = 'Liberal Democrats'

docs = [TaggedDocument(words=simple_preprocess(row['text']),tags=[row['manifesto'],str(row['edate'])]) for _, row in df.iterrows()]

model = Doc2Vec(docs,
                vector_size=300,
                hs=1,
                negative=0,
                epochs=400,
                min_count=50,
                window=15,
                dm=0,
                dbow_words=1)

embeddings = model.dv[df['manifesto']]

pca = PCA(n_components=2)
df[['dim1','dim2']] = pca.fit_transform(embeddings)

party_palette = {'Conservative Party': '#0087DC',
                 'Labour Party': '#E4003B',
                 'Liberal Democrats': '#FAA61A'}

fig, axs = plt.subplots(ncols=3,figsize=(16,5))
fig.subplots_adjust(hspace=0.2, wspace=0.2)

sns.scatterplot(data=df,x='dim1',y='dim2',hue='partyname',palette=party_palette,ax=axs[0])
axs[0].set_title('PCA scatter plot')

sns.lineplot(data=df,x='edate',y='dim1',hue='partyname',palette=party_palette,ax=axs[1])
axs[1].set_title('PC1 over time')

sns.lineplot(data=df,x='edate',y='dim2',hue='partyname',palette=party_palette,ax=axs[2])
axs[2].set_title('PC2 over time')

axs[0].legend([],[], frameon=False)
axs[1].legend([],[], frameon=False)
sns.move_legend(axs[2],loc='upper left',bbox_to_anchor=(1,1))