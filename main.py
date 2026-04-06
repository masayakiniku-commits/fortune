import requests
from bs4 import BeautifulSoup
import datetime
import os

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def send(msg):
    try:
        r = requests.post(WEBHOOK, json={"content": msg})
        print("送信:", r.status_code)
    except Exception as e:
        print("送信エラー:", e)

def get_yahoo():
    try:
        url = "https://fortune.yahoo.co.jp/12astro/libra"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select(".ranking li")
        results = []

        for i, item in enumerate(items[:3]):
            txt = item.get_text(strip=True)
            results.append(f"{i+1}位 {txt}")

        return ("Yahoo", results if results else ["取得失敗"])

    except:
        return ("Yahoo", ["エラー"])

def get_fashion():
    try:
        url = "https://www.fashion-press.net/horoscope/libra"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select(".horoscope-ranking li")
        results = []

        for i, item in enumerate(items[:3]):
            txt = item.get_text(strip=True)
            results.append(f"{i+1}位 {txt}")

        return ("Fashion", results if results else ["取得失敗"])

    except:
        return ("Fashion", ["エラー"])

def get_goo():
    try:
        url = "https://fortune.goo.ne.jp/12seiza/libra/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select(".ranking li")
        results = []

        for i, item in enumerate(items[:3]):
            txt = item.get_text(strip=True)
            results.append(f"{i+1}位 {txt}")

        return ("goo", results if results else ["取得失敗"])

    except:
        return ("goo", ["エラー"])

def main():
    print("===== 起動確認 =====")

    today = datetime.date.today()
    msg = f"🔮 てんびん座占いランキング（{today}）\n"

    results = []
    results.append(get_yahoo())
    results.append(get_fashion())
    results.append(get_goo())

    print("取得結果:", results)

    for site, data in results:
        msg += f"\n【{site}】\n"
        for d in data:
            msg += d + "\n"

    # ★必ず送信（ここが重要）
    send(msg)

if __name__ == "__main__":
    main()
