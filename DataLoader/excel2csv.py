import pandas as pd
import os

file_path='newNode.xlsx'
new_path='newGenerNode'
if not os.path.exists(new_path):
    os.mkdir(new_path)

for idx in range(4):

    data=pd.read_excel(file_path,sheet_name=idx)
    data_col_name=data.columns.values
    data_col_name[0]='name'
    data.columns=data_col_name
    data.to_csv(os.path.join(new_path,'{}.csv'.format(idx+1)),sep=',',encoding='utf-8',index=None)