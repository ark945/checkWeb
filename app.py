import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="網站監控工具", page_icon="🌐")

st.title("🌐 網站狀態監控")
st.write("點擊下方按鈕以檢查 `urlList.txt` 中的網站狀態。")

def load_urls(filename='urlList.txt'):
    urls = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        current_name = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if it's a URL (simple check)
            if line.startswith('http://') or line.startswith('https://'):
                if current_name:
                    urls.append({'Name': current_name, 'URL': line})
                    current_name = None # Reset
            else:
                # Assume it's a name if it's not a URL and we interpret lines in pairs or blocks
                # Based on the file format: Name then URL.
                # Example:
                # 1: 基金相關系統驗證網址: (This looks like a header, might need to skip or treat as name)
                # 2: TAQ
                # 3: https://...
                
                # Heuristic: If the line doesn't start with http, treat it as a potential name.
                # However, looking at the file content provided in history:
                # Line 1: 基金相關系統驗證網址:
                # Line 2: TAQ
                # Line 3: https://...
                # Line 5: FDATA
                # Line 6: https://...
                
                # So we can treat any non-url line as a name. 
                # If we encounter two names in a row, the first one might be a section header or just previous name.
                # Let's just store the most recent non-url line as current_name.
                current_name = line
                
        return urls
    except FileNotFoundError:
        st.error(f"找不到檔案: {filename}")
        return []

def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        return {
            'Status': response.status_code,
            'Time (ms)': round(response.elapsed.total_seconds() * 1000, 2),
            'Result': '✅ 正常' if response.status_code == 200 else f'❌ 異常 ({response.status_code})'
        }
    except requests.exceptions.RequestException as e:
        return {
            'Status': 'Error',
            'Time (ms)': 0,
            'Result': f'⚠️ 無法連線'
        }

if st.button('開始檢查 🚀'):
    urls = load_urls()
    
    if not urls:
        st.warning("沒有找到網址或 urlList.txt 為空。")
    else:
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, item in enumerate(urls):
            status_text.text(f"正在檢查: {item['Name']} ({item['URL']})...")
            
            check_result = check_website(item['URL'])
            result_entry = {
                '名稱': item['Name'],
                '網址': item['URL'],
                '狀態': check_result['Result'],
                '回應時間 (ms)': check_result['Time (ms)'],
                '代碼': check_result['Status']
            }
            results.append(result_entry)
            progress_bar.progress((i + 1) / len(urls))
            
        status_text.text("檢查完成！")
        
        df = pd.DataFrame(results)
        st.dataframe(df)

        # Download button for report
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "下載檢測報告 (CSV)",
            csv,
            "website_status_report.csv",
            "text/csv",
            key='download-csv'
        )
