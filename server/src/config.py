import json
import os
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# プロジェクトルートのパス
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# 設定ファイルのパス
SETTINGS_PATH = ROOT_DIR / "settings.json"
DEFAULT_SETTINGS_PATH = ROOT_DIR / "settings.default.json"
ENV_PATH = ROOT_DIR / ".env"

# .env の読み込み (ルートディレクトリ)
load_dotenv(ENV_PATH)

def get_env(key: str) -> str:
    """環境変数を取得し、存在しない場合はエラーを発生させる (Fail-Fast)"""
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"Config Error: '{key}' is missing in .env")
    return val

def load_settings_json() -> Dict[str, Any]:
    """
    settings.json を読み込む。
    存在しない場合は settings.default.json を読み込んでデフォルト値とする。
    """
    # 優先順位: settings.json > settings.default.json
    if SETTINGS_PATH.exists():
        path_to_load = SETTINGS_PATH
        print(f"Loading config from: {SETTINGS_PATH}")
    elif DEFAULT_SETTINGS_PATH.exists():
        path_to_load = DEFAULT_SETTINGS_PATH
        print(f"Loading config from: {DEFAULT_SETTINGS_PATH} (Default)")
    else:
        raise RuntimeError(f"Config Error: Neither {SETTINGS_PATH} nor {DEFAULT_SETTINGS_PATH} found.")
    
    try:
        with open(path_to_load, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading settings from {path_to_load}: {e}")

# 設定のロード
_settings = load_settings_json()

# --- 環境変数 (.env) からの設定 ---
GOOGLE_API_KEY = get_env("GOOGLE_API_KEY")
AG_UI_AGENT_NAME = get_env("AG_UI_AGENT_NAME")
SERVER_HOST = get_env("SERVER_HOST")
SERVER_PORT = int(get_env("SERVER_PORT"))
CLIENT_PORT = int(get_env("CLIENT_PORT"))

# CORS Origins の自動生成
CORS_ORIGINS: List[str] = [
    f"http://localhost:{CLIENT_PORT}",
    f"http://127.0.0.1:{CLIENT_PORT}"
]

# --- JSON からの設定 ---
# 明示的なチェックは行わず、キーが存在しない場合は KeyError を発生させる (Fail-Fast)
_server_settings = _settings["server"]
_ui_settings = _settings["ui"]

LLM_MODEL = _server_settings["llmModel"]
SYSTEM_PROMPT = _server_settings["systemPrompt"]
LOG_MAX_BYTES = _server_settings["logMaxBytes"]
LOG_BACKUP_COUNT = _server_settings["logBackupCount"]
