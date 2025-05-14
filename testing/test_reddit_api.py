import os
import praw
from dotenv import load_dotenv

# Load API credentials from .env
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Test: Search for posts about "Toyota Hilux"
query = "Toyota Hilux"
subreddit = reddit.subreddit("CarsAustralia")

print(f"Top 5 Reddit posts for: {query}\n")

for post in subreddit.search(query, sort="relevance", limit=5):
    print(f"Title: {post.title}")
    print(f"Score: {post.score}")
    print(f"URL:   {post.url}")
    print("---")
