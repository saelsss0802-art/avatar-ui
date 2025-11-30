# OSS配布用除外メモ
- 目的: OSS 配布時に含めない生成物・機密・内部資料を明確化する。
- 更新日: 2025-11-30

## 配布から除外するもの
- `.git/` 配下（`logs/` 含む）: Git のメタデータ。
- `.DS_Store`, `Thumbs.db`: OS が自動生成するキャッシュ。
- `.env`, `.env.local`: 秘密情報を含む環境変数ファイル。
- `settings.json5`: ローカル環境用設定（配布は `settings.default.json5` のみ）。
- `docs/internal/` 配下: 内部向けドキュメント。
- `app/node_modules/`: インストール済み依存物のコピー。
- `app/dist/`, `app/dist-electron/`, `build/`: ビルド成果物。
- `server/.venv/`, `venv/`, `env/`, `ENV/`: ローカル仮想環境。
- `__pycache__/`, `.pytest_cache/`, `*.py[cod]`, `*.so`: Python キャッシュ／バイトコード。
- `server/src/ag_ui_adk.egg-info`: パッケージング生成物。
- `server/uv.lock`（生成される場合）: 依存ロックの生成物。
- `server/logs/`, `app/logs/`, `*app_log*`, `*.log`: 実行時に生成されるログ。

## 配布に含める前提の設定例
- `.env.example` はサンプルとして配布する。
- `settings.default.json5` はデフォルト設定として配布・コメント付与対象。
