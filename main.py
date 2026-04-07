import requests
import os
from bs4 import BeautifulSoup
import json

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
CACHE_FILE = "cache.json"


# -----------------------------
# ① メイン：めざまし占い
# -----------------------------
def get_fortune_main():
    url = "https://www.fujitv.co.jp/meza/uranai/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".ranking li")

        result = []
        for i, item in enumerate(items[:3], 1):
            text = item.text.strip()
            if text:
                result.append(f"{i}位：{text}")

        return result
    except Exception as e:
        print("メイン失敗:", e)
        return []


# -----------------------------
# ② サブ：別占いサイト
# -----------------------------
def get_fortune_sub():
    url = "https://uranai.tv/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("h3")

        result = []
        for i, item in enumerate(items[:3], 1):
            text = item.text.strip()
            if text:
                result.append(f"{i}位：{text}")

        return result
    except Exception as e:
        print("サブ失敗:", e)
        return []


# -----------------------------
# ③ キャッシュ保存
# -----------------------------
def save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return []
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# ④ Discord送信
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
# ⑤ メイン処理
# -----------------------------
def main():
    print("===== 起動確認 =====")

    data = get_fortune_main()

    if not data:
        print("→ サブサイト試行")
        data = get_fortune_sub()

    if not data:
        print("→ キャッシュ使用")
        data = load_cache()

    if not data:
        send("占い取得完全失敗（全滅）")
        return

    save_cache(data)

    msg = "【占いランキング】\n" + "\n".join(data)
    print(msg)

    send(msg)


if __name__ == "__main__":
    main()
