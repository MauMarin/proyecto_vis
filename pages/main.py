import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
import plotly.express as px
import geopandas as gpd

st.set_page_config(
    page_title = 'GDP/Employment Dashboard',
    page_icon = '📈',
    layout = 'wide'
)

#load custom css
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

df = px.data.election()
geo_df = gpd.GeoDataFrame.from_features(
    px.data.election_geojson()["features"]
).merge(df, on="district").set_index("district")

fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           color="Joly",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="open-street-map",
                           zoom=8.5,
                           height=1100)



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
   st.plotly_chart(fig, use_container_width=True)
