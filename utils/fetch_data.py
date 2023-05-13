import pandas as pd

class Utils:

    def __init__(self) -> None:
        path = '../data/final_datasets'
        
        self.gdp = pd.read_csv(f"{path}/gdp.csv")
        self.gdp_growth = pd.read_csv(f"{path}/gdp_growth.csv")
        self.gdp_per_capita_growth = pd.read_csv(f"{path}/gdp_per_capita_growth.csv")
        self.gdp_per_capita = pd.read_csv(f"{path}/gdp_per_capita.csv")
        self.gdp_ppp = pd.read_csv(f"{path}/gdp_ppp.csv")
        self.gdp_ppp_per_capita = pd.read_csv(f"{path}/gdp_ppp_per_capita.csv")
        self.unemployment = pd.read_csv(f"{path}/unemployment analysis.csv")
        self.happiness = pd.read_csv(f"{path}/Happiness_data.csv")

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
        
        return temp[ temp['Year'] == year ]
    
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
        
        return temp[ temp['Country Name'] == country ]
    
    def get_unemployment_by_year(self, year):
        return self.unemployment[ self.unemployment['Year'] == year ]
    
    def get_unemployment_by_country(self, country):
        return self.unemployment[ self.unemployment['Country Name'] == country ]
    
    def get_happiness_by_year(self, year):
        return self.happiness[ self.happiness['year'] == year ]
    
    def get_happiness_by_country(self, country):
        return self.happiness[ self.happiness['Country name'] == country ]
    

utils = Utils()
# print(utils.get_gdp_by_year('gdp_per_capita', 2015))
# print(utils.get_gdp_by_country('gdp_per_capita', 'Costa Rica'))
# print(utils.get_unemployment_by_country('Costa Rica'))
# print(utils.get_unemployment_by_year(2015))
# print(utils.get_happiness_by_country('Costa Rica'))
print(utils.get_happiness_by_year(2015))