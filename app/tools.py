from datetime import datetime

from app.knowledge_store import search_knowledge_base as semantic_search


def search_knowledge_base(query: str) -> str:
    """Search the local customer support knowledge base."""

    results = semantic_search(
        query=query,
        top_k=2,
    )

    if not results:
        return (
            "KNOWLEDGE_BASE_NO_RESULTS: "
            "No relevant information was found in the knowledge base."
        )

    output = []

    for index, result in enumerate(results, start=1):
        output.append(
            f"[{index}]\n"
            f"Question: {result['question']}\n"
            f"Answer: {result['answer']}\n"
            f"Similarity: {result['score']:.4f}"
        )

    return "\n\n".join(output)


def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""

    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception:
        return "Unable to calculate the expression."


def get_current_time() -> str:
    """Return the current local date and time."""

    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


TOOLS = {
    "calculate": calculate,
    "get_current_time": get_current_time,
    "search_knowledge_base": search_knowledge_base,
}
