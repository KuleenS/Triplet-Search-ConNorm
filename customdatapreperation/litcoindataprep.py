# %%
import pandas as pd

# %%
DISEASE = True
CHEMICAL = True

#load the train and test for training data 
entities_train = pd.read_csv('../data/LITCOIN/entities_train.csv', sep='\t')
entities_test = pd.read_csv('../data/LITCOIN/entities_test.csv', sep='\t')

# %%
import os
#create the DILBERT prepared folders
os.makedirs('../data/LITCOINDILBERTPREPARED/train/', exist_ok=True)
os.makedirs('../data/LITCOINDILBERTPREPARED/test/', exist_ok=True)

# %%

#get all the disease or chemical from entities train and put them into dilbert training data
with open(f'../data/LITCOINTRIPLETPREPARED/train.tsv', 'w') as f:
    for abstract_id in entities_train.abstract_id.unique():
        temp_df = entities_train[entities_train.abstract_id == abstract_id]
        for i,v in temp_df.iterrows():
            if DISEASE and v['type']=='DiseaseOrPhenotypicFeature':
                entity_id = v['entity_ids'].replace("OMIM", "")
                f.write(f"{v['mention']}\t{entity_id}\n")
            elif CHEMICAL and v['type']=='ChemicalEntity':
                entity_id = v['entity_ids'].replace("OMIM", "")
                f.write(f"{v['mention']}\t{entity_id}\n")


#get all the disease or chemical from entities train and put them into dilbert testing data
with open(f'../data/LITCOINTRIPLETPREPARED/test.tsv', 'w') as f:
    for abstract_id in entities_test.abstract_id.unique():
        temp_df = entities_test[entities_test.abstract_id == abstract_id]
        for i,v in temp_df.iterrows():
            if DISEASE and v['type']=='DiseaseOrPhenotypicFeature':
                entity_id = v['entity_ids'].replace("OMIM", "")
                f.write(f"{v['mention']}\t{entity_id}\n")
            elif CHEMICAL and v['type']=='ChemicalEntity':
                entity_id = v['entity_ids'].replace("OMIM", "")
                f.write(f"{v['mention']}\t{entity_id}\n")

# %%



