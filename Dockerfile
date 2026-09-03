# 使用 Python 3.10 slim 作為基礎鏡像
FROM python:3.10-slim

# 設定環境變數
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    STREAMLIT_SERVER_PORT=10000 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 設定工作目錄
WORKDIR /app

# 安裝系統層級依賴套件 (Playwright 需求庫與繁體中文字體 fonts-noto-cjk，避免截圖亂碼)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    fonts-noto-cjk \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libxshmfence1 \
    libglu1-mesa \
    libnspr4 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# 複製 Python 依賴套件清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 預先下載並安裝 Playwright Chromium 核心瀏覽器
RUN playwright install chromium

# 複製專案程式碼
COPY . .

# 暴露端口 (Render 預設 10000)
EXPOSE 10000

# 啟動 Streamlit 服務 (支援 Render 動態指定之 $PORT)
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-10000} --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false"]
