import os

import ollama

from app.memory import add_message, get_history
from app.tools import TOOLS


MODEL = "llama3.2:latest"

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

ollama_client = ollama.Client(
    host=OLLAMA_HOST,
)

MAX_TOOL_ITERATIONS = 5


SYSTEM_PROMPT = """
You are an AI customer support agent.

You have access to conversation history and tools.

Important instructions:

- Use the conversation history to understand follow-up questions.
- Resolve pronouns and references such as "it", "its", "they", "that",
  and "the previous one" using the conversation context.
- When a user asks a follow-up question, preserve the topic from the
  previous conversation unless the user clearly changes the topic.
- Choose the tool that best matches the user's actual intent.

Tool selection rules:

- Use search_knowledge_base for questions about company policies,
  shipping, refunds, orders, passwords, and customer support information.
- Use search_web for current, recent, latest, or external information.
- Use calculate for mathematical calculations.
- Use get_current_time for the current date or time.
- If a follow-up question refers to information previously searched on
  the web, continue using search_web unless the user clearly changes
  the topic to company-specific support information.

Knowledge base follow-up rules:

- If a follow-up question refers to a previous company policy,
  product, order, shipping, refund, password, or support answer,
  use search_knowledge_base again.
- Resolve references such as "it", "that", "the order", or
  "the previous one" using conversation history before searching.
- The knowledge base result is the source of truth for company-specific
  information.
- Do not use the current date to infer or calculate company policy
  deadlines unless the knowledge base explicitly requires such a calculation.
- Do not invent additional conditions or assumptions that are not present
  in the knowledge base.

Tool result rules:

- Use the information returned by tools as the source of truth.
- Do not invent facts that are not supported by the tool results.
- If a tool reports that no results were found or that the search failed,
  clearly tell the user that the search was unsuccessful.
- Do not pretend that you found information when the tool returned no
  useful results.

Web search failure rules:

- If search_web returns WEB_SEARCH_FAILED or WEB_SEARCH_NO_RESULTS,
  do not invent, guess, or use outdated knowledge as if it were current.
- Clearly tell the user that current web information could not be retrieved.
- Do not claim that you successfully searched the web when the tool failed.
- If the user asks a follow-up question about a previous web search,
  use the previous conversation context to understand the topic.
- If the follow-up requires current information, call search_web again.

Do not use search_web when the answer can be obtained from the
company knowledge base.
"""

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": ("Calculate a mathematical expression."),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A mathematical expression such as 25 * 4 or 100 / 8."
                        ),
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": ("Get the current local date and time."),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": (
                "Search the local customer support knowledge base "
                "for company-specific information about products, "
                "orders, shipping, refunds, returns, passwords, "
                "accounts, and customer support policies."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": ("The customer's customer-support question."),
                    }
                },
                "required": ["query"],
            },
        },
    },
]


def generate_response(
    message: str,
    session_id: str = "default",
    tool_history: list[str] | None = None,
) -> str:
    """Generate a response using the local LLM, tools, and memory."""

    # --------------------------------------------------
    # Load conversation history
    # --------------------------------------------------

    history = get_history(session_id)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    # --------------------------------------------------
    # Agent tool loop
    # --------------------------------------------------

    for _ in range(MAX_TOOL_ITERATIONS):
        response = ollama_client.chat(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
        )

        # --------------------------------------------------
        # No tool required
        # --------------------------------------------------

        if not response.message.tool_calls:
            final_answer = response.message.content.strip()

            add_message(
                session_id,
                "user",
                message,
            )

            add_message(
                session_id,
                "assistant",
                final_answer,
            )

            return final_answer

        # --------------------------------------------------
        # LLM requested one or more tools
        # --------------------------------------------------

        messages.append(response.message)

        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            # Record tool usage for evaluation.
            if tool_history is not None:
                tool_history.append(tool_name)

            tool = TOOLS.get(tool_name)

            # --------------------------------------------------
            # Unknown tool
            # --------------------------------------------------

            if tool is None:
                result = f"TOOL_ERROR: Unknown tool '{tool_name}'."

            # --------------------------------------------------
            # Execute tool
            # --------------------------------------------------

            else:
                try:
                    result = tool(**arguments)

                except Exception as e:
                    result = f"TOOL_ERROR: {e}"

            # --------------------------------------------------
            # Debug output
            # --------------------------------------------------

            print(f"Tool: {tool_name}")
            print(f"Arguments: {arguments}")
            print(f"Result: {result}")

            # --------------------------------------------------
            # Knowledge-base failure handling
            # --------------------------------------------------

            if tool_name == "search_knowledge_base" and (
                str(result).startswith("KNOWLEDGE_BASE_NO_RESULTS:")
                or str(result).startswith("TOOL_ERROR:")
            ):
                final_answer = (
                    "I couldn't find relevant information "
                    "in the customer support knowledge base."
                )

                add_message(
                    session_id,
                    "user",
                    message,
                )

                add_message(
                    session_id,
                    "assistant",
                    final_answer,
                )

                return final_answer

            # --------------------------------------------------
            # Send tool result back to the LLM
            # --------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "content": str(result),
                }
            )

    # --------------------------------------------------
    # Tool iteration safety limit
    # --------------------------------------------------

    answer = (
        "I was unable to complete the request because the tool-call limit was reached."
    )

    add_message(
        session_id,
        "user",
        message,
    )

    add_message(
        session_id,
        "assistant",
        answer,
    )

    return answer
