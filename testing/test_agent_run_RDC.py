import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env manually
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# # Prevent fallback to OpenAI by explicitly setting defaults
# os.environ["LITELLM_MODEL"] = "groq/llama3-70b-8192"
# os.environ["LITELLM_API_KEY"] = os.getenv("GROQ_API_KEY")
# os.environ["LITELLM_BASE_URL"] = "https://api.groq.com/openai/v1"

from crewai import Crew, Task
from agents.data_collector_agent import data_collector_agent

task = Task(
    description="Fetch Reddit posts about Honda Civic 2020",
    agent=data_collector_agent,
    expected_output="Summarized Reddit feedback about the car"
)

crew = Crew(
    agents=[data_collector_agent],
    tasks=[task],
    verbose=True,
    planning=True
)

crew.kickoff()
