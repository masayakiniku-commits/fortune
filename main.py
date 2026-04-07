import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def get_site1():
    try:
        url = "https://uranai-daily.com/libra"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        return text.strip()[:120]
    except:
        return "取得失敗"

def get_site2():
    try:
        url = "https://fortune.line.me/horoscope/libra/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        return text.strip()[:120]
    except:
        return "取得失敗"

def get_site3():
    try:
        url = "https://plaza.rakuten.co.jp/fortune/"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        return text.strip()[:120]
    except:
        return "取得失敗"

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def main():
    print("===== 起動確認 =====")

    s1 = get_site1()
    s2 = get_site2()
    s3 = get_site3()

    msg = f"""【てんびん座 今日の占い】

① {s1}

② {s2}

③ {s3}
"""
    send(msg)
    print("送信完了")

if __name__ == "__main__":
    main()
