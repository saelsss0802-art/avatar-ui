# 参照資料カタログ

> GrokスタックAIエージェント設計仕様書の補足資料  
> 最終更新: 2026-01-13

---

## 概要

本ファイルは設計仕様書（`GrokスタックAIエージェント設計仕様書.md`）から分離した出典リストです。

### Status列の定義

| Status | 意味 |
|--------|------|
| ✅ 採用 | 設計に採用済み。要件または実装に反映 |
| 🔍 検討中 | 選択肢として検討中。比較検証または議論後に決定 |
| 🔍 参考 | 参考情報として保持。採用判断は未定 |
| ❌ 却下 | 検討の結果、採用しない |

---

## 1. Grokスタック基礎（xAI公式一次情報）

### API / 推論

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| XAI-CHAT-RESPONSES | ✅ 採用 | [docs/guides/chat](https://docs.x.ai/docs/guides/chat) | APIの推奨I/FはChat Responses。状態保持可能、サーバ側に履歴保存（30日） | 長期記憶は自前設計が必要 |
| XAI-RESPONSES-API | ✅ 採用 | [docs/guides/responses-api](https://docs.x.ai/docs/guides/responses-api) | Responses APIで状態保持。履歴30日保存 | SPECTRAの長期記憶は基盤側で持ち、APIは推論I/Oに集中 |
| XAI-REGIONAL-ENDPOINTS | 🔍 参考 | [docs/key-information/regions](https://docs.x.ai/docs/key-information/regions) | デフォルトはapi.x.ai。リージョン指定可能 | レイテンシ/規制要件に応じて接続先切替 |

### SDK / クライアント

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| XAI-SDK-PYTHON | 🔍 参考 | [xai-sdk-python](https://github.com/xai-org/xai-sdk-python) | 公式Python SDK。pip/uvでインストール可能。Python 3.10+が必要。同期/非同期クライアントを提供し、`XAI_API_KEY`環境変数を既定で参照 | Pythonでの検証・運用ツールを作る場合の標準クライアント。SDK前提機能の互換性管理が必要 |

### Function Calling / ツール

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| XAI-FUNCTION-CALLING | ✅ 採用 | [docs/guides/function-calling](https://docs.x.ai/docs/guides/function-calling) | ツール呼び出し最大200。tool_choice制御、並列呼び出し可能 | アダプタ層でツール群を統合、SPECTRA固有ツールは差し替え可能に |
| XAI-TOOLS-OVERVIEW | ✅ 採用 | [docs/guides/tools/overview](https://docs.x.ai/docs/guides/tools/overview) | サーバ側自律ツール呼び出し（agentic tool calling）機構あり | ADK/サブエージェントの有無は未確認だが、agentic tool callingは確認済み |
| XAI-SDK-TOOLS-VERSION | ✅ 採用 | [docs/guides/tools/overview](https://docs.x.ai/docs/guides/tools/overview) | xAI Python SDKでagentic tool calling APIを使うにはxai-sdk 1.3.1が必要 | Pythonでツール連携する場合はSDKバージョン固定が必要 |
| XAI-SDK-INLINE-CITATIONS | ✅ 採用 | [docs/guides/tools/overview](https://docs.x.ai/docs/guides/tools/overview) | Inline citationsはxai-sdk 1.5.0+が必要 | 引用付き応答をPython SDKで使う場合は1.5.0以上を前提にする |
| XAI-SEARCH-TOOLS | 🔍 参考 | [docs/guides/tools/search-tools](https://docs.x.ai/docs/guides/tools/search-tools) | Web/X検索のサーバサイドツール、agentic探索可能 | 最新情報取得はサーバ側ツールで完結、クライアント軽量化 |

### Voice

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| XAI-VOICE-OVERVIEW | ✅ 採用 | [docs/guides/voice](https://docs.x.ai/docs/guides/voice) | Grok Voice Agent APIはWebSocket（wss://api.x.ai/v1/realtime）でリアルタイム音声対話 | 音声ボディ向けに音声I/O経路を標準化 |
| XAI-VOICE-AGENT | ✅ 採用 | [docs/guides/voice/agent](https://docs.x.ai/docs/guides/voice/agent) | エフェメラルトークンでクライアント接続保護。ツール設定可能 | ブラウザ/配信クライアント向けに安全な接続フロー必要 |

### Collections / RAG

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| XAI-COLLECTIONS-OVERVIEW | ✅ 採用 | [docs/key-information/collections](https://docs.x.ai/docs/key-information/collections) | Collectionsはファイル+コレクションで構成、埋め込み検索前提 | 長期知識はCollectionsをRAG基盤として扱う可能性 |
| XAI-USING-COLLECTIONS | ✅ 採用 | [docs/guides/using-collections](https://docs.x.ai/docs/guides/using-collections) | ドキュメント永続保存、セマンティック検索可能。ファイル上限10万 | 知識基盤はコレクション容量と運用を考慮 |
| XAI-COLLECTIONS-API | 🔍 参考 | [docs/guides/using-collections/api](https://docs.x.ai/docs/guides/using-collections/api) | Collections APIには管理キーと権限が必要 | 管理キーは運用基盤側、クライアントから直接触れさせない |
| XAI-COLLECTIONS-SEARCH-TOOL | ✅ 採用 | [docs/guides/tools/collections-search-tool](https://docs.x.ai/docs/guides/tools/collections-search-tool) | Collections検索ツールはRAG用途想定 | 基盤側に「RAG検索」アダプタ、SPECTRA固有知識と分離 |
| XAI-COLLECTIONS-LIMITS | ✅ 採用 | [docs/key-information/collections](https://docs.x.ai/docs/key-information/collections) | 最大ファイルサイズ100MB、ファイル数上限10万、総容量100GB | 大容量アップロードは外部基盤側で管理、分割/圧縮の検討 |
| XAI-COLLECTIONS-API-REF | ✅ 採用 | [docs/collections-api](https://docs.x.ai/docs/collections-api) | 管理APIは`https://management-api.x.ai/v1`、検索は`https://api.x.ai`。管理キー/通常キーが分かれる | Roblox側から直接管理APIを叩かず、基盤側で中継する設計が安全 |

### Files / ドキュメント添付

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| XAI-SDK-FILES-VERSION | ✅ 採用 | [docs/guides/files](https://docs.x.ai/docs/guides/files) | Files APIをPython SDKで使うにはxai-sdk 1.4.0が必要 | ファイル添付/検索をPython SDKで使う場合はSDK 1.4.0以上を前提 |

### モデル / リリース

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| XAI-GROK-4-MODEL | ✅ 採用 | [docs/models/grok-4](https://docs.x.ai/docs/models/grok-4) | Grok 4のモデル名、コンテキスト長256,000 | 推論モデル選定と長文コンテキスト設計の基準 |
| XAI-RELEASE-NOTES | 🔍 参考 | [docs/release-notes](https://docs.x.ai/docs/release-notes) | API/ツールの更新履歴 | 機能追加のタイミングを前提知識に反映 |

### 料金（2026-01-09時点）

| ID | Status | 項目 | 料金 | 設計への示唆（推論） |
|----|--------|------|------|---------------------|
| XAI-PRICING-SEARCH-TOOLS | 🔍 参考 | Web/X Search | $5.00/1K calls | 検索は必要時のみ、キャッシュ/要約で抑制 |
| XAI-PRICING-COLLECTIONS-SEARCH | 🔍 参考 | Collections Search | $2.50/1K calls | RAG検索は頻度とコストを管理 |
| XAI-PRICING-DOCUMENTS-SEARCH | 🔍 参考 | Documents Search | $2.50/1K requests | Collectionsツールと区別が必要 |
| XAI-PRICING-LIVE-SEARCH-DEPRECATION | ❌ 却下 | Live Search | $25/1K sources | 2026-01-12廃止予定、依存設計は避ける |
| XAI-PRICING-VOICE | 🔍 参考 | Voice Agent | $0.05/min | 音声接続は必要時のみ、無音時は切断 |

---

## 2. MIA設計例

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| MIA-HOME | 🔍 参考 | [mia.miao.gg](https://mia.miao.gg/) | xAI技術+独自パイプラインのAIコンパニオン | xAI APIを基盤に、キャラ固有の中間処理（パイプライン）を持つ構成が有力 |
| MIA-FEATURES | 🔍 参考 | [mia.miao.gg](https://mia.miao.gg/) | 全プラットフォーム横断の中央集約メモリ、リアルタイム感情 | SPECTRAは感情不採用。「統合メモリ層」と「人格一貫性の状態管理」に置き換え |
| MIA-MULTI-PLATFORM | ✅ 採用 | [mia.miao.gg](https://mia.miao.gg/) | VRChat, Minecraft, Discord対応 | SPECTRAのCLI/Live2D/VRM/Roblox差し替えは「単一人格の多面展開」設計に近い |
| MIA-ALPHA-ROADMAP | 🔍 参考 | [mia.miao.gg](https://mia.miao.gg/) | Alpha V0.1.2 / 2026年1月。記憶・感情・音声・能動的呼びかけを先行投入 | 初期CLI段階で記憶・能動性・一貫性を先に設計するとボディ差し替えが容易 |
| MIA-VOICE | 🔍 参考 | [mia.miao.gg](https://mia.miao.gg/) | 音声対話が初期から主要機能 | 音声I/Oは基盤側の標準アダプタに含めるべき |
| MIA-BUG-BOUNTY-SCOPE | ✅ 採用 | [mia.miao.gg/bug-bounty](https://mia.miao.gg/bug-bounty) | メモリ（公開/非公開）、音声統合、APIエンドポイントがスコープ | 「公開/非公開メモリ分離」「音声統合」「API境界」を最初から設計に含める |
| MIA-UPDATES-X | 🔍 参考 | [x.com/miao_xAI](https://x.com/miao_xAI) | X本体の一次情報 | ユーザー収集後に反映 |
| MIA-UPDATES-X-MIRROR | 🔍 参考 | [twstalker.com/miao_xAI](https://twstalker.com/miao_xAI) | MIA v0.1 Alpha公開、音声不具合/感情更新バグ/認証方式/インフラ増強などの運用課題 | 初期リリース時は「音声I/O」「認証/セキュリティ」「インフラ耐性」がボトルネック |
| MIA-ARCH-DIAGRAM | ✅ 採用 | 提供画像（Miao_Architecture.png） | 音声I/O→Grok Voice API→Context Manager構成。VRChat OSCでアバター操作 | SPECTRAは感情状態を持たないため、Context Managerは「人格一貫性/記憶/視覚文脈」に置き換え |

---

## 3. Roblox（NPC / AI基盤）

### キャラクター制御

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-HUMANOID | ✅ 採用 | [Humanoid](https://create.roblox.com/docs/ja-jp/reference/engine/classes/Humanoid) | キャラクター機能を付与する基本要素 | NPCの身体制御はHumanoid前提 |
| ROBLOX-ANIMATOR | ✅ 採用 | [Animator](https://create.roblox.com/docs/ja-jp/reference/engine/classes/Animator) | アニメーションの再生と複製を担当 | 行動表現はAnimator/AnimationTrackを標準経路に |
| ROBLOX-ANIMATION | 🔍 参考 | [Animation](https://create.roblox.com/docs/ja-jp/reference/engine/classes/Animation) | アニメーションアセットを参照 | 動作表現は「資産参照→ロード」の流れに揃える |
| ROBLOX-ANIMATIONTRACK | 🔍 参考 | [AnimationTrack](https://create.roblox.com/docs/ja-jp/reference/engine/classes/AnimationTrack) | 再生・速度・ループ・優先度を制御 | 行動アダプタは「再生/停止/速度」制御を抽象化 |

### 移動 / 経路探索

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-PATHFINDING-GUIDE | ✅ 採用 | [pathfinding](https://create.roblox.com/docs/ja-jp/characters/pathfinding) | 障害物・危険領域を避けて移動。CreatePathのエージェント設定が重要 | NPC移動は「制限値」「エージェント設定」「コスト設計」を前提に |
| ROBLOX-PATHFINDING-SERVICE | ✅ 採用 | [PathfindingService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/PathfindingService) | 二点間の論理的経路を見つける中核サービス | 移動アダプタはPathfindingServiceを標準利用 |
| ROBLOX-PATH | 🔍 参考 | [Path](https://create.roblox.com/docs/ja-jp/reference/engine/classes/Path) | ComputeAsync→GetWaypoints→Blockedイベントで再計算 | 移動は「経路→ウェイポイント→再計算」のループで統合 |

### 環境 / 知覚

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-WORKSPACE | 🔍 参考 | [Workspace](https://create.roblox.com/docs/ja-jp/reference/engine/classes/Workspace) | 3Dオブジェクトを収容し描画・物理相互作用に参加 | 知覚・行動対象はWorkspace階層を基準に |
| ROBLOX-RAYCASTPARAMS | 🔍 参考 | [RaycastParams](https://create.roblox.com/docs/ja-jp/reference/engine/datatypes/RaycastParams) | レイキャスト操作のフィルタ/除外/衝突グループ等を指定 | 視覚/環境認識はRaycastParamsで制御 |

### インタラクション

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-PROXIMITYPROMPT | ✅ 採用 | [ProximityPrompt](https://create.roblox.com/docs/ja-jp/reference/engine/classes/ProximityPrompt) | 距離/視線/入力条件で対話を促す | NPCの対話トリガーはProximityPromptを標準候補に |
| ROBLOX-CLICKDETECTOR | 🔍 参考 | [ClickDetector](https://create.roblox.com/docs/ja-jp/reference/engine/classes/ClickDetector) | BasePart/Modelに対するクリック入力 | クリック型インタラクションの標準アダプタに |
| ROBLOX-COLLECTIONSERVICE | 🔍 参考 | [CollectionService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/CollectionService) | タグでインスタンスを整理・検索 | NPCが関与する対象をタグで抽象化 |

### チャット / テキスト

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-TEXTCHATSERVICE | ✅ 採用 | [TextChatService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextChatService) | 体験内テキストチャットの中核サービス | NPCの発話はTextChatService前提 |
| ROBLOX-TEXTCHANNEL | ✅ 採用 | [TextChannel](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextChannel) | SendAsync/DisplaySystemMessageで送信、MessageReceivedで受信 | NPC発話はTextChannel経由 |
| ROBLOX-TEXTSERVICE | 🔍 参考 | [TextService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextService) | FilterStringAsync等のフィルタ系API | 外部LLM出力はテキストフィルタ設計を組み込む |
| ROBLOX-LEGACY-CHAT-GUIDE | ❌ 却下 | [legacy-chat-system](https://create.roblox.com/docs/ja-jp/chat/legacy/legacy-chat-system) | TextChatServiceが推奨。レガシーは非推奨 | レガシーには依存しない |
| ROBLOX-TEXTCHAT-OVERVIEW | ✅ 採用 | [in-experience-text-chat](https://create.roblox.com/docs/chat/in-experience-text-chat) | TextChatServiceはメッセージのフィルタリング/モデレーション/権限管理を担う | NPC発話はTextChatServiceの規約・フィルタを前提に設計 |
| ROBLOX-TEXTCHANNEL-PARENTING | ✅ 採用 | [in-experience-text-chat](https://create.roblox.com/docs/chat/in-experience-text-chat) | TextChannelはTextChatService配下に置く必要がある。既定でRBXGeneral/RBXSystemが自動生成される | NPC用の専用チャンネルを作る場合も親子関係を厳守 |
| ROBLOX-TEXTCHANNEL-SENDASYNC | ✅ 採用 | [TextChannel](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextChannel) | SendAsyncはLocalScript/RunContext.Client限定。metadataは200文字まで | NPC送信はクライアント実行経路を設計する必要 |
| ROBLOX-TEXTCHANNEL-DISPLAYSYSTEM | ✅ 採用 | [TextChannel](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextChannel) | DisplaySystemMessageはクライアント限定。対象ユーザーのみに表示、フィルタ/ローカライズなし | サーバからの一斉配信は別経路設計が必要 |
| ROBLOX-TEXTCHANNEL-SHOULDDELIVER | ✅ 採用 | [in-experience-text-chat](https://create.roblox.com/docs/chat/in-experience-text-chat) | ShouldDeliverCallbackはサーバーのみで定義し、各クライアントへの配信可否を判定 | NPC発話の配信制御はサーバ側コールバックで統制する |
| ROBLOX-TEXTCHAT-FILTERING | ✅ 採用 | [in-experience-text-chat](https://create.roblox.com/docs/chat/in-experience-text-chat) | SendAsyncにはフィルタ処理が組み込まれており、TextChatServiceが自動フィルタを行う | NPC発話もフィルタ結果に合わせた出力設計が必要 |
| ROBLOX-TEXTSOURCE | 🔍 参考 | [TextSource](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextSource) | TextChannel内のスピーカー（ユーザー）を表す。AddUserAsyncで作成。UserId読み取り専用。「将来的に負の数を渡すことで非ユーザーエンティティのサポートが追加される可能性がある」と記載 | **現時点ではNPC名義での発話には使用不可**。将来のAPI更新を待つ必要 |
| ROBLOX-DISPLAYBUBBLE | 🔍 検討中 | [bubble-chat](https://create.roblox.com/docs/chat/bubble-chat) | TextChatService:DisplayBubble(character, message)でNPCの頭上にバブル表示可能。クライアント側のみで動作（LocalScript/RunContext.Client必須）。**チャットログには残らない** | NPC発話の選択肢の一つ。視覚表現は優秀だが、見逃し問題あり。チャット併用やカスタムUIとの比較が必要 |
| ROBLOX-ONBUBBLEADDED | 🔍 検討中 | [bubble-chat](https://create.roblox.com/docs/chat/bubble-chat) | TextChatService.OnBubbleAddedコールバックでバブルの外観をカスタマイズ可能 | DisplayBubble採用時はSpectra専用のバブルスタイル（色/フォント）を設定可能 |

### NPC AI / テキスト生成

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-TEXTGENERATOR | 🔍 参考 | [TextGenerator](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextGenerator) | Roblox組み込みLLM。SystemPrompt/Temperature/TopP/Seed設定可能。GenerateTextAsyncでテキスト生成。ContextTokenで会話状態維持。レート制限100 req/min（ユーザー数でスケールアップ） | **xAI Grok APIの代替候補**。Roblox内完結のためHttpService制限を回避可能。ただしモデル選択不可、カスタマイズ性に制限あり。Spectraの人格表現に十分かは要検証 |
| ROBLOX-TEXTGENERATOR-CONTEXTTOKEN | 🔍 参考 | [TextGenerator](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextGenerator) | ContextTokenは会話履歴の要約を含むトークン。次リクエストに渡すことで会話状態を復元 | 短期記憶はContextTokenで維持可能。ただし長期記憶（Deep Context）は別途設計が必要 |
| ROBLOX-TEXTGENERATOR-JSONSCHEMA | 🔍 参考 | [TextGenerator](https://create.roblox.com/docs/ja-jp/reference/engine/classes/TextGenerator) | JsonSchemaパラメータで構造化出力を強制可能（json-schema.org準拠） | Function Calling相当の構造化応答が可能。行動決定や意思決定の出力形式を統一できる |

### 実行環境 / 通信

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-RUNSERVICE | 🔍 参考 | [RunService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/RunService) | IsClient/IsServer/IsStudioで実行コンテキスト判定 | 処理はサーバ/クライアントで明確に分ける |
| ROBLOX-REMOTEEVENT | ✅ 採用 | [RemoteEvent](https://create.roblox.com/docs/ja-jp/reference/engine/classes/RemoteEvent) | 非同期・非ブロッキングの一方向通信 | NPC制御の入力/出力はRemoteEvent経由で分離 |
| ROBLOX-SERVERSCRIPTSERVICE | ✅ 採用 | [ServerScriptService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/ServerScriptService) | サーバ専用スクリプトの格納先、複製されない | NPCロジックはServerScriptServiceに集約 |
| ROBLOX-REPLICATEDSTORAGE | ✅ 採用 | [ReplicatedStorage](https://create.roblox.com/docs/ja-jp/reference/engine/classes/ReplicatedStorage) | サーバ/クライアントで共有するModuleScript等に適する | 共通設定・プロトコル定義はReplicatedStorageに |
| ROBLOX-PLAYERS | 🔍 参考 | [Players](https://create.roblox.com/docs/ja-jp/reference/engine/classes/Players) | 現在接続されているPlayerオブジェクトを含むサービス | NPCの対話相手や権限判定の入口 |

### 外部連携 / 永続化

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-HTTPSERVICE | ✅ 採用 | [HttpService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/HttpService) | HTTPリクエスト送信、JSON操作。HttpEnabled必要 | 外部AI連携はHttpServiceを標準経路に |
| ROBLOX-HTTPSERVICE-HTTPENABLED | ✅ 採用 | [HttpService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/HttpService) | HttpEnabledがtrueのときのみ外部HTTPリクエストが送信可能 | 外部AI連携は起動時にHttpEnabledを前提条件として明記 |
| ROBLOX-HTTPSERVICE-LIMITS | ✅ 採用 | [HttpService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/HttpService) | 外部HTTPは500 req/min、Open Cloudは2500 req/minの制限 | バッチ/キュー処理とリトライ制御が必須 |
| ROBLOX-HTTPSERVICE-REQUESTASYNC | ✅ 採用 | [HttpService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/HttpService) | RequestAsyncはhttp/httpsのみ。ヘッダー指定に制限あり | API連携は許可ヘッダー前提で設計する |
| ROBLOX-OPEN-CLOUD-RATELIMITS | ✅ 採用 | [http-service](https://create.roblox.com/docs/cloud-services/http-service) | Open Cloudはサーバーごとに2500 req/min。一般HTTP 500 req/minとは別枠で、超過時は送信が停止する | Open Cloud連携は専用のリトライ/バックオフ戦略が必要 |
| ROBLOX-DATASTORE | ✅ 採用 | [DataStoreService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/DataStoreService) | 持続的なデータストレージへのアクセス | 長期記憶の保管場所として利用 |
| ROBLOX-MEMORYSTORE | 🔍 参考 | [MemoryStoreService](https://create.roblox.com/docs/ja-jp/reference/engine/classes/MemoryStoreService) | 急速に変化するデータを扱うMemoryStore | 短期共有状態やキューはMemoryStoreで |
| ROBLOX-MEMORYSTORE-EXTENDED-LIMITS | ✅ 採用 | [memory-stores-now-offers-extended-service-support](https://devforum.roblox.com/t/memory-stores-now-offers-extended-service-support/3774857) | デフォルト上限: Request Units = 1000 + (CCU x 120) / 分、Storage = 64KB + (D8PCU x 1.2KB)。超過分はExtended Servicesで拡張可能 | RU/容量の予算化とピークCCU/D8PCUを前提にスケーリング設計 |
| ROBLOX-MEMORYSTORE-QUOTA-UPDATE | ✅ 採用 | [memory-stores-service-quota-update](https://devforum.roblox.com/t/memory-stores-service-quota-update/2062296) | Request Unit制導入。経験全体のRU上限は1000 + 100 x CCU / 分。大半のAPIは1RU、GetRangeAsync/ReadAsyncは返却件数分RU消費。単一Queue/SortedMapは100,000 RU/分。単一構造体は最大100万アイテム・総サイズ100MB | 2025の拡張サービスで基礎RUが更新済みのため、上限値は最新情報と整合確認が必要。高コストAPIの頻度制御が必須 |
| ROBLOX-MEMORYSTORE-RETRY | ✅ 採用 | [memorystoreservice-internal-errors](https://devforum.roblox.com/t/i-keep-getting-memorystoreservice-internal-errors/3879189) | MemoryStoreServiceのInternalErrorは発生しうる想定で、pcallと指数バックオフの再試行が推奨される | 重要経路はリトライ/バックオフとフェイルセーフを設計に組み込む |
| ROBLOX-MEMORYSTORE-TTL-MAX | ✅ 採用 | [memory-stores-do-not-support-31-day-month-use-cases](https://devforum.roblox.com/t/memory-stores-do-not-support-31-day-month-use-cases/1651607/3) | MemoryStoreの最大有効期限は45日へ更新済み | ランキング等は「45日以内で期限設計」が必須 |
| ROBLOX-MEMORYSTORE-SIZE-QUOTA-LOOKBACK | ✅ 採用 | [memory-stores-size-quota-now-traces-back-to-8-days](https://devforum.roblox.com/t/memory-stores-size-quota-now-traces-back-to-8-days/2312662) | サイズクォータのトレースバック期間が8日に延長。長い有効期限と大量データの組み合わせはリスクが高く、最短の有効期限設定が推奨 | TTLは用途別に短/中/長を定義。大量データは短TTL+明示削除、少量のみ長TTLに限定 |
| ROBLOX-MEMORYSTORE-EXPERIENCE-WIDE | ✅ 採用 | [a-memory-store-size-quota-overflow-affects-all-memory-stores](https://devforum.roblox.com/t/a-memory-store-size-quota-overflow-affects-all-memory-stores/2025741) | MemoryStoreのサイズクォータは経験全体で共有される（経験全体のメモリ制限に到達すると全MemoryStoreに影響） | 監視は個別構造体だけでなく経験全体の使用量として捉える必要がある |
| ROBLOX-MEMORYSTORE-OBSERVABILITY-DASHBOARD | ✅ 採用 | [memorystoreservice-sortedmap-requests-failing](https://devforum.roblox.com/t/memorystoreservice-sortedmap-requests-failing/3653528) | Memory Stores Observability Dashboardでリアルタイムのリクエスト統計が確認できる | 運用監視の一次情報源として、アラート設計の根拠にできる |
| ROBLOX-MEMORYSTORE-ALERT-RULES | 🔍 参考 | [memorystoreservice-sortedmap-requests-failing](https://devforum.roblox.com/t/memorystoreservice-sortedmap-requests-failing/3653528) | モデレーター回答で、監視指標（タイムアウト/失敗率/429/500s等）を確認し、観測ダッシュボードと照合する運用が示唆される | ダッシュボードでRU逼迫・失敗率増を検知したら、TTL短縮/件数削減/書込頻度抑制を自動適用する運用設計が必要 |
| ROBLOX-MEMORYSTORE-EVICTION-POLICY | ✅ 採用 | [document-memory-store-eviction-policy](https://devforum.roblox.com/t/document-memory-store-eviction-policy/2493002) | MemoryStoreのエビクションはTTLベース。期限切れ後に削除され、メモリ上限到達時は新規書き込みが失敗する。期限切れ or RemoveAsyncでのみ解放される | TTLはフェイルセーフ扱いにし、処理完了後はRemoveAsyncで即時削除。書込失敗時はDataStore等の保険ルートを用意 |
| ROBLOX-MEMORYSTORE-GETSIZE | ✅ 採用 | [public-beta-memory-stores-getsize](https://devforum.roblox.com/t/public-beta-memory-stores-sorted-map-queue-getsize/3678891) | MemoryStoreSortedMap/QueueにGetSize()が追加され、データ構造内のアイテム数を取得可能。HashMapはパーティション分割のため対象外 | 監視指標として「件数の直接取得」が可能に。HashMapは件数監視を別設計にする必要 |
| ROBLOX-OPEN-CLOUD-MEMORYSTORES | 🔍 参考 | [open-cloud-memory-stores-api-beta](https://devforum.roblox.com/t/open-cloud-memory-stores-api-beta/3041236) | Open CloudからMemoryStoreのQueue/SortedMapを外部アプリで操作可能。Flush/GetFlushエンドポイント追加 | 運用監視や緊急時の外部メンテ（クリア/調査）経路を用意できる |
| ROBLOX-OPEN-CLOUD-DATASTORES | 🔍 参考 | [usage-data-stores](https://create.roblox.com/docs/ja-jp/cloud/guides/usage-data-stores) | 外部からデータストアにアクセス可能。ユニバースID必須 | 外部運用ツールはOpen Cloud経由で統合 |
| ROBLOX-OPEN-CLOUD-API-KEYS | 🔍 参考 | [api-keys](https://create.roblox.com/docs/ja-jp/cloud/auth/api-keys) | x-api-keyヘッダー認証。権限スコープ/IP制限可能 | 鍵管理と権限分離を基盤設計に組み込む |
| ROBLOX-DATASTORES-GUIDE | ✅ 採用 | [data-stores](https://create.roblox.com/docs/ja-jp/scripting/data/data-stores) | データストアは体験内で一貫して共有され、異なるサーバー上の場所からも同一データにアクセス可能。外部アクセスはOpen Cloudを利用 | 記憶の正本はDataStoreで維持し、外部運用はOpen Cloud経由に整理 |
| ROBLOX-DATASTORES-STUDIO | ✅ 採用 | [data-stores](https://create.roblox.com/docs/ja-jp/scripting/data/data-stores) | Studioでは既定でデータストアにアクセスできず、Security設定で有効化が必要。Studioは本番データと同じデータストアを参照するため、テスト用に分離が推奨 | 検証用Experienceを分離し、誤上書きを防ぐ運用ルールが必要 |
| ROBLOX-DATASTORES-SERVERONLY | ✅ 採用 | [data-stores](https://create.roblox.com/docs/ja-jp/scripting/data/data-stores) | データストアはサーバー側Scriptでのみアクセス可能。LocalScriptからのアクセスはエラー | 記憶I/Oはサーバ専用に設計し、クライアントは経由させない |

### サーバー間通信 / サーバー種別

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| ROBLOX-MESSAGINGSERVICE-LIMITS | ✅ 採用 | [enhanced-messagingservice-limits](https://devforum.roblox.com/t/enhanced-messagingservice-limits/2835576) | メッセージサイズ1KB。送信: 600 + 240 * players / 分。受信(トピック): 40 + 80 * servers / 分。受信(全体): 400 + 200 * servers / 分。購読数: 20 + 8 * players。購読リクエスト: 240 / 分 | サーバー間通知は間引き/集約/キュー化を前提にし、ピーク時に破綻しない設計に |
| ROBLOX-MESSAGINGSERVICE-PUBSUB-REALTIME | ✅ 採用 | [messagingservice-release](https://devforum.roblox.com/t/messagingservice-release/254462) | MessagingServiceはサーバー間通信を「near real-time(<1s)」で提供。PublishAsyncはトピックに送信、SubscribeAsyncはトピックを購読し受信時にコールバック | トピック単位のpub/sub前提。通知・イベント同期など「瞬時性は欲しいが厳密性は不要」な用途に限定する |
| ROBLOX-MESSAGINGSERVICE-DELIVERY-BEST-EFFORT | ✅ 採用 | [messagingservice-failure-cases](https://devforum.roblox.com/t/messagingservice-failure-cases/3112794) | 配送保証や失敗検知の方法はない。非クリティカル用途に限定し、重要データはDataStore等を使用。PublishAsyncはpcallでエラー捕捉可能（レート制限/不正データ/サービス不可） | 「ベストエフォート通知バス」として設計。再試行/バックオフ/冪等化/代替経路の併設が必須 |
| ROBLOX-TELEPORT-SERVER-TARGET | ✅ 採用 | [teleporting](https://create.roblox.com/docs/projects/teleporting) | TeleportOptionsで特定サーバー指定が可能。ServerInstanceIdで公開サーバー、ReservedServerAccessCodeで予約サーバー、ShouldReserveServer=trueで新規予約サーバー作成。未指定の場合はマッチメイクされた公開サーバーへ | ReservedServerAccessCodeは入室用のユニークコード。発行→保存→配布→更新→失効のライフサイクル設計が必須 |
| ROBLOX-TELEPORT-DATA-SECURITY | ✅ 採用 | [teleporting](https://create.roblox.com/docs/projects/teleporting) | TeleportOptions:SetTeleportData()は基本的な非セキュアデータ用。安全なデータは送らない | アクセスコードや認可情報はTeleportDataに載せず、サーバー側で管理してTeleportOptionsにセットする |
| ROBLOX-TELEPORT-SERVER-SIDE | ✅ 採用 | [teleporting](https://create.roblox.com/docs/projects/teleporting) | TeleportAsyncはサーバー側スクリプトからのみ呼び出せる（クライアントはTeleportを使えるが非推奨） | 予約サーバー誘導やアクセスコードの発行/管理はサーバー側に閉じる |
| ROBLOX-TELEPORT-RETRY | ✅ 採用 | [teleporting](https://create.roblox.com/docs/projects/teleporting) | TeleportAsyncはpcall推奨。特に予約サーバー関連の失敗は再試行が有効。開始済みでも失敗し得て、その場合はTeleportService.TeleportInitFailedが発火 | 失敗時は予約サーバーを再発行し、アクセスコードを更新するフローを用意する |
| ROBLOX-RESERVED-SERVER-SINGLETON-FLOW | ✅ 採用 | [teleporting](https://create.roblox.com/docs/projects/teleporting) | ReservedServerAccessCodeを指定して常に同一の予約サーバーへテレポートできる | 単一性を担保するには、最新アクセスコードをサーバー側で保持し、失効時のみ再発行する運用が必要 |
| ROBLOX-PRIVATE-SERVER-FAQ | 🔍 参考 | [private-vip-server-faq](https://en.help.roblox.com/hc/en-us/articles/205345050-Private-VIP-Servers-FAQ) | Private Serverは体験側で有効化が必要。ユーザーがRobuxで購入し、Serversタブから作成/設定。最大50ユーザーの許可や接続リスト許可、招待リンク作成が可能。月額課金が発生 | VIP/Privateはユーザー課金・参加制限・招待運用が前提のため、常駐型NPC運用とは別設計が必要 |
| ROBLOX-PRIVATE-SERVER-MIN-REQ | ✅ 採用 | [private-vip-servers-faq](https://en.help.roblox.com/hc/nl/articles/205345050-Private-VIP-Servers-FAQ) | Private Serverの前提: 体験側でPrivate Serversが有効化されていること。ユーザーはServersタブから購入し、名前設定・招待リンク作成・参加許可（最大50ユーザー or Connections）を設定できる。月額サブスクで維持 | Private/VIPはユーザー主導の購入/設定フローが前提。運用設計は「ユーザーが設定できる範囲」を越えないことが必須 |
| ROBLOX-SERVER-TYPES-DIFF | ✅ 採用 | [teleporting](https://create.roblox.com/docs/projects/teleporting), [private-vip-server-faq](https://en.help.roblox.com/hc/en-us/articles/205345050-Private-VIP-Servers-FAQ) | Reserved ServerはReservedServerAccessCodeで指定してテレポートする。Private Serverは体験側で有効化が必要で、ユーザーがRobuxで購入し、最大50ユーザー許可や招待リンク作成が可能（サブスク型） | Reservedは開発側がアクセスコード制御、Privateはユーザー管理と課金/招待が中心。用途の違い（単一性/運用コントロール vs 参加者管理/収益性）で選定 |

---

## 4. Live2D

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| LIVE2D-CUBISM-SDK | ✅ 採用 | [sdk/about](https://www.live2d.com/en/sdk/about/) | Cubism SDKはモデル/アニメーションをアプリ上で描画するSDK | SDK選定（Unity/Web/Native）を先に決め、出力アダプタを分岐 |
| LIVE2D-UNITY-SDK | 🔍 参考 | [cubism-sdk-for-unity](https://docs.live2d.com/en/cubism-sdk-manual/cubism-sdk-for-unity/) | Unity向けSDK。Cubism Coreは配布パッケージに含まれる | 配布パッケージ前提で依存関係を管理 |
| LIVE2D-WEB-SDK | 🔍 参考 | [cubism-sdk-for-web](https://docs.live2d.com/en/cubism-sdk-manual/cubism-sdk-for-web/) | Web向けSDK。配布パッケージにCoreが含まれる | 配信/デスクトップ用途でWeb実装する場合の選択肢 |
| LIVE2D-LICENSE | ✅ 採用 | [sdk/license](https://www.live2d.com/en/sdk/license/) | 初期費用なし。商用リリース時は契約必要（個人・小規模事業者は免除） | OSS公開時にライセンス条件を明記、配布形態に注意 |
| LIVE2D-RUNTIME-INTEGRATION | 🔍 参考 | [cubism-sdk-for-unity](https://docs.live2d.com/en/cubism-sdk-manual/cubism-sdk-for-unity/) | CoreはGitHub非公開、配布パッケージに含まれる | 依存をOSS側に含めない構成で配布手順を分離 |

---

## 5. VRM

| ID | Status | URL | 要約（事実） | 設計への示唆（推論） |
|----|--------|-----|-------------|---------------------|
| VRM-SPEC | ✅ 採用 | [vrm.dev/en/vrm1](https://vrm.dev/en/vrm1/) | VRM 1.0は2022年9月に正式公開 | VRMボディ採用時は1.0仕様を前提に |
| VRM-CONSORTIUM | 🔍 参考 | [vrm-consortium.org/en](https://vrm-consortium.org/en/) | VRMはglTF2.0ベース。標準化された骨格・表情・メタ情報・ライセンス設定 | 基盤化と相性が良く、人格/ライセンス管理も設計に含める |
| VRM-UNIVRM | ✅ 採用 | [github.com/vrm-c/UniVRM](https://github.com/vrm-c/UniVRM) | Unity向け公式実装。VRM 1.0/0.x対応、ランタイム入出力可能 | Unity経由のVRM統合はUniVRMを標準ルートに |

---

## 記録テンプレ（調査追加用）

```
【出典ID】
【Status】✅ 採用 / 🔍 参考 / ❌ 却下
【対象領域】例: Grok基礎 / Voice / RAG / MIA / Roblox / Live2D / VRM
【URL】
【要約（事実）】公式情報のみ
【設計への示唆（推論）】基盤/体験/運用にどう効くか
```

---

## 出典マップのルール

- 公式にまとまった情報がある場合は、ページ単位でURLを分けて管理する
- 具体例（MIA等）と基礎情報（Grokスタック）は混ぜずに並列管理する
- 重要度は「SPECTRA実装に必須か」「基盤化に必須か」「両方に有効か」で判断
- **事実（要約）と推論（示唆）は列を分けて記載**し、混同を防ぐ
