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
            "local_server": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [SERVER_SCRIPT],
                "cwd": SCRIPT_DIR,
                "env": dict(os.environ),
            }
        }
    )
    # get tools
    tools = await client.get_tools()
    print(f"Tools disponibles : {[t.name for t in tools]}")

    # get resources
    resources = await client.get_resources("local_server")
    print(f"Resources disponibles : {resources}")

    # get prompt
    prompt_messages = await client.get_prompt("local_server", "prompt")
    prompt_text = prompt_messages[0].content if prompt_messages else ""

    # Initialiser le modèle Ollama
    model = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt_text
    )

    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="Tell me about the langchain-mcp-adapters library")]},
        config=config
    )

    print(response['messages'][-1].content)


asyncio.run(main())