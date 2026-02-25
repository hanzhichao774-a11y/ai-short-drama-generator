"""
短剧剧本生成器 - 核心生成引擎
"""

import os
import json
import requests
from prompts import SYSTEM_PROMPT, get_user_prompt, PRESET_TEMPLATES

# API配置
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-sp-7ca5054ae83f464eb25e33a3dcc41942")
API_URL = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"

def generate_script(user_idea, stream=False):
    """
    生成短剧剧本

    Args:
        user_idea: 用户的创意输入
        stream: 是否使用流式输出

    Returns:
        如果 stream=False: 返回完整的剧本文本
        如果 stream=True: 返回生成器
    """
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "glm-4.7",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": get_user_prompt(user_idea)}
            ],
            "temperature": 0.9,  # 提高创造性
            "top_p": 0.95,
            "stream": stream
        }

        if stream:
            # 流式输出
            response = requests.post(
                API_URL,
                headers=headers,
                json=data,
                stream=True
            )

            response.raise_for_status()

            def generate_text():
                for line in response.iter_lines():
                    if line:
                        try:
                            line_text = line.decode('utf-8')
                            if line_text.startswith('data: '):
                                data_str = line_text[6:]
                                if data_str == '[DONE]':
                                    break
                                try:
                                    json_data = json.loads(data_str)
                                    if 'choices' in json_data and len(json_data['choices']) > 0:
                                        delta = json_data['choices'][0].get('delta', {})
                                        if 'content' in delta:
                                            yield delta['content']
                                except json.JSONDecodeError:
                                    pass
                        except Exception as e:
                            pass

            return generate_text()
        else:
            # 非流式输出
            response = requests.post(
                API_URL,
                headers=headers,
                json=data
            )

            response.raise_for_status()
            result = response.json()

            return result['choices'][0]['message']['content']

    except Exception as e:
        raise Exception(f"生成剧本失败: {str(e)}")

def format_script(script_text):
    """
    格式化剧本文本，增强可读性
    """
    # 简单的格式化处理
    lines = script_text.split('\n')
    formatted_lines = []

    for line in lines:
        # 强调关键部分
        if '【场景】' in line:
            formatted_lines.append(f"\n🎬 {line}\n")
        elif '【角色设定】' in line:
            formatted_lines.append(f"\n👥 {line}\n")
        elif '【剧本正文】' in line:
            formatted_lines.append(f"\n📝 {line}\n")
        elif '【核心反转点/爽点】' in line:
            formatted_lines.append(f"\n💥 {line}\n")
        elif line.strip().startswith('*(动作'):
            formatted_lines.append(f"\n🎭 {line}")
        elif '**' in line and '**' in line:
            # 角色对话
            formatted_lines.append(f"\n{line}")
        elif line.strip():
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)

if __name__ == "__main__":
    # 测试
    test_idea = "男主是个送外卖的，在老婆的家族聚会上被丈母娘百般羞辱，要求离婚。此时本市首富突然推门进来，对着男主单膝跪地。"

    print("🎬 短剧剧本生成器测试\n")
    print(f"创意：{test_idea}\n")
    print("正在生成...\n")

    script = generate_script(test_idea)
    print(format_script(script))