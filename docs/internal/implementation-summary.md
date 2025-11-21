# CLI → Electron GUI 移行：問題点と解決法の総まとめ

## ✅ 完了した実装

CLI ベースの AG-UI チャットアプリケーションを、Electron + レトロターミナル UI に移行しました。

---

## 📋 問題点と解決法一覧

### 1. **`setMessages` 問題：空のメッセージ配列がサーバーに送信される**

#### 問題点
- クライアント側で独自の `messages` 配列を管理していた
- `agent.addMessage(userMessage)` を呼び出していたが、その後に `agent.runAgent({ messages: [] })` と空配列を渡していた
- 結果：サーバー側で `new_message` エラーが発生

#### 根本原因
- `HttpAgent.runAgent()` は内部の `this.messages` を自動的に使用する
- 外部から空の `messages` パラメータを渡すと、内部メッセージが無視される

#### 解決方法（公式準拠）
```typescript
// ❌ 間違い（旧実装）
const messages: Message[] = [];
messages.push(userMessage);
agent.addMessage(userMessage);
await agent.runAgent({ messages: [], ... });

// ✅ 正しい（現在の実装）
agent.messages.push(userMessage);
await agent.runAgent({ runId, threadId }, subscriber);
```

**公式準拠状態：✅ 完全準拠**
- `AbstractAgent.messages` への直接 push は公式実装と一致
- `runAgent()` に `messages` パラメータを渡さないのが正しい使い方

---

### 2. **UI層の分離設計：CLI コードと UI コードが混在**

#### 問題点
- `app/src/index.ts` に入力処理、AI通信、表示処理がすべて混在
- UI を変更するたびに AI 通信ロジックも影響を受ける可能性

#### 解決方法（公式準拠の AgentSubscriber パターン）
```
app/src/
├── core/                  ← AI 通信・ロガー（UI 非依存）
│   ├── agent.ts          ← HttpAgent インスタンス
│   └── loggerSubscriber.ts  ← ログ記録用 Subscriber
└── renderer/              ← Electron UI 層
    ├── index.html        ← レトロターミナル HTML
    ├── style.css         ← レトロスキン
    ├── main.ts           ← UI ロジック + agent 呼び出し
    ├── subscriber.ts     ← UI 更新用 Subscriber
    └── animation.ts      ← アバターアニメーション
```

**公式準拠状態：✅ 完全準拠**
- `AgentSubscriber` インターフェースを使った UI 更新
- グローバル subscriber（logger）とローカル subscriber（UI）の組み合わせ
- これは AG-UI 公式の推奨パターン

---

### 3. **Electron 統合：2コマンド開発（Vite + Electron）の複雑さ**

#### 問題点（codex の初期提案）
- `npm run dev:ui` で Vite を起動
- `npm run dev:electron` で Electron を起動
- 2つのターミナルが必要で、ホットリロードも効かない

#### 解決方法（統合アプローチ）
```json
// package.json
{
  "main": "dist-electron/index.js",
  "scripts": {
    "dev": "vite",           // ← 1コマンドで完結
    "build": "vite build",
    "package": "electron-builder"
  }
}
```

**使用技術：**
- `vite-plugin-electron`：Vite と Electron を統合
- `vite-plugin-electron-renderer`：**未使用**（Node統合を避けるため）。必要なら preload で最小権限を公開する方針。

**結果：**
- `npm run dev` だけで Electron + ホットリロード
- main プロセスと renderer プロセスが自動リロード

**公式準拠状態：✅ ベストプラクティス**
- Vite + Electron の標準的な統合手法

---

### 4. **Node.js API アクセス：セキュリティ優先で renderer をブラウザ相当の権限に固定**

#### 方針
- 危険な情報（検索クエリ等）を renderer から直接送出しないため、`nodeIntegration: false` / `contextIsolation: true` を維持。
- Node API が必要な場合は **preload + contextBridge** 経由で最小権限のエクスポートを行う（現在は何も公開していない）。

#### 現状設定（2025-11-20 時点）
```typescript
// app/src/main/index.ts
const win = new BrowserWindow({
  webPreferences: {
    nodeIntegration: false,   // Node API を封じる
    contextIsolation: true,   // renderer を隔離
  },
});
```

**結果：**
- renderer から `fs`/`process.env` などへは直接アクセス不可。
- 「危険データを誤送信させない」ことを最優先し、必要になった場合のみ preload でピンポイント公開する運用にする。

**公式準拠状態：✅ Electronセキュリティ推奨**
- デスクトップ専用でも、外部APIを扱う場合は `nodeIntegration: false` が推奨。必要最低限だけcontextBridgeで渡す。

---

### 5. **CORS エラー：Vite dev server から FastAPI サーバーへのリクエストが拒否**

