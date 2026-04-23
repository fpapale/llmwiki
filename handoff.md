# LLMWiki API - Handoff Document

Questo documento riassume tutto il lavoro svolto finora per l'implementazione del servizio **`wiki-api`** all'interno dell'infrastruttura **LLMWiki**, come richiesto dalle specifiche di progetto.

## 🏗️ Architettura e Struttura Implementata
L'applicazione è stata sviluppata seguendo l'approccio "filesystem-first" delineato nel brief. La root directory `d:\LLMWiki` contiene ora:
- `raw/`: Cartella destinata all'importazione dei file sorgenti grezzi non ancora elaborati.
- `wiki/`: Il vero e proprio vault, che ospita i file markdown della knowledge base, tra cui `index.md` e `log.md`.
- `runtime/config/`: Contiene le configurazioni dell'ambiente (vedi sezione *Configurazione*).
- `service/wiki-api/`: L'intero codice sorgente del servizio FastAPI.
- `schema.md` e `AGENT.MD`: Documentazione operativa base del wiki.

## ⚙️ Configurazione e Portabilità
Per rendere il servizio pronto al deploy remoto e indipendente dal codice, la configurazione è stata esternalizzata:
- **`config.yaml`**: Si trova in `runtime/config/config.yaml`. Contiene tutti i path (relativi alla sua stessa posizione, per garantirne il funzionamento ovunque lo si copi), le feature toggles (abilitazione mock, fallback) e le opzioni per il provider LLM.
- **`secrets.env`**: File posizionato in `runtime/config/secrets.env` adibito al caricamento delle API Key (escluso dal `.gitignore` per motivi di sicurezza).

## 🚀 Endpoint Sviluppati
Tutte le API richieste sono state esposte su `http://127.0.0.1:8080`:
- `GET /health`: Healthcheck standard e stato di operatività del servizio.
- `GET /config`: Ispezione della configurazione corrente (mascherando i segreti).
- `GET /pages/{slug}`: Recupero del contenuto di una singola pagina del wiki.
- `POST /sources/import`: Scrittura di un file sorgente direttamente nella cartella `raw/`.
- `POST /ingest/run`: Elaborazione asincrona (mock/reale) di un sorgente, aggiornamento di `index.md` e append in `log.md`.
- `POST /query/run`: Ricerca e generazione di risposta basata sui contenuti del wiki (con *fallback deterministico* integrato).
- `POST /lint/run`: Controllo di consistenza del vault (verifica indici e link orfani).

## 🧠 Integrazione LLM (OpenAI & OpenRouter)
Il motore LLM (`app/services/llm_service.py`) è in grado di funzionare in **due modalità**:
1. **Mock Mode** (`enable_mock_llm: true`): Perfetto per lo sviluppo locale e i test, non effettua chiamate di rete e restituisce risposte simulate, permettendo di testare il flusso (ingest e update del log) a costo zero.
2. **Real Mode** (`enable_mock_llm: false`): Instanzia il client ufficiale `openai`. Leggendo il file YAML, è capace di utilizzare sia le API dirette di **OpenAI** sia le API di **OpenRouter** (cambiando la variabile `api_key_env` e il `base_url`).

## 🐳 Deploy e Ambiente di Produzione
L'applicazione è attualmente pubblicata e in esecuzione come container Docker sul server remoto locale `192.168.0.68` (nella directory `~/docker/llmwiki`).
- È presente un `Dockerfile` (leggero e basato su Python 3.11 slim) completo di file `.dockerignore`.
- Il `docker-compose.yml` è configurato per montare la directory di configurazione in `/config` e l'intera root del vault in `/vault`. Viene inoltre utilizzato il file specifico `config.docker.yml`.
- È stato creato uno script `install.sh` ed è stato ottimizzato lo script Python `service/wiki-api/deploy_remote.py`. Quest'ultimo automatizza il deploy collegandosi via SSH, aggiornando il repository tramite git pull, trasferendo i file non tracciati o modificati (come `secrets.env` e `config.docker.yml`) via SFTP, e lanciando l'installazione su Docker Compose.

## 🧪 Testing e Qualità
- Tutti i test richiesti (Healthcheck, Config, Endpoints di base e flussi LLM mockati) sono stati implementati utilizzando `pytest`.
- I test passano con successo in ambiente locale.

## 📦 Versionamento
L'intero blocco di codice (incluso un esaustivo `README.md` sotto `service/wiki-api/` contenente le istruzioni di setup) è costantemente allineato sul branch `main` del repository GitHub: **[fpapale/llmwiki](https://github.com/fpapale/llmwiki)**.

---
**Stato Attuale e Prossimi Passi**:
1. **Ambiente Live**: Il servizio risponde su `http://192.168.0.68:8080/` ed è pronto a ricevere chiamate REST.
2. **Motore LLM Attivo**: L'impostazione `enable_mock_llm` è stata modificata a `false` nel file `config.docker.yml`. Questo significa che il server sta utilizzando i veri servizi AI (tramite la chiave configurata in `secrets.env`).
3. **Prossimo Step - Integrazione**: Procedere all'integrazione di questi endpoint all'interno dei workflow di **n8n** per avviare l'orchestrazione automatica tra Ingestione, Query e la UI.
