import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, LLM, Task
from tools.reddit_scrapper_tool import fetch_reddit_posts

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

gpt_llm = LLM(model="gpt-3.5-turbo",
          # base_url="https://api.groq.com/openai/v1",
          api_key=os.getenv("OPENAI_API_KEY"),
          max_tokens=500)

data_collector_agent = Agent(
    role="Reddit Data Collector",
    goal="Fetch Reddit posts and top comments about specific car models",
    backstory="You specialize in extracting relevant Reddit content for vehicle comparisons.",
    llm=gpt_llm,
    max_iter = 3,
    tools=[fetch_reddit_posts],
    verbose=True
)


task = Task(
    description="Fetch Reddit posts about Toyota Hilux",
    agent=data_collector_agent,
    expected_output="Summarized Reddit feedback about the car, taking into consideration the sentiment overall on said car."
)

# 🔍 Test a direct task run
if __name__ == "__main__":
    result = data_collector_agent.execute_task(task)
    print("\n🧠 Agent Output:\n", result)