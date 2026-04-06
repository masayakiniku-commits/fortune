import requests
import xml.etree.ElementTree as ET
import datetime
import os

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def send(msg):
    try:
        r = requests.post(WEBHOOK, json={"content": msg})
        print("送信:", r.status_code)
    except Exception as e:
        print("送信エラー:", e)

# ★ 安定：RSS取得
def get_rss():
    try:
        url = "https://uranaitv.jp/feed"
        res = requests.get(url, timeout=10)

        root = ET.fromstring(res.content)

        items = root.findall(".//item")

        results = []

        for i, item in enumerate(items[:3]):
            title = item.find("title").text
            results.append(f"{i+1}位 {title}")

        return ("占いTV", results if results else ["取得失敗"])

    except Exception as e:
        print("RSSエラー:", e)
        return ("占いTV", ["エラー"])

# ★ 保険（絶対通知）
def fallback():
    return ("システム", [
        "1位 今日はバランスがカギ",
        "2位 人間関係に良い流れ",
        "3位 焦らずが吉"
    ])

def main():
    print("===== 起動確認 =====")

    today = datetime.date.today()
    msg = f"🔮 てんびん座占い（{today}）\n"

    results = []

    rss = get_rss()
    results.append(rss)

    # ★ 取得ダメなら保険発動
    if "エラー" in str(rss) or "取得失敗" in str(rss):
        results.append(fallback())

    print("取得結果:", results)

    for site, data in results:
        msg += f"\n【{site}】\n"
        for d in data:
            msg += d + "\n"

    send(msg)

if __name__ == "__main__":
    main()
