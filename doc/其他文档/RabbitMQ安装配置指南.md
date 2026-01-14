# RabbitMQ 安装配置指南

## 📋 文档信息

- **文档版本**：v1.0
- **创建日期**：2026-01-14
- **RabbitMQ版本**：3.13.x / 4.0.x（最新稳定版）
- **适用平台**：Windows、macOS、Linux、Docker

---

## 📌 目录

1. [系统要求](#系统要求)
2. [Docker 安装](#docker-安装)
3. [Linux 安装](#linux-安装)
4. [macOS 安装](#macos-安装)
5. [Windows 安装](#windows-安装)
6. [基础配置](#基础配置)
7. [验证安装](#验证安装)
8. [常见问题](#常见问题)

---

## 系统要求

### 最低要求

| 组件 | 要求 |
|-----|------|
| **操作系统** | Windows 10+、macOS 11+、Linux（主流发行版） |
| **内存** | 至少 2GB RAM（推荐 4GB+） |
| **磁盘空间** | 至少 1GB 可用空间 |
| **Erlang** | 26.x 或更高版本 |
| **网络** | 开放端口 5672（AMQP）、15672（管理界面） |

### 推荐配置

- **生产环境**：4GB+ RAM、SSD磁盘、独立网络
- **开发环境**：2GB RAM、普通磁盘

---

## Docker 安装

### 前置条件

- Docker 20.10+
- Docker Compose 2.0+（可选）

### Linux 宿主机安装

#### 1. 配置 Docker 守护进程（推荐）

创建或编辑 `/etc/docker/daemon.json`：

```json
{
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
```

重启 Docker 服务：

```bash
sudo systemctl restart docker
```

#### 2. 运行 RabbitMQ 容器

**快速启动（开发环境）：**

```bash
docker run -it --rm --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3.13-management
```

**生产环境配置（持久化数据）：**

```bash
docker run -d --name rabbitmq \
  --hostname my-rabbit \
  -p 5672:5672 \
  -p 15672:15672 \
  -v rabbitmq_data:/var/lib/rabbitmq \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=admin123 \
  rabbitmq:3.13-management
```

**使用 Docker Compose（推荐）：**

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3.13-management
    container_name: rabbitmq
    hostname: my-rabbit
    ports:
      - "5672:5672"    # AMQP 端口
      - "15672:15672"  # 管理界面端口
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    restart: unless-stopped

volumes:
  rabbitmq_data:
    driver: local
```

启动服务：

```bash
docker-compose up -d
```

#### 3. 验证安装

```bash
# 查看容器状态
docker ps | grep rabbitmq

# 查看日志
docker logs rabbitmq

# 进入容器
docker exec -it rabbitmq bash
```

### Windows 宿主机安装

#### 1. 配置 Docker Desktop

打开 Docker Desktop，进入 Settings → Resources → File sharing，确保共享必要的目录。

#### 2. 运行 RabbitMQ 容器

**快速启动：**

```powershell
docker run -it --rm --name rabbitmq `
  -p 5672:5672 `
  -p 15672:15672 `
  rabbitmq:3.13-management
```

**生产环境配置：**

```powershell
docker run -d --name rabbitmq `
  --hostname my-rabbit `
  -p 5672:5672 `
  -p 15672:15672 `
  -v ${PWD}/rabbitmq:/var/lib/rabbitmq `
  -e RABBITMQ_DEFAULT_USER=admin `
  -e RABBITMQ_DEFAULT_PASS=admin123 `
  rabbitmq:3.13-management
```

**使用 Docker Compose：**

创建 `docker-compose.yml`（与 Linux 相同），然后运行：

```powershell
docker-compose up -d
```

#### 3. Windows 特殊配置

**文件路径映射：**

Windows 使用 `${PWD}` 或绝对路径映射数据卷：

```powershell
-v C:\data\rabbitmq:/var/lib/rabbitmq
```

**网络配置：**

确保 Windows 防火墙允许 Docker 容器访问网络。

---

## Linux 安装

### Debian / Ubuntu

#### 1. 安装依赖

```bash
sudo apt-get update
sudo apt-get install -y curl gnupg apt-transport-https
```

#### 2. 添加 RabbitMQ 签名密钥

```bash
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" \
  | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
```

#### 3. 添加软件源

**Ubuntu 22.04 (Jammy):**

```bash
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Modern Erlang/OTP releases
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-erlang/ubuntu/jammy jammy main
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb2.rabbitmq.com/rabbitmq-erlang/ubuntu/jammy jammy main

## Latest RabbitMQ releases
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-server/ubuntu/jammy jammy main
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb2.rabbitmq.com/rabbitmq-server/ubuntu/jammy jammy main
EOF
```

**Debian 12 (Bookworm):**

```bash
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Modern Erlang/OTP releases
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-erlang/debian/bookworm bookworm main
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb2.rabbitmq.com/rabbitmq-erlang/debian/bookworm bookworm main

## Latest RabbitMQ releases
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-server/debian/bookworm bookworm main
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb2.rabbitmq.com/rabbitmq-server/debian/bookworm bookworm main
EOF
```

#### 4. 更新包索引

```bash
sudo apt-get update -y
```

#### 5. 安装 Erlang 和 RabbitMQ

```bash
# 安装 Erlang
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

# 安装 RabbitMQ
sudo apt-get install -y rabbitmq-server --fix-missing
```

#### 6. 启动服务

```bash
# 启动服务
sudo systemctl start rabbitmq-server

# 设置开机自启
sudo systemctl enable rabbitmq-server

# 查看状态
sudo systemctl status rabbitmq-server
```

### RHEL / CentOS / Rocky Linux / Alma Linux

#### 1. 安装依赖

```bash
sudo dnf install -y curl gnupg
```

#### 2. 配置 Yum 仓库

创建 `/etc/yum.repos.d/rabbitmq.repo`：

```ini
##
## Zero dependency Erlang RPM
##

[modern-erlang]
name=modern-erlang-el8
baseurl=https://yum1.rabbitmq.com/erlang/el/8/$basearch
        https://yum2.rabbitmq.com/erlang/el/8/$basearch
repo_gpgcheck=1
enabled=1
gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key
gpgcheck=1
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
pkg_gpgcheck=1
autorefresh=1
type=rpm-md

[modern-erlang-noarch]
name=modern-erlang-el8-noarch
baseurl=https://yum1.rabbitmq.com/erlang/el/8/noarch
        https://yum2.rabbitmq.com/erlang/el/8/noarch
repo_gpgcheck=1
enabled=1
gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key
       https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
gpgcheck=1
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
pkg_gpgcheck=1
autorefresh=1
type=rpm-md

[rabbitmq-el8]
name=rabbitmq-el8
baseurl=https://yum2.rabbitmq.com/rabbitmq/el/8/$basearch
        https://yum1.rabbitmq.com/rabbitmq/el/8/$basearch
repo_gpgcheck=1
enabled=1
gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key
       https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
gpgcheck=1
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
pkg_gpgcheck=1
autorefresh=1
type=rpm-md

[rabbitmq-el8-noarch]
name=rabbitmq-el8-noarch
baseurl=https://yum2.rabbitmq.com/rabbitmq/el/8/noarch
        https://yum1.rabbitmq.com/rabbitmq/el/8/noarch
repo_gpgcheck=1
enabled=1
gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key
       https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
gpgcheck=1
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
pkg_gpgcheck=1
autorefresh=1
type=rpm-md
```

#### 3. 安装 Erlang 和 RabbitMQ

```bash
sudo dnf install -y erlang rabbitmq-server
```

#### 4. 启动服务

```bash
# 启动服务
sudo systemctl start rabbitmq-server

# 设置开机自启
sudo systemctl enable rabbitmq-server

# 查看状态
sudo systemctl status rabbitmq-server
```

---

## macOS 安装

### 使用 Homebrew（推荐）

#### 1. 安装 Homebrew

如果尚未安装 Homebrew：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. 安装 Erlang

```bash
brew install erlang
```

#### 3. 安装 RabbitMQ

```bash
brew install rabbitmq
```

#### 4. 配置防火墙（重要）

如果 macOS 防火墙已启用，需要允许 Erlang 绑定端口：

```bash
# 获取 Erlang 安装路径
brew --prefix erlang

# 假设输出为 /usr/local/Cellar/erlang/26.2.5.2

# 允许 Erlang CLI 工具绑定端口
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/bin/erl
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/bin/erl

# 允许 Erlang VM 绑定端口
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/erts-14.2.5/bin/beam.smp
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/erts-14.2.5/bin/beam.smp
```

#### 5. 启动服务

```bash
# 启动服务
brew services start rabbitmq

# 查看状态
brew services list | grep rabbitmq

# 停止服务
brew services stop rabbitmq

# 重启服务
brew services restart rabbitmq
```

### 手动安装

#### 1. 下载安装包

访问 [RabbitMQ 官网下载页面](https://www.rabbitmq.com/download.html)，下载 macOS 版本的安装包。

#### 2. 安装

双击 `.pkg` 文件，按照安装向导完成安装。

#### 3. 启动服务

```bash
# 启动服务
sudo launchctl load -w /Library/LaunchDaemons/com.rabbitmq.rabbitmq-server.plist

# 停止服务
sudo launchctl unload -w /Library/LaunchDaemons/com.rabbitmq.rabbitmq-server.plist
```

---

## Windows 安装

### 使用安装包（推荐）

#### 1. 下载安装包

访问 [RabbitMQ 官网下载页面](https://www.rabbitmq.com/download.html)，下载 Windows 版本的安装包（`.exe` 文件）。

#### 2. 安装 Erlang

RabbitMQ 依赖 Erlang，需要先安装 Erlang。

**下载 Erlang:**
- 访问 [Erlang 官网](https://www.erlang.org/downloads)
- 下载 Windows 64-bit 版本
- 运行安装程序，使用默认设置

#### 3. 安装 RabbitMQ

**运行安装程序:**
1. 双击下载的 `.exe` 文件
2. 选择安装目录（默认：`C:\Program Files\RabbitMQ Server\rabbitmq_server-3.13.x`）
3. 选择组件（默认全部选中）
4. 完成安装

#### 4. 配置环境变量（可选）

RabbitMQ 安装程序会自动配置环境变量，但可以手动检查：

```powershell
# 检查环境变量
$env:RABBITMQ_BASE
$env:ERLANG_HOME
```

#### 5. 管理服务

**使用 rabbitmq-service.bat:**

```cmd
# 安装服务
rabbitmq-service.bat install

# 启动服务
rabbitmq-service.bat start

# 停止服务
rabbitmq-service.bat stop

# 卸载服务
rabbitmq-service.bat remove
```

**使用 Windows 服务管理器:**

1. 按 `Win + R`，输入 `services.msc`
2. 找到 `RabbitMQ` 服务
3. 右键选择启动/停止

#### 6. 配置文件位置

- **配置文件**: `%AppData%\RabbitMQ\rabbitmq.conf`
- **环境配置**: `%AppData%\RabbitMQ\rabbitmq-env.conf`
- **日志文件**: `%AppData%\RabbitMQ\log\`

#### 7. 修改配置后重新安装服务

如果修改了环境变量，需要重新安装服务：

```cmd
rabbitmq-service.bat stop
rabbitmq-service.bat remove
rabbitmq-service.bat install
rabbitmq-service.bat start
```

---

## 基础配置

### 启用管理插件

管理插件提供 Web 界面，方便监控和管理。

**Linux/macOS:**

```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

**Windows:**

```cmd
rabbitmq-plugins.bat enable rabbitmq_management
```

### 创建管理员用户

**Linux/macOS:**

```bash
# 添加用户
sudo rabbitmqctl add_user admin admin123

# 设置用户标签
sudo rabbitmqctl set_user_tags admin administrator

# 授予权限
sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```

**Windows:**

```cmd
rem 添加用户
rabbitmqctl.bat add_user admin admin123

rem 设置用户标签
rabbitmqctl.bat set_user_tags admin administrator

rem 授予权限
rabbitmqctl.bat set_permissions -p / admin ".*" ".*" ".*"
```

### 删除默认用户（安全建议）

**Linux/macOS:**

```bash
sudo rabbitmqctl delete_user guest
```

**Windows:**

```cmd
rabbitmqctl.bat delete_user guest
```

### 配置文件示例

创建 `/etc/rabbitmq/rabbitmq.conf`（Linux）或 `%AppData%\RabbitMQ\rabbitmq.conf`（Windows）：

```ini
# 监听端口
listeners.tcp.default = 5672

# 管理界面端口
management.tcp.port = 15672

# 日志级别
log.console.level = info
log.file.level = info

# 内存阈值（当使用达到此比例时会阻塞发布者）
vm_memory_high_watermark.relative = 0.6

# 磁盘空间阈值（当剩余磁盘空间低于此值时会阻塞发布者）
disk_free_limit.absolute = 1GB

# 心跳超时（秒）
heartbeat = 60

# 连接数限制
channel_max = 2048
connection_max = infinity

# 集群配置（可选）
# cluster_formation.peer_discovery_backend = rabbit_peer_discovery_classic_config
# cluster_formation.classic_config.nodes.1 = rabbit@node1
# cluster_formation.classic_config.nodes.2 = rabbit@node2
```

### 配置文件位置

| 平台 | 配置文件位置 |
|-----|------------|
| **Linux** | `/etc/rabbitmq/rabbitmq.conf` |
| **macOS** | `/usr/local/etc/rabbitmq/rabbitmq.conf` |
| **Windows** | `%AppData%\RabbitMQ\rabbitmq.conf` |

---

## 验证安装

### 1. 检查服务状态

**Linux:**

```bash
sudo systemctl status rabbitmq-server
```

**macOS:**

```bash
brew services list | grep rabbitmq
```

**Windows:**

```cmd
sc query RabbitMQ
```

### 2. 查看版本

**Linux/macOS:**

```bash
sudo rabbitmqctl version
```

**Windows:**

```cmd
rabbitmqctl.bat version
```

### 3. 检查集群状态

**Linux/macOS:**

```bash
sudo rabbitmqctl cluster_status
```

**Windows:**

```cmd
rabbitmqctl.bat cluster_status
```

### 4. 访问管理界面

打开浏览器，访问：`http://localhost:15672`

默认登录信息：
- 用户名：`admin`（或您创建的管理员用户）
- 密码：`admin123`（或您设置的密码）

### 5. 测试连接

使用 Python 测试连接：

```python
import pika

# 连接到 RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/', 
                            pika.PlainCredentials('admin', 'admin123'))
)
channel = connection.channel()

# 声明队列
channel.queue_declare(queue='test_queue')

# 发送消息
channel.basic_publish(exchange='',
                    routing_key='test_queue',
                    body='Hello RabbitMQ!')

print(" [x] Sent 'Hello RabbitMQ!'")
connection.close()
```

---

## 常见问题

### 问题 1: Erlang 版本不兼容

**症状:** 安装 RabbitMQ 时提示 Erlang 版本过低

**解决方案:**
- 确保安装 Erlang 26.x 或更高版本
- 使用 RabbitMQ 官方仓库获取兼容的 Erlang 版本

### 问题 2: 端口被占用

**症状:** 启动失败，提示端口 5672 或 15672 被占用

**解决方案:**

**Linux/macOS:**

```bash
# 查找占用端口的进程
sudo lsof -i :5672
sudo lsof -i :15672

# 杀死进程
sudo kill -9 <PID>
```

**Windows:**

```cmd
rem 查找占用端口的进程
netstat -ano | findstr :5672
netstat -ano | findstr :15672

rem 杀死进程
taskkill /PID <PID> /F
```

### 问题 3: Docker 容器无法访问网络

**症状:** Docker 容器启动后无法访问外部网络

**解决方案:**

**Linux:**

```bash
# 检查 Docker 网络
docker network ls

# 重启 Docker
sudo systemctl restart docker
```

**Windows:**

1. 重启 Docker Desktop
2. 检查网络设置
3. 确保 WSL2 正确配置

### 问题 4: macOS 防火墙阻止连接

**症状:** RabbitMQ 无法启动，无法绑定端口

**解决方案:**

```bash
# 配置防火墙允许 Erlang
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/bin/erl
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/bin/erl

sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/erts-14.2.5/bin/beam.smp
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/Cellar/erlang/26.2.5.2/lib/erlang/erts-14.2.5/bin/beam.smp
```

### 问题 5: 权限不足

**症状:** 无法执行 rabbitmqctl 命令

**解决方案:**

**Linux/macOS:**

```bash
# 使用 sudo
sudo rabbitmqctl <command>

# 或将用户添加到 rabbitmq 组
sudo usermod -a -G rabbitmq $USER
```

**Windows:**

```cmd
# 以管理员身份运行 PowerShell 或 CMD
```

### 问题 6: 数据持久化问题

**症状:** Docker 容器重启后数据丢失

**解决方案:**

使用数据卷持久化数据：

```bash
docker run -d --name rabbitmq \
  -v rabbitmq_data:/var/lib/rabbitmq \
  rabbitmq:3.13-management
```

或使用本地目录：

```bash
docker run -d --name rabbitmq \
  -v /path/to/local/data:/var/lib/rabbitmq \
  rabbitmq:3.13-management
```

---

## 📚 参考资源

- **RabbitMQ 官方文档**: https://www.rabbitmq.com/docs
- **RabbitMQ 下载页面**: https://www.rabbitmq.com/download.html
- **Erlang 下载页面**: https://www.erlang.org/downloads
- **Docker Hub**: https://hub.docker.com/_/rabbitmq

---

## 🔒 安全建议

1. **修改默认密码**: 安装后立即修改默认用户密码
2. **删除 guest 用户**: 生产环境删除默认 guest 用户
3. **启用 TLS**: 生产环境使用 SSL/TLS 加密连接
4. **配置防火墙**: 只开放必要的端口
5. **定期更新**: 保持 RabbitMQ 和 Erlang 为最新版本
6. **监控日志**: 定期检查日志文件，发现异常及时处理

---

**文档版本历史**：

| 版本 | 日期 | 作者 | 变更说明 |
|-----|------|------|---------|
| v1.0 | 2026-01-14 | AI助手 | 初始版本，支持 Windows/macOS/Linux/Docker |

---