from crewai import Agent
from tools.reddit_scrapper_tool import fetch_reddit_posts_tool

data_collector_agent = Agent(
    role="Reddit Data Collector",
    goal="Fetch Reddit posts and top comments about specific car models",
    backstory="You specialize in extracting relevant Reddit content for vehicle comparisons.",
    tools=[fetch_reddit_posts_tool], 
    allow_delegation=False
)
