from app.knowledge_store import search_knowledge_base


def test_search_knowledge_base_finds_shipping():
    results = search_knowledge_base("How long does shipping take?")

    assert len(results) > 0

    assert results[0]["question"] == "How long does shipping take?"


def test_search_knowledge_base_finds_semantically_similar_question():
    results = search_knowledge_base("When will my package arrive?")

    assert len(results) > 0

    assert results[0]["question"] == "How long does shipping take?"


def test_search_knowledge_base_rejects_unrelated_question():
    results = search_knowledge_base("How do I cook pasta?")

    assert results == []
