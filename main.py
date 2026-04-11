import requests
from bs4 import BeautifulSoup
import os
import datetime

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# ========= 取得処理 =========
def get_fortune():
    url = "https://uranai.ac/horoscope/libra"  # ←必要なら変更
    res = requests.get(url, timeout=10)

    if res.status_code != 200:
        raise Exception(f"HTTPエラー: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")

    # ※ここはサイト構造に応じて調整
    result = soup.select_one(".result")

    if not result:
        return None

    return result.get_text(strip=True)

# ========= 通知 =========
def send_discord(message):
    res = requests.post(
        WEBHOOK_URL,
        json={"content": message},
        timeout=10
    )
    print("status:", res.status_code)
    print("body:", res.text)

# ========= メイン =========
def main():
    print("===== 起動確認 =====")

    try:
        data = get_fortune()

        if not data:
            send_discord("⚠ 【てんびん座 今日の運勢】取得できず（構造変更 or 空）")
            return

        today = datetime.datetime.now().strftime("%Y-%m-%d")

        message = f"""【てんびん座 今日の運勢】
{today}

{data}
"""

        send_discord("✅ 正常取得\n" + message)

    except Exception as e:
        send_discord(f"❌ エラー発生\n{e}")

# ========= 実行 =========
if __name__ == "__main__":
    main()
