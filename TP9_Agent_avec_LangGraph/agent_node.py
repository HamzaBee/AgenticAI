import os
from operator import add
from typing import Literal
from typing_extensions import TypedDict, Annotated

from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from tools_setup import model_with_tools, tools_by_name

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add]
    llm_calls: int

def llm_call(state: AgentState):
    """LLM decides whether to call tools or respond."""
    response = model_with_tools.invoke(
        [SystemMessage(content="You are a helpful assistant that solves arithmetic problems using tools when needed.")]
        + state["messages"]
    )
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

def tool_node(state: AgentState):
    """Execute tool calls from last AI message."""
    last = state["messages"][-1]
    results = []
    for call in last.tool_calls:
        tool = tools_by_name[call["name"]]

        observation = tool.invoke(call["args"])
        results.append(ToolMessage(
            content=str(observation),
            tool_call_id=call["id"]
        ))
    return {"messages": results}

def should_continue(state: AgentState) -> Literal["tool_node", END]:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None) and last.tool_calls:
        return "tool_node"
    return END

builder = StateGraph(AgentState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)

builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "llm_call")

agent = builder.compile()

if __name__ == "__main__":
    try:
        os.makedirs("ScreenshotsGraph", exist_ok=True)
        agent.get_graph().draw_mermaid_png(output_file_path="ScreenshotsGraph/agent_graph.png")
        print("Graph visualization saved to 'ScreenshotsGraph/agent_graph.png'")
    except Exception as e:
        print(f"[Warning] Could not save graph visualization: {e}")

    print("\n--- 1. Simple Invoke ---")
    result = agent.invoke({"messages": [HumanMessage(content="Add 3 and 4.")], "llm_calls": 0})
    print("\nState after execution:")
    print(result)
    print("\nPretty Printing Messages:")
    for m in result["messages"]:
        try:
            m.pretty_print()
        except Exception as ex:
            print(f"Error printing message: {ex}\n{m}")

    print("\n--- 2. Streaming Updates (State Deltas) ---")
    for chunk in agent.stream(
        {"messages": [HumanMessage(content="Multiply 30 and 43.")], "llm_calls": 0},
        stream_mode="updates"
    ):
        print(chunk)

    print("\n--- 3. Streaming Messages (Tokens) ---")
    for message_chunk, metadata in agent.stream(
        {"messages": [HumanMessage(content="Divide 30 and 43.")], "llm_calls": 0},
        stream_mode="messages"
    ):
        if getattr(message_chunk, "content", None):
            print(message_chunk.content, end="", flush=True)
    print()
