````markdown
# AI Customer Support Agent

A full-stack AI customer support agent built with **Python, FastAPI, Ollama, RAG, tool calling, conversation memory, Next.js, TypeScript, Docker, and Docker Compose**.

The project demonstrates how to build an LLM-powered application that can understand user requests, select appropriate tools, retrieve information from a knowledge base, maintain conversation context, and expose the functionality through a REST API and web interface.

---

## Features

- LLM-powered customer support agent
- Local LLM inference using Ollama
- Tool calling
- Retrieval-Augmented Generation (RAG)
- Semantic search over a customer-support knowledge base
- Conversation memory using session IDs
- Mathematical calculation tool
- Current date/time tool
- Customer support knowledge-base search
- FastAPI REST API
- Next.js frontend
- Docker and Docker Compose
- Automated tests with pytest
- Agent evaluation for tool selection and answer quality

---

## Architecture

```text
                    ┌─────────────────────────┐
                    │     Next.js Frontend    │
                    │   React + TypeScript    │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP
                                 ▼
                    ┌─────────────────────────┐
                    │        FastAPI          │
                    │                         │
                    │ POST /chat              │
                    │ GET  /health            │
                    │ DELETE /sessions/{id}   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       LLM Agent         │
                    │         Ollama          │
                    │                         │
                    │ Tool Selection          │
                    │ Conversation Context    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┼─────────────┐
                    │            │             │
                    ▼            ▼             ▼
             ┌──────────┐ ┌───────────┐ ┌──────────────┐
             │ Calculate│ │ Current   │ │ Knowledge    │
             │  Tool    │ │ Time Tool │ │ Base / RAG   │
             └──────────┘ └───────────┘ └───────┬──────┘
                                               │
                                               ▼
                                      ┌────────────────┐
                                      │ Semantic Search│
                                      │ Support Data  │
                                      └────────────────┘

                         ┌─────────────────┐
                         │ Conversation    │
                         │ Memory          │
                         └─────────────────┘
````

---

## How It Works

When a user sends a message, the request follows this flow:

```text
User
 │
 ▼
Next.js Frontend
 │
 ▼
FastAPI /chat
 │
 ▼
LLM Agent
 │
 ├── calculate ───────────────► Mathematical result
 │
 ├── get_current_time ───────► Current local time
 │
 └── search_knowledge_base ──► Relevant support information
                                  │
                                  ▼
                              LLM response
                                  │
                                  ▼
                              User
```

The LLM determines which tool is appropriate based on the user's intent.

For example:

```text
User:
What is 125 * 48?

LLM:
Use calculate

Tool:
6000

Agent:
The result of 125 multiplied by 48 is 6000.
```

For a customer-support question:

```text
User:
What is your refund policy?

LLM:
Use search_knowledge_base

Knowledge Base:
Refund requests can be submitted within 30 days
of purchase.

Agent:
Refund requests can be submitted within 30 days
of purchase.
```

---

# RAG / Knowledge Base

The project uses Retrieval-Augmented Generation (RAG) for customer-support questions.

Instead of asking the LLM to generate company-specific information from its own knowledge, the agent first searches the company's knowledge base.

The retrieved information is then provided to the LLM so it can generate the final response.

```text
User Question
      │
      ▼
Semantic Search
      │
      ▼
Relevant Knowledge
      │
      ▼
LLM
      │
      ▼
Final Answer
```

The knowledge base contains customer-support information such as:

* Refund policies
* Shipping information
* Password reset instructions
* Other support policies

This reduces the risk of the model inventing company-specific information.

---

# Tool Calling

The agent has several tools available.

## 1. Calculate

Used for mathematical calculations.

Example:

```text
User:
Calculate 17.5 * 24.

Tool:
calculate

Result:
420.0
```

---

## 2. Current Time

Used when the user asks for the current date or time.

Example:

```text
User:
What time is it?

Tool:
get_current_time

Result:
2026-08-26 18:41:31 +07
```

---

## 3. Knowledge Base Search

Used for customer-support questions.

Example:

```text
User:
How long does shipping take?

Tool:
search_knowledge_base

Result:
Standard shipping usually takes 3-5 business days.
Express shipping usually takes 1-2 business days.
```

---

# Conversation Memory

The application supports multi-turn conversations using a `session_id`.

For example:

```text
User:
What is your refund policy?

Agent:
Refund requests can be submitted within 30 days of purchase.

User:
How long do I have to request it?

Agent:
You have 30 days from the date of purchase to request a refund.
```

The second question uses the conversation context to understand what **"it"** refers to.

Each conversation has its own session ID.

The frontend stores the session ID locally and sends it with each request.

Starting a new conversation creates a new session.

---

# Backend API

The backend is implemented with FastAPI.

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

---

## Chat

```http
POST /chat
```

Request:

```json
{
  "message": "What is your refund policy?",
  "session_id": "customer-session-123"
}
```

Response:

```json
{
  "answer": "Refund requests can be submitted within 30 days of purchase."
}
```

---

## Delete Session

```http
DELETE /sessions/{session_id}
```

Example:

```http
DELETE /sessions/customer-session-123
```

Response:

```json
{
  "session_id": "customer-session-123",
  "status": "cleared"
}
```

---

# Tech Stack

## Backend

* Python
* FastAPI
* Pydantic
* Ollama
* Llama 3.2
* pytest

## AI / ML

* Large Language Model (LLM)
* Retrieval-Augmented Generation (RAG)
* Semantic search
* Tool calling
* Conversation memory

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

## Infrastructure

* Docker
* Docker Compose

---

# Project Structure

```text
ai-customer-support-agent/
│
├── app/
│   ├── __init__.py
│   ├── llm.py
│   ├── memory.py
│   ├── knowledge.py
│   ├── knowledge_store.py
│   └── tools.py
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── evaluation/
│   ├── evaluate.py
│   └── questions.json
│
├── tests/
│   ├── test_llm.py
│   ├── test_memory.py
│   ├── test_tools.py
│   └── test_main.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── ChatInput.tsx
│   │   └── MessageBubble.tsx
│   │
│   ├── lib/
│   │   └── api.ts
│   │
│   ├── package.json
│   ├── Dockerfile
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

