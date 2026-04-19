import os, sys
sys.path.append(os.path.dirname(__file__))

from flask import Flask, render_template_string, request, session
import secrets
from datetime import datetime, timezone, timedelta
import random
import requests

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
    #1,アルバム収録曲
    "spoQeZea7s8",
    "56Na2tuPOXs",
    "VRhZgfFOvZQ",
    "w3S9o1kSpqE",
    "5Zz_00sjwW0",
    #2,アルバム収録曲（現時点での）
    "RO6Z16icc8c",
    #最新曲---------------------------------------------------
    "x0APPrPgexY",
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

#ID確認用
# for i in ALL_VIDEOS:
#     print(f"https://www.youtube.com/watch?v={ i }")


# メイン用タイトル辞書------------------------------------------
VIDEO_TITLES = {
    #1,アルバム収録曲
    "spoQeZea7s8":"淡さと微睡む",
    "56Na2tuPOXs":"れじぇろ",
    "VRhZgfFOvZQ":"アンダー",
    "w3S9o1kSpqE":"水流音楽",
    "5Zz_00sjwW0":"いいじゃない",
    #2,アルバム収録曲（現時点での）
    "RO6Z16icc8c":"大丈夫だよ。 (feat. 可不)",
    #最新曲---------------------------------------------------
    "x0APPrPgexY":"『月夜』/ MIMI feat. 宵 (Music Video)",
    "IxVFW1XIW7Q":"『花びら哀歌』/ feat. 重音テトSV",
    "-2FCAZLhh-Y":"『 柔く、ほどいて 』 / feat.初音ミク＆重音テトSV",
    "iUXrTnEeqRw":"『それでも優しかった君へ』/ MIMI feat.沖石",
    "uoYegcqyfxE":"『トリックハート』 / feat.重音テトSV",
    "8gcrKkXTx64":"『声の欠片』/ MIMI feat. 月",
    "Wiz0Ap2ge5U":"『星涙哀歌』/ MIMI feat. 初音ミク",
    "ZzBp3xUHvis":"『凪と藍空』 / MIMI feat. マス",
    "VPK-lxmGyDk":"『 愛されたいって願ってる 』/ MIMI feat. 可不",
    "wW1UjAtAZ1A":"『痛いの痛いの飛んでいけっ』 / MIMI feat. saewool (Music Video)",
    "tHo25oDiNNY":"『海辺の電話ボックス』/ feat. 音街ウナSV",
    "TC80uw4HgCw":"『マジック・メイド』 / feat.重音テトSV",
    "Td9YlfLfXzM":"『 愛してランデブー 』/ feat. 初音ミク",
    "5uHtY6DpRi4":"『余熱 』/ feat. 初音ミク",
    "Mb_bFtcyg3E":"『もしも』 / MIMI feat. マス",
    "HhEJsD-ZOJU":"『ラベンダー』 / MIMI feat. saewool (Music Video)",
    "NNgCHHgJ2W8":"MIMI 2AM. Study Session", #Session
    "N5YD6SEVwKs":"『シャボン』/ feat.初音ミク",
    "iiPet5Z6vmg":"『恋しくなったら手を叩こう』/ MIMI feat.花鏡紅璃",
    "5ImdVATcfKs":"『恋しくなったら手を叩こう』 / feat.重音テトSV",
    "LKyLOLosp54":"『お砂糖哀歌』 / feat. 初音ミク",
    "-yRWO4ODgQQ":"『夜と幸せ』/MIMI feat. 詩の出素。 (Music Video)",
    "5hgSET4bpbk":"『アンコールダンス』/ feat. 重音テトSV",
    "mCYjEWWsqZ8":"『天使の涙』 / feat.初音ミク",
    "qDV_zAf9T6g":"『ソルティメロウ』 / feat. 可不",
    "m-bvW4pKT68":"MIMI - サイエンス (feat.重音テトSV)",
    "sU9GBNnoEmA":"『星恋歌 』/ MIMI feat.しょうゆ",
    "ConmlXSnM0E":"『星恋歌 』/ feat. 初音ミク",
    "HkTihNKCWFA":"『劣等哀歌』 / feat. 初音ミク＆重音テトSV",
    "JE_GFOk90oU":"MIMI 1AM. Study Session", #Session
    "dgkP8RQw-sQ":"『茜の鼓動 』/ feat. 初音ミク",
    "7WXadfU7UOk":"『夜風に吹かれて口笛を』/ MIMI feat. 花鏡紅璃",
    "9OiYX68L0BU":"『To U』 / feat. 初音ミク",
    "Hvt59Q47M8k":"『消えない温度』 / feat. 可不",
    "6f3GJ3uUc34":"『音の灯火』 / feat.詩の出素。",
    "qXvVt75kNmE":"微熱のリリック / feat. 重音テトSV",
    "bqyENYGSQzg":"『すろーりーないと』 / feat. 初音ミク",
    "q8Ap-1MUTew":"『わたしまだBABY』 / feat. 狐子",
    "uUB2qgVBBjY":"UNFADING / feat. 初音ミク",
    "ZiUwbmrMiAY":"『解答』 / MIMI feat.わん子",
    "p3Geomh2EuY":"『 ツキミチシルベ 』 / feat. 初音ミク ＆ 可不",
    "lEoDjtCm488":"『触れていたいだけ』/ MIMI feat. 月 (Music Video)",
    "vAFoNaPZ5Pk":"『ありあ』 / feat. 可不",
    "rNZiCyCVIBQ":"『頂戴な』/ MIMI feat. 沖石",
    "xQYp4-Ett6A":"『愛し愛』 / feat. 初音ミク ・ 可不",
    "CHP7xCe8454":"『 それで充分だよ。』/ feat. 可不",
    "Rpe5gphy3Dg":"『Lilly 』/ MIMI",
    "tW6pTE_ENeo":"『始点前夕暮れ』 / feat. 初音ミク",
    "PAwZl3Up-hc":"『 はぐ 』 / 初音ミク・可不",
    "FXNUn2KzcE8":"『心を刺す言葉だけ』/ feat. 初音ミク＆可不",
    "NihQBHOZLIw":"『 Maple 』/ feat. 羽累",
    "xgNeFTCzpgo":"『フィオーレ 』/ feat. 初音ミク＆可不",
    "YXCBQDK4DlE":"『Without Knowing』 / MIMI feat. アカラカイ",
    "zQqIm-EVlkQ":"『コウフク貯金』 / feat. 初音ミク",
    "ArqagB9P1Qs":"『息をするだけ』/ feat. 可不",
    "SrdCXBZs4j8":"『What Call This Day ? 』/ MIMI feat. にんじん (from ロクデナシ)",
    "cGGlBYzZiJs":"『サヨナラは言わないでさ 』/ feat. 可不",
    "ioW9iGDpQyw":"『妄想哀歌』/ feat. 初音ミク＆可不",
    "hupkoU8e1is":"『 わたしマニュアル (Original Arrange Ver.) 』/ MIMI feat. 可不",
    "f6TytcA47rI":"『くうになる』 / feat. 初音ミク ＆ 可不",
    "UZTcXWLf2Ek":"『GLACIES』/ MIMI feat. 初音ミク",
    "filTeBL7mA0":"『ロココ 』/ feat. 初音ミク",
    "o2CD3DjPHmU":"『オマジナイ』 ( long ver. ) / 可不",
    "340OXvocRMM":"『 今はいいんだよ。』/ feat. 可不",
    "M50V-UBjqcI":"『 夜のあいろに 』/ feat. 初音ミク",
    "eurJC5ElRPE":"『 ポシェット 』/ feat. 可不",
    "7xht3kQO_TM":"『 ハナタバ 』/ MIMI feat. 可不",
    "HyQK7IssB9M":"『 愛するように 』/ feat. 可不",
    "sVqtVjtRcN8":"『ぽけっと・愛の歌』/ feat. 裏命",
    "_eBe5rD73Eg":"『 あのね 』/ feat. 可不",
    "S2AhFrGXa8I":"『みにまむ』/ MIMI feat. わん子",
    "vULemZ6DhM8":"『風鈴歌』 / feat. 初音ミク",
    "1gSMjPLRJik":"『ヒミツ 』/ feat. 可不",
    "XiKZE967BD4":"『えすけーぷ』/ feat. 星界",
    "sFoWYa6QNKk":"『ぎゅって』/ feat. 初音ミク",
    "yIo2ePCm4bY":"『 だきしめるまで。』/ feat. 可不",
    "exo3XdtPrgs":"『もーいいかい』/ feat. 初音ミク",
    "tI4nhL7qQdk":"『LyriC』 / MIMI",
    "vLigCJOcHOE":"『いっせーのーで』/ feat. 可不",
    "PJrjwIlWVXA":"『よるつむぎ』/ feat. 初音ミク",
    "P_DgrvZmXM0":"『もでらーと 』/ MIMI feat. わん子",
    "06YWg6Y1kxo":"MIMI『 Pale 』feat. 初音ミク",
    "r5xaccIl1Ps":"SorrowChat / feat. 初音ミク",
    "Ou8sl4s3NJg":"ゆめまぼろし / feat. 初音ミク",
    "Ziz_ckzVjyA":"MIMI『ルルージュ』feat.初音ミク",
    "Txh4DZmcbPk":"そして夜と灯る / feat.初音ミク",
    "ZTFQs7MspEI":"Cold Waltz - in G Minor MIMI",
    "UGzd2dnkhME":"夜明け前に飛び乗って / feat. 初音ミク",
    "89p7DWIqOu8":"カラバコにアイ / feat.初音ミク",
    "pcRaY5kq4YY":"静寂に咲く / feat.初音ミク",
    "Q5XzviXSHQ4":"何もない様な / feat.初音ミク",
    "qtuX4cHk-vE":"マシュマリー / feat.初音ミク",
    "rzamOqbbBfQ":"モーメント / feat.初音ミク",
    "QJaY60vjSxw":"【初音ミク】 水音とカーテン 【オリジナル曲】",
    "w4fxj1toPzc":"【オリジナル曲】「NOREEN」",
    "AfteRl4ePBc":"【初音ミク】 ミライリフレクト　【オリジナル曲】",
    "lnfYoNLrMJE":"【初音ミク】parabola【オリジナル曲】",
    "qivTJhNbqUc":"【初音ミク】　透明夏　【オリジナル曲】",
    "SBlkzGiM5uE":"【初音ミク】「ラピスラズリ」【オリジナル曲】",
    # 全曲リスト
    }

