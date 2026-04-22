# Brief operativo per Antigravity — Servizio `wiki-api`

## Obiettivo

Nel workspace esistente `LLMWiki`, crea un **servizio applicativo Python/FastAPI** chiamato `wiki-api` che lavori sulla wiki markdown già presente e che sia progettato per:

- operare sul filesystem reale della wiki;
- rispettare il pattern LLM Wiki già definito in `wiki/AGENT.MD`;
- esporre API REST richiamabili da browser, da test locali e da `n8n`;
- essere sviluppato e testato sul **Portatile**;
- essere poi esportato e deployato in Docker sul **Server di deploy** `192.168.0.68`;
- usare una **configurazione esterna montata da path locale**, così da non dover modificare il container internamente per cambiare path, provider, modelli o chiavi.

---

## Contesto già presente

La struttura del repository è già simile a questa:

```text
LLMWiki/
├─ .obsidian/
├─ raw/
│  └─ assets/
└─ wiki/
   ├─ index.md
   ├─ log.md
   ├─ AGENT.MD
   └─ schema.md
```

### Vincoli obbligatori

1. **Non modificare distruttivamente** la struttura esistente.
2. Il sistema deve restare **filesystem-first**:
   - `raw/` = fonti sorgente
   - `wiki/` = pagine markdown generate e mantenute
   - `AGENT.MD` = schema operativo dell'agente
3. `index.md` e `log.md` devono essere trattati come file centrali del sistema.
4. Il core MVP **non deve dipendere da database esterni**.
5. Il servizio deve leggere/scrivere file markdown reali e non simulazioni in memoria.
6. La configurazione deve stare **fuori dal codice** e **fuori dal container**.

---

## Stack richiesto

Usa:

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic Settings
- PyYAML
- pytest
- httpx per i test delle API
- logging standard Python

Evita per ora:

- vector DB
- database SQL/NoSQL
- code enterprise inutilmente complesso
- code generation eccessiva
- sistemi RAG complessi

---

## Struttura che devi creare

Crea questa struttura applicativa aggiuntiva:

```text
LLMWiki/
├─ raw/
├─ wiki/
├─ service/
│  └─ wiki-api/
│     ├─ app/
│     │  ├─ main.py
│     │  ├─ config.py
│     │  ├─ dependencies.py
│     │  ├─ api/
│     │  │  ├─ health.py
│     │  │  ├─ sources.py
│     │  │  ├─ ingest.py
│     │  │  ├─ query.py
│     │  │  ├─ lint.py
│     │  │  └─ pages.py
│     │  ├─ models/
│     │  │  ├─ requests.py
│     │  │  └─ responses.py
│     │  ├─ services/
│     │  │  ├─ file_service.py
│     │  │  ├─ path_service.py
│     │  │  ├─ log_service.py
│     │  │  ├─ index_service.py
│     │  │  ├─ llm_service.py
│     │  │  ├─ ingest_service.py
│     │  │  ├─ query_service.py
│     │  │  └─ lint_service.py
│     │  └─ utils/
│     │     └─ markdown_utils.py
│     ├─ tests/
│     │  ├─ test_health.py
│     │  ├─ test_config.py
│     │  ├─ test_pages.py
│     │  └─ test_ingest_smoke.py
│     ├─ requirements.txt
│     ├─ README.md
│     ├─ .env.example
│     ├─ Dockerfile
│     └─ docker-compose.yml
└─ runtime/
   ├─ config/
   │  ├─ config.yaml
   │  ├─ secrets.env
   │  └─ .gitkeep
   └─ data/
      └─ .gitkeep
```

### Note importanti sui path

- `runtime/config/` deve contenere la configurazione modificabile dall'esterno.
- in futuro questo path verrà montato nel container come `/config`
- il servizio dovrà poter leggere la configurazione anche in locale dal **Portatile**
- non usare path hardcoded assoluti specifici del tuo computer

---

## Requisiti funzionali MVP

Implementa questi endpoint.

### 1. Healthcheck

**GET** `/health`

Risposta attesa:

```json
{
  "status": "ok",
  "service": "wiki-api"
}
```

---

### 2. Config inspection

**GET** `/config`

Restituisce una versione sicura della configurazione caricata, senza esporre chiavi segrete.

Deve mostrare almeno:
- path wiki effettivi risolti
- provider LLM
- modello configurato
- root directory del vault

---

### 3. Lettura pagina wiki

**GET** `/pages/{slug}`

Comportamento:
- legge `wiki/{slug}.md`
- restituisce titolo, slug, path e contenuto markdown

Esempio:
- `GET /pages/index`
- `GET /pages/log`

---

### 4. Import source

