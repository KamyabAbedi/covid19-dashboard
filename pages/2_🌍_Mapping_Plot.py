from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector

from datetime import datetime
import streamlit as st

import plotly.express as px

import pandas as pd
import numpy as np



def set_page_config():
    st.set_page_config(page_title="Mapping Plot",
                       page_icon="🌍"
    )


@st.cache_resource
def create_session():
   #Creates a Snowflake session and caches it for performance optimization.
    return Session.builder.configs(
        {"user" :"kamyababedi",
        "password" : "ivationToken=ver%3A1-hint",
        "account" : "xg72263.switzerland-north.azure",
        "warehouse" : "COMPUTE_WH",
        "database" : "COVID",
        "schema" : "PUBLIC"}).create()


@st.cache_data
def load_data(sql_query):
    return session.sql(sql_query).collect()


def plot_map(df, col, pal):
    fig = px.choropleth(df, locations="REGION", locationmode='country names', 
                  color=col, hover_name="REGION", 
                  title=col.capitalize()+ " Cases", hover_data=[col], color_continuous_scale=pal)
    st.plotly_chart(fig, use_container_width=True)


def set_side_bar():
    # Sidebar - User Input
    st.sidebar.header("⛏️ Choose Cases")
    option = st.sidebar.selectbox("Select an Option",
                         ("CONFIRMED", "DEATHS"),
    )
    st.sidebar.markdown("---")
    st.sidebar.write("Made by ❤️ for bawag team")
    return option


def set_page_content():
    st.markdown("""
        # 🌍 Regional Data and Mapping Plot
        ## **Dataset Overview**
        This page includes a table summarizing key COVID-19 metrics for different regions and a world map visualization to illustrate the spread of confirmed cases.

        ---

        ## **Columns Description**
        - **REGION**: Country or region name.
        - **CONFIRMED**: Cumulative confirmed cases.
        - **DEATHS**: Cumulative deaths.
        - **RECOVERED**: Cumulative recoveries.
        - **ACTIVE**: Current active cases (calculated as `CONFIRMED - (DEATHS + RECOVERED)`).
        - ...
        """)

    # SQL query to retrieve data from the Snowflake table
    sql_query = f"""
    SELECT
    *
    FROM
    "COUNTRY_WISE_LATEST"
    """
    sql_data = load_data(sql_query)
    country_cases_df = pd.DataFrame(sql_data)
    country_cases_df
    option = set_side_bar()
    # Metrics Display
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Confirmed Cases", f"{country_cases_df['CONFIRMED'].sum():,}")
    col2.metric("Total Deaths Cases", f"{country_cases_df['DEATHS'].sum():,}")
    col3.metric("Total Recovered Cases", f"{country_cases_df['RECOVERED'].sum():,}")
    col4.metric("Total Active Cases", f"{country_cases_df['ACTIVE'].sum():,}")
    st.markdown("""
        ## **Key Features**

        1. **Summarized Metrics**:
           - **Total Confirmed Cases**: 16,480,485
           - **Total Death Cases**: 654,036
           - **Total Recovered Cases**: 9,468,087
           - **Total Active Cases**: 6,358,362

        3. **Mapping Visualization**:
           - Color-coded map to highlight the number of confirmed cases across different regions.
           - Darker colors represent higher case counts, providing an intuitive visual comparison.
   """)
    plot_map(country_cases_df, option, 'matter')
    st.markdown("""
        ## Recovery Rate Per 100 Cases

        ### **Formula**
        To calculate the recovery rate per 100 cases:

        Recovered per 100 cases = ((RECOVERED) / (CONFIRMED)) * 100

        This metric provides an intuitive understanding of how many people recover for every 100 confirmed cases in a region.

        """)
    if option == "DEATHS":
        fig = px.choropleth(country_cases_df, locations="REGION", locationmode='country names', 
                            color='RECOVERED', hover_name="REGION", 
                            title="Deaths / 100 Cases", hover_data=['DEATHS_PER100_CASES'], color_continuous_scale='matter')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.choropleth(country_cases_df, locations="REGION", locationmode='country names', 
                            color='DEATHS', hover_name="REGION", 
                            title="Recovered / 100 Cases", hover_data=['RECOVERED_PER100_CASES'], color_continuous_scale='matter')
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    set_page_config()

    # Create and retrieve the Snowflake session
    session = create_session()
    print(session)

    active_session = get_active_session()# Ensure we have the active session
    print(active_session)

    # Content page
    set_page_content()