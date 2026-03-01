import os, sys
sys.path.append(os.path.dirname(__file__))

from flask import Flask, render_template_string, request, session
import secrets
from datetime import datetime, timezone, timedelta
import random

JST = timezone(timedelta(hours=9))

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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
    "morning": "前向きな朝に",
    "day": "穏やかな日常に",
    "evening": "夕暮れ、帰り道",
    "night": "夜の音をひとつ",
    "late night": "眠れない夜に",
}

FOOTER_TEXT = {
    "morning": "今日が少しやさしく始まるように",
    "day": "無理のない歩幅で",
    "evening": "今日の終わりに、少しだけ",
    "night": "そっと寄り添えるように",
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
    "night": "#cfd3ff",
    "late night": "#d6d9ff",
}

BG_COLOR = {
    "morning": "#E3ECFF",
    "day": "#D6EEF9",
    "evening": "#FFD6C9",
    "night": "#1E1E3F",
    "late night": "#0B0B1A"
}

# 動画ID------------------------------------------------------
ALL_VIDEOS = [
    #最新曲---------------------------------------------------
    "IxVFW1XIW7Q",
    "-2FCAZLhh-Y",
    "iUXrTnEeqRw",
    "uoYegcqyfxE",
    "8gcrKkXTx64",
    "Wiz0Ap2ge5U",
    "ZzBp3xUHvis",
    "VPK-lxmGyDk",
    "wW1UjAtAZ1A",
    "tHo25oDiNNY",
    "TC80uw4HgCw",
    "Td9YlfLfXzM",
    "5uHtY6DpRi4",
    "Mb_bFtcyg3E",
    "HhEJsD-ZOJU",
    "NNgCHHgJ2W8", #Session
    "N5YD6SEVwKs",
    "iiPet5Z6vmg",
    "5ImdVATcfKs",
    "LKyLOLosp54",
    "-yRWO4ODgQQ",
    "5hgSET4bpbk",
    "mCYjEWWsqZ8",
    "qDV_zAf9T6g",
    "m-bvW4pKT68",
    "sU9GBNnoEmA",
    "ConmlXSnM0E",
    "HkTihNKCWFA",
    "JE_GFOk90oU", #Session
    "dgkP8RQw-sQ",
    "7WXadfU7UOk",
    "9OiYX68L0BU",
    "Hvt59Q47M8k",
    "6f3GJ3uUc34",
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
    "qtuX4cHk-vE",
    "rzamOqbbBfQ",
    "QJaY60vjSxw",
    "w4fxj1toPzc",
    "AfteRl4ePBc",
    "lnfYoNLrMJE",
    "qivTJhNbqUc",
    "SBlkzGiM5uE",
    # 全曲リスト
    

]

#移動中表示-------------------------------------------

LOADING_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="1.2;url=/main">
<title>MIMI Time</title>

<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500&display=swap" rel="stylesheet">

