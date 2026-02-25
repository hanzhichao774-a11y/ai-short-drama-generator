# 个人工作区

这是我的个人工作区，包含了多个项目和工具。

## 📁 项目结构

```
clawd/
├── ai-short-drama-generator/    # AI短剧剧本生成器
├── send_ai_news_email.py        # AI新闻邮件发送工具（通用）
├── send_today_ai_news.py        # AI新闻日报发送工具（固定日期）
├── canvas/                      # Canvas可视化项目
├── AGENTS.md                    # Moltbot工作区配置
├── SOUL.md                      # AI助手人格定义
├── USER.md                      # 用户信息
└── TOOLS.md                     # 本地工具配置
```

## 🎬 AI短剧剧本生成器

一个基于AI的短剧剧本生成工具，能将一句话创意转化为抓马、狗血、快节奏的短剧剧本片段。

### 功能特性
- 🚀 一键生成短剧剧本
- 🎭 抓马风格（赘婿逆袭、真假千金等热门套路）
- 💬 流式输出，实时展示生成过程
- 📚 预设模板，快速上手

### 快速开始
```bash
cd ai-short-drama-generator
pip install -r requirements.txt
streamlit run app.py
```

详细说明请查看 [ai-short-drama-generator/README.md](./ai-short-drama-generator/README.md)

## 📧 AI新闻邮件发送工具

自动发送AI领域新闻日报到邮箱的工具。

### send_ai_news_email.py
通用邮件发送工具，支持发送测试邮件和自定义新闻列表。

```bash
# 发送测试邮件
python3 send_ai_news_email.py --test
```

### send_today_ai_news.py
发送固定日期的AI新闻日报（2026年2月24日），内置新闻列表。

```bash
python3 send_today_ai_news.py
```

### 配置说明
- SMTP服务器: smtp.gmail.com
- 发件人: hanzhichao774@gmail.com
- 收件人: 304286127@qq.com

## 🎨 Canvas

可视化展示项目，用于呈现数据和内容。

## 🔧 技术栈

- **Python**: 主要开发语言
- **Streamlit**: Web界面框架
- **通义千问 GLM-4.7**: AI模型
- **Gmail SMTP**: 邮件服务

## 📝 注意事项

- 本仓库包含个人工作配置，请注意敏感信息的保护
- AI短剧生成器需要配置通义千问API Key
- 邮件发送工具需要Gmail应用密码

## 📧 联系方式

- Email: hanzhichao774@gmail.com
- GitHub: [@hanzhichao774-a11y](https://github.com/hanzhichao774-a11y)

---

*最后更新: 2026年2月25日*