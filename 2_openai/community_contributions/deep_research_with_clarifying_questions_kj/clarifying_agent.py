import os
from dotenv import load_dotenv
from agents import Agent
from pydantic import BaseModel

load_dotenv(override=True)

INSTRUCTIONS = """
You are a research assistant. Your task is to ask 3 clarifying questions that help refine and understand a research query better. After the user answers them, hand off control to the Research Coordinator to perform the full research.
"""

class ClarifyingQuestions(BaseModel):
    questions: list[str]
    """Three clarifying questions to better understand the user's query."""

from agents.extensions.models.litellm_model import LitellmModel

model = LitellmModel(
    model="gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)

clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=INSTRUCTIONS,
    model=model,
    output_type=ClarifyingQuestions,
)