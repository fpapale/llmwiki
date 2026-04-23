import urllib.request
import urllib.parse
import json
import time

BASE_URL = "http://127.0.0.1:8080"

def print_separator(title):
    print(f"\n{'='*50}")
    print(f"--- {title} ---")
    print(f"{'='*50}")

def make_request(method, endpoint, payload=None):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n> {method} {url}")
    
    headers = {'Content-Type': 'application/json'}
    data = None
    if payload:
        data = json.dumps(payload).encode('utf-8')
        print(f"> Payload: {json.dumps(payload, indent=2)}")
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        start_time = time.time()
        with urllib.request.urlopen(req) as response:
            duration = time.time() - start_time
            body = response.read().decode('utf-8')
            status = response.status
            
            print(f"< Status: {status} ({duration:.2f}s)")
            try:
                # Try to pretty print JSON
                parsed = json.loads(body)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print(body)
                
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"< Status: {e.code} Error")
        try:
            parsed = json.loads(body)
            print(json.dumps(parsed, indent=2))
        except:
            print(body)
    except Exception as e:
        print(f"Errore di connessione: {e}")

def run_all_tests():
    print("Inizio test delle API REST di LLMWiki...")
    
    # 1. Healthcheck
    print_separator("1. Controllo Salute (Healthcheck)")
    make_request("GET", "/health")

    # 2. Configurazione
    print_separator("2. Lettura Configurazione (Safe)")
    make_request("GET", "/config")

    # 3. Importazione di una nuova sorgente
    print_separator("3. Importazione di una nuova Source")
    import_payload = {
        "filename": "test-api-source.md",
        "content": "# Test Source API\n\nQuesta sorgente è stata creata automaticamente dallo script di test."
    }
    make_request("POST", "/sources/import", import_payload)

    # 4. Ingestione (Elaborazione della sorgente)
    print_separator("4. Ingestione (Generazione Riepiloghi)")
    # Nota: richiede che test-api-source.md esista nella cartella raw
    ingest_payload = {
        "source_path": "raw/test-api-source.md",
        "mode": "summary_only" 
    }
    make_request("POST", "/ingest/run", ingest_payload)

    # 5. Lettura Indice Wiki
    print_separator("5. Lettura Indice Wiki")
    make_request("GET", "/pages/index")

    # 6. Query con LLM
    print_separator("6. Esecuzione Query (RAG)")
    query_payload = {
        "question": "Quali argomenti sono trattati nella test source?"
    }
    make_request("POST", "/query/run", query_payload)

    # 7. Linting
    print_separator("7. Esecuzione Linting della Wiki")
    make_request("POST", "/lint/run")

if __name__ == "__main__":
    run_all_tests()
