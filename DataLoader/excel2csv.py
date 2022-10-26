import pandas as pd

file_path='newNode.xlsx'

for idx in range(4):

    data=pd.read_excel(file_path,sheet_name=idx)
    data_col_name=data.columns.values
    data_col_name[0]='name'
    data.columns=data_col_name
    data.to_csv('newGenerNode/{}.csv'.format(idx),sep=',',encoding='utf-8',index=None)