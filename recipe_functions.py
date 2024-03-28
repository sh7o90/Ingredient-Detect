import requests
from urllib.parse import urlparse

RECIPE_API_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426"
RECIPE_RANKING_API_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"
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

def get_recipe_ranking(category_id):
    """
    指定されたカテゴリーのレシピランキングを取得する関数

    Args:
        category_id (str): カテゴリーID

    Returns:
        list: 指定されたカテゴリーのレシピランキング情報を含むリスト
              取得に失敗した場合はNoneを返す
    """
    params = {
        "format": "json",
        "categoryId": category_id,
        "applicationId": APP_ID
    }
    response = requests.get(RECIPE_RANKING_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        return None


def search_recipe_by_keyword(keyword):
    """
    指定されたキーワードに関連するレシピカテゴリーを検索する関数

    Args:
        keyword (str): 検索キーワード

    Returns:
        list: 検索キーワードと完全一致するレシピカテゴリーのリスト
              一致するカテゴリーがない場合は空のリストを返す
    """
    categories_response = get_recipe_categories()
    if categories_response:
        categories = categories_response["result"]["small"]
        matching_categories = []
        for category in categories:
            # キーワードとカテゴリー名が完全一致する場合のみ追加
            if keyword == category["categoryName"]:
                matching_categories.append(category)
        return matching_categories
    else:
        return None

def get_recipe_categories():
    """
    レシピカテゴリーを楽天レシピAPIから取得する関数

    Returns:
        dict: 楽天レシピAPIから取得したレシピカテゴリー情報を含むJSON形式のデータ
              取得に失敗した場合はNoneを返す
    """
    params = {
        "format": "json",
        "categoryType": "small",
        "applicationId": APP_ID
    }
    response = requests.get(RECIPE_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
