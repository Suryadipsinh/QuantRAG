from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# 1. Load the specific Finance CSV you uploaded
df = pd.read_csv("Finance_Data.csv")

# Fill missing values with empty strings so concatenation doesn't break
df = df.fillna("")

# 2. Initialize the local embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Set the database directory
db_location = "./chroma_quantrag_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    print("Initializing QuantRAG Database...")
    print(f"Processing {len(df)} financial records. This may take a few minutes...")
    
    documents = []
    ids = []
    
    for i, row in df.iterrows():
        # Cleanly format the text so the LLM understands the context of the data
        page_content = (
            f"Financial Scenario/Instruction: {row['instruction']}\n"
            f"Context/Input: {row['input']}\n"
            f"Expert Resolution/Output: {row['output']}"
        )
        
        document = Document(
            page_content=page_content,
            metadata={"source": "finance_alpaca", "row_id": i},
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)
        
# 3. Create or load the vector database
vector_store = Chroma(
    collection_name="quantrag_financial_intel",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    # Add documents in batches if necessary, but this handles the direct ingestion
    vector_store.add_documents(documents=documents, ids=ids)
    print("Database built successfully!")
    
# 4. Create the retriever (fetches the top 4 most relevant financial chunks)
retriever = vector_store.as_retriever(
    search_kwargs={"k": 4} 
)