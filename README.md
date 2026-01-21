# SPECTRA

Grok API (xai-sdk) を使用したAIキャラクター基盤システム。
Roblox、Console、その他のプラットフォームから統一されたAPIでアクセス可能。

## システム概要

```
┌─────────────────────────────────────────────────────────────┐
│  クライアント                                                │
│  [Roblox]  [Console]  [その他]                              │
│      ↓       ↓       ↓                                      │
└──────┼───────┼───────┼──────────────────────────────────────┘
       │       │       │
       ↓       ↓       ↓
┌─────────────────────────────────────────────────────────────┐
│  https://spectra.siqi.jp                                    │
│  (Cloudflare Tunnel)                                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌──────────────────────────▼──────────────────────────────────┐
│  SPECTRA Core (Python + FastAPI)                            │
│                                                             │
│  ├── /health     → ヘルスチェック                           │
│  ├── /v1/think   → 汎用コアAPI                              │
│  └── /roblox     → Roblox互換エンドポイント                 │
│                                                             │
│  [xai-sdk] → [Grok API]                                     │
└─────────────────────────────────────────────────────────────┘
```

## ディレクトリ構造

```
spectra/
├── config.yaml          # 設定ファイル（モデル、人格プロンプト）
├── requirements.txt     # Python依存関係
├── .env                 # 環境変数（APIキー）※Git管理外
│
├── core/                # 脳（LLM + Context）
│   ├── __init__.py
│   └── main.py          # FastAPIサーバー
│
├── command/             # 指令室
│   └── console/         # Electronコンソール
│
├── channels/            # 対話経路
│   └── roblox/
│       ├── __init__.py
│       ├── router.py    # Pythonルーター
│       ├── GrokChat.server.lua
│       └── ChatClient.client.lua
│
├── scripts/             # 運用補助（Windows）
│   ├── register-task.ps1
│   └── register-tunnel-task.ps1
│
└── docs/
    ├── GrokスタックAIエージェント設計仕様書.md
    ├── implementation_plan.md
    └── reference_catalog.md
```

## クイックスタート

### 前提条件

- Python 3.10+
- Windows 10/11
- Cloudflareアカウント（Tunnel用）
- xAI APIキー

### 1. リポジトリのクローン

```powershell
mkdir C:\dev
cd C:\dev
git clone <repository-url> spectra
cd spectra
```

### 2. 仮想環境のセットアップ

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. 環境変数の設定

```powershell
@'
XAI_API_KEY=your-xai-api-key-here
SPECTRA_API_KEY=your-secret-key-here
'@ | Set-Content .env
```

| 変数 | 必須 | 説明 |
|------|------|------|
| `XAI_API_KEY` | ✅ | xAI API（Grok）にアクセスするためのキー |
| `SPECTRA_API_KEY` | ✅ | SPECTRAエンドポイントへのアクセスを制限するキー |

### 4. ローカルでテスト起動

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn core.main:app --host 127.0.0.1 --port 8000
```

別ターミナルで動作確認：

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}

curl -X POST http://127.0.0.1:8000/roblox \
  -H "Content-Type: application/json" \
  -d '{"prompt": "こんにちは"}'
```

## Cloudflare Tunnel 設定（Windows）

### 1. cloudflared のインストール

```powershell
winget install --id Cloudflare.cloudflared
```

または、公式の Windows バイナリを直接ダウンロードして PATH に配置します。
例: `https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe`

### 2. Cloudflare にログイン

```powershell
cloudflared tunnel login
```

### 3. トンネル作成

```powershell
# トンネル作成
cloudflared tunnel create spectra

# DNS設定（例: spectra.your-domain.com）
cloudflared tunnel route dns spectra spectra.your-domain.com
```

### 4. 設定ファイル作成

```powershell
# トンネルIDを確認
cloudflared tunnel list

# credentials を SYSTEM から参照できる場所へコピー
New-Item -ItemType Directory -Force "C:\\ProgramData\\cloudflared" | Out-Null
Copy-Item "$env:USERPROFILE\\.cloudflared\\<TUNNEL_ID>.json" "C:\\ProgramData\\cloudflared\\" -Force

# 設定ファイル作成（TUNNEL_IDを置き換え）
@'
tunnel: spectra
credentials-file: C:/ProgramData/cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: spectra.your-domain.com
    service: http://localhost:8000
  - service: http_status:404
'@ | Set-Content "C:\\ProgramData\\cloudflared\\config.yml"
```

### 5. トンネル起動（手動）

```powershell
cloudflared tunnel --config "C:\\ProgramData\\cloudflared\\config.yml" run spectra
```

Note: Windows の `cloudflared` は自動更新されないため、定期的に手動更新が必要です。

## 自動起動（Windows タスクスケジューラ）

PC起動時に自動でSPECTRAを起動するための設定。

### 1. タスク作成

- 名前: `SPECTRA Core`
- 実行ユーザー: 「ユーザーがログオンしているかどうかにかかわらず実行する」
- 「最上位の特権で実行する」にチェック

### 2. トリガー

- 「スタートアップ時」

