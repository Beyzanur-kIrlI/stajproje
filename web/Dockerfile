FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY api /app/api

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-m", "api.app"]

