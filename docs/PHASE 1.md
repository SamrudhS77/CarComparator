### ✅ Phase 1: Reddit-Based Car Comparison (In Progress)
Build an agentic system that:
- Uses Reddit as the primary data source
- Allows user to input **Car A** and **Car B**
- Fetches top Reddit threads and comments related to both cars
- Summarizes pros, cons, and user sentiment for each
- Compares both cars side-by-side based on extracted insights

#### 🗝️ Key Components
- 🧑‍💼 **CrewAI Framework** to manage a team of role-based agents:
  - `RedditResearchAgent`: Finds and collects user discussions
  - `InsightSummarizerAgent`: Extracts pros/cons and reliability sentiment
  - `ComparisonAdvisorAgent`: Compares Car A vs Car B across user-sourced metrics
- 🛠️ **LangChain tools** to wrap scraping, sentiment scoring, and data parsing
- 🔁 **LangGraph** (optional in later phases) to coordinate multi-step flows

#### ⚙️ Tools & Tech
- CrewAI for role-driven collaboration
- PRAW for Reddit API access
- LiteLLM + Groq for summarization (LLM backend)
- LangChain for tool abstraction
- pandas for data organization