### 3. 操作

- プログラム: `C:\dev\spectra\.venv\Scripts\python.exe`
- 引数: `-m uvicorn core.main:app --host 127.0.0.1 --port 8000`
- 開始 (作業フォルダー): `C:\dev\spectra`

### 4. 設定

- 「失敗したら再起動する」を有効化
- 「すでに実行中なら新しいインスタンスを開始しない」

### 5. スクリプトで登録（任意）

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-task.ps1
```

管理者 PowerShell で実行してください。

### 6. Tunnel（cloudflared）自動起動

Roblox など外部から常時アクセスするなら必須。SYSTEM 実行にする場合は
`C:\ProgramData\cloudflared` に credentials と `config.yml` を置く。

- タスク名: `SPECTRA Tunnel`
- トリガー: 「スタートアップ時」
- 実行ユーザー: SYSTEM（SID `S-1-5-18`）または自分のユーザー
- 実行コマンド（例）:
  - `C:\dev\bin\cloudflared.exe tunnel --config "C:\ProgramData\cloudflared\config.yml" run spectra`
- `config.yml` の `credentials-file` と `hostname` が一致していること

スクリプトで登録する場合（任意）:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-tunnel-task.ps1
```

## Roblox アダプタの使い方

### エンドポイント

```
POST https://spectra.siqi.jp/roblox
```

### リクエスト形式

```json
{
  "prompt": "ユーザーの入力テキスト",
  "previous_response_id": "前回のresponse_id（初回はnull）"
}
```

### レスポンス形式

```json
{
  "success": true,
  "text": "SPECTRAの応答テキスト",
  "response_id": "次回の継続用ID"
}
```

### Luaスクリプト

Roblox用のスクリプトは [`channels/roblox/`](channels/roblox/) フォルダに格納しています。

| ファイル | 配置場所 | 説明 |
|---------|---------|------|
| [`GrokChat.server.lua`](channels/roblox/GrokChat.server.lua) | ServerScriptService | サーバー側でSPECTRA APIを呼び出す |
| [`ChatClient.client.lua`](channels/roblox/ChatClient.client.lua) | StarterPlayerScripts | クライアント側でチャットを処理 |

詳細は [`channels/roblox/README.md`](channels/roblox/README.md) を参照。

### Roblox側の設定

1. **HttpService を有効化**: Game Settings → Security → Allow HTTP Requests
2. **API_KEY を設定**: `GrokChat.server.lua` の10行目を編集
3. **SpectraCommunicator**: Workspaceにキャラクターモデルを配置（バブル表示用）

## API リファレンス

### GET /health

ヘルスチェック用エンドポイント。

**レスポンス:**
```json
{"status": "ok"}
```

### POST /v1/think

汎用コアAPI。内部利用向け。

**リクエスト:**
```json
{
  "prompt": "入力テキスト",
  "session_id": "セッション識別子",
  "channel": "roblox"
}
```

**レスポンス:**
```json
{
  "response": "応答テキスト",
  "session_id": "セッション識別子",
  "response_id": "レスポンスID"
}
```

### POST /roblox

Roblox互換エンドポイント。

**リクエスト:**
```json
{
  "prompt": "入力テキスト",
  "previous_response_id": "前回のresponse_id（オプション）"
}
```

**レスポンス:**
```json
{
  "success": true,
  "text": "応答テキスト",
  "response_id": "次回継続用ID"
}
```

## 設定ファイル

### config.yaml

```yaml
# 使用するGrokモデル
model: grok-4-1-fast-non-reasoning

# 表示名
user_name: USER
avatar_name: SPECTRA
avatar_fullname: Spectra Communicator

# 人格プロンプト
system_prompt: >
  あなたはSpectraというAIアシスタントです。
  技術的で直接的なスタイルで簡潔に応答してください。
```

### .env

```bash
# 必須: xAI API（Grok）にアクセスするためのキー
XAI_API_KEY=your-xai-api-key

# 必須: SPECTRAエンドポイントへのアクセスを制限するキー
SPECTRA_API_KEY=your-secret-key
```

> **重要**: `SPECTRA_API_KEY` を設定しないと、URLを知っている人は誰でもAPIを使用でき、xAI APIの課金が発生します。

## トラブルシューティング

### タスクが起動しない

```powershell
Get-ScheduledTaskInfo -TaskName "SPECTRA Core"
Get-ScheduledTaskInfo -TaskName "SPECTRA Tunnel"
```

よくある原因:
- `.env` がない / `XAI_API_KEY` が空
- `C:\dev\spectra\.venv\Scripts\python.exe` が存在しない
- `C:\ProgramData\cloudflared\config.yml` がない
- `credentials-file` のパスが間違っている

### 502 Bad Gateway

- uvicorn サーバーが起動しているか確認
- `curl http://127.0.0.1:8000/health` でローカル確認

## ライセンス

Private - All rights reserved

## 関連ドキュメント

- [設計仕様書](docs/GrokスタックAIエージェント設計仕様書.md)
- [参照資料カタログ](docs/reference_catalog.md)
