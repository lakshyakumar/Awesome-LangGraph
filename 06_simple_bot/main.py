from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv # used to store secret stuff like API keys or configuration values
from colorama import Fore 

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatOpenAI(model="gpt-4o")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print("\nAI:" + Fore.YELLOW + f" {response.content}" + Fore.RESET)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()


try:
    user_input = input("Enter: " + Fore.GREEN)
    while user_input != "exit":
        print(Fore.RESET)
        result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
        user_input = input("Enter: " + Fore.GREEN)
except KeyboardInterrupt:
    print(Fore.RED + "\nExecution interrupted by user (Ctrl+C)." + Fore.RESET)
except Exception as e:
    print(Fore.RED + f"\nAn error occurred: {e}" + Fore.RESET)
finally:
    print(Fore.BLUE + "Exiting the program. Goodbye!" + Fore.RESET)