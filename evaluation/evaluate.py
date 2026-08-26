import json
from pathlib import Path

import ollama

from app.llm import generate_response


MODEL = "llama3.2:latest"
QUESTIONS_FILE = Path("evaluation/questions.json")


def load_questions() -> list[dict]:
    with open(QUESTIONS_FILE) as file:
        return json.load(file)


def judge_answer(
    question: str,
    expected_answer: str | None,
    actual_answer: str,
) -> bool:
    """Use the local LLM to judge whether an answer is correct."""

    if expected_answer is None:
        return True

    prompt = f"""
You are evaluating an AI customer support agent.

Question:
{question}

Expected answer:
{expected_answer}

Agent answer:
{actual_answer}

Determine whether the agent answer is factually correct.

Important rules:
- Judge the meaning, not the exact wording.
- Numerically equivalent values are considered correct.
- For example, 420 and 420.0 are the same value.
- Different wording is acceptable if the underlying answer is correct.
- Do not require the agent to use the exact same sentence as the expected answer.

Respond with exactly one word:
PASS
or
FAIL
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    judgment = response.message.content.strip().upper()

    return judgment.startswith("PASS")


def evaluate_single_question(
    index: int,
    item: dict,
) -> tuple[int, int]:
    """Evaluate one single-turn question."""

    question = item["question"]
    expected_tool = item["expected_tool"]
    expected_answer = item.get("expected_answer")

    tool_history = []

    print(f"\n[{index}] {question}")
    print(f"Expected tool: {expected_tool}")

    answer = generate_response(
        message=question,
        session_id=f"evaluation-{index}",
        tool_history=tool_history,
    )

    actual_tool = tool_history[0] if tool_history else None

    print(f"Actual tool:   {actual_tool}")
    print(f"Answer:        {answer}")

    # Tool selection
    tool_pass = actual_tool == expected_tool

    if tool_pass:
        print("Tool selection: PASS")
    else:
        print("Tool selection: FAIL")

    # Answer quality
    answer_pass = judge_answer(
        question=question,
        expected_answer=expected_answer,
        actual_answer=answer,
    )

    if answer_pass:
        print("Answer quality:  PASS")
    else:
        print("Answer quality:  FAIL")

    return int(tool_pass), int(answer_pass)


def evaluate_conversation(
    index: int,
    conversation: dict,
) -> tuple[int, int]:
    """Evaluate a multi-turn conversation."""

    session_id = conversation["session_id"]
    messages = conversation["messages"]

    print(f"\n[{index}] Multi-turn conversation")
    print(f"Session: {session_id}")

    tool_correct = 0
    answer_correct = 0

    for turn, item in enumerate(messages, start=1):
        question = item["question"]
        expected_tool = item["expected_tool"]
        expected_answer = item.get("expected_answer")

        tool_history = []

        print(f"\n  Turn {turn}: {question}")
        print(f"  Expected tool: {expected_tool}")

        answer = generate_response(
            message=question,
            session_id=session_id,
            tool_history=tool_history,
        )

        actual_tool = tool_history[0] if tool_history else None

        print(f"  Actual tool:   {actual_tool}")
        print(f"  Answer:        {answer}")

        # Tool selection
        tool_pass = actual_tool == expected_tool

        if tool_pass:
            tool_correct += 1
            print("  Tool selection: PASS")
        else:
            print("  Tool selection: FAIL")

        # Answer quality
        answer_pass = judge_answer(
            question=question,
            expected_answer=expected_answer,
            actual_answer=answer,
        )

        if answer_pass:
            answer_correct += 1
            print("  Answer quality:  PASS")
        else:
            print("  Answer quality:  FAIL")

    return tool_correct, answer_correct


def main() -> None:
    questions = load_questions()

    tool_correct = 0
    answer_correct = 0

    total_questions = 0

    print("=" * 60)
    print("AI CUSTOMER SUPPORT AGENT EVALUATION")
    print("=" * 60)

    for index, item in enumerate(questions, start=1):
        if item.get("type") == "conversation":
            conversation_tool_correct, conversation_answer_correct = (
                evaluate_conversation(
                    index=index,
                    conversation=item,
                )
            )

            tool_correct += conversation_tool_correct
            answer_correct += conversation_answer_correct
            total_questions += len(item["messages"])

        else:
            single_tool_correct, single_answer_correct = evaluate_single_question(
                index=index,
                item=item,
            )

            tool_correct += single_tool_correct
            answer_correct += single_answer_correct
            total_questions += 1

    tool_accuracy = tool_correct / total_questions * 100
    answer_accuracy = answer_correct / total_questions * 100

    print("\n" + "=" * 60)
    print(
        f"Tool selection accuracy: "
        f"{tool_correct}/{total_questions} "
        f"({tool_accuracy:.1f}%)"
    )
    print(
        f"Answer quality:          "
        f"{answer_correct}/{total_questions} "
        f"({answer_accuracy:.1f}%)"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
