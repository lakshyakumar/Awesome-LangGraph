# libraries
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from colorama import Fore

# load environment variables from .env file
_ = load_dotenv()

# connect
client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
print("Search using Tavily API")

query = "What is in Nvidia's new Blackwell GPU?"
print("query : ", Fore.YELLOW + query + Fore.RESET)
result = client.search(query=query,
                       include_answer=True)

# print the answer
print("results : ", Fore.GREEN+result["answer"]+Fore.RESET)