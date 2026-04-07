import requests
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_fortune():
    try:
        url = "https://aztro.sameerkumar.website/"
        params = {
            "sign": "libra",
            "day": "today"
        }

        res = requests.post(url, params=params, headers=HEADERS, timeout=10)

        print("status:", res.status_code)
        print("body:", res.text[:100])  # ←デバッグ

        if res.status_code != 200:
            return None

        data = res.json()

        return f"""【てんびん座 今日の運勢】

■ 総合運：
{data.get('description','')}

■ ラッキーナンバー：{data.get('lucky_number','')}
■ ラッキーカラー：{data.get('color','')}
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
        result = "【てんびん座 今日の運勢】\n\n取得失敗（API応答異常）"

    send(result)
    print("送信完了")

if __name__ == "__main__":
    main()
