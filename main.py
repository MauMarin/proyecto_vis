import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
import plotly.express as px
import geopandas as gpd
import json
import utils.fetch_data as utils
  
# Opening JSON file
f = open('data/countries.geojson')
  
# returns JSON object as 
# a dictionary
geodata = json.load(f)

utility = utils.Utils()

values = ['gdp','gdp_growth','gdp_per_capita_growth','gdp_per_capita','gdp_ppp','gdp_ppp_per_capita']

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

    fig = px.choropleth_mapbox(
        geo_df,
        geojson=geo_df.geometry,
        locations=geo_df.index,
        color='value',
        color_continuous_scale="haline",
        center={"lat": 0, "lon": 0},
        mapbox_style="carto-positron",
        zoom=1.2,
        hover_data=['Country Name', 'value'],
        range_color=[df['min'], df['max']],
        height=1100
    )

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
    global_year = st.slider('Year', 1960, 2020, 2010)

tab1, tab2, tab3 = st.tabs(["PIB per capita", "Casos de crecimiento", "Ver datos de país"])

with tab1:
	with st.container():
		fig = apply_filter("gdp_per_capita",global_year)
		st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = apply_filter_unemp(global_year)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
	with st.container():
		col1, col2, col3 = st.columns(3)

		charts = []
		country = 'Costa Rica'

		for i in values:
			t = utility.get_gdp_by_country(i, country)
			chart = px.scatter(t['df'], x = 'Year', y = 'value', title=i, labels=['year', i])
			charts.append(chart)


		with col1:
			st.plotly_chart(charts[0], use_container_width=True)
			st.plotly_chart(charts[3], use_container_width=True)
		with col2:
			st.plotly_chart(charts[1], use_container_width=True)
			st.plotly_chart(charts[4], use_container_width=True)
		with col3:
			st.plotly_chart(charts[2], use_container_width=True)
			st.plotly_chart(charts[5], use_container_width=True)