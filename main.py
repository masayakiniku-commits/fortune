import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_site1():
    try:
        url = "https://uranai-daily.com/libra"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()
        return text.strip().replace("\n", "")[:120]
    except Exception as e:
        print("site1失敗:", e)
        return None

def get_site2():
    try:
        url = "https://fortune.line.me/horoscope/libra/"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()
        return text.strip().replace("\n", "")[:120]
    except Exception as e:
        print("site2失敗:", e)
        return None

def get_site3():
    try:
        url = "https://uranai.nifty.com/libra/"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()
        return text.strip().replace("\n", "")[:120]
    except Exception as e:
        print("site3失敗:", e)
        return None

def send_discord(message):
    if not WEBHOOK_URL:
        print("WEBHOOK未設定")
        return
    requests.post(WEBHOOK_URL, json={"content": message})

def main():
    print("===== 起動確認 =====")

    results = []

    s1 = get_site1()
    if s1:
        results.append("① " + s1)

    s2 = get_site2()
    if s2:
        results.append("② " + s2)

    s3 = get_site3()
    if s3:
        results.append("③ " + s3)

    if not results:
        message = "【てんびん座 今日の占い】\n\n取得できませんでした"
    else:
        message = "【てんびん座 今日の占い】\n\n" + "\n\n".join(results)

    send_discord(message)
    print("送信完了")

if __name__ == "__main__":
    main()
