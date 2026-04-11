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

        # てんびん座の位置を探す
        if "てんびん座" not in text:
            return None

        start = text.find("てんびん座")
        end = start + 300
        raw = text[start:end]

        # 不要な空白除去＆整形
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        result = "\n".join(lines)

        return f"""【てんびん座 今日の運勢】

{result}
"""

    except Exception as e:
        print("取得失敗:", e)
        return None


def send(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    except Exception as e:
        print("送信失敗:", e)


def main():
    print("===== 起動確認 =====")

    result = get_fortune()

    if not result:
        result = "【てんびん座 今日の運勢】\n\n取得失敗（サイト変更 or 一時エラー）"

    send(result)
    print("送信完了")


if __name__ == "__main__":
    main()
