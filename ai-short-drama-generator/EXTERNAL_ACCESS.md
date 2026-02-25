# 🌐 外网访问配置说明

## 📋 访问地址

根据你的服务器信息，可以通过以下地址访问：

- **外网访问**：`http://47.77.180.50:8501`
- **内网访问**：`http://172.17.22.78:8501`

## ⚙️ 配置步骤

### 1. 检查防火墙/安全组

**重要**：需要在你的云服务器（阿里云）上开放8501端口！

#### 方法1：阿里云控制台配置（推荐）

1. 登录 [阿里云控制台](https://ecs.console.aliyun.com/)
2. 找到你的服务器实例
3. 进入"安全组"设置
4. 添加入方向规则：
   - 端口范围：`8501/8501`
   - 授权对象：`0.0.0.0/0`（允许所有IP访问）
   - 协议类型：`TCP`
   - 策略：`允许`

#### 方法2：命令行配置（如果有iptables）

```bash
# 允许8501端口
sudo iptables -A INPUT -p tcp --dport 8501 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 8501 -j ACCEPT

# 保存规则
sudo service iptables save
```

### 2. 启动服务

使用外网启动脚本：

```bash
cd /home/admin/clawd/ai-short-drama-generator
./start_external.sh
```

或者手动启动：

```bash
python3 -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

### 3. 访问测试

在浏览器中打开：`http://47.77.180.50:8501`

## 🔐 安全提示

### 生产环境建议

如果你计划长期对外开放，建议：

1. **使用HTTPS**：配置SSL证书，使用 Nginx 反向代理
2. **添加认证**：配置用户名密码或访问令牌
3. **限制访问IP**：只允许特定IP段访问
4. **使用非标准端口**：避免使用常见端口

### 简单的认证方案

可以修改 `app.py`，添加简单的密码验证：

```python
import streamlit as st

# 添加密码验证
def check_password():
    def password_entered():
        if st.session_state["password"] == "your_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.text_input("请输入密码", type="password", on_change=password_entered, key="password")
        st.write("请先登录")
        return False
    return True

# 在主程序开始时检查
if not check_password():
    st.stop()
```

## 🚀 后台运行

如果想让服务在后台持续运行，可以使用以下方法：

### 方法1：使用 nohup

```bash
cd /home/admin/clawd/ai-short-drama-generator
nohup python3 -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501 > streamlit.log 2>&1 &

# 查看日志
tail -f streamlit.log

# 停止服务
pkill -f "streamlit run app.py"
```

### 方法2：使用 systemd（推荐）

创建服务文件：

```bash
sudo nano /etc/systemd/system/ai-drama-generator.service
```

内容：

```ini
[Unit]
Description=AI Short Drama Generator
After=network.target

[Service]
Type=simple
User=admin
WorkingDirectory=/home/admin/clawd/ai-short-drama-generator
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-drama-generator
sudo systemctl start ai-drama-generator

# 查看状态
sudo systemctl status ai-drama-generator

# 查看日志
sudo journalctl -u ai-drama-generator -f
```

## 📊 性能优化

如果并发访问量大，可以考虑：

1. **增加Streamlit Worker数量**：
   ```bash
   streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.maxUploadSize=200 --server.maxMessageSize=200
   ```

2. **使用Nginx反向代理**：添加负载均衡和缓存

3. **优化API调用**：添加缓存机制，避免重复生成相同创意

## 🛠️ 故障排查

### 问题1：无法访问

**检查清单：**
- ✅ 服务是否启动：`ps aux | grep streamlit`
- ✅ 端口是否监听：`netstat -tlnp | grep 8501`
- ✅ 防火墙是否开放：阿里云安全组设置
- ✅ 云服务器安全组是否允许：检查8501端口

### 问题2：页面加载慢

**可能原因：**
- API调用超时
- 网络问题
- 服务器负载过高

**解决方案：**
- 检查网络连接
- 查看日志：`tail -f streamlit.log`
- 检查服务器资源：`htop`

### 问题3：生成失败

**检查清单：**
- ✅ API Key是否正确
- ✅ 是否有足够的API额度
- ✅ 网络连接是否正常

## 📞 联系支持

如果遇到问题，可以：
1. 查看日志文件
2. 检查阿里云控制台的实例监控
3. 重启服务

---

**🎬 现在就可以通过 http://47.77.180.50:8501 访问你的AI短剧剧本生成器了！**