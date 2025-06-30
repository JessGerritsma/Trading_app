---
status: todo
priority: high
due: 2025-07-05
tags: [backend, api]
---
put the above into task or project notes can customize the fields to relevant info

### How to organize:

| Content Type                         | Where to put it                                                                            | Example or Purpose                                                                                  |                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Markdown** (tasks, notes, queries) | Inside your `project_todo.md` or other `.md` notes in `/09_Tasks/` folder                  | Contains your task lists and Dataview queries to display/filter them dynamically.                   | # Project TODO List<br><br>```dataview<br>table status, priority, due<br>from "09_Tasks"<br>where status != "done"<br>sort due asc<br>                                                                                                                                                                                                                                           |
| **YAML frontmatter**                 | At the very top of each Markdown note where you want metadata (e.g. task status, priority) | Helps Dataview filter and organize your notes/tasks. Example: `--- status: todo priority: high ---` | <br>This will show a table of all notes under `09_Tasks` folder where `status` is not done, sorted by due date.<br><br>---<br><br>## ✅ Step 4: Use Inline Task Queries<br><br>You can also show all tasks with a specific tag or priority:<br><br>```markdown<br>```dataview<br>task from "09_Tasks"<br>where contains(tags, "backend") and !completed<br>sort priority desc<br> |
| **SQL**                              | Not used directly in Obsidian (Dataview doesn’t run SQL)                                   | Ignore SQL unless you use an external DB; Dataview uses its own query language inside Markdown.     | <br>---<br><br>## ✅ Step 5: Tag & Update Tasks in Your Notes<br><br>In any note inside your task folder, write tasks like this:<br><br>```markdown<br>- [ ] Implement API client #backend #priority-high<br>- [x] Write AI trading logic #backend #done<br>                                                                                                                      |

This will show a table of all notes under `09_Tasks` folder where `status` is not done, sorted by due date.

---

## Development Assistant Prompts

Here are specific prompts to help set up your system:

### **Prompt 1: Repository Analysis & Architecture**

```
I'm building a personal cryptocurrency trading system with the following stack:
- Frontend: React
- Backend: Python/FastAPI
- Database: SQLite initially
- AI: Local LLM integration
- Binance API integration

My current repo structure is: [paste your current folder structure]

Please analyze my existing codebase and provide:
1. Recommended folder structure for the trading system
2. How to integrate the new trading components with existing code
3. Dependencies I need to add to requirements.txt
4. Environment variables I should set up
5. A step-by-step development plan

My technical background: Frontend foundations, Python basics, some API experience.
```

### **Prompt 2: Binance API Integration Setup**

```
Help me set up Binance API integration for my Python trading system. I need:

1. Complete code for connecting to Binance Testnet (paper trading)
2. Functions for:
   - Getting real-time price data
   - Placing test orders
   - Checking account balance
   - Getting historical data
3. Error handling and rate limiting
4. Configuration management for API keys
5. A simple test script to verify everything works

Please provide complete, production-ready code with comments explaining each part.
```

### **Prompt 3: Database Schema Design**

```
Design a SQLite database schema for my crypto trading system. I need tables for:

1. Price data storage (OHLCV data)
2. Trade logging (entries, exits, P&L)
3. Strategy performance tracking
4. Risk management metrics
5. AI analysis results/logs

Provide:
- Complete SQL CREATE TABLE statements
- Python SQLAlchemy models
- Database initialization script
- Sample queries for common operations
- Indexing recommendations for performance

Focus on scalability - I'll eventually move to PostgreSQL.
```

### **Prompt 4: Local LLM Integration**

```
Show me how to integrate Ollama/Llama 3.1 into my Python trading system. I need:

1. Python code to communicate with local Ollama instance
2. Prompt templates for:
   - Market analysis
   - Trade opportunity evaluation
   - Risk assessment
   - Strategy suggestions
3. Response parsing and error handling
4. Async implementation for non-blocking operations
5. Context management for ongoing conversations

The AI should analyze market data and provide structured responses I can use programmatically.
```

### **Prompt 5: Real-time Data Pipeline**

```
Create a real-time data collection system for crypto trading:

1. WebSocket connection to Binance for live price feeds
2. Data processing and cleaning pipeline
3. Technical indicator calculations (RSI, MACD, Moving Averages)
4. Data storage with efficient querying
5. Event-driven architecture for trade signals
6. Memory management for long-running processes

Provide complete Python code with proper error handling and reconnection logic.
```

### **Prompt 6: Risk Management System**

```
Build a comprehensive risk management system with:

1. Position sizing calculations
2. Stop-loss automation
3. Portfolio-level risk monitoring
4. Daily/weekly loss limits
5. Maximum drawdown protection
6. Risk metrics calculation and logging

Include both preventive measures (before trades) and reactive measures (during trades).
```

## Integration with Your Existing Repo

To connect this with your current repository:

### **Prompt 7: Repository Integration**

```
I have an existing [React/Python/etc.] project. Help me integrate a trading system module:

Current repo structure: [paste structure]

Show me:
1. How to add trading functionality without breaking existing code
2. Shared utilities and configurations
3. API endpoint structure for frontend-backend communication
4. Component structure for trading UI
5. State management for real-time data
6. How to run both systems simultaneously

Provide migration steps and code examples.
```