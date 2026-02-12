import os, sys
sys.path.append(os.path.dirname(__file__))

from flask import Flask, render_template_string
from datetime import datetime, timezone, timedelta
import random

JST = timezone(timedelta(hours=9))  # ← import の「後」

app = Flask(__name__)

# 日本時間を取得 ---------------------------------
def get_current_hour():
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    return now.hour

# 時間帯判定--------------------------------------------------
def get_time_zone(hour):
    if 5 <= hour < 8:
        return "morning"
    elif 8 <= hour < 17:
        return "day"
    elif 17 <= hour < 19:
        return "evening"
    elif 19 <= hour < 23:
        return "night"
    else:
        return "late night"

# 表示テキスト------------------------------------------------
TIME_LABEL = {
    "morning": "前向きな朝になるように",
    "day": "笑顔でいられるように",
    "evening": "夕暮れ、帰り道",
    "night": "夜の静けさ",
    "late night": "眠れない夜に",
}

FOOTER_TEXT = {
    "morning": "今日が少しやさしく始まるように",
    "day": "焦らず、自分が頑張れる範囲で",
    "evening": "今日の終わりに、少しだけ",
    "night": "静かな音が、そっと寄り添うように",
    "late night": "眠れない夜のために",
}

# 色設定------------------------------------------------------
TEXT_COLOR_MAIN = {
    "morning": "#2f2f2f",
    "day": "#2f2f2f",
    "evening": "#2b2b2b",
    "night": "#ffffff",
    "late night": "#ffffff"
}

TEXT_COLOR_SUB = {
    "morning": "#555555",
    "day": "#555555",
    "evening": "#555555",
    "night": "#d0d3ff",
    "late night": "#c8ccff"
}

TEXT_COLOR_FAINT = {
    "morning": "#777777",
    "day": "#777777",
    "evening": "#777777",
    "night": "#cfd3ff",   # ← 明度を上げる
    "late night": "#d6d9ff",
}

BG_COLOR = {
    "morning": "#F2E6B8",
    "day": "#D6EEF9",
    "evening": "#FFD6C9",
    "night": "#1E1E3F",
    "late night": "#0B0B1A"
}

# 動画ID------------------------------------------------------
ALL_VIDEOS = {
    #最新曲---------------------------------------------------
    "-2FCAZLhh-Y",
    "ZQKAYcqIYzv",
    "uoYegcqyfxE",
    "8gcrKkXTx64",
    "Wiz0Ap2ge5U",
    "ZzBp3xUHvis",
    "VPK-lxmGyDk",
    "wW1UjAtAZ1A",
    "tHo25oDiNNY",
    "VS4yusNNKkQ",
    "TC80uw4HgCw",
    "Td9YlfLfXzM",
    "ZQKAYcqIYzv",
    "Mb_bFtcyg3E",
    "HhEJsD-ZOJU",
    "N5YD6SEVwKs",
    "iiPet5Z6vmg",
    "5ImdVATcfKs",
    "LKyLOLosp54",
    "ZQKAYcqIYzv",
    "-yRWO4ODgQQ",
    "ZQKAYcqIYzv",
    #天使の涙から----------------------------------------------------
    "mCYjEWWsqZ8",
    "qDV_zAf9T6g",
    "m-bvW4pKT68",
    "sU9GBNnoEmA",
    "ConmlXSnM0E",
    "HkTihNKCWFA",
    "dgkP8RQw-sQ",
    "7WXadfU7UOk",
    "9OiYX68L0BU",
    "Hvt59Q47M8k",
    "6f3GJ3uUc34",
    "Mb9TWJm_5L4",
    "qXvVt75kNmE",
    "bqyENYGSQzg",
    "q8Ap-1MUTew",
    "uUB2qgVBBjY",
    "ZiUwbmrMiAY",
    "p3Geomh2EuY",
    "lEoDjtCm488",
    "vAFoNaPZ5Pk",
    "rNZiCyCVIBQ",
    "xQYp4-Ett6A",
    "CHP7xCe8454",
    "Rpe5gphy3Dg",
    "tW6pTE_ENeo",
    "PAwZl3Up-hc",
    "FXNUn2KzcE8",
    "NihQBHOZLIw",
    "xgNeFTCzpgo",
    "YXCBQDK4DlE",
    "zQqIm-EVlkQ",
    "ArqagB9P1Qs",
    "SrdCXBZs4j8",
    "cGGlBYzZiJs",
    "ioW9iGDpQyw",
    "hupkoU8e1is",
    "f6TytcA47rI",
    "UZTcXWLf2Ek",
    "filTeBL7mA0",
    "o2CD3DjPHmU",
    "340OXvocRMM",
    "M50V-UBjqcI",
    "eurJC5ElRPE",
    "7xht3kQO_TM",
    "HyQK7IssB9M",
    "sVqtVjtRcN8",
    "_eBe5rD73Eg",
    "S2AhFrGXa8I",
    "vULemZ6DhM8",
    "1gSMjPLRJik",
    "XiKZE967BD4",
    "sFoWYa6QNKk",
    "yIo2ePCm4bY",
    "exo3XdtPrgs",
    "tI4nhL7qQdk",
    "vLigCJOcHOE",
    "PJrjwIlWVXA",
    "P_DgrvZmXM0",
    "06YWg6Y1kxo",
    "r5xaccIl1Ps",
    "Ou8sl4s3NJg",
    "Ziz_ckzVjyA",
    "Txh4DZmcbPk",
    "ZTFQs7MspEI",
    "UGzd2dnkhME",
    "89p7DWIqOu8",
    "pcRaY5kq4YY",
    "Q5XzviXSHQ4",
    "EGJR43xgFgQ",
    "fztKqreP1pk",
    "qtuX4cHk-vE",
    "rzamOqbbBfQ",
    "QJaY60vjSxw",
    "w4fxj1toPzc",
    "AfteRl4ePBc",
    "lnfYoNLrMJE",
    "qivTJhNbqUc",
    "SBlkzGiM5uE",
    # 全曲リスト
    

}
# HTML--------------------------------------------------------
HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>MIMI Time</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500&display=swap" rel="stylesheet">


