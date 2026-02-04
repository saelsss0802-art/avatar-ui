# AVATAR UI

📖 [English](README.md)

デスクトップで動く、自分専用AIアバターのエージェントUI。  
Grok APIを使用したCore + Consoleアーキテクチャ。

![demo](docs/demo.gif)

[![GeckoTerminal](https://img.shields.io/badge/GeckoTerminal-Token%20Info-blue)](https://www.geckoterminal.com/solana/pools/ky7frWSyXRcHKvN7UXyPuhA5rjP1ypDPDJNEHxJubmJ)
[![Orynth](https://img.shields.io/badge/Orynth-Featured-green)](https://orynth.dev/projects/avatar-ui)

## 特徴

- **ローカル専用** – 自分のマシンで完結
- **承認フロー** – コマンド実行前に確認
- **自律ループ** – 目的 → 目標 → タスクの階層構造
- **拡張可能** – チャネル、ペルソナ、ツールを追加可能

## 使い方

1. Coreを起動 → Consoleが表示される
2. 目的を設定 → アバターが目標・タスクを提案
3. 各アクションを承認または拒否
4. アバターが実行し結果を報告

## クイックスタート

### 前提条件

- Python 3.10+
- Node.js 18+
- [xAI APIキー](https://x.ai/)

### セットアップ

```bash
git clone https://github.com/siqidev/avatar-ui.git
cd avatar-ui

# Python
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Console
cd command/console && npm install && cd ../..
```

### 環境変数

`.env` を作成:

```bash
XAI_API_KEY=your-xai-api-key
SPECTRA_API_KEY=your-secret-key
SPECTRA_CORE_URL=http://127.0.0.1:8000/v1/think
```

### 起動

```bash
# ターミナル1: Core
source .venv/bin/activate
python -m uvicorn core.main:app --host 127.0.0.1 --port 8000

# ターミナル2: Console
cd command/console && npm start
```

## 設定

`config.yaml` を編集:

```yaml
avatar:
  name: AVATAR

grok:
  model: grok-4-1-fast-non-reasoning
  temperature: 1.0
  daily_token_limit: 100000

system_prompt: |
  技術的で直接的なスタイルで簡潔に応答してください。
```

## ドキュメント

- [アーキテクチャ](docs/agent_design.md)
- [実装計画](docs/implementation_plan.md)

## サポート

AUIはAVATAR UIのコミュニティトークンです。

- [Orynth](https://orynth.dev/projects/avatar-ui)
- [GeckoTerminal](https://www.geckoterminal.com/solana/pools/ky7frWSyXRcHKvN7UXyPuhA5rjP1ypDPDJNEHxJubmJ)

Token CA (Solana): `63rvcwia2reibpdJMCf71bPLqBLvPRu9eM2xmRvNory`

> このセクションは情報提供のみを目的としています。

## セキュリティ

AVATAR UIはOS権限でコマンドを実行します。

| 原則 | 内容 |
|------|------|
| **ローカル専用** | 自分だけが使用する前提で設計 |
| **承認フロー** | コマンド実行前に内容を確認 |
| **APIキー管理** | `.env`をgit管理外に保持 |

> Discord/Roblox連携はv0.3.0で対応予定。

## ライセンス

MIT License

© 2025 SIQI (Sito Sikino)