# dev用ALL_VIDEOS------------------------------------------
DEV_ALL_VIDEOS = [
    #1,アルバム収録曲
    "spoQeZea7s8",
    "56Na2tuPOXs",
    "VRhZgfFOvZQ",
    "w3S9o1kSpqE",
    "5Zz_00sjwW0",
    #2,アルバム収録曲（現時点での）
    "RO6Z16icc8c",
    #最新曲---------------------------------------------------
    "x0APPrPgexY",
    "IxVFW1XIW7Q",
    "-2FCAZLhh-Y",
    "iUXrTnEeqRw",
    "uoYegcqyfxE",
    "8gcrKkXTx64",
    "Wiz0Ap2ge5U",
    "ZzBp3xUHvis",
    "VPK-lxmGyDk",
    "wW1UjAtAZ1A",
#     "tHo25oDiNNY",
#     "TC80uw4HgCw",
#     "Td9YlfLfXzM",
#     "5uHtY6DpRi4",
#     "Mb_bFtcyg3E",
#     "HhEJsD-ZOJU",
#     "NNgCHHgJ2W8", #Session
#     "N5YD6SEVwKs",
#     "iiPet5Z6vmg",
#     "5ImdVATcfKs",
#     "LKyLOLosp54",
#     "-yRWO4ODgQQ",
#     "5hgSET4bpbk",
#     "mCYjEWWsqZ8",
#     "qDV_zAf9T6g",
#     "m-bvW4pKT68",
#     "sU9GBNnoEmA",
#     "ConmlXSnM0E",
#     "HkTihNKCWFA",
#     "JE_GFOk90oU", #Session
#     "dgkP8RQw-sQ",
#     "7WXadfU7UOk",
#     "9OiYX68L0BU",
#     "Hvt59Q47M8k",
#     "6f3GJ3uUc34",
#     "qXvVt75kNmE",
#     "bqyENYGSQzg",
#     "q8Ap-1MUTew",
#     "uUB2qgVBBjY",
#     "ZiUwbmrMiAY",
#     "p3Geomh2EuY",
#     "lEoDjtCm488",
#     "vAFoNaPZ5Pk",
#     "rNZiCyCVIBQ",
#     "xQYp4-Ett6A",
#     "CHP7xCe8454",
#     "Rpe5gphy3Dg",
#     "tW6pTE_ENeo",
#     "PAwZl3Up-hc",
#     "FXNUn2KzcE8",
#     "NihQBHOZLIw",
#     "xgNeFTCzpgo",
#     "YXCBQDK4DlE",
#     "zQqIm-EVlkQ",
#     "ArqagB9P1Qs",
#     "SrdCXBZs4j8",
#     "cGGlBYzZiJs",
#     "ioW9iGDpQyw",
#     "hupkoU8e1is",
#     "f6TytcA47rI",
#     "UZTcXWLf2Ek",
#     "filTeBL7mA0",
#     "o2CD3DjPHmU",
#     "340OXvocRMM",
#     "M50V-UBjqcI",
#     "eurJC5ElRPE",
#     "7xht3kQO_TM",
#     "HyQK7IssB9M",
#     "sVqtVjtRcN8",
#     "_eBe5rD73Eg",
#     "S2AhFrGXa8I",
#     "vULemZ6DhM8",
#     "1gSMjPLRJik",
#     "XiKZE967BD4",
#     "sFoWYa6QNKk",
#     "yIo2ePCm4bY",
#     "exo3XdtPrgs",
#     "tI4nhL7qQdk",
#     "vLigCJOcHOE",
#     "PJrjwIlWVXA",
#     "P_DgrvZmXM0",
#     "06YWg6Y1kxo",
#     "r5xaccIl1Ps",
#     "Ou8sl4s3NJg",
#     "Ziz_ckzVjyA",
#     "Txh4DZmcbPk",
#     "ZTFQs7MspEI",
#     "UGzd2dnkhME",
#     "89p7DWIqOu8",
#     "pcRaY5kq4YY",
#     "Q5XzviXSHQ4",
#     "qtuX4cHk-vE",
#     "rzamOqbbBfQ",
#     "QJaY60vjSxw",
#     "w4fxj1toPzc",
#     "AfteRl4ePBc",
#     "lnfYoNLrMJE",
#     "qivTJhNbqUc",
#     "SBlkzGiM5uE",
    # 全曲リスト
    

]

