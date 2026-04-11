print("★★★絶対ここ通る★★★")
def get_fortune():
    try:
        url = "https://uranai.nosv.org/u.php/honbun/12seiza/"

        res = requests.get(url, headers=HEADERS, timeout=10)

        print("status:", res.status_code)

        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()

        # デバッグ用
        print(text[:500])

        # 「てんびん」「天秤」どっちでも拾う
        keywords = ["てんびん座", "天秤座"]

        start = -1
        for k in keywords:
            if k in text:
                start = text.find(k)
                break

        if start == -1:
            return None

        raw = text[start:start+500]

        lines = []
        for line in raw.splitlines():
            line = line.strip()
            if line and "順位" not in line:
                lines.append(line)

        result = "\n".join(lines[:8])

        return f"""【てんびん座 今日の運勢】

{result}
"""

    except Exception as e:
        print("取得失敗:", e)
        return None
