#!/usr/bin/env python3
"""
AI News Email Sender
发送AI新闻邮件脚本
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import sys
import argparse

# Gmail SMTP 配置
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "hanzhichao774@gmail.com"
SMTP_PASSWORD = "ockxicvn ymohykcy"

# 收件人
RECIPIENT = "304286127@qq.com"

def send_email(subject, content, html=False):
    """
    发送邮件

    Args:
        subject: 邮件主题
        content: 邮件内容
        html: 是否为HTML格式
    """
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = f"Clawd AI Assistant <{SMTP_USER}>"
        msg['To'] = RECIPIENT
        msg['Subject'] = subject

        # 添加邮件正文
        if html:
            msg.attach(MIMEText(content, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

        # 连接SMTP服务器
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # 启用TLS加密
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()

        print(f"✅ 邮件发送成功！收件人: {RECIPIENT}")
        return True

    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def send_test_email():
    """发送测试邮件"""
    subject = "【测试】Clawd 邮件服务测试"
    content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #e67e22;">🦞 测试邮件</h2>
        <p>这是一封来自 Clawd AI Assistant 的测试邮件。</p>
        <hr>
        <p>如果您收到这封邮件，说明邮件服务配置成功！</p>
        <p style="color: #7f8c8d; font-size: 12px;">
            发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            发送人: Clawd AI Assistant 🦞
        </p>
    </body>
    </html>
    """
    return send_email(subject, content, html=True)

def send_ai_news(news_list, date_str=None):
    """
    发送AI新闻邮件

    Args:
        news_list: 新闻列表，每个元素为包含 title, source, link, summary 的字典
        date_str: 日期字符串，如果为None则使用昨天
    """
    if date_str is None:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime('%Y年%m月%d日')

    subject = f"【AI新闻日报】{date_str}的AI新闻"

    # 构建HTML内容
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

    return send_email(subject, html_content, html=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='发送AI新闻邮件')
    parser.add_argument('--test', action='store_true', help='发送测试邮件')
    args = parser.parse_args()

    if args.test:
        send_test_email()
    else:
        print("请使用 --test 参数发送测试邮件")
        print("示例: python3 /home/admin/clawd/send_ai_news_email.py --test")