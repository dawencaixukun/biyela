# 个人健康运动管理平台 —— 小白保姆级部署教程

> 本教程专为计算机毕业设计、课程设计以及零基础同学编写。提供 **Windows 系统** 与 **Linux 服务器** 两种部署方式，步骤详尽，跟着一步一步复制粘贴命令即可在本地或云端成功跑起系统！

---

## 目录
1. [系统整体技术架构概览](#1-系统整体技术架构概览)
2. [环境准备要求](#2-环境准备要求)
3. [Windows 平台小白部署指南](#3-windows-平台小白部署指南)
4. [Linux 服务器部署指南 (含后台守护进程)](#4-linux-服务器部署指南-含后台守护进程)
5. [系统使用与预置测试账号](#5-系统使用与预置测试账号)
6. [小白常见问题与避坑指南 (FAQ)](#6-小白常见问题与避坑指南-faq)

---

## 1. 系统整体技术架构概览

* **前端技术**：Vue 3 + HTML5 + Element Plus（完全响应式，适配宽屏电脑与手机屏幕，所有前端类库均已内置在 `static/vendor` 中，**无需复杂安装 nodejs/npm**，开箱即用！）
* **后端技术**：Python 3.10+ / FastAPI（轻量高效，提供完全兼容 SpringBoot 契约的规范 RESTful 接口）
* **数据库**：MySQL 8.0+ / MariaDB 10.5+
* **AI 赋能**：集成大语言模型 API，提供阶段性运动数据量化总结与健康建议，带本地智能降级保护。

---

## 2. 环境准备要求

在开始部署前，请确保电脑/服务器上具备以下两样基础环境：
1. **Python**：版本建议 `3.10` 或 `3.11`（安装时务必勾选 **Add Python to PATH**）
2. **MySQL**：版本建议 `5.7`、`8.0` 或 `MariaDB 10.5+`

---

## 3. Windows 平台小白部署指南

### 第一步：安装 Python 与 MySQL
1. **安装 Python**：
   * 前往 Python 官网下载 Windows 安装包：[https://www.python.org/downloads/](https://www.python.org/downloads/)
   * 运行安装包时，**务必勾选底部的 “Add Python to PATH”（添加到环境变量）**，然后点击 “Install Now” 即可。
2. **安装并启动 MySQL**：
   * 推荐小白使用 **phpStudy (小皮面板)** 或者常规 **MySQL 8.0 Installer**。
   * 启动 MySQL 服务，默认端口为 `3306`。

### 第二步：导入数据库脚本
1. 打开 Navicat、DBeaver 或 MySQL 命令行工具，连接到本地 MySQL。
2. 新建名为 **`health_platform`** 的数据库，字符集选择 **`utf8mb4`**。
3. 导入本项目 `sql/health_platform.sql` 文件：
   * **Navicat 方式**：右键点击 `health_platform` 数据库 -> 点击“运行 SQL 文件” -> 选择项目里的 `sql/health_platform.sql` -> 点击开始。
   * **CMD 命令行方式**：
     ```cmd
     mysql -u root -p health_platform < sql/health_platform.sql
     ```
   导入完成后，检查数据库中应包含 8 张表：`sys_user`、`body_metrics`、`sport_dict`、`workout_record`、`diet_record`、`exercise_plan`、`ai_suggestion_record`、`system_notice`。

### 第三步：配置数据库连接（可选）
打开项目目录下的 `app/main.py` 文件，搜索 `MYSQL_CONFIG`（约第 25 行），如果你的本地 MySQL 密码不是默认的，修改为自己的账号密码：
```python
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",            # 你的 MySQL 用户名
    "password": "your_password", # 你的 MySQL 密码
    "database": "health_platform",
    "port": 3306,
    "charset": "utf8mb4",
    "autocommit": True
}
```

### 第四步：安装依赖并启动服务
1. 打开项目根目录，在文件夹上方地址栏输入 `cmd` 并回车，打开黑色的命令提示符窗口。
2. 创建并激活虚拟环境（防止包污染）：
   ```cmd
   python -m venv venv
   call venv\Scripts\activate
   ```
3. 使用国内清华大学镜像源快速安装运行依赖：
   ```cmd
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```
4. 运行服务：
   ```cmd
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8090
   ```
5. 打开浏览器，输入访问地址：
   👉 **`http://localhost:8090`** 或 **`http://127.0.0.1:8090`** 即可进入系统！

---

## 4. Linux 服务器部署指南 (含后台守护进程)

以主流的 **Ubuntu / Debian** 系统为例（CentOS 系统命令相似）：

### 第一步：安装系统基础依赖
```bash
# 1. 更新软件包列表
sudo apt-get update -y

# 2. 安装 Python3 与虚拟环境组件
sudo apt-get install -y python3 python3-pip python3.11-venv git

# 3. 安装轻量且兼容 MySQL 的 MariaDB 服务器
sudo apt-get install -y mariadb-server mariadb-client

# 4. 启动数据库服务
sudo systemctl enable mariadb
sudo systemctl start mariadb
```

### 第二步：创建数据库并导入数据
进入 MySQL 并配置应用专属账号与数据库：
```bash
sudo mysql -e "
CREATE DATABASE IF NOT EXISTS health_platform DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'health_user'@'localhost' IDENTIFIED BY 'health_pass_2026';
CREATE USER IF NOT EXISTS 'health_user'@'127.0.0.1' IDENTIFIED BY 'health_pass_2026';
GRANT ALL PRIVILEGES ON health_platform.* TO 'health_user'@'localhost';
GRANT ALL PRIVILEGES ON health_platform.* TO 'health_user'@'127.0.0.1';
FLUSH PRIVILEGES;
"

# 导入 SQL 初始化脚本
mysql -u health_user -phealth_pass_2026 -h 127.0.0.1 health_platform < sql/health_platform.sql
```

### 第三步：配置 Python 虚拟环境与依赖
假设项目代码放置在 `/opt/grad-sys` 或 `/root/grad-sys`：
```bash
cd /root/grad-sys

# 1. 创建虚拟环境
python3 -m venv venv

# 2. 安装项目依赖（使用国内清华源高速下载）
./venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 第四步：配置 Linux systemd 后台守护进程（实现开机自启、崩溃自动重启）
1. 创建 systemd 服务配置文件：
```bash
sudo cat <<'EOF' > /etc/systemd/system/grad-sys.service
[Unit]
Description=Personal Health and Sports Management Platform
After=network.target mariadb.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/grad-sys
ExecStart=/root/grad-sys/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8090 --workers 1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

2. 启动并启用服务自启：
```bash
sudo systemctl daemon-reload
sudo systemctl enable grad-sys
sudo systemctl restart grad-sys
sudo systemctl status grad-sys --no-pager
```

3. 检查端口监听与防火墙：
```bash
# 确认 8090 端口已在监听
sudo ss -tulpn | grep 8090

# 若有云服务器防火墙/安全组，请在云控制台安全组入方向放行 TCP 8090 端口！
```
浏览器访问：`http://<你的服务器IP>:8090` 即可开始使用！

---

## 5. 系统使用与预置测试账号

系统预置了完整的测试数据与角色，右上角提供**免密一键切换下拉菜单**（专为毕设答辩演示设计，无需繁琐退登），同时支持标准账密登录：

| 角色类型 | 用户名 | 默认密码 | 说明与功能亮点 |
| :--- | :--- | :--- | :--- |
| **系统管理员** | `admin` | `123456` | **管理员后台**：全站数据大盘监管、用户管理与一键封禁开关、运动打卡监管、健康科普发布、运动字典维护 |
| **健身学员 (前台)** | `user_alex` | `123456` | 姓名：**张健**。体验日常打卡、近7天能量双轨走势图、**一键生成大模型 AI 运动健康分析周报** |
| **减脂学员 (前台)** | `user_lisa` | `123456` | 姓名：**李悦**。体验多用户数据隔离、个性化目标进度管理 |

---

## 6. 小白常见问题与避坑指南 (FAQ)

### Q1: 启动时提示 `Address already in use` (8090 端口被占用) 怎么办？
* **Windows**：打开 CMD 运行 `netstat -ano | findstr 8090`，找到最后一列的 PID（进程号），运行 `taskkill /F /PID <PID>` 杀掉该进程，再重新启动。
* **Linux**：运行 `fuser -k 8090/tcp` 释放端口后重启服务。

### Q2: 提示 `OperationalError: (1045, "Access denied for user ...")` 数据库密码错误？
* 请检查 `app/main.py` 中的 `MYSQL_CONFIG` 配置，确保用户名、密码与你本地 MySQL 的账号密码完全一致，且 `health_platform` 数据库已成功创建。

### Q3: 为什么不需要安装 Node.js 和前端打包工具？
* 本系统采用轻量工程化思想，前端全部采用标准的 Vue 3 + Element Plus 单页面应用架构，依赖文件均以 IIFE 格式存放在 `static/vendor` 中。零编译、免安装复杂的前端构建链路，保证小白同学不论在任何电脑上都能即下即跑，永远不会遇到前端 `node_modules` 依赖冲突或安装报错！

### Q4: 毕设答辩 PPT 在哪里？
* 汇报答辩 PPT 位于项目根目录下以及 `docs/` 文件夹中：
  📄 **`docs/个人健康运动管理平台_毕设总结报告.pptx`**  
  支持使用 Microsoft PowerPoint 或 WPS Office 直接打开演示汇报。
