#!/usr/bin/env python3
"""
Identity Kernel - SPECTRAの人格核
Grok APIを通じて思考の「深さ」を実装するコア部品
"""
import os
import yaml
from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user, system

# .envからAPIキー等を読み込む
load_dotenv()

# 設定ファイルを読み込む
with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# APIキーで認証されたクライアントを生成
client = Client(api_key=os.getenv("XAI_API_KEY"))

# 会話インスタンスを作成
chat = client.chat.create(model=config["model"])

# 人格の種（システムプロンプト）を注入
chat.append(system(config["system_prompt"]))

# 入力（ここを書き換えてテスト）
chat.append(user("こんにちは、一言で自己紹介して"))

# 応答を生成して出力
response = chat.sample()
print(f"{config['avatar_name']}: {response.content}")
