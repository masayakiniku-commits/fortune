def get_fortune():
    try:
        url = "https://uranai.nosv.org/u.php/honbun/12seiza/"

        res = requests.get(url, headers=HEADERS, timeout=10)

        print("status:", res.status_code)

        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()

        if "てんびん座" not in text:
            return None

        # 範囲を広めに取る（ここがポイント）
        start = text.find("てんびん座")
        raw = text[start:start+500]

        # 整形（ここで完成度決まる）
        lines = []
        for line in raw.splitlines():
            line = line.strip()
            if line and "順位" not in line:
                lines.append(line)

        result = "\n".join(lines[:8])  # 長すぎ防止

        return f"""【てんびん座 今日の運勢】

{result}
"""

    except Exception as e:
        print("取得失敗:", e)
        return None
