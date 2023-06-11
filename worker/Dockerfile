FROM python:3.9-slim

WORKDIR /worker

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "worker.py"]



