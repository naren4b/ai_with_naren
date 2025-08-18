#!/bin/bash

# install docker 
apt install docker.io
pip install jq

# Running with large language models locally.CPU Only 
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Download the model
docker exec -it ollama ollama run llama3

# Check the models 
curl -s http://localhost:11434/api/tags | jq

# Install Web UI for Ollama based Models 
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
              -v ollama-webui:/app/backend/data \
              --name ollama-webui --restart always \
              ghcr.io/ollama-webui/ollama-webui:main



