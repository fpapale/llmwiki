# 🔄 n8n Workflow — LLMWiki Ingestione Automatica Raw

Questo documento spiega come installare, configurare e utilizzare il workflow n8n che automatizza l'ingestione dei documenti nel sistema **LLMWiki**.

---

## 📋 Prerequisiti

Prima di importare il workflow, assicurati che:

| Componente | Requisito |
|---|---|
| n8n | Versione ≥ 1.0 (self-hosted o cloud) |
| Wiki API | In esecuzione su `http://192.168.0.68:8080` |
| Rete | n8n deve raggiungere `192.168.0.68` sulla porta `8080` |

---

## 🏗️ Architettura del Sistema

```
┌─────────────┐       ogni 15 min       ┌────────────────────────────────────┐
│  n8n        │ ─────────────────────── │  Server 192.168.0.68               │
│  (scheduler)│                         │                                    │
│             │ GET /sources/unprocessed│  ┌─────────────┐                   │
│             │ ──────────────────────► │  │  wiki-api   │ :8080             │
│             │ ◄────────────────────── │  │  (FastAPI)  │                   │
│             │  ["raw/doc.pdf", ...]   │  └──────┬──────┘                   │
│             │                         │         │ legge file                │
│             │ POST /ingest/run        │  ┌──────▼──────┐                   │
│             │ {source_path, mode}     │  │  raw/       │ (volume Docker)   │
│             │ ──────────────────────► │  │  ├─ *.md    │                   │
│             │ ◄────────────────────── │  │  └─ assets/ │                   │
│             │  {"status": "ok"}       │  │     ├─ *.pdf│                   │
└─────────────┘                         │  │     ├─ *.docx                   │
                                        │  │     └─ *.xlsx                   │
                                        │  └─────────────┘                   │
                                        │                                    │
                                        │  ┌─────────────┐                   │
                                        │  │  wiki/      │ → output Obsidian │
                                        │  │  *-summary.md                   │
                                        │  └─────────────┘                   │
                                        └────────────────────────────────────┘
```

---

## 🚀 Installazione su Server Remoto (192.168.0.68)

### 1. Installare n8n con Docker

Connettiti al server via SSH e lancia n8n:

```bash
ssh utente@192.168.0.68

# Crea la directory di dati
mkdir -p ~/n8n-data

# Lancia n8n con Docker
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v ~/n8n-data:/home/node/.n8n \
  --add-host=host.docker.internal:host-gateway \
  n8nio/n8n:latest
```

> **Nota**: L'opzione `--add-host=host.docker.internal:host-gateway` permette a n8n (dentro Docker) di raggiungere la `wiki-api` che gira sullo stesso server. In alternativa, usa l'IP diretto `192.168.0.68`.

### 2. Accedere all'interfaccia n8n

Apri il browser e vai su:

```
http://192.168.0.68:5678
```

Al primo accesso, crea un account amministratore (rimane locale, non richiede connessione internet).

### 3. Importare il Workflow

1. Nella sidebar sinistra, clicca su **Workflows**
2. Clicca sul pulsante **⊕ Add workflow** (in alto a destra)
3. Nel menu del workflow, clicca su **···** → **Import from File**
4. Seleziona il file: `n8n/llmwiki_ingestione_automatica.json`
5. Il workflow viene importato con tutti i nodi configurati

### 4. Verificare la Connettività

Prima di attivare, verifica che n8n raggiunga la wiki-api:

```bash
# Dal server 192.168.0.68
curl http://192.168.0.68:8080/sources/unprocessed
# Risposta attesa: {"unprocessed": [...]}

curl http://192.168.0.68:8080/health
# Risposta attesa: {"status": "ok"}
```

### 5. Attivare il Workflow

1. Apri il workflow importato
2. Clicca il toggle **Inactive → Active** in alto a destra
3. Il workflow inizierà a girare automaticamente ogni **15 minuti**

---

## ⚙️ Come Funziona il Workflow (Nodo per Nodo)

Il workflow è composto da **4 nodi** in sequenza:

```
[Schedule Trigger] → [Get Unprocessed] → [Split Items] → [Ingest File]
```

### Nodo 1 — Schedule Trigger ⏰

| Campo | Valore |
|---|---|
| Tipo | `scheduleTrigger` |
| Frequenza | Ogni **15 minuti** |
| Funzione | Avvia il workflow automaticamente |

Puoi modificare l'intervallo aprendo il nodo e cambiando `minutesInterval`. Valori suggeriti:
- `5` → molto frequente (test)
- `15` → standard (produzione)
- `60` → ogni ora (basso traffico)

---

### Nodo 2 — Get Unprocessed 📋

