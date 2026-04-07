import requests
import os
import datetime

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def get_fortune():
    try:
        url = "https://aztro.sameerkumar.website/?sign=libra&day=today"
        res = requests.post(url, timeout=10)
        data = res.json()

        return f"""【てんびん座 今日の運勢】

■ 総合運：
{data['description']}

■ ラッキーナンバー：{data['lucky_number']}
■ ラッキーカラー：{data['color']}
"""
    except Exception as e:
        print("API失敗:", e)
        return None

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def main():
    print("===== 起動確認 =====")

    result = get_fortune()

    if not result:
        result = "【てんびん座 今日の運勢】\n\n取得失敗"

    send(result)
    print("送信完了")

if __name__ == "__main__":
    main()
