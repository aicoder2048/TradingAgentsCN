# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
# Install dependencies using uv (recommended - modern, fast package manager)
uv sync

# Or traditional pip installation
pip install -r requirements.txt
```

### Running the Project
```bash
# Interactive CLI for trading analysis (recommended)
uv run -m cli.main

# Direct execution for programmatic usage
uv run main.py

# Generate comprehensive trading report from existing analyses
uv run -m cli.gen_final_report results/NVDA/2025-07-17/reports
```

**Note**: The report generation tool requires `pandoc` for HTML conversion. Install it with:
- macOS: `brew install pandoc`
- Ubuntu/Debian: `sudo apt-get install pandoc`
- Windows: `choco install pandoc`

### Environment Configuration
Create a `.env` file in the project root (copy from `.env.sample`):
- `FINNHUB_API_KEY`: Required for financial data (free tier at finnhub.io)
- `OPENAI_API_KEY`: Required for OpenAI models
- `DEEPSEEK_API_KEY`: Optional, for DeepSeek models (cost-effective)
- `MOONSHOT_API_KEY`: Optional, for Kimi K2 models (overseas version)
- `ANTHROPIC_API_KEY`: Optional, for Claude models
- `GOOGLE_API_KEY`: Optional, for Gemini models
- `TRADINGAGENTS_RESULTS_DIR`: Optional, defaults to "./results"

## Architecture Overview

### Core Framework
TradingAgents is a multi-agent LLM trading framework built on LangGraph. It simulates a real trading firm with specialized agents collaborating through structured workflows.

### Key Components and Their Interactions

#### 1. Agent Network (`tradingagents/agents/`)
**Analysts** - Data gathering and initial analysis:
- `fundamentals_analyst.py`: Analyzes company financials, earnings, P/E ratios
- `market_analyst.py`: Technical analysis using MACD, RSI, price patterns
- `news_analyst.py`: Processes global news and macroeconomic indicators
- `social_media_analyst.py`: Sentiment analysis from Reddit, social platforms

**Researchers** - Critical evaluation through debate:
- `bull_researcher.py`: Advocates for positive outlook based on analyst reports
- `bear_researcher.py`: Challenges with bearish perspectives
- Debate process controlled by `max_debate_rounds` in config

**Decision Makers**:
- `trader.py`: Synthesizes all reports to make buy/sell/hold decisions
- `risk_mgmt/`: Three debators (aggressive, conservative, neutral) evaluate risk
- `managers/`: Research and risk managers coordinate agent activities

#### 2. LangGraph Orchestration (`tradingagents/graph/`)
- `trading_graph.py`: Main class `TradingAgentsGraph` that coordinates entire workflow
- `propagation.py`: Implements forward propagation through agent network
- `conditional_logic.py`: Routes decisions based on agent outputs
- `reflection.py`: Manages learning from past decisions
- `signal_processing.py`: Processes trading signals from agents

#### 3. Data Layer (`tradingagents/dataflows/`)
- `interface.py`: Unified interface for all data sources
- API integrations: `finnhub_utils.py`, `yfin_utils.py`, `stockstats_utils.py`
- News/sentiment: `googlenews_utils.py`, `reddit_utils.py`
- `data_cache/`: Pre-downloaded market data for offline testing

### Configuration (`tradingagents/default_config.py`)
Key settings that control behavior:
```python
{
    "llm_provider": "openai",  # or "anthropic", "google"
    "deep_think_llm": "o4-mini",  # For complex reasoning tasks
    "quick_think_llm": "gpt-4o-mini",  # For quick decisions
    "max_debate_rounds": 1,  # Number of bull/bear debate rounds
    "max_risk_discuss_rounds": 1,  # Risk assessment iterations
    "online_tools": True,  # Use live data vs cached
}
```

### Workflow Execution Flow
1. **Data Collection**: Analysts gather market data, news, sentiment
2. **Analysis Phase**: Each analyst produces specialized reports
3. **Research Debate**: Bull/bear researchers debate findings
4. **Trading Decision**: Trader synthesizes all inputs
5. **Risk Assessment**: Risk team evaluates proposed trades
6. **Final Execution**: Portfolio manager approves/rejects

### Output Structure
Results saved to `results/{TICKER}/{DATE}/`:
- `reports/`: Individual agent reports (fundamentals, market, news, sentiment)
- `trader_investment_plan.md`: Proposed trading strategy
- `final_trade_decision.md`: Executed decision after risk review
- `message_tool.log`: Complete agent communication log

### CLI Features (`cli/`)
- `main.py`: Interactive interface for selecting stocks, dates, models
- `gen_final_report.py`: Merges individual reports into comprehensive HTML
- `models.py`: Data models for CLI operations
- `static/welcome.txt`: ASCII art welcome screen

### LLM Provider Integration
Supports multiple providers with different cost/performance tradeoffs:
- **OpenAI**: GPT-4o, o1 models (default)
- **Anthropic**: Claude 3.5/4 series
- **Google**: Gemini 2.0/2.5 series
- **DeepSeek**: Cost-effective alternative
- **Moonshot**: Kimi K2 for long context

Provider-specific configuration in `ai_docs/` directory.

### Development Notes
- The framework uses extensive logging for debugging agent decisions
- Memory system (`agents/utils/memory.py`) enables learning from past trades
- Agent states (`agents/utils/agent_states.py`) maintain conversation context
- All agents inherit from base classes in `agents/utils/agent_utils.py`