# dev用タイトル辞書------------------------------------------
DEV_VIDEO_TITLES = {
    #1,アルバム収録曲
    "spoQeZea7s8":"淡さと微睡む",
    "56Na2tuPOXs":"れじぇろ",
    "VRhZgfFOvZQ":"アンダー",
    "w3S9o1kSpqE":"水流音楽",
    "5Zz_00sjwW0":"いいじゃない",
    #2,アルバム収録曲（現時点での）
    "RO6Z16icc8c":"大丈夫だよ。 (feat. 可不)",
    #最新曲---------------------------------------------------
    "x0APPrPgexY":"『月夜』/ MIMI feat. 宵 (Music Video)",
    "IxVFW1XIW7Q":"『花びら哀歌』/ feat. 重音テトSV",
    "-2FCAZLhh-Y":"『 柔く、ほどいて 』 / feat.初音ミク＆重音テトSV",
    "iUXrTnEeqRw":"『それでも優しかった君へ』/ MIMI feat.沖石",
    "uoYegcqyfxE":"『トリックハート』 / feat.重音テトSV",
    "8gcrKkXTx64":"『声の欠片』/ MIMI feat. 月",
    "Wiz0Ap2ge5U":"『星涙哀歌』/ MIMI feat. 初音ミク",
    "ZzBp3xUHvis":"『凪と藍空』 / MIMI feat. マス",
    "VPK-lxmGyDk":"『 愛されたいって願ってる 』/ MIMI feat. 可不",
    "wW1UjAtAZ1A":"『痛いの痛いの飛んでいけっ』 / MIMI feat. saewool (Music Video)",
     }
