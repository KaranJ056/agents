from pydantic import BaseModel, Field
from agents import Agent
import os
from dotenv import load_dotenv

load_dotenv(override=True)

HOW_MANY_SEARCHES = 3

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
from agents.extensions.models.litellm_model import LitellmModel

model = LitellmModel(
    model="gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)

planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model=model,
    output_type=WebSearchPlan,
)