| Campo | Valore |
|---|---|
| Tipo | `HTTP Request GET` |
| URL | `http://192.168.0.68:8080/sources/unprocessed` |

Interroga la wiki-api per ottenere l'elenco dei file **non ancora elaborati**. La API controlla:
- Tutti i file `.md` in `raw/`
- Tutti i file `.pdf`, `.docx`, `.xlsx` in `raw/assets/`
- Per ognuno verifica se esiste già il corrispondente summary in `wiki/`

**Risposta tipica:**
```json
{
  "unprocessed": [
    "raw/assets/documento.pdf",
    "raw/nuovo-articolo.md"
  ]
}
```

---

### Nodo 3 — Split Items ✂️

| Campo | Valore |
|---|---|
| Tipo | `Code` (JavaScript) |
| Funzione | Trasforma la lista in item separati |

```javascript
const unprocessed = $input.first().json.unprocessed || [];
return unprocessed.map(path => ({json: {source_path: path}}));
```

Questo nodo prende l'array `["file1.pdf", "file2.md"]` e lo converte in **due item distinti**, in modo che il nodo successivo venga eseguito una volta per ogni file.

---

### Nodo 4 — Ingest File 📥

| Campo | Valore |
|---|---|
| Tipo | `HTTP Request POST` |
| URL | `http://192.168.0.68:8080/ingest/run` |
| Body | JSON con `source_path` e `mode` |

Per ogni file dell'elenco, chiama la wiki-api per avviarne l'elaborazione:

```json
{
  "source_path": "raw/assets/documento.pdf",
  "mode": "summary_only"
}
```

La wiki-api:
1. Legge il file (con parsing nativo per PDF/DOCX/XLSX)
2. Invia il testo all'LLM configurato
3. Scrive il summary in `wiki/<nome-file>-summary.md`

**Risposta:**
```json
{
  "status": "ok",
  "output_path": "wiki/documento-summary.md"
}
```

---

## 📂 Formati di File Supportati

| Formato | Estensione | Directory |
|---|---|---|
| Markdown | `.md` | `raw/` |
| PDF | `.pdf` | `raw/assets/` |
| Word | `.docx` | `raw/assets/` |
| Excel | `.xlsx` | `raw/assets/` |

---

## 🔧 Configurazione Avanzata

### Cambiare il Server API

Se la wiki-api viene spostata su un altro IP/porta, modifica i nodi **Get Unprocessed** e **Ingest File** aggiornando l'URL:

```
http://<NUOVO_IP>:<NUOVA_PORTA>/sources/unprocessed
http://<NUOVO_IP>:<NUOVA_PORTA>/ingest/run
```

### Cambiare la Modalità di Ingestione

Il parametro `mode` nel nodo **Ingest File** può essere:

| Mode | Descrizione |
|---|---|
| `summary_only` | Genera solo il file summary in `wiki/` (default) |
| `full` | Indicizza anche in vettoriale (se configurato) |

### Monitorare le Esecuzioni

In n8n, vai su **Executions** nella sidebar per vedere:
- Lo storico di tutte le esecuzioni
- I file elaborati per ogni run
- Eventuali errori con il dettaglio del messaggio

---

## 🩺 Troubleshooting

### Il workflow non trova file da elaborare

```bash
# Verifica che i file siano nella directory giusta sul server
ls -la ~/docker/llmwiki/raw/assets/

# Verifica che la API risponda correttamente
curl http://192.168.0.68:8080/sources/unprocessed
```

### Errore di connessione al momento dell'ingestione

```bash
# Verifica che wiki-api sia in esecuzione
docker ps | grep wiki-api

# Verifica i log del container
docker logs wiki-api --tail 50
```

### Il summary non viene creato

```bash
# Controlla i log della wiki-api per errori LLM
docker logs wiki-api --tail 100 | grep ERROR

# Verifica la configurazione della chiave API LLM in
cat ~/docker/llmwiki/runtime/config/secrets.env
```

---

## 🔁 Flusso Completo End-to-End

```
1. Utente aggiunge file in raw/assets/ sul server
      ↓
2. sync_wiki.sh (cron ogni N minuti) → git push su GitHub
      ↓
3. n8n (Schedule Trigger ogni 15 min) → GET /sources/unprocessed
      ↓
4. wiki-api risponde con lista file non processati
      ↓
5. n8n → POST /ingest/run per ogni file
      ↓
6. wiki-api: parsing (PDF/DOCX/XLSX) → LLM → summary.md in wiki/
      ↓
7. sync_wiki.sh → git push dei summary generati su GitHub
      ↓
8. git pull sul PC locale → summary disponibili in Obsidian
```
