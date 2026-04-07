import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")


# -----------------------------
# ① めざまし占い（メイン）
# -----------------------------
def get_mezamashi():
    url = "https://www.fujitv.co.jp/meza/uranai/"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select(".ranking li")

        result = []
        for i, item in enumerate(items[:3], 1):
            text = item.text.strip()
            if text:
                result.append(f"{i}位：{text}")

        print("めざまし件数:", len(result))
        return result

    except Exception as e:
        print("めざまし失敗:", e)
        return []


# -----------------------------
# ② Yahoo占い（サブ）
# -----------------------------
def get_yahoo():
    url = "https://fortune.yahoo.co.jp/12astro/"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select("li")

        result = []
        for i, item in enumerate(items[:3], 1):
            text = item.text.strip()
            if text:
                result.append(f"{i}位：{text}")

        print("Yahoo件数:", len(result))
        return result

    except Exception as e:
        print("Yahoo失敗:", e)
        return []


# -----------------------------
# Discord送信
# -----------------------------
def send(msg):
    if not WEBHOOK:
        print("WEBHOOK未設定")
        return

    try:
        res = requests.post(WEBHOOK, json={"content": msg}, timeout=10)
        print("送信結果:", res.status_code)
    except Exception as e:
        print("送信エラー:", e)


# -----------------------------
# メイン処理
# -----------------------------
def main():
    print("===== 起動確認 =====")

    data = get_mezamashi()

    if not data:
        print("→ Yahooへフォールバック")
        data = get_yahoo()

    if not data:
        print("→ 最終フォールバック")
        data = ["本日の占いは取得できませんでした"]

    msg = "【今日の占い】\n" + "\n".join(data)
    print(msg)

    send(msg)


if __name__ == "__main__":
    main()
