import os

from langchain_text_splitters import RecursiveJsonSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document
import json


def get_issue_content(issue):
    # Create a readable text representation of the issue
    content = f"Title: {issue.get('title', 'No title')}\n\n"

    if issue.get("body"):
        content += f"Description: {issue.get('body')}\n\n"

    content += f"State: {issue.get('state', 'unknown')}\n"
    content += f"Issue Number: {issue.get('number', 'unknown')}\n"
    content += f"Created: {issue.get('created_at', 'unknown')}\n"
    content += f"Updated: {issue.get('updated_at', 'unknown')}\n"

    # Add labels if they exist
    labels = issue.get("labels", [])
    if labels:
        label_names = [label.get("name", "") for label in labels]
        content += f"Labels: {', '.join(label_names)}\n"

    content += f"URL: {issue.get('html_url', '')}"

    # Create document with metadata
    return Document(
        page_content=content,
        metadata={
            "issue_id": str(issue.get("id", "")),
            "issue_number": str(issue.get("number", "")),
            "title": issue.get("title", ""),
            "state": issue.get("state", ""),
            "url": issue.get("html_url", ""),
            "created_at": issue.get("created_at", ""),
            "updated_at": issue.get("updated_at", ""),
        },
    )


# Define the directory containing the text file and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data", "goharbor-issues.json")
persistent_directory = os.path.join(current_dir, "db", "goharbor-issues-open")

# Check if the Chroma vector store already exists
if not os.path.exists(persistent_directory):
    print("Persistent directory does not exist. Initializing vector store...")

    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )

    # Read the text content from the file
    with open(file_path, "r", encoding="utf-8") as f:
        issues = json.load(f)
    print(f"Length of issues {len(issues)}")
    splitter = RecursiveJsonSplitter(max_chunk_size=300)
    docs = []
    for i, issue in enumerate(issues):
        docs.append(get_issue_content(issue))
        if i == 2:  # for POC taking shorter list
            break
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(issues)} issues")

    # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")
    print(f"Sample chunk:\n{docs[0].page_content}\n")

    # Create embeddings
    print("\n--- Creating embeddings ---")
    embeddings = OllamaEmbeddings(
        base_url="http://localhost:11434",
        model="llama3:latest",
    )
    print("\n--- Finished creating embeddings ---")

    # Create the vector store and persist it automatically
    print("\n--- Creating vector store ---")
    db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
    print("\n--- Finished creating vector store ---")

else:
    print("Vector store already exists. No need to initialize.")