<style>
body {
    margin: 0;
    background-color: {{ bg }};
    font-family: 'Zen Maru Gothic', sans-serif;
    transition: background-color 1.5s;
    text-align: center;
}

/* 公式サイト + 利用上の注意 を横並びにする */
.credit-links {
    display: flex;
    gap: 10px;              /* ボタン同士の間隔 */
    justify-content: center;
    align-items: center;
    margin-top: 16px;
    margin-bottom: 42px;
    flex-wrap: wrap;        /* スマホで潰れたら縦に落ちる */
}

/* ===== 利用上の注意リンク ================================- */
/* 利用上の注意（公式リンク横・同サイズ） */
.about-link a {
    display: inline-block;
    padding: 10px 18px;        /* ← 公式リンクと同じ */
    font-size: 0.95em;         /* ← 公式リンクと同じ */
    font-weight: 500;
    border-radius: 999px;

    background: rgba(0, 0, 0, 0.05);
    color: inherit;
    text-decoration: none;

    transition: background 0.2s ease, transform 0.15s ease;
}

/* 夜 */
body.night .about-link a,
body.late .about-link a {
    background: rgba(255, 255, 255, 0.08);
}

.about-link a:hover,
.about-link a:active {
    transform: translateY(-1px);
    background: rgba(0, 0, 0, 0.12);
}

/* ===== ここまで ====================================================== */

.container {
    max-width: 560px;
    margin: 0 auto;

    /* 上 / 左右 / 下（safe-area対応） */
    padding: 96px 16px calc(96px + env(safe-area-inset-bottom));

    box-sizing: border-box;
}

.subtitle {
    margin-top: 4px;      /* 「眠れない夜に」との間：ほんの少し */
    margin-bottom: 12px;  /* 時間表示との間 */
    font-size: 0.85em;
    opacity: 0.65;
    color: {{ text_faint }};
}

h1 {
    margin: 0 0 8px;
    color: {{ text_main }};
}

/* ← ここに追加 */
.subtitle {
    margin-top: 2px;        /* 「眠れない夜に」と少しだけ離す */
    margin-bottom: 6px;     /* 時間表示とは詰め気味に */
    font-size: 0.85em;
    opacity: 0.65;
    color: {{ text_faint }};
}

p {
    margin: 6px 0;
    color: {{ text_sub }};
}

.time {
    color: {{ text_faint }};
}

.video-wrap {
    margin-top: 24px;
}

.video-wrap iframe {
    width: 100%;
    aspect-ratio: 16 / 9;
    border-radius: 12px;
    border: none;
}

.footer-text {
    margin-top: 12apx;
    color: {{ text_faint }};
}

.credit {
    margin-top: 8px;
    font-size: 0.8em;
    opacity: 0.45;
}

.credit a {
    color: {{ text_faint }};
    text-decoration: none;
}

@media (max-width: 600px) {
    .container {
        padding-top: 64px;
    }
    h1 {
        font-size: 1.9em;
    }
}

/* クレジット文字色：昼 */
body.morning .credit,
body.day .credit,
body.evening .credit {
    color: #333333;          /* やさしい黒 */
}

/* クレジット文字色：夜 */
body.night .credit,
body.late .credit {
    color: rgba(255, 255, 255, 0.75);  /* 薄い白 */
}

.credit a {
    color: inherit;
}

/* 公式サイト誘導リンク */
.official-link {
    margin-top: 18px;          /* ← 少し離す */
}

