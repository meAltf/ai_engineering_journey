# ============================================================
# PART 1 — IMPORTS AND ENVIRONMENT
# ============================================================

import os
import json

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
)

from sentence_transformers import SentenceTransformer
from groq import Groq

from prompts import prompt_askllm, prompt_precision, prompt_recall, prompt_faithfullness, prompt_relevancy, prompt_correctness

# ============================================================
# PART 2 — LOAD ENVIRONMENT
# ============================================================

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

open_ai_gpt_model = "openai/gpt-oss-120b"
embedding_model = "all-MiniLM-L6-v2"

# ============================================================
# PART 3 — CONNECT TO QDRANT
# ============================================================

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)
print("Connected to Qdrant Cloud!")


# ============================================================
# PART 4 — CREATE QDRANT COLLECTION
# ============================================================

COLLECTION_NAME = "rag_evaluation"
EMBEDDING_SIZE = 384


if client.collection_exists(COLLECTION_NAME):
    print( f"Deleting existing collection: {COLLECTION_NAME}" )
    client.delete_collection( COLLECTION_NAME )

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams( size=EMBEDDING_SIZE, distance=Distance.COSINE )
)

print(f"Created collection: {COLLECTION_NAME}")


# ============================================================
# PART 5 — CREATE CATEGORY INDEX
# ============================================================

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)


# ============================================================
# PART 6 — LOAD KNOWLEDGE
# ============================================================

with open( "knowledge.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

print( f"Loaded {len(documents)} knowledge documents." )


# ============================================================
# PART 7 — CREATE EMBEDDINGS
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer(embedding_model)
print("Embedding model ready!")


texts = [ document["text"] for document in documents ]
embeddings = model.encode( texts )

print(f"Generated {len(embeddings)} embeddings.")
print(f"Embedding size: {len(embeddings[0])}")


# ============================================================
# PART 8 — CREATE QDRANT POINTS
# ============================================================

points = []
for i in range(len(documents)):
    point = PointStruct(
        id=i + 1,
        vector=embeddings[i].tolist(),
        payload=documents[i]
    )
    points.append(point)


# ============================================================
# PART 9 — UPLOAD KNOWLEDGE TO QDRANT
# ============================================================

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)
print(f"Uploaded {len(points)} documents to Qdrant!")


# ============================================================
# PART 10 — SEARCH QDRANT
# ============================================================

def search(question, top_k=3):
    query_vector = embedding_model.encode(question).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    ).points

    return results

# ============================================================
# PART 11 — CONNECT TO GROQ
# ============================================================

groq_client = Groq( api_key=GROQ_API_KEY )

# ============================================================
# PART 12 — ASK THE LLM
# ============================================================

