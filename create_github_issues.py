import requests

# === Configuration ===
GITHUB_TOKEN = "your_github_token_here"  # Replace with a GitHub personal access token
REPO_OWNER = "JessGerritsma"             # Replace with your GitHub username
REPO_NAME = "Trading_app"                # Replace with your repo name

# === Issues to Create ===
issues = [
    {"title": "Implement Base Strategy Framework", "labels": ["backend", "strategy", "core"], "body": "Create BaseStrategy class with standard methods (calculate_signals, should_buy, should_sell)."},
    {"title": "Build Mean Reversion Strategy", "labels": ["backend", "strategy"], "body": "Use moving average and price thresholds to define buy/sell signals."},
    {"title": "Implement Backtester for Strategies", "labels": ["backend", "strategy", "testing"], "body": "Run historical price data through strategies and generate performance reports."},
    {"title": "Set Up Ollama Integration with LLM Client", "labels": ["backend", "AI"], "body": "Implement async client for local Ollama model interactions."},
    {"title": "Refactor Backend Structure into /src/api, /core, etc.", "labels": ["backend", "refactor"], "body": "Restructure code to use modular architecture as defined in roadmap."},
    {"title": "Create Binance Service for Market Data + Orders", "labels": ["backend", "exchange"], "body": "Create real-time price feed, order submission, and account tracking."},
    {"title": "Add Paper Trading Execution Engine", "labels": ["backend", "simulation"], "body": "Simulate trades without real execution based on strategies."},
    {"title": "Design and Implement SQLite Models (Trade, Strategy, etc.)", "labels": ["backend", "database"], "body": "Create SQLAlchemy models and migrations for trades, strategies, market data."},
    {"title": "Create WebSocket Server for Real-Time Price Feeds", "labels": ["backend", "realtime"], "body": "Expose real-time data to frontend clients using FastAPI websockets."},
    {"title": "Build Overview Dashboard: Portfolio Charts and Stats", "labels": ["frontend", "charts", "analytics"], "body": "Add charts, stats, and visual summaries of account performance."},
    {"title": "Implement Trade Journal Table with Filtering", "labels": ["frontend", "journal", "UX"], "body": "Display trade history with reason, timestamps, and result evaluations."},
    {"title": "Create Settings Panel for Automation Toggles and Risk", "labels": ["frontend", "settings", "UX"], "body": "Allow users to set trading preferences, toggles, coin filters."},
    {"title": "Integrate WebSocket into Frontend for Live Price Updates", "labels": ["frontend", "realtime"], "body": "Connect frontend to backend websocket for live pricing."},
    {"title": "Set Up GitHub Actions CI for Backend and Frontend", "labels": ["CI/CD", "testing"], "body": "Create workflows to lint, test and optionally deploy."},
    {"title": "Add Unit Tests for Strategy Module", "labels": ["testing", "backend"], "body": "Write tests for strategy signal logic using pytest."},
    {"title": "Create .env.example and Add API Key Handling", "labels": ["security", "devops"], "body": "Standardize environment config and prevent secret leaks."},
    {"title": "Set Up Bandit and Safety for Python Security Scanning", "labels": ["security", "linting"], "body": "Add security scanners to lint and validate dependencies."}
]

# === API Call ===
def create_github_issue(title, body, labels):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "title": title,
        "body": body,
        "labels": labels
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"✅ Created issue: {title}")
    else:
        print(f"❌ Failed to create issue: {title} | {response.status_code} - {response.text}")

# === Run Script ===
if __name__ == "__main__":
    for issue in issues:
        create_github_issue(issue["title"], issue["body"], issue["labels"])
