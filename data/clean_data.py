import pandas as pd
from os import listdir
from os.path import isfile, join


def transform_datasets():
    path = 'raw_datasets'
    file_names = [f for f in listdir(path) if isfile(join(path, f))]

    for file in file_names:
        df = pd.read_csv(f"{path}/{file}")
        year_cols = list(df.columns[2:])

        df = pd.melt(df, id_vars=['Country Name', 'Code'], var_name=['Year'], value_vars=year_cols)
        df = df.sort_values(by=['Country Name', 'Year'])
        df = df.dropna(subset='value')
        df.to_csv(f'final_datasets/{file}', index=0)


transform_datasets()