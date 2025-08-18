"""
This script demonstrates how to use Ollama for text embedding generation and Pinecone (local) as a vector database for storing and querying text embeddings.

Features:
- Loads data from a CSV file.
- Splits text into manageable chunks.
- Generates embeddings for each chunk using Ollama.
- Upserts embeddings into a local Pinecone vector database.
- Provides a command-line interface to query the vector database for similar text.

Dependencies:
- langchain_text_splitters
- pinecone
- ollama

Author: naren4b
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone.grpc import PineconeGRPC, GRPCClientConfig
import ollama
import time
import os


# OLLAMA CONFIGURATION
TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.5"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:latest")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# PINECONE CONFIGURATION
PINECONE_LOCAL_HOST = "localhost:5081"
PINECONE_INDEX_NAME = "ollama-llama3-embeddings"
PINECONE_NAMESPACE = "csv-hobby"
PINECONE_API_KEY = "pclocal"


# Initialize Pinecone Local client
print("Initializing Pinecone Local client...")
pc = PineconeGRPC(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(
    host=PINECONE_LOCAL_HOST, grpc_config=GRPCClientConfig(secure=False)
)
print("Pinecone Local client initialized.")


# Text splitting function
def get_splitted_text(text):
    """
    Splits the input text into chunks using RecursiveCharacterTextSplitter.
    Args:
        text (str): The input text to split.
    Returns:
        List[str]: List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    return text_splitter.split_text(text)


# Generates a vector embedding for the given text using Ollama.
def get_embedding(text):
    """
    Generates a vector embedding for the given text using Ollama.
    Args:
        text (str): The input text to embed.
    Returns:
        list or None: The embedding vector, or None if an error occurs.
    """
    try:
        response = ollama.embeddings(model=OLLAMA_MODEL, prompt=text)
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding for '{text}': {e}")
        return None


# Prepares vectors for upsert
def get_vectors_for_upsert(data):
    """
    Prepares a list of vectors for upsert into Pinecone.
    Args:
        data (List[str]): List of text chunks.
    Returns:
        List[dict]: List of vectors with id, values, and metadata.
    """
    vectors_for_pinecone = []
    for i, text in enumerate(data):
        embedding = get_embedding(text)
        if embedding:
            vectors_for_pinecone.append(
                {
                    "id": f"doc_{i}",
                    "values": embedding,
                    "metadata": {"text": text, "source": "ollama_llama3_demo"},
                }
            )
    return vectors_for_pinecone


# Upsert vectors to Pinecone Local
def upsert_to_pinecone_local(vectors_to_upsert):
    """
    Upserts vectors to the specified Pinecone Local index.
    Args:
        vectors_to_upsert (List[dict]): List of vectors to upsert.
    """
    try:
        pinecone_index.upsert(vectors=vectors_to_upsert, namespace=PINECONE_NAMESPACE)
        print(
            f"Successfully upserted {len(vectors_to_upsert)} vectors to Pinecone Local."
        )
    except Exception as e:
        print(f"Error upserting to Pinecone Local: {e}")


# Queries the Pinecone Local index
def query_pinecone_local(query_text):
    """
    Queries the Pinecone Local index for similar vectors.
    Args:
        query_text (str): The input text to query for similarity.
    Returns:
        Query results or None if an error occurs.
    """
    query_vector = get_embedding(query_text)
    top_k = 2
    include_values = False
    include_metadata = True

    try:
        query_results = pinecone_index.query(
            vector=query_vector,
            top_k=top_k,
            include_values=include_values,
            include_metadata=include_metadata,
            namespace=PINECONE_NAMESPACE,
        )
        return query_results
    except Exception as e:
        print(f"Error querying Pinecone Local: {e}")
        return None


# Loads data from a CSV file
def my_data():
    """
    Loads data from a CSV file (res/my-data.csv).
    Returns:
        List[str]: List of lines from the CSV file.
    """
    data = []
    with open("res/my-data.csv", "r") as f:
        for line in f:
            data.append(line.strip())
    return data


# Initializes the Pinecone index
def __init_my_vector_db__():
    """
    Initializes the Pinecone index by loading data, splitting text, generating embeddings, and upserting to Pinecone.
    """
    content = my_data()
    splitted_texts = []
    for data in content:
        splitted_texts.extend(get_splitted_text(data))
    vectors_for_pinecone = get_vectors_for_upsert(splitted_texts)

    upsert_to_pinecone_local(vectors_for_pinecone)

    time.sleep(2)


# Main Execution
if __name__ == "__main__":
    __init_my_vector_db__()
    while True:
        try:
            query_text = input("🗣️ :")
            if query_text.strip().lower() == "exit":
                break
            results = query_pinecone_local(query_text)
            print(f"🌰: \n {results}")
            if results:
                for match in results.matches:
                    print(
                        f"  ID: {match.id}, Score: {match.score}, Text: {match.metadata['text']}"
                    )
            else:
                print("No query results found.")
        except KeyboardInterrupt:
            print("Bye...")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