#     "tHo25oDiNNY",
#     "TC80uw4HgCw",
#     "Td9YlfLfXzM",
#     "5uHtY6DpRi4",
#     "Mb_bFtcyg3E",
#     "HhEJsD-ZOJU",
#     "NNgCHHgJ2W8", #Session
#     "N5YD6SEVwKs",
#     "iiPet5Z6vmg",
#     "5ImdVATcfKs",
#     "LKyLOLosp54",
#     "-yRWO4ODgQQ",
#     "5hgSET4bpbk",
#     "mCYjEWWsqZ8",
#     "qDV_zAf9T6g",
#     "m-bvW4pKT68",
#     "sU9GBNnoEmA",
#     "ConmlXSnM0E",
#     "HkTihNKCWFA",
#     "JE_GFOk90oU", #Session
#     "dgkP8RQw-sQ",
#     "7WXadfU7UOk",
#     "9OiYX68L0BU",
#     "Hvt59Q47M8k",
#     "6f3GJ3uUc34",
#     "qXvVt75kNmE",
#     "bqyENYGSQzg",
#     "q8Ap-1MUTew",
#     "uUB2qgVBBjY",
#     "ZiUwbmrMiAY",
#     "p3Geomh2EuY",
#     "lEoDjtCm488",
#     "vAFoNaPZ5Pk",
#     "rNZiCyCVIBQ",
#     "xQYp4-Ett6A",
#     "CHP7xCe8454",
#     "Rpe5gphy3Dg",
#     "tW6pTE_ENeo",
#     "PAwZl3Up-hc",
#     "FXNUn2KzcE8",
#     "NihQBHOZLIw",
#     "xgNeFTCzpgo",
#     "YXCBQDK4DlE",
#     "zQqIm-EVlkQ",
#     "ArqagB9P1Qs",
#     "SrdCXBZs4j8",
#     "cGGlBYzZiJs",
#     "ioW9iGDpQyw",
#     "hupkoU8e1is",
#     "f6TytcA47rI",
#     "UZTcXWLf2Ek",
#     "filTeBL7mA0",
#     "o2CD3DjPHmU",
#     "340OXvocRMM",
#     "M50V-UBjqcI",
#     "eurJC5ElRPE",
#     "7xht3kQO_TM",
#     "HyQK7IssB9M",
#     "sVqtVjtRcN8",
#     "_eBe5rD73Eg",
#     "S2AhFrGXa8I",
#     "vULemZ6DhM8",
#     "1gSMjPLRJik",
#     "XiKZE967BD4",
#     "sFoWYa6QNKk",
#     "yIo2ePCm4bY",
#     "exo3XdtPrgs",
#     "tI4nhL7qQdk",
#     "vLigCJOcHOE",
#     "PJrjwIlWVXA",
#     "P_DgrvZmXM0",
#     "06YWg6Y1kxo",
#     "r5xaccIl1Ps",
#     "Ou8sl4s3NJg",
#     "Ziz_ckzVjyA",
#     "Txh4DZmcbPk",
#     "ZTFQs7MspEI",
#     "UGzd2dnkhME",
#     "89p7DWIqOu8",
#     "pcRaY5kq4YY",
#     "Q5XzviXSHQ4",
#     "qtuX4cHk-vE",
#     "rzamOqbbBfQ",
#     "QJaY60vjSxw",
#     "w4fxj1toPzc",
#     "AfteRl4ePBc",
#     "lnfYoNLrMJE",
#     "qivTJhNbqUc",
#     "SBlkzGiM5uE",
#     # 全曲リスト
#     }

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

