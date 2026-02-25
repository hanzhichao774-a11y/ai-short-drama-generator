"""
测试短剧剧本生成器的功能
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generator import generate_script, format_script

def test_basic_generation():
    """测试基础生成功能"""
    print("=" * 60)
    print("🎬 测试1：基础剧本生成")
    print("=" * 60)

    test_idea = "男主是个送外卖的，在老婆的家族聚会上被丈母娘百般羞辱，要求离婚。此时本市首富突然推门进来，对着男主单膝跪地。"

    print(f"\n💡 创意：{test_idea}\n")
    print("🔄 正在生成...\n")

    try:
        script = generate_script(test_idea, stream=False)
        formatted = format_script(script)

        print("✅ 生成成功！\n")
        print(formatted)

        return True
    except Exception as e:
        print(f"❌ 生成失败：{str(e)}")
        return False

def test_stream_generation():
    """测试流式生成功能"""
    print("\n\n" + "=" * 60)
    print("🎬 测试2：流式生成")
    print("=" * 60)

    test_idea = "女主是高冷校花，看不起男主。男主其实是顶级财阀继承人，在晚会上暴露身份打脸全场。"

    print(f"\n💡 创意：{test_idea}\n")
    print("🔄 正在流式生成...\n")

    try:
        full_text = ""
        for chunk in generate_script(test_idea, stream=True):
            print(chunk, end='', flush=True)
            full_text += chunk

        print("\n\n✅ 流式生成成功！")

        return True
    except Exception as e:
        print(f"\n❌ 流式生成失败：{str(e)}")
        return False

def test_presets():
    """测试预设模板"""
    print("\n\n" + "=" * 60)
    print("🎬 测试3：预设模板")
    print("=" * 60)

    from prompts import PRESET_TEMPLATES

    print(f"✅ 共有 {len(PRESET_TEMPLATES)} 个预设模板：\n")
    for name, content in PRESET_TEMPLATES.items():
        print(f"  • {name}")
        print(f"    {content[:50]}...")
        print()

    return True

if __name__ == "__main__":
    print("\n🎬 AI短剧剧本生成器 - 功能测试\n")

    # 运行测试
    results = []

    results.append(("基础生成", test_basic_generation()))
    results.append(("流式生成", test_stream_generation()))
    results.append(("预设模板", test_presets()))

    # 汇总结果
    print("\n\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")

    print("\n" + "=" * 60)

    if all(r for _, r in results):
        print("🎉 所有测试通过！系统运行正常。\n")
        sys.exit(0)
    else:
        print("⚠️  部分测试失败，请检查配置。\n")
        sys.exit(1)