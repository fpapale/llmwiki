#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/docker/llmwiki"
LOCK_FILE="/tmp/llmwiki-sync.lock"
LOG_PREFIX="[llmwiki-sync]"

log() {
  echo "$LOG_PREFIX $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  log "altra istanza già in esecuzione, esco."
  exit 0
fi

cd "$REPO_DIR"

# Config Git minima, se non già presente
git config user.name "LLMWiki Server" >/dev/null
git config user.email "server@llmwiki.local" >/dev/null

# Verifica veloce repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "directory non valida come repository git: $REPO_DIR"
  exit 1
fi

# Aggiungi solo i path che vuoi davvero sincronizzare (incluso assets)
git add raw raw/assets wiki AGENT.MD schema.md README.md 2>/dev/null || true

# Se ci sono modifiche staged, crea un commit
if git diff --cached --quiet; then
  log "nessuna nuova modifica da committare."
else
  COMMIT_MSG="auto-sync: wiki update $(date '+%Y-%m-%d %H:%M:%S')"
  git commit -m "$COMMIT_MSG"
  log "commit creato: $COMMIT_MSG"
fi

# Controlla se ci sono commit locali non ancora pushati
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null || echo "none")

if [ "$LOCAL" = "$REMOTE" ]; then
  log "nulla da pushare, tutto allineato."
  exit 0
fi

log "trovati commit non pushati, sincronizzo..."

# Allineamento col remoto
if ! git pull --rebase --autostash origin main; then
  log "errore durante git pull --rebase origin main"
  exit 1
fi

# Push finale
if ! git push origin main; then
  log "errore durante git push origin main"
  exit 1
fi

log "sincronizzazione completata con successo."
