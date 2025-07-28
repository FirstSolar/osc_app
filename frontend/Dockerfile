FROM python:3.11-slim

WORKDIR /app

COPY frontend.py .

RUN pip install streamlit pandas requests streamlit-autorefresh

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "frontend.py"]
CMD ["--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
