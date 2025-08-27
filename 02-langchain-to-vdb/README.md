# LangChain to VectorDB (Ollama + Pinecone Local)

This project demonstrates how to use [Ollama](https://ollama.com/) for generating text embeddings and [Pinecone Local](https://docs.pinecone.io/docs/local) as a vector database for storing and querying those embeddings. The workflow is designed for easy experimentation with local LLMs and vector search.

## Features

- Loads data from a CSV file (`res/my-data.csv`).
- Splits text into manageable chunks.
- Generates embeddings for each chunk using Ollama.
- Upserts embeddings into a local Pinecone vector database.
- Provides a command-line interface to query the vector database for similar text.

## Project Structure

```
02-langchain-to-vdb/
├── app.py              # Main script
├── install.sh          # Shell script to run Ollama and pull models
├── .env                # Environment variables for Pinecone hosts
├── res/
│   ├── my-data.csv     # Sample data
│   └── ai-langchain-vectordb.jpg
└── README.md           # This file
```

## Setup & Usage

1. **Start Ollama and Pinecone Local**
   - Use `install.sh` to start Ollama in a container and pull required models.
   - Make sure Pinecone Local is running (see Pinecone docs for setup).
2. **Install Python dependencies**
   ```bash
   pip install langchain_text_splitters pinecone ollama
   ```
3. **Configure Environment (optional)**
   - Edit `.env` to set Pinecone hosts if needed.
   - You can also set OLLAMA_MODEL, OLLAMA_HOST, and OLLAMA_TEMPERATURE as environment variables.
4. **Run the script**
   ```bash
   python app.py
   ```
   - The script will load data, generate embeddings, upsert to Pinecone, and enter a query loop.
   - Type your query and get the most similar text chunks from the database.
   - Type `exit` to quit.

## Data Example

The file `res/my-data.csv` contains sample records:

```
Name,Age,Gender,Blood Type,Medical Condition,Date of Admission,Doctor,Hospital,Insurance Provider,Billing Amount,Room Number,Admission Type,Discharge Date,Medication,Test Results
Bobby JacksOn,30,Male,B-,Cancer,2024-01-31,Matthew Smith,Sons and Miller,Blue Cross,18856.281305978155,328,Urgent,2024-02-02,Paracetamol,Normal
LesLie TErRy,62,Male,A+,Obesity,2019-08-20,Samantha Davies,Kim Inc,Medicare,33643.327286577885,265,Emergency,2019-08-26,Ibuprofen,Inconclusive
```

## Flow Diagram

```mermaid
flowchart TD
    A[Load CSV Data] --> B[Split Text into Chunks]
    B --> C[Generate Embeddings with Ollama]
    C --> D[Upsert Embeddings to Pinecone Local]
    D --> E[Query Loop: User Input]
    E --> F[Generate Query Embedding]
    F --> G[Query Pinecone for Similar Vectors]
    G --> H[Display Results]
    E -- exit --> I[End]
```

## Notes

- Ollama and Pinecone Local must be running for the script to work.
- You can customize the chunk size, model, and other parameters in `app.py`.
- This project is for local/demo use and not intended for production.

---

**Author:** naren4b
