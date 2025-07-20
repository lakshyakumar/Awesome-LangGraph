from dotenv import load_dotenv

_ = load_dotenv(override=True)  # Ensure environment variables are loaded

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from tavily import TavilyClient
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from colorama import Fore

class Queries(BaseModel):
    queries: List[str]
    
class AgentState(TypedDict):
    task: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    revision_number: int
    max_revisions: int
    messages: Annotated[list[AnyMessage], operator.add] 
    
class PromptManager:
    # Static variables for prompts
    PLANNER_PROMPT = "You are an expert Business Analyst who are tasked to write a high level outline of a market research for an Idea and competitor analysis. \
                     Write such an outline for the user provided idea. Give an outline of the report along with any relevant notes or instructions for the sections. \
                     Title of the  report can be the problem statement.\\Include leanstack section as well to come up with  the below sections  \n\
                         **Top Problem existed in the domain with existing alternatives**\n \
                         **Targeted Customer Segments and early adopters.**\n \
                         **Unique Value Proposition (UVP) or Unique Selling Point (USP), single, clear, compelling that turns an unaware visitor into an interested prospect.**\n \
                         **Solution Overview.**\n \
                         **Unfair Advantage or Competitive Edge, something that cannot be copied.**\n \
                         **Revenue streams**\n \
                         **Cost Structure, with fixed and variable costs**\n \
                         **Key Metrics, how you measure success**\n \
                         **Channels, how you reach your customers**\n \
                         **Current Gaps in market** \n \
                         **Similar Ideas** \n \
                     here are the critique for previous draft:\n ----- \n {critique}, \
                     try to incorporate points by critique in the plan to get better score in the next draft.\
                         make sure to pivot user Idea if needed to make it more viable."
    RESEARCHER_PROMPT = "You are a market trends researcher charged with providing information that can \
        be used when writing the following report for Idea viability. Generate a list of search queries that will gather \
        any relevant information on market trends and competitors. Only generate 20 queries max."
    WRITER_PROMPT = "You are an essay assistant tasked with writing excellent report. Generate the best market and competitor analysis possible for the user's request and the initial outline. \
        If the user provides critique, respond with a revised version of your previous attempts. Utilize all the information below as needed: \n------\n {content}"
    REFLECTION_PROMPT = "You are an seasoned CEO grading written draft based on an Idea. \
        Generate critique and recommendations for the report and its direction. \
        Provide detailed recommendations, including requests for length, depth, style, etc.\
        give a score from 1 to 10 for the draft and provide a detailed explanation of the score."


tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
# tavily = TavilySearchResults(max_results=5)  # Reduced number of results for simplicity
model = ChatOpenAI(model="gpt-4o", temperature=0)
 
    
class Agent:
    def __init__(self, model, tools, system=""):
        try:
            self.system = system
            builder = StateGraph(AgentState)
            builder.add_node("planner", self.plan)
            builder.add_node("researcher", self.research)
            builder.add_node("writer", self.write)
            builder.add_node("reflector", self.reflect)
            builder.set_entry_point("planner")
            builder.add_conditional_edges(
                "reflector", 
                self.should_continue, 
                {
                    False:END,
                    True: "planner",
                }
            )
            builder.add_edge("planner", "researcher")
            builder.add_edge("researcher", "writer")
            builder.add_edge("writer", "reflector")
            # self.tools = {t.name: t for t in tools}
            self.model = model
            # self.model = model.bind_tools(tools)
            self.graph = builder.compile()
        except Exception as e:
            print(Fore.RED + f"Error initializing agent: {e}")
            print(Fore.RESET)
    def should_continue(self,state: AgentState) -> bool:
        if state['revision_number'] >= state['max_revisions']:
            print(Fore.RED + "Max revisions reached. Ending process."+ Fore.RESET)
            return False
        return True
    
    def plan(self,state: AgentState):
        messages = [
            SystemMessage(content=PromptManager.PLANNER_PROMPT.format(critique=state.get('critique', ''))),
            HumanMessage(content=state['task'])
        ]
        response = self.model.invoke(messages)
        print("Planning node: \n" + Fore.YELLOW + response.content + Fore.RESET)
        return {'plan': response.content}
    
    def research(self,state: AgentState):
        queries = self.model.with_structured_output(Queries).invoke([
            SystemMessage(content=PromptManager.RESEARCHER_PROMPT + "\n\n" + state['critique']),
            HumanMessage(content=state['task'])
        ])
        print("Researching plan node: ", Fore.YELLOW + "Queries: " + str(queries.queries) + Fore.RESET)
        content = state.get('content', [])
        for q in queries.queries:
            response = tavily.search(query=q, max_results=2)
            for r in response['results']:
                content.append(r['content'])
        return {"content": content}
    
    def write(self,state: AgentState):
        content = "\n\n".join(state['content'] or [])
        user_message = HumanMessage(
            content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']} \n\n Here is the critique of the previous draft:\n\n{state['critique']}")
        messages = [
            SystemMessage(
                content=PromptManager.WRITER_PROMPT.format(content=content)
            ),
            user_message
            ]
        response = self.model.invoke(messages)
        print("Generation node: ", Fore.YELLOW + "Draft: " + response.content + Fore.RESET)
        return {
            "draft": response.content, 
            "revision_number": state.get("revision_number", 1) + 1
        }
        
    def reflect(self,state: AgentState):
        messages = [
            SystemMessage(content=PromptManager.REFLECTION_PROMPT), 
            HumanMessage(content=state['draft'])
        ]
        response = self.model.invoke(messages)
        print("Reflection node: ", Fore.YELLOW + "Critique: " + response.content + Fore.RESET)
        return {"critique": response.content}
        
    
    def invoke(self, state: AgentState):
        return self.graph.invoke(state)
    
graph = Agent(model=model, tools=[tavily])

user_input = input("Enter the Idea on which you want me to create report: " + Fore.GREEN)
print(Fore.RESET)
        
result = graph.invoke(AgentState(
    task=user_input,
    plan="",
    draft="",
    critique="",
    content=[],
    revision_number=0,
    max_revisions=3
))


print(Fore.GREEN + "Final Draft: " + result['draft'] + Fore.RESET)