/* --------- 高さ ------- */
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


.secret-modal {
  position: fixed;
  inset: 0;

  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(4px);

  z-index: 3000;
}


.secret-box {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  background: rgba(20,20,45,1);
  padding: 24px;
  border-radius: 16px;
  color: rgba(255,255,255,0.92);
  text-align: center;
  width: 260px;

  max-height: 80vh;
}

.secret-box p:first-child {
    color: #ffffff !important;
    font-weight: 500;
}

.secret-hint {
  font-size: 12px;
  margin-top: 6px;
  color: rgba(255, 255, 255, 0.65);
}

.secret-box button {
    background: transparent;
    color: #fff;
    height: 30px;
    font-size: 15px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.4);
    cursor: pointer;
}

.secret-box button:hover {
    background: #e6e6e6;
}



/* Enterボタン右寄せ */
.secret-box button:first-of-type {
    margin-left: 6px;
}

/* 閉じるボタン下中央 */
#passwordModal .secret-box button:last-of-type {
    display: block;
    margin: 16px auto 0 auto;
}

.secret-box input[type="password"] {
    font-size: 16px;
    width: 170px;
    height: 32px;
    padding: 4px 8px;
    border-radius: 6px;
    border: none;
    box-sizing: border-box;
}

.secret-box .button-row {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 16px;
}

