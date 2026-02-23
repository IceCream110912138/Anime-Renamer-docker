# 1. 使用轻量级的 Python 镜像作为基础
FROM python:3.9-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 将当前目录下的文件复制到镜像的 /app 目录下
COPY requirements.txt .
COPY logic.py .
COPY main.py .
COPY static/ ./static/

# 4. 安装依赖
# 使用阿里云镜像源加速安装（适合国内 NAS 用户）
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 5. 暴露程序运行的端口
EXPOSE 8000

# 6. 启动程序
# 必须使用 0.0.0.0 才能让外部通过 NAS IP 访问
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]