---

# Running Locally

## Prerequisites

Make sure you have:

* Python 3.13+
* Node.js
* Ollama
* Docker
* Docker Compose

---

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-customer-support-agent
```

---

## 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

---

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install and run Ollama

Make sure Ollama is installed and running.

Pull the model:

```bash
ollama pull llama3.2:latest
```

Verify:

```bash
ollama list
```

---

## 5. Start the backend

```bash
uvicorn api.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

## 6. Start the frontend

Go to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

---

# Running with Docker Compose

The project can also be run using Docker Compose.

From the project root:

```bash
docker compose up --build
```

Stop the services:

```bash
docker compose down
```

The services include:

```text
Frontend
    │
    ▼
Next.js

Backend
    │
    ▼
FastAPI
    │
    ▼
Ollama / LLM
```

---

# Testing

The project includes automated tests using pytest.

Run all tests:

```bash
pytest
```

The current test suite contains:

```text
30 passed
```

The tests cover areas such as:

* API endpoints
* Tool functions
* Conversation memory
* Application behavior

---

# Agent Evaluation

The project also includes a separate evaluation suite for measuring the agent's behavior.

Run:

```bash
python -m evaluation.evaluate
```

The evaluation measures two main areas:

### Tool Selection Accuracy

Whether the agent selected the correct tool.

Examples:

```text
"What is 125 * 48?"
        ↓
calculate
```

```text
"What time is it?"
        ↓
get_current_time
```

```text
"What is your refund policy?"
        ↓
search_knowledge_base
```

### Answer Quality

Whether the final response correctly answers the user's question based on the expected result.

The current evaluation achieved:

```text
Tool selection accuracy: 100%
Answer quality:          100%
```

---

# Example Conversation

```text
User:
What is your refund policy?

AI:
Refund requests can be submitted within 30 days of purchase.
Approved refunds are normally processed within 5-10 business days.

User:
How long do I have to request it?

AI:
You have 30 days from the date of purchase to request a refund.

User:
Does that apply to my order?

AI:
Based on our knowledge base, the 30-day refund window applies
to the order.
```

---

# Design Decisions

## Why use a local LLM?

Ollama allows the application to run an LLM locally without requiring an external LLM API for inference.

Benefits include:

* Local development
* No API key required for the LLM
* Lower external dependency
* Better control over the development environment

---

## Why use tools?

LLMs are not always the best component for deterministic operations.

For example, calculations should be performed by a deterministic function rather than relying on the model to calculate the result.

The same principle applies to retrieving the current time.

The LLM decides **which tool to use**, while the tool performs the actual operation.

---

## Why use RAG?

Company-specific information should come from a controlled knowledge source rather than the model's general training data.

RAG allows the system to retrieve relevant company information and provide it to the LLM as context.

---

## Why use session IDs?

Session IDs allow multiple conversations to maintain separate conversation histories.

For example:

```text
Session A
    └── Customer's refund conversation

Session B
    └── Customer's shipping conversation
```

This prevents conversations from different users or sessions from being mixed together.

---

# Error Handling

The application handles several failure scenarios, including:

* Failed tool execution
* Unknown tools
* Failed API requests
* Empty search results
* Knowledge-base retrieval failures
* Web-search failures
* Excessive tool-call iterations

The agent is instructed not to fabricate information when a tool fails.

---

# Limitations

This is a portfolio/demo project and is not intended to be a production customer-support platform.

Current limitations include:

* Local LLM inference
* Simple in-memory conversation storage
* Small knowledge base
* No authentication
* No user management
* No persistent production database
* No streaming responses
* No production monitoring
* No production-scale deployment

---

# Future Improvements

Possible future improvements include:

* Persistent conversation storage
* PostgreSQL or another production database
* Authentication and authorization
* Streaming LLM responses
* More sophisticated RAG pipelines
* Document ingestion pipeline
* Better retrieval and reranking
* Observability and monitoring
* Production cloud deployment
* Human-agent handoff
* Customer/order integrations

---

# What This Project Demonstrates

This project demonstrates practical experience with:

* Building LLM-powered applications
* LLM tool calling
* RAG architecture
* Semantic search
* Conversation memory
* Prompt engineering
* FastAPI
* REST APIs
* React / Next.js
* TypeScript
* Docker
* Docker Compose
* Automated testing
* AI agent evaluation
* Designing AI systems with deterministic tools

---

# License

This project is for portfolio and educational purposes.

````

### One important thing before you commit

I deliberately **did not describe the web search as a working feature**. We decided to move away from the unreliable `ddgs` online search and make the project primarily offline. That keeps the README honest.

Also, I would **not add more functionality now**. For your portfolio, the next step should be:

```text
README
  ↓
.gitignore check
  ↓
docker compose up --build
  ↓
pytest
  ↓
evaluation
  ↓
Git commit
  ↓
GitHub
  ↓
CV / portfolio
````

The project is at the point where polishing the documentation and publishing it gives you much more value than adding another feature.