.button-row {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 20px;
}


.secret-message {
    font-size: 14px;
    margin: 12px 0 20px 0;
    color: rgba(255,255,255,0.88); 
    line-height: 1.8;
}


.song-title{
display:block;
max-width:90%;
margin:12px auto;
font-size:16px;
line-height:1.6;
text-align:center;
word-break:keep-all;
overflow-wrap:break-word;
opacity:0.85;
color: #95999d;
text-decoration:none;
}

.song-title:hover{
opacity:0.8;
}

.ext{
margin-left:6px;
font-size:0.8em;
opacity:0.6;
}

.share-btn{
display:block;
margin-top:14px;
font-size:14px;
opacity:1;
text-decoration:none;
color:#808080;
font-weight:500;
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

<button onclick="location.href='/dev'" style="
  margin-top:10px;
  padding:8px 12px;
  border-radius:8px;
  background:#222;
  color:#e6e8ff;
  border:none;
  cursor:pointer;
">
  開発者モード
</button>

<hr>

<details class="update-section">
  <summary>更新履歴</summary>

  <!-- 直近の更新履歴 -->
  <div class="update-list">
    26.4.11 楽曲情報の表示を追加<br>
    26.4.5 開発者モードの追加<br>
    26.4.5 重複IDの削除<br>
    26.3.25 楽曲追加<br>
    26.3.8 Twitter(X)共有機能を追加<br>
  </div>

  <!-- 古い履歴 -->
  <details>
    <summary>過去の更新を見る</summary>
    <div class="update-list">
      26.3.8 MIMI Time内の収録曲数の追加<br>
      26.3.8 楽曲情報の追加<br>
      26.3.2 特定操作で表示されるページを追加<br>
      26.3.2 各種動作の安定化<br>
      26.3.1 更新状況タブを追加<br>
      26.3.1 文字色の修正<br>
      26.3.1 更新履歴タブの修正<br>
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
    1,修正コードの作成<br>
    2,全曲（提供曲）の登録<br>
  </div>
</details>

<details class="license-section">
  <summary>ライセンス</summary>

  <div class="license-text">
    © 2026 yu-sabu<br>
    本サイトのコードは、個人利用および非商用利用に限り使用を許可します。<br>
    商用利用は禁止します。<br>
    記載している動画はYouTube公式の埋め込み機能を使用しています。<br>
    各動画の著作権はそれぞれの権利者様に帰属します。<br>
    X（旧Twitter）はX Corp.の商標です。<br><br>
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

<h1 id="mainTitle">{{ label }}</h1>

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

<a class="song-title"
href="https://www.youtube.com/watch?v={{ video_id }}"
target="_blank"
onclick="return confirmYouTube()">

{{ title }}

</a>

<button class="main-btn" onclick="reloadWithOption()">
    もう一曲と出会う
</button>

{% if footer %}
<div class="footer-text">{{ footer }}</div>
{% endif %}

<a class="share-btn"
href="https://twitter.com/intent/tweet?text=今、この曲に出会いました。%0A%0A{{ title }}%0Ahttps://youtu.be/{{ video_id }}%0A%0AMIMI Time%0Ahttps://mimitimefan03.pythonanywhere.com%0A%0A%23MI民%E3%80%80%23MIMI_Time03"
target="_blank">
 ▶ この曲をXで共有する
</a>

<p style="opacity:0.55; font-size:13px; margin-top:10px;">
現在 {{ song_count }} 曲収録されています
</p>

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


// パスワード表示

let tapCount = 0;
let tapTimer = null;

document.getElementById("mainTitle").addEventListener("click", function() {

    tapCount++;

    if (tapCount >= 5) {
        document.getElementById("passwordModal").style.display = "flex";
        tapCount = 0;
    }

    clearTimeout(tapTimer);
    tapTimer = setTimeout(() => {
        tapCount = 0;
    }, 2000);
});


// パスワード解除

function unlockSecret() {
    const input = document.getElementById("secretInput").value.trim().toLowerCase();

    const validPasswords = [
        "mimi",
        "マシュマリー",
        "ましゅまりー",
        "mashumary",
        "masyumary",
        "ただ声一つ",
        "ただこえひとつ",
        "tadakoehitotu",
        "ハナタバ",
        "はなたば",
        "hanataba",
        "ラピスラズリ",
        "らぴすらずり",
        "rapisurazuri",
        "よるつむぎ",
        "yorutumugi"
        
    ];

    if (validPasswords.includes(input)) {
        document.getElementById("passwordModal").style.display = "none";
        document.getElementById("secretModal").style.display = "flex";
        document.body.style.overflow = "hidden";
        document.getElementById("secretInput").value = "";
    } else {
        alert("パスワードが違うようです");
    }
}

function closePassword() {
    document.getElementById("passwordModal").style.display = "none";
    document.body.style.overflow = "auto";
}

function goHome() {
    document.getElementById("secretModal").style.display = "none";
    document.body.style.overflow = "";
}

window.addEventListener("DOMContentLoaded", function() {
    document.getElementById("secretInput").addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            unlockSecret();
        }
    });
});

