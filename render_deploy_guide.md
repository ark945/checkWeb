# Render.com 雲端部署指南 (checkWeb 網站監控與截圖工具)

本指南說明如何將 **網站狀態監控與截圖工具 (`checkWeb`)** 部署至 [Render.com](https://render.com/)，徹底解決 Hugging Face Spaces 易發生的 Playwright 瀏覽器建置失敗、缺少系統相依函式庫與連線逾時問題。

---

## 🌟 為什麼選擇 Render.com 部署 Streamlit + Playwright？

| 比較特性 | Hugging Face Spaces | Render.com (Docker) |
| :--- | :--- | :--- |
| **Playwright 支援度** | 依賴執行時動態安裝，常因缺少系統庫或逾時導致 Build/Runtime Error | **Docker 映像檔於建置時直接預裝 Chromium 與完整系統函式庫，100% 穩定啟動** |
| **中文字體渲染** | 偶有字體缺失問題，截圖中文容易變成方框 (`□`) | **內建 `fonts-noto-cjk` 完整字型庫，台灣/繁體網頁截圖完美呈現** |
| **伺服器區域** | 美國東部 (連線延遲高，偶有網路波動) | **新加坡 (Singapore)**，對台灣與亞洲目標網站檢測極速 (< 50ms) |
| **CI/CD 自動發布** | 需額外手動同步至 HF git | **自動與 GitHub 倉庫同步，`git push` 即自動打包上線** |

---

## 📋 準備工作

1. **GitHub 倉庫**：確認本機程式碼已推送到您的 GitHub 倉庫（例如：`https://github.com/ark945/checkWeb`）。
2. **Render.com 帳號**：若無帳號，請前往 [Render 官網](https://render.com/) 直接使用 GitHub 帳號快速登入。

---

## 🔐 環境變數 (Environment Variables) 設定一覽

本專案無需外接資料庫或機密密鑰，Render 預設會自動注入 `$PORT`。建議設定以下環境變數以優化效能：

| 變數名稱 (Key) | 建議數值 | 功能說明 |
| :--- | :---: | :--- |
| `PYTHONUNBUFFERED` | `1` | 強制 Python standard output 即時輸出日誌至 Render 控制台 |
| `STREAMLIT_SERVER_HEADLESS` | `true` | 強制 Streamlit 以無頭背景伺服器模式運行 |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | `false` | 關閉 Streamlit 遙測數據收集，提升隱私與執行效能 |

---

## 🚀 部署方式 (二選一)

> [!IMPORTANT]
> **專屬網域名稱規範**：
> 依據國際網域名稱規範 (RFC 1123 / DNS 標準)，主機名稱與子網域**不允許使用底線 `_`**。建議使用英數字與連字號 `-`，例如 `check-web` 或 `ark-check-web`。

---

### 方式一：Blueprint 自動一鍵部署 (推薦最快)

專案已內建 [`render.yaml`](file:///d:/MyLab/checkWeb/render.yaml) 基礎設施設定檔：

1. 登入 [Render Dashboard](https://dashboard.render.com/)。
2. 點擊右上角 **"New +"** 按鈕，選擇 **"Blueprint"**。
3. 連接您的 GitHub 帳號並選取 **`checkWeb`** 倉庫。
4. **Blueprint Name**：輸入 **`check-web`** (或自訂名稱)。
5. 點擊 **"Apply"**。
6. Render 會自動解析 `render.yaml` 並依照 Dockerfile 自動編譯、安裝 Chromium 瀏覽器並部署上線！

---

### 方式二：手動在 Dashboard 建立 Web Service

1. 登入 [Render Dashboard](https://dashboard.render.com/)。
2. 點擊右上角 **"New +"** -> 選擇 **"Web Service"**。
3. 選擇 **"Build and deploy from a Git repository"**，點擊 **Next**。
4. 選擇您的 GitHub 倉庫 `checkWeb`。
5. 填寫服務基本設定：
   - **Name**：輸入 **`check-web`** (專屬網址將為：`https://check-web.onrender.com`)
   - **Region**：選擇 **Singapore**（新加坡節點）
   - **Branch**：`main`
   - **Runtime**：選擇 **Docker** (專案已內建 Playwright 專用 Dockerfile)
   - **Instance Type**：選擇 **Free** (免費方案)
6. 展開 **"Advanced"** 進階設定：
   - **Health Check Path**：填入 `/_stcore/health` (Streamlit 原生健康檢查端點)
7. 點擊底部的 **"Create Web Service"** 即可開始自動建置。

---

## 🔍 驗證部署狀態

1. 等候約 2~3 分鐘構建完成（Docker 會自動完成 Debian 系統庫與 Chromium 下載），日誌顯示：
   ```text
   You can now view your Streamlit app in your browser.
   URL: http://0.0.0.0:10000
   ```
2. 當服務狀態顯示為綠色 **"Live"** 即代表部署成功。
3. 點擊進入專屬網址：
   👉 **`https://check-web.onrender.com/`**
4. 點擊畫面上的 **「開始檢查 🚀」** 按鈕，即可自動依據 `urlList.txt` 檢測各網站連線狀態、拍攝截圖，並支援一鍵下載 CSV 與含截圖之 Word 完整報表！

---

## ⚡ 實用技巧：防止免費版休眠 (Keep-Alive)

> [!NOTE]
> Render 免費實例若在 **15 分鐘內無連線請求**，會自動進入休眠狀態。休眠後首次喚醒容器需時約 30~50 秒。

若希望隨時秒開，可使用免費的心跳監控服務定期 Ping 健康檢查端點：

### 使用 [cron-job.org](https://cron-job.org/) 或 [UptimeRobot](https://uptimerobot.com/)
1. 註冊免費帳號並新增監控項目 (New Monitor / Cronjob)。
2. **URL**：填寫您的健康檢查網址：
   `https://check-web.onrender.com/_stcore/health`
3. **頻率 (Interval)**：設定為 **每 10 分鐘或 12 分鐘** 發送一次 GET 請求。
4. 儲存啟用後，即可 24 小時保持容器常駐活躍！

---

## 🌐 綁定自有網域 (Custom Domain)

1. 在 Render Web Service 頁面中，點擊左側 **"Settings"**。
2. 滾動至 **"Custom Domains"** 區塊，點擊 **"Add Custom Domain"**。
3. 輸入您的網域名稱（例如：`check.yourdomain.com`）。
4. 在 DNS 託管商新增一條 **CNAME** 紀錄指向 `check-web.onrender.com` 即可。
