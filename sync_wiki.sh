#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/docker/llmwiki"
LOCK_FILE="/tmp/llmwiki-sync.lock"
LOG_PREFIX="[llmwiki-sync]"

log() {
  echo "$LOG_PREFIX $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

# Lock: evita esecuzioni concorrenti
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  log "altra istanza già in esecuzione, esco."
  exit 0
fi

cd "$REPO_DIR"

# Config Git minima
git config user.name  "LLMWiki Server"    >/dev/null
git config user.email "server@llmwiki.local" >/dev/null

# Verifica repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "ERRORE: $REPO_DIR non è un repository git valido"
  exit 1
fi

# ── STEP 1: stash di TUTTO (staged, unstaged, untracked) ──────────────────────
# Deve avvenire PRIMA di qualsiasi operazione remota per evitare
# l'errore "cannot pull with rebase: You have unstaged changes"
STASH_REF="auto-stash-llmwiki-$(date +%s)"
STASHED=0
if ! git stash push -u -m "$STASH_REF" --quiet 2>/dev/null; then
  log "nessun file da stashare, continuo."
else
  STASHED=1
  log "stash temporaneo creato: $STASH_REF"
fi

# ── STEP 2: fetch per conoscere lo stato del remoto ───────────────────────────
log "scarico aggiornamenti dal remoto..."
git fetch origin main --quiet 2>/dev/null || git fetch origin main

AHEAD=$(git rev-list origin/main..HEAD --count 2>/dev/null || echo 0)
BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo 0)
log "stato locale: $AHEAD commit da pushare, $BEHIND commit da ricevere"

# ── STEP 3: rebase sui commit remoti se necessario ────────────────────────────
if [ "$BEHIND" -gt 0 ]; then
  log "applico $BEHIND commit dal remoto con rebase..."
  if ! git rebase origin/main; then
    log "ERRORE durante il rebase, annullo e ripristino lo stash..."
    git rebase --abort 2>/dev/null || true
    [ $STASHED -eq 1 ] && git stash pop --quiet 2>/dev/null || true
    exit 1
  fi
  log "rebase completato."
fi

# ── STEP 4: ripristina i file dallo stash ─────────────────────────────────────
if [ $STASHED -eq 1 ]; then
  if git stash pop --quiet 2>/dev/null; then
    log "stash ripristinato con successo."
  else
    log "ATTENZIONE: conflitti nel ripristino dello stash — richiede intervento manuale."
    log "Usa: git stash list / git stash show / git stash pop"
  fi
fi

# ── STEP 5: stage e commit dei file wiki ──────────────────────────────────────
git add raw/ wiki/ AGENT.MD schema.md README.md 2>/dev/null || true

if git diff --cached --quiet; then
  log "nessuna nuova modifica da committare."
else
  COMMIT_MSG="auto-sync: wiki update $(date '+%Y-%m-%d %H:%M:%S')"
  git commit -m "$COMMIT_MSG"
  log "commit creato: $COMMIT_MSG"
fi

# ── STEP 6: push ──────────────────────────────────────────────────────────────
AHEAD=$(git rev-list origin/main..HEAD --count 2>/dev/null || echo 0)

if [ "$AHEAD" -gt 0 ]; then
  log "push di $AHEAD commit verso origin/main..."
  if ! git push origin main; then
    log "ERRORE durante git push"
    exit 1
  fi
  log "sincronizzazione completata con successo."
else
  log "tutto allineato, nulla da pushare."
fi