// リセット（隠しページ内）

function resetSecret() {
    document.getElementById("secretOption").checked = false;

    document.getElementById("secretModal").style.display = "none";
    document.getElementById("passwordModal").style.display = "flex";
}


</script>


<!-- パスワード画面 -->
<div id="passwordModal" class="secret-modal" style="display:none;">
  <div class="secret-box">
    <p>パスワードを入力してください</p>
    <p class="secret-hint">ヒント：MIMIさんの代表曲は？</p>
    <input type="password" id="secretInput">
    <button onclick="unlockSecret()">Enter</button>
    <button onclick="closePassword()">閉じる</button>
    
  </div>
</div>

<!-- 隠しページ -->
<div id="secretModal" class="secret-modal" style="display:none;">
  <div class="secret-box">
    <p>この場所を見つけたあなたへ。</p>
    <p class="secret-message">
        ここは見つけたあなただけが変えられる場所です
    </p>
<label>
    <input type="checkbox" id="secretOption">
    未設定項目です
</label>

<div class="button-row">
    <button onclick="resetSecret()">設定をリセット</button>
    <button onclick="goHome()">ホームに戻る</button>
</div>    

</div>

</body>
</div>
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
#開発モード------------------------------------------------------------------------------------------------------------------------
DEV_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>[DEV] MIMI Time</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500&display=swap" rel="stylesheet">
<style>



body {
    margin: 0;
    background-color: {{ bg }};
    font-family: 'Zen Maru Gothic', sans-serif;
    transition: background-color 0.5s;
    text-align: center;
    color: {{ text_main }};
}

/* 開発バー（上部固定）*/
#devBar {
    position: fixed;
    top: 0; left: 0; right: 0;
    background: rgba(20, 20, 20, 0.92);
    color: #e6e8ff;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 9999;
    font-size: 13px;
    flex-wrap: wrap;
    backdrop-filter: blur(6px);
}

#devBar a {
    color: #aac0ff;
    text-decoration: none;
    padding: 4px 10px;
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 999px;
    font-size: 12px;
}

#devBar select {
    background: #1e1e3f;
    color: #e6e8ff;
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 12px;
}

#devBar span {
    opacity: 0.5;
    font-size: 12px;
}

.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 110px 16px 96px;
    box-sizing: border-box;
}

h1 { margin: 0 0 8px; color: {{ text_main }}; }
p { margin: 6px 0; color: {{ text_sub }}; }
.time { color: {{ text_faint }}; }

.video-wrap { margin-top: 24px; }
.video-wrap iframe {
    width: 100%;
    aspect-ratio: 16 / 9;
    border-radius: 12px;
    border: none;
}

.song-title {
    display: block;
    max-width: 90%;
    margin: 12px auto;
    font-size: 16px;
    line-height: 1.6;
    text-align: center;
    color: #a9a9a9;
    text-decoration: none;
}

/*再リロード*/

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
    background: rgba(255,255,255,0.25);
}



.main-btn:hover {
    background: rgba(255,255,255,0.25);
    transform: translateY(-2px);
}

