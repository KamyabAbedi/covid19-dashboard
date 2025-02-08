from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector

import streamlit as st

from dotenv import load_dotenv
import os



def set_page_config():
    st.set_page_config(
    page_title="COVID-19 Analytics Dashboard",
    page_icon="🦠",
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


def set_side_bar():
    st.sidebar.write("Made by ❤️ for bawag team")


def set_page_content():
    # Title & Subtitle
    st.markdown("""
    # 🦠 COVID-19 Analytics Dashboard

    ## Overview
    The **COVID-19 Analytics Dashboard** is an interactive data-driven web application built using **Streamlit** and powered by **Snowflake**. It provides insightful visualizations and analytics on COVID-19 data, enabling users to explore key trends, compare regions, and derive meaningful insights.

    ## Features
    - 🌍 **Global and Regional COVID-19 Trends**: Track cases, recoveries, and fatalities over time.
    - ✨ **Interactive Visualizations**: Dynamic charts and tables for deeper analysis.
    - ⚙️ **Customizable Filters**: Select specific regions, timeframes, and metrics.
    - 🏢 **Deployment via Docker**: Containerized for portability.

    ## Tech Stack
    - **Frontend**: Streamlit 🖥️
    - **Database**: Snowflake ❄
    - **Data Processing**: Pandas, NumPy
    - **Visualization**: Plotly
    - **Deployment**: Docker

    ## Installation & Setup

    ### Prerequisites
    Ensure you have the following installed:
    - Python 3.8.20
    - Snowflake Python Connector
    - Streamlit
    - Pandas, NumPy, Plotly
    - Docker

    ### Steps
    1. Clone the repository:
       ```bash
       git clone https://github.com/kamyababedi/covid19-dashboard.git
       cd covid19-dashboard
       ```
    2. Install dependencies:
       ```bash
       pip install -r requirements.txt
       ```
    3. Configure **Snowflake Credentials** in `.env` or Streamlit secrets.
    4. Run the app:
       ```bash
       streamlit run 🦠_COVID-19_Analytics_Dashboard.py
       ```
    5. Deploy using Docker:
       ```bash
       docker build -t covid19-dashboard .
       docker run -p 8501:8501 covid19-dashboard
       ```

    ## Contributing
    We welcome contributions! Feel free to open issues, suggest improvements, or submit pull requests.

    ## License
    This project is licensed under the **MIT License**.

    ## Contact
    For queries or collaborations, reach out via [kamyababedi@gmail.com](mailto:kamyababedi@gmail.com) or visit the [GitHub Repository](https://github.com/KamyabAbedi/covid19-dashboard).

    """, unsafe_allow_html=True)
    set_side_bar()


if __name__ == "__main__":
    set_page_config()

    # Create and retrieve the Snowflake session
    session = create_session()
    # print(session)

    active_session = get_active_session()# Ensure we have the active session
    print(active_session)

    # Content page
    set_page_content()
