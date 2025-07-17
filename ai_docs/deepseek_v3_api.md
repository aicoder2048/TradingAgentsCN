当然！下面是将您提供的 **DeepSeek API Quickstart 文档** 转换成简洁、中文 Markdown 格式的版本，仅保留 **Python 相关内容**，并专注于 Python 环境：

---

# 快速开始：DeepSeek API

DeepSeek API 使用与 OpenAI 兼容的 API 格式。通过简单修改配置，您可以使用 OpenAI SDK 或其他兼容 OpenAI API 的软件来调用 DeepSeek API。

## 基本参数

| 参数         | 说明                                                                                                    |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| `base_url` | `https://api.deepseek.com`<br>*为了兼容 OpenAI，也可以使用 `https://api.deepseek.com/v1`，但请注意，这里的 `v1` 与模型版本无关* |
| `api_key`  | 需申请 API Key (通常有较好的免费配额)                                                                      |

### 可用模型

* `deepseek-chat`：对应模型版本 **DeepSeek-V3-0324**，使用时 `model="deepseek-chat"`。
* `deepseek-reasoner`：对应模型版本 **DeepSeek-R1-0528**，使用时 `model="deepseek-reasoner"`。

## 调用 Chat API 示例

成功获取 API Key 后，可以使用以下 Python 示例脚本调用 DeepSeek API（此示例为非流式，若需流式返回可将 `stream` 参数设为 `True`）：

```python
# 请先安装 OpenAI SDK: pip install openai

from openai import OpenAI

client = OpenAI(
    api_key="<DeepSeek API Key>",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
```

---

✅ **温馨提示**

> 本文仅供学习和参考。具体使用请根据实际环境调整配置，并建议查阅 [DeepSeek 官方文档](https://api.deepseek.com) 以获取最新信息。

---

如需我帮您再加上 **详细注释或目录导航**，随时告诉我！👍
