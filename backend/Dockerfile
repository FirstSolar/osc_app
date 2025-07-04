FROM python:3.11-slim

WORKDIR /app

COPY backend.py .

RUN pip install flask paramiko flask-cors

EXPOSE 5000

CMD ["python", "backend.py"]
