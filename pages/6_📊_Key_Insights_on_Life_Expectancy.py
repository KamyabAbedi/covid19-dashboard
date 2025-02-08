from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector

from datetime import datetime
import streamlit as st

import plotly.express as px

import pandas as pd
import numpy as np

import altair as alt
from urllib.error import URLError
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

def set_page_config():
    st.set_page_config(page_title="Key Insights on Life Expectancy",
                        page_icon="📊"
    )


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


@st.cache_data
def load_data(sql_query):
    return session.sql(sql_query).collect()


def set_page_content():

    st.markdown("""
                # 📊 Key Insights on Life Expectancy
                ## **Overview**
                The World Happiness Report is a landmark survey of the state of global happiness.
                The following columns: GDP per Capita, Family, Life Expectancy, Freedom, Generosity, Trust Government Corruption describe the extent to which these factors contribute in evaluating the happiness in each country.
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

    # SQL query to retrieve data from the Snowflake table
    sql_d_query = f"""
    SELECT
    *
    FROM
    "LIFE_EXPECTENCY"
    """
    le = load_data(sql_d_query)
    le = pd.DataFrame(le)
    le
    happiness_report = le[['COUNTRY', 'HEALTHY_IFE_EXPECTANCY']]
    # gdp_report = le[['COUNTRY', 'GDP_PER_CAPITA']]

    temp = country_cases_df.merge(happiness_report, left_on='REGION', right_on='COUNTRY')
    fig = px.scatter(temp, y='DEATHS_PER100_CASES', x='HEALTHY_IFE_EXPECTANCY', color='WHO_REGION', hover_data=['COUNTRY'])
    st.plotly_chart(fig, use_container_width=True)
    print(le.columns)
    

if __name__ == "__main__":
    set_page_config()

    # Create and retrieve the Snowflake session
    session = create_session()
    print(session)

    active_session = get_active_session()# Ensure we have the active session
    print(active_session)

    # Content page
    set_page_content()