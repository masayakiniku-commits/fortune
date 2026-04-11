import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_fortune():
    try:
        url = "https://uranai.nosv.org/u.php/honbun/12seiza/"

        res = requests.get(url, headers=HEADERS, timeout=10)

        print("status:", res.status_code)

        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()

        # 天秤座の部分だけ抜き出し
        if "てんびん座" in text:
            start = text.find("てんびん座")
            result = text[start:start+200]
        else:
            return None

        return f"""【てんびん座 今日の運勢】

{result}
"""

    except Exception as e:
        print("取得失敗:", e)
        return None

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def main():
    print("===== 起動確認 =====")

    result = get_fortune()

    if not result:
        result = "【てんびん座 今日の運勢】\n\n取得失敗（サイト変更 or 接続エラー）"

    send(result)
    print("送信完了")

if __name__ == "__main__":
    main()
