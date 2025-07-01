import React, { useState, useEffect } from 'react';
import { FileText, GitBranch, Target, Code, TrendingUp, MessageSquare, CheckCircle, Clock, AlertCircle, Plus, Save, RotateCcw, Bot } from 'lucide-react';

// Define a type for conversation items
interface ConversationItem {
  id: number;
  type: string;
  content: string;
  timestamp: string;
}

const TradingBotWorkflow = () => {
  const [currentPhase, setCurrentPhase] = useState('mvp-backtesting');
  const [activeSession, setActiveSession] = useState('2025-06-30');
  const [contextData, setContextData] = useState({
    strategy: 'BTC Mean Reversion v1',
    progress: 'Binance API Integration',
    blockers: [],
    nextSteps: []
  });
  const [aiConversation, setAiConversation] = useState<ConversationItem[]>([]);
  const [currentPrompt, setCurrentPrompt] = useState('');
  const [sessionNotes, setSessionNotes] = useState('');

  const phases = [
    { id: 'mvp-backtesting', name: 'MVP Backtesting', status: 'active' },
    { id: 'agent-logic', name: 'Agent Logic', status: 'in-progress' },
    { id: 'api-integration', name: 'API Integration', status: 'in-progress' },
    { id: 'frontend-dashboard', name: 'Frontend Dashboard', status: 'pending' },
    { id: 'deployment', name: 'Deployment', status: 'pending' }
  ];

  const obsidianStructure = {
    '00_Overview': ['README.md'],
    '01_Architecture': ['agent_workflow.md', 'data_pipeline.md', 'system_design.md'],
    '02_Strategies': ['mean_reversion_v1.md', 'momentum_strategy_v1.md'],
    '03_Prompts': ['chatgpt_prompt_templates.md', 'claude_prompt_templates.md'],
    '04_Logs': ['2025-06-30_session.md', 'trade_analysis_log.md'],
    '05_Code': ['api_docs.md', 'notes_on_trading_bot_logic.md'],
    '09_Tasks': ['dashboard_trading_app.md', 'project_todo.md']
  };

  const generateContextPrompt = () => {
    const context = `
# Trading Bot Development Context

## Current Phase: ${phases.find(p => p.id === currentPhase)?.name}
## Strategy: ${contextData.strategy}
## Current Focus: ${contextData.progress}

## Project Structure:
- Backend: Python/FastAPI (apps/backend/)
- Frontend: React/Vite/TypeScript (apps/frontend/)
- Documentation: Obsidian vault with organized folders
- Deployment: Docker containers

## Recent Progress:
- Architecture design completed
- Claude prompt templates created for agent execution
- Binance API integration in progress

## Current Blockers:
${contextData.blockers.map(b => `- ${b}`).join('\n')}

## Next Steps Needed:
${contextData.nextSteps.map(s => `- ${s}`).join('\n')}

## Session Notes:
${sessionNotes}

---

Please provide specific, actionable guidance for the current development phase. Focus on:
1. Immediate next steps
2. Code examples if needed
3. Architecture decisions
4. Testing approaches
`;
    setCurrentPrompt(context);
  };

  const addToConversation = (type: string, content: string) => {
    setAiConversation((prev: ConversationItem[]) => [
      ...prev,
      {
        id: Date.now(),
        type,
        content,
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);
  };

  const handleQuickPrompt = (prompt: string) => {
    setCurrentPrompt(prompt);
    addToConversation('user', prompt);
  };

  const quickPrompts = [
    {
      title: "Review Current Code",
      prompt: "Review my current backend/frontend code structure and identify gaps or improvements needed for the trading bot."
    },
    {
      title: "Binance API Integration",
      prompt: "Help me implement Binance API integration for real-time price feeds and order execution."
    },
    {
      title: "Agent Logic Design",
      prompt: "Design the core agent decision-making loop for the mean reversion strategy."
    },
    {
      title: "Backtesting Framework",
      prompt: "Create a backtesting framework to validate trading strategies before live deployment."
    },
    {
      title: "Frontend Dashboard",
      prompt: "Design and implement a React dashboard for monitoring trading bot performance."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
            <Bot className="w-10 h-10 text-blue-400" />
            Trading Bot AI Development Hub
          </h1>
          <p className="text-blue-200">Seamless AI collaboration for your trading bot project</p>
        </div>

        {/* Project Status */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2 bg-slate-800/50 rounded-lg p-6 backdrop-blur-sm">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-green-400" />
              Development Phases
            </h2>
            <div className="space-y-3">
              {phases.map(phase => (
                <div key={phase.id} className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${
                    phase.status === 'active' ? 'bg-green-400' :
                    phase.status === 'in-progress' ? 'bg-yellow-400' :
                    'bg-gray-600'
                  }`} />
                  <span className={`${phase.status === 'active' ? 'text-green-300 font-semibold' : 'text-gray-300'}`}>
                    {phase.name}
                  </span>
                  {phase.status === 'active' && (
                    <span className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded">
                      CURRENT
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-6 backdrop-blur-sm">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-400" />
              Current Focus
            </h2>
            <div className="space-y-3">
              <div>
                <span className="text-sm text-gray-400">Strategy:</span>
                <p className="text-blue-300 font-medium">{contextData.strategy}</p>
              </div>
              <div>
                <span className="text-sm text-gray-400">Progress:</span>
                <p className="text-green-300 font-medium">{contextData.progress}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Workflow */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* AI Conversation Panel */}
          <div className="bg-slate-800/50 rounded-lg p-6 backdrop-blur-sm">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-purple-400" />
              AI Collaboration
            </h2>
            
            {/* Quick Prompts */}
            <div className="mb-4">
              <h3 className="text-sm font-medium text-gray-300 mb-2">Quick Prompts:</h3>
              <div className="grid grid-cols-1 gap-2">
                {quickPrompts.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickPrompt(prompt.prompt)}
                    className="text-left p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded text-sm transition-colors"
                  >
                    {prompt.title}
                  </button>
                ))}
              </div>
            </div>

            {/* Context Generator */}
            <div className="mb-4">
              <button
                onClick={generateContextPrompt}
                className="w-full bg-blue-600 hover:bg-blue-700 p-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
              >
                <RotateCcw className="w-4 h-4" />
                Generate Full Context Prompt
              </button>
            </div>

            {/* Prompt Display */}
            <div className="bg-slate-900/50 rounded p-4 max-h-96 overflow-y-auto">
              <h4 className="text-sm font-medium text-gray-300 mb-2">Current Prompt:</h4>
              <pre className="text-xs text-gray-300 whitespace-pre-wrap">
                {currentPrompt || "Click 'Generate Full Context Prompt' to create a comprehensive prompt for AI assistance"}
              </pre>
            </div>
          </div>

          {/* Project Management */}
          <div className="bg-slate-800/50 rounded-lg p-6 backdrop-blur-sm">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5 text-orange-400" />
              Session Management
            </h2>

            {/* Session Notes */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Session Notes (2025-06-30):
              </label>
              <textarea
                value={sessionNotes}
                onChange={(e) => setSessionNotes(e.target.value)}
                className="w-full h-32 bg-slate-900/50 border border-slate-600 rounded p-3 text-sm resize-none focus:outline-none focus:border-blue-400"
                placeholder="Document progress, decisions, and next steps..."
              />
            </div>

            {/* Obsidian Structure */}
            <div className="mb-4">
              <h3 className="text-sm font-medium text-gray-300 mb-2">Obsidian Vault Structure:</h3>
              <div className="bg-slate-900/50 rounded p-3 text-xs">
                {Object.entries(obsidianStructure).map(([folder, files]) => (
                  <div key={folder} className="mb-2">
                    <div className="text-blue-300 font-medium">{folder}/</div>
                    {files.map(file => (
                      <div key={file} className="ml-4 text-gray-400">├── {file}</div>
                    ))}
                  </div>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2">
              <button className="flex-1 bg-green-600 hover:bg-green-700 p-2 rounded font-medium transition-colors flex items-center justify-center gap-2">
                <Save className="w-4 h-4" />
                Update State
              </button>
              <button className="flex-1 bg-purple-600 hover:bg-purple-700 p-2 rounded font-medium transition-colors flex items-center justify-center gap-2">
                <Code className="w-4 h-4" />
                Code Review
              </button>
            </div>
          </div>
        </div>

        {/* Next Steps */}
        <div className="mt-8 bg-slate-800/50 rounded-lg p-6 backdrop-blur-sm">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-400" />
            Immediate Action Items
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-green-300 mb-2">Backend Tasks:</h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Complete Binance API integration</li>
                <li>• Implement mean reversion strategy logic</li>
                <li>• Create backtesting framework</li>
                <li>• Set up database for trade history</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-blue-300 mb-2">Frontend Tasks:</h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Build trading dashboard UI</li>
                <li>• Create real-time charts</li>
                <li>• Implement strategy controls</li>
                <li>• Add performance analytics</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradingBotWorkflow;