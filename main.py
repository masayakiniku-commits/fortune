import requests
import datetime
import os
import random

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def send(msg):
    r = requests.post(WEBHOOK, json={"content": msg})
    print("送信:", r.status_code)

# ★ 疑似ランキング生成（安定100%）
def generate_ranking():
    signs = [
        "おひつじ座","おうし座","ふたご座","かに座",
        "しし座","おとめ座","てんびん座","さそり座",
        "いて座","やぎ座","みずがめ座","うお座"
    ]

    random.shuffle(signs)

    ranking = {sign: i+1 for i, sign in enumerate(signs)}

    return ranking

def main():
    print("===== 起動確認 =====")

    today = datetime.date.today()

    ranking = generate_ranking()
    libra_rank = ranking["てんびん座"]

    msg = f"🔮 てんびん座の運勢（{today}）\n"
    msg += f"\n👉 今日の順位：{libra_rank}位 / 12位\n"

    # ★ コメントも付ける
    if libra_rank <= 3:
        msg += "✨ 絶好調！攻めてOK"
    elif libra_rank <= 6:
        msg += "👍 安定ゾーン"
    elif libra_rank <= 9:
        msg += "⚠️ 慎重に行動"
    else:
        msg += "💤 無理せず休む日"

    send(msg)

if __name__ == "__main__":
    main()
