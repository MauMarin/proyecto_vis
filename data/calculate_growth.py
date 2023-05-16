import pandas as pd
import numpy as np

df = pd.read_csv(f"final_datasets/unemployment analysis.csv")
df = df.reset_index()

df_gdp = pd.read_csv(f"final_datasets/gdp_per_capita_growth.csv")
df_gdp = df_gdp.reset_index()

previous_value = 0

def growth(row):
    global previous_value
    growth = np.NaN
    if int(row['Year']) != 1991:
        growth = row['value'] - previous_value
    previous_value = row['value']
    growth = round(growth, 2)
    return growth


def calculate_growth():
    
    df['growth'] = df.apply(growth, axis=1)

    df.to_csv(f'final_datasets/unemployment analysis.csv', index=0)


def classify(row):
    gdp = 0
    country = row['Country Name']
    year = row['Year']
    #print (country)
    #print (year)
    #gdp = float(df_gdp[df_gdp['Country Name'] == country and df_gdp['Year'] == row['Year']].iloc[0]['value'])
    #gdp = df_gdp[df_gdp['Country Name'] == country and df_gdp['Year'] == row['Year']]['value']
    gdp = df_gdp.query(f"`Country Name` == '{country}' and Year == {year}")
    #print(gdp)

    if gdp.empty:
        return np.NaN
    
    #print("Hola")
    gdp = float(gdp['value'])
    unemp = float(row['growth'])

    if gdp > 0 and unemp < 0:
        return 1
    elif gdp < 0 and unemp < 0:
        return 2
    elif gdp > 0 and unemp > 0:
        return 3
    elif gdp < 0 and unemp > 0:
        return 4
    else:
        return np.NaN


def calculate_case():
    df['case'] = df.apply(classify, axis=1)

    df.to_csv(f'final_datasets/unemployment analysis.csv', index=0)


calculate_case()
