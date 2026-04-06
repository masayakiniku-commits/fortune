import requests
from bs4 import BeautifulSoup
import datetime
import os

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

def get_goo_libra():
    try:
        url = "https://fortune.goo.ne.jp/12seiza/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select(".ranking li")

        for i, item in enumerate(items):
            text = item.get_text()
            if "てんびん座" in text:
                return i + 1

        return None

    except:
        return None

def main():
    today = datetime.date.today()

    rank = get_goo_libra()

    if rank:
        msg = f"🔮 てんびん座（{today}）\n👉 {rank}位 / 12位"
    else:
        msg = f"⚠️ 占い取得失敗（{today}）"

    send(msg)

if __name__ == "__main__":
    main()