def ask_llm(question, context):

    prompt = prompt_askllm(question, context)
    response = groq_client.chat.completions.create(
        model=open_ai_gpt_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


# ============================================================
# PART 13 — GOLDEN DATASET
# Questions for which we know the correct answer.
# ============================================================
from golden_dataset import golden_dataset

# ============================================================
# PART 14 — LLM AS A JUDGE | to judge the received response
# ============================================================

def llm_judge(prompt):

    response = groq_client.chat.completions.create(
        model=open_ai_gpt_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0
    )

    return json.loads(
        response.choices[0].message.content
    )


# ============================================================
# PART 15 — CONTEXT PRECISION
# For every retrieved chunk, ask: "Is this chunk relevant to the question?"
# Precision = relevant retrieved chunks / total retrieved chunks
# ============================================================

def context_precision( question, retrieved_docs ):

    relevant_chunks = 0
    for i, doc in enumerate( retrieved_docs ):
        chunk = doc.payload["text"]

        prompt = prompt_precision(question)

        result = llm_judge(prompt)
        if result["relevant"]:
            relevant_chunks += 1

    if len(retrieved_docs) == 0:
        return 0.0

    return ( relevant_chunks / len(retrieved_docs)
    )


# ============================================================
# PART 16 — CONTEXT RECALL
# Did we retrieve the information needed to answer the question?
# ============================================================

def context_recall( question, context, ground_truth ):
    prompt = prompt_recall(question, ground_truth, context)
    result = llm_judge( prompt )
    return result


# ============================================================
# PART 17 — FAITHFULNESS
# Is the generated answer supported by the retrieved context?
# ============================================================

def evaluate_faithfulness( question, context, answer ):
    prompt = prompt_faithfullness(question, context, answer)
    return llm_judge( prompt )


# ============================================================
# PART 18 — ANSWER RELEVANCY
# ============================================================

def evaluate_relevancy( question, answer ):
    prompt = prompt_relevancy(question, answer)
    return llm_judge( prompt )


# ============================================================
# PART 19 — ANSWER CORRECTNESS
# ============================================================

def evaluate_correctness( answer, ground_truth ):
    prompt = prompt_correctness(answer, ground_truth)
    return llm_judge( prompt )


# ============================================================
# PART 20 — RUN COMPLETE EVALUATION
# ============================================================

def run_evaluation():

    print("\n")
    print("=" * 70)
    print("RAG EVALUATION")
    print("=" * 70)

    all_scores = {
        "precision": [],
        "recall": [],
        "faithfulness": [],
        "relevancy": [],
        "correctness": []
    }


    # ========================================================
    # RUN EVERY GOLDEN QUESTION THROUGH THE REAL RAG
    # ========================================================

    for test in golden_dataset:
        question = test["question"]

        print("\n")
        print("-" * 70)
        print( f"QUESTION: {question}" )

        # Retrieval
        results = search( question, top_k=3 )

        # Retrieved documents
        print("\nRetrieved Documents:")
        for i, result in enumerate( results ):
            print(  f"\nChunk {i + 1}" )
            print( f"Score: {result.score:.3f}")
            print( result.payload["text"])

        # create context
        context = "\n".join(
            result.payload["text"]
            for result in results
        )

        # generate answer
        answer = ask_llm( question, context)
        print("\nGenerated Answer:")
        print(answer)

        # metric-1 | context precision
        precision = context_precision( question, results)

        # metric-2 | context recall
        recall_result = context_recall( question, context, test["ground_truth"])
        recall = float( recall_result["score"])

        # metric-3 | faithfullness
        faithfulness_result = ( evaluate_faithfulness( question, context, answer))
        faithfulness = float( faithfulness_result["score"])

        # metric-4 | answer relevancy
        relevancy_result = evaluate_relevancy(question, answer)
        relevancy = float(relevancy_result["score"])

        # metric-5 | correctness
        correctness_result = (evaluate_correctness( answer, test["ground_truth"]))
        correctness = float(correctness_result["score"])

        # save scores
        all_scores["precision"].append(precision)
        all_scores["recall"].append(recall)
        all_scores["faithfulness"].append(faithfulness)
        all_scores["relevancy"].append(relevancy)
        all_scores["correctness"].append(correctness)

        # print scores
        print("\nScores")
        print(f"Context Precision : {precision:.2f}")
        print(f"Context Recall    : {recall:.2f}")
        print(f"Faithfulness      : {faithfulness:.2f}")
        print(f"Answer Relevancy  : {relevancy:.2f}")
        print(f"Answer Correctness: {correctness:.2f}")

        # Final checklist
        print("\nDiagnosis")
        if precision < 0.7:
            print("❌ Retrieval is returning irrelevant chunks.")

        if recall < 0.7:
            print("❌ Retrieval is missing important information.")

        if faithfulness < 0.7:
            print("❌ Answer is not properly grounded.")

        if relevancy < 0.7:
            print("❌ Answer is not sufficiently relevant.")

        if correctness < 0.7:
            print("❌ Answer is not sufficiently correct.")

        if ( precision >= 0.7 and recall >= 0.7 and faithfulness >= 0.7 and relevancy >= 0.7 and correctness >= 0.7):
            print("✅ Good RAG response.")


    # Final summary:
    print("\n")
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    for metric, values in all_scores.items():
        average = (sum(values)/len(values))
        print(f"{metric.capitalize():20}: {average:.2f}")

if __name__ == "__main__":

    run_evaluation()