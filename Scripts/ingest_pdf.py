import argparse, os, re
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

# ---------------------
# Chunking logic
# ---------------------
def chunk(text, size=800, overlap=150):
    chunks=[]; i=0
    while i < len(text):
        part = text[i:i+size]
        if len(part.strip()) > 50:
            chunks.append(part.strip())
        i += (size - overlap)
    return chunks

# ---------------------
# PDF extraction
# ---------------------
def extract_pdf(path):
    pdf = PdfReader(path)
    full_text = ""
    for page in pdf.pages:
        t = page.extract_text() or ""
        full_text += t + "\n"
    full_text = re.sub(r"\s+\n", "\n", full_text)
    return full_text

# ---------------------
# BATCH WRITER
# ---------------------
def add_in_batches(collection, chunks, batch_size=4000):
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"page_hint": i} for i in range(len(chunks))]

    for i in range(0, len(chunks), batch_size):
        batch_docs = chunks[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]

        print(f"Adding batch {i} → {i+len(batch_docs)}")
        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=batch_meta
        )

# ---------------------
# MAIN
# ---------------------
def main(pdf_path):
    os.makedirs("app/rag/store", exist_ok=True)

    client = chromadb.PersistentClient(path="app/rag/store")
    coll = client.get_or_create_collection(
        name="nephro",
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    )

    # Clear old data
    if coll.count() > 0:
        coll.delete(where={})

    print("[STEP 1] Reading PDF...")
    text = extract_pdf(pdf_path)

    print("[STEP 2] Chunking...")
    chunks = chunk(text)
    print(f"Total chunks: {len(chunks)}")

    print("[STEP 3] Adding to ChromaDB in batches...")
    add_in_batches(coll, chunks, batch_size=4000)

    print("✅ Ingestion completed successfully!")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    args = ap.parse_args()
    main(args.pdf)
