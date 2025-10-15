# 画像ビューア RESTful API システム

画像管理・閲覧機能を提供する RESTful API システムです。Python + Tornado で構築されています。

## 技術スタック

- **Framework**: Tornado（非同期 Web フレームワーク）
- **Language**: Python 3.x
- **Data Storage**: CSV ファイル（Pandas DataFrame として管理）

## 機能

### データ構造

- CSV ファイルに以下の情報を保存：
  - `filename`: 画像ファイル名
  - `original`: 元画像の註釈
  - `protanope`: 第一色覚者向けシミュレーション画像の註釈
- CSV ファイル名: `images.csv`
- 画像保存ディレクトリ: `./images/`
  - `images/original/{filename}` - 元画像
  - `images/protanope/{filename}` - シミュレーション画像

### API エンドポイント

1. **GET /api/images**
   - 全画像のリストを取得（ページネーション対応）
   - パラメータ：
     - `page`: ページ番号（デフォルト: 1）
     - `page_size`: 1ページあたりの件数（デフォルト: 20、最大: 100）
   - レスポンス形式: JSON

2. **GET /api/images/{imagetype}/{filename}**
   - 特定の画像の詳細情報を取得
   - `imagetype`: `original` または `protanope`
   - レスポンス形式: JSON

3. **GET /images/{imagetype}/{filename}**
   - 実際の画像ファイルを返す
   - Content-Type: image/*

4. **GET /**
   - 簡易的な HTML ビューア

## ディレクトリ構成

```
project/
├── server.py           # メインアプリケーション
├── handlers/           # リクエストハンドラ
│   ├── __init__.py
│   ├── image_handler.py
│   └── api_handler.py
├── models/             # データモデル
│   ├── __init__.py
│   └── image_model.py
├── static/             # 静的ファイル
│   └── index.html      # HTMLビューア
├── images/             # 画像保存ディレクトリ
│   ├── original/       # 元画像
│   └── protanope/      # シミュレーション画像
├── images.csv          # メタデータ
├── requirements.txt
└── README.md
```

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. データの準備

#### images.csv の作成

CSV ファイルを以下の形式で作成してください：

```csv
filename,original,protanope
image1.jpg,元画像の説明,シミュレーション画像の説明
image2.jpg,元画像の説明,シミュレーション画像の説明
```

#### 画像ファイルの配置

画像を適切なディレクトリに配置してください：

```
images/
├── original/
│   ├── image1.jpg
│   └── image2.jpg
└── protanope/
    ├── image1.jpg
    └── image2.jpg
```

## 起動方法

```bash
python server.py
```

または

```bash
python3 server.py
```

サーバーは http://localhost:8888 で起動します。

## 使用例

### API リクエスト例

#### 全画像リストの取得（1ページ目）
```bash
curl http://localhost:8888/api/images?page=1&page_size=20
```

#### 特定の画像の詳細情報取得
```bash
curl http://localhost:8888/api/images/original/image1.jpg
```

#### 画像ファイルの取得
```bash
curl http://localhost:8888/images/original/image1.jpg -o image1.jpg
```

### Web ブラウザでの閲覧

ブラウザで http://localhost:8888 にアクセスすると、HTMLビューアが表示されます。

## 拡張性

### 画像タイプの追加

新しい画像タイプを追加する場合：

1. `handlers/image_handler.py` の `IMAGE_TYPES` リストに新しいタイプを追加
2. `images/` ディレクトリに新しいサブディレクトリを作成
3. CSV ファイルに対応するカラムを追加

例：
```python
# handlers/image_handler.py
IMAGE_TYPES = ['original', 'protanope', 'deuteranope']
```

## ログ

サーバーは標準出力にログを出力します。ログレベルは INFO です。

## エラーハンドリング

- 400: 不正なリクエストパラメータ
- 404: 画像が見つからない
- 500: サーバー内部エラー

## ライセンス

このプロジェクトは教育・研究目的で作成されたものです。