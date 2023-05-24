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


@st.cache_data
def load_data():
    f = open('data/countries.geojson')
    geodata = json.load(f)
    utility = utils.Utils()
    return (geodata, utility)


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
    geo_df_tmp = gpd.GeoDataFrame.from_features(
        geodata["features"]
    ).rename(columns={"ISO_A3":"Code"})

    geo_df = geo_df_tmp.merge(df, how="inner").set_index("Code")

    fig = px.choropleth_mapbox(geo_df,
        geojson=geo_df.geometry,
        locations=geo_df.index,
        color='case',
        color_continuous_scale=["blue", "green", "yellow", "red"],
        center={"lat": 0, "lon": 0},
        mapbox_style="carto-positron",
        zoom=1,
        range_color=[1, 4],
        height=1100
	)
    return fig

def main():

    global_year=2020
    global_country=""

    #load custom css
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

    with st.sidebar:
        global_year = st.slider('Year', 1990, 2020, 2000)

        df = utility.get_gdp_by_year("gdp_per_capita", global_year)
        df = df["dataframe"]
        global_country = st.selectbox(
            'Country',
            df["Country Name"]
        )

    tab1, tab2, tab3, tab4 = st.tabs(["GDP per Capita", "Growth Cases", "Data per Country", "Multivariable Comparison"])

    with tab1:
        with st.container():
            fig = apply_filter_gdp("gdp_per_capita",global_year)
            st.plotly_chart(fig, use_container_width=True)
        
        with st.container():
            col1, col2, col3 = st.columns(3)

            for i in values:
                t1 = utility.get_gdp_by_year(i, global_year)['dataframe']
                t2 = utility.get_unemployment_by_year(global_year).rename(columns={'value': 'value_unemp'})
                new_df = pd.merge(t1, t2, on='Country Name', how='inner')
                chart = px.scatter(new_df, x = 'value_unemp', y = 'value', title=f'{i} vs Unemployment')
                st.plotly_chart(chart, use_container_width=True)

    with tab2:
        fig = apply_filter_unemp(global_year)
        st.plotly_chart(fig, use_container_width=True)


    with tab3:
        temp_unemp = utility.get_unemployment_by_country(global_country)
        chart = px.line(
            temp_unemp, 
            x = 'Year', 
            y = 'value',
            title=f'{global_country}\'s Unemployment Throughout the Years',
            labels={"value": "Unemployment", "Year": "Year"}
        )

        st.plotly_chart(chart, use_container_width=True)


        curr_index = st.selectbox(
            'Economic Index',
            [
                'Gdp', 
                'Gdp Growth', 
                'Gdp Per Capita Growth', 
                'Gdp Per Capita', 
                'Gdp Ppp', 
                'Gdp Ppp Per Capita'
            ]
        )

        econ = utility.get_gdp_by_country(curr_index.lower().replace(' ', '_'), global_country)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(
                x=temp_unemp['Year'], 
                y=temp_unemp['value'], 
                name="Unemployment", 
                mode='lines'
            ),
            secondary_y=True,
        )

        fig.add_trace(
            go.Scatter(
                x=econ['df']['Year'], 
                y=econ['df']['value'], 
                name=curr_index, 
                mode='lines'
            ),
            secondary_y=False,
        )

        # Add figure title
        fig.update_layout(
            title_text=f"Unemployment vs {curr_index}"
        )
        fig.update_xaxes(title_text="Year")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
        fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

    
    with tab4:
        curr_index = st.selectbox(
            'Economic Index',
            [
                'Gdp', 
                'Gdp Growth', 
                'Gdp Per Capita Growth', 
                'Gdp Per Capita', 
                'Gdp Ppp', 
                'Gdp Ppp Per Capita'
            ],
            key=42069
        )

        curr_hap = st.selectbox(
            'Happiness Factor',
            [
                'Life Ladder',
                'Log GDP per capita',
                'Social support',
                'Healthy life expectancy at birth',
                'Freedom to make life choices',
                'Generosity',
                'Perceptions of corruption',
                'Positive affect',
                'Negative affect',
                'Confidence in national government'
            ]
        )

        global_year = 2014

        df1 = utility.get_unemployment_by_year(global_year)
        df2 = utility.get_happiness_by_year(global_year).rename(columns={'Country name': 'Country Name'})
        df3 = utility.get_gdp_by_year(curr_index.lower().replace(' ', '_'), global_year)['dataframe']

        temp_df = pd.merge(df1, df3, on='Country Name', how='inner')
        temp_df = pd.merge(temp_df, df2, on='Country Name', how='inner')


        fig = px.scatter_3d(temp_df, x='value_x', y='value_y', z=curr_hap, color='value_x', labels={'value_y': curr_index, "value_x": "Unemployment"})
        st.plotly_chart(fig, use_container_width=True)




st.set_page_config(
    page_title = 'GDP/Employment Dashboard',
    page_icon = '📈',
    layout = 'wide'
)

geodata, utility = load_data()
main()