import requests
import os

url = os.environ["DISCORD_WEBHOOK"]

try:
    data = "←ここに取得結果"

    if not data:
        requests.post(url, json={"content": "⚠ データ空"})
    else:
        requests.post(url, json={"content": "正常取得"})

except Exception as e:
    requests.post(url, json={"content": f"エラー: {e}"})
    
