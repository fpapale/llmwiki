# LLMWiki

LLMWiki è una knowledge base (Wiki) "filesystem-oriented" potenziata dall'Intelligenza Artificiale (LLM). L'obiettivo è quello di fornire un sistema per gestire, ingerire ed interrogare fonti di conoscenza in formato Markdown tramite agenti e flussi automatizzati (ad es. n8n).

L'architettura separa nettamente i dati di runtime (file wiki, configurazioni, sorgenti) dall'applicazione backend che gestisce l'elaborazione.

## Struttura del Progetto

- `raw/`: Cartella di ingresso per i documenti sorgente (da ingerire).
- `wiki/`: Cartella di destinazione che ospita le note e la knowledge base elaborata, tra cui:
  - `AGENT.MD`: Istruzioni core del sistema.
  - `index.md`: L'indice automatico delle fonti e delle note.
  - `log.md`: Log testuale delle operazioni.
  - `schema.md`: Definizione del formato dei dati estratti.
- `runtime/`: File di configurazione dell'ambiente.
  - `config/config.yaml`: Configurazioni locali per l'API.
  - `config/config.docker.yml`: Configurazioni ottimizzate per l'ambiente containerizzato in produzione.
  - `config/secrets.env`: (Non versionato) Contiene le chiavi API (es. `OPENROUTER_API_KEY`).
- `service/wiki-api/`: Backend applicativo in Python/FastAPI che espone i comandi di base.

## Cosa serve per eseguire l'applicativo?

Per eseguire LLMWiki in locale, i requisiti di sistema sono:
- **Python 3.9+** installato sulla macchina (per l'esecuzione diretta).
- **Docker e Docker Compose** (opzionale, se si desidera eseguire via container per produzione).
- Una chiave API attiva per un provider LLM supportato (es. OpenRouter, OpenAI).

## Installazione e Avvio Locale (Senza Docker)

L'applicazione espone un'API REST costruita con FastAPI. Per avviarla localmente sul tuo sistema operativo in modalità sviluppo:

### 1. Configurazione dei Segreti
Crea il file `runtime/config/secrets.env` partendo da eventuali esempi se presenti o semplicemente inserendo le chiavi necessarie:
```env
OPENROUTER_API_KEY=la-tua-chiave-api
```

### 2. Creazione dell'Ambiente Virtuale
```bash
cd service/wiki-api
python -m venv .venv

# Su Windows:
.venv\Scripts\activate
# Su Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Avvio dell'Applicazione
Prima di avviare il server, è necessario informare l'applicazione di dove si trovino i file di configurazione impostando due variabili d'ambiente.

**Su Windows (PowerShell):**
```powershell
$env:WIKI_API_CONFIG_PATH="../../runtime/config/config.yaml"
$env:WIKI_API_SECRETS_PATH="../../runtime/config/secrets.env"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

**Su Linux/Mac (Bash):**
```bash
export WIKI_API_CONFIG_PATH="../../runtime/config/config.yaml"
export WIKI_API_SECRETS_PATH="../../runtime/config/secrets.env"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

A questo punto, l'API sarà disponibile all'indirizzo `http://127.0.0.1:8080`.
Puoi esplorare l'interfaccia interattiva dell'API (Swagger) visitando `http://127.0.0.1:8080/docs`.

Nel progetto troverai anche lo script `service/wiki-api/test_client.py`, eseguibile da shell per effettuare test rapidi agli endpoint dell'API.

## Deploy su Server (Con Docker)

Per deploy in un ambiente di produzione (o su server locale tramite Docker), il progetto è fornito di `Dockerfile` e `docker-compose.yml` nella cartella `service/wiki-api/`.
1. Assicurati che il file `runtime/config/secrets.env` sia compilato.
2. Vai in `service/wiki-api/` ed avvia i container in background:
```bash
cd service/wiki-api
docker-compose up -d --build
```
Il container Docker monterà la cartella di base dell'intero progetto LLMWiki come volume interno per poter leggere e scrivere i file nelle directory `raw/` e `wiki/`.
