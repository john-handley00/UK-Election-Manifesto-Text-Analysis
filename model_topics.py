import pandas as pd
from top2vec import Top2Vec
import time

# Load data
print('Loading data')
start = time.time()
manifestos = pd.read_csv('data/uk_manifestos.csv')
party_lookup = pd.read_csv('data/mpd_party_lookup.csv')
end = time.time()
print(f'Done in {end-start}s')


# Create party id to name dictionary
print('Creating party id: name dictionary')
start = time.time()
party_lookup = party_lookup[(party_lookup['countryname']=='United Kingdom') & (party_lookup['name'].isin(["Labour Party","Liberal Party","Social Democratic Party","Liberal Democrats","Conservative Party"]))]
party_lookup = pd.Series(party_lookup.name.values,index=party_lookup.party).to_dict()
end = time.time()
print(f'Done in {end-start}s')

# Clean data
print('Cleaning data')
start = time.time()

# Clean text
manifestos['text'] = manifestos['text'].str.lower()
manifestos['text'] = manifestos['text'].str.replace('\"','')

# Get party names
manifestos[['party','election']] = manifestos['id'].str.split('_',expand=True)
manifestos['party'] = manifestos['party'].astype('int')
manifestos['party'] = manifestos['party'].map(party_lookup)

# Drop NA rows
manifestos = manifestos.dropna(subset=['text'])

# Save to csv
manifestos.to_csv('data/manifestos_cleaned.csv')

end = time.time()
print(f'Done in {end-start}s')

# Fit top2vec model
print('Fitting Top2Vec model')
start = time.time()
model = Top2Vec(documents=manifestos['text'].tolist(),
                embedding_model='doc2vec')

model.save('data/manifesto_topic_model')
end = time.time()
print(f'Done in {end-start}s')