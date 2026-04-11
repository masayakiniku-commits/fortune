import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja-JP,ja;q=0.9"
}

# ------------------------
# 各サイト取得関数
# ------------------------

def yahoo():
    try:
        url = "https://fortune.yahoo.co.jp/12astro/libra"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        p = soup.find("p")
        if p:
            text = p.get_text(strip=True)
            if len(text) > 20:
                return f"Yahoo占い:\n{text}"
    except:
        return None


def goo():
    try:
        url = "https://fortune.goo.ne.jp/fortune/today/libra/"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        p = soup.find("p")
        if p:
            text = p.get_text(strip=True)
            if len(text) > 20:
                return f"goo占い:\n{text}"
    except:
        return None


def rakuten():
    try:
        url = "https://fortune.rakuten.co.jp/"
        res = requests.get(url, headers=headers, timeout=10)

        if "天秤座" in res.text:
            return "楽天占い: 今日の運勢チェック（簡易）"
    except:
        return None


def fallback():
    return "⚠ 占い取得失敗（全サイトNG）\n今日は静観が吉"

# ------------------------
# メインロジック
# ------------------------

def get_fortune():
    funcs = [yahoo, goo, rakuten]

    for func in funcs:
        result = func()
        if result:
            return result

    return fallback()

# ------------------------
# Discord送信
# ------------------------

def send_discord(message):
    data = {
        "content": message
    }
    requests.post(WEBHOOK_URL, json=data)

# ------------------------
# 実行
# ------------------------

if __name__ == "__main__":
    try:
        fortune = get_fortune()
        send_discord(f"🔮 今日の占い\n\n{fortune}")
    except Exception as e:
        send_discord(f"❌ エラー\n{str(e)}")
