# AG-UI + Google ADK メモ

更新日: 2025-11-22

## 1. 方針
- フロント側は Electron + Vite による **レトロターミナル風 GUI アプリケーション** (`app/`)。
- バックエンド側は **AG-UI 公式リポジトリ** に含まれる `ag_ui_adk` ミドルウェア（FastAPI + Google ADK Agent）を利用する (`server/`)。
- 現状のLLMは Gemini 2 系（Google Search 標準ツールを利用）。他プロバイダ対応は未実装で、検討中。
- MCP は未導入。採用するか、どのサーバを使うかは今後の検討項目。
- 設定は `settings.json` で一元管理し、SSOT (Single Source of Truth) を徹底する。

## 2. システム構成 (Architecture)

```
【Client: Electron】         【Server: Python (FastAPI)】          【Cloud】
  [UI Layer]                    [Agent Layer]
  (Renderer) <---(HTTP/SSE)---> (ADK Agent) <---(MCP Protocol)---> [MCP Servers]
      |                             |                                  (Filesystem, Command...)
      |                             +-----(Google GenAI SDK)---------> [Gemini API]
   [TerminalEngine]
   (Game Loop)
```

## 3. Google ADK ミドルウェア（公式サンプル）
1. **リポジトリ入手**
   ```bash
   git clone https://github.com/ag-ui-protocol/ag-ui.git ag-ui-upstream
   ```
   - `ag-ui-upstream/typescript-sdk/integrations/adk-middleware` に FastAPI サンプルがある。
   - 付属ドキュメント（`USAGE.md`, `CONFIGURATION.md`, `TOOLS.md`, `ARCHITECTURE.md`）が一次情報源。

2. **ローカル展開**
   - 推奨構成：`server/` に `app/`, `requirements.txt`, `.env.example` を配置（サンプル通り）。

3. **依存導入**
   ```bash
   cd server
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install .
   ```
   - サンプルは `pip install .`（または `pip install -e .`）でミドルウェア本体と依存を導入。

4. **環境変数**
   - `server/.env` ではなくルートの `.env` で一元管理。`GOOGLE_API_KEY=...` 等を設定。

5. **起動**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   - `server/main.py` で `add_adk_fastapi_endpoint(..., path="/agui")` を指定してあるため、`http://localhost:8000/agui` がクライアント用エンドポイントになる。

## 4. MCP連携（検討メモ）

- 現状: 未導入。どのMCPサーバ（filesystem/commands/etc.）を採用するか未定。
- 公式一次情報:
  - ADK MCP integration（StdioServerParameters + MCPToolset）。citehttps://cloud.google.com/blog/topics/developers-practitioners/use-google-adk-and-mcp-with-an-external-serverhttps://codelabs.developers.google.com/multi-agent-app-toolbox-adk
- 課題: 採用サーバと権限範囲、セキュリティポリシーを決める必要がある。

## 5. ディレクトリ構成

- `app/` – Electron クライアント (UI)
  - `src/renderer/` – UI ソースコード (HTML, CSS, TypeScript)。
  - `src/main/` – Electron メインプロセス。
  - `vite.config.ts` – ビルド設定。
- `server/` – FastAPI サーバー (Agent)
  - `main.py` – エントリーポイント。
  - `src/config.py` – 設定ローダー (Fail-Fast)。
- `settings.json` – 全体設定 (SSOT)。
- `.env` – 秘密情報 (API Key等)。

## 6. AG-UI イベント → DOM 更新方針（GUI）

| イベント | DOM 操作 / 表示 | 備考 |
|----------|----------------|------|
| `TextMessageStart` | `.text-line.text-line--assistant` を新規作成し、`#pane-output .text-scroll` に追加。アバター状態を `talk` に更新。 | 1メッセージ=1要素でストリーミング開始 |
| `TextMessageContent` | 直近の `.text-line--assistant` に `event.delta` を連結。スクロール位置を末尾へ。 | CLI の `process.stdout.write` 相当。加工なし。 |
| `TextMessageEnd` | アバター状態を `idle` に戻し、メッセージ行末に改行を付与。 | run終了を待たず、各メッセージごとに talk→idle を繰り返す。 |
| `ToolCallStart` | `.text-line.text-line--tool` を追加（例: `🔧 Tool call: ${event.toolCallName}`）。 | ツールイベントも出力欄に流す。 |
| `ToolCallArgs` / `ToolCallResult` | 同 `.text-line--tool` に追記 or 新規行で結果を表示（例: `🔍 Result: ...`）。 | 装飾は簡素に、テキストと同じ枠で表現。 |
| `RunError` / `onRunFailedEvent` | `.text-line.text-line--error` を追加（赤系表示）。 | 出力欄にエラーを流し、ログはロガー subscriber が別途記録。 |

