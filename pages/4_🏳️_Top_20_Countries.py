from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector

from datetime import datetime
import streamlit as st

import plotly.express as px

import pandas as pd
import numpy as np



def set_page_config():
    st.set_page_config(page_title="Top 20 Countries",
                       page_icon="🏳️"
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


def plot_hbar(df, col, n, hover_data=[]):
    fig = px.bar(df.sort_values(col).tail(n), 
                 x=col, y="REGION", color='WHO_REGION',  
                 text=col, orientation='h', width=700, hover_data=hover_data,
                 color_discrete_sequence = px.colors.qualitative.Dark2)
    fig.update_layout(title=col, xaxis_title="", yaxis_title="", 
                      yaxis_categoryorder = 'total ascending',
                      uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)


def set_side_bar():
    # Sidebar - User Input
    st.sidebar.header("🔍 Plotting")
    selected_choice = st.sidebar.selectbox("📈 Select a col for Plotting", sorted(['RECOVERED', 'DEATHS', 'ACTIVE', 'CONFIRMED', 'NEW_CASES', 'NEW_DEATHS', 'NEW_RECOVERED', 'DEATHS_PER100_CASES', 'DEATHS_PER100_RECOVERED', 'RECOVERED_PER100_CASES', 'ONE_WEEK_CHANGE', 'ONE_WEEK_INCREASE', ]))

    st.sidebar.markdown("---")
    st.sidebar.write("Made by ❤️ for bawag team")
    return selected_choice


def set_page_content():
    st.markdown("""
        # 🏳️ Top 20 Countries by COVID Metrics

        ## **Overview**
        This page presents an interactive analysis of the top 20 countries most affected by COVID-19, based on key metrics such as confirmed cases, deaths, recoveries, and active cases.

        The goal is to provide insights into the global impact of the pandemic and figour it out which country has a better performance.

        ---
        Interpreting the Table

        | Column Name            | Description                                                                 |
        |------------------------|-----------------------------------------------------------------------------|
        | **COUNTRY**            | Name of the country.                                                       |
        | **CONFIRMED**          | Total confirmed cases reported.                                            |
        | **DEATHS**             | Total deaths reported.                                                    |
        | **RECOVERED**          | Total recoveries reported.                                                |
        | **ACTIVE**             | Number of active cases.                                                   |
        | **NEW_CASES**          | Recent cases reported (last update).                                      |
        | **NEW_DEATHS**         | Recent deaths reported (last update).                                     |
        | **DEATHS_PER100_CASES**| Deaths per 100 confirmed cases.                                            |
        | **DEATHS_PER100_RECOVERED** | Deaths per 100 recoveries, reflecting severity compared to recoveries.|
        | **RECOVERED_PER100_CASES**  | Recoveries per 100 confirmed cases, showing recovery efficiency.      |
        | **ONE_WEEK_CHANGE**    | Change in active cases over the last 7 days.                              |
        | **ONE_WEEK_INCREASE**  | Percentage increase in active cases compared to the previous week.        |
    """)

    # SQL query to retrieve data from the Snowflake table
    sql_d_query = f"""
    SELECT
    *
    FROM
    "COUNTRY_WISE_LATEST"
    """
    country_wise = load_data(sql_d_query)
    country_wise = pd.DataFrame(country_wise)
    country_wise
    selected_choice = set_side_bar()
    plot_hbar(country_wise, selected_choice, 15)


if __name__ == "__main__":
    set_page_config()

    # Create and retrieve the Snowflake session
    session = create_session()
    print(session)

    active_session = get_active_session()# Ensure we have the active session
    print(active_session)

    # Content page
    set_page_content()