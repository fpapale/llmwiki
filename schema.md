# LLM Wiki Schema

Questo file descrive come l'LLM deve gestire questo wiki.

## Regole Generali
- Il wiki è un insieme di file markdown gestito interamente dall'LLM. L'utente curerà le fonti, porrà domande e delineerà la sintesi, ma spetta all'LLM l'onere dell'aggiornamento e della manutenzione.
- I sorgenti grezzi si trovano in `raw/` e non devono mai essere modificati (read-only per l'LLM).
- Tutti i file generati, di sintesi e di metadati vengono salvati in `wiki/`.
- La comunicazione avverrà esclusivamente in lingua italiana.

## Operazioni
1. **Ingest (Ingestione):** Quando l'utente aggiunge una nuova fonte in `raw/` e chiede di processarla, l'LLM deve:
   - Leggere la fonte senza alterarla.
   - Discutere i punti chiave con l'utente, se richiesto.
   - Creare una pagina di sintesi o di note in `wiki/`.
   - Aggiornare `wiki/index.md` con il nuovo file.
   - Aggiornare o creare pagine di concetti/entità correlate.
   - Aggiungere una voce in `wiki/log.md` alla fine.
2. **Query (Consultazione):** Per rispondere alle domande, l'LLM cerca prima in `wiki/index.md` per individuare le pagine rilevanti, quindi legge i relativi file. Risposte di alto valore (confronti, analisi complesse) possono essere salvate come nuove pagine in `wiki/` su istruzione o suggerimento all'utente.
3. **Lint (Manutenzione):** Su richiesta, l'LLM esaminerà il wiki per identificare contraddizioni, informazioni obsolete, pagine orfane, concetti mancanti o reference non validi, proponendo all'utente nuovi approfondimenti per mantenere in salute la knowledge base.

## Formato del Log
In `wiki/log.md`, usare sempre il seguente prefisso cronologico per facilitare il parsing (es. con `grep` o plugin come Dataview):
`## [YYYY-MM-DD] <operazione> | Titolo`

(Tipi di operazione: `ingest`, `query`, `lint`, `update`, `init`)
