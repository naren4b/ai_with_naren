import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

load_dotenv()

# Define the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "goharbor-issues-open")

embeddings = OllamaEmbeddings(
    model="llama3:latest",
)

# Load the existing vector store with the embedding function
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)


# Function to query a vector store with different search types and parameters
def query_vector_store(
    store_name, query, embedding_function, search_type, search_kwargs
):
    if os.path.exists(persistent_directory):
        print(f"\n--- Querying the Vector Store {store_name} ---")
        db = Chroma(
            persist_directory=persistent_directory,
            embedding_function=embedding_function,
        )
        retriever = db.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )
        relevant_docs = retriever.invoke(query)
        # Display the relevant results with metadata
        print(f"\n--- Relevant Documents for {store_name} ---")
        for i, doc in enumerate(relevant_docs, 1):
            if doc.metadata:
                for info in doc.metadata:
                    print(f"{info}: {doc.metadata[info]}")
    else:
        print(f"Vector store {store_name} does not exist.")


query = "Redis connection?"

print("\n--- Using Similarity Search ---")
query_vector_store("chroma_db_with_metadata", query, embeddings, "similarity", {"k": 1})
