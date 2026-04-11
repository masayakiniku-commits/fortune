import requests
from bs4 import BeautifulSoup
import os
import datetime

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

# ========= 取得 =========
def get_fortune():
    url = "https://fortune.yahoo.co.jp/12astro/libra"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers, timeout=10)

    if res.status_code != 200:
        raise Exception(f"HTTPエラー: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")

    # Yahoo占いの本文（比較的安定な取り方）
    result = soup.find("p")

    if not result:
        return None

    text = result.get_text(strip=True)

    # 異常に短い場合は失敗扱い
    if len(text) < 20:
        return None

    return text

# ========= 通知 =========
def send(msg):
    requests.post(
        WEBHOOK_URL,
        json={"content": msg},
        timeout=10
    )

# ========= メイン =========
def main():
    try:
        data = get_fortune()
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        if not data:
            send(f"⚠ 【てんびん座】{today}\n取得失敗（構造変更 or 空）")
            return

        message = f"""✅ 【てんびん座 今日の運勢】{today}

{data}
"""
        send(message)

    except Exception as e:
        send(f"❌ エラー\n{e}")

# ========= 実行 =========
if __name__ == "__main__":
    main()
