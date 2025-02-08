from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector

from datetime import datetime
import streamlit as st

import plotly.express as px

import pandas as pd
import numpy as np



def set_page_config():
    st.set_page_config(page_title="Composition of Cases",
                       page_icon="🗺️"
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


def plot_treemap(country_wise, col):
    fig = px.treemap(country_wise, path=[px.Constant("world"),'WHO_REGION', 'REGION'], values=col, height=700,
                 title=col, color_discrete_sequence = px.colors.qualitative.Dark2)
    fig.data[0].textinfo = 'label+text+value'
    st.plotly_chart(fig, use_container_width=True)


def set_page_content():
    st.markdown("""
        # 🗺️ Composition of Cases
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
    # country_wise
    plot_treemap(country_wise, 'CONFIRMED')
    plot_treemap(country_wise, 'DEATHS')


if __name__ == "__main__":
    set_page_config()

    # Create and retrieve the Snowflake session
    session = create_session()
    print(session)

    active_session = get_active_session()# Ensure we have the active session
    print(active_session)

    # Content page
    set_page_content()