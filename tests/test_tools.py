from app.tools import (
    calculate,
    get_current_time,
    search_knowledge_base,
)


def test_calculate():
    assert calculate("125 * 48") == "6000"


def test_calculate_decimal():
    assert calculate("17.5 * 24") == "420.0"


def test_calculate_division():
    assert calculate("1000 / 8") == "125.0"


def test_calculate_invalid_expression():
    result = calculate("invalid expression")

    assert result == "Unable to calculate the expression."


def test_get_current_time():
    result = get_current_time()

    assert isinstance(result, str)
    assert len(result) > 0


def test_search_knowledge_base_refund():
    result = search_knowledge_base("What is the refund policy?")

    assert "30 days" in result
    assert "5-10 business days" in result


def test_search_knowledge_base_shipping():
    result = search_knowledge_base("How long does shipping take?")

    assert "3-5 business days" in result
    assert "1-2 business days" in result


def test_search_knowledge_base_password():
    result = search_knowledge_base("How can I reset my password?")

    assert "Forgot password" in result
