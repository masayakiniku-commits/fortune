import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_wikipedia():
    try:
        url = "https://ja.wikipedia.org/wiki/天秤座"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        p = soup.find("p")
        return p.get_text().strip()[:120]
    except Exception as e:
        print("wiki失敗:", e)
        return None

def get_line_fortune():
    try:
        url = "https://fortune.line.me/horoscope/libra/"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        return text.strip().replace("\n", "")[:120]
    except Exception as e:
        print("LINE失敗:", e)
        return None

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def main():
    print("===== 起動確認 =====")

    results = []

    w = get_wikipedia()
    if w:
        results.append("① " + w)

    l = get_line_fortune()
    if l:
        results.append("② " + l)

    if not results:
        msg = "【てんびん座 今日の占い】\n\n取得できませんでした"
    else:
        msg = "【てんびん座 今日の占い】\n\n" + "\n\n".join(results)

    send(msg)
    print("送信完了")

if __name__ == "__main__":
    main()
