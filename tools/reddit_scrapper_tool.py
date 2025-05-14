# tools/reddit_scrapper_tool.py

import os
import re
import praw
from dotenv import load_dotenv
from crewai.tools import tool

# Load environment variables
load_dotenv()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

@tool("fetch_reddit_posts")
def fetch_reddit_posts(input_text: str) -> str:
    """
    Search Reddit for user feedback on a specific car model and year.
    
    Format:
    - 'Car Model | subreddit1,subreddit2,...'
    - Example: 'Honda Civic 2020 | cars,whatcarshouldibuy,CarsAustralia'

    Defaults to the latest model if no year is provided.
    """
    try:
        if "|" in input_text:
            car_model, subreddit_str = [s.strip() for s in input_text.split("|")]
            subreddits = [s.strip() for s in subreddit_str.split(",")]
        else:
            car_model = input_text
            subreddits = ["cars", "whatcarshouldibuy", "askcarsales"]

        car_model = car_model.lower()
        year_match = re.search(r"\b(19|20)\d{2}\b", car_model)
        required_year = year_match.group(0) if year_match else None

        results = []

        for sub in subreddits:
            for submission in reddit.subreddit(sub).search(car_model, sort="relevance", limit=7):
                if not submission.is_self or submission.score < 2:
                    continue

                if required_year:
                    if required_year not in submission.title and required_year not in submission.selftext:
                        continue
                    conflicting_years = re.findall(r"\b(19|20)\d{2}\b", submission.title + " " + submission.selftext)
                    conflicting_years = [y for y in conflicting_years if y != required_year]
                    if conflicting_years:
                        continue

                if len(submission.selftext.strip()) < 100:
                    continue

                snippet = submission.selftext.split("\n")[0][:300].strip()

                submission.comment_sort = 'top'
                submission.comments.replace_more(limit=0)
                top_comments = []

                for comment in submission.comments[:6]:
                    text = comment.body.strip()
                    if len(text) > 50 and "bot" not in text.lower():
                        top_comments.append(f"💬 {text[:200]}...")

                if not top_comments:
                    continue

                comments_section = "\n".join(top_comments)

                results.append(
                    f"---\n"
                    f"📌 **r/{sub}**: [{submission.title}]({submission.url}) (Score: {submission.score})\n"
                    f"{snippet}...\n\n{comments_section}"
                )

        if not results:
            return f"🔍 No useful posts found for '{car_model}' in subreddits: {', '.join(subreddits)}."

        readable_title = f"{car_model} {required_year}" if required_year else f"{car_model.title()} (Latest Model)"
        return f"🔎 Reddit Results for **{readable_title}**\n\n" + "\n\n".join(results[:10])

    except Exception as e:
        return f"❌ Error fetching Reddit posts: {e}"
