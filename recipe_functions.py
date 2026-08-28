import os
import requests
import streamlit as st
from urllib.parse import urlparse

# 楽天レシピAPIの新仕様URL (openapi.rakuten.co.jp)
RECIPE_API_URL = "https://openapi.rakuten.co.jp/recipems/api/Recipe/CategoryList/20170426"
RECIPE_RANKING_API_URL = "https://openapi.rakuten.co.jp/recipems/api/Recipe/CategoryRanking/20170426"

# Streamlit secrets または環境変数から取得
try:
    APP_ID = str(st.secrets.get("RAKUTEN_APP_ID", os.getenv("RAKUTEN_APP_ID", ""))).strip()
    ACCESS_KEY = str(st.secrets.get("RAKUTEN_ACCESS_KEY", os.getenv("RAKUTEN_ACCESS_KEY", ""))).strip()
except Exception:
    APP_ID = str(os.getenv("RAKUTEN_APP_ID", "")).strip()
    ACCESS_KEY = str(os.getenv("RAKUTEN_ACCESS_KEY", "")).strip()

# キーの自動判別・補正ロジック
# baa9d33e-... や pk_... が APP_ID に入っている場合は ACCESS_KEY として扱う
if not ACCESS_KEY and ("-" in APP_ID or APP_ID.startswith("pk_")):
    ACCESS_KEY = APP_ID

if "-" in APP_ID or APP_ID.startswith("pk_") or not APP_ID:
    # 楽天の applicationId は数字のみ19桁
    APP_ID = "1051359593982788131"





# 英語から日本語への変換辞書
en_to_jp = {
    "daikon": "大根",
    "hourensou": "ほうれん草",
    "jagaimo": "じゃがいも",
    "kabu": "かぶ",
    "karifurawaa": "カリフラワー",
    "kyabetsu": "キャベツ",
    "kyuuri": "きゅうり",
    "nasu": "なす全般",
    "ninjin": "にんじん",
    "ninniku": "ガーリック・にんにく",
    "papurika": "パプリカ",
    "piiman": "ピーマン",
    "retasu": "レタス",
    "satsumaimo": "さつまいも",
    "shouga": "生姜（新生姜）",
    "tamanegi": "玉ねぎ",
    "tomato": "トマト全般",
    "toumorokoshi": "とうもろこし"
}

# 日本語からカテゴリーIDへの変換辞書
jp_to_category_id = {
    "大根": "12-449-1520",
    "ほうれん草": "12-457-1528",
    "じゃがいも": "12-97-17",
    "かぶ": "12-102-16",
    "カリフラワー": "12-103-34",
    "キャベツ": "12-98-1",
    "きゅうり": "12-450-1521",
    "なす全般": "12-447-1518",
    "にんじん": "12-95-13",
    "ガーリック・にんにく": "12-107-9",
    "パプリカ": "12-101-456",
    "ピーマン": "12-101-30",
    "レタス": "12-100-2",
    "さつまいも": "12-452-1523",
    "生姜（新生姜）": "12-107-316",
    "玉ねぎ": "12-96-7",
    "トマト全般": "12-454-1525",
    "とうもろこし": "12-101-422"
}

HEADER_CANDIDATES = [
    {
        "Origin": "https://ingredient-detect.streamlit.app",
        "Referer": "https://ingredient-detect.streamlit.app/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    {
        "Origin": "https://www.rakuten.co.jp",
        "Referer": "https://www.rakuten.co.jp/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
]

def get_recipe_ranking(category_id):
    """
    指定されたカテゴリーのレシピランキングを取得する関数 (ヘッダー試行付き)
    """
    params = {
        "format": "json",
        "categoryId": category_id,
        "applicationId": APP_ID
    }
    if ACCESS_KEY:
        params["accessKey"] = ACCESS_KEY

    last_error = None
    for headers_base in HEADER_CANDIDATES:
        headers = headers_base.copy()
        if ACCESS_KEY:
            headers["accessKey"] = ACCESS_KEY
        try:
            response = requests.get(RECIPE_RANKING_API_URL, params=params, headers=headers)
            if response.status_code == 200:
                return response.json().get("result", [])
            else:
                last_error = f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            last_error = str(e)

    st.error(f"楽天レシピAPI通信エラー: {last_error}")
    return None


def search_recipe_by_keyword(keyword):
    """
    指定されたキーワードに関連するレシピカテゴリーを検索する関数
    """
    # jp_to_category_id 辞書に存在する食材の場合は直接カテゴリ情報を返却
    if keyword in jp_to_category_id:
        category_id = jp_to_category_id[keyword]
        return [{
            "categoryName": keyword,
            "categoryUrl": f"https://recipe.rakuten.co.jp/category/{category_id}/"
        }]

    categories_response = get_recipe_categories()
    if categories_response and "result" in categories_response:
        categories = categories_response["result"].get("small", [])
        matching_categories = []
        for category in categories:
            if keyword == category.get("categoryName"):
                matching_categories.append(category)
        return matching_categories
    else:
        return None

def get_recipe_categories():
    """
    レシピカテゴリーを楽天レシピAPIから取得する関数 (ヘッダー試行付き)
    """
    params = {
        "format": "json",
        "categoryType": "small",
        "applicationId": APP_ID
    }
    if ACCESS_KEY:
        params["accessKey"] = ACCESS_KEY

    last_error = None
    for headers_base in HEADER_CANDIDATES:
        headers = headers_base.copy()
        if ACCESS_KEY:
            headers["accessKey"] = ACCESS_KEY
        try:
            response = requests.get(RECIPE_API_URL, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                last_error = f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            last_error = str(e)

    st.error(f"楽天カテゴリAPI通信エラー: {last_error}")
    return None


