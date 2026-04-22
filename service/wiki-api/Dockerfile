FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Di default, i file di configurazione sono attesi in /config
ENV WIKI_API_CONFIG_PATH=/config/config.yaml
ENV WIKI_API_SECRETS_PATH=/config/secrets.env

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
