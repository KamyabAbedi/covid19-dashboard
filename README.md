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
Feel free to open issues, suggest improvements, or submit pull requests.

## License
This project is licensed under the **MIT License**.

## Contact
For queries or collaborations, reach out via [kamyababedi@gmail.com](mailto:kamyababedi@gmail.com) or visit the [GitHub Repository](https://github.com/KamyabAbedi/covid19-dashboard).