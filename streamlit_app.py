import os
import streamlit as st
import requests
import base64
import io
from PIL import Image
from urllib.parse import urlparse
from object_detection import detect_objects
from recipe_functions import (
    search_recipe_by_keyword,
    get_recipe_ranking,
    en_to_jp,
    jp_to_category_id
)

def resize_image(image_url, width):
    """
    画像を指定された幅と高さにリサイズする関数

    Args:
        image_url (str): 画像のURL
        width (int): リサイズ後の幅

    Returns:
        リサイズ後の画像URL
    """

    # 画像をダウンロード
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))

    # 画像の幅と高さを指定してリサイズ
    resized_image = image.resize((width, int(image.height * width / image.width)))

    # リサイズ後の画像を保存
    buffer = io.BytesIO()
    resized_image.save(buffer, format="JPEG")

    # リサイズ後の画像URLを返す
    return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode()}"

IMG_TMP = 'tmp'

def main():
    st.title("Ingredient Detect")

    # ファイルのアップロード
    img_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if img_file is not None:
        # アップロードした画像データを取得
        img_bytes = img_file.getvalue()

        col1, col2 = st.columns(2)

        with col1:
            st.image(img_bytes, use_column_width=True)

        # 物体検出の実行
        results = detect_objects(img_bytes)

        with col2:
            st.image(img_bytes, use_column_width=True)

        # 物体検出の結果を表示
        classes = results[0].boxes.cls
        classes_map = results[0].names  # クラス番号と名称
        detected_classes = [classes_map[int(cls)] for cls in classes]

        # 重複を削除して一意の選択肢のみを取得
        unique_detected_classes = list(set(detected_classes))

        # コンボボックスと検索ボタンを作成
        selected_class = st.sidebar.selectbox("Select a detected class:", unique_detected_classes)
        search_button = st.sidebar.button("Search Recipes")

        # 検索ボタンが押された場合
        if search_button:
            # キーワードに関連するレシピを検索
            st.sidebar.write(f"Searching for recipes related to '{selected_class}'...")
            selected_class_jp = en_to_jp.get(selected_class, selected_class)
            matching_categories = search_recipe_by_keyword(selected_class_jp)
            if matching_categories:
                # 検索結果がある場合はカテゴリごとに表示
                st.sidebar.write("Search results found:")
                for category in matching_categories:
                    # カテゴリ名とURLを表示
                    category_id = urlparse(category['categoryUrl']).path.split('/')[2]
                    st.sidebar.write(f"Category Name: {selected_class_jp}({selected_class}) ")
                    st.sidebar.write(f"Category URL: {category_id}")
                    # カテゴリIDを渡してレシピランキングを取得
                    recipe_ranking = get_recipe_ranking(category_id)
                    if recipe_ranking:
                        # レシピランキングがある場合は表示
                        recipe_data = []

                        # ランキング取得
                        for rank, recipe in enumerate(recipe_ranking, start=1):
                            # レシピ情報をリストに追加
                            recipe_info = {
                                "rank": rank,
                                "foodImageUrl": recipe["foodImageUrl"],
                                "recipeTitle": recipe["recipeTitle"],
                                "recipeUrl": recipe["recipeUrl"],
                                "recipeMaterial": recipe["recipeMaterial"],
                                "recipeIndication": recipe["recipeIndication"]
                            }
                            recipe_data.append(recipe_info)

                        # 画像サイズを統一
                        for recipe in recipe_data:
                            recipe["foodImageUrl"] = resize_image(recipe["foodImageUrl"], width=150)

                        # CSSによるスタイル設定
                        st.markdown(f"""
                        <style>
                        img {{
                            width: 150px;
                            border: 1px solid #ccc;
                            padding: 10px;
                            filter: opacity(0.7);
                        }}
                        .recipe-title {{
                            font-size: 18px;
                            font-weight: bold;
                            text-decoration: none;
                            color: #000;
                        }}
                        </style>
                        """, unsafe_allow_html=True)

                        # ランキング表示
                        for recipe in recipe_data:
                            # レシピ情報
                            rank = recipe["rank"]
                            recipe_title = recipe["recipeTitle"]
                            recipe_url = recipe["recipeUrl"]
                            recipe_indication = recipe["recipeIndication"]
                            recipe_material = recipe["recipeMaterial"]

                            # 2列レイアウト
                            with st.container():
                                col1, col2 = st.columns([1, 2])

                                with col1:
                                    # レシピ画像 (CSSによるスタイルが適用される)
                                    st.image(recipe["foodImageUrl"])

                                with col2:
                                    # レシピ情報
                                    st.markdown(f"<p class='recipe-rank'>{recipe['rank']}位</p>", unsafe_allow_html=True)
                                    st.markdown(f"<a href='{recipe['recipeUrl']}' class='recipe-title'>{recipe['recipeTitle']}</a>", unsafe_allow_html=True)
                                    st.markdown(f"<p class='recipe-indication'>{recipe['recipeIndication']}</p>", unsafe_allow_html=True)

                                    # 材料の表示
                                    st.markdown(f"""
                                    <ul style="list-style: none; padding: 0;">
                                    {''.join([f'<li>{item}</li>' for item in recipe_material])}
                                    </ul>
                                    """, unsafe_allow_html=True)

                                    # 作り方
                                    st.markdown(f"<a href='{recipe['recipeUrl']}' class='recipe-link'><span class='recipe-icon'><i class='fas fa-chevron-right'></i></span> 作り方はこちら</a>", unsafe_allow_html=True)
                    # else:
                        # st.write(f"No recipe ranking found for category ID {category_id}.")
            else:
                # 検索結果がない場合はメッセージを表示
                st.write("No search results found.")

if __name__ == "__main__":
    main()
