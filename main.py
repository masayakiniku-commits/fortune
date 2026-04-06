import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def get_fortune():
    url = "https://uranaitv.jp/content/999"  # 安定して取れる例
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select("h3")[:3]  # 上位3件だけ
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

    requests.post(WEBHOOK, json={"content": msg})

def main():
    print("===== 起動確認 =====")

    data = get_fortune()

    if not data:
        send("取得失敗")
        return

    msg = "【占いランキング】\n" + "\n".join(data)
    print(msg)

    send(msg)

if __name__ == "__main__":
    main()
