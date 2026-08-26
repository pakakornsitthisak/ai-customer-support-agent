from app.llm import generate_response
from app.memory import clear_history


session_id = "manual-test"

clear_history(session_id)


print("\n=== Question 1 ===")

answer = generate_response(
    "What is Python?",
    session_id=session_id,
)

print("Answer:", answer)


print("\n=== Question 2 ===")

answer = generate_response(
    "What is it mainly used for?",
    session_id=session_id,
)

print("Answer:", answer)


print("\n=== Question 3 ===")

answer = generate_response(
    "Calculate 25 * 4.",
    session_id=session_id,
)

print("Answer:", answer)
