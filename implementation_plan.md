# 在 Hugging Face Spaces 建立 URL 監控應用程式

目標是在 Hugging Face Spaces 上建立一個簡單的網頁應用程式，該程式讀取文字檔案中的 URL 列表，並在點擊按鈕後檢查它們的狀態（可用性）。

## 需要使用者審查
> [!NOTE]
> 我選擇了 **Streamlit** 作為框架，因為它允許使用內建組件（按鈕、表格）快速開發以數據為中心的網頁應用程式。

## 建議變更

### 專案結構
專案將包含在一個目錄中（例如 `d:\MyLab\checkWeb`）。
為 Hugging Face Spaces 設計的檔案：

#### [NEW] [app.py](file:///d:/MyLab/checkWeb/app.py)
- **函式庫**: Streamlit, Requests
- **邏輯**:
    - 讀取相對於腳本的 `urlList.txt`。
    - 解析檔案格式（交替的名稱與 URL）。
    - 顯示「開始檢查」按鈕。
    - 點擊後：迭代 URL，發送 HTTP GET 請求（帶有超時設定）。
    - 收集 HTTP 狀態碼與回應時間。
    - 在 Streamlit DataFrame 或表格中顯示結果。

#### [NEW] [requirements.txt](file:///d:/MyLab/checkWeb/requirements.txt)
- `streamlit`
- `requests`
- `pandas` (選用，用於更美觀的表格)

## 驗證計畫

### 自動化測試
- 此簡單腳本不計畫進行自動化測試。

### 手動驗證
1.  **本地執行**: 在本地執行 `streamlit run app.py`。
2.  **互動**: 點擊按鈕並驗證：
    - 檔案是否正確讀取。
    - 是否發送了真實的 HTTP 請求。
    - 結果（成功/失敗）是否正確顯示。
