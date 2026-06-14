# Agentic AI TPs

This repository contains various TPs (Travaux Pratiques) related to Agentic AI and Prompt Engineering.

## Structure
- `TP1_Prompt_Engineering/`: Introduction to prompting, tokenization, and multi-modal models.
- `TP2_Langchain/`: Building agents with LangChain, including tools, memory, and structured responses.
- `TP3-RAG/`: Implementing Retrieval-Augmented Generation (RAG) with PDFs and SQL agents.
- `TP4_MCP/`: Exploring Model Context Protocol (MCP) with local and distant servers.
- `TP5_LangGraph_Studio/`: Developing stateful agents using LangGraph Studio.
- `TP6_état_contexte/`: Managing state and context in AI agents.
- `TP_chef_personnel/`: Personal Chef Agent project.

## Environment
This workspace uses a shared Python environment at the root level.
- `pyproject.toml`: Dependency management via `uv`.
- `.env`: API keys (not committed).

## How to run
1. Ensure you have `uv` installed.
2. Run `uv sync` to set up the environment.
3. Activate the environment: `.venv\Scripts\activate` (Windows).
4. Run scripts from their respective folders, e.g.: `python TP1_Prompt_Engineering/01_tokenisation.py`
