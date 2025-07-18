#!/usr/bin/env python3
"""
合并交易分析子报告的工具

这个工具将多个子报告合并成一个完整的交易分析报告，
并支持导出为 Markdown 和 HTML 格式。
"""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary
import subprocess
from datetime import datetime
import re

# 初始化控制台和CLI应用
console = Console()
app = typer.Typer(
    name="gen_final_report",
    help="合并交易分析子报告并生成最终报告",
    add_completion=False,
)

# 定义必需的子报告文件
REQUIRED_REPORTS = [
    ("fundamentals_report.md", "基本面分析报告"),
    ("market_report.md", "技术面分析报告"),
    ("news_report.md", "新闻分析报告"),
    ("sentiment_report.md", "情绪分析报告"),
    ("investment_plan.md", "投资策略报告"),
    ("trader_investment_plan.md", "交易员执行方案"),
    ("final_trade_decision.md", "最终交易决策"),
]


def check_required_files(report_dir: Path) -> tuple[bool, list]:
    """
    检查必需的报告文件是否存在
    
    Args:
        report_dir: 报告目录路径
        
    Returns:
        tuple: (是否所有文件都存在, 缺失文件列表)
    """
    missing_files = []
    
    for filename, description in REQUIRED_REPORTS:
        file_path = report_dir / filename
        if not file_path.exists():
            missing_files.append((filename, description))
    
    return len(missing_files) == 0, missing_files


def extract_info_from_path(report_dir: Path) -> tuple[str, str]:
    """
    从报告目录路径提取股票代码和日期
    
    Args:
        report_dir: 报告目录路径
        
    Returns:
        tuple: (股票代码, 日期)
    """
    # 期望的路径格式: results/{TICKER}/{DATE}/reports
    parts = report_dir.parts
    
    # 尝试从路径中提取信息
    ticker = "UNKNOWN"
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 查找 results 在路径中的位置
    try:
        results_idx = parts.index("results")
        if results_idx + 2 < len(parts):
            ticker = parts[results_idx + 1]
            date_str = parts[results_idx + 2]
            # 验证日期格式
            if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                date = date_str
    except ValueError:
        # 如果找不到 results，使用默认值
        pass
    
    return ticker, date


