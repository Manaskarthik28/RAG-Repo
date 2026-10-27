import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

client = chromadb.PersistentClient(path="items")
collection = client.get_or_create_collection(name="my-collection")

def get_document(file):
    text = file.read().decode('utf-8')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    texts = text_splitter.split_text(text)
    return texts

def save_db(texts: list[str], query: str):
    chunks = texts
    ids=[f"{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        ids=ids
    )
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results




