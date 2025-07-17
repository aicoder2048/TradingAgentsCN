<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: 多智能体大语言模型金融交易框架

> ⭐ **这是TradingAgents的中文本地化Fork版本**
>
> 🔗 **原始仓库**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
>
> 🌟 **本Fork版本特色**:
> - 🇨🇳 完整的中文交易报告支持
> - 📚 增强的中文文档和API指南
> - ⚡ 现代化的依赖管理工具（uv + pyproject.toml）
> - 🔌 扩展的LLM提供商支持（DeepSeek、Moonshot等）
> - 💰 成本优化的模型选择建议
>
> 🙏 **致谢**: 特别感谢 [TauricResearch](https://github.com/TauricResearch) 创建了这个出色的框架！

> 🎉 **TradingAgents** 正式发布！我们收到了大量关于这项工作的询问，对社区的热情表示感谢。
>
> 因此我们决定完全开源这个框架。期待与您共同构建有影响力的项目！

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

<div align="center">

🚀 [TradingAgents框架](#tradingagents-framework) | ⚡ [安装和CLI](#installation-and-cli) | 🎬 [演示视频](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [包使用方法](#tradingagents-package) | 🤝 [贡献指南](#contributing) | 📄 [引用说明](#citation)

</div>

## TradingAgents 框架

TradingAgents 是一个多智能体交易框架，模拟真实世界交易公司的运作动态。通过部署专业的大语言模型驱动的智能体：从基本面分析师、情绪专家、技术分析师，到交易员、风险管理团队，平台协同评估市场状况并为交易决策提供信息。此外，这些智能体还参与动态讨论，以确定最优策略。

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents 框架专为研究目的而设计。交易表现可能因多种因素而异，包括所选择的主干语言模型、模型温度、交易周期、数据质量和其他非确定性因素。[本框架不构成金融、投资或交易建议。](https://tauric.ai/disclaimer/)

我们的框架将复杂的交易任务分解为专业化的角色。这确保系统实现了稳健、可扩展的市场分析和决策制定方法。

### 分析师团队 (Analyst Team)
- **基本面分析师 (Fundamentals Analyst)**: 评估公司财务和绩效指标，识别内在价值和潜在风险信号
- **情绪分析师 (Sentiment Analyst)**: 使用情绪评分算法分析社交媒体和公众情绪，以衡量短期市场情绪
- **新闻分析师 (News Analyst)**: 监控全球新闻和宏观经济指标，解读事件对市场状况的影响
- **技术分析师 (Technical Analyst)**: 利用技术指标（如MACD和RSI）检测交易模式并预测价格走势

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### 研究团队 (Researcher Team)
- 包含看多和看空研究员，他们批判性地评估分析师团队提供的洞察。通过结构化辩论，平衡潜在收益与固有风险。

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 交易员智能体 (Trader Agent)
- 整合分析师和研究员的报告，做出明智的交易决策。基于全面的市场洞察确定交易时机和规模。

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 风险管理和投资组合经理 (Risk Management and Portfolio Manager)
- 通过评估市场波动性、流动性和其他风险因素持续评估投资组合风险。风险管理团队评估并调整交易策略，向投资组合经理提供评估报告以做最终决策。
- 投资组合经理批准/拒绝交易提案。如获批准，订单将发送到模拟交易所并执行。

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## 安装和CLI使用

### 安装

克隆此中文本地化版本：
```bash
git clone https://github.com/aicoder2048/TradingAgentsCN.git
cd TradingAgentsCN
```

使用 uv 安装依赖（推荐）：
```bash
# 如果尚未安装uv，请先安装 (macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装所有依赖并进行版本锁定
uv sync

# 如需添加其他包
uv add package_name
```

> **注意：** 本项目使用现代Python依赖管理工具 `uv` 和 `pyproject.toml`。相比传统的pip，这确保了可重现的安装和更快的依赖解析。

### 必需的API密钥

使用 .env 文件设置您的API密钥（推荐）：
```bash
# 复制示例文件并编辑填入您的API密钥
cp .env.sample .env
# 编辑 .env 文件填入真实的API密钥
```

**.env 文件示例**：
```bash
# 必需的API密钥
FINNHUB_API_KEY=your_finnhub_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# 可选的LLM提供商API密钥
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
MOONSHOT_API_KEY=your_moonshot_api_key_here

# 可选的结果保存目录
TRADINGAGENTS_RESULTS_DIR=./results
```

项目现在支持自动 .env 文件加载，无需手动导出环境变量。

**必需的API密钥：**
- **FinnHub API**: 在 [finnhub.io](https://finnhub.io/) 获取免费版本
- **OpenAI API**: 在 [platform.openai.com](https://platform.openai.com/api-keys) 获取密钥

**可选的API密钥**（用于其他大语言模型提供商）：
- **Anthropic API**: 用于 Claude 模型 - [console.anthropic.com](https://console.anthropic.com/)
- **Google API**: 用于 Gemini 模型 - [aistudio.google.com](https://aistudio.google.com/apikey)
- **DeepSeek API**: 用于 DeepSeek 模型（高性价比选择）- [platform.deepseek.com](https://platform.deepseek.com/api_keys)
- **Moonshot API**: 用于 Kimi K2 模型（海外版）- [platform.moonshot.ai](https://platform.moonshot.ai/)

### CLI 使用

您可以直接运行CLI来体验：
```bash
uv run -m cli.main
```
您将看到一个界面，可以选择股票代码、日期、大语言模型、研究深度等。

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

运行时会出现界面显示实时结果，让您可以跟踪智能体的运行进度。

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents 包使用

### 实现详情

我们使用 LangGraph 构建 TradingAgents 以确保灵活性和模块化。在实验中我们使用 `o1-preview` 和 `gpt-4o` 作为深度思考和快速思考的大语言模型。但是，出于测试目的，我们推荐您使用 `o4-mini` 和 `gpt-4.1-mini` 来节省成本，因为我们的框架会进行**大量**API调用。

### 支持的大语言模型提供商

本框架支持多种大语言模型提供商，用户可以根据成本和性能需求选择：

- **OpenAI**: GPT-4o、o1、o3 系列模型
- **Anthropic**: Claude 3.5/4 系列模型  
- **Google**: Gemini 2.0/2.5 系列模型
- **DeepSeek**: DeepSeek-Chat、DeepSeek-Reasoner（高性价比）
- **Moonshot（海外版）**: Kimi K2 模型（长上下文支持）
- **OpenRouter**: 多种开源模型（免费额度）
- **Ollama**: 本地部署模型支持

> **成本优化建议**: DeepSeek 提供了极具竞争力的定价，是成本敏感用户的理想选择。Moonshot（海外版）的 Kimi K2 模型在长文档处理方面表现优异。

### Python 使用方法

要在您的代码中使用 TradingAgents，可以导入 `tradingagents` 模块并初始化 `TradingAgentsGraph()` 对象。`.propagate()` 函数将返回决策。您可以运行 `main.py`，以下是一个快速示例：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

您也可以调整默认配置来设置自己选择的大语言模型、辩论轮数等。

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 创建自定义配置
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4.1-nano"  # 使用不同模型
config["quick_think_llm"] = "gpt-4.1-nano"  # 使用不同模型
config["max_debate_rounds"] = 1  # 增加辩论轮数
config["online_tools"] = True # 使用在线工具或缓存数据

# 使用自定义配置初始化
ta = TradingAgentsGraph(debug=True, config=config)

# 前向传播
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

> 对于 `online_tools`，我们建议在实验时启用它们，因为它们提供实时数据访问。智能体的离线工具依赖于来自我们 **Tauric TradingDB** 的缓存数据，这是我们用于回测的精选数据集。我们目前正在完善这个数据集，计划与即将推出的项目一起发布。敬请期待！

您可以在 `tradingagents/default_config.py` 中查看完整的配置列表。

## Fork维护指南 (Fork Maintenance Guide)

如果你Fork了这个项目进行自己的开发（比如汉化版本），以下是保持与原仓库同步的最佳实践：

### 同步原仓库更新

定期同步上游仓库的最新更改：

```bash
# 获取上游仓库的最新更改
git fetch upstream

# 合并到你的主分支
git checkout main
git merge upstream/main

# 推送到你的Fork
git push origin main
```

### 处理合并冲突

当你的修改与上游更新冲突时：

1. **识别冲突文件**：Git会标记冲突的文件
2. **手动解决冲突**：编辑文件，保留需要的更改
3. **提交解决方案**：
   ```bash
   git add .
   git commit -m "解决与上游的合并冲突"
   git push origin main
   ```

### 分支管理建议

- **main分支**：保持与上游同步，包含你的核心修改（如汉化）
- **feature分支**：开发新功能时创建独立分支
- **定期同步**：建议每周或在上游有重大更新时同步

### 保持Fork活跃

- 定期检查上游是否有重要的bug修复或新功能
- 在README中说明你的Fork的特色（如汉化支持）
- 考虑将有价值的改进提交回上游项目

> **提示**：通过 `git pull upstream main` 可以快速同步原仓库更新到你的本地分支。

## 贡献指南

我们欢迎社区的贡献！无论是修复错误、改进文档，还是建议新功能，您的投入都有助于让这个项目变得更好。如果您对这一研究领域感兴趣，请考虑加入我们的开源金融AI研究社区 [Tauric Research](https://tauric.ai/)。

## 引用说明

如果您发现 *TradingAgents* 对您有所帮助，请引用我们的工作 :)

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```
