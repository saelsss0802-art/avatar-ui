# Avatar UI (with Google ADK)

レトロフューチャーなデザインのチャットボットUIアプリケーションです。
Google Gemini (Google ADK) をバックエンドに使用し、Electron で動作するデスクトップアプリとして設計されています。

![screenshot](./app/src/renderer/assets/idle.png)

## ✨ 特徴

*   **レトロ端末風 UI**: 懐かしくも新しい、コンソール風のインターフェース。
*   **Google Gemini 連携**: Google の最新 AI モデルによる高度な会話機能。
*   **Google 検索対応**: 最新の情報を検索して回答する機能を標準搭載。
*   **Electron アプリ**: Windows, Mac, Linux で動作するデスクトップアプリケーション。
*   **開発者フレンドリー**: AG-UI プロトコル準拠。Python (FastAPI) と TypeScript (Electron) の分離構成で拡張が容易。

## 🚀 クイックスタート（開発者向け）

ソースコードをクローンして、開発モードで起動する手順です。

### 1. 前提条件
*   Node.js (v20以上推奨)
*   Python (v3.12以上推奨)
*   Google Gemini API Key ([取得はこちら](https://aistudio.google.com/app/apikey))

### 2. インストール

```bash
# リポジトリをクローン
git clone https://github.com/avatar-ui/sito-dev-019.git avatar-ui
cd avatar-ui

# クライアント依存パッケージのインストール
cd app
npm install
```

### 3. サーバー設定

```bash
# サーバーディレクトリへ移動
cd ../server

# 仮想環境の作成と有効化
python3 -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# 依存ライブラリのインストール
pip install .

# 環境変数の設定
cp .env.example .env
# .env を開き、GOOGLE_API_KEY にキーを入力してください
```

### 4. 起動

クライアントとサーバーを同時に起動します。

```bash
# アプリディレクトリで実行
cd ../app
npm run dev
```

アプリが起動し、チャットが可能になります。

## 📦 配布用パッケージのビルド

エンドユーザー向けに `.exe` や `.dmg` ファイルを作成する場合の手順です。

```bash
cd app
npm run build    # ビルド
npm run package  # パッケージ作成
```

`app/dist/` フォルダにインストーラーが生成されます。
Github Releases などで配布することを推奨します。

## 🛠️ カスタマイズ

*   **エージェントの性格**: `server/main.py` の `instruction` を変更してください。
*   **ツールの追加**: `server/main.py` の `tools` リストに追加します。
*   **UIの変更**: `app/src/renderer/` 内の HTML/CSS を編集してください。

## 📜 ライセンス

[MIT License](LICENSE)
