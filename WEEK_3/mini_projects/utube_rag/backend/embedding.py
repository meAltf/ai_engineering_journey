from sentence_transformers import SentenceTransformer
import json
from pathlib import Path


# Load model
emb_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load json from yt-transcriber -> output section
DATA_PATH = Path("../yt-transcriber/output")

# Debuggin path's related issue
# print(Path.cwd())
# print(Path("../yt_transcriber/output").resolve())
# print(Path("../yt_transcriber/output").exists())


documents = []

# Load all json files
for file in DATA_PATH.glob("*.json"):
    with open(file, "r", encoding="utf-8") as fileOpen:
        data = json.load(fileOpen)
        
        # List of chunks
        for chunk in data:
            documents.append({
                "id": f"{chunk['video_id']}_{chunk['start']}",
                "video_id": chunk["video_id"],
                "start": chunk["start"],
                "end": chunk["end"],
                "text": chunk["text"]
            })

print(f'Loaded {len(documents)} chunks!!')


# Create embeddings
def create_embeddings(documents):
    texts = []
    valid_docs = []

    # step-1 |  Remove empty text & extract text
    for doc in documents:
        if doc["text"].strip():
            texts.append(doc["text"])
            valid_docs.append(doc)

    # step-2 | Generate embeddings
    embeddings = emb_model.encode(texts, batch_size = 32, show_progress_bar=True)

    # step-3 | Attach embeddings back
    for i, doc in enumerate(valid_docs):
        doc["embedding"] = embeddings[i].tolist()
        # print(f' {documents[i].keys()} and {documents[i].values()}')

    return valid_docs

# Test
final_documents = create_embeddings(documents)
print(f' {documents[48].keys()} and {documents[48].values()}')