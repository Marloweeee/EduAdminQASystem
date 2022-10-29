# coding=utf8
import pandas as pd
import os

file_path='newNode.xlsx'
new_path='newGenerNode'
if not os.path.exists(new_path):
    os.mkdir(new_path)

sen=[]

for idx in range(14):



    data=pd.read_excel(file_path,sheet_name=idx)
    data_col_name=data.columns.values
    data_col_name[0]='name'
    data.columns=data_col_name
    data.to_csv(os.path.join(new_path,'{}.csv'.format(idx+1)),sep=',',encoding='utf-8',index=None)

    merge_sentence = "LOAD CSV WITH HEADERS FROM 'file:///DataLoader/newGenerNode/{}.csv' AS row MERGE (n:{}{}name:row.name" .format(idx+1,data.iloc[0][0],'{')
    for name in data_col_name[1:]:
        merge_sentence+=',{}:row.{}'.format(name,name)
    merge_sentence+='})'
    sen.append(merge_sentence)
for i in sen:
    with open('newGenerNode/cql_import.txt','a+') as f:
        f.write(i+'\n')
