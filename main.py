def get_fortune():
    try:
        url = "https://aztro.sameerkumar.website/?sign=libra&day=today"

        res = requests.post(url, headers=HEADERS, timeout=10)

        print("status:", res.status_code)
        print("body:", res.text[:100])

        if res.status_code != 200:
            return None

        try:
            data = res.json()
        except:
            print("JSON変換失敗:", res.text[:200])
            return None

        return f"""【てんびん座 今日の運勢】

■ 総合運：
{data.get('description','')}

■ ラッキーナンバー：{data.get('lucky_number','')}
■ ラッキーカラー：{data.get('color','')}
"""
    except Exception as e:
        print("API失敗:", e)
        return None