def merge_reports(report_dir: Path, ticker: str, date: str) -> str:
    """
    合并所有子报告成为一个完整的报告
    
    Args:
        report_dir: 报告目录路径
        ticker: 股票代码
        date: 分析日期
        
    Returns:
        str: 合并后的报告内容
    """
    # 读取当前股价（从基本面报告中提取）
    fundamentals_path = report_dir / "fundamentals_report.md"
    current_price = None
    
    try:
        with open(fundamentals_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # 定义多个匹配模式以适应不同的报告格式
            patterns = [
                # 匹配表格格式：| 当前股价 | 328.8美元
                r'\|\s*当前股价\s*\|\s*([\d.]+)美元',
                # 匹配粗体格式：**当前股价**: 328.8
                r'\*\*当前股价\*\*[:\s]*([\d.]+)',
                # 匹配直接文本：股价为328.80美元
                r'股价为([\d.]+)美元',
                # 匹配开头描述：TSLA的股价为328.80美元
                r'[A-Z]+的股价为([\d.]+)美元',
                # 匹配：当前股价为328.8美元
                r'当前股价为([\d.]+)美元'
            ]
            
            # 尝试所有模式
            for pattern in patterns:
                price_match = re.search(pattern, content)
                if price_match:
                    current_price = f"${price_match.group(1)}"
                    break
            
            # 如果仍无法提取，尝试从文件第一行提取
            if not current_price:
                lines = content.split('\n')
                if lines:
                    # 查找第一行中的价格信息
                    first_line_match = re.search(r'([\d.]+)美元', lines[0])
                    if first_line_match:
                        current_price = f"${first_line_match.group(1)}"
    except Exception as e:
        console.print(f"[yellow]警告: 读取基本面报告时出错: {e}[/yellow]")
    
    # 如果无法提取股价，使用明确的错误提示
    if not current_price:
        current_price = "未能提取（请检查基本面报告）"
    
    # 构建报告头部
    merged_content = f"""# {ticker} 完整交易分析报告

**股票代码**: {ticker}  
**分析日期**: {date}  
**当前股价**: {current_price}

---

## 目录

1. [基本面分析](#1-基本面分析)
2. [技术面分析](#2-技术面分析)
3. [新闻分析](#3-新闻分析)
4. [情绪分析](#4-情绪分析)
5. [投资策略制定](#5-投资策略制定)
6. [交易员执行计划](#6-交易员执行计划)
7. [最终交易决策](#7-最终交易决策)

---

"""
    
    # 定义每个部分的标题
    section_titles = [
        "## 1. 基本面分析\n\n",
        "## 2. 技术面分析\n\n",
        "## 3. 新闻分析\n\n",
        "## 4. 情绪分析\n\n",
        "## 5. 投资策略制定\n\n",
        "## 6. 交易员执行计划\n\n",
        "## 7. 最终交易决策\n\n",
    ]
    
    # 按顺序合并报告
    for i, (filename, description) in enumerate(REQUIRED_REPORTS):
        file_path = report_dir / filename
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
            # 添加分节标题
            merged_content += section_titles[i]
            
            # 添加内容
            merged_content += content
            
            # 添加分隔线（最后一个除外）
            if i < len(REQUIRED_REPORTS) - 1:
                merged_content += "\n\n---\n\n"
            
        except Exception as e:
            console.print(f"[red]读取文件 {filename} 时出错: {e}[/red]")
            return ""
    
    # 添加报告总结
    merged_content += f"""

---

## 报告总结

本报告从基本面分析出发，结合技术面指标，通过牛熊双方辩论，最终得出交易决策。

*报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*"""
    
    return merged_content


def check_pandoc_installed() -> bool:
    """
    检查系统是否安装了 pandoc
    
    Returns:
        bool: 是否安装了 pandoc
    """
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def generate_simple_css() -> str:
    """
    生成简单样式的CSS
    
    Returns:
        str: 简单CSS样式内容
    """
    return """
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", 
                 "PingFang SC", "Microsoft YaHei", sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5rem;
    text-align: left;
}

th {
    background-color: #f5f5f5;
}

code {
    background-color: #f5f5f5;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
}

pre {
    background-color: #f5f5f5;
    padding: 1rem;
    overflow-x: auto;
}

blockquote {
    border-left: 4px solid #ddd;
    margin: 1rem 0;
    padding-left: 1rem;
}

@media print {
    body {
        font-size: 11pt;
        color: black;
        max-width: 100%;
    }
}
</style>
"""


def generate_custom_css(theme: str) -> str:
    """
    生成自定义CSS样式
    
    Args:
        theme: 主题名称 (light/dark/auto)
        
    Returns:
        str: CSS样式内容
    """
    base_css = """
<style>
/* 基础样式 */
:root {
    --max-width: 1400px;
    --content-width: 90%;
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", 
                   "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                   "Helvetica Neue", Helvetica, Arial, sans-serif;
}

body {
    font-family: var(--font-family);
    line-height: 1.6;
    margin: 0;
    padding: 0;
    max-width: var(--max-width);
    width: var(--content-width);
    margin: 0 auto;
    padding: 2rem 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
    :root {
        --content-width: 95%;
    }
    body {
        padding: 1rem 0.5rem;
    }
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.25rem; }
}

@media (min-width: 1600px) {
    :root {
        --max-width: 1600px;
        --content-width: 85%;
    }
}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

h1 { font-size: 2.5rem; border-bottom: 3px solid var(--border-color); padding-bottom: 0.5rem; }
h2 { font-size: 2rem; border-bottom: 2px solid var(--border-color); padding-bottom: 0.3rem; }
h3 { font-size: 1.5rem; }

/* 表格美化 */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1.5rem 0;
    font-size: 0.95em;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

th {
    background-color: var(--header-bg);
    font-weight: 600;
}

tr:hover {
    background-color: var(--row-hover);
}

/* 代码块 */
pre {
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    background-color: var(--code-bg);
    border: 1px solid var(--border-color);
}

code {
    font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
    font-size: 0.9em;
}

/* 引用块 */
blockquote {
    margin: 1rem 0;
    padding: 0.5rem 1rem;
    border-left: 4px solid var(--accent-color);
    background-color: var(--quote-bg);
}

/* 链接 */
a {
    color: var(--link-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* 目录样式 */
#TOC {
    background-color: var(--toc-bg);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 2rem;
}

#TOC ul {
    list-style: none;
    padding-left: 1rem;
}

#TOC a {
    color: var(--text-color);
}

/* 列表样式 */
ul, ol {
    margin: 1rem 0;
    padding-left: 2rem;
}

li {
    margin: 0.5rem 0;
}

/* 分隔线 */
hr {
    border: none;
    border-top: 2px solid var(--border-color);
    margin: 2rem 0;
}
"""
    
    light_theme = """
/* 浅色主题 */
body {
    --bg-color: #ffffff;
    --text-color: #1a1a1a;
    --header-bg: #f6f8fa;
    --border-color: #e1e4e8;
    --link-color: #0366d6;
    --code-bg: #f6f8fa;
    --quote-bg: #f6f8fa;
    --row-hover: #f6f8fa;
    --toc-bg: #f6f8fa;
    --accent-color: #0366d6;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}

/* 打印优化 */
@media print {
    body {
        font-size: 11pt;
        line-height: 1.5;
        color: black !important;
        background: white !important;
        max-width: 100%;
        width: 100%;
        padding: 0;
        margin: 0;
    }
    
    #TOC {
        display: none;
    }
    
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
        margin-top: 1.5rem;
    }
    
    table, figure, pre {
        page-break-inside: avoid;
    }
    
    a {
        color: black !important;
        text-decoration: none !important;
    }
    
    a[href]:after {
        content: " (" attr(href) ")";
        font-size: 0.8em;
        color: #666;
    }
}
"""
    
    dark_theme = """
/* 深色主题 */
body {
    --bg-color: #0d1117;
    --text-color: #c9d1d9;
    --header-bg: #161b22;
    --border-color: #30363d;
    --link-color: #58a6ff;
    --code-bg: #161b22;
    --quote-bg: #161b22;
    --row-hover: #161b22;
    --toc-bg: #161b22;
    --accent-color: #58a6ff;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}

/* 深色主题下的表格 */
table {
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* 深色主题不适合打印，打印时强制使用浅色 */
@media print {
    body {
        --bg-color: #ffffff !important;
        --text-color: #1a1a1a !important;
        background-color: white !important;
        color: black !important;
    }
    
    * {
        background-color: white !important;
        color: black !important;
    }
}
"""
    
    auto_theme = """
/* 自动主题 - 根据系统偏好 */
@media (prefers-color-scheme: light) {
""" + light_theme + """
}

@media (prefers-color-scheme: dark) {
""" + dark_theme + """
}
"""
    
    # 添加更多主题色彩
    bamboo_green_theme = """
/* 竹绿色主题 */
body {
    --bg-color: #f0f7f0;
    --text-color: #1a3d1a;
    --header-bg: #d4e8d4;
    --border-color: #8fc08f;
    --link-color: #2d7a2d;
    --code-bg: #e8f3e8;
    --quote-bg: #e1f0e1;
    --row-hover: #deedde;
    --toc-bg: #e8f3e8;
    --accent-color: #4a9d4a;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    ocean_blue_theme = """
/* 海洋蓝主题 */
body {
    --bg-color: #f0f8ff;
    --text-color: #0c2340;
    --header-bg: #cfe7ff;
    --border-color: #87ceeb;
    --link-color: #0066cc;
    --code-bg: #e6f3ff;
    --quote-bg: #dbeeff;
    --row-hover: #d4e9ff;
    --toc-bg: #e6f3ff;
    --accent-color: #4682b4;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    warm_apricot_theme = """
/* 暖杏黄主题 */
body {
    --bg-color: #fef9f3;
    --text-color: #3d2914;
    --header-bg: #ffefd5;
    --border-color: #ddb892;
    --link-color: #cd853f;
    --code-bg: #fff5e6;
    --quote-bg: #ffefdc;
    --row-hover: #ffe9d0;
    --toc-bg: #fff5e6;
    --accent-color: #d2691e;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    sakura_pink_theme = """
/* 樱花粉主题 */
body {
    --bg-color: #fdf5f8;
    --text-color: #4a1f2e;
    --header-bg: #ffe4f1;
    --border-color: #ffb6d9;
    --link-color: #d1477a;
    --code-bg: #ffeef6;
    --quote-bg: #ffe8f2;
    --row-hover: #ffdded;
    --toc-bg: #ffeef6;
    --accent-color: #ff69b4;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    dawn_orange_theme = """
/* 晨曦橙主题 */
body {
    --bg-color: #fff8f0;
    --text-color: #3d2414;
    --header-bg: #ffe4cc;
    --border-color: #ffb380;
    --link-color: #ff6b35;
    --code-bg: #fff0e5;
    --quote-bg: #ffe9d9;
    --row-hover: #ffe0cc;
    --toc-bg: #fff0e5;
    --accent-color: #ff8c42;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    violet_theme = """
/* 紫罗兰主题 */
body {
    --bg-color: #f8f5ff;
    --text-color: #2d1b69;
    --header-bg: #e8deff;
    --border-color: #b794f6;
    --link-color: #6b46c1;
    --code-bg: #f2ecff;
    --quote-bg: #ebe4ff;
    --row-hover: #e3d9ff;
    --toc-bg: #f2ecff;
    --accent-color: #8b5cf6;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    mint_cyan_theme = """
/* 薄荷青主题 */
body {
    --bg-color: #f0fffa;
    --text-color: #0d3d2e;
    --header-bg: #ccf5e8;
    --border-color: #66d9bf;
    --link-color: #00a86b;
    --code-bg: #e0f9f0;
    --quote-bg: #d6f5ea;
    --row-hover: #ccf0e5;
    --toc-bg: #e0f9f0;
    --accent-color: #00cc88;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    aurora_purple_theme = """
/* 极光紫主题 */
body {
    --bg-color: #1a0f2e;
    --text-color: #e0d5f7;
    --header-bg: #2d1f4e;
    --border-color: #6441a5;
    --link-color: #9b72cf;
    --code-bg: #251a3e;
    --quote-bg: #2a1d47;
    --row-hover: #342454;
    --toc-bg: #251a3e;
    --accent-color: #b380ff;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}

/* 极光紫主题下的特殊处理 */
table {
    box-shadow: 0 2px 8px rgba(180, 128, 255, 0.3);
}

@media print {
    body {
        background-color: white !important;
        color: black !important;
    }
}
"""
    
    steel_gray_theme = """
/* 钢铁灰主题 */
body {
    --bg-color: #f5f5f7;
    --text-color: #1c1c1e;
    --header-bg: #e5e5e7;
    --border-color: #c7c7cc;
    --link-color: #007aff;
    --code-bg: #ededf0;
    --quote-bg: #e8e8eb;
    --row-hover: #e0e0e3;
    --toc-bg: #ededf0;
    --accent-color: #5856d6;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}
"""
    
    rock_gray_theme = """
/* 岩石灰主题 */
body {
    --bg-color: #2c2c2e;
    --text-color: #e5e5e7;
    --header-bg: #3a3a3c;
    --border-color: #48484a;
    --link-color: #64d2ff;
    --code-bg: #363638;
    --quote-bg: #38383a;
    --row-hover: #424245;
    --toc-bg: #363638;
    --accent-color: #0a84ff;
    
    background-color: var(--bg-color);
    color: var(--text-color);
}

/* 岩石灰主题下的特殊处理 */
table {
    box-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

@media print {
    body {
        background-color: white !important;
        color: black !important;
    }
}
"""
    
    css_map = {
        "light": base_css + light_theme,
        "dark": base_css + dark_theme,
        "auto": base_css + auto_theme,
        "bamboo": base_css + bamboo_green_theme,
        "ocean": base_css + ocean_blue_theme,
        "apricot": base_css + warm_apricot_theme,
        "sakura": base_css + sakura_pink_theme,
        "dawn": base_css + dawn_orange_theme,
        "violet": base_css + violet_theme,
        "mint": base_css + mint_cyan_theme,
        "aurora": base_css + aurora_purple_theme,
        "steel": base_css + steel_gray_theme,
        "rock": base_css + rock_gray_theme
    }
    
    return css_map.get(theme, css_map["light"]) + "\n</style>"


def convert_to_html(md_file: Path, ticker: str, date: str, style: str = "professional", theme: str = "light") -> Path:
    """
    使用 pandoc 将 Markdown 转换为 HTML
    
    Args:
        md_file: Markdown 文件路径
        ticker: 股票代码
        date: 分析日期
        style: 样式 (simple/professional)
        theme: 主题 (light/dark/auto) - 仅在professional样式下有效
        
    Returns:
        Path: 生成的 HTML 文件路径
    """
    # 根据样式和主题生成文件名
    if style == "simple":
        html_filename = f"{md_file.stem}_simple.html"
    else:
        html_filename = f"{md_file.stem}_{theme}.html" if theme != "light" else f"{md_file.stem}.html"
    
    html_file = md_file.parent / html_filename
    title = f"TradingAgent分析: {ticker} on {date}"
    
    # 根据样式生成CSS
    if style == "simple":
        css_content = generate_simple_css()
    else:
        css_content = generate_custom_css(theme)
    
    # 创建临时CSS文件
    css_file = md_file.parent / f".temp_style_{theme}.css"
    try:
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(css_content)
        
        # 构建 pandoc 命令
        cmd = [
            "pandoc",
            str(md_file),
            "-o", str(html_file),
            "--standalone",
            "--self-contained",  # 生成独立HTML文件
            "--metadata", f"title={title}",
            "--metadata", f"lang=zh-CN",
            "--toc",  # 添加目录
            "--toc-depth=2",  # 目录深度
            "--highlight-style", "pygments" if theme == "light" else "zenburn",
            "--include-in-header", str(css_file),
            "--mathjax",  # 支持数学公式
            "--wrap=none",  # 不换行
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return html_file
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]转换 HTML 时出错: {e.stderr}[/red]")
        raise
    finally:
        # 清理临时文件
        if css_file.exists():
            css_file.unlink()


def interactive_menu():
    """
    交互式菜单，让用户输入参数
    
    Returns:
        tuple: (report_dir, style, theme)
    """
    console.print(Panel.fit(
        "[bold cyan]TradingAgents 报告合并工具 - 交互模式[/bold cyan]",
        border_style="cyan"
    ))
    
    # 输入报告目录
    console.print("\n[yellow]请输入报告目录路径[/yellow]")
    console.print("[dim]例如: results/NVDA/2025-07-17/reports[/dim]")
    
    report_dir = questionary.text(
        "报告目录:",
        validate=lambda x: len(x.strip()) > 0 or "请输入有效的目录路径"
    ).ask()
    
    if not report_dir:
        console.print("[red]未提供目录路径，退出...[/red]")
        raise typer.Exit(1)
    
    # 选择样式
    style = questionary.select(
        "选择报告样式:",
        choices=[
            questionary.Choice("简单样式 - 清爽简洁，快速生成", value="simple"),
            questionary.Choice("专业样式 - 美观大气，支持主题", value="professional")
        ]
    ).ask()
    
    if not style:
        console.print("[red]未选择样式，退出...[/red]")
        raise typer.Exit(1)
    
    theme = "light"  # 默认主题
    
    # 如果选择专业样式，询问主题
    if style == "professional":
        theme = questionary.select(
            "选择主题:",
            choices=[
                questionary.Choice("💡 浅色主题 - 适合打印和日间阅读", value="light"),
                questionary.Choice("🌙 深色主题 - 适合夜间阅读", value="dark"),
                questionary.Choice("🔄 自动主题 - 根据系统设置", value="auto"),
                questionary.Choice("🎋 竹绿色主题 - 清新自然", value="bamboo"),
                questionary.Choice("🌊 海洋蓝主题 - 深邃宁静", value="ocean"),
                questionary.Choice("🍑 暖杏黄主题 - 温暖舒适", value="apricot"),
                questionary.Choice("🌸 樱花粉主题 - 优雅浪漫", value="sakura"),
                questionary.Choice("🌅 晨曦橙主题 - 活力充沛", value="dawn"),
                questionary.Choice("🔮 紫罗兰主题 - 神秘优雅", value="violet"),
                questionary.Choice("🌿 薄荷青主题 - 清爽醒目", value="mint"),
                questionary.Choice("🌌 极光紫主题 - 深邃神秘", value="aurora"),
                questionary.Choice("🔧 钢铁灰主题 - 专业现代", value="steel"),
                questionary.Choice("🗿 岩石灰主题 - 沉稳大气", value="rock")
            ]
        ).ask()
        
        if not theme:
            console.print("[red]未选择主题，退出...[/red]")
            raise typer.Exit(1)
    
    return report_dir, style, theme


def process_report(report_dir: str, style: str = "professional", theme: str = "light"):
    """
    处理报告的核心函数
    
    Args:
        report_dir: 报告目录路径
        style: 样式 (simple/professional)
        theme: 主题 (light/dark/auto)
    """
    # 转换为 Path 对象
    report_path = Path(report_dir)
    
    # 显示处理信息
    console.print(Panel.fit(
        "[bold cyan]TradingAgents 报告合并工具[/bold cyan]\n"
        f"正在处理报告目录...\n"
        f"样式: {style} | 主题: {theme if style == 'professional' else 'N/A'}",
        border_style="cyan"
    ))
    
    # 检查目录是否存在
    if not report_path.exists():
        console.print(f"[red]错误: 目录不存在 - {report_path}[/red]")
        raise typer.Exit(1)
    
    if not report_path.is_dir():
        console.print(f"[red]错误: 路径不是目录 - {report_path}[/red]")
        raise typer.Exit(1)
    
    # 提取股票代码和日期
    ticker, date = extract_info_from_path(report_path)
    console.print(f"[green]股票代码: {ticker}[/green]")
    console.print(f"[green]分析日期: {date}[/green]")
    
    if style == "professional":
        console.print(f"[green]HTML主题: {theme}[/green]")
        
        # 显示主题说明
        theme_descriptions = {
            "light": "浅色主题 - 适合打印和日间阅读",
            "dark": "深色主题 - 适合夜间阅读，打印时自动转换为浅色",
            "auto": "自动主题 - 根据系统设置自动切换",
            "bamboo": "竹绿色主题 - 清新自然的绿色调",
            "ocean": "海洋蓝主题 - 深邃宁静的蓝色调",
            "apricot": "暖杏黄主题 - 温暖舒适的杏黄色调",
            "sakura": "樱花粉主题 - 优雅浪漫的粉色调",
            "dawn": "晨曦橙主题 - 活力充沛的橙色调",
            "violet": "紫罗兰主题 - 神秘优雅的紫色调",
            "mint": "薄荷青主题 - 清爽醒目的青色调",
            "aurora": "极光紫主题 - 深邃神秘的夜空紫",
            "steel": "钢铁灰主题 - 专业现代的金属灰",
            "rock": "岩石灰主题 - 沉稳大气的深灰色"
        }
        console.print(f"[dim]{theme_descriptions.get(theme, '')}[/dim]")
    else:
        console.print("[green]样式: 简单样式[/green]")
        console.print("[dim]清爽简洁的报告样式[/dim]")
    
    console.print()
    
    # 检查必需文件
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]检查必需文件...", total=None)
        
        all_files_exist, missing_files = check_required_files(report_path)
        progress.update(task, completed=True)
    
    if not all_files_exist:
        console.print("[red]错误: 缺少以下必需的报告文件:[/red]")
        
        # 显示缺失文件表格
        table = Table(title="缺失文件列表", show_header=True, header_style="bold red")
        table.add_column("文件名", style="cyan")
        table.add_column("说明", style="yellow")
        
        for filename, description in missing_files:
            table.add_row(filename, description)
        
        console.print(table)
        console.print("\n[yellow]请确保所有报告文件都已生成后再运行此工具。[/yellow]")
        raise typer.Exit(1)
    
    console.print("[green]✓ 所有必需文件都已找到[/green]\n")
    
    # 合并报告
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]合并报告文件...", total=None)
        
        merged_content = merge_reports(report_path, ticker, date)
        if not merged_content:
            console.print("[red]错误: 合并报告失败[/red]")
            raise typer.Exit(1)
        
        # 生成输出文件名
        output_filename = f"complete_trading_analysis_{date}.md"
        output_path = report_path / output_filename
        
        # 写入合并后的内容
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(merged_content)
        
        progress.update(task, completed=True)
    
    console.print(f"[green]✓ Markdown 报告已生成:[/green]")
    console.print(f"  [cyan]{output_path.absolute()}[/cyan]\n")
    
    # 转换为 HTML
    if not check_pandoc_installed():
        console.print("[yellow]警告: 未检测到 pandoc 工具[/yellow]")
        console.print("[yellow]请使用以下命令安装 pandoc:[/yellow]")
        console.print("[cyan]  brew install pandoc[/cyan]")
        console.print("\n[yellow]Markdown 报告已生成，但无法转换为 HTML 格式。[/yellow]")
        raise typer.Exit(0)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]转换为 HTML 格式...", total=None)
        
        try:
            html_path = convert_to_html(output_path, ticker, date, style, theme)
            progress.update(task, completed=True)
            
            console.print(f"[green]✓ HTML 报告已生成:[/green]")
            console.print(f"  [cyan]{html_path.absolute()}[/cyan]\n")
            
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"[red]HTML 转换失败: {e}[/red]")
            console.print("[yellow]Markdown 报告已成功生成。[/yellow]")
    
    # 显示完成信息
    if style == "simple":
        html_suffix = "_simple.html"
    else:
        html_suffix = f"_{theme}.html" if theme != "light" else ".html"
    
    console.print(Panel.fit(
        "[bold green]报告合并完成！[/bold green]\n\n"
        f"生成的文件:\n"
        f"• Markdown: {output_filename}\n"
        f"• HTML ({style}样式{', ' + theme + '主题' if style == 'professional' else ''}): "
        f"{output_filename.replace('.md', html_suffix)}",
        border_style="green"
    ))


@app.command()
def main(
    report_dir: Optional[str] = typer.Argument(None, help="报告目录路径 (例如: results/NVDA/2025-07-17)"),
    style: str = typer.Option("professional", "--style", "-s", help="HTML样式 (simple/professional)"),
    theme: str = typer.Option("light", "--theme", "-t", help="颜色主题"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="交互式菜单模式")
):
    """
    合并交易报告并生成HTML版本
    
    默认运行交互式模式，或指定目录直接处理。
    
    支持的主题：
    - light: 浅色主题（适合打印）
    - dark: 深色主题
    - auto: 自动跟随系统
    - bamboo: 竹绿色主题
    - ocean: 海洋蓝主题
    - apricot: 暖杏黄主题
    - sakura: 樱花粉主题
    - dawn: 晨曦橙主题
    - violet: 紫罗兰主题
    - mint: 薄荷青主题
    - aurora: 极光紫主题
    - steel: 钢铁灰主题
    - rock: 岩石灰主题
    """
    # 如果没有提供目录参数，默认进入交互式模式
    if not report_dir:
        report_dir, style, theme = interactive_menu()
        process_report(report_dir, style, theme)
    elif interactive:
        # 用户明确指定了 --interactive 标志
        report_dir, style, theme = interactive_menu()
        process_report(report_dir, style, theme)
    else:
        # 验证参数
        valid_themes = ["light", "dark", "auto", "bamboo", "ocean", "apricot", 
                       "sakura", "dawn", "violet", "mint", "aurora", "steel", "rock"]
        if theme not in valid_themes:
            console.print(f"[red]错误: 无效的主题 '{theme}'。[/red]")
            console.print(f"[yellow]可用主题: {', '.join(valid_themes)}[/yellow]")
            raise typer.Exit(1)
        
        if style not in ["simple", "professional"]:
            console.print(f"[red]错误: 无效的样式 '{style}'。请使用 simple 或 professional。[/red]")
            raise typer.Exit(1)
        
        # 使用命令行参数处理
        process_report(report_dir, style, theme)


if __name__ == "__main__":
    app()