.footer-text { margin-top: 12px; color: {{ text_faint }}; }
</style>
</head>

<body class="{{ zone }}">

<!-- 開発バー -->
<div id="devBar">
    <a href="/main">← メインに戻る</a>
    <span>DEV MODE</span>
    <label>時間帯：
        <select onchange="location.href='/dev?zone='+this.value">
            <option value="morning"   {% if zone=='morning'   %}selected{% endif %}>morning（朝）</option>
            <option value="day"       {% if zone=='day'       %}selected{% endif %}>day（昼）</option>
            <option value="evening"   {% if zone=='evening'   %}selected{% endif %}>evening（夕）</option>
            <option value="night"     {% if zone=='night'     %}selected{% endif %}>night（夜）</option>
            <option value="late night"{% if zone=='late night'%}selected{% endif %}>late night（深夜）</option>
        </select>
    </label>
    <span>動画ID: {{ video_id }}</span>
</div>

<div class="container">

    <h1>{{ label }}</h1>
    <p>時間帯：{{ zone }} / {{ time }}</p>

    {% if video_id %}
    <div class="video-wrap">
        <iframe src="https://www.youtube.com/embed/{{ video_id }}" allowfullscreen></iframe>
    </div>
    {% endif %}

    <a class="song-title"
       href="https://www.youtube.com/watch?v={{ video_id }}"
       target="_blank">{{ title }}</a>

    <button class="main-btn" onclick="location.reload()">別の曲を試す</button>

    {% if footer %}
    <div class="footer-text">{{ footer }}</div>
    {% endif %}
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
    title = VIDEO_TITLES.get(video_id, "")
#     title = get_title(video_id)
    
    return render_template_string(
        HTML,
        label=TIME_LABEL[zone],
        zone=zone,
        time=now.strftime("%H:%M"),
        bg=BG_COLOR[zone],
        footer=FOOTER_TEXT[zone],
        video_id=video_id,
        title=title,
        text_main=TEXT_COLOR_MAIN[zone],
        text_sub=TEXT_COLOR_SUB[zone],
        text_faint=TEXT_COLOR_FAINT[zone],
        song_count=len(ALL_VIDEOS),
    )

def get_title(video_id):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data["title"]
    except:
        return ""

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
    print("selected:", selected)

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
# 調整用----------------------------------------------------------------------------

@app.route("/dev")
def dev():
    zone_override = request.args.get("zone")
    no_repeat = request.args.get("no_repeat") == "true"

    hour = get_current_hour()
    zone = zone_override if zone_override in TIME_LABEL else get_time_zone(hour)
    now = datetime.now(JST)

    video_id = random.choice(DEV_ALL_VIDEOS)
    title = DEV_VIDEO_TITLES.get(video_id, "")

    return render_template_string(
        DEV_HTML,
        label=TIME_LABEL[zone],
        zone=zone,
        time=now.strftime("%H:%M"),
        bg=BG_COLOR[zone],
        footer=FOOTER_TEXT[zone],
        video_id=video_id,
        title=title,
        text_main=TEXT_COLOR_MAIN[zone],
        text_sub=TEXT_COLOR_SUB[zone],
        text_faint=TEXT_COLOR_FAINT[zone],
        song_count=len(DEV_ALL_VIDEOS),
    )

@app.errorhandler(404)
def not_found(e):
    return render_template_string("""
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {
        background:#0B0B1A;
        color:white;
        text-align:center;
        font-family:sans-serif;
        padding-top:100px;
    }
    a {
        color:#aaa;
        text-decoration:none;
    }
    </style>
    </head>
    <body>
        <h1>ページが見つかりませんでした</h1>
        <p>現在このページは表示できません</p>
        <br>
        <a href="/main">もう一度試す</a>
    </body>
    </html>
    """), 404

@app.errorhandler(500)
def server_error(e):
    return render_template_string("""
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {
        background:#0B0B1A;
        color:white;
        text-align:center;
        font-family:sans-serif;
        padding-top:100px;
    }
    a {
        color:#aaa;
        text-decoration:none;
    }
    </style>
    </head>
    <body>
        <h1>サーバーでエラーが発生しました</h1>
        <p>現在この曲は表示できません</p>
        <br>
        <a href="/main">もう一度試す</a>
    </body>
    </html>
    """), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)