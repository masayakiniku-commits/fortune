import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja-JP,ja;q=0.9"
}

# ------------------------
# 通信テスト ← ここに追加①
# ------------------------
def test_connection():
    try:
        res = requests.get("https://www.google.com", timeout=5)
        return f"通信OK: {res.status_code}"
    except Exception as e:
        return f"通信NG: {str(e)}"


# ------------------------
# 占い取得
# ------------------------
def get_fortune():
    return "仮の占い結果"  # 今は適当でOK


# ------------------------
# Discord送信
# ------------------------
def send_discord(message):
    requests.post(WEBHOOK_URL, json={"content": message})


# ------------------------
# 実行 ← ここに追加②（ここが一番重要）
# ------------------------
if __name__ == "__main__":
    try:
        # ★ここに入れる（最初に通信確認）
        status = test_connection()
        send_discord(f"🌐 通信テスト\n{status}")

        # ★そのあと占い
        fortune = get_fortune()
        send_discord(f"🔮 今日の占い\n\n{fortune}")

    except Exception as e:
        send_discord(f"❌ エラー\n{str(e)}")
