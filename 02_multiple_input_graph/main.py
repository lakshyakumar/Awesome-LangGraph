from typing import TypedDict, List
from langgraph.graph import StateGraph 


class AgentState(TypedDict):
    values: List[int]
    name: str 
    result: str 
    
def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    # print(state)
    state["result"] = f"Hi there {state["name"]}! Your sum = {sum(state["values"])}"
    # print(state)
    return state

graph = StateGraph(AgentState)
graph.add_node("processor", process_values)
graph.set_entry_point("processor") # Set the starting node
graph.set_finish_point("processor") # Set the ending node
app = graph.compile() # Compiling the graph


answers = app.invoke({"values": [1,2,3,4], "name": "Steve"})
print(answers["result"])