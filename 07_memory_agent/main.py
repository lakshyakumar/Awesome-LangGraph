import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4o-mini")

log_file_path = "./07_memory_agent/logging.txt"

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content)) 
    print("CURRENT STATE: ", Fore.MAGENTA ,  state["messages"] , Fore.RESET)

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

conversation_history = []

# Load conversation history from logging.txt if it exists
if os.path.exists(log_file_path):
    with open(log_file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("You:"):
                conversation_history.append(HumanMessage(content=line[4:].strip()))
            elif line.startswith("AI:"):
                conversation_history.append(AIMessage(content=line[3:].strip()))

try:
    user_input = input( "Enter: " + Fore.GREEN )
    while user_input != "exit":
        print(Fore.RESET)
        conversation_history.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": conversation_history})
        conversation_history = result["messages"]

        # Display AI response in yellow
        for message in conversation_history[-1:]:
            if isinstance(message, AIMessage):
                print(Fore.YELLOW + f"AI: {message.content}" + Fore.RESET)

        user_input = input( "Enter: " + Fore.GREEN)

except KeyboardInterrupt:
    print(Fore.RED + "\nExecution interrupted by user (Ctrl+C)." + Fore.RESET)
except Exception as e:
    print(Fore.RED + f"\nAn error occurred: {e}" + Fore.RESET)
finally:
    # Save conversation to a log file
    with open(log_file_path, "w") as file:
        file.write("Your Conversation Log:\n")
        for message in conversation_history:
            if isinstance(message, HumanMessage):
                file.write(f"You: {message.content}\n")
            elif isinstance(message, AIMessage):
                file.write(f"AI: {message.content}\n\n")
        file.write("End of Conversation")

    print(Fore.BLUE + "Conversation saved to logging.txt. Goodbye!" + Fore.RESET)
    
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")