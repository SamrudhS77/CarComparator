import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, LLM, Task
from tools.reddit_scrapper_tool import fetch_reddit_posts

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

llama_llm = LLM(model="groq/llama3-70b-8192",
          base_url="https://api.groq.com/openai/v1",
          api_key=os.getenv("GROQ_API_KEY"))

data_collector_agent = Agent(
    role="Reddit Data Collector",
    goal="Fetch Reddit posts and top comments about specific car models",
    backstory="You specialize in extracting relevant Reddit content for vehicle comparisons.",
    llm=llama_llm,
    tools=[fetch_reddit_posts],
    verbose=True
)


task = Task(
    description="Fetch Reddit posts about Honda Civic 2020",
    agent=data_collector_agent,
    expected_output="Summarized Reddit feedback about the car"
)

# 🔍 Test a direct task run
if __name__ == "__main__":
    result = data_collector_agent.execute_task(task)
    print("\n🧠 Agent Output:\n", result)