import pandas as pd
from os import listdir
from os.path import isfile, join


def transform_datasets():
    raw_gdp_path = 'raw_gdp_datasets'
    file_names = [f for f in listdir(raw_gdp_path) if isfile(join(raw_gdp_path, f))]

    for file in file_names:
        df = pd.read_csv(f"data/raw_gdp_datasets/{file}")
        year_cols = list(df.columns[2:])

        df = pd.melt(df, id_vars=['Country Name', 'Code'], var_name=['Year'], value_vars=year_cols)
        df = df.sort_values(by=['Country Name', 'Year'])
        df.to_csv(f'final_datasets/{file}')


transform_datasets()