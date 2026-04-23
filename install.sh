#!/bin/bash
set -e

echo "Starting LLMWiki Installation..."

# Naviga nella directory in cui si trova questo script
cd "$(dirname "$0")"

# Assicurati che le directory runtime/config esistano
mkdir -p runtime/config
mkdir -p raw
mkdir -p wiki

# Avvia i container docker
echo "Building and starting Docker containers..."
cd service/wiki-api
if command -v docker-compose &> /dev/null; then
    docker-compose up -d --build
else
    docker compose up -d --build
fi

echo "LLMWiki has been successfully installed and started."
