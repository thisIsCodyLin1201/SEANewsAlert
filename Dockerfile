# 使用 Python 3.11 官方映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴（WeasyPrint 需要）
RUN apt-get update && apt-get install -y \
    gcc \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    libcairo2 \
    libcairo2-dev \
    libgdk-pixbuf2.0-0 \
    libgdk-pixbuf2.0-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# 安裝 UV
RUN pip install --no-cache-dir uv

# 複製專案文件
COPY pyproject.toml .
COPY config.py .
COPY workflow.py .
COPY app.py .
COPY main.py .
COPY agents/ ./agents/
COPY templates/ ./templates/

# 安裝 Python 依賴
RUN uv pip install --system -e .

# 建立報告目錄
RUN mkdir -p reports

# 暴露 Streamlit 端口
EXPOSE 8501

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# 啟動命令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
