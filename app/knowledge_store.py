from sentence_transformers import SentenceTransformer

from app.knowledge import KNOWLEDGE_BASE


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

SIMILARITY_THRESHOLD = 0.45


def search_knowledge_base(
    query: str,
    top_k: int = 2,
) -> list[dict]:
    """Search the support knowledge base using semantic similarity."""

    query_embedding = model.encode(query)

    documents = [item["question"] for item in KNOWLEDGE_BASE]

    document_embeddings = model.encode(documents)

    similarities = model.similarity(
        query_embedding,
        document_embeddings,
    )[0]

    ranked_indices = similarities.argsort(descending=True)

    results = []

    for index in ranked_indices:
        score = float(similarities[index])

        # Stop considering results that are not relevant.
        if score < SIMILARITY_THRESHOLD:
            break

        item = KNOWLEDGE_BASE[int(index)]

        results.append(
            {
                "question": item["question"],
                "answer": item["answer"],
                "score": score,
            }
        )

        if len(results) >= top_k:
            break

    return results
