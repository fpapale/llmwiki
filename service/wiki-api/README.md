# Wiki API

Servizio applicativo Python/FastAPI progettato per operare sulla wiki markdown, esponendo API REST richiamabili da browser o sistemi come n8n.
Legge la configurazione esternamente.

## Setup locale sul Portatile

```bash
cd service/wiki-api
python3 -m venv .venv
source .venv/bin/activate  # Su Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Esporta le variabili d'ambiente per puntare ai file di configurazione
export WIKI_API_CONFIG_PATH=../../runtime/config/config.yaml
export WIKI_API_SECRETS_PATH=../../runtime/config/secrets.env
# Su PowerShell:
# $env:WIKI_API_CONFIG_PATH="../../runtime/config/config.yaml"
# $env:WIKI_API_SECRETS_PATH="../../runtime/config/secrets.env"

# Avvio
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## Esecuzione test

```bash
cd service/wiki-api
source .venv/bin/activate
export WIKI_API_CONFIG_PATH=../../runtime/config/config.yaml
export WIKI_API_SECRETS_PATH=../../runtime/config/secrets.env
pytest -q
```

## Esempi di chiamata API locale

Healthcheck:
```bash
curl http://127.0.0.1:8080/health
```

Configurazione sicura:
```bash
curl http://127.0.0.1:8080/config
```

Lettura indice:
```bash
curl http://127.0.0.1:8080/pages/index
```

Import di una source:
```bash
curl -X POST http://127.0.0.1:8080/sources/import \
  -H "Content-Type: application/json" \
  -d '{"filename": "source-test.md", "content": "# Test source\n\nQuesta è una fonte di prova."}'
```

Ingest:
```bash
curl -X POST http://127.0.0.1:8080/ingest/run \
  -H "Content-Type: application/json" \
  -d '{"source_path": "raw/source-test.md", "mode": "summary_only"}'
```

Query:
```bash
curl -X POST http://127.0.0.1:8080/query/run \
  -H "Content-Type: application/json" \
  -d '{"question": "Quali fonti sono presenti nella wiki?"}'
```

Lint:
```bash
curl -X POST http://127.0.0.1:8080/lint/run
```

## Utilizzo sul Server di deploy

Sul server `192.168.0.68` verranno usati `Dockerfile` e `docker-compose.yml`. La cartella di configurazione locale viene montata dentro `/config`, e il vault all'interno di `/vault`.
