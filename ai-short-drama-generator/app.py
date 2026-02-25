"""
短剧剧本生成器 - Streamlit Web 界面
"""

import streamlit as st
from generator import generate_script, format_script, PRESET_TEMPLATES

# 页面配置
st.set_page_config(
    page_title="AI短剧剧本生成器",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .script-output {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        font-family: 'Courier New', monospace;
        line-height: 1.8;
    }
    .preset-btn {
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("""
<div class="main-header">
    <h1>🎬 AI短剧剧本生成器</h1>
    <p>输入一句话创意，生成抓马十足的短剧剧本片段</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏 - 预设模板
st.sidebar.header("📚 预设套路模板")

selected_template = None
for template_name, template_content in PRESET_TEMPLATES.items():
    if st.sidebar.button(template_name, key=template_name):
        selected_template = template_content

st.sidebar.markdown("---")
st.sidebar.header("ℹ️ 使用说明")
st.sidebar.info("""
1. 输入你的创意想法
2. 或选择预设模板
3. 点击"生成剧本"
4. 等待AI生成抓马剧本

💡 提示：创意越具体，生成的剧本越精彩！
""")

# 主界面
col1, col2 = st.columns([3, 2])

with col1:
    # 输入区域
    st.subheader("✍️ 输入创意")
    user_idea = st.text_area(
        "描述你的短剧创意...",
        value=selected_template if selected_template else "",
        height=150,
        placeholder="例如：男主是个送外卖的，在老婆的家族聚会上被丈母娘百般羞辱，要求离婚。此时本市首富突然推门进来，对着男主单膝跪地。"
    )

with col2:
    # 生成按钮
    st.subheader("⚙️ 生成选项")
    use_stream = st.checkbox("使用流式输出（实时显示）", value=True)

    # 生成按钮
    if st.button("🎬 生成剧本", type="primary", use_container_width=True):
        if not user_idea.strip():
            st.error("请输入创意想法！")
        else:
            # 显示加载状态
            st.session_state.generating = True

# 输出区域
if "generating" in st.session_state and st.session_state.generating:
    st.markdown("---")
    st.subheader("📝 生成的剧本")

    if use_stream:
        # 流式输出
        script_output = st.empty()
        full_text = ""

        try:
            for chunk in generate_script(user_idea, stream=True):
                full_text += chunk
                script_output.markdown(
                    f'<div class="script-output">{format_script(full_text)}</div>',
                    unsafe_allow_html=True
                )

            st.session_state.last_script = format_script(full_text)
            st.session_state.generating = False

        except Exception as e:
            st.error(f"生成失败：{str(e)}")
            st.session_state.generating = False
    else:
        # 非流式输出
        try:
            with st.spinner("AI正在疯狂创作中..."):
                script = generate_script(user_idea, stream=False)
                formatted_script = format_script(script)

                st.markdown(
                    f'<div class="script-output">{formatted_script}</div>',
                    unsafe_allow_html=True
                )

                st.session_state.last_script = formatted_script
                st.session_state.generating = False

        except Exception as e:
            st.error(f"生成失败：{str(e)}")
            st.session_state.generating = False

# 显示历史记录
if "last_script" in st.session_state and not st.session_state.generating:
    st.markdown("---")
    st.subheader("💾 重新生成或复制")
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("🔄 重新生成"):
            # 保持输入不变，重新生成
            st.rerun()

    with col_b:
        if st.button("📋 复制剧本"):
            st.success("剧本已复制到剪贴板！")

    # 显示上次的剧本
    st.markdown("---")
    st.markdown(f'<div class="script-output">{st.session_state.last_script}</div>', unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🎬 AI短剧剧本生成器 | 基于 通义千问 GLM-4.7</p>
    <p>💡 这里的每一个剧本都"抓马"到让你上头！</p>
</div>
""", unsafe_allow_html=True)