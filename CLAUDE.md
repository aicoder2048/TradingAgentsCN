# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Or install with uv for faster package management
uv pip install -r requirements.txt
```

### CLI Usage
```bash
# Run the interactive CLI for trading analysis
python -m cli.main

# Direct Python usage
python main.py
```

### Required Environment Variables
- `FINNHUB_API_KEY`: Required for financial data (free tier available)
- `OPENAI_API_KEY`: Required for LLM agents
- `TRADINGAGENTS_RESULTS_DIR`: Optional, defaults to "./results"

## Architecture Overview

### Core Framework
TradingAgents is a multi-agent LLM trading framework built on LangGraph. The system simulates a real trading firm with specialized agents that collaborate to make trading decisions.

### Main Components

#### 1. Multi-Agent System (`tradingagents/agents/`)
- **Analysts**: Specialized analysis agents for different market aspects
  - `fundamentals_analyst.py`: Company financials and performance metrics
  - `news_analyst.py`: Global news and macroeconomic indicators
  - `social_media_analyst.py`: Sentiment analysis from social platforms
  - `market_analyst.py`: Technical indicators (MACD, RSI) and patterns
- **Researchers**: Bull/bear debate system
  - `bull_researcher.py` and `bear_researcher.py`: Critical assessment through structured debates
- **Trader**: `trader.py` - Makes trading decisions based on analyst reports
- **Risk Management**: Portfolio risk assessment and strategy evaluation
  - `risk_mgmt/`: Contains aggressive, conservative, and neutral debators

#### 2. Graph Orchestration (`tradingagents/graph/`)
- `trading_graph.py`: Main orchestration class `TradingAgentsGraph`
- `propagation.py`: Forward propagation through the agent network
- `conditional_logic.py`: Decision routing and conditional flows
- `reflection.py`: Learning and memory management
- `signal_processing.py`: Signal analysis and processing

#### 3. Data Management (`tradingagents/dataflows/`)
- `interface.py`: Data flow configuration and management
- Financial data APIs: `finnhub_utils.py`, `yfin_utils.py`, `stockstats_utils.py`
- News/sentiment data: `googlenews_utils.py`, `reddit_utils.py`
- `data_cache/`: Cached financial data for offline analysis

#### 4. Configuration (`tradingagents/default_config.py`)
Key configuration options:
- `llm_provider`: "openai", "anthropic", or "google"
- `deep_think_llm`/`quick_think_llm`: Model selection for different reasoning tasks
- `max_debate_rounds`: Controls debate intensity
- `online_tools`: Use real-time data vs cached data

### Usage Patterns

#### Basic Usage
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
_, decision = ta.propagate("NVDA", "2024-05-10")
```

#### Custom Configuration
```python
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"  # Cost-effective option
config["max_debate_rounds"] = 2  # More thorough analysis
config["online_tools"] = False  # Use cached data
```

### Key Design Principles
- **Modular Agent Design**: Each agent has specific expertise and can be independently configured
- **Debate-Driven Decisions**: Bull/bear researchers challenge analyst findings through structured debates
- **Risk-Aware Trading**: Multi-layer risk assessment before execution
- **Memory and Reflection**: Agents learn from past decisions through the reflection system
- **Flexible LLM Integration**: Supports multiple LLM providers with role-specific model selection

### Results and Output
- Trading decisions and analysis reports are saved to `results/{TICKER}/{DATE}/`
- Includes market reports, investment plans, and final trade decisions
- Log files track the complete decision-making process

### Testing and Validation
The framework is designed for research purposes and includes extensive logging for analysis. Trading performance varies based on model selection, market conditions, and configuration parameters.