# checkWeb 專案移植至 Render.com 規劃方案

本規劃旨在將 **`checkWeb`** (網站狀態監控與自動截圖工具) 從 Hugging Face Spaces 遷移至 **[Render.com](https://render.com/)** 雲端平台，透過專屬 Docker 容器化技術徹底解決 Playwright 瀏覽器依賴套件、中文字體亂碼 (□) 與啟動超時問題。

---

## 評估與架構調整分析

### 1. 現狀問題與痛點
- **Hugging Face Spaces 限制**：HF Spaces 依靠 `packages.txt` 與執行時安裝 Playwright，易因權限、套件依賴遺失或建置超時產生 Build/Runtime Error。
- **依賴套件缺失**：目前 `requirements.txt` 未包含 `streamlit` 與 `pandas`（之前依賴 HF 內建環境），脫離 HF 後無法直接啟動。
- **無 Docker 封裝**：Playwright 在 Linux 容器中需要 X11、NSS、GBM 等底層系統函式庫與中文字體 (`fonts-noto-cjk`)，若無專屬 Docker 鏡像，在雲端伺服器極易崩潰。

### 2. 改造重點
1. **專屬 Dockerfile 封裝**：
   - 採用 `python:3.10-slim` 基礎鏡像。
   - 預先安裝 `fonts-noto-cjk`（防止台灣/繁體網頁截圖變框框亂碼）與 Playwright 完整依賴庫。
   - 在 Docker Build 階段執行 `playwright install chromium`，避免容器啟動時重複下載造成超時。
2. **依賴套件補全 (`requirements.txt`)**：
   - 明確加入 `streamlit>=1.41.0` 與 `pandas`。
3. **動態端口與無頭模式綁定**：
   - 指令調整為：`streamlit run app.py --server.port=${PORT:-10000} --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false`。
4. **健康檢查端點**：
   - 使用 Streamlit 原生健康檢查端點 `/_stcore/health`，提供 Render 自動存活檢測與防休眠 Ping。
5. **基礎設施規格 (`render.yaml`)**：
   - 建立 Render Blueprint，宣告新加坡節點 (`singapore`)、免費方案 (`plan: free`) 與健康檢查。
6. **編寫說明文件與操作手冊**：
   - 建立專屬部署指南 `render_deploy_guide.md`。
   - 依規範編寫完整 `操作手冊.md`。

---

## 雲端環境變數 (Environment Variables) 規劃

| 變數名稱 (Key) | 必填/選填 | 預設建議值 | 說明 |
| :--- | :---: | :--- | :--- |
| `PYTHONUNBUFFERED` | 建議 | `1` | 強制 Python standard output 即時輸出日誌至 Render 控制台 |
| `STREAMLIT_SERVER_HEADLESS` | 建議 | `true` | 強制 Streamlit 以無頭模式 (Headless) 運行 |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | 建議 | `false` | 關閉 Streamlit 遙測統計以提升隱私與效能 |

---

## 變更項目清單
1. `requirements.txt`：加入 `streamlit>=1.41.0` 與 `pandas`。
2. `Dockerfile`：完整 Playwright + 中文字體 + 依賴套件環境封裝。
3. `render.yaml`：Render Blueprint 基礎設施定義。
4. `render_deploy_guide.md`：Render 部署步驟說明手冊。
5. `操作手冊.md`：符合規範之系統操作手冊。
