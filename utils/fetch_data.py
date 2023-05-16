import pandas as pd

class Utils:

    path = 'data/final_datasets'

    def __init__(self) -> None:
        pass

    def get_gdp_by_year(self, val, year):
        temp = ''

        if val == 'gdp':
            temp = pd.read_csv(f"{self.path}/gdp.csv", quotechar='"')  
        elif val == 'gdp_growth':
            temp = pd.read_csv(f"{self.path}/gdp_growth.csv")
        elif val == 'gdp_per_capita_growth':
            temp = pd.read_csv(f"{self.path}/gdp_per_capita_growth.csv")
        elif val == 'gdp_per_capita':
            temp = pd.read_csv(f"{self.path}/gdp_per_capita.csv")
        elif val == 'gdp_ppp':
            temp = pd.read_csv(f"{self.path}/gdp_ppp.csv")
        elif val == 'gdp_ppp_per_capita':
            temp = pd.read_csv(f"{self.path}/gdp_ppp_per_capita.csv")
        
        temp = temp[ temp['Year'] == year ]

        # print(temp['value'].mean())

        q1 = temp['value'].quantile(0.25)
        q3 = temp['value'].quantile(0.87)
        iqr = q3-q1
        outliers = temp[((temp['value']<(q3+1.5*iqr)))]

        temp_dic = {
            'dataframe': temp,
            'max': outliers['value'].max(),
            'min': temp['value'].min()
        }
        
        return temp_dic
    
    def get_gdp_by_country(self, val, country):
        temp = ''

        if val == 'gdp':
            temp = pd.read_csv(f"{self.path}/gdp.csv", quotechar='"')  
        elif val == 'gdp_growth':
            temp = pd.read_csv(f"{self.path}/gdp_growth.csv")
        elif val == 'gdp_per_capita_growth':
            temp = pd.read_csv(f"{self.path}/gdp_per_capita_growth.csv")
        elif val == 'gdp_per_capita':
            temp = pd.read_csv(f"{self.path}/gdp_per_capita.csv")
        elif val == 'gdp_ppp':
            temp = pd.read_csv(f"{self.path}/gdp_ppp.csv")
        elif val == 'gdp_ppp_per_capita':
            temp = pd.read_csv(f"{self.path}/gdp_ppp_per_capita.csv")
        
        temp = temp[ temp['Country Name'] == country ]

        ret_dict = {
            'df': temp,
            'years': temp['Year'],
            'values': temp['value']
        }
        
        return ret_dict
    
    def get_unemployment_by_year(self, year):
        temp = pd.read_csv(f"{self.path}/unemployment analysis.csv")
        return temp[ temp['Year'] == year ]
    
    def get_unemployment_by_country(self, country):
        temp = pd.read_csv(f"{self.path}/unemployment analysis.csv")
        return temp[ temp['Country Name'] == country ]
    
    def get_happiness_by_year(self, year):
        temp = pd.read_csv(f"{self.path}/Happiness_data.csv")
        return temp[ temp['year'] == year ]
    
    def get_happiness_by_country(self, country):
        temp = pd.read_csv(f"{self.path}/Happiness_data.csv")
        return temp[ temp['Country name'] == country ]
    
# utils = Utils()
