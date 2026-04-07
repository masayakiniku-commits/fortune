import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")


# -----------------------------
# ① めざまし占い（てんびん座）
# -----------------------------
def get_mezamashi():
    url = "https://www.fujitv.co.jp/meza/uranai/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # てんびん座を含む要素を探す
        items = soup.select("li")
        for item in items:
            text = item.text.strip()
            if "てんびん座" in text:
                return f"めざまし：{text}"

    except Exception as e:
        print("めざまし失敗:", e)

    return None


# -----------------------------
# ② Yahoo占い（てんびん座）
# -----------------------------
def get_yahoo():
    url = "https://fortune.yahoo.co.jp/12astro/libra/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        return "Yahoo：" + text[:120]  # 冒頭だけ

    except Exception as e:
        print("Yahoo失敗:", e)

    return None


# -----------------------------
# ③ 楽天占い（てんびん座）
# -----------------------------
def get_rakuten():
    url = "https://fortune.rakuten.co.jp/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select("li")
        for item in items:
            text = item.text.strip()
            if "てんびん座" in text:
                return f"楽天：{text}"

    except Exception as e:
        print("楽天失敗:", e)

    return None


# -----------------------------
# 送信
# -----------------------------
def send(msg):
    if not WEBHOOK:
        print("WEBHOOK未設定")
        return

    res = requests.post(WEBHOOK, json={"content": msg}, timeout=10)
    print("送信結果:", res.status_code)


# -----------------------------
# メイン
# -----------------------------
def main():
    print("===== 起動確認 =====")

    results = []

    for func in [get_mezamashi, get_yahoo, get_rakuten]:
        r = func()
        if r:
            results.append(r)

    if not results:
        results = ["てんびん座の占い取得失敗"]

    msg = "【てんびん座 今日の占い】\n\n" + "\n\n".join(results)
    print(msg)

    send(msg)


if __name__ == "__main__":
    main()
