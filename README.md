# AI Trading App

The **AI Trading App** is a full-stack cryptocurrency trading platform built for personal use, enabling safe, automated trading decisions powered by AI and quantitative strategies. It supports Binance integration and enforces a strict flow of strategy validation: every new strategy or coin pair must pass backtesting and paper trading before any live trades are allowed.

AI integration is focused on execution and continuous improvement rather than chat, allowing the system to adapt and optimize strategies based on performance over time. A modern frontend provides dynamic insights into portfolio performance, trade journals, and strategy control.

---

## 🚀 Features

### Backend

- FastAPI-based modular service
    
- Binance integration (planned)
    
- Backtesting engine (planned)
    
- AI/LLM execution engine (planned via Ollama)
    
- Strategy framework with versioning and validation
    

### Frontend

- **Overview Tab**: Portfolio breakdowns, performance charts, win rates, profit percentages
    
- **Journal Tab**: Trade logs, timestamps, entry/exit reasons, outcome analyses
    
- **Chat Tab**: Optional strategy updates with AI (non-core)
    
- **Settings Tab**: Control risk, automation, coin pair selection, permissions
    

### System

- Paper trading environment by default
    
- Live trading toggled per strategy upon approval
    
- Modular strategy engine with optional AI filters
    
- Future-proofed for multi-exchange expansion
    

---

## 📂 Project Structure (Monorepo)

```bash
Trading_app/
├── apps/
│   ├── backend/         # FastAPI core
│   └── frontend/        # React client
├── obsidian/
│   ├──
├── packages/
│   └── shared/          # Shared types/utilities
├──venv/
├── .devcontainer/       # VSCode remote environment
├── docker-compose.yml   # Dev orchestration
```

---

## ⚙️ Getting Started

### Prerequisites

- Docker + Docker Compose
    
- Python 3.11+
    
- Node.js 18+
    

### Run the App

```bash
docker compose up --build
```

### Access

- Backend: [http://localhost:8000/docs](http://localhost:8000/docs)
    
- Frontend: [http://localhost:3000](http://localhost:3000/)
    

---

## 📈 Roadmap (Major Milestones)

-  Frontend & backend scaffolding
    
-  Binance price feed + trade execution
    
-  Paper trading engine
    
-  Backtesting module with strategy versions
    
-  Ollama-powered AI analysis
    
-  Full CI/CD pipeline and unit tests
    
-  Production-ready monitoring & logging
    

---

## 🤝 Contributing

Coming soon: setup guide, dev conventions, and testing instructions.

---

## 🛡 License

This project is for personal use by the author. Contact for collaboration.