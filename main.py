import requests
from bs4 import BeautifulSoup
import os
import datetime

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

def get_fortune():
    url = "https://uranai.ac/horoscope/libra"
    res = requests.get(url, timeout=10)

    if res.status_code != 200:
        raise Exception(f"HTTPエラー: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")
    result = soup.select_one(".result")

    if not result:
        return None

    return result.get_text(strip=True)

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)

def main():
    try:
        data = get_fortune()

        today = datetime.datetime.now().strftime("%Y-%m-%d")

        if not data:
            send(f"⚠ 【てんびん座】{today}\n取得失敗（構造変更 or 空）")
            return

        send(f"""✅ 【てんびん座 今日の運勢】{today}

{data}
""")

    except Exception as e:
        send(f"❌ エラー\n{e}")

if __name__ == "__main__":
    main()
