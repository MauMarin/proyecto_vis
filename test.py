import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import geopandas as gpd
import json
import utils.fetch_data as utils
import pandas as pd


# Global Variables
values = ['gdp','gdp_growth','gdp_per_capita_growth','gdp_per_capita','gdp_ppp','gdp_ppp_per_capita']


utility = utils.Utils()

print(utility.get_happiness_by_year(2014))