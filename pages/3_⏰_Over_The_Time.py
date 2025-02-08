from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector

from datetime import datetime
import streamlit as st

import plotly.express as px

import pandas as pd
import numpy as np



def set_page_config():
    st.set_page_config(page_title="Over the time",
                       page_icon="⏰"
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


def plot_daywise(day_wise, col, hue):
    fig = px.bar(day_wise, x="DATE", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)


def plot_daywise_line(day_wise, col, hue):
    fig = px.line(day_wise, x="DATE", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)


def set_side_bar(day_wise):
    # Sidebar - User Input
    # selected_choice = st.sidebar.selectbox("🌍 Select a Country", sorted(['RECOVERED', 'DEATHS', 'ACTIVE', 'CONFIRMED', 'NEW_CASES', 'NEW_DEATHS', 'NEW_RECOVERED']))
    selected_choice = st.sidebar.selectbox("📈 Select a col for Plotting", sorted(['DEATHS_PER100_CASES', 'DEATHS_PER100_RECOVERED', 'RECOVERED_PER100_CASES']))

    st.sidebar.markdown("---")
    st.sidebar.write("Made by ❤️ for bawag team")
    return selected_choice


def set_page_content():
    st.markdown("""
        # ⏰ COVID Cases Over Time
        ## **Overview**
        This dashboard provides an animated, time-based visualization of COVID-19 cases across the globe, along with a cumulative graph showing the progression of cases over time.
        """)

    # SQL query to retrieve data from the Snowflake table
    sql_query = f"""
    SELECT
    *
    FROM
    "FULL_GROUPED"
    """
    sql_data = load_data(sql_query)
    full_grouped = pd.DataFrame(sql_data)

    full_grouped["DATE"] = pd.to_datetime(full_grouped["DATE"])
    # full_grouped
    # Over the time
    fig = px.choropleth(full_grouped, locations="REGION",
                    color=np.log(full_grouped["CONFIRMED"]),
                    locationmode='country names', hover_name="REGION", 
                    animation_frame=full_grouped["DATE"].dt.strftime('%Y-%m-%d'),
                    title='Cases over time', color_continuous_scale=px.colors.sequential.matter)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        ## **Key Features**

        ### 1. **Animated World Map**
        - Displays the spread of COVID-19 cases globally.
        - **Color Intensity**: Represents the severity of cases in each region (darker colors indicate higher case counts).
        - **Time Slider**: Allows users to view data for specific dates or play the animation for a dynamic visualization.

        ### 2. **Cumulative Cases Graph**
        - Stacked area chart displaying the progression of:
          - **Recovered Cases**: Shown in light blue.
          - **Deaths**: Shown in blue.
          - **Active Cases**: Shown in red.
        - Helps in understanding how the pandemic evolved over time with respect to recoveries, deaths, and active cases.
        """)

    temp = full_grouped.groupby('DATE')[['RECOVERED', 'DEATHS', 'ACTIVE']].sum().reset_index()
    temp = temp.melt(id_vars="DATE", value_vars=['RECOVERED', 'DEATHS', 'ACTIVE'],
                 var_name='Case', value_name='Count')
    fig = px.area(temp, x="DATE", y="Count", color='Case', height=600, width=700,
             title='Cases over time')
    fig.update_layout(xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

    # SQL query to retrieve data from the Snowflake table
    sql_d_query = f"""
    SELECT
    *
    FROM
    "DAY_WISE"
    """
    day_wise = load_data(sql_d_query)
    day_wise = pd.DataFrame(day_wise)
    day_wise
    # selected_choice = set_side_bar(day_wise)
    # plot_daywise(day_wise,selected_choice, '#333333')
    selected_choice = set_side_bar(day_wise)
    plot_daywise_line(day_wise, selected_choice, '#333333')


if __name__ == "__main__":
    set_page_config()

    # Create and retrieve the Snowflake session
    session = create_session()
    print(session)

    active_session = get_active_session()# Ensure we have the active session
    print(active_session)

    # Content page
    set_page_content()