## 7. 開発フロー
1. **サーバー起動**: `cd server && uvicorn main:app --reload`
2. **クライアント起動**: `cd app && npm run dev`
3. **設定変更**: `settings.json` を編集し、リロード（または再起動）で反映。

## テーマ構想メモ（現行と将来）

- 現行: 「Classic / Cobalt / Amber」の3テーマは**カラー差分のみ**で運用（枠の形状や丸みは変えない）
- 将来案: テーマごとに枠の丸み・レイアウト・スキャンライン強度などを差分化
  - 例: 角丸や別フォント、アンバーCRT風エフェクトなどを個別に付与
- 現時点では開発コストが見合わないためペンディング。カラー差分のみを維持する。

### Electron/app 設定ロードの将来拡張メモ
- 目標: 「開発者が .env で自由に設定」「エンドユーザー配布は常に安全（prod固定）」を両立する。
- 現状の課題: 本番パッケージで dotenv を読もうとする設計だと、.env 不在で dev 扱いになったり秘密情報混入リスクがある。
- 解決策（導入時に実装すること）:
  - dev 判定: `VITE_DEV_SERVER_URL` の有無で dev / prod を分岐。
  - dev のみ dotenv 読み込み: `if (process.env.VITE_DEV_SERVER_URL) loadEnv(...)`
  - APP_ENV などは「デフォルト prod」にする: `const APP_ENV = process.env.APP_ENV ?? 'prod'` （他のフラグも同様にデフォルト安全側）
  - 本番ビルドでは .env を同梱しない / dotenv を読まない。
  - 秘密情報は本番では環境変数注入 or 将来の設定画面で安全ストア保存に切り替える。
- 将来の接続設定（local/remote両対応）:
  - settings.json に `connection.mode: local|remote` と `localHost/localPort/remoteUrl` を追加し、mode に応じて接続先を組み立てる。
  - APIキーは将来、設定画面で入力→暗号化保存（safeStorage）する。ローカルモードはユーザーキー、リモートモードは公式キー or 不要。

---

## 付録：CLI → Electron GUI 移行の再現メモ（2025-11-19）
CLI テンプレの AG-UI を Electron + レトロターミナル UI に移植した際の主な問題と解決策（再現性確保のため記録）。

- メッセージ送信の公式準拠  
  - 誤り: `runAgent({ messages: [] })` で内部キューを空配列上書き → `new_message` エラー。  
  - 解決: `agent.messages.push(userMessage)` だけ行い、`runAgent()` に `messages` を渡さない。

- UI 層分離（AgentSubscriber パターン）  
  - コア（agent/logger）と UI（renderer/subscriber/animation）を分離。  
  - UI 更新は公式推奨の `AgentSubscriber` 実装で行う。

- Electron 開発フロー統合  
  - `vite-plugin-electron` 採用で `npm run dev` 一発起動（Vite+Electron ホットリロード）。  
  - `nodeIntegration:false`, `contextIsolation:true`, `sandbox:true` を維持し、必要なら preload で最小権限公開。

- CORS / Vite ルート設定  
  - FastAPI に CORS を追加（dev: localhost:5173 を許可）。  
  - `vite.config.ts` で `root: src/renderer`、entry を絶対パス指定、HTML の JS/CSS を相対パス化。

- アバター・テーマ  
  - Classic / Cobalt / Amber の3テーマを設定駆動化。  
  - モノクロ素材＋カラーオーバーレイ方式でテーマ切替を実現。

- パッケージング  
  - `electron-builder.yml` で dist-electron / dist/renderer のみ同梱、mac 言語を ja/en に削減、asar 有効。  
  - CSP 明示（img/media data/blob/https, connect localhost/127.0.0.1/https/ws/wss）、DevTools は dev のみ。

- 外部要因エラー  
  - Gemini API の一時的 503 overload は待機・再試行・モデル一時切替で回避（コード変更不要）。

総評: 公式ミドルウェア（AG-UI / Google ADK）への準拠を維持したまま GUI 化を完了。主要リスクは外部APIの過負荷のみ。
