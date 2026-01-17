#!/usr/bin/env python3
"""
CLIアダプタ。
コアは別プロセスで動かし、ここはAPIを呼ぶだけにする。
"""
import json
import os
import urllib.error
import urllib.request

import yaml
from dotenv import load_dotenv

# .envを読み込み、ローカルの環境変数を使う。
load_dotenv()

config_path = os.getenv("SPECTRA_CONFIG", "config.yaml")
# コアと同じ設定ファイルから表示名だけ取得する。
with open(config_path, encoding="utf-8") as f:
    config = yaml.safe_load(f)

# コアAPIのURLと任意のAPIキー。
core_url = os.getenv("SPECTRA_CORE_URL", "http://127.0.0.1:8000/v1/think")
api_key = os.getenv("SPECTRA_API_KEY", "")
session_id = os.getenv("SPECTRA_SESSION_ID", "cli")

user_name = config.get("user_name", "USER")
avatar_name = config.get("avatar_name", "SPECTRA")


def _post(prompt: str) -> dict:
    # 入力をコアAPIへ送る。
    payload = {
        "prompt": prompt,
        "session_id": session_id,
        "channel": "cli",
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key

    req = urllib.request.Request(core_url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


while True:
    try:
        # シンプルな対話ループ。
        prompt = input(f"{user_name}: ")
        if not prompt:
            break
        try:
            data = _post(prompt)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8")
            print(f"Error: HTTP {exc.code}: {detail}")
            continue
        except urllib.error.URLError as exc:
            print(f"Error: {exc.reason}")
            continue

        print(f"{avatar_name}: {data.get('response', '')}")
    except (KeyboardInterrupt, EOFError):
        break
