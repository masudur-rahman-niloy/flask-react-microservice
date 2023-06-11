FROM python:3.9-slim

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]




