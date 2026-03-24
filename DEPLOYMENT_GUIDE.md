# 網站狀態監控工具 - 部署指南

## 應用程式功能
- **狀態檢查**: 自動檢查網站 HTTP 狀態與回應時間
- **網頁截圖**: 使用 Playwright 對每個網站進行截圖
- **CSV 報告**: 匯出檢測結果為 CSV
- **Word 報告**: 匯出包含截圖的完整 Word 報告

## 🚀 部署到 Hugging Face Spaces

### 方法一：透過 Git 直接推送（推薦）

```bash
# 1. 新增 Hugging Face 為遠端儲存庫（首次設定）
git remote add hf https://huggingface.co/spaces/ark945/checkWeb

# 2. 推送到 Hugging Face
git push hf main

# 3. 如果推送被拒絕（歷史紀錄不同），使用強制推送
git push hf main --force
```

### 方法二：同時推送到 GitHub 與 Hugging Face

```bash
# 推送到 GitHub
git push origin main

# 推送到 Hugging Face
git push hf main
```

### 方法三：手動上傳

1. 前往 [https://huggingface.co/spaces/ark945/checkWeb](https://huggingface.co/spaces/ark945/checkWeb)
2. 點選上方的 **Files** 標籤
3. 點選 **Add file** → **Upload files**
4. 上傳以下檔案：
   - `app.py`
   - `requirements.txt`
   - `packages.txt`
   - `urlList.txt`
   - `README.md`
   - `.gitattributes`
5. 點擊 **Commit changes to main**

### 注意事項

- `packages.txt` 和 `requirements.txt` 必須使用 **LF 換行格式**（不可使用 Windows 的 CRLF），否則 Linux 環境會讀取錯誤。專案中的 `.gitattributes` 已自動處理此問題。
- Hugging Face 會根據 `README.md` 中的 `sdk_version` 自動安裝 Streamlit，因此 `requirements.txt` 中**不需要**包含 `streamlit`。

## 🔧 常見問題

| 問題 | 解決方式 |
|------|----------|
| 截圖中文亂碼 (□) | `packages.txt` 已包含 `fonts-noto-cjk` |
| 時間差 8 小時 | 程式已設定台灣時區 (UTC+8) |
| Build error: Unable to locate package | 確認 `.gitattributes` 已上傳，強制 LF 換行 |
| Runtime error: Could not resolve host | 點擊 Space 的「Restart this Space」重啟 |
| Failed to fetch module | 按 `Ctrl+Shift+R` 強制重新整理瀏覽器快取 |
