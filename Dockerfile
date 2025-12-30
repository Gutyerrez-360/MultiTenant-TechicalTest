FROM python:3.13-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8006
EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

