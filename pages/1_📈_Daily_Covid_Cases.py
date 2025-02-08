from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector

from datetime import datetime
import streamlit as st

import plotly.express as px

import pandas as pd
import numpy as np

from dotenv import load_dotenv
import os



def set_page_config():
    st.set_page_config(page_title="Daily Covid Cases", 
                       page_icon="📈"
    )


# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def create_session():
    return Session.builder.configs({
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA")
    }).create()



def set_side_bar(country_cases_df):
    # Sidebar - User Input
    st.sidebar.header("🔍 Filter Data")
    selected_country = st.sidebar.selectbox("🌍 Select a Country", sorted(set(country_cases_df.REGION)))
    start_date, end_date = st.slider(
        "Select Date Range:",
        min_value=country_cases_df["DATE"].min(),
        max_value=country_cases_df["DATE"].max(),
        value=(country_cases_df["DATE"].min(), country_cases_df["DATE"].max()),
        format="YYYY-MM-DD"
    )
    filtered_data = country_cases_df[(country_cases_df["REGION"] == selected_country) & (country_cases_df["DATE"] >= start_date) & (country_cases_df["DATE"] <= end_date)]
    filtered_data

    st.sidebar.markdown("---")
    st.sidebar.write("Made by ❤️ for bawag team")
    return filtered_data, selected_country


@st.cache_data
def load_data(sql_query):
    return session.sql(sql_query).collect()


def set_page_content():
    st.markdown("""
        # 📈 Daily Covid Cases Tracker

        ## **Dataset Overview**
        The dataset tracks daily COVID-19 statistics across regions, providing detailed metrics for confirmed cases, deaths, recoveries, and active cases.

        ---

        ## **Columns Description**
        - **STATE**: Administrative division within a country (e.g., province or state).
        - **REGION**: The country name (e.g., Afghanistan).
        - **LAT**: Latitude coordinate of the region.
        - **LONG**: Longitude coordinate of the region.
        - **DATE**: Date of the recorded data.
        - **CONFIRMED**: Cumulative confirmed cases up to the specified date.
        - **DEATHS**: Cumulative deaths up to the specified date.
        - **RECOVERED**: Cumulative recoveries up to the specified date.
        - **ACTIVE**: Number of active cases (likely calculated as `CONFIRMED - (DEATHS + RECOVERED)`).
        - **WHO Region**: World Health Organization's regional classification for the region.

        """)

    # SQL query to retrieve data from the Snowflake table
    sql_query = f"""
    SELECT
    *
    FROM
    "COVID_19_CLEAN_COMPLETE"
    """
    sql_data = load_data(sql_query)

    country_cases_df = pd.DataFrame(sql_data)

    filtered_data, selected_country = set_side_bar(country_cases_df)

    # Metrics Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Confirmed Cases", f"{filtered_data['CONFIRMED'].max():,}")
    col2.metric("Total Deaths Cases", f"{filtered_data['DEATHS'].max():,}")
    col3.metric("Total Recovered Cases", f"{filtered_data['RECOVERED'].max():,}")

    st.markdown("""
        ---
        ## **Key Features**
        - **Interactive Filters**:
          - Date Range: Allows filtering of data within a specific date range.

        - **Summarized Metrics**:
          - **Total Confirmed Cases**: Aggregate of confirmed cases within the selected date range.
          - **Total Death Cases**: Aggregate of death cases within the selected date range.
          - **Total Recovered Cases**: Aggregate of recoveries within the selected date range.

        ---

        ## **Possible Uses**
        1. **Trend Analysis**: Analyze how cases, deaths, and recoveries evolve over time.
        2. **Regional Comparison**: Compare COVID-19 impact across regions.
        3. **Public Health Insights**: Support decision-making in managing resources and implementing policies.
        """
        )

    fig = px.line(filtered_data[filtered_data.REGION==selected_country], x="DATE", y="ACTIVE", title=f"{selected_country} - Daily Active COVID Cases")
    st.plotly_chart(fig)


if __name__ == "__main__":
    set_page_config()

    # Create and retrieve the Snowflake session
    session = create_session()
    print(session)

    active_session = get_active_session()# Ensure we have the active session
    print(active_session)

    # Content page
    set_page_content()