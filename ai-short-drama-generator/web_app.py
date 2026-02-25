"""
AI短剧剧本生成器 - 简单Web界面（基于Flask）
"""

from flask import Flask, render_template_string, request, jsonify
import json
from generator import generate_script, format_script

app = Flask(__name__)

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 AI短剧剧本生成器</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }

        .input-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }

        .output-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }

        h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }

        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            min-height: 150px;
            transition: border-color 0.3s;
        }

        textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        .preset-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }

        .preset-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .preset-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102,126,234,0.4);
        }

        .generate-btn {
            width: 100%;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(245,87,108,0.4);
        }

        .generate-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .script-output {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            font-family: 'Courier New', monospace;
            line-height: 1.8;
            white-space: pre-wrap;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .loading-spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .copy-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
            transition: background 0.3s;
        }

        .copy-btn:hover {
            background: #5568d3;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 AI短剧剧本生成器</h1>
            <p>输入创意，一键生成抓马十足的短剧剧本</p>
        </div>

        <div class="main-content">
            <div class="input-section">
                <h2>✍️ 输入创意</h2>

                <label>选择预设模板：</label>
                <div class="preset-buttons">
                    <button class="preset-btn" onclick="setTemplate('赘婿逆袭')">赘婿逆袭</button>
                    <button class="preset-btn" onclick="setTemplate('真假千金')">真假千金</button>
                    <button class="preset-btn" onclick="setTemplate('霸总追妻')">霸总追妻</button>
                    <button class="preset-btn" onclick="setTemplate('豪门弃子')">豪门弃子</button>
                    <button class="preset-btn" onclick="setTemplate('师姐的秘密')">师姐的秘密</button>
                </div>

                <label>或输入你的创意：</label>
                <textarea id="userIdea" placeholder="例如：男主是个送外卖的，在老婆的家族聚会上被丈母娘百般羞辱，要求离婚。此时本市首富突然推门进来，对着男主单膝跪地。">{{ idea|safe }}</textarea>

                <button class="generate-btn" id="generateBtn" onclick="generateScript()">
                    🎬 生成剧本
                </button>
            </div>

            <div class="output-section">
                <h2>📝 生成的剧本</h2>
                <div id="output" class="script-output">
                    {% if script %}
                        {{ script|safe }}
                    {% else %}
                        <div class="loading">
                            <p>等待生成...</p>
                            <p style="font-size: 12px; margin-top: 10px;">💡 输入创意，点击生成按钮开始</p>
                        </div>
                    {% endif %}
                </div>
                {% if script %}
                <button class="copy-btn" onclick="copyScript()">📋 复制剧本</button>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        const presets = {
            '赘婿逆袭': '男主是个被家族看不起的赘婿，在妻子的生日宴会上被丈母娘当众羞辱，要求离婚。此时本市最大的黑道大佬突然冲进来，对着男主跪地喊大哥。',
            '真假千金': '女主是被抱错的假千金，被真千金抢走未婚夫和家族地位，被迫净身出户。几天后，假千金的公司突然破产，所有资产被神秘人收购，神秘人竟然是女主的亲哥哥。',
            '霸总追妻': '女主是霸总的前妻，三年前被霸道总裁误会背叛而离婚。现在女主回国成了顶级设计师，在聚会上偶遇前夫。前夫发现三年前的误会，开始疯狂追妻。',
            '豪门弃子': '男主是豪门弃子，被继母和继弟联手赶出家门，一无所有。三个月后，继母和继弟正得意地召开家族发布会，男主以百亿投资人身份出现。',
            '师姐的秘密': '女主是高冷校花师姐，表面看不起学弟男主。男主其实是顶级财阀继承人，一直隐藏身份。校庆晚会上，师姐被其他富二代羞辱，男主暴露身份打脸全场。'
        };

        function setTemplate(templateName) {
            document.getElementById('userIdea').value = presets[templateName];
        }

        function generateScript() {
            const idea = document.getElementById('userIdea').value.trim();
            if (!idea) {
                alert('请输入创意想法！');
                return;
            }

            const btn = document.getElementById('generateBtn');
            const output = document.getElementById('output');

            btn.disabled = true;
            btn.innerHTML = '⏳ 正在生成...';

            output.innerHTML = '<div class="loading"><div class="loading-spinner"></div><p>AI正在疯狂创作中...</p></div>';

            fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ idea: idea })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    output.innerHTML = data.script;
                    location.reload(); // 刷新页面显示完整结果
                } else {
                    output.innerHTML = '<div class="loading"><p style="color: #e74c3c;">❌ 生成失败：' + data.error + '</p></div>';
                }
            })
            .catch(error => {
                output.innerHTML = '<div class="loading"><p style="color: #e74c3c;">❌ 网络错误，请重试</p></div>';
            })
            .finally(() => {
                btn.disabled = false;
                btn.innerHTML = '🎬 生成剧本';
            });
        }

        function copyScript() {
            const script = document.getElementById('output').innerText;
            navigator.clipboard.writeText(script).then(() => {
                alert('✅ 剧本已复制到剪贴板！');
            }).catch(err => {
                alert('❌ 复制失败，请手动复制');
            });
        }
    </script>
</body>
</html>
"""

# 全局变量
generated_script = None
last_idea = ""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, script=generated_script, idea=last_idea)

@app.route('/generate', methods=['POST'])
def generate():
    global generated_script, last_idea

    try:
        data = request.get_json()
        idea = data.get('idea', '').strip()

        if not idea:
            return jsonify({'success': False, 'error': '请输入创意想法'})

        last_idea = idea

        # 生成剧本
        script = generate_script(idea, stream=False)
        formatted = format_script(script)

        generated_script = formatted

        return jsonify({'success': True, 'script': formatted})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/copy', methods=['POST'])
def copy():
    global generated_script
    if generated_script:
        return jsonify({'success': True, 'script': generated_script})
    return jsonify({'success': False, 'error': '暂无生成的剧本'})

if __name__ == '__main__':
    print("\n🎬 AI短剧剧本生成器 - Web服务启动")
    print("=" * 50)
    print("🌐 访问地址：")
    print("   外网: http://47.77.180.50:8501")
    print("   内网: http://172.17.22.78:8501")
    print("=" * 50)
    print()

    app.run(host='0.0.0.0', port=8501, debug=False)