import os
import praw
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

@tool("fetch_reddit_posts", return_direct=True)
def fetch_reddit_posts_tool(car_model: str) -> str:
    """
    Searches Reddit for posts about a specific car model and returns the top 5 threads.
    """
    try:
        results = []
        for submission in reddit.subreddit("cars+whatcarshouldibuy+askcarsales+carsAustralia").search(car_model, sort="relevance", limit=5):
            results.append(f"- {submission.title} (Score: {submission.score})\n{submission.selftext[:300]}...\nURL: {submission.url}")
        
        if not results:
            return f"No posts found for '{car_model}'."
        
        return f"Top posts for '{car_model}':\n\n" + "\n\n".join(results)
    
    except Exception as e:
        return f"Error fetching Reddit posts: {e}"
