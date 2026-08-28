import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, MatchAny, PayloadSchemaType
from groq import Groq

from embedding import final_documents


# Load variables from env
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(
    url = QDRANT_URL,
    api_key = QDRANT_API_KEY
)

print("------ Successfully connected to Qdrant cloud! -------------")

# Create Qdrant collection & Index
COLLECTION_NAME = "striver_dsa"
EMBEDDING_SIZE = 384

def create_collection_index(COLLECTION_NAME: str, recreate: bool = False):
    if recreate and qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.delete_collection(COLLECTION_NAME)

    qdrant_client.create_collection(
        collection_name = COLLECTION_NAME,
        vectors_config = VectorParams(
            size = EMBEDDING_SIZE,
            distance = Distance.COSINE
        ),
    )
    print(f'Created collection name: {COLLECTION_NAME}')
    print(f'Embedding size: {EMBEDDING_SIZE}')
    print(f'Distance/algorithm: COSINE')

    # create index
    qdrant_client.create_payload_index(
        collection_name = COLLECTION_NAME,
        field_name = "video_id",
        field_schema = PayloadSchemaType.KEYWORD
    )

# Create Qdrant points through embeddings
def generate_points(final_documents):
    created_points = []
    print("inside generated points")
    for doc in final_documents:
        point = PointStruct(
            id=doc["id"],
            vector=doc["embedding"],
            payload={
                "text": doc["text"],
                "video_id": doc["video_id"],
                "start": doc["start"],
                "end": doc["end"]
            }
        )
        created_points.append(point)

    print("points has been generated.....................")
    qdrant_client.upsert(
        collection_name = COLLECTION_NAME,
        points = created_points
        )
    
    print(f'Uploaded {len(created_points)} documents to Qdrant cloud!')

    return created_points

# Test    
create_collection_index(COLLECTION_NAME, True)
generate_points(final_documents)

