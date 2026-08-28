# Ingredient Detect 🥑🔍

画像から食材（野菜など）を自動検出し、その食材を使った楽天レシピのランキングを表示するStreamlitアプリケーションです。

## 概要

本アプリケーションは、アップロードされた食材画像をYOLOv8モデル（`mybest.pt`）で解析し、検出された食材を用いたレシピを楽天レシピAPI経由で検索・表示します。

🌐 **Web App**: [https://ingredient-detect.streamlit.app/](https://ingredient-detect.streamlit.app/)

---

## 🛠 セットアップ & 実行手順

### 1. 仮想環境（venv）の作成と有効化

**Windows**:
```cmd
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. APIキーの設定

楽天デベロッパーで取得したアプリID（`applicationId`）およびアクセスキー（`accessKey`）を設定します。
サンプル設定ファイルをコピーし、ご自身のキーを入力してください。

```bash
# サンプル設定ファイルをコピー
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml` を開き、キーを入力します。
```toml
RAKUTEN_APP_ID = "YOUR_APPLICATION_ID"
RAKUTEN_ACCESS_KEY = "YOUR_ACCESS_KEY"
```

### 4. 作業用フォルダの準備

アプリがアップロード画像を一時保存する `tmp` フォルダを作成します。

```bash
mkdir tmp
```

### 5. アプリケーションの起動

```bash
streamlit run streamlit_app.py
```

起動後、自動的にブラウザが開くか、表示された [http://localhost:8501](http://localhost:8501) にアクセスしてください。
また、公開中のアプリは [https://ingredient-detect.streamlit.app/](https://ingredient-detect.streamlit.app/) からご利用いただけます。

---

## 📖 使い方

1. **画像のアップロード**: サイドバーの「Upload an image」から食材画像（`.jpg` / `.png`）をアップロードします。
   *(※ 動作確認用の画像が `sample_images/` ディレクトリに用意されています)*
2. **自動検出**: 画像内の食材がYOLOv8モデルにより自動で識別されます。
3. **食材の選択**: サイドバーの「Select a detected class」から検索したい食材（例: `tamanegi`, `ninjin` など）を選択します。
4. **レシピ検索**: 「Search Recipes」ボタンをクリックすると、楽天レシピAPIよりランキング形式でレシピ情報（画像、タイトル、調理目安、材料一覧）が表示されます。

---

## 📁 プロジェクト構成

```
Ingredient-Detect/
├── .streamlit/
│   └── secrets.toml.example # 秘密情報設定サンプルの設定ファイル
├── sample_images/           # 動作確認用サンプル画像フォルダ
├── .gitignore               # Git除外設定ファイル
├── mybest.pt                # 食材検出用ファインチューニング済みYOLOv8モデル
├── yolov8n.pt               # YOLOv8 nano ベースモデル
├── object_detection.py      # YOLOv8を用いた物体検出モジュール
├── recipe_functions.py      # 楽天レシピAPI連携・カテゴリ変換モジュール
├── streamlit_app.py         # Streamlit UI / アプリケーションメイン処理
├── requirements.txt         # 必要なPythonパッケージ一覧
├── packages.txt             # システム依存パッケージ一覧（Streamlit Cloud等用）
└── README.md                # 本ドキュメント
```

---

## 🔗 連携サービス
- [楽天ウェブサービス / 楽天レシピAPI](https://webservice.rakuten.co.jp/)
