from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun, BraveSearch
from dotenv import load_dotenv

load_dotenv()

search_tool = DuckDuckGoSearchRun()

@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=df521f6df417c8b7b77c8838701ec384&query={city}'

  response = requests.get(url)

  return response.json()

llm = ChatOpenAI()

from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Step 2: Pull the ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")  # pulls the standard ReAct agent prompt

# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_react_agent(
    llm=llm,
    tools=[search_tool, get_weather_data],
    prompt=prompt
)

# Step 4: Wrap it with AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, get_weather_data],
    verbose=True
)
# Step 5: Invoke
response = agent_executor.invoke({"input": " Find current weather condition of Ireland"})
print(response)

response['output']
