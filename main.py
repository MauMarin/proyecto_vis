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

def apply_filter(year):
    df = utility.get_gdp_by_year("gdp",year)
    df2 = df["dataframe"]
    print(df2)
    geo_df_tmp = gpd.GeoDataFrame.from_features(
        geodata["features"]
    ).rename(columns={"ISO_A3":"Code"})

    geo_df = geo_df_tmp.merge(df2, how="inner").set_index("Code")
    #print(geo_df)
    #).merge(df2, on="Code").set_index("ISO_A3")

    fig = px.choropleth_mapbox(geo_df,
                               geojson=geo_df.geometry,
                               locations=geo_df.index,
                               color="value",
                               center={"lat": 0, "lon": 0},
                               mapbox_style="carto-positron",
                               zoom=1,
                               height=1100)
    return fig

#load custom css
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

with st.sidebar:

    with st.form('filters'):
        PROVINCES = ['Cartago', 'San Jose', 'Guanacaste', 'Heredia', 'Alajuela', 'Limon', 'Puntarenas', 'Unknown']

        with st.expander('', expanded = True):
            year = selectbox("Year", options = [2019, 2020, 2021], label_visibility = 'visible', no_selection_label = 'All')
        with st.expander('', expanded = True):
            province = selectbox("Province", options = PROVINCES, label_visibility = 'visible', no_selection_label = 'All')
        with st.expander('', expanded = True):
            time_day = selectbox("Time of day", options = ['Early Morning', 'Morning', 'Night', 'Afternoon'], label_visibility = 'visible', no_selection_label = 'All')
        with st.expander('', expanded = True):
            gender = selectbox("Gender", options = ['Male', 'Female', 'Non applicable'], label_visibility = 'visible', no_selection_label = 'All')

        st.form_submit_button('Apply    ', type = 'primary', use_container_width= True)

tab1, tab2 = st.tabs(["Map1", "Map2"])

with tab1:
   fig = apply_filter(2020)
   st.plotly_chart(fig, use_container_width=True)
