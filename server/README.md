# ag_ui_adk (server)

FastAPI + Google ADK + AG-UI middleware bridge used by avatar-ui.

## 開発メモ
- 仮想環境: `python -m venv .venv && source .venv/bin/activate`
- 依存インストール: `pip install -e .`
- 起動: `uvicorn main:app --host 0.0.0.0 --port 8000`

## 設定
- `.env` に API キーなどの機密値
- `settings.json` (JSON5可) に UI/サーバー設定
