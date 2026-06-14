import asyncio
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
import os
import sys

# Resolve the path to mcp_local_server.py relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPT = os.path.join(SCRIPT_DIR, "mcp_local_server.py")


async def main():
    client = MultiServerMCPClient(
        {
            "time": {
                "transport": "stdio",
                "command": "mcp-server-time",
                "args": [
                    "--local-timezone=Africa/Casablanca"
                ]
            }
        }
    )
    # get tools
    tools = await client.get_tools()
    print(f"Tools disponibles : {[t.name for t in tools]}")

    # Initialiser le modèle Ollama
    model = ChatOllama(
        model="llama3.2:3b",
    )

    agent = create_agent(
        model=model,
        tools=tools,
    )

    question = HumanMessage(content="What time is it in Japan")

    response = await agent.ainvoke(
        {"messages": [question]}
    )

    print(response['messages'][-1].content)


asyncio.run(main())