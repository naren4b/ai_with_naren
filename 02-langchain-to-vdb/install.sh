podman run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

podman exec -it ollama ollama pull llama3 
podman exec -it ollama ollama pull gemma3:latest

# podman run -d -p 3000:8080 \
#         --add-host=host.docker.internal:host-gateway \
#         -v ollama-webui:/app/backend/data \
#         --name ollama-webui \
#         --restart always \
#         ghcr.io/ollama-webui/ollama-webui:main



# import ollama

# embedding_dimension = len(
#     ollama.embeddings(model="llama3:latest", prompt="Test sentence.")["embedding"]
# )


LLM_DIMENSION=4096 # len(embedding)
NAME_OF_INDEX=ollama-llama3-embeddings


PORT=5081
podman run -d \
    --name $NAME_OF_INDEX \
    -e PORT=$PORT \
    -e INDEX_TYPE=serverless \
    -e DIMENSION=$LLM_DIMENSION \
    -e METRIC=cosine \
    -p $PORT:$PORT \
    --platform linux/amd64 \
    ghcr.io/pinecone-io/pinecone-index:latest