.official-link a {
    display: inline-block;
    padding: 10px 18px;
    font-size: 0.95em;         /* 少し大きめ */
    font-weight: 500;
    border-radius: 999px;      /* やさしい丸 */
    text-decoration: none;
    transition: all 0.2s ease;
}

/* 昼・夕 */
body.morning .official-link a,
body.day .official-link a,
body.evening .official-link a {
    color: #333;
    background: rgba(0, 0, 0, 0.05);
}

/* 夜・深夜 */
body.night .official-link a,
body.late .official-link a {
    color: rgba(255, 255, 255, 0.9);
    background: rgba(255, 255, 255, 0.08);
}

/* ホバー時（PC用） */
.official-link a:hover {
    transform: translateY(-1px);
    opacity: 0.9;
}

/* === 高さを完全に揃える上書き === */
.official-link a,
.about-link a {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 44px;
    padding: 0 18px;
    line-height: 1;
    box-sizing: border-box;
}

</style>
</head>

<body class="{{ zone }}">

<div class="container">

<h1>{{ label }}</h1>

<p class="subtitle">MIMIさんの曲に、ふと出会うための場所</p>


<p>現在の時間帯：{{ zone }}</p>

<p class="time">
    現在時刻：<span id="clock">{{ time }}</span>
</p>


{% if video_id %}
<div class="video-wrap">
    <iframe src="https://www.youtube.com/embed/{{ video_id }}" allowfullscreen></iframe>
</div>
{% endif %}

{% if footer %}
<div class="footer-text">{{ footer }}</div>
{% endif %}

</div>


<div class="credit">
    <div class="credit-note">
        このサイトはMIMIさんの非公式ファンサイトです。<br>
        (ご利用時の注意点は下部にあります)<br>
        詳細情報は公式サイトをご確認ください。<br>
        動画は、YouTube公式の埋め込み機能を使用しています。
    </div>
<div class="credit-links">
    <div class="official-link">
        <a href="https://www.youtube.com/@MIMI...official" target="_blank">
            ▶ MIMIさんの公式サイトはこちら
        </a>
    </div>
    
    <div class="about-link">
        <a href="/about">
            ご利用時の注意点
        </a>
    </div>
</div>
</div>

<script>
function updateClock() {
    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    document.getElementById("clock").textContent = h + ":" + m;
}
updateClock();
setInterval(updateClock, 60000);
</script>

</body>
</html>
"""

ABOUT_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>ご利用時の注意点</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500&display=swap" rel="stylesheet">
<style>
body {
    margin: 0;
    font-family: 'Zen Maru Gothic', sans-serif;
    background: #1e1e3f;
    color: #e6e8ff;
}
.container {
    max-width: 640px;
    margin: 0 auto;
    padding: 64px 20px;
}
h1 {
    text-align: center;
    margin-bottom: 32px;
}
p {
    line-height: 1.8;
    margin-bottom: 16px;
}
a {
    color: #cfd3ff;
    text-decoration: none;
}
.back {
    text-align: center;
    margin-top: 32px;
}
</style>
</head>

<body>
<div class="container">
<h1>ご利用時の注意点</h1>

<p>
このサイトは、ボカロP「MIMI」(@mimi_3mi)さんの楽曲をきっかけに、  
時間帯の雰囲気に合わせた背景とともに、ランダムで選曲される音楽と出会う体験を目的として制作した、  
非公式のファンサイトです。
</p>

<p>
本サイトは、MIMIさんの作品に影響を受けて制作したものです。
</p>

<p>
掲載している動画は、YouTube公式の埋め込み機能を利用しています。  
動画の著作権は各権利者様に帰属します。
</p>

<p>
本サイトは営利目的ではありません。  
万が一問題等がございましたら、速やかに対応いたします。
</p>

<p>
何かございましたらX(旧Twitter)のDMまでご連絡ください。
</p>

<p>
                                     作成者　ゆーさぶ
</p>
<div class="back">
    <a href="/">← トップページに戻る</a>
</div>
</div>
</body>
</html>
"""



@app.route("/")
def index():
    hour = get_current_hour()
    zone = get_time_zone(hour)

    now = datetime.now(JST)  # ← ここで使える

    return render_template_string(
        HTML,
        label=TIME_LABEL[zone],
        zone=zone,
        time=now.strftime("%H:%M"),
        bg=BG_COLOR[zone],
        footer=FOOTER_TEXT[zone],
        video_id=random.choice(list(ALL_VIDEOS)),
        text_main=TEXT_COLOR_MAIN[zone],
        text_sub=TEXT_COLOR_SUB[zone],
        text_faint=TEXT_COLOR_FAINT[zone],
    )
# about接続用--------------------------------------------------
@app.route("/about")
def about():
    return render_template_string(ABOUT_HTML)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
