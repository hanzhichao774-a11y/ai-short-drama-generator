#!/usr/bin/env python3
"""
发送今天的AI新闻 - 2026年2月25日
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Today's AI news (2026-02-24)
news_list = [
    {
        "title": "白宫经济学家称Citrini AI报告是\"科幻小说\"",
        "source": "Bloomberg",
        "link": "https://www.bloomberg.com/news/articles/2026-02-24/white-house-economist-calls-citrini-ai-report-science-fiction",
        "summary": "一位顶级白宫经济学家将周末关于人工智能风险的报告称为\"科幻小说\"，该报告曾引发股市动荡。"
    },
    {
        "title": "Anthropic称中国AI公司使用1600万次Claude查询复制模型",
        "source": "The Hacker News",
        "link": "https://www.xloggs.com/2026/02/24/breaking-news-cyber-threats-2026-02-24-0200-pst/",
        "summary": "Anthropic在周一表示，他们发现三家AI公司（DeepSeek、Moonshot AI等）发起了\"工业规模的运动\"，利用超过1600万次Claude查询来复制其模型。"
    },
    {
        "title": "贝莱德支持荷兰芯片制造商Axelera AI，融资2.5亿美元",
        "source": "Bloomberg",
        "link": "https://www.bloomberg.com/news/articles/2026-02-24/blackrock-backs-dutch-chipmaker-axelera-ai-in-250-million-round",
        "summary": "荷兰芯片制造商Axelera AI从包括贝莱德在内的投资者处筹集了超过2.5亿美元，用于制造节能型半导体，这些半导体专为在训练后运行AI模型而设计。"
    },
    {
        "title": "科技股反弹：AI担忧缓解推动市场复苏",
        "source": "Bloomberg",
        "link": "https://www.bloomberg.com/news/articles/2026-02-23/stock-market-today-dow-s-p-live-updates",
        "summary": "科技公司的反弹推动了股市复苏，此前市场曾因对人工智能颠覆性影响的担忧而暴跌，消费者信心的改善也提振了市场情绪。"
    },
    {
        "title": "Meta与AMD合作推动AI支出激增",
        "source": "Bloomberg",
        "link": "https://www.bloomberg.com/news/videos/2026-02-24/open-interest-2-24-2026-video",
        "summary": "Meta与AMD的合作关系正在推动AI支出的激增，两家公司在AI硬件和基础设施方面展开深度合作。"
    },
    {
        "title": "Google和OpenAI与国防部谈判扩大AI合作",
        "source": "Media Bias/Fact Check",
        "link": "https://mediabiasfactcheck.com/2026/02/24/media-news-daily-top-stories-for-02-24-2026/",
        "summary": "据报道，Google和OpenAI正在与国防部谈判扩大合作，国防部加速努力确保替代AI合作伙伴。"
    },
    {
        "title": "泽连斯基声称乌克兰强制动员的视频大多是俄罗斯用AI生成的",
        "source": "Pravda",
        "link": "https://news-pravda.com/world/2026/02/24/2094747.html",
        "summary": "乌克兰总统泽连斯基声称，关于乌克兰强制动员的大多数视频都是俄罗斯使用AI生成的虚假信息。"
    },
    {
        "title": "AI技术对工作的影响：不减负反而加剧",
        "source": "Harvard Business Review",
        "link": "https://hbr.org/2026/02/ai-doesnt-reduce-work-it-intensifies-it",
        "summary": "AI的承诺之一是减少工作量，让员工专注于更高价值、更有吸引力的任务。但新研究表明，AI工具不会减少工作，反而会持续加剧工作强度。"
    },
    {
        "title": "路透社AI新闻板块：最新头条和发展动态",
        "source": "Reuters",
        "link": "https://www.reuters.com/technology/artificial-intelligence/",
        "summary": "路透社AI新闻板块提供人工智能领域的最新头条和发展动态，涵盖技术创新、市场应用和政策变化。"
    },
    {
        "title": "财富杂志AI专栏：人工智能趋势与市场影响",
        "source": "Fortune",
        "link": "https://fortune.com/section/artificial-intelligence/",
        "summary": "财富杂志AI专栏专注于人工智能趋势和市场影响，提供深入的分析和行业洞察。"
    }
]

# Send email
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "hanzhichao774@gmail.com"
SMTP_PASSWORD = "ockxicvn ymohykcy"
RECIPIENT = "304286127@qq.com"

today = datetime.now().strftime('%Y年%m月%d日')
subject = f"【AI新闻日报】2026年2月24日的AI新闻"

html_content = f"""
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif; max-width: 700px; margin: 0 auto; padding: 30px; background-color: #f8f9fa;">
    <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h1 style="color: #e67e22; margin: 0 0 20px 0; border-bottom: 3px solid #e67e22; padding-bottom: 10px;">
            🦞 {subject}
        </h1>
"""

for i, news in enumerate(news_list, 1):
    html_content += f"""
        <div style="margin-bottom: 25px; padding: 20px; background-color: #f8f9fa; border-left: 4px solid #e67e22; border-radius: 5px;">
            <h3 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 18px;">
                {i}. {news.get('title', '无标题')}
            </h3>
            <p style="color: #7f8c8d; margin: 0 0 10px 0; font-size: 14px;">
                <strong>来源:</strong> {news.get('source', '未知来源')}
            </p>
            <p style="margin: 0 0 15px 0;">
                <strong>链接:</strong> <a href="{news.get('link', '#')}" style="color: #3498db; text-decoration: none;">{news.get('link', '#')}</a>
            </p>
            <p style="color: #34495e; line-height: 1.6; margin: 0;">
                <strong>摘要:</strong> {news.get('summary', '暂无摘要')}
            </p>
        </div>
    """

html_content += f"""
        <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">
        <p style="color: #7f8c8d; font-size: 12px; text-align: center; margin: 0;">
            此邮件由 <strong>Clawd AI Assistant</strong> 自动生成 🦞<br>
            发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
    </div>
</body>
</html>
"""

try:
    msg = MIMEMultipart()
    msg['From'] = f"Clawd AI Assistant <{SMTP_USER}>"
    msg['To'] = RECIPIENT
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

    print(f"✅ 邮件发送成功！收件人: {RECIPIENT}")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")