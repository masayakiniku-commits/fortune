import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def get_site1():
    url = "https://fortune.yahoo.co.jp/12astro/ranking.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    ranks = soup.select(".rankingList li")

    for i, r in enumerate(ranks, start=1):
        sign = r.select_one(".name").text.strip()
        if "てんびん座" in sign:
            results.append(("Yahoo占い", i))
    return results

def get_site2():
    url = "https://www.fashion-press.net/horoscope/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    ranks = soup.select(".horoscope-ranking li")

    for i, r in enumerate(ranks, start=1):
        sign = r.text.strip()
        if "てんびん座" in sign:
            results.append(("FashionPress", i))
    return results

def send_discord(message):
    data = {
        "content": message
    }
    requests.post(WEBHOOK_URL, json=data)

def main():
    all_results = []

    for func in [get_site1, get_site2]:
        try:
            all_results.extend(func())
        except:
            pass

    # 3位以内のみ
    top_results = [r for r in all_results if r[1] <= 3]

    if not top_results:
        return

    today = datetime.now().strftime("%Y-%m-%d")

    msg = f"【てんびん座 今日の運勢TOP3入り】\n{today}\n\n"

    for site, rank in top_results:
        msg += f"{site}：{rank}位\n"

    send_discord(msg)

if __name__ == "__main__":
    main()
