import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ===== サイト1（Yahoo）=====
def get_yahoo():
    url = "https://fortune.yahoo.co.jp/12astro/ranking.html"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        ranks = soup.select("li")
        results = []

        for i, r in enumerate(ranks, start=1):
            text = r.get_text()
            if "てんびん座" in text:
                results.append(("Yahoo", i))

        return results if results else [("Yahoo", "取得失敗")]
    except Exception as e:
        return [("Yahoo", f"エラー")]


# ===== サイト2（FashionPress）=====
def get_fashion():
    url = "https://www.fashion-press.net/horoscope/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        ranks = soup.select("li")
        results = []

        for i, r in enumerate(ranks, start=1):
            text = r.get_text()
            if "てんびん座" in text:
                results.append(("FashionPress", i))

        return results if results else [("FashionPress", "取得失敗")]
    except Exception as e:
        return [("FashionPress", f"エラー")]


# ===== Discord送信 =====
def send_discord(msg):
    if not WEBHOOK_URL:
        print("Webhook未設定")
        return

    data = {"content": msg}
    try:
        res = requests.post(WEBHOOK_URL, json=data, timeout=10)
        print("Discord:", res.status_code)
    except Exception as e:
        print("Discord送信エラー:", e)


# ===== メイン処理 =====
def main():
    results = []

    # 各サイト取得（死んでも止まらない）
    for func in [get_yahoo, get_fashion]:
        try:
            results.extend(func())
        except Exception as e:
            results.append(("不明サイト", "致命的エラー"))

    print("取得結果:", results)

    # ===== メッセージ生成 =====
    today = datetime.now().strftime("%Y-%m-%d")
    msg = f"【てんびん座 今日の運勢】\n{today}\n\n"

    top3_flag = False

    for site, rank in results:
        msg += f"{site}：{rank}位\n"

        if isinstance(rank, int) and rank <= 3:
            top3_flag = True

    if top3_flag:
        msg += "\n🔥 TOP3入りあり！"

    # 全部ダメだった場合
    if all(not isinstance(r[1], int) for r in results):
        msg += "\n⚠️ すべてのサイトで取得失敗"

    # ===== 必ず送信 =====
    send_discord(msg)


if __name__ == "__main__":
    main()
