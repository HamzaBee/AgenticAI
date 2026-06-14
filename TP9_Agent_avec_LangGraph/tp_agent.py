import os
from operator import add
from typing import Literal
from typing_extensions import TypedDict, Annotated

from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.base import BaseStore
from langgraph.func import entrypoint

from tools_setup import model_with_tools, tools_by_name

@entrypoint()
def example_store_workflow(user_input: dict, *, store: BaseStore):
    return {"ok": True}

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

def should_continue(state: AgentState) -> Literal["approve", END]:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None) and last.tool_calls:
        return "approve"
    return END

def approve_node(state: AgentState) -> Command[Literal["tool_node", "__end__"]]:
    """Dynamically interrupt execution to ask for human approval."""
    decision = interrupt({
        "question": "Approve tool execution?",
        "tool_calls": state["messages"][-1].tool_calls
    })
    return Command(goto="tool_node" if decision else END)

builder = StateGraph(AgentState)
builder.add_node("llm_call", llm_call)
builder.add_node("approve", approve_node)
builder.add_node("tool_node", tool_node)

checkpointer = InMemorySaver()
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, ["approve", END])
builder.add_edge("tool_node", "llm_call")

agent = builder.compile(checkpointer=checkpointer)
agent_studio = builder.compile()  # Compiled without custom checkpointer for LangGraph Studio compatibility

if __name__ == "__main__":
    try:
        os.makedirs("ScreenshotsGraph", exist_ok=True)
        agent.get_graph().draw_mermaid_png(output_file_path="ScreenshotsGraph/tp_agent_graph.png")
        print("Graph visualization saved to 'ScreenshotsGraph/tp_agent_graph.png'")
    except Exception as e:
        print(f"[Warning] Could not save graph visualization: {e}")


    print("\n================== 1. RUN WITH APPROVAL ==================")
    config = {"configurable": {"thread_id": "thread-1"}}
    
    result = agent.invoke(
        {"messages": [HumanMessage(content="Add 3 and 4.")], "llm_calls": 0},
        config=config
    )

    if "__interrupt__" in result and result["__interrupt__"]:
        print("Interrupt payload:", result["__interrupt__"][0].value)
        
        resume = agent.invoke(Command(resume=True), config=config)
        print("Done. Last message:")
        resume["messages"][-1].pretty_print()
    else:
        print("No interrupt triggered. Final message:")
        result["messages"][-1].pretty_print()


    print("\n================== 2. RUN WITH REJECTION ==================")
    config_reject = {"configurable": {"thread_id": "thread-1-reject"}}
    
    result_reject = agent.invoke(
        {"messages": [HumanMessage(content="Multiply 30 and 41.")], "llm_calls": 0},
        config=config_reject
    )
    
    if "__interrupt__" in result_reject and result_reject["__interrupt__"]:
        print("Interrupt payload:", result_reject["__interrupt__"][0].value)

        resume_reject = agent.invoke(Command(resume=False), config=config_reject)
        print("Done. Last message:")
        resume_reject["messages"][-1].pretty_print()
    else:
        print("No interrupt triggered.")


    print("\n================== 3. STATE FORKING & TIME TRAVEL ==================")
    history = list(agent.get_state_history(config_reject))
    print(f"Number of checkpoints in reject thread: {len(history)}")
    
    for idx, snap in enumerate(history):
        print(f"  Checkpoint {idx}: id={snap.config['configurable'].get('checkpoint_id')}, next={snap.next}")
    
    picked = history[1]
    print(f"\nPicked checkpoint ID: {picked.config['configurable']['checkpoint_id']} (next node to run: {picked.next})")
    
    new_config = agent.update_state(
        picked.config,
        values={
            "messages": [HumanMessage(content="Multiply 30 and 41.")], 
            "llm_calls": 0
        }
    )
    
    forked = agent.invoke(None, new_config)
    print("\nForked Execution Completed! Messages in final state:")
    for msg in forked["messages"]:
        try:
            msg.pretty_print()
        except Exception as e:
            print(msg)
