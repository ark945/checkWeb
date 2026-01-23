# 專案完成與部署指南

我已成功建立 Streamlit 網站監控應用程式，並將程式碼推送至您的 GitHub：
👉 [https://github.com/ark945/checkWeb](https://github.com/ark945/checkWeb)

## 應用程式功能
- **讀取清單**: 自動讀取 `urlList.txt`。
- **狀態檢查**: 檢查網站 HTTP 狀態與回應時間。
- **報告下載**: 支援將檢查結果下載為 CSV。

## 🚀 如何部署到 Hugging Face Spaces

請依照以下步驟將此應用程式發布到 Hugging Face：

1.  **登入 Hugging Face**
    - 前往 [huggingface.co](https://huggingface.co/) 並登入您的帳號。

2.  **建立新 Space**
    - 點擊右上角頭像旁的 **New Space**。
    - **Space Name**: 輸入 `checkWeb` (或您喜歡的名字)。
    - **License**: 選擇 `MIT` 或留空。
    - **Select the Space SDK**: 選擇 **Streamlit** (這很重要！)。
    - 點擊 **Create Space**。

3.  **上傳程式碼 (最簡單的方法)**
    Space 建立後，您有幾種方式上傳程式碼，建議使用「**Files**」頁面直接上傳：
    - 在您的 Space 頁面，點選上方的 **Files** 標籤。
    - 點選 **Add file** -> **Upload files**。
    - 將您電腦中 `d:\MyLab\checkWeb` 資料夾內的以下檔案拖曳上傳：
        - `app.py`
        - `requirements.txt`
        - `packages.txt` (新增：用於截圖功能)
        - `urlList.txt`
        - `README.md`
    - 在 "Commit changes" 訊息框輸入 "Add screenshot function"，然後點擊 **Commit changes to main**。

    > **進階方法 (同步 GitHub)**:
    > 您也可以在 Space 的 **Settings** 中，找到 "Docker" 或相關設定來連結 GitHub Repository，這樣每次 GitHub 更新時 Space 也會自動更新。但直接上傳檔案通常最快。

4.  **等待建置**
    - 上傳後，Hugging Face 會自動開始安裝 `requirements.txt` 中的套件並啟動應用程式。
    - 等待幾分鐘，直到狀態顯示為 **Running**。

5.  **測試**
    - 您的應用程式現在應該可以在 Space 頁面上直接使用了！