<style>
body {
    margin: 0;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;

    background: radial-gradient(circle at center, #1a1a3a, #0B0B1A);
    font-family: 'Zen Maru Gothic', sans-serif;
}

.loading {
    font-size: 2.2rem;
    font-weight: 500;
    color: rgba(255,255,255,0.9);

    opacity: 0;
    animation: fadeIn 0.8s ease forwards;
}

.dots {
    display: inline-block;
    animation: blink 1.2s infinite;
}

/* フェードイン */
@keyframes fadeIn {
    to { opacity: 1; }
}

/* ・・・点滅 */
@keyframes blink {
    0% { opacity: 0.3; }
    50% { opacity: 1; }
    100% { opacity: 0.3; }
}
</style>
</head>

<body>
<div class="loading">
    MIMI Timeへ移動中<span class="dots">...</span>
</div>
</body>
</html>
"""

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

/* --------設定ボタン-------- */
#settingsBtn {
    position: absolute;
    top: 22px;
    right: 24px;

    padding: 5px 14px;
    border-radius: 999px;

    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.25);

    color: white;
    font-size: 12px;
    letter-spacing: 1px;

    backdrop-filter: blur(6px);
    cursor: pointer;
    z-index: 1000;
    transition: all 0.2s ease;
}

#settingsBtn:hover {
    background: rgba(0,0,0,0.5);
}

/* -------- 設定パネル------- */
#settingsPanel {
    position: fixed;
    top: 22px;
    right: 24px;
    background: none;
    color: white;
    padding: 15px;
    border-radius: 12px;
    display: none;
    width: 230px;
    font-size: 14px;
    z-index: 1000;
}

body {
    margin: 0;
    background-color: {{ bg }};
    font-family: 'Zen Maru Gothic', sans-serif;
    transition: background-color 1.5s;
    text-align: center;
}

/* 公式サイトと利用系の位置*/
.credit-links {
    display: flex;
    gap: 10px;
    justify-content: center;
    align-items: center;
    margin-top: 16px;
    margin-bottom: 42px;
    flex-wrap: wrap;
}

/*-------------------- 利用上の注意リンク ---------------------------- */
/* 利用上の注意 */
.about-link a {
    display: inline-block;
    padding: 10px 18px;
    font-size: 0.95em;
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

/*------------------------------------------------------- */

.container {
    max-width: 560px;
    margin: 0 auto;

    /* safe-area */
    padding: 96px 16px calc(96px + env(safe-area-inset-bottom));

    box-sizing: border-box;
}

.subtitle {
    margin-top: 4px;
    margin-bottom: 12px;
    font-size: 0.85em;
    opacity: 0.65;
    color: {{ text_faint }};
}

h1 {
    margin: 0 0 8px;
    color: {{ text_main }};
}

/* 追加 */
.subtitle {
    margin-top: 2px;
    margin-bottom: 6px;
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

/* クレジット文字色・昼 */
body.morning .credit,
body.day .credit,
body.evening .credit {
    color: #333333;
}

/*------------------------------朝　全体文字色------------------------------------------*/
body.morning {
    color: #1F2538;
}

/* クレジット文字色・夜 */
body.night .credit,
body.late .credit {
    color: rgba(255, 255, 255, 0.75);
}

.credit a {
    color: inherit;
}

/* 公式サイトリンク */
.official-link {
    margin-top: 18px;
}

.official-link a {
    display: inline-block;
    padding: 10px 18px;
    font-size: 0.95em;
    font-weight: 500;
    border-radius: 999px;
    text-decoration: none;
    transition: all 0.2s ease;
}

/* 昼、夕 */
body.morning .official-link a,
body.day .official-link a,
body.evening .official-link a {
    color: #333;
    background: rgba(0, 0, 0, 0.05);
}

/* 夜、深夜 */
body.night .official-link a,
body.late .official-link a {
    color: rgba(255, 255, 255, 0.9);
    background: rgba(255, 255, 255, 0.08);
}

/* PC用 */
.official-link a:hover {
    transform: translateY(-1px);
    opacity: 0.9;
}

/* --------- 高さをそろえる ------- */
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

/* ----------- 再リロード用 --------------------------------------------------- */
.main-btn {
    appearance: none;
    -webkit-appearance: none;

    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.05);

    color: rgba(255,255,255,0.85);
    padding: 5px 16px;
    font-size: 13px;

    cursor: pointer;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);

    transition: all 0.3s ease;
    
    margin-top: 6px;
    margin-bottom: 4px;
}

.main-btn:hover {
    background: rgba(255,255,255,0.12);
}

.main-btn:hover {
    background: rgba(255,255,255,0.25);
    transform: translateY(-2px);
}
/*-----------------------リロード----------------------------------------------*/


/*  朝、昼、夕 */
body.morning .main-btn,
body.day .main-btn,
body.evening .main-btn {
    background: rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.15);
    color: #2E2E3A;
}

/*  夜、深夜 */
body.night .main-btn,
body.late-night .main-btn {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.4);
    color: #ffffff;
}

/* 背景を暗く */
#overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(4px);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 2000;
}

/* 設定 */
#settingsModal {
    text-aglign: left;
    background: rgba(30, 30, 60, 0.85);
    color: white;
    padding: 24px 28px;
    border-radius: 18px;
    width: 260px;
    max-width: 80%;
    
    max-height: 80vh;
    overflow-y: auto;
    
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}


.license-text a {
  color: #e6c77a;
  text-decoration: underline;
  font-weight: 500;
}

.license-text a:hover {
  opacity: 0.8;
}

#settingsModal {
  text-align: left;
}

#settingsModal h2 {
  text-align: center;
}

#settingsModal label {
  display: block;
  text-align: center;
}

#settingsModal details {
  text-align: left;
}

#settingsModal summary {
  text-align: left;
}

#closeSettings {
  display: block;
  margin: 20px auto 0;
}

/* ホバー */
#settingsBtn:hover {
    background: rgba(255,255,255,0.18);
    border-color: white;
}

/* 押した時 */
#settingsBtn:active {
    transform: scale(0.95);
}

/* 閉じるボタン */
#closeSettings {
    background: none;
    border: 1px solid rgba(255,255,255,0.4);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    cursor: pointer;
}
/*更新*/
.update-list {
  text-align: left;
  }
  
/*ライセンス*/
.license-section {
  margin-top: 10px;
}
/*ライセンステキスト*/
.license-text {
  text-align: left;
  font-size: 13px;
  line-height: 1.6;
  opacity: 0.85;
}
/*タブ揃え*/
details {
  margin: 0;
  padding: 0;
}

summary::before {
  content: "▶";
}
details[open] summary::before {
  content: "▼";
}


summary {
  margin: 0;
  padding-left: 0;
  list-style: none;
}

</style>
</head>



<body class="{{ zone }}">

<button id="settingsBtn">設定</button>

<div id="overlay">
    <div id="settingsModal">
        <h2>設定</h2>

        <label>
            <input type="checkbox" id="noRepeatToggle">
            さらにランダムにする
        </label>

<hr>

<details class="update-section">
  <summary>更新履歴</summary>

  <!-- 直近の更新履歴 -->
  <div class="update-list">
    26.3.1 更新状況タブを追加<br>
    26.3.1 文字色の修正<br>
    26.3.1 更新履歴タブの修正<br>
  </div>

  <!-- 古い履歴 -->
  <details>
    <summary>過去の更新を見る</summary>
    <div class="update-list">
      26.3.1 （設定）直近ランダム修正<br>
      26.3.1 外部リンクセキュリティ対策<br>
      26.3.1 ライセンス表記追加<br>
      26.3.1 設定欄追加<br>
      26.3.1 設定項目追加<br>
    </div>
  </details>

</details>

<details class="status-section">
  <summary>更新状況</summary>
  <div class="update-list">
    現時点での更新はありません<br>
  </div>
</details>

<details class="license-section">
  <summary>ライセンス</summary>

  <div class="license-text">
    © 2026 yu-sabu<br>
    本サイトのコードは、個人利用および非商用利用に限り使用を許可します。<br>
    商用利用は禁止します。<br>
    記載している動画はYouTube公式の埋め込み機能を使用しています。<br>
    各動画の著作権はそれぞれの権利者様に帰属します。<br><br>
    Music and artwork belong to their respective owners.<br><br>
    ソースコードはGitHubで公開しています。<br>
    Source code is available on GitHub.<br>
<a href="https://github.com/MIMI-time-dev/MIMI-Time" target="_blank" rel="noopener noreferrer">GitHubへ移動</a><br>

  </div>
  
</details>
        <br><br>
        <button id="closeSettings">閉じる</button>
    </div>
</div>

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

<button class="main-btn" onclick="reloadWithOption()">
    もう一曲と出会う
</button>


{% if footer %}
<div class="footer-text">{{ footer }}</div>
{% endif %}

</div>


<div class="credit">
    <div class="credit-note">
        このサイトはMIMIさんの非公式ファンサイトです。<br>
        動画は、YouTube公式の埋め込み機能を使用しています。<br>
        詳細は公式サイトをご確認ください。
    </div>
<div class="credit-links">
    <div class="official-link">
        <a href="https://www.youtube.com/@MIMI...official" target="_blank">
            ▶ MIMIさんの公式サイトはこちら
        </a>
    </div>
    
    <div class="about-link">
        <a href="/about">
            ご利用時の注意と説明
        </a>
    </div>
</div>

<div class="footer-license">
  © 2026 yu-sabu<br><br>
  <span>  
    For personal, non-commercial use only.
    Music and artwork belong to their respective owners.
   </span>
  
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

function reloadWithOption() {
    const checked = document.getElementById("noRepeatToggle").checked;

    if (checked) {
        window.location.href = "/main?no_repeat=true";
    } else {
        window.location.href = "/main";
    }
}

// URLから復元
if (window.location.search.includes("no_repeat=true")) {
    document.getElementById("noRepeatToggle").checked = true;
}

const noRepeatToggle = document.getElementById("noRepeatToggle");

// 保存されていた場合復元
if (localStorage.getItem("noRepeat") === "true") {
    noRepeatToggle.checked = true;
}

// チェック変更時保存
noRepeatToggle.addEventListener("change", () => {
    localStorage.setItem("noRepeat", noRepeatToggle.checked);
});

const settingsBtn = document.getElementById("settingsBtn");
const overlay = document.getElementById("overlay");
const closeSettings = document.getElementById("closeSettings");

settingsBtn.addEventListener("click", () => {
    overlay.style.display = "flex";
    document.body.style.overflow = "hidden";
});

closeSettings.addEventListener("click", () => {
    overlay.style.display = "none";
    document.body.style.overflow = "";
});

overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
        overlay.style.display = "none";
        document.body.style.overflow = "";
    }
});



</script>

</body>
</html>
"""

ABOUT_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>ご利用時の注意と説明</title>
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

.back {
  text-align: center;
  margin-top: 32px;
}

/* ライセンス表記 */
.footer-license {
  padding-bottom: 30px;
  font-size: 12px;
  opacity: 0.6;
  line-height: 1.6;
}

body {
    padding-botom: 80px;
}
</style>
</head>

<body>
<div class="container">
<h1>ご利用時の注意と説明</h1>

<p>
このサイトは、ボカロP「MIMI」(@mimi_3mi)さんの楽曲をきっかけに、  
時間帯の雰囲気に合わせた背景とともに、ランダムで選曲される音楽と出会う体験を目的として制作した、  
非公式のファンサイトです。
</p>

<p>
掲載している動画は、YouTube公式の埋め込み機能を利用しています。  
</p>

<p>本サイトは非営利目的で運営しています。</p>
<p>万が一問題等がございましたら、可能な限り対応いたします。</p>

<p>
何かございましたら、X(旧Twitter)のDMから教えていただけると嬉しいです。
</p>

<p>
                                     作成者　ゆーさぶ
</p>
<div class="back">
    <a href="/">← トップページに戻る</a>
</div>
</body>
</html>
"""



@app.route("/")
def loading():
    return render_template_string(LOADING_HTML)

@app.route("/main")

#@app.route("/")
def index():

    hour = get_current_hour()
    zone = get_time_zone(hour)
    now = datetime.now(JST)

    no_repeat = request.args.get("no_repeat") == "true"
    video_id = get_random_video(no_repeat)

    return render_template_string(
        HTML,
        label=TIME_LABEL[zone],
        zone=zone,
        time=now.strftime("%H:%M"),
        bg=BG_COLOR[zone],
        footer=FOOTER_TEXT[zone],
        video_id=video_id,
        text_main=TEXT_COLOR_MAIN[zone],
        text_sub=TEXT_COLOR_SUB[zone],
        text_faint=TEXT_COLOR_FAINT[zone],
    )

def get_random_video(no_repeat=False):

    history = session.get("history", [])

    if no_repeat:
        # 直近5曲を除外
        candidates = [v for v in ALL_VIDEOS if v not in history]

        # すべて使うとリセット
        if not candidates:
            history = []
            candidates = ALL_VIDEOS
    else:
        candidates = ALL_VIDEOS

    selected = random.choice(candidates)

    # 履歴に追加
    history.append(selected)

    # 直近5曲のみ保持
    history = history[-5:]

    session["history"] = history

    return selected

# about接続用--------------------------------------------------
@app.route("/about")
def about():
    return render_template_string(ABOUT_HTML)

@app.errorhandler(404)
def not_found(e):
    return "ページが見つかりません。", 404

@app.errorhandler(500)
def server_error(e):
    return "サーバーでエラーが発生しました。", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)