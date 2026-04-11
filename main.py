import requests
from bs4 import BeautifulSoup
import os
import datetime

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

# ===== ここに入れる =====
def get_fortune():
    url = "https://fortune.yahoo.co.jp/12astro/libra"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for _ in range(3):  # リトライ
        try:
            res = requests.get(url, headers=headers, timeout=10)
            break
        except:
            continue
    else:
        raise Exception("通信失敗")

    if res.status_code != 200:
        raise Exception(f"HTTPエラー: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")
    result = soup.find("p")

    if not result:
        return None

    text = result.get_text(strip=True)

    if len(text) < 20:
        return None

    return text
# ===== ここまで =====


def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)


def main():
    try:
        data = get_fortune()  # ←ここで呼び出す

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
