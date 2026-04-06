import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {"User-Agent": "Mozilla/5.0"}

# =========================
# 共通関数
# =========================
def safe_request(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        return BeautifulSoup(res.text, "html.parser")
    except:
        return None

def score(rank):
    if not isinstance(rank, int):
        return 0
    if rank == 1: return 3
    if rank == 2: return 2
    if rank == 3: return 1
    return 0

# =========================
# 各サイト
# =========================
def get_yahoo():
    soup = safe_request("https://fortune.yahoo.co.jp/12astro/ranking.html")
    if not soup:
        return ("Yahoo", "エラー")

    items = soup.select("ol li")
    for i, item in enumerate(items, 1):
        if "てんびん座" in item.text:
            return ("Yahoo", i)

    return ("Yahoo", "取得失敗")


def get_fashion():
    soup = safe_request("https://www.fashion-press.net/horoscope/")
    if not soup:
        return ("Fashion", "エラー")

    items = soup.select("li")
    for i, item in enumerate(items, 1):
        if "てんびん座" in item.text:
            return ("Fashion", i)

    return ("Fashion", "取得失敗")


def get_goo():
    soup = safe_request("https://fortune.goo.ne.jp/ranking/")
    if not soup:
        return ("goo", "エラー")

    items = soup.select("li")
    for i, item in enumerate(items, 1):
        if "てんびん座" in item.text:
            return ("goo", i)

    return ("goo", "取得失敗")


# =========================
# Discord送信
# =========================
def send(msg):
    if not WEBHOOK_URL:
        print("Webhookなし")
        return

    try:
        r = requests.post(WEBHOOK_URL, json={"content": msg})
        print("送信:", r.status_code)
    except Exception as e:
        print("送信失敗:", e)

# =========================
# メイン
# =========================
def main():
    funcs = [get_yahoo, get_fashion, get_goo]

    results = []
    for f in funcs:
        try:
            results.append(f())
        except:
            results.append(("不明", "エラー"))

    print(results)

    today = datetime.now().strftime("%Y-%m-%d")

    msg = f"【てんびん座 総合運勢】\n{today}\n\n"

    total_score = 0
    valid_count = 0

    for site, rank in results:
        msg += f"{site}：{rank}位\n"

        if isinstance(rank, int):
            total_score += score(rank)
            valid_count += 1

    msg += "\n"

    # ===== 評価 =====
    if valid_count == 0:
        msg += "⚠️ 全サイト取得失敗"
    else:
        avg = total_score / valid_count

        if avg >= 2:
            msg += "🔥 かなり良い日"
        elif avg >= 1:
            msg += "○ そこそこ良い"
        else:
            msg += "△ ふつう〜注意"

    # TOP3判定
    if any(isinstance(r[1], int) and r[1] <= 3 for r in results):
        msg += "\n🎯 TOP3入りあり！"

    send(msg)


if __name__ == "__main__":
    main()
