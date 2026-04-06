import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_rank_from_text(url, site_name):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        text = res.text

        signs = [
            "おひつじ座","おうし座","ふたご座","かに座","しし座","おとめ座",
            "てんびん座","さそり座","いて座","やぎ座","みずがめ座","うお座"
        ]

        if "てんびん座" not in text:
            return (site_name, "取得失敗")

        # 出現順で順位判定（簡易だが安定）
        order = []
        for s in signs:
            pos = text.find(s)
            if pos != -1:
                order.append((s, pos))

        order.sort(key=lambda x: x[1])

        for i, (s, _) in enumerate(order, 1):
            if s == "てんびん座":
                return (site_name, i)

        return (site_name, "不明")

    except:
        return (site_name, "エラー")


def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})


def main():
    sites = [
        ("Yahoo", "https://fortune.yahoo.co.jp/12astro/ranking.html"),
        ("goo", "https://fortune.goo.ne.jp/ranking/"),
        ("Rakuten", "https://fortune.rakuten.co.jp/"),
    ]

    results = [get_rank_from_text(url, name) for name, url in sites]

    today = datetime.now().strftime("%Y-%m-%d")

    msg = f"【てんびん座 総合運勢】\n{today}\n\n"

    success = False

    for site, rank in results:
        msg += f"{site}：{rank}位\n"
        if isinstance(rank, int):
            success = True

    if not success:
        msg += "\n⚠️ 全サイト取得失敗"

    send(msg)


if __name__ == "__main__":
    main()
