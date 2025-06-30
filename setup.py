import os

vault_name = "AI-Trading-Brain"
base_path = os.path.join(os.getcwd(), vault_name)

structure = {
    "00_Overview": {
        "README.md": "# AI Trading Vault\n\nWelcome to your trading vault. Use this space to coordinate AI agents.",
        "_current_state.md": """# 📌 Current State

## 📊 Project Phase
- MVP build: Backtesting & agent logic in progress

## ✅ Recent Progress
- Finished architecture draft
- Designed Claude prompt for agent execution loop

## 🔧 In Progress
- Connecting Binance API for price feed
- Evaluating which agent logic performs best

## 🧠 Notes for AI
Please continue from current progress. We're iterating on strategy testing and agent coordination.
"""
    },
    "01_Architecture": {
        "system_design.md": "# System Design\n\nOutline the overall trading system architecture here.",
        "data_pipeline.md": "# Data Pipeline\n\nDescribe how data is collected, cleaned, and fed into strategies.",
        "agent_workflow.md": "# Agent Workflow\n\nHow AI agents interact with each other and trading logic."
    },
    "02_Strategies": {
        "momentum_strategy_v1.md": "# Momentum Strategy v1\n\nDescribe logic, performance, and assumptions.",
        "mean_reversion_v1.md": "# Mean Reversion Strategy v1\n\nInitial draft and testing logs."
    },
    "03_Prompts": {
        "chatgpt_prompt_templates.md": "# ChatGPT Prompt Templates\n\nPrompts for trade logic, summarization, etc.",
        "claude_prompt_templates.md": "# Claude Prompt Templates\n\nPrompts for document reasoning and strategy comparison.",
        "prompt_chain_templates.md": "# Prompt Chain Templates\n\nOutline multi-step prompt chains."
    },
    "04_Logs": {
        "2025-06-30_session.md": "# Session Log – 2025-06-30\n\nSummary of work and AI assistance.",
        "trade_analysis_log.md": "# Trade Analysis Log\n\nDate-by-date reviews of performance."
    },
    "05_Code": {
        "notes_on_trading_bot_logic.md": "# Trading Bot Logic Notes\n\nBasic logic and agent loop.",
        "api_integration_plan.md": "# API Integration Plan\n\nEndpoints and polling logic."
    },
    "06_Research": {
        "links_to_papers.md": "# Research Papers\n\nUseful links to trading and AI resources.",
        "ideas_from_other_bots.md": "# Bot-Inspired Ideas\n\nWhat we’ve learned from other tools.",
        "backtesting_approaches.md": "# Backtesting\n\nTools and methods we're using/tested."
    },
    "07_Ideas": {
        "feature_ideas.md": "# Feature Ideas\n\nIdeas to enhance the app.",
        "ui_concepts.md": "# UI Concepts\n\nDrawings, mockups, or text-based UI thoughts.",
        "feedback_from_ai.md": "# Feedback From AI\n\nInsights or improvements proposed by AI."
    }
}

# Create folders and files
for folder, files in structure.items():
    folder_path = os.path.join(base_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    for filename, content in files.items():
        with open(os.path.join(folder_path, filename), "w", encoding="utf-8") as f:
            f.write(content)

print(f"✅ Obsidian vault created at: {base_path}")
