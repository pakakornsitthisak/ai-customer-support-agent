from app.knowledge import KNOWLEDGE_BASE


def test_knowledge_base_is_not_empty():
    assert len(KNOWLEDGE_BASE) > 0


def test_knowledge_base_has_required_fields():
    for item in KNOWLEDGE_BASE:
        assert "question" in item
        assert "answer" in item

        assert isinstance(item["question"], str)
        assert isinstance(item["answer"], str)

        assert item["question"].strip()
        assert item["answer"].strip()


def test_knowledge_base_contains_shipping_information():
    questions = [item["question"] for item in KNOWLEDGE_BASE]

    assert "How long does shipping take?" in questions
