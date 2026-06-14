import time
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import interrupt, Command

@task
def write_essay(topic: str) -> str:
    print(f"[Task] Drafting essay for topic: '{topic}'...")
    time.sleep(1)
    return f"This is an essay draft about '{topic}' (crafted with love)."

@entrypoint(checkpointer=InMemorySaver())
def workflow(topic: str) -> dict:
    draft = write_essay(topic).result()
    
    print(f"[Entrypoint] Interrupting workflow. Awaiting human validation for draft...")
    response = interrupt({
        "draft": draft,
        "action": "approve or reject the essay"
    })
    
    print(f"[Entrypoint] Resuming. Human response received: {response}")
    return {"draft": draft, "approved": response}

if __name__ == "__main__":
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("\n=== 1. Starting First Execution (Will interrupt) ===")
    first_run_interrupted = False
    
    for item in workflow.stream("cats", config):
        print("[Stream Output]:", item)
        if "__interrupt__" in item:
            first_run_interrupted = True
            
    print("\n--- Interrupt State ---")
    if first_run_interrupted:
        print("Workflow is suspended. Human feedback required.")
    else:
        print("Workflow completed without interruption.")

    print("\n=== 2. Resuming Execution with Approval (resume=True) ===")

    for item in workflow.stream(Command(resume=True), config):
        print("[Stream Output]:", item)
