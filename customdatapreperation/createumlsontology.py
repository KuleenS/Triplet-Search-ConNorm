# %%
import mysql.connector
import pandas as pd

# %%
#get all the AUIS associated with items in MSH and OMIM
query = ("SELECT DISTINCT MRREL.AUI2, MRREL.AUI1, MRREL.REL, SAB FROM MRREL WHERE (REL = 'PAR' or REL='CHD') and (SAB LIKE '%MSH%' OR SAB LIKE '%OMIM%')")

conn = mysql.connector.connect(user='', password='', database='', host='')
cursor = conn.cursor()

# %%
cursor.execute(query)

# %%
total_relations_umls = []
for x in cursor:
    total_relations_umls.append(x)

# %%
df = pd.DataFrame(total_relations_umls, columns =['FirstAUI', 'SecondAUI', 'REL','SAB'])

# %%

#get all the sabs and AUIS to join with the first dataframe in order to get MSH and OMIM specific codes
query2 = ("SELECT AUI, SAB, CODE, STR FROM MRCONSO WHERE (SAB LIKE '%MSH%' OR SAB LIKE '%OMIM%')")

# %%
cursor.execute(query2)

# %%
names_of_CUIS = []
for x in cursor:
    names_of_CUIS.append(x)

# %%
df2 = pd.DataFrame(names_of_CUIS, columns =['AUI', 'SAB', 'CODE','STR'])

#remove U and Q rows as these are not in LITCOIN
df2 = df2[(~df2.CODE.str.contains('U'))& (~df2.CODE.str.contains('Q'))]

#df2 = df2[df2.CODE.str.len()<8]

#df2 = df2.drop_duplicates(subset=['CODE'])

# %%
#writes all the codes to a folder for dilberts reference
with open('../data/LITCOINDILBERTPREPARED/ontology.tsv', 'w') as f:
    for i,v in df2.iterrows():
        f.write(f'{v["STR"]}\t{v["CODE"]}\n')


