FROM python:3.8.10

WORKDIR /Internship

COPY . .

RUN pip3.8 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "🦠_COVID-19_Analytics_Dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
