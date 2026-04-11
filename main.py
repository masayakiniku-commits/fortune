import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_fortune():
    try:
        url = "https://fortune.yahoo.co.jp/12astro/libra"

        res = requests.get(url, headers=HEADERS, timeout=10)

        print("status:", res.status_code)

        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        # 総合運
        desc = soup.select_one(".yjS .lead")
        desc_text = desc.text.strip() if desc else "取得失敗"

        # ラッキー系
        lucky = soup.select(".yjS dl dd")
        lucky_items = [x.text.strip() for x in lucky]

        return f"""【てんびん座 今日の運勢】

■ 総合運：
{desc_text}

■ ラッキーカラー：{lucky_items[0] if len(lucky_items)>0 else ""}
■ ラッキーアイテム：{lucky_items[1] if len(lucky_items)>1 else ""}
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
        result = "【てんびん座 今日の運勢】\n\n取得失敗（スクレイピング異常）"

    send(result)
    print("送信完了")

if __name__ == "__main__":
    main()