#### 問題点
```
Access to fetch at 'http://localhost:8000/agui' from origin 'http://localhost:5173'
has been blocked by CORS policy
```

#### 原因
- Electron の renderer は Vite dev server（`http://localhost:5173`）経由で読み込まれる
- FastAPI サーバーが CORS ヘッダーを返していない

#### 解決方法
```python
# server/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**公式準拠状態：✅ FastAPI 公式の CORS 設定**
- 開発環境での標準的な対処法
- 本番環境では `allow_origins` を適切に制限

---

### 6. **Vite 設定の混乱：Entry point が見つからない**

#### 問題点
```
Could not resolve entry module "src/renderer/src/main/index.ts"
```

#### 原因
- `vite.config.ts` の `root` と `entry` パスが不整合
- HTML 内の `<script src>` パスが相対パスとして正しくない

#### 解決方法
```typescript
// vite.config.ts
export default {
  plugins: [
    electron({
      entry: resolve(__dirname, 'src/main/index.ts'),  // ← 絶対パス
      outDir: 'dist-electron',
    }),
  ],
  root: 'src/renderer',       // ← renderer のルート
  publicDir: 'src/renderer/assets',
  build: {
    outDir: 'dist/renderer',
  },
};
```

```html
<!-- src/renderer/index.html -->
<link rel="stylesheet" href="./style.css">  <!-- ← 相対パス -->
<script type="module" src="./main.ts"></script>
```

**公式準拠状態：✅ Vite + Electron の標準構成**

---

### 7. **Gemini API Overload：503 Service Unavailable**

#### 問題点
```
google.genai.errors.ServerError: 503 Service Unavailable
"message": "The model is overloaded. Please try again later."
```

#### 原因
- **これはコードの問題ではない**
- Google の Gemini API サーバーが一時的に過負荷状態

#### 対処方法
1. **1-2分待つ**：API が落ち着くのを待つ
2. **再試行する**：同じ入力をもう一度送信
3. **モデル変更（一時的）**：`gemini-1.5-flash` など安定モデルに切り替え

**公式準拠状態：N/A（外部 API の問題）**

---

## 🔍 リファクタリングの必要性チェック

### ✅ 必要なし：既に公式準拠

#### 1. **メッセージ管理**
- `agent.messages.push()` → ✅ 公式実装と同じ
- `agent.runAgent()` に `messages` を渡さない → ✅ 正しい

#### 2. **Subscriber パターン**
- `AgentSubscriber` インターフェース使用 → ✅ 公式推奨
- グローバル（logger）+ ローカル（UI） → ✅ 公式パターン

#### 3. **FastAPI サーバー**
```python
# 現在の実装
agent = ADKAgent(
    adk_agent=sample_agent,
    app_name="agents",
    user_id="cli_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)
add_adk_fastapi_endpoint(app, agent, path="/agui")
```
→ ✅ 公式 USAGE.md の推奨実装と完全一致

#### 4. **Electron 統合**
- `vite-plugin-electron` + `vite-plugin-electron-renderer` → ✅ ベストプラクティス
- `nodeIntegration: false` / `contextIsolation: true` → ✅ セキュリティ優先（必要時のみ preload で権限付与）

---

## 💡 今後の拡張ポイント（任意）

### オプション 1：環境変数の柔軟性向上
```python
# server/main.py
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not set, trying Application Default Credentials")
    # Google ADK が自動的に ADC を試す
```
**優先度：低**（現在の実装で十分動作する）

### オプション 2：Health Check エンドポイント
```python
@app.get("/health")
def health():
    return {"status": "ok", "agui_endpoint": "/agui"}
```
**優先度：低**（開発環境では不要）

### オプション 3：Live2D アバター統合
- 現在の `animation.ts` を拡張
- Live2D SDK を追加して口パク・表情制御

**優先度：中**（UI の高度化）

---

## 📊 最終評価

| 項目 | 状態 | 公式準拠 |
|------|------|---------|
| メッセージ管理 | ✅ | ✅ 完全準拠 |
| Subscriber パターン | ✅ | ✅ 完全準拠 |
| FastAPI 設定 | ✅ | ✅ 完全準拠 |
| Electron 統合 | ✅ | ✅ ベストプラクティス |
| CORS 設定 | ✅ | ✅ 公式推奨 |
| エラー処理 | ✅ | ✅ 適切 |

**総合評価：🎉 すべて公式準拠、リファクタリング不要**

---

## 🚀 次のステップ

1. **現在の状態をコミット・プッシュ**
2. **Live2D 統合の検討**（より高度なアバター表現）
3. **追加ツールの実装**（天気、ニュース、etc.）

---

生成日時：2025-11-19
