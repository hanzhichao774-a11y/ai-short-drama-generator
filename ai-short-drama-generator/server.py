"""
AI短剧剧本生成器 - 极简Web界面（无依赖版本）
使用Python内置的http.server和cgi模块
"""

import http.server
import socketserver
import json
import urllib.parse
from generator import generate_script, format_script

# 全局变量
last_idea = ""
generated_script = None

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 AI短剧剧本生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; padding: 30px; background: rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .section { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        h2 { color: #667eea; margin-bottom: 20px; }
        textarea { width: 100%; padding: 15px; border: 2px solid #e0e0e0; border-radius: 8px; min-height: 150px; font-family: inherit; }
        .preset-buttons { display: flex; flex-wrap: wrap; gap: 10px; margin: 15px 0; }
        .preset-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; }
        .generate-btn { width: 100%; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; padding: 15px; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; }
        .script-output { background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; font-family: 'Courier New', monospace; line-height: 1.8; white-space: pre-wrap; min-height: 400px; max-height: 600px; overflow-y: auto; }
        .loading { text-align: center; padding: 40px; }
        @media (max-width: 768px) { .main-content { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 AI短剧剧本生成器</h1>
            <p>输入创意，一键生成抓马十足的短剧剧本</p>
        </div>
        <div class="main-content">
            <div class="section">
                <h2>✍️ 输入创意</h2>
                <div class="preset-buttons">
                    <button class="preset-btn" onclick="setTemplate('赘婿逆袭')">赘婿逆袭</button>
                    <button class="preset-btn" onclick="setTemplate('真假千金')">真假千金</button>
                    <button class="preset-btn" onclick="setTemplate('霸总追妻')">霸总追妻</button>
                    <button class="preset-btn" onclick="setTemplate('豪门弃子')">豪门弃子</button>
                    <button class="preset-btn" onclick="setTemplate('师姐的秘密')">师姐的秘密</button>
                </div>
                <textarea id="userIdea" placeholder="输入你的创意想法...">{{ idea }}</textarea>
                <button class="generate-btn" id="generateBtn" onclick="generateScript()">🎬 生成剧本</button>
            </div>
            <div class="section">
                <h2>📝 生成的剧本</h2>
                <div id="output" class="script-output">
                    {% if script %}
{{ script }}
                    {% else %}
                        <div class="loading"><p>等待生成...</p></div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    <script>
        const presets = {
            '赘婿逆袭': '男主是个被家族看不起的赘婿，在妻子的生日宴会上被丈母娘当众羞辱，要求离婚。此时本市最大的黑道大佬突然冲进来，对着男主跪地喊大哥。',
            '真假千金': '女主是被抱错的假千金，被真千金抢走未婚夫和家族地位，被迫净身出户。几天后，假千金的公司突然破产，所有资产被神秘人收购。',
            '霸总追妻': '女主是霸总的前妻，三年前被误会背叛而离婚。现在女主回国成了顶级设计师，前夫开始疯狂追妻。',
            '豪门弃子': '男主是豪门弃子，被继母和继弟赶出家门。三个月后，男主以百亿投资人身份出现在家族发布会上。',
            '师姐的秘密': '女主是高冷校花，表面看不起学弟男主。男主其实是顶级财阀继承人，在校庆晚会上暴露身份打脸全场。'
        };
        function setTemplate(name) { document.getElementById('userIdea').value = presets[name]; }
        function generateScript() {
            const idea = document.getElementById('userIdea').value.trim();
            if (!idea) { alert('请输入创意！'); return; }
            const btn = document.getElementById('generateBtn');
            const output = document.getElementById('output');
            btn.disabled = true;
            btn.innerHTML = '⏳ 正在生成...';
            output.innerHTML = '<div class="loading"><p>AI正在疯狂创作中...</p></div>';
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/generate';
            const input = document.createElement('input');
            input.name = 'idea';
            input.value = idea;
            form.appendChild(input);
            document.body.appendChild(form);
            form.submit();
        }
    </script>
</body>
</html>
"""

class DramaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global last_idea, generated_script

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # 安全转义HTML
            safe_idea = last_idea.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            safe_script = generated_script.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') if generated_script else ''

            html = HTML_TEMPLATE.replace('{{ idea }}', safe_idea).replace('{% if script %}', '').replace('{% endif %}', '').replace('{{ script }}', safe_script)
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404)

    def do_POST(self):
        global last_idea, generated_script

        if self.path == '/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            idea = params.get('idea', [''])[0].strip()

            if idea:
                last_idea = idea
                try:
                    script = generate_script(idea, stream=False)
                    formatted = format_script(script)
                    generated_script = formatted

                    # 重定向到首页显示结果
                    self.send_response(303)
                    self.send_header('Location', '/')
                    self.end_headers()
                except Exception as e:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()

                    error_html = HTML_TEMPLATE.replace('{{ idea }}', idea)
                    error_html = error_html.replace('{% if script %}', '').replace('{% endif %}', '').replace('{{ script }}', f'<div style="color: red;">生成失败：{str(e)}</div>')
                    self.wfile.write(error_html.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                html = HTML_TEMPLATE.replace('{{ idea }}', '').replace('{% if script %}', '').replace('{% endif %}', '').replace('{{ script }}', '<div style="color: red;">请输入创意想法</div>')
                self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == '__main__':
    PORT = 8501

    print("\n🎬 AI短剧剧本生成器 - Web服务启动")
    print("=" * 50)
    print("🌐 访问地址：")
    print("   外网: http://47.77.180.50:8501")
    print("   内网: http://172.17.22.78:8501")
    print("=" * 50)
    print("\n⏳ 服务正在启动...")
    print("📝 提示：如果在浏览器中看不到页面，请确保在阿里云控制台开放了8501端口")
    print()

    with socketserver.TCPServer(("0.0.0.0", PORT), DramaHandler) as httpd:
        print(f"✅ 服务已启动，正在监听 0.0.0.0:{PORT}")
        print(f"🌍 访问地址：http://0.0.0.0:{PORT}")
        print()
        print("按 Ctrl+C 停止服务\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ 服务已停止")