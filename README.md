# 🚀 Anime Renamer Web (docker Edition)

[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://www.python.org/)

**专门为 NAS 动漫收藏家设计的一键批量重命名神器。**

## 🌟 为什么选择这个工具？

在使用 TinyMediaManager (TMM) 或 Plex 进行刮削时，很多压制组（如 **Moozzi2**, **VCB-Studio**）的文件名常导致识别错误：
- **压制组名干扰**：`[Moozzi2] ...` 里的 `2` 经常被刮削器当成集数。
- **分辨率干扰**：`1920x1080` 里的数字也会产生干扰。

**本工具核心逻辑：**
1. 自动忽略 `[]` 和 `()` 内的所有内容。
2. 自动剔除 `v2`, `v3` 等版本标识。
3. 在剩余文本中智能定位**最后一个数字序列**，精准提取集数。
4. 提供 WebUI 界面，完美适配 **飞牛 fnOS**、群晖、威联通等 Linux NAS 系统。

---

## ✨ 功能特性

- **可视化 Web 操作**：无需 SSH，浏览器端一键完成。
- **智能纠错**：预览阶段支持**原位双击编辑**，识别错了直接手动改，安全可靠。
- **自定义格式**：支持占位符 `{n}`(名称)、`{s}`(季数)、`{e}`(集数)，格式随心所欲。
- **Docker 部署**：极简部署，不污染 NAS 系统环境。
- **全格式兼容**：支持 `mkv`, `mp4`, `ass`, `srt` 等视频与字幕格式同步重命名。

---

## 📸 软件截图

*(建议在此处上传你的 Web 界面截图，命名为 `screenshot.png` 放在 assets 文件夹)*
<img width="1704" height="1060" alt="image" src="https://github.com/user-attachments/assets/46c51cf5-423d-410e-83ed-d41e63ba7fba" />


---

## 🚀 快速开始 (Docker 部署)

这是 NAS 用户最推荐的部署方式。

### 1. 运行 Docker 容器

在你的 NAS 终端执行以下命令，或者在 NAS 的 Docker 界面手动配置：

```bash
docker run -d \
  --name anime-renamer \
  -p 8000:8000 \
  -v /你的动漫真实路径:/data \
  --restart always \
  icecream110912138/anime-renamer-web:latest
```

**参数说明：**
- `-p 8000:8000`: 访问端口。
- `-v /你的动漫真实路径:/data`: **核心步骤**，将 NAS 存储番剧的文件夹映射到容器内的 `/data` 路径。

### 2. 开始使用
1. 浏览器访问 `http://NAS-IP:8000`。
2. **文件夹路径**：填写 `/data` (或者是 `/data/K-ON` 等子目录)。
3. **番剧名称**：输入识别后的标准名称。
4. **生成预览** -> **核对修改** -> **执行重命名**。

---

## 🛠 开发与手动运行

如果你想在本地开发环境运行：

1. 克隆仓库：
   ```bash
   git clone https://github.com/你的用户名/Anime-Renamer-GUI.git
   cd Anime-Renamer-GUI
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 启动后端：
   ```bash
   python main.py
   ```
4. 访问 `http://localhost:8000`。

---

## 📅 路线图 (Roadmap)

- [x] WebUI 界面开发
- [x] Docker 容器化
- [ ] 文件夹自动监控 (Watchdog 模式)
- [ ] 接入 qBittorrent API，下载完自动触发重命名
- [ ] 多语言支持

---

## 📄 开源协议
基于 [MIT License](LICENSE) 许可开源。

---

**IceCream110912138 倾情打造。如果你觉得好用，请点个 🌟 Star！**
