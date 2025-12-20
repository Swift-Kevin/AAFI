# OpenAI Chatbot Assignment

## Description
A simple and lightweight chatbot designed to answer questions regarding Weather, Population, and search a simple knowledge base of information.

## Features
- Local Chat site with conversation states
- Calling built in tools:
  - `get_weather(city)`
  - `lookup_kb(query)`
  - `get_population(city)`
- Short-term memory (rolling conversation history)
- Message safety by filtering banned phrases/keywords
- Logging metrics: latency, tokens, estimated cost, and tool usage
- Light/Dark theme visual support for the local site

## Tech Stack
- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/) 0.123.5
- [Uvicorn](https://www.uvicorn.org/) 0.38.0
- [OpenAI Python SDK](https://pypi.org/project/openai/) 2.8.1
- [Pydantic](https://pydantic-docs.helpmanual.io/) 2.12.5

## Installation & Running
Option 1:
- Run the `StartChatbot.bat` script.

Option 2:
- At the directories location, run the command: `uvicorn app:app --reload`
- Open the localhost: http://127.0.0.1:8000