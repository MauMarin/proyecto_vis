import pandas as pd

class Utils:

    path = 'data/final_datasets'

    def __init__(self) -> None:
        self.gdp                    = pd.read_csv(f"{self.path}/gdp.csv")  
        self.gdp_growth             = pd.read_csv(f"{self.path}/gdp_growth.csv")
        self.gdp_per_capita_growth  = pd.read_csv(f"{self.path}/gdp_per_capita_growth.csv")
        self.gdp_per_capita         = pd.read_csv(f"{self.path}/gdp_per_capita.csv")
        self.gdp_ppp                = pd.read_csv(f"{self.path}/gdp_ppp.csv")
        self.gdp_ppp_per_capita     = pd.read_csv(f"{self.path}/gdp_ppp_per_capita.csv")
        self.unemployment           = pd.read_csv(f"{self.path}/unemployment analysis.csv")
        self.happiness              = pd.read_csv(f"{self.path}/Happiness_data.csv")

    def get_gdp_by_year(self, val, year):
        temp = ''

        if val == 'gdp':
            temp = self.gdp
        elif val == 'gdp_growth':
            temp = self.gdp_growth
        elif val == 'gdp_per_capita_growth':
            temp = self.gdp_per_capita_growth
        elif val == 'gdp_per_capita':
            temp = self.gdp_per_capita
        elif val == 'gdp_ppp':
            temp = self.gdp_ppp
        elif val == 'gdp_ppp_per_capita':
            temp = self.gdp_ppp_per_capita
        
        temp = temp[ temp['Year'] == year ]

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
            temp = self.gdp
        elif val == 'gdp_growth':
            temp = self.gdp_growth
        elif val == 'gdp_per_capita_growth':
            temp = self.gdp_per_capita_growth
        elif val == 'gdp_per_capita':
            temp = self.gdp_per_capita
        elif val == 'gdp_ppp':
            temp = self.gdp_ppp
        elif val == 'gdp_ppp_per_capita':
            temp = self.gdp_ppp_per_capita
        
        temp = temp[ temp['Country Name'] == country ]

        ret_dict = {
            'df': temp,
            'years': temp['Year'],
            'values': temp['value']
        }
        
        return ret_dict
    
    def get_unemployment_by_year(self, year):
        return self.unemployment[ self.unemployment['Year'] == year ]
    
    def get_unemployment_by_country(self, country):
        return self.unemployment[ self.unemployment['Country Name'] == country ]
    
    def get_happiness_by_year(self, year):
        return self.happiness[ self.happiness['year'] == year ]
    
    def get_happiness_by_country(self, country):
        return self.happiness[ self.happiness['Country name'] == country ]
    
# utils = Utils()
