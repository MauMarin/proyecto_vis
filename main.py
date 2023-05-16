import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
import plotly.express as px
import geopandas as gpd
import json
import utils.fetch_data
  
# Opening JSON file
f = open('data/countries.geojson')
  
# returns JSON object as 
# a dictionary
geodata = json.load(f)

utility = utils.fetch_data.Utils()

st.set_page_config(
    page_title = 'GDP/Employment Dashboard',
    page_icon = '📈',
    layout = 'wide'
)
global_year=2020

def apply_filter_gdp(metric, year):
    df = utility.get_gdp_by_year(metric, year)
    df2 = df["dataframe"]
    geo_df_tmp = gpd.GeoDataFrame.from_features(
        geodata["features"]
    ).rename(columns={"ISO_A3":"Code"})

    geo_df = geo_df_tmp.merge(df2, how="inner").set_index("Code")

    fig = px.choropleth_mapbox(geo_df,
                               geojson=geo_df.geometry,
                               locations=geo_df.index,
                               color='value',
                               color_continuous_scale="haline",
                               center={"lat": 0, "lon": 0},
                               mapbox_style="carto-positron",
                               zoom=1,
                               range_color=[df['min'], df['max']], #
                               height=1100)
    return fig

def apply_filter_unemp(year):
    df = utility.get_unemployment_by_year(year)
    #df["case"] = df["case"].astype(str)
    geo_df_tmp = gpd.GeoDataFrame.from_features(
        geodata["features"]
    ).rename(columns={"ISO_A3":"Code"})

    geo_df = geo_df_tmp.merge(df, how="inner").set_index("Code")

    fig = px.choropleth_mapbox(geo_df,
                               geojson=geo_df.geometry,
                               locations=geo_df.index,
                               color='case',
                               color_continuous_scale=["blue", "green",
                                         "yellow", "red"],
                               center={"lat": 0, "lon": 0},
                               mapbox_style="carto-positron",
                               zoom=1,
                               range_color=[1, 4],
                               height=1100)
    return fig

#load custom css
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

with st.sidebar:

    global_year = st.slider('Year', 1960, 2021, 2020)

tab1, tab2 = st.tabs(["PIB per capita", "Casos de crecimiento"])

with tab1:
   fig = apply_filter_gdp("gdp_per_capita",global_year)
   st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = apply_filter_unemp(global_year)
    st.plotly_chart(fig, use_container_width=True)