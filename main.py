import requests
import os
from bs4 import BeautifulSoup

# 環境変数取得（統一）
WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def get_fortune():
    url = "https://uranaitv.jp/content/999"
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print("取得エラー:", e)
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select("h3")[:3]
    result = []

    for i, item in enumerate(items, 1):
        text = item.text.strip()
        if text:
            result.append(f"{i}位：{text}")

    return result


def send(msg):
    if not WEBHOOK:
        print("WEBHOOK未設定")
        return

    try:
        res = requests.post(WEBHOOK, json={"content": msg}, timeout=10)
        print("送信結果:", res.status_code)
    except Exception as e:
        print("送信エラー:", e)


def main():
    print("===== 起動確認 =====")
    print("Webhook確認:", "OK" if WEBHOOK else "NG")

    data = get_fortune()

    if not data:
        send("占い取得失敗")
        return

    msg = "【占いランキング】\n" + "\n".join(data)
    print(msg)

    send(msg)


if __name__ == "__main__":
    main()
