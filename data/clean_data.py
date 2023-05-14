import pandas as pd
from os import listdir
from os.path import isfile, join
import json



def transform_datasets():
    changes = json.load(open('name_changes.json'))['others']

    path = 'raw_datasets'
    file_names = [f for f in listdir(path) if isfile(join(path, f))]

    old = changes['old']
    new = changes['new']

    for file in file_names:
        df = pd.read_csv(f"{path}/{file}")
        year_cols = list(df.columns[2:])

        df = pd.melt(df, id_vars=['Country Name', 'Code'], var_name=['Year'], value_vars=year_cols)
        df = df.sort_values(by=['Country Name', 'Year'])
        df = df.dropna(subset='value')

        df['Country Name'] = df['Country Name'].replace(old, new)

        df.to_csv(f'final_datasets/{file}', index=0)


def rename_happiness():
    changes = json.load(open('name_changes.json'))['happiness']
    path = 'final_datasets'
    file = "Happiness_data.csv"

    df = pd.read_csv(f"{path}/{file}")
    df['Country name'] = df['Country name'].replace(changes['old'], changes['new'])

    df.to_csv(f'final_datasets/{file}', index=0)

transform_datasets()
rename_happiness()