**POST** `/sources/import`

Input JSON:

```json
{
  "filename": "source-test.md",
  "content": "# Test source\n\nQuesta è una fonte di prova."
}
```

Comportamento:
- salva il file in `raw/`
- non sovrascrive senza controllo
- restituisce il path creato

---

### 5. Ingest

**POST** `/ingest/run`

Input JSON:

```json
{
  "source_path": "raw/source-test.md",
  "mode": "summary_only"
}
```

Comportamento MVP:
- legge il file sorgente
- legge `wiki/AGENT.MD`
- crea una pagina di summary in `wiki/` con nome derivato dalla source, ad esempio `source-test-summary.md`
- aggiorna `wiki/index.md` aggiungendo una voce se assente
- aggiorna `wiki/log.md` aggiungendo una entry cronologica
- restituisce i file toccati

Non è necessario, in questa prima versione, implementare una vera intelligenza avanzata di knowledge graph. Va bene una prima logica semplice ma pulita.

---

### 6. Query

**POST** `/query/run`

Input JSON:

```json
{
  "question": "Quali fonti sono presenti nella wiki?"
}
```

Comportamento MVP:
- legge prima `wiki/index.md`
- legge eventualmente `wiki/log.md`
- legge le pagine più rilevanti tra `index.md`, `log.md` e altre pagine semplici
- restituisce una risposta testuale strutturata
- se l'LLM non è configurato, deve poter rispondere in fallback in modo deterministico usando solo il filesystem

---

### 7. Lint

**POST** `/lint/run`

Comportamento MVP:
- controlla che esistano `index.md`, `log.md`, `AGENT.MD`
- cerca pagine `.md` in `wiki/` non indicizzate
- cerca file vuoti
- produce un report JSON semplice

---

## Configurazione esterna obbligatoria

Il servizio deve leggere la configurazione da un file YAML esterno e da un file `.env` esterno.

### Variabili ambiente richieste

Supporta queste variabili:

```bash
WIKI_API_CONFIG_PATH
WIKI_API_SECRETS_PATH
```

### Percorsi attesi

#### Sul Portatile, in locale

Esempio:

```bash
export WIKI_API_CONFIG_PATH=../../runtime/config/config.yaml
export WIKI_API_SECRETS_PATH=../../runtime/config/secrets.env
```

#### Nel container, in futuro

```text
/config/config.yaml
/config/secrets.env
```

---

## Contenuto atteso di `runtime/config/config.yaml`

Crea un file di esempio come questo:

```yaml
app:
  name: wiki-api
  host: 0.0.0.0
  port: 8080
  log_level: INFO

paths:
  vault_root: ../../
  raw_dir: ../../raw
  wiki_dir: ../../wiki
  schema_dir: ../../wiki
  agent_file: ../../wiki/AGENT.MD
  index_file: ../../wiki/index.md
  log_file: ../../wiki/log.md

llm:
  enabled: true
  provider: openai
  base_url: https://api.openai.com/v1
  model: gpt-5.4
  api_key_env: OPENAI_API_KEY
  timeout_seconds: 120

features:
  enable_fallback_query: true
  enable_mock_llm: true
```

### Regola sui path

Il servizio deve:
- risolvere i path relativi a partire dalla posizione del file `config.yaml`
- supportare anche path assoluti
- validare all'avvio che i path essenziali esistano

---

## Contenuto atteso di `runtime/config/secrets.env`

Crea un template come questo:

```env
OPENAI_API_KEY=replace_me
```

Non committare valori reali.

---

## Requisiti applicativi

### Config loader
Implementa un loader robusto che:
- carica `config.yaml`
- carica `secrets.env`
- risolve e valida i path
- espone una configurazione typed via Pydantic

### LLM service
Implementa `llm_service.py` con interfaccia astratta semplice:
- se `llm.enabled = false`, usa fallback deterministico
- se `enable_mock_llm = true`, consenti una modalità mock per test locali
- incapsula tutta la logica provider in un unico punto

### File service
Implementa operazioni sicure per:
- leggere file
- scrivere file
- creare directory se assenti
- evitare path traversal
- verificare estensioni markdown dove opportuno

### Index service
Implementa una logica minima per:
- leggere `index.md`
- verificare se una pagina è già presente
- aggiungere una nuova voce in fondo o in una sezione semplice

### Log service
Implementa una logica minima per:
- appendere righe a `log.md`
- usare formato coerente tipo:

```md
## [2026-04-22 16:30:00] ingest | source-test.md
- created: wiki/source-test-summary.md
- updated: wiki/index.md
- updated: wiki/log.md
```

---

## Requisiti di qualità

- codice chiaro e leggibile
- moduli piccoli
- type hints
- docstring essenziali
- error handling chiaro
- niente overengineering
- README con istruzioni reali
- test minimi eseguibili

---

## README richiesto

Crea un `README.md` che spieghi:

1. cos'è il servizio
2. come configurarlo sul Portatile
3. come avviarlo in locale
4. come eseguire i test
5. come chiamare gli endpoint principali
6. come verrà poi usato sul Server di deploy

---

## Comandi che devi preparare nel README

Inserisci nel README i comandi operativi esatti.

### Setup locale sul Portatile

```bash
cd service/wiki-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export WIKI_API_CONFIG_PATH=../../runtime/config/config.yaml
export WIKI_API_SECRETS_PATH=../../runtime/config/secrets.env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Esecuzione test

```bash
cd service/wiki-api
source .venv/bin/activate
export WIKI_API_CONFIG_PATH=../../runtime/config/config.yaml
export WIKI_API_SECRETS_PATH=../../runtime/config/secrets.env
pytest -q
```

### Esempi di chiamata API locale

```bash
curl http://127.0.0.1:8080/health
```

```bash
curl http://127.0.0.1:8080/config
```

```bash
curl http://127.0.0.1:8080/pages/index
```

```bash
curl -X POST http://127.0.0.1:8080/sources/import \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "source-test.md",
    "content": "# Test source\n\nQuesta è una fonte di prova."
  }'
```

```bash
curl -X POST http://127.0.0.1:8080/ingest/run \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "raw/source-test.md",
    "mode": "summary_only"
  }'
```

```bash
curl -X POST http://127.0.0.1:8080/query/run \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quali fonti sono presenti nella wiki?"
  }'
```

```bash
curl -X POST http://127.0.0.1:8080/lint/run
```

---

## Cosa devi fare ora in Antigravity

Esegui in questo ordine:

### Task 1
Crea tutta la struttura del progetto `service/wiki-api` e `runtime/config`.

### Task 2
Genera il codice del servizio FastAPI con gli endpoint MVP richiesti.

### Task 3
Genera i file di configurazione di esempio:
- `runtime/config/config.yaml`
- `runtime/config/secrets.env`
- `service/wiki-api/.env.example`

### Task 4
Genera il `README.md` con i comandi esatti di setup, run e test.

### Task 5
Genera i test minimi:
- health
- config load
- pages/index
- ingest smoke test

### Task 6
Esegui localmente, dal Portatile, i seguenti controlli:
- install dipendenze
- avvio server
- test pytest
- chiamate curl principali

### Task 7
Se trovi errori, correggili fino ad avere:
- server avviabile
- endpoint health funzionante
- config caricata correttamente
- import source funzionante
- ingest smoke funzionante
- lint funzionante

---

## Cosa mi devi restituire in output

Alla fine del lavoro, mostrami:

1. l'albero finale dei file creati
2. l'elenco dei file principali con una breve spiegazione
3. i comandi esatti da eseguire sul Portatile
4. il risultato atteso di:
   - `/health`
   - `/config`
   - import source
   - ingest
   - lint
5. eventuali problemi rimasti aperti
6. eventuali scelte tecniche fatte

---

## Cosa chiamare per il test da Antigravity

Quando hai finito di generare e correggere il progetto, esegui e/o fammi eseguire questi test sul Portatile:

### Test 1
```bash
curl http://127.0.0.1:8080/health
```

### Test 2
```bash
curl http://127.0.0.1:8080/config
```

### Test 3
```bash
curl http://127.0.0.1:8080/pages/index
```

### Test 4
```bash
curl -X POST http://127.0.0.1:8080/sources/import \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "source-test.md",
    "content": "# Test source\n\nQuesta è una fonte di prova."
  }'
```

### Test 5
```bash
curl -X POST http://127.0.0.1:8080/ingest/run \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "raw/source-test.md",
    "mode": "summary_only"
  }'
```

### Test 6
```bash
curl -X POST http://127.0.0.1:8080/lint/run
```

### Test 7
```bash
curl -X POST http://127.0.0.1:8080/query/run \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quali fonti sono presenti nella wiki?"
  }'
```

---

## Requisito finale importante

Il codice deve essere scritto in modo che, al passo successivo, si possa fare il deploy in Docker sul **Server di deploy** `192.168.0.68` con:

- mount del vault wiki
- mount della cartella di configurazione locale su `/config`
- esposizione porta API
- utilizzo da `n8n` remoto via HTTP

Quindi già ora:
- separa bene codice, dati e configurazione
- non hardcodare path
- non hardcodare chiavi
- rendi chiaro cosa andrà montato come volume nel deploy

Fine task.
