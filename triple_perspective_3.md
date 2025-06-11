# トリプルパースペクティブ型戦略AIレーダー：外部・内部インターフェース詳細設計

## 概要（Abstract）

本文書は、「トリプルパースペクティブ型 戦略AIレーダー」システムの外部・内部インターフェース設計の詳細を記述するものである。テクノロジー、マーケット、ビジネスの三層構造に基づく統合的情報収集・分析システムの実装に必要なインターフェース仕様を網羅的に定義している。外部インターフェースとしてはユーザー対話API、データ取得インターフェース、サードパーティ連携APIなどを規定し、内部インターフェースとしてはマイクロサービス間通信、データモデル、イベント駆動設計、分析エンジンインターフェースなどを詳述している。クラウドネイティブかつスケーラブルな設計を採用し、REST/GraphQL API、Kafka/RabbitMQメッセージング、Protobuf/Avroシリアライゼーションなどの最新技術を活用している。本設計に基づく実装により、高精度な変化点検出と将来予測を実現し、企業の戦略的意思決定を支援する実用的システムの開発が可能となる。

## 1. 序論

### 1.1 設計目的と範囲

本文書は、「トリプルパースペクティブ型 戦略AIレーダー」（以下、システム）の外部・内部インターフェース設計の詳細を定義するものである。本設計は、テクノロジー、マーケット、ビジネスの三層構造に基づく情報収集・分析・予測機能を持つシステムの実装に必要なすべてのインターフェースを対象とする。本設計文書は、開発チームによる実装の直接的な指針として使用されることを目的としている。

### 1.2 設計前提と制約条件

本インターフェース設計には、以下の前提と制約条件が適用される：

1. **アーキテクチャ前提**
   - マイクロサービスアーキテクチャを採用
   - コンテナ化技術（Docker, Kubernetes）を使用
   - クラウドネイティブ設計原則に準拠

2. **技術スタック制約**
   - バックエンド言語：Go, Python, TypeScript (Node.js)
   - フロントエンド：React.js, TypeScript
   - データストア：TimescaleDB, MongoDB, Neo4j, Elasticsearch
   - メッセージング：Apache Kafka, RabbitMQ

3. **非機能要件**
   - 応答性：対話的操作で95%のリクエストが1.5秒以内に応答
   - スケーラビリティ：最大500同時ユーザーをサポート
   - 可用性：99.9%以上（年間ダウンタイム8.76時間未満）
   - セキュリティ：OWASP Top 10に対応した脆弱性対策

### 1.3 用語と略語

| 用語/略語 | 定義 |
|----------|------|
| API | Application Programming Interface |
| REST | Representational State Transfer |
| GraphQL | Facebook開発のクエリ言語およびランタイム |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token |
| TLS | Transport Layer Security |
| RBAC | Role-Based Access Control |
| TPR | True Positive Rate |
| FPR | False Positive Rate |
| MAPE | Mean Absolute Percentage Error |
| gRPC | Google Remote Procedure Call |
| CDC | Change Data Capture |
| ETL | Extract, Transform, Load |
| SSE | Server-Sent Events |
| WSS | WebSocket Secure |

## 2. インターフェース設計の基本原則

### 2.1 設計原則

本システムのインターフェース設計は、以下の原則に基づいて行われる：

1. **疎結合性**
   - サービス間の依存関係を最小限に抑え、独立した開発・テスト・デプロイを可能にする
   - 明確に定義されたインターフェース契約に基づいた連携

2. **API第一設計**
   - インターフェース定義を先行し、実装はインターフェース契約に従う
   - OpenAPI/Swagger, Protocol Buffersなどの標準的な定義形式を使用

3. **バージョニング**
   - すべての公開インターフェースに明示的なバージョン管理を適用
   - 互換性を維持するための機構を組み込む

4. **標準化と一貫性**
   - 命名規則、エラー処理、認証方式などの一貫したパターン
   - REST、GraphQLなどのインターフェース設計における業界標準の採用

5. **可観測性**
   - すべてのインターフェースにロギング、メトリクス、トレーシングを組み込む
   - 問題診断とパフォーマンス最適化のための情報収集

6. **セキュリティバイデザイン**
   - すべてのインターフェースにセキュリティ考慮事項を組み込む
   - 認証、認可、暗号化、入力検証などの防御層を構築

### 2.2 インターフェースタイプの分類

本システムで使用されるインターフェースは、以下の分類に従って設計される：

1. **外部インターフェース**
   - **ユーザーインターフェース**：エンドユーザーとシステムの対話
   - **プログラマティックAPI**：外部システムとの連携
   - **データ取得インターフェース**：外部データソースからの情報収集
   - **通知インターフェース**：ユーザーへの能動的情報配信

2. **内部インターフェース**
   - **同期通信インターフェース**：リクエスト/レスポンスモデルの通信
   - **非同期通信インターフェース**：イベント駆動型の通信
   - **ストレージインターフェース**：データ永続化層とのやり取り
   - **分析エンジンインターフェース**：AIモデルとのやり取り

### 2.3 共通データ形式と標準

すべてのインターフェースで使用される共通データ形式と標準は以下の通り：

1. **データシリアライゼーション**
   - REST API: JSON（RFC 8259）
   - 内部高性能通信: Protocol Buffers (v3)、Apache Avro
   - ストリーミングデータ: Apache Kafka（Avroスキーマ）

2. **日時形式**
   - すべての日時データは ISO 8601 (UTC) 形式を使用: `YYYY-MM-DDThh:mm:ss.sssZ`
   - 例: `2025-04-10T15:30:45.123Z`

3. **エラー形式**
   - HTTP APIエラーは標準JSONレスポンスフォーマットを使用:
     ```json
     {
       "status": "error",
       "code": "ERROR_CODE",
       "message": "Human readable error message",
       "details": { ... }
     }
     ```

4. **ページネーション標準**
   - カーソルベースページネーション:
     ```
     ?cursor=CURSOR_TOKEN&limit=25
     ```
   - オフセットベースページネーション:
     ```
     ?offset=100&limit=25
     ```

5. **バージョニングスキーム**
   - セマンティックバージョニング (SemVer): `vX.Y.Z`
   - URL内のバージョン: `/api/v1/...`
   - ヘッダーベースバージョニング: `Accept: application/vnd.radar.v1+json`

## 3. 外部インターフェース設計

### 3.1 ユーザーインターフェース

#### 3.1.1 RESTful API

ウェブおよびモバイルアプリケーションとのインターフェースとして、RESTful APIを提供する。

**基本エンドポイント**: `https://api.strategic-radar.com/v1`

**共通ヘッダー**:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Accept: application/json
X-Request-ID: <UNIQUE_REQUEST_ID>
```

**認証エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/auth/login` | POST | ユーザー認証とトークン発行 | `{ "email": "user@example.com", "password": "secure_password" }` | `{ "token": "JWT_TOKEN", "expires_at": "ISO_DATETIME", "refresh_token": "REFRESH_TOKEN" }` |
| `/auth/refresh` | POST | アクセストークンの更新 | `{ "refresh_token": "REFRESH_TOKEN" }` | `{ "token": "NEW_JWT_TOKEN", "expires_at": "ISO_DATETIME", "refresh_token": "NEW_REFRESH_TOKEN" }` |
| `/auth/logout` | POST | セッション終了とトークン無効化 | `{}` | `{ "status": "success" }` |

**キートピック管理エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/topics` | GET | キートピック一覧取得 | N/A | `{ "topics": [{ "id": "topic_id", "name": "Topic Name", "created_at": "ISO_DATETIME", "priority": 1-5, ... }] }` |
| `/topics` | POST | 新規キートピック作成 | `{ "name": "New Topic", "description": "...", "layers": ["tech", "market", "business"], "keywords": ["key1", "key2"], "priority": 3 }` | `{ "id": "new_topic_id", "name": "New Topic", ... }` |
| `/topics/{id}` | GET | キートピック詳細取得 | N/A | `{ "id": "topic_id", "name": "Topic Name", "keywords": [...], ... }` |
| `/topics/{id}` | PUT | キートピック更新 | `{ "name": "Updated Name", "keywords": [...], ... }` | `{ "id": "topic_id", "name": "Updated Name", ... }` |
| `/topics/{id}` | DELETE | キートピック削除 | N/A | `{ "status": "success" }` |
| `/topics/{id}/expand` | POST | キートピック自動拡張 | `{ "expansion_level": 2 }` | `{ "added_keywords": ["keyword1", ...], "added_sources": ["source1", ...] }` |

**変化点検出エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/changepoints` | GET | 検出された変化点一覧 | `?topic_id=ID&from=ISO_DATE&to=ISO_DATE&layer=tech&min_importance=3` | `{ "changepoints": [{ "id": "cp_id", "topic_id": "topic_id", "detected_at": "ISO_DATETIME", "layer": "tech", "importance": 4, "description": "...", "evidence": [...] }] }` |
| `/changepoints/{id}` | GET | 変化点詳細 | N/A | `{ "id": "cp_id", "description": "...", "detected_at": "ISO_DATETIME", "data_points": [...], "related_changes": [...], "impact_analysis": {...} }` |
| `/changepoints/search` | POST | 変化点高度検索 | `{ "keywords": [...], "layers": [...], "min_importance": 3, "date_range": {...}, "cross_layer": true }` | `{ "changepoints": [...], "total": 42, "page_info": {...} }` |

**予測エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/predictions/short-term` | GET | 短期予測（2-3ヶ月）取得 | `?topic_id=ID&layer=tech` | `{ "predictions": [{ "topic_id": "topic_id", "target_date": "ISO_DATE", "value": 42.5, "confidence_interval": [40.1, 44.9], "factors": [...] }] }` |
| `/predictions/mid-term` | GET | 中期予測（6ヶ月）取得 | `?topic_id=ID&layer=market` | `{ "predictions": [...], "scenarios": [{ "name": "Base Case", "probability": 0.7, "predictions": [...] }, ...] }` |
| `/predictions/generate` | POST | カスタム予測生成 | `{ "topic_id": "topic_id", "horizon": "3m", "parameters": {...}, "scenarios": [...] }` | `{ "request_id": "req_id", "status": "processing" }` |
| `/predictions/requests/{request_id}` | GET | 予測リクエスト状態確認 | N/A | `{ "status": "completed", "result_url": "/predictions/results/xyz" }` |

**ダッシュボードデータエンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/dashboard/summary` | GET | ダッシュボード概要データ | `?topic_ids=ID1,ID2` | `{ "recent_changes": [...], "upcoming_predictions": [...], "alerts": [...] }` |
| `/dashboard/timeline` | GET | 時系列表示データ | `?topic_id=ID&from=ISO_DATE&to=ISO_DATE` | `{ "events": [{ "date": "ISO_DATE", "type": "change_point", "layer": "tech", "importance": 4, "description": "..." }] }` |
| `/dashboard/relationships` | GET | レイヤー間関係データ | `?topic_id=ID` | `{ "nodes": [...], "edges": [...], "clusters": [...] }` |

**設定エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/settings/crawling` | GET | クローリング設定取得 | N/A | `{ "default_interval": "4h", "topic_settings": [...] }` |
| `/settings/crawling` | PUT | クローリング設定更新 | `{ "default_interval": "2h", "topic_settings": [...] }` | `{ "status": "success", "updated_settings": {...} }` |
| `/settings/alerts` | GET | アラート設定取得 | N/A | `{ "email_alerts": true, "alert_threshold": 4, "alert_channels": [...] }` |
| `/settings/alerts` | PUT | アラート設定更新 | `{ "email_alerts": false, "alert_channels": [...] }` | `{ "status": "success" }` |

#### 3.1.2 GraphQL API

より柔軟なデータクエリを可能にするため、GraphQL APIを提供する。

**エンドポイント**: `https://api.strategic-radar.com/graphql`

**スキーマ概要**:

```graphql
type Query {
  # トピック関連クエリ
  topics(filter: TopicFilter, pagination: PaginationInput): TopicConnection!
  topic(id: ID!): Topic
  
  # 変化点関連クエリ
  changePoints(filter: ChangePointFilter, pagination: PaginationInput): ChangePointConnection!
  changePoint(id: ID!): ChangePoint
  
  # 予測関連クエリ
  shortTermPredictions(topicId: ID!, layer: Layer): [Prediction!]!
  midTermPredictions(topicId: ID!, layer: Layer): PredictionWithScenarios!
  
  # ダッシュボード関連クエリ
  dashboardSummary(topicIds: [ID!]): DashboardSummary!
  timelineEvents(topicId: ID!, dateRange: DateRangeInput!): [TimelineEvent!]!
  relationshipGraph(topicId: ID!): RelationshipGraph!
}

type Mutation {
  # 認証関連
  login(email: String!, password: String!): AuthPayload!
  refreshToken(refreshToken: String!): AuthPayload!
  logout: Boolean!
  
  # トピック関連
  createTopic(input: CreateTopicInput!): Topic!
  updateTopic(id: ID!, input: UpdateTopicInput!): Topic!
  deleteTopic(id: ID!): Boolean!
  expandTopic(id: ID!, expansionLevel: Int!): TopicExpansionResult!
  
  # 設定関連
  updateCrawlingSettings(input: CrawlingSettingsInput!): CrawlingSettings!
  updateAlertSettings(input: AlertSettingsInput!): AlertSettings!
  
  # 予測関連
  generateCustomPrediction(input: CustomPredictionInput!): PredictionRequest!
}

type Subscription {
  # リアルタイム通知
  onChangePointDetected(topicIds: [ID!]): ChangePoint!
  onPredictionCompleted(requestId: ID!): PredictionResult!
  onAlert(severity: AlertSeverity): Alert!
}

# 主要データ型
type Topic {
  id: ID!
  name: String!
  description: String
  layers: [Layer!]!
  keywords: [String!]!
  priority: Int!
  createdAt: DateTime!
  updatedAt: DateTime!
  relatedTopics: [Topic!]!
  recentChangePoints: [ChangePoint!]!
}

type ChangePoint {
  id: ID!
  topicId: ID!
  topic: Topic!
  layer: Layer!
  detectedAt: DateTime!
  importance: Int!
  description: String!
  evidence: [Evidence!]!
  dataPoints: [DataPoint!]!
  relatedChangePoints: [ChangePoint!]!
  impactAnalysis: ImpactAnalysis
}

type Prediction {
  id: ID!
  topicId: ID!
  topic: Topic!
  targetDate: Date!
  value: Float
  confidenceInterval: [Float!]
  factors: [PredictionFactor!]!
  accuracy: Float
}

enum Layer {
  TECHNOLOGY
  MARKET
  BUSINESS
}

# 入力型、接続型、その他の型は省略
```

**クエリ例**:

```graphql
# トピックと関連変化点の取得
query GetTopicWithChangePoints($topicId: ID!) {
  topic(id: $topicId) {
    id
    name
    description
    layers
    keywords
    recentChangePoints {
      id
      layer
      detectedAt
      importance
      description
    }
  }
}

# 予測とその要因の取得
query GetPredictionsWithFactors($topicId: ID!, $layer: Layer) {
  shortTermPredictions(topicId: $topicId, layer: $layer) {
    targetDate
    value
    confidenceInterval
    factors {
      name
      contribution
      direction
    }
  }
}

# 新しいトピックの作成
mutation CreateNewTopic($input: CreateTopicInput!) {
  createTopic(input: $input) {
    id
    name
    layers
    keywords
  }
}
```

#### 3.1.3 WebSocketインターフェース

リアルタイム更新とイベント通知のために、WebSocketインターフェースを提供する。

**エンドポイント**: `wss://api.strategic-radar.com/ws`

**認証**:
- 接続時のクエリパラメータとしてJWTトークンを提供: `?token=JWT_TOKEN`
- または、接続後の認証メッセージ:
  ```json
  {
    "type": "auth",
    "token": "JWT_TOKEN"
  }
  ```

**サブスクリプション登録**:
```json
{
  "type": "subscribe",
  "channel": "changepoints",
  "filter": {
    "topic_ids": ["topic1", "topic2"],
    "min_importance": 3
  }
}
```

**サポートするチャネル**:

| チャネル名 | 説明 | フィルタオプション |
|----------|------|-----------------|
| `changepoints` | 新規変化点検出通知 | `topic_ids`, `layers`, `min_importance` |
| `predictions` | 予測更新通知 | `topic_ids`, `prediction_type`, `request_ids` |
| `alerts` | システムアラート通知 | `severity`, `topic_ids` |
| `system` | システムステータス更新 | `types` |

**メッセージフォーマット例**:
```json
{
  "type": "event",
  "channel": "changepoints",
  "timestamp": "2025-04-10T15:30:45.123Z",
  "data": {
    "event_type": "new_changepoint",
    "changepoint": {
      "id": "cp_123",
      "topic_id": "topic1",
      "layer": "tech",
      "detected_at": "2025-04-10T14:22:33.000Z",
      "importance": 4,
      "description": "Significant increase in patent filings for quantum computing memory solutions"
    }
  }
}
```

**エラーレスポンス**:
```json
{
  "type": "error",
  "code": "invalid_subscription",
  "message": "Invalid subscription parameters",
  "request_id": "req_abc123"
}
```

#### 3.1.4 SSE (Server-Sent Events) インターフェース

WebSocketの代替として、HTTPベースのストリーミングイベントをサポート。

**エンドポイント**: `https://api.strategic-radar.com/v1/events`

**認証**: 標準のAuthorizationヘッダーを使用

**イベントストリーム**:

| イベントストリーム | 説明 | クエリパラメータ |
|-----------------|------|--------------|
| `/events/changepoints` | 変化点検出イベント | `?topic_ids=id1,id2&min_importance=3` |
| `/events/predictions` | 予測更新イベント | `?topic_ids=id1,id2&types=short_term,mid_term` |
| `/events/alerts` | アラートイベント | `?min_severity=warning` |

**イベントフォーマット**:
```
event: new_changepoint
id: evt_123456
data: {"id":"cp_123","topic_id":"topic1","importance":4,"description":"..."}

event: prediction_updated
id: evt_123457
data: {"topic_id":"topic1","prediction_type":"short_term","updated_at":"2025-04-10T15:30:45.123Z"}
```

### 3.2 外部APIインターフェース

外部システムとの統合のために公開API（プログラマティックインターフェース）を提供する。

#### 3.2.1 外部システム統合API

**エンドポイント**: `https://api.strategic-radar.com/v1/integration`

**認証**:
- API Key認証: `X-API-Key: API_KEY_VALUE`
- JWT認証: `Authorization: Bearer JWT_TOKEN`
- OAuth 2.0: 標準的なOAuthフロー

**API使用量制限**:
- レート制限: ティアに基づく（例: 基本プラン 100リクエスト/分）
- ヘッダーでの使用量通知:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1617981389
  ```

**主要エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/integration/import` | POST | 外部データのインポート | `{ "data_type": "market_report", "content": {...}, "metadata": {...} }` | `{ "status": "success", "imported_items": 1, "job_id": "job_123" }` |
| `/integration/export` | POST | システムデータのエクスポート | `{ "topic_ids": [...], "data_types": ["changepoints", "predictions"], "format": "json" }` | `{ "status": "success", "download_url": "https://..." }` |
| `/integration/sync` | POST | 双方向データ同期設定 | `{ "external_system": "salesforce", "mappings": [...], "sync_interval": "1h" }` | `{ "status": "success", "sync_id": "sync_123" }` |
| `/integration/webhook` | POST | Webhookイベント登録 | `{ "event_types": ["new_changepoint", "high_impact_prediction"], "callback_url": "https://...", "secret": "..." }` | `{ "webhook_id": "wh_123", "status": "active" }` |

**Webhook通知フォーマット**:
```json
{
  "event_type": "new_changepoint",
  "timestamp": "2025-04-10T15:30:45.123Z",
  "webhook_id": "wh_123",
  "signature": "HMAC_SIGNATURE",
  "data": {
    "changepoint_id": "cp_123",
    "topic_id": "topic1",
    "importance": 4,
    "description": "Significant technology breakthrough detected",
    "details_url": "https://api.strategic-radar.com/v1/changepoints/cp_123"
  }
}
```

#### 3.2.2 デバイク連携API（モバイル、IoT）

モバイルアプリケーションやIoTデバイスとの連携のための最適化されたAPI。

**エンドポイント**: `https://api.strategic-radar.com/v1/device`

**最適化機能**:
- 帯域幅効率: ペイロード最小化、圧縮
- バッテリー効率: バックグラウンド同期最適化
- オフライン対応: 操作キューイングとコンフリクト解決

**主要エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/device/register` | POST | デバイス登録 | `{ "device_id": "dev_123", "platform": "ios", "push_token": "..." }` | `{ "status": "success", "device_token": "..." }` |
| `/device/sync` | POST | 差分同期 | `{ "last_sync_token": "sync_abc", "changes": [...] }` | `{ "sync_token": "sync_xyz", "updates": [...], "conflicts": [...] }` |
| `/device/notifications` | PUT | 通知設定更新 | `{ "channels": ["alerts", "changepoints"], "quiet_hours": {...} }` | `{ "status": "success", "updated_at": "..." }` |

### 3.3 データ取得インターフェース

外部データソースからの情報収集のためのインターフェース仕様。

#### 3.3.1 クローラーインターフェース

ウェブコンテンツ収集のためのクローラー設定インターフェース。

**エンドポイント**: `https://api.strategic-radar.com/v1/crawlers`

**主要エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/crawlers/sources` | GET | データソース一覧取得 | `?type=news&status=active` | `{ "sources": [{ "id": "src_123", "name": "Tech News Site", "type": "news", "url_pattern": "https://...", "crawl_frequency": "4h" }] }` |
| `/crawlers/sources` | POST | データソース追加 | `{ "name": "New Source", "type": "blog", "url_pattern": "https://...", "extraction_rules": {...} }` | `{ "id": "src_124", "status": "created", ... }` |
| `/crawlers/jobs` | POST | クロールジョブ手動実行 | `{ "source_ids": ["src_123"], "priority": "high" }` | `{ "job_id": "job_456", "status": "queued" }` |
| `/crawlers/jobs/{job_id}` | GET | クロールジョブ状態確認 | N/A | `{ "status": "running", "completion": 0.65, "items_processed": 42 }` |

**ソース設定スキーマ例**:
```json
{
  "id": "src_123",
  "name": "Tech Industry News",
  "type": "news",
  "url_pattern": "https://technews.example.com/*",
  "crawl_frequency": "4h",
  "extraction_rules": {
    "title": { "selector": "h1.article-title", "attribute": "innerText" },
    "date": { "selector": "meta[property='article:published_time']", "attribute": "content" },
    "content": { "selector": "div.article-body", "attribute": "innerHTML" },
    "author": { "selector": "span.author-name", "attribute": "innerText" },
    "tags": { "selector": "ul.tags li", "attribute": "innerText", "multiple": true }
  },
  "layer_mappings": {
    "tech": ["AI", "blockchain", "quantum", "semiconductor"],
    "market": ["market share", "consumer trend", "demand"],
    "business": ["merger", "acquisition", "strategy", "revenue"]
  }
}
```

#### 3.3.2 API連携インターフェース

外部APIからのデータ取得のための設定インターフェース。

**エンドポイント**: `https://api.strategic-radar.com/v1/api-connectors`

**主要エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/api-connectors` | GET | API連携設定一覧 | N/A | `{ "connectors": [{ "id": "conn_123", "name": "Patent API", "type": "rest", "base_url": "https://...", "auth_type": "api_key" }] }` |
| `/api-connectors` | POST | API連携設定追加 | `{ "name": "Financial Data API", "type": "rest", "base_url": "https://...", "endpoints": [...], "auth": {...} }` | `{ "id": "conn_124", "status": "created" }` |
| `/api-connectors/{id}/test` | POST | 連携テスト実行 | `{ "endpoint_id": "endpoint_1" }` | `{ "status": "success", "response_sample": {...} }` |
| `/api-connectors/{id}/schedule` | PUT | 取得スケジュール設定 | `{ "schedule": "0 */4 * * *", "endpoints": [...] }` | `{ "status": "updated" }` |

**API連携設定スキーマ例**:
```json
{
  "id": "conn_123",
  "name": "Patent Database API",
  "type": "rest",
  "base_url": "https://patent-api.example.com/v2",
  "auth": {
    "type": "api_key",
    "header_name": "X-API-Key",
    "value": "{{PATENT_API_KEY}}"
  },
  "endpoints": [
    {
      "id": "endpoint_1",
      "path": "/search",
      "method": "GET",
      "parameters": [
        { "name": "q", "value": "{{TOPIC_KEYWORDS}}", "required": true },
        { "name": "date_range", "value": "{{DATE_RANGE}}" },
        { "name": "fields", "value": "title,abstract,applicant,filing_date,status" }
      ],
      "response_mapping": {
        "root_path": "results",
        "mappings": {
          "title": "title",
          "description": "abstract",
          "date": "filing_date",
          "entity": "applicant.name",
          "metadata": {
            "status": "status",
            "id": "patent_id"
          }
        }
      }
    }
  ],
  "variable_definitions": {
    "TOPIC_KEYWORDS": { "type": "topic_property", "property": "keywords", "join_by": " OR " },
    "DATE_RANGE": { "type": "dynamic", "value": "last_30_days" }
  }
}
```

#### 3.3.3 データインポートインターフェース

構造化データのバッチインポートのためのインターフェース。

**エンドポイント**: `https://api.strategic-radar.com/v1/import`

**サポートするデータ形式**:
- JSON
- CSV
- XML
- Excel (XLSX)
- RDF/OWL (知識グラフ)

**主要エンドポイント**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/import/schema/{type}` | GET | インポートスキーマ取得 | N/A | `{ "required_fields": [...], "optional_fields": [...], "field_formats": {...} }` |
| `/import/validate` | POST | データ検証（インポート前） | MultipartForm w/ file | `{ "status": "valid", "warnings": [...], "record_count": 1250 }` |
| `/import/upload` | POST | データアップロード | MultipartForm w/ file + mapping | `{ "import_id": "imp_123", "status": "queued" }` |
| `/import/{import_id}` | GET | インポート状態確認 | N/A | `{ "status": "processing", "progress": 0.7, "processed": 875, "total": 1250, "errors": [] }` |

**マッピング設定例**:
```json
{
  "file_type": "csv",
  "has_header": true,
  "delimiter": ",",
  "mapping": {
    "title": "Article Title",
    "published_date": "Publication Date",
    "source": "Source Name",
    "url": "URL",
    "content": "Content",
    "topics": "Categories"
  },
  "transformations": [
    { "field": "published_date", "type": "date", "format": "MM/DD/YYYY" },
    { "field": "topics", "type": "split", "delimiter": ";" }
  ],
  "layer_assignment": {
    "method": "keyword_matching",
    "rules": [
      { "layer": "tech", "keywords": ["technology", "innovation", "patent", "R&D"] },
      { "layer": "market", "keywords": ["market", "consumer", "demand", "segment"] },
      { "layer": "business", "keywords": ["strategy", "revenue", "profit", "company"] }
    ]
  }
}
```

### 3.4 サードパーティシステム連携インターフェース

主要な企業システムとの統合のための専用インターフェース。

#### 3.4.1 BI/分析ツール連携

BI/分析ツール（PowerBI, Tableau, Qlikなど）との連携インターフェース。

**データエクスポートエンドポイント**:

| エンドポイント | メソッド | 説明 | パラメータ | 応答 |
|--------------|--------|------|----------|-----|
| `/export/bi/dataset/{topic_id}` | GET | トピック別データセット | `?layers=tech,market&format=csv` | CSV/JSON データまたはダウンロードURL |
| `/export/bi/changepoints` | GET | 変化点データセット | `?from=ISO_DATE&to=ISO_DATE&format=json` | JSON データ |
| `/export/bi/predictions` | GET | 予測データセット | `?horizon=short_term&format=excel` | Excel ファイル |

**OData対応エンドポイント**: `https://api.strategic-radar.com/v1/odata/`

**PowerBIコネクタ設定例**:
```json
{
  "connector_id": "powerbi",
  "authentication": {
    "method": "oauth2",
    "client_id": "{{CLIENT_ID}}",
    "tenant_id": "{{TENANT_ID}}"
  },
  "datasets": [
    {
      "id": "changepoints",
      "refresh_schedule": "daily",
      "schema": {
        "tables": [
          {
            "name": "ChangePoints",
            "columns": [
              { "name": "Id", "dataType": "string" },
              { "name": "TopicId", "dataType": "string" },
              { "name": "Layer", "dataType": "string" },
              { "name": "DetectedAt", "dataType": "datetime" },
              { "name": "Importance", "dataType": "int" },
              { "name": "Description", "dataType": "string" }
            ]
          },
          {
            "name": "Topics",
            "columns": [
              { "name": "Id", "dataType": "string" },
              { "name": "Name", "dataType": "string" },
              { "name": "Description", "dataType": "string" }
            ]
          }
        ],
        "relationships": [
          {
            "name": "ChangePointTopic",
            "fromTable": "ChangePoints",
            "fromColumn": "TopicId",
            "toTable": "Topics",
            "toColumn": "Id"
          }
        ]
      }
    }
  ]
}
```

#### 3.4.2 CRM/ERPシステム連携

CRM/ERPシステム（Salesforce, SAP, Microsoft Dynamics）との連携インターフェース。

**主要連携機能**:

1. **データプッシュ**:
   - 変化点通知をCRMのタスク/アクティビティとして登録
   - 予測データをCRMのレポート/ダッシュボードに連携
   - マーケット変化をERPの需要予測に反映

2. **データプル**:
   - CRMの顧客セグメントデータをトピック分析に活用
   - ERPの製品/サービスデータをトピック定義に活用
   - 営業情報を市場データとして取り込み

**Salesforce連携設定例**:
```json
{
  "integration_id": "salesforce_1",
  "system_type": "salesforce",
  "auth": {
    "type": "oauth2",
    "auth_url": "https://login.salesforce.com/services/oauth2/authorize",
    "token_url": "https://login.salesforce.com/services/oauth2/token",
    "client_id": "{{SF_CLIENT_ID}}",
    "client_secret": "{{SF_CLIENT_SECRET}}",
    "refresh_token": "{{SF_REFRESH_TOKEN}}"
  },
  "mappings": [
    {
      "source": {
        "type": "changepoint",
        "filter": { "importance_min": 4, "layers": ["market", "business"] }
      },
      "target": {
        "object": "Task",
        "field_mapping": {
          "Subject": "New market change detected: {{changepoint.description}}",
          "Description": "{{changepoint.evidence_summary}}\n\nMore details: {{changepoint.url}}",
          "Priority": "{% if changepoint.importance >= 4 %}High{% else %}Normal{% endif %}",
          "Status": "Not Started",
          "WhatId": "{{salesforce.opportunity_id}}",
          "OwnerId": "{{salesforce.user_id}}"
        }
      },
      "trigger": "on_detection"
    },
    {
      "source": {
        "type": "prediction",
        "filter": { "horizon": "short_term", "topics": ["topic_id_1", "topic_id_2"] }
      },
      "target": {
        "object": "Market_Intelligence__c",
        "field_mapping": {
          "Prediction_Date__c": "{{prediction.target_date}}",
          "Prediction_Value__c": "{{prediction.value}}",
          "Confidence_Lower__c": "{{prediction.confidence_interval[0]}}",
          "Confidence_Upper__c": "{{prediction.confidence_interval[1]}}",
          "Related_Product__c": "{{salesforce.product_id}}",
          "Source__c": "AI Radar"
        }
      },
      "trigger": "on_update"
    }
  ]
}
```

#### 3.4.3 ナレッジマネジメントシステム連携

ナレッジマネジメントシステム（SharePoint, Confluence, 社内Wiki）との連携インターフェース。

**主要連携機能**:

1. **コンテンツプッシュ**:
   - 変化点レポートの自動生成と公開
   - トレンド分析の定期的な更新
   - 予測シナリオの共有

2. **コンテンツプル**:
   - 社内ドキュメントからの知識抽出
   - 専門家のナレッジベースからのトピック拡張
   - 社内レポートの分析と構造化

**Confluence連携設定例**:
```json
{
  "integration_id": "confluence_1",
  "system_type": "confluence",
  "base_url": "https://company.atlassian.net/wiki",
  "auth": {
    "type": "basic",
    "username": "{{CONF_USERNAME}}",
    "api_token": "{{CONF_API_TOKEN}}"
  },
  "content_push": [
    {
      "source": "monthly_market_report",
      "target": {
        "space_key": "MKT",
        "parent_page_id": "123456",
        "title_template": "Market Intelligence Report - {{date.format('MMMM YYYY')}}",
        "template_key": "market_report_template",
        "variables": {
          "report_date": "{{date.iso}}",
          "topics": "{{selected_topics}}",
          "change_points": "{{recent_changepoints}}",
          "predictions": "{{short_term_predictions}}",
          "authored_by": "Strategic AI Radar"
        }
      },
      "schedule": "0 9 1 * *" // Monthly on the 1st at 9am
    }
  ],
  "content_pull": [
    {
      "source": {
        "space_key": "RESEARCH",
        "cql": "type=page AND space=RESEARCH AND label=market_analysis AND created >= -90d"
      },
      "extraction": {
        "title": { "path": "title" },
        "content": { "path": "body.view.value" },
        "author": { "path": "history.createdBy.displayName" },
        "created_date": { "path": "history.createdDate" },
        "labels": { "path": "metadata.labels[].name" }
      },
      "mapping": {
        "layer": "market",
        "content_type": "expert_analysis",
        "topic_mapping": [
          { "label": "ai", "topic_id": "topic_id_1" },
          { "label": "blockchain", "topic_id": "topic_id_2" }
        ]
      },
      "schedule": "0 3 * * *" // Daily at 3am
    }
  ]
}
```

## 4. 内部インターフェース設計

### 4.1 マイクロサービス間通信インターフェース

#### 4.1.1 同期通信インターフェース (REST/gRPC)

マイクロサービス間の同期通信に使用するインターフェース。

**REST API規約**:

1. **基本URL構造**:
   - サービス内部URL: `http://{service-name}.{namespace}.svc.cluster.local/v{version}/{resource}`
   - 例: `http://topic-service.radar.svc.cluster.local/v1/topics`

2. **共通ヘッダー**:
   ```
   X-Request-ID: {request-id}
   X-Source-Service: {calling-service-name}
   X-Correlation-ID: {correlation-id}
   Content-Type: application/json
   ```

3. **エラーレスポンス形式**:
   ```json
   {
     "status": "error",
     "code": "ERROR_CODE",
     "message": "Error message",
     "details": { ... },
     "service": "service-name",
     "trace_id": "trace-id"
   }
   ```

**gRPC インターフェース**:

主要なマイクロサービス間で高性能な通信を実現するためのgRPCインターフェース定義。

**Protocol Buffers 定義例（Topic管理サービス）**:
```protobuf
syntax = "proto3";

package radar.topics.v1;

option go_package = "github.com/strategic-radar/proto/topics/v1";

import "google/protobuf/timestamp.proto";

service TopicService {
  // トピック作成
  rpc CreateTopic(CreateTopicRequest) returns (Topic);
  // トピック取得
  rpc GetTopic(GetTopicRequest) returns (Topic);
  // トピック一覧取得
  rpc ListTopics(ListTopicsRequest) returns (ListTopicsResponse);
  // トピック更新
  rpc UpdateTopic(UpdateTopicRequest) returns (Topic);
  // トピック削除
  rpc DeleteTopic(DeleteTopicRequest) returns (DeleteTopicResponse);
  // トピック自動拡張
  rpc ExpandTopic(ExpandTopicRequest) returns (ExpandTopicResponse);
  // トピック監視
  rpc WatchTopics(WatchTopicsRequest) returns (stream TopicChange);
}

message Topic {
  string id = 1;
  string name = 2;
  string description = 3;
  repeated string keywords = 4;
  repeated string layers = 5;
  int32 priority = 6;
  google.protobuf.Timestamp created_at = 7;
  google.protobuf.Timestamp updated_at = 8;
  map<string, string> metadata = 9;
}

message CreateTopicRequest {
  string name = 1;
  string description = 2;
  repeated string keywords = 3;
  repeated string layers = 4;
  int32 priority = 5;
  map<string, string> metadata = 6;
}

message GetTopicRequest {
  string id = 1;
}

message ListTopicsRequest {
  int32 page_size = 1;
  string page_token = 2;
  string filter = 3;
}

message ListTopicsResponse {
  repeated Topic topics = 1;
  string next_page_token = 2;
  int32 total_size = 3;
}

message UpdateTopicRequest {
  string id = 1;
  string name = 2;
  string description = 3;
  repeated string keywords = 4;
  repeated string layers = 5;
  int32 priority = 6;
  map<string, string> metadata = 7;
}

message DeleteTopicRequest {
  string id = 1;
}

message DeleteTopicResponse {
  bool success = 1;
}

message ExpandTopicRequest {
  string id = 1;
  int32 expansion_level = 2;
  double relevance_threshold = 3;
  bool apply_immediately = 4;
}

message ExpandTopicResponse {
  repeated string added_keywords = 1;
  repeated string added_sources = 2;
  repeated string suggested_keywords = 3; 
}

message WatchTopicsRequest {
  repeated string topic_ids = 1;
  bool include_updates = 2;
}

message TopicChange {
  enum ChangeType {
    UNKNOWN = 0;
    CREATED = 1;
    UPDATED = 2;
    DELETED = 3;
  }
  ChangeType type = 1;
  Topic topic = 2;
  google.protobuf.Timestamp change_time = 3;
}
```

**Protocol Buffers 定義例（変化点検出サービス）**:
```protobuf
syntax = "proto3";

package radar.changepoints.v1;

option go_package = "github.com/strategic-radar/proto/changepoints/v1";

import "google/protobuf/timestamp.proto";

service ChangePointService {
  // 変化点検出リクエスト
  rpc DetectChangePoints(DetectChangePointsRequest) returns (DetectChangePointsResponse);
  // 変化点取得
  rpc GetChangePoint(GetChangePointRequest) returns (ChangePoint);
  // 変化点一覧取得
  rpc ListChangePoints(ListChangePointsRequest) returns (ListChangePointsResponse);
  // 変化点解析
  rpc AnalyzeChangePoint(AnalyzeChangePointRequest) returns (ChangePointAnalysis);
  // 変化点ストリーム
  rpc StreamChangePoints(StreamChangePointsRequest) returns (stream ChangePoint);
}

message ChangePoint {
  string id = 1;
  string topic_id = 2;
  string layer = 3;
  google.protobuf.Timestamp detected_at = 4;
  int32 importance = 5;
  string description = 6;
  repeated Evidence evidence = 7;
  google.protobuf.Timestamp data_start_time = 8;
  google.protobuf.Timestamp data_end_time = 9;
  repeated DataPoint data_points = 10;
  float confidence = 11;
  map<string, string> metadata = 12;
}

message Evidence {
  string type = 1;
  string source = 2;
  string content = 3;
  google.protobuf.Timestamp timestamp = 4;
  float relevance = 5;
  string url = 6;
}

message DataPoint {
  google.protobuf.Timestamp timestamp = 1;
  string metric = 2;
  double value = 3;
  map<string, string> dimensions = 4;
}

message DetectChangePointsRequest {
  string topic_id = 1;
  repeated string layers = 2;
  google.protobuf.Timestamp start_time = 3;
  google.protobuf.Timestamp end_time = 4;
  DetectionConfig config = 5;
}

message DetectionConfig {
  float sensitivity = 1;
  int32 min_importance = 2;
  bool detect_cross_layer = 3;
  map<string, float> algorithm_weights = 4;
}

message DetectChangePointsResponse {
  repeated ChangePoint change_points = 1;
  string job_id = 2;
}

message GetChangePointRequest {
  string id = 1;
}

message ListChangePointsRequest {
  string topic_id = 1;
  repeated string layers = 2;
  google.protobuf.Timestamp start_time = 3;
  google.protobuf.Timestamp end_time = 4;
  int32 min_importance = 5;
  int32 page_size = 6;
  string page_token = 7;
}

message ListChangePointsResponse {
  repeated ChangePoint change_points = 1;
  string next_page_token = 2;
  int32 total_size = 3;
}

message AnalyzeChangePointRequest {
  string change_point_id = 1;
  repeated string analysis_types = 2;
}

message ChangePointAnalysis {
  string change_point_id = 1;
  Impact impact = 2;
  repeated RelatedChangePoint related_change_points = 3;
  Explanation explanation = 4;
}

message Impact {
  int32 business_impact = 1;
  string impact_description = 2;
  map<string, float> affected_metrics = 3;
  repeated string affected_entities = 4;
}

message RelatedChangePoint {
  string change_point_id = 1;
  string relation_type = 2;
  float relation_strength = 3;
  string description = 4;
}

message Explanation {
  string summary = 1;
  repeated Factor factors = 2;
  map<string, float> feature_importance = 3;
}

message Factor {
  string name = 1;
  float contribution = 2;
  string description = 3;
}

message StreamChangePointsRequest {
  repeated string topic_ids = 1;
  repeated string layers = 2;
  int32 min_importance = 3;
  bool include_evidence = 4;
}
```

#### 4.1.2 非同期通信インターフェース（イベントドリブン）

マイクロサービス間のイベント駆動型通信のインターフェース。

**イベントメッセージング規約**:

1. **基本構造**:
   ```json
   {
     "id": "evt_123456",
     "type": "event.domain.action",
     "source": "service-name",
     "time": "2025-04-10T15:30:45.123Z",
     "data": { ... },
     "metadata": {
       "trace_id": "trace-123",
       "correlation_id": "corr-456",
       "version": "1.0"
     }
   }
   ```

2. **イベントネーミング規則**:
   - パターン: `{operation}.{entity}.{action}`
   - 例: `created.topic.new`, `detected.changepoint.significant`, `updated.prediction.accuracy`

3. **デリバリー保証**:
   - 最低1回配信 (at-least-once)
   - べき等性サポート（重複排除メカニズム）
   - デッドレターキュー (DLQ) 処理

**主要イベントトピック**:

| トピック名 | 用途 | 優先パブリッシャー | キー構造 | スキーマレジストリ |
|----------|------|-----------------|----------|----------------|
| `topics` | トピック関連イベント | Topic Service | `{topic_id}` | Yes (Avro) |
| `crawler.data` | クローラー収集データ | Crawler Service | `{source_id}_{timestamp}` | Yes (Avro) |
| `structured.data` | 構造化済みデータ | Structure Service | `{entity_type}_{id}` | Yes (Avro) |
| `changepoints` | 変化点検出イベント | Changepoint Service | `{topic_id}_{layer}` | Yes (Avro) |
| `predictions` | 予測更新イベント | Prediction Service | `{topic_id}_{prediction_type}` | Yes (Avro) |
| `notifications` | 通知イベント | Notification Service | `{user_id}_{priority}` | Yes (Avro) |

**Apache Avroスキーマ例（ChangePointイベント）**:
```json
{
  "namespace": "com.strategicradar.events",
  "type": "record",
  "name": "ChangePointDetectedEvent",
  "fields": [
    {"name": "event_id", "type": "string"},
    {"name": "event_type", "type": {"type": "enum", "name": "EventType", "symbols": ["NEW", "UPDATED", "MERGED"]}},
    {"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "changepoint_id", "type": "string"},
    {"name": "topic_id", "type": "string"},
    {"name": "layer", "type": {"type": "enum", "name": "Layer", "symbols": ["TECH", "MARKET", "BUSINESS"]}},
    {"name": "importance", "type": "int"},
    {"name": "description", "type": "string"},
    {"name": "detected_at", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "confidence", "type": "float", "default": 1.0},
    {"name": "evidence", "type": {"type": "array", "items": {
      "type": "record",
      "name": "Evidence",
      "fields": [
        {"name": "source", "type": "string"},
        {"name": "url", "type": ["null", "string"], "default": null},
        {"name": "content_snippet", "type": "string"},
        {"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}}
      ]
    }}},
    {"name": "cross_layer_impact", "type": ["null", {
      "type": "record",
      "name": "CrossLayerImpact",
      "fields": [
        {"name": "layers", "type": {"type": "array", "items": "Layer"}},
        {"name": "impact_scores", "type": {"type": "map", "values": "float"}}
      ]
    }], "default": null},
    {"name": "metadata", "type": ["null", {"type": "map", "values": "string"}], "default": null}
  ]
}
```

**コンシューマーグループ設計**:

| グループ名 | 購読トピック | 用途 | 処理特性 |
|----------|------------|------|----------|
| `changepoint-analyzer` | `changepoints` | 変化点詳細分析 | バッチ処理 |
| `prediction-updater` | `changepoints` | 予測モデル更新 | 準リアルタイム |
| `cross-layer-detector` | `changepoints` | レイヤー間関連分析 | 準リアルタイム |
| `notification-dispatcher` | `changepoints`, `predictions` | ユーザー通知生成 | リアルタイム |
| `knowledge-graph-updater` | `structured.data`, `changepoints` | ナレッジグラフ更新 | バッチ処理 |

#### 4.1.3 サービスディスカバリと設定管理

マイクロサービスのディスカバリと設定管理インターフェース。

**サービスディスカバリ**:

1. **Kubernetes DNS**:
   - 形式: `{service-name}.{namespace}.svc.cluster.local`
   - ポート: サービス定義に基づく名前付きポート

2. **サービスメッシュ（Istio）**:
   - サービスエンドポイント: `http://{service-name}.{namespace}.svc.cluster.local:{port}/{path}`
   - トラフィック管理: レート制限、サーキットブレーカー、リトライポリシー

**設定管理インターフェース**:

1. **ConfigMap**:
   - 非機密設定データのための標準K8s ConfigMap
   - マウントパス: `/etc/config/{config-name}`

2. **Secret**:
   - 機密データのためのK8s Secret
   - マウントパス: `/etc/secrets/{secret-name}`

3. **分散設定（Hashicorp Consul）**:
   - 動的設定のためのKV API
   - エンドポイント: `http://consul.{namespace}.svc.cluster.local:8500/v1/kv/{service-name}/{key}`

4. **設定リロード**:
   - エンドポイント: `http://{service-name}.{namespace}.svc.cluster.local:{admin-port}/config/reload`
   - メソッド: POST
   - ペイロード: `{"reload_type": "full|partial", "keys": ["key1", "key2"]}`

### 4.2 データモデルとスキーマ

システム内部で使用されるコアデータモデルとスキーマ定義。

#### 4.2.1 コアドメインモデル

システムのドメインモデルを定義するスキーマ。

**Topic Model**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Topic",
  "type": "object",
  "required": ["id", "name", "keywords", "layers", "created_at", "updated_at"],
  "properties": {
    "id": {
      "type": "string",
      "description": "トピックの一意識別子"
    },
    "name": {
      "type": "string",
      "description": "トピック名",
      "minLength": 3,
      "maxLength": 100
    },
    "description": {
      "type": "string",
      "description": "トピックの説明",
      "maxLength": 5000
    },
    "keywords": {
      "type": "array",
      "description": "関連キーワードのリスト",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "layers": {
      "type": "array",
      "description": "関連レイヤー",
      "items": {
        "type": "string",
        "enum": ["tech", "market", "business"]
      },
      "minItems": 1
    },
    "priority": {
      "type": "integer",
      "description": "優先度（1-5）",
      "minimum": 1,
      "maximum": 5,
      "default": 3
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "作成日時"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "最終更新日時"
    },
    "metadata": {
      "type": "object",
      "description": "追加メタデータ",
      "additionalProperties": {
        "type": "string"
      }
    },
    "crawling_settings": {
      "type": "object",
      "description": "クローリング設定",
      "properties": {
        "interval": {
          "type": "string",
          "description": "クローリング間隔",
          "default": "4h",
          "pattern": "^\\d+[mhd]$"
        },
        "sources": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "depth": {
          "type": "integer",
          "minimum": 1,
          "maximum": 5,
          "default": 2
        }
      }
    },
    "related_topics": {
      "type": "array",
      "description": "関連トピックの参照",
      "items": {
        "type": "object",
        "properties": {
          "topic_id": {
            "type": "string"
          },
          "relation_type": {
            "type": "string",
            "enum": ["parent", "child", "related", "similar"]
          },
          "relation_strength": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": ["topic_id", "relation_type"]
      }
    }
  }
}
```

**ChangePoint Model**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ChangePoint",
  "type": "object",
  "required": ["id", "topic_id", "layer", "detected_at", "importance", "description"],
  "properties": {
    "id": {
      "type": "string",
      "description": "変化点の一意識別子"
    },
    "topic_id": {
      "type": "string",
      "description": "関連トピックID"
    },
    "layer": {
      "type": "string",
      "enum": ["tech", "market", "business"],
      "description": "変化が検出されたレイヤー"
    },
    "detected_at": {
      "type": "string",
      "format": "date-time",
      "description": "検出日時"
    },
    "actual_change_time": {
      "type": "string",
      "format": "date-time",
      "description": "実際の変化が発生した推定日時"
    },
    "importance": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "description": "重要度（1-5）"
    },
    "description": {
      "type": "string",
      "description": "変化の説明"
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "検出信頼度"
    },
    "change_type": {
      "type": "string",
      "enum": ["trend_shift", "spike", "step_change", "emergence", "volatility_change", "pattern_break"],
      "description": "変化の種類"
    },
    "detection_method": {
      "type": "string",
      "description": "検出に使用したアルゴリズム"
    },
    "evidence": {
      "type": "array",
      "description": "変化の証拠",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": ["document", "data_point", "entity_relation", "statistic", "expert_opinion"]
          },
          "source": {
            "type": "string"
          },
          "content": {
            "type": "string"
          },
          "url": {
            "type": "string",
            "format": "uri"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time"
          },
          "relevance": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": ["type", "source", "content"]
      }
    },
    "data_points": {
      "type": "array",
      "description": "関連データポイント",
      "items": {
        "type": "object",
        "properties": {
          "timestamp": {
            "type": "string",
            "format": "date-time"
          },
          "metric": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "dimensions": {
            "type": "object",
            "additionalProperties": {
              "type": "string"
            }
          }
        },
        "required": ["timestamp", "metric", "value"]
      }
    },
    "cross_layer_impact": {
      "type": "object",
      "description": "他レイヤーへの影響",
      "properties": {
        "tech": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "market": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "business": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        }
      }
    },
    "related_changes": {
      "type": "array",
      "description": "関連する変化点",
      "items": {
        "type": "object",
        "properties": {
          "change_point_id": {
            "type": "string"
          },
          "relation_type": {
            "type": "string",
            "enum": ["cause", "effect", "correlated", "similar"]
          },
          "relation_strength": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": ["change_point_id", "relation_type"]
      }
    },
    "impact_analysis": {
      "type": "object",
      "description": "影響分析",
      "properties": {
        "business_impact": {
          "type": "integer",
          "minimum": 1,
          "maximum": 5
        },
        "impact_description": {
          "type": "string"
        },
        "affected_metrics": {
          "type": "object",
          "additionalProperties": {
            "type": "number"
          }
        },
        "affected_entities": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "additionalProperties": {
        "type": "string"
      }
    }
  }
}
```

**Prediction Model**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Prediction",
  "type": "object",
  "required": ["id", "topic_id", "target_date", "created_at", "prediction_type"],
  "properties": {
    "id": {
      "type": "string",
      "description": "予測の一意識別子"
    },
    "topic_id": {
      "type": "string",
      "description": "関連トピックID"
    },
    "layer": {
      "type": "string",
      "enum": ["tech", "market", "business"],
      "description": "予測対象レイヤー"
    },
    "prediction_type": {
      "type": "string",
      "enum": ["short_term", "mid_term", "custom"],
      "description": "予測タイプ"
    },
    "metric": {
      "type": "string",
      "description": "予測対象メトリック"
    },
    "target_date": {
      "type": "string",
      "format": "date-time",
      "description": "予測対象日時"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "予測生成日時"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "最終更新日時"
    },
    "value": {
      "type": "number",
      "description": "予測値"
    },
    "confidence_interval": {
      "type": "array",
      "description": "信頼区間",
      "items": {
        "type": "number"
      },
      "minItems": 2,
      "maxItems": 2
    },
    "confidence_level": {
      "type": "number",
      "description": "信頼水準（0〜1）",
      "minimum": 0,
      "maximum": 1
    },
    "factors": {
      "type": "array",
      "description": "予測要因",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "contribution": {
            "type": "number",
            "description": "寄与度（-1〜1）",
            "minimum": -1,
            "maximum": 1
          },
          "direction": {
            "type": "string",
            "enum": ["positive", "negative", "neutral"],
            "description": "影響方向"
          }
        },
        "required": ["name", "contribution", "direction"]
      }
    },
    "scenarios": {
      "type": "array",
      "description": "予測シナリオ（中期予測用）",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "probability": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "シナリオ発生確率"
          },
          "value": {
            "type": "number",
            "description": "シナリオ下での予測値"
          },
          "conditions": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "シナリオ前提条件"
          }
        },
        "required": ["name", "probability", "value"]
      }
    },
    "model_metadata": {
      "type": "object",
      "description": "モデルメタデータ",
      "properties": {
        "model_type": {
          "type": "string",
          "description": "使用したモデルタイプ"
        },
        "features": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "使用した特徴量"
        },
        "training_window": {
          "type": "string",
          "description": "学習期間"
        },
        "accuracy_metrics": {
          "type": "object",
          "description": "精度メトリック",
          "properties": {
            "mape": {
              "type": "number",
              "description": "平均絶対パーセント誤差"
            },
            "rmse": {
              "type": "number",
              "description": "平均二乗誤差の平方根"
            }
          }
        }
      }
    }
  }
}
```

#### 4.2.2 データベーススキーマ

各データストアで使用するスキーマ定義。

**TimescaleDB（時系列データ）スキーマ**:

```sql
-- メトリックデータテーブル
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    topic_id TEXT NOT NULL,
    layer TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    source TEXT,
    dimensions JSONB,
    metadata JSONB
);

-- ハイパーテーブルとして設定（時系列最適化）
SELECT create_hypertable('metrics', 'time');

-- 検出された変化点テーブル
CREATE TABLE change_points (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    layer TEXT NOT NULL,
    detected_at TIMESTAMPTZ NOT NULL,
    actual_change_time TIMESTAMPTZ,
    importance INTEGER NOT NULL,
    description TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    change_type TEXT NOT NULL,
    detection_method TEXT NOT NULL,
    evidence JSONB,
    data_points JSONB,
    cross_layer_impact JSONB,
    related_changes JSONB,
    impact_analysis JSONB,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 予測データテーブル
CREATE TABLE predictions (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    layer TEXT NOT NULL,
    prediction_type TEXT NOT NULL,
    metric TEXT NOT NULL,
    target_date TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    value DOUBLE PRECISION,
    confidence_interval DOUBLE PRECISION[],
    confidence_level FLOAT,
    factors JSONB,
    scenarios JSONB,
    model_metadata JSONB
);

-- インデックス
CREATE INDEX idx_metrics_topic_layer ON metrics (topic_id, layer, time DESC);
CREATE INDEX idx_change_points_topic_layer ON change_points (topic_id, layer, detected_at DESC);
CREATE INDEX idx_predictions_topic_target ON predictions (topic_id, target_date DESC);

-- 集計用マテリアライズドビュー
CREATE MATERIALIZED VIEW metrics_daily_summary AS
SELECT
    time_bucket('1 day', time) AS bucket,
    topic_id,
    layer,
    metric_name,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value,
    COUNT(*) AS sample_count
FROM metrics
GROUP BY bucket, topic_id, layer, metric_name;

-- 定期的なリフレッシュのための関数
CREATE FUNCTION refresh_metrics_summary() RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY metrics_daily_summary;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 集計の自動更新トリガー
CREATE TRIGGER trigger_refresh_metrics_summary
AFTER INSERT OR UPDATE ON metrics
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_metrics_summary();
```

**MongoDB（ドキュメントデータ）スキーマ**:

```javascript
// topics コレクション
db.createCollection("topics", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "name", "keywords", "layers", "created_at", "updated_at"],
      properties: {
        id: { bsonType: "string" },
        name: { bsonType: "string" },
        description: { bsonType: "string" },
        keywords: { bsonType: "array", items: { bsonType: "string" } },
        layers: { bsonType: "array", items: { bsonType: "string", enum: ["tech", "market", "business"] } },
        priority: { bsonType: "int", minimum: 1, maximum: 5 },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" },
        crawling_settings: { bsonType: "object" },
        related_topics: { bsonType: "array" },
        metadata: { bsonType: "object" }
      }
    }
  }
});

// content_items コレクション（収集コンテンツ）
db.createCollection("content_items", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "source", "content_type", "collected_at", "content"],
      properties: {
        id: { bsonType: "string" },
        source: { bsonType: "string" },
        source_url: { bsonType: "string" },
        content_type: { bsonType: "string", enum: ["news", "blog", "research", "patent", "social", "report"] },
        title: { bsonType: "string" },
        author: { bsonType: "string" },
        published_at: { bsonType: "date" },
        collected_at: { bsonType: "date" },
        content: { bsonType: "string" },
        content_structured: { bsonType: "object" },
        topics: { bsonType: "array", items: { bsonType: "string" } },
        layers: { bsonType: "array", items: { bsonType: "string" } },
        entities: { bsonType: "array" },
        sentiment: { bsonType: "object" },
        relevance_scores: { bsonType: "object" },
        metadata: { bsonType: "object" },
        embedding: { bsonType: "array", items: { bsonType: "double" } }
      }
    }
  }
});

// analysis_results コレクション（分析結果）
db.createCollection("analysis_results", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "topic_id", "analysis_type", "created_at", "results"],
      properties: {
        id: { bsonType: "string" },
        topic_id: { bsonType: "string" },
        analysis_type: { bsonType: "string" },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" },
        parameters: { bsonType: "object" },
        results: { bsonType: "object" },
        visualizations: { bsonType: "array" },
        summary: { bsonType: "string" },
        metadata: { bsonType: "object" }
      }
    }
  }
});

// インデックス作成
db.topics.createIndex({ id: 1 }, { unique: true });
db.topics.createIndex({ name: 1 });
db.topics.createIndex({ keywords: 1 });
db.topics.createIndex({ layers: 1 });

db.content_items.createIndex({ id: 1 }, { unique: true });
db.content_items.createIndex({ source: 1, published_at: -1 });
db.content_items.createIndex({ topics: 1, collected_at: -1 });
db.content_items.createIndex({ layers: 1 });
db.content_items.createIndex({ embedding: "hnsw" }, { 
  name: "content_vector_index",
  hnsw: { maxConnections: 64, efConstruction: 128 }
});

db.analysis_results.createIndex({ id: 1 }, { unique: true });
db.analysis_results.createIndex({ topic_id: 1, analysis_type: 1, created_at: -1 });
```

**Neo4j（グラフデータ）スキーマ**:

```cypher
// ノードラベルの制約
CREATE CONSTRAINT topic_id IF NOT EXISTS FOR (t:Topic) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT change_point_id IF NOT EXISTS FOR (c:ChangePoint) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE;

// インデックス
CREATE INDEX topic_name IF NOT EXISTS FOR (t:Topic) ON (t.name);
CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name);
CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type);
CREATE INDEX change_point_date IF NOT EXISTS FOR (c:ChangePoint) ON (c.detected_at);
CREATE INDEX document_date IF NOT EXISTS FOR (d:Document) ON (d.published_at);

// 時間的インデックス
CREATE INDEX temporal_change_point IF NOT EXISTS FOR (c:ChangePoint) ON (c.temporal_range);

// エンティティタイプごとのノードラベル
CREATE CONSTRAINT tech_entity_id IF NOT EXISTS FOR (e:TechEntity) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT market_entity_id IF NOT EXISTS FOR (e:MarketEntity) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT business_entity_id IF NOT EXISTS FOR (e:BusinessEntity) REQUIRE e.id IS UNIQUE;

// 全文検索インデックス
CALL db.index.fulltext.createNodeIndex(
  "entity_fulltext",
  ["Entity", "TechEntity", "MarketEntity", "BusinessEntity"],
  ["name", "description"]
);

CALL db.index.fulltext.createNodeIndex(
  "document_fulltext",
  ["Document"],
  ["title", "content"]
);

// グラフデータモデルの例示
// （実際の操作ではなく、参照用の構造定義）

// トピックノード
CREATE (t:Topic {
  id: "topic123",
  name: "Quantum Computing",
  description: "Emerging quantum computing technologies and applications",
  layers: ["tech", "market", "business"],
  priority: 4,
  created_at: datetime(),
  updated_at: datetime()
});

// エンティティノード
CREATE (e:Entity:TechEntity {
  id: "tech456",
  name: "Quantum Annealing",
  type: "technology",
  description: "Quantum annealing is a metaheuristic for finding the global minimum...",
  layer: "tech",
  first_seen: datetime(),
  last_updated: datetime()
});

// ドキュメントノード
CREATE (d:Document {
  id: "doc789",
  title: "Advances in Quantum Annealing Hardware",
  source: "Quantum Research Journal",
  content_type: "research",
  published_at: datetime(),
  collected_at: datetime(),
  url: "https://example.com/quantum-paper"
});

// 変化点ノード
CREATE (c:ChangePoint {
  id: "change123",
  topic_id: "topic123",
  layer: "tech",
  detected_at: datetime(),
  importance: 4,
  description: "Significant breakthrough in quantum error correction",
  confidence: 0.92,
  change_type: "emergence",
  temporal_range: duration({months: 6})
});

// 関係定義
CREATE (t)-[:CONTAINS {relevance: 0.95}]->(e);
CREATE (e)-[:APPEARS_IN {relevance: 0.88}]->(d);
CREATE (c)-[:AFFECTS {impact: 0.85}]->(e);
CREATE (d)-[:EVIDENCES {strength: 0.9}]->(c);
CREATE (e1)-[:RELATED_TO {relation_type: "enables", strength: 0.75}]->(e2);
CREATE (c1)-[:LEADS_TO {confidence: 0.8, lag: duration({weeks: 3})}]->(c2);
```

**Elasticsearch（検索エンジン）スキーマ**:

```json
PUT /documents
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "snowball", "asciifolding"]
        }
      }

# トリプルパースペクティブ型戦略AIレーダー：外部・内部インターフェース詳細設計（続き）

## 4. 内部インターフェース設計（続き）

### 4.2 データモデルとスキーマ（続き）

#### 4.2.2 データベーススキーマ（続き）

**Elasticsearch（検索エンジン）スキーマ（続き）**:

```json
PUT /documents
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "snowball", "asciifolding"]
        },
        "keyphrase_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "shingle"]
        }
      },
      "filter": {
        "shingle": {
          "type": "shingle",
          "min_shingle_size": 2,
          "max_shingle_size": 3
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "topic_id": { "type": "keyword" },
      "source": { "type": "keyword" },
      "source_url": { "type": "keyword" },
      "content_type": { "type": "keyword" },
      "layers": { "type": "keyword" },
      "title": {
        "type": "text",
        "analyzer": "custom_analyzer",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 },
          "keyphrase": { "type": "text", "analyzer": "keyphrase_analyzer" }
        }
      },
      "author": { "type": "keyword" },
      "published_at": { "type": "date" },
      "collected_at": { "type": "date" },
      "content": {
        "type": "text",
        "analyzer": "custom_analyzer",
        "fields": {
          "keyphrase": { "type": "text", "analyzer": "keyphrase_analyzer" }
        }
      },
      "summary": { "type": "text", "analyzer": "custom_analyzer" },
      "entities": {
        "type": "nested",
        "properties": {
          "name": { "type": "keyword" },
          "type": { "type": "keyword" },
          "relevance": { "type": "float" },
          "positions": {
            "type": "nested",
            "properties": {
              "start": { "type": "integer" },
              "end": { "type": "integer" }
            }
          }
        }
      },
      "keywords": {
        "type": "nested",
        "properties": {
          "text": { "type": "keyword" },
          "score": { "type": "float" }
        }
      },
      "sentiment": {
        "properties": {
          "score": { "type": "float" },
          "magnitude": { "type": "float" },
          "positive": { "type": "float" },
          "negative": { "type": "float" },
          "neutral": { "type": "float" }
        }
      },
      "vector_embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      },
      "topic_relevance": {
        "type": "nested",
        "properties": {
          "topic_id": { "type": "keyword" },
          "score": { "type": "float" }
        }
      },
      "metadata": { "type": "object", "enabled": false }
    }
  }
}

PUT /changepoints
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "snowball", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "topic_id": { "type": "keyword" },
      "layer": { "type": "keyword" },
      "detected_at": { "type": "date" },
      "actual_change_time": { "type": "date" },
      "importance": { "type": "integer" },
      "description": { "type": "text", "analyzer": "custom_analyzer" },
      "confidence": { "type": "float" },
      "change_type": { "type": "keyword" },
      "detection_method": { "type": "keyword" },
      "evidence": {
        "type": "nested",
        "properties": {
          "type": { "type": "keyword" },
          "source": { "type": "keyword" },
          "content": { "type": "text" },
          "url": { "type": "keyword" },
          "timestamp": { "type": "date" },
          "relevance": { "type": "float" }
        }
      },
      "cross_layer_impact": {
        "properties": {
          "tech": { "type": "float" },
          "market": { "type": "float" },
          "business": { "type": "float" }
        }
      },
      "related_changes": {
        "type": "nested",
        "properties": {
          "change_point_id": { "type": "keyword" },
          "relation_type": { "type": "keyword" },
          "relation_strength": { "type": "float" }
        }
      },
      "impact_analysis": {
        "properties": {
          "business_impact": { "type": "integer" },
          "impact_description": { "type": "text" },
          "affected_metrics": { "type": "object" },
          "affected_entities": { "type": "keyword" }
        }
      },
      "vector_embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}

PUT /predictions
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "topic_id": { "type": "keyword" },
      "layer": { "type": "keyword" },
      "prediction_type": { "type": "keyword" },
      "metric": { "type": "keyword" },
      "target_date": { "type": "date" },
      "created_at": { "type": "date" },
      "updated_at": { "type": "date" },
      "value": { "type": "float" },
      "confidence_interval": { "type": "float" },
      "confidence_level": { "type": "float" },
      "factors": {
        "type": "nested",
        "properties": {
          "name": { "type": "keyword" },
          "description": { "type": "text" },
          "contribution": { "type": "float" },
          "direction": { "type": "keyword" }
        }
      },
      "scenarios": {
        "type": "nested",
        "properties": {
          "name": { "type": "keyword" },
          "description": { "type": "text" },
          "probability": { "type": "float" },
          "value": { "type": "float" },
          "conditions": { "type": "text" }
        }
      },
      "model_metadata": { "type": "object" }
    }
  }
}
```

### 4.3 分析エンジンインターフェース

AIモデルと分析エンジンとのやり取りを行うためのインターフェース。

#### 4.3.1 テキスト分析インターフェース

テキストデータの解析を行うAIモデルとのインターフェース。

**エンドポイント**: `http://text-analysis-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/analyze/entities` | POST | エンティティ抽出 | `{ "text": "...", "topic_id": "topic1", "min_relevance": 0.4 }` | `{ "entities": [{ "name": "Quantum Computing", "type": "technology", "relevance": 0.85, "positions": [...] }] }` |
| `/analyze/sentiment` | POST | 感情分析 | `{ "text": "...", "granularity": "document" }` | `{ "sentiment": { "score": 0.25, "magnitude": 0.8, "positive": 0.6, "negative": 0.35, "neutral": 0.05 } }` |
| `/analyze/keywords` | POST | キーワード抽出 | `{ "text": "...", "max_keywords": 10 }` | `{ "keywords": [{ "text": "AI safety", "score": 0.92 }, ...] }` |
| `/analyze/summarize` | POST | テキスト要約 | `{ "text": "...", "max_length": 200, "style": "informative" }` | `{ "summary": "...", "compression_ratio": 0.15 }` |
| `/analyze/classify` | POST | レイヤー/トピック分類 | `{ "text": "...", "classification_type": "layer" }` | `{ "classifications": [{ "label": "tech", "score": 0.87 }, ...] }` |
| `/analyze/embedding` | POST | ベクトル埋め込み生成 | `{ "text": "...", "model": "multilingual-e5-large" }` | `{ "embedding": [0.12, -0.45, ...], "dimensions": 768 }` |

**バッチ処理API**:

```
POST /analyze/batch
Content-Type: application/json

{
  "texts": [
    { "id": "text1", "content": "..." },
    { "id": "text2", "content": "..." }
  ],
  "analyses": ["entities", "sentiment", "keywords", "embedding"],
  "options": {
    "entities": { "min_relevance": 0.4 },
    "keywords": { "max_keywords": 5 },
    "embedding": { "model": "multilingual-e5-large" }
  }
}
```

**レスポンス例**:
```json
{
  "results": [
    {
      "id": "text1",
      "entities": [{ "name": "AI", "type": "technology", "relevance": 0.92 }, ...],
      "sentiment": { "score": 0.25, "magnitude": 0.8 },
      "keywords": [{ "text": "machine learning", "score": 0.88 }, ...],
      "embedding": [0.12, -0.45, ...]
    },
    {
      "id": "text2",
      "entities": [...],
      "sentiment": {...},
      "keywords": [...],
      "embedding": [...]
    }
  ]
}
```

#### 4.3.2 時系列分析インターフェース

時系列データの解析を行うAIモデルとのインターフェース。

**エンドポイント**: `http://timeseries-analysis-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/changepoints/detect` | POST | 変化点検出 | `{ "metric": "patent_filings", "topic_id": "topic1", "data": [...], "method": "bayesian" }` | `{ "changepoints": [{ "time": "2025-01-15", "score": 0.92, "change_type": "step" }] }` |
| `/forecast/generate` | POST | 予測生成 | `{ "metric": "market_share", "horizon": "90d", "history": [...], "model": "prophet" }` | `{ "forecast": [...], "confidence_intervals": [...] }` |
| `/anomaly/detect` | POST | 異常検出 | `{ "metric": "sentiment_score", "data": [...], "sensitivity": 0.8 }` | `{ "anomalies": [{ "time": "2025-02-03", "score": 0.95, "magnitude": 2.3 }] }` |
| `/patterns/discover` | POST | パターン発見 | `{ "metric": "user_adoption", "data": [...], "pattern_types": ["seasonal", "trend"] }` | `{ "patterns": [{ "type": "seasonal", "period": "7d", "strength": 0.76 }] }` |
| `/correlation/analyze` | POST | 相関分析 | `{ "target": "revenue", "factors": ["web_traffic", "social_mentions"], "data": { "revenue": [...], "web_traffic": [...], "social_mentions": [...] } }` | `{ "correlations": [{ "factor": "web_traffic", "coefficient": 0.82, "lag": 14 }] }` |

**時系列データ形式**:
```json
{
  "data": [
    { "timestamp": "2025-01-01T00:00:00Z", "value": 125.7 },
    { "timestamp": "2025-01-02T00:00:00Z", "value": 128.3 },
    ...
  ],
  "dimensions": {
    "region": "north_america",
    "segment": "enterprise"
  },
  "metadata": {
    "unit": "USD_million",
    "source": "quarterly_report"
  }
}
```

**一括分析ジョブAPI**:
```
POST /analysis/jobs
Content-Type: application/json

{
  "job_name": "quarterly_market_analysis",
  "topic_id": "topic1",
  "metrics": ["market_share", "patent_filings", "social_mentions"],
  "time_range": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2025-03-31T23:59:59Z"
  },
  "analyses": [
    { "type": "changepoint_detection", "params": { "methods": ["bayesian", "cusum"], "min_importance": 3 } },
    { "type": "forecast", "params": { "horizon": "180d", "models": ["prophet", "arima", "lstm"] } },
    { "type": "correlation", "params": { "lag_max": 30, "min_correlation": 0.6 } }
  ],
  "callback_url": "http://analysis-manager.radar.svc.cluster.local/v1/callbacks/job_completed"
}
```

**ジョブステータス確認API**:
```
GET /analysis/jobs/{job_id}
```

**レスポンス例**:
```json
{
  "job_id": "job_123456",
  "status": "running",
  "progress": 0.65,
  "steps_completed": 4,
  "steps_total": 6,
  "current_step": "forecast_generation",
  "results_available": [
    "changepoint_detection_market_share",
    "changepoint_detection_patent_filings"
  ],
  "created_at": "2025-04-10T10:30:00Z",
  "updated_at": "2025-04-10T10:45:30Z",
  "estimated_completion": "2025-04-10T11:00:00Z"
}
```

#### 4.3.3 グラフ分析インターフェース

ナレッジグラフの解析を行うAIモデルとのインターフェース。

**エンドポイント**: `http://graph-analysis-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/entities/related` | POST | 関連エンティティ検索 | `{ "entity_id": "ent123", "relation_types": ["enables", "competes_with"], "max_distance": 2, "min_relevance": 0.6 }` | `{ "related_entities": [{ "id": "ent456", "name": "Edge AI", "path": [...], "relevance": 0.85 }] }` |
| `/paths/find` | POST | エンティティ間のパス検索 | `{ "from_entity": "ent123", "to_entity": "ent789", "max_paths": 3 }` | `{ "paths": [{ "nodes": [...], "edges": [...], "strength": 0.75 }] }` |
| `/clusters/detect` | POST | クラスター検出 | `{ "topic_id": "topic1", "layer": "tech", "algorithm": "louvain", "min_cluster_size": 5 }` | `{ "clusters": [{ "id": "cluster1", "nodes": [...], "center": "ent123", "cohesion": 0.82 }] }` |
| `/influence/analyze` | POST | 影響分析 | `{ "entity_id": "ent123", "analysis_type": "cascade", "depth": 3 }` | `{ "influence_score": 0.88, "affected_entities": [...], "propagation_paths": [...] }` |
| `/temporal/evolution` | POST | 時間的進化分析 | `{ "topic_id": "topic1", "time_points": ["2025-01", "2025-02", "2025-03"], "metrics": ["density", "centrality"] }` | `{ "evolution": [{ "time": "2025-01", "metrics": { "density": 0.45 } }, ...], "emerging_nodes": [...], "fading_nodes": [...] }` |

**グラフクエリ言語インターフェース**:
```
POST /query/graph
Content-Type: application/json

{
  "query": "MATCH (e:Entity)-[r:RELATED_TO]->(t:Entity) WHERE e.layer = 'tech' AND r.strength > 0.7 RETURN e, r, t LIMIT 100",
  "parameters": {},
  "result_format": "graph",
  "include_properties": true
}
```

**レスポンス例**:
```json
{
  "nodes": [
    { "id": "ent123", "labels": ["Entity", "TechEntity"], "properties": { "name": "Quantum Computing", "layer": "tech" } },
    { "id": "ent456", "labels": ["Entity", "TechEntity"], "properties": { "name": "Quantum Cryptography", "layer": "tech" } }
  ],
  "relationships": [
    { "id": "rel789", "start": "ent123", "end": "ent456", "type": "RELATED_TO", "properties": { "strength": 0.85, "relation_type": "enables" } }
  ],
  "stats": {
    "nodes_returned": 2,
    "relationships_returned": 1,
    "query_time_ms": 45
  }
}
```

**クロスレイヤー影響分析API**:
```
POST /analysis/cross-layer
Content-Type: application/json

{
  "source": {
    "layer": "tech",
    "entities": ["quantum_computing", "quantum_cryptography"]
  },
  "target_layers": ["market", "business"],
  "time_horizon": "6m",
  "analysis_type": "impact_propagation",
  "min_impact_score": 0.5
}
```

**レスポンス例**:
```json
{
  "propagation_paths": [
    {
      "source_entity": "quantum_computing",
      "path": [
        { "entity": "quantum_computing", "layer": "tech" },
        { "entity": "data_security_market", "layer": "market", "impact": 0.82, "lag": "3m" },
        { "entity": "financial_service_providers", "layer": "business", "impact": 0.71, "lag": "5m" }
      ],
      "overall_impact": 0.71
    },
    ...
  ],
  "layer_impact_summary": {
    "market": { "average_impact": 0.76, "highest_impact_entity": "data_security_market" },
    "business": { "average_impact": 0.68, "highest_impact_entity": "financial_service_providers" }
  },
  "visualization_data": {
    "nodes": [...],
    "links": [...],
    "layout_algorithm": "force_directed"
  }
}
```

#### 4.3.4 モデル管理インターフェース

AIモデルの管理と制御を行うためのインターフェース。

**エンドポイント**: `http://model-management-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/models/list` | GET | 利用可能モデル一覧 | `?type=text_embedding&status=active` | `{ "models": [{ "id": "multilingual-e5-large", "type": "text_embedding", "version": "1.2.0", "status": "active" }] }` |
| `/models/info/{model_id}` | GET | モデル詳細情報 | N/A | `{ "id": "multilingual-e5-large", "type": "text_embedding", "version": "1.2.0", "capabilities": [...], "parameters": {...}, "performance_metrics": {...} }` |
| `/models/train` | POST | モデル訓練実行 | `{ "base_model": "change_detection_v1", "training_data": { "dataset_ids": [...] }, "hyperparameters": {...} }` | `{ "job_id": "train_123", "status": "submitted", "estimated_duration": "2h" }` |
| `/models/deploy` | POST | モデルデプロイ | `{ "model_id": "custom_forecaster_v2", "version": "1.0.0", "deployment_env": "staging" }` | `{ "deployment_id": "deploy_456", "status": "in_progress" }` |
| `/models/evaluate` | POST | モデル評価 | `{ "model_id": "entity_extractor_v3", "test_dataset": "test_set_1", "metrics": ["precision", "recall", "f1"] }` | `{ "evaluation_id": "eval_789", "results": { "precision": 0.92, "recall": 0.88, "f1": 0.90 } }` |
| `/models/versions/{model_id}` | GET | バージョン履歴取得 | N/A | `{ "versions": [{ "version": "1.2.0", "released_at": "2025-03-15", "changes": [...] }] }` |

**モデル訓練設定例**:
```json
{
  "base_model": "topic_classifier_v1",
  "training_data": {
    "dataset_ids": ["tech_articles_2024", "market_reports_2024"],
    "validation_split": 0.2
  },
  "training_config": {
    "epochs": 10,
    "batch_size": 32,
    "learning_rate": 1e-5,
    "early_stopping": {
      "metric": "val_f1",
      "patience": 3
    }
  },
  "hyperparameters": {
    "dropout": 0.1,
    "hidden_layers": [256, 128]
  },
  "output_config": {
    "model_name": "topic_classifier_custom",
    "description": "Fine-tuned topic classifier for tech and market articles",
    "tags": ["custom", "topics", "multilingual"]
  },
  "notification": {
    "email": "model-admin@example.com",
    "webhook": "http://notification-service/callbacks/model-training"
  }
}
```

**モデルモニタリングAPI**:
```
GET /models/monitoring/{model_id}
```

**レスポンス例**:
```json
{
  "model_id": "entity_extractor_v3",
  "version": "1.2.0",
  "deployment_status": "active",
  "health": "healthy",
  "monitoring_metrics": {
    "inference_latency_p95_ms": 245,
    "inference_latency_p99_ms": 320,
    "throughput_per_second": 42.5,
    "error_rate": 0.0023,
    "drift_detection": {
      "feature_drift_score": 0.12,
      "prediction_drift_score": 0.08,
      "last_checked": "2025-04-10T10:15:00Z"
    }
  },
  "resource_usage": {
    "cpu_utilization": 0.65,
    "memory_utilization": 0.78,
    "gpu_utilization": 0.82
  },
  "prediction_quality": {
    "current_accuracy": 0.91,
    "rolling_f1_score": 0.89,
    "baseline_comparison": {
      "accuracy_delta": -0.01,
      "f1_delta": -0.005
    }
  }
}
```

### 4.4 ワークフローとジョブ管理インターフェース

#### 4.4.1 ワークフロー定義インターフェース

複雑な分析処理フローを定義・管理するためのインターフェース。

**エンドポイント**: `http://workflow-service.radar.svc.cluster.local/v1`

**ワークフロー定義スキーマ**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AnalysisWorkflow",
  "type": "object",
  "required": ["name", "version", "steps"],
  "properties": {
    "id": {
      "type": "string",
      "description": "ワークフローの一意識別子"
    },
    "name": {
      "type": "string",
      "description": "ワークフロー名"
    },
    "description": {
      "type": "string"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "input_schema": {
      "type": "object",
      "description": "ワークフロー入力のJSONスキーマ"
    },
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type"],
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "type": {
            "type": "string",
            "enum": ["task", "condition", "parallel", "foreach", "wait"]
          },
          "task": {
            "type": "object",
            "properties": {
              "service": {
                "type": "string"
              },
              "endpoint": {
                "type": "string"
              },
              "method": {
                "type": "string",
                "enum": ["GET", "POST", "PUT", "DELETE"]
              },
              "input_mapping": {
                "type": "object"
              },
              "output_mapping": {
                "type": "object"
              },
              "retry": {
                "type": "object",
                "properties": {
                  "max_attempts": {
                    "type": "integer",
                    "minimum": 1
                  },
                  "interval": {
                    "type": "string"
                  }
                }
              }
            },
            "required": ["service", "endpoint", "method"]
          },
          "condition": {
            "type": "object",
            "properties": {
              "expression": {
                "type": "string"
              },
              "if_true": {
                "type": "string"
              },
              "if_false": {
                "type": "string"
              }
            },
            "required": ["expression", "if_true", "if_false"]
          },
          "parallel_tasks": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "foreach": {
            "type": "object",
            "properties": {
              "items_path": {
                "type": "string"
              },
              "task": {
                "type": "string"
              }
            },
            "required": ["items_path", "task"]
          },
          "wait": {
            "type": "object",
            "properties": {
              "wait_time": {
                "type": "string"
              },
              "wait_condition": {
                "type": "string"
              }
            }
          },
          "depends_on": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "timeout": {
            "type": "string"
          }
        }
      }
    },
    "error_handling": {
      "type": "object",
      "properties": {
        "on_failure": {
          "type": "string",
          "enum": ["abort", "continue", "retry", "compensate"]
        },
        "error_handler_step": {
          "type": "string"
        }
      }
    },
    "timeout": {
      "type": "string"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/workflows` | GET | ワークフロー一覧取得 | `?tags=topic_analysis&status=active` | `{ "workflows": [{ "id": "wf_123", "name": "Tech Trend Analysis", "version": "1.2.0" }] }` |
| `/workflows` | POST | 新規ワークフロー登録 | `{ "name": "Market Change Detection", "version": "1.0.0", "steps": [...] }` | `{ "id": "wf_124", "status": "created" }` |
| `/workflows/{id}` | GET | ワークフロー定義取得 | N/A | `{ "id": "wf_123", "name": "Tech Trend Analysis", "version": "1.2.0", "steps": [...] }` |
| `/workflows/{id}` | PUT | ワークフロー更新 | `{ "version": "1.2.1", "steps": [...] }` | `{ "id": "wf_123", "status": "updated" }` |
| `/workflows/{id}/validate` | POST | ワークフロー検証 | N/A | `{ "valid": true, "issues": [] }` |
| `/workflows/{id}/visualize` | GET | ワークフロー可視化 | `?format=svg` | SVGデータまたはJSON形式のグラフ定義 |

**ワークフロー定義例（変化点検出と予測生成）**:
```json
{
  "id": "wf_change_detection_prediction",
  "name": "Change Detection and Prediction Pipeline",
  "description": "Detect changes in time series data and generate predictions",
  "version": "1.0.0",
  "input_schema": {
    "type": "object",
    "required": ["topic_id", "layer", "time_range"],
    "properties": {
      "topic_id": { "type": "string" },
      "layer": { "type": "string", "enum": ["tech", "market", "business"] },
      "time_range": {
        "type": "object",
        "properties": {
          "start": { "type": "string", "format": "date-time" },
          "end": { "type": "string", "format": "date-time" }
        }
      },
      "metrics": {
        "type": "array",
        "items": { "type": "string" }
      },
      "detection_sensitivity": { "type": "number", "default": 0.7 }
    }
  },
  "steps": [
    {
      "id": "fetch_time_series",
      "name": "Fetch Time Series Data",
      "type": "task",
      "task": {
        "service": "data-service",
        "endpoint": "/timeseries/query",
        "method": "POST",
        "input_mapping": {
          "topic_id": "$.input.topic_id",
          "layer": "$.input.layer",
          "time_range": "$.input.time_range",
          "metrics": "$.input.metrics"
        },
        "output_mapping": {
          "time_series_data": "$.result"
        }
      }
    },
    {
      "id": "check_data_quality",
      "name": "Check Data Quality",
      "type": "task",
      "task": {
        "service": "data-quality-service",
        "endpoint": "/quality/check",
        "method": "POST",
        "input_mapping": {
          "data": "$.steps.fetch_time_series.time_series_data"
        },
        "output_mapping": {
          "quality_score": "$.score",
          "quality_issues": "$.issues"
        }
      },
      "depends_on": ["fetch_time_series"]
    },
    {
      "id": "quality_decision",
      "name": "Evaluate Data Quality",
      "type": "condition",
      "condition": {
        "expression": "$.steps.check_data_quality.quality_score >= 0.8",
        "if_true": "detect_changes",
        "if_false": "handle_quality_issues"
      },
      "depends_on": ["check_data_quality"]
    },
    {
      "id": "handle_quality_issues",
      "name": "Handle Data Quality Issues",
      "type": "task",
      "task": {
        "service": "data-cleansing-service",
        "endpoint": "/cleanse",
        "method": "POST",
        "input_mapping": {
          "data": "$.steps.fetch_time_series.time_series_data",
          "issues": "$.steps.check_data_quality.quality_issues"
        },
        "output_mapping": {
          "cleansed_data": "$.result"
        }
      }
    },
    {
      "id": "detect_changes",
      "name": "Detect Changes in Time Series",
      "type": "task",
      "task": {
        "service": "timeseries-analysis-service",
        "endpoint": "/changepoints/detect",
        "method": "POST",
        "input_mapping": {
          "data": "$.steps.quality_decision.if_true ? $.steps.fetch_time_series.time_series_data : $.steps.handle_quality_issues.cleansed_data",
          "topic_id": "$.input.topic_id",
          "sensitivity": "$.input.detection_sensitivity",
          "methods": ["bayesian", "cusum"]
        },
        "output_mapping": {
          "change_points": "$.changepoints"
        }
      },
      "depends_on": ["quality_decision"]
    },
    {
      "id": "parallel_analysis",
      "name": "Parallel Analysis Tasks",
      "type": "parallel",
      "parallel_tasks": ["analyze_changes", "generate_forecast"],
      "depends_on": ["detect_changes"]
    },
    {
      "id": "analyze_changes",
      "name": "Analyze Detected Changes",
      "type": "task",
      "task": {
        "service": "changepoint-analysis-service",
        "endpoint": "/analyze",
        "method": "POST",
        "input_mapping": {
          "change_points": "$.steps.detect_changes.change_points",
          "topic_id": "$.input.topic_id",
          "layer": "$.input.layer"
        },
        "output_mapping": {
          "change_analysis": "$.result"
        }
      }
    },
    {
      "id": "generate_forecast",
      "name": "Generate Time Series Forecast",
      "type": "task",
      "task": {
        "service": "timeseries-analysis-service",
        "endpoint": "/forecast/generate",
        "method": "POST",
        "input_mapping": {
          "data": "$.steps.quality_decision.if_true ? $.steps.fetch_time_series.time_series_data : $.steps.handle_quality_issues.cleansed_data",
          "change_points": "$.steps.detect_changes.change_points",
          "horizon": "90d",
          "models": ["prophet", "lstm"]
        },
        "output_mapping": {
          "forecast": "$.forecast",
          "confidence_intervals": "$.confidence_intervals"
        }
      }
    },
    {
      "id": "cross_layer_impact",
      "name": "Analyze Cross-Layer Impact",
      "type": "task",
      "task": {
        "service": "graph-analysis-service",
        "endpoint": "/analysis/cross-layer",
        "method": "POST",
        "input_mapping": {
          "source": {
            "layer": "$.input.layer",
            "change_points": "$.steps.detect_changes.change_points"
          },
          "target_layers": "$.input.layer == 'tech' ? ['market', 'business'] : ($.input.layer == 'market' ? ['business', 'tech'] : ['tech', 'market'])"
        },
        "output_mapping": {
          "impact_analysis": "$.propagation_paths",
          "layer_impacts": "$.layer_impact_summary"
        }
      },
      "depends_on": ["parallel_analysis"]
    },
    {
      "id": "generate_report",
      "name": "Generate Analysis Report",
      "type": "task",
      "task": {
        "service": "reporting-service",
        "endpoint": "/reports/generate",
        "method": "POST",
        "input_mapping": {
          "topic_id": "$.input.topic_id",
          "layer": "$.input.layer",
          "time_range": "$.input.time_range",
          "change_points": "$.steps.detect_changes.change_points",
          "change_analysis": "$.steps.analyze_changes.change_analysis",
          "forecast": "$.steps.generate_forecast.forecast",
          "confidence_intervals": "$.steps.generate_forecast.confidence_intervals",
          "cross_layer_impact": "$.steps.cross_layer_impact.impact_analysis"
        },
        "output_mapping": {
          "report": "$.report",
          "report_url": "$.url"
        }
      },
      "depends_on": ["cross_layer_impact"]
    }
  ],
  "error_handling": {
    "on_failure": "compensate",
    "error_handler_step": "handle_workflow_error"
  },
  "timeout": "1h",
  "tags": ["change_detection", "forecasting", "cross_layer"]
}
```

#### 4.4.2 ワークフロー実行インターフェース

ワークフローの実行と管理を行うためのインターフェース。

**エンドポイント**: `http://workflow-execution-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/executions` | POST | ワークフロー実行 | `{ "workflow_id": "wf_123", "input": { "topic_id": "topic1", "layer": "tech" } }` | `{ "execution_id": "exec_456", "status": "started" }` |
| `/executions/{id}` | GET | 実行状態確認 | N/A | `{ "execution_id": "exec_456", "workflow_id": "wf_123", "status": "running", "progress": 0.6, "current_step": "detect_changes" }` |
| `/executions/{id}/steps` | GET | 実行ステップ詳細 | N/A | `{ "steps": [{ "step_id": "fetch_time_series", "status": "completed", "started_at": "2025-04-10T10:30:00Z", "completed_at": "2025-04-10T10:30:05Z", "output": {...} }] }` |
| `/executions/{id}/cancel` | POST | 実行キャンセル | N/A | `{ "execution_id": "exec_456", "status": "cancelling" }` |
| `/executions/{id}/retry` | POST | 失敗ステップからリトライ | `{ "from_step": "detect_changes" }` | `{ "execution_id": "exec_457", "original_execution_id": "exec_456", "status": "started" }` |
| `/executions/schedules` | GET | スケジュール一覧取得 | N/A | `{ "schedules": [{ "id": "sched_123", "workflow_id": "wf_123", "cron": "0 2 * * *" }] }` |
| `/executions/schedules` | POST | 実行スケジュール作成 | `{ "workflow_id": "wf_123", "cron": "0 2 * * *", "input_template": { "layer": "tech" } }` | `{ "schedule_id": "sched_123", "status": "created" }` |

**実行履歴取得API**:
```
GET /executions/history?workflow_id=wf_123&status=completed&from=2025-04-01&to=2025-04-10&limit=20
```

**レスポンス例**:
```json
{
  "executions": [
    {
      "execution_id": "exec_456",
      "workflow_id": "wf_123",
      "workflow_version": "1.2.0",
      "status": "completed",
      "started_at": "2025-04-05T10:30:00Z",
      "completed_at": "2025-04-05T10:35:45Z",
      "duration_seconds": 345,
      "input": {
        "topic_id": "topic1",
        "layer": "tech"
      },
      "output": {
        "report_url": "https://reports.example.com/r123"
      },
      "metrics": {
        "steps_completed": 9,
        "steps_failed": 0,
        "total_steps": 9
      }
    },
    {
      "execution_id": "exec_452",
      "workflow_id": "wf_123",
      "workflow_version": "1.2.0",
      "status": "completed",
      "started_at": "2025-04-04T10:30:00Z",
      "completed_at": "2025-04-04T10:36:12Z",
      "duration_seconds": 372,
      "input": {
        "topic_id": "topic1",
        "layer": "market"
      },
      "output": {
        "report_url": "https://reports.example.com/r122"
      },
      "metrics": {
        "steps_completed": 9,
        "steps_failed": 0,
        "total_steps": 9
      }
    }
  ],
  "pagination": {
    "total": 45,
    "page": 1,
    "page_size": 20,
    "next_page_url": "/executions/history?workflow_id=wf_123&status=completed&from=2025-04-01&to=2025-04-10&limit=20&page=2"
  },
  "summary": {
    "success_rate": 0.95,
    "avg_duration_seconds": 358,
    "slowest_step": "generate_forecast",
    "most_failed_step": "cross_layer_impact"
  }
}
```

**スケジュール設定例**:
```json
{
  "workflow_id": "wf_change_detection_prediction",
  "name": "Daily tech layer analysis",
  "cron": "0 2 * * *",
  "timezone": "UTC",
  "input_template": {
    "topic_id": "topic1",
    "layer": "tech",
    "time_range": {
      "start": "{{ now().subtract(days=30).format('YYYY-MM-DD') }}",
      "end": "{{ now().format('YYYY-MM-DD') }}"
    },
    "metrics": ["patent_filings", "research_publications", "social_mentions"],
    "detection_sensitivity": 0.7
  },
  "active": true,
  "max_concurrent_executions": 1,
  "retry_policy": {
    "max_retries": 3,
    "retry_interval": "10m"
  },
  "notifications": {
    "on_success": [
      {
        "type": "email",
        "recipients": ["analyst@example.com"],
        "include_summary": true
      }
    ],
    "on_failure": [
      {
        "type": "email",
        "recipients": ["analyst@example.com", "admin@example.com"],
        "include_error": true
      },
      {
        "type": "webhook",
        "url": "http://alert-service/workflows/failed"
      }
    ]
  }
}
```

### 4.5 可視化および通知インターフェース

#### 4.5.1 可視化データ生成インターフェース

分析結果の可視化データを生成するためのインターフェース。

**エンドポイント**: `http://visualization-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/charts/timeseries` | POST | 時系列チャートデータ生成 | `{ "data": [...], "change_points": [...], "predictions": [...], "chart_type": "line", "annotations": true }` | `{ "chart_data": {...}, "chart_config": {...}, "annotations": [...] }` |
| `/charts/relationships` | POST | 関係性グラフデータ生成 | `{ "nodes": [...], "edges": [...], "layout": "force_directed", "clustering": true }` | `{ "graph_data": {...}, "clusters": [...], "metrics": {...} }` |
| `/charts/heatmap` | POST | ヒートマップデータ生成 | `{ "data": [...], "dimensions": ["x", "y"], "value_field": "impact", "colorscale": "viridis" }` | `{ "heatmap_data": {...}, "config": {...}, "scale_info": {...} }` |
| `/charts/comparison` | POST | 比較チャートデータ生成 | `{ "datasets": [...], "chart_type": "radar", "dimensions": [...] }` | `{ "comparison_data": {...}, "dimension_info": {...} }` |
| `/dashboards/layout` | POST | ダッシュボードレイアウト生成 | `{ "topic_id": "topic1", "layer": "tech", "widgets": [...] }` | `{ "layout": {...}, "widget_data": {...}, "refresh_info": {...} }` |

**時系列チャートリクエスト例**:
```json
{
  "data": [
    { "date": "2025-01-01", "value": 125, "group": "actual" },
    { "date": "2025-01-02", "value": 128, "group": "actual" },
    ...
  ],
  "change_points": [
    { "date": "2025-01-15", "importance": 4, "description": "Major product announcement" },
    { "date": "2025-02-05", "importance": 3, "description": "New regulation announced" }
  ],
  "predictions": [
    { "date": "2025-04-01", "value": 145, "lower": 135, "upper": 155, "group": "prediction" },
    { "date": "2025-04-02", "value": 148, "lower": 138, "upper": 158, "group": "prediction" },
    ...
  ],
  "chart_type": "line",
  "annotations": true,
  "confidence_intervals": true,
  "time_format": "YYYY-MM-DD",
  "title": "Market Growth Trend with Predictions",
  "y_axis_label": "Market Size ($ millions)",
  "color_scheme": "blue",
  "height": 400,
  "width": 800,
  "legend": true,
  "responsive": true
}
```

**関係性グラフリクエスト例**:
```json
{
  "nodes": [
    { "id": "tech1", "label": "Quantum Computing", "type": "technology", "layer": "tech", "size": 25, "attributes": { "maturity": 0.6 } },
    { "id": "tech2", "label": "Quantum Cryptography", "type": "technology", "layer": "tech", "size": 20, "attributes": { "maturity": 0.7 } },
    { "id": "market1", "label": "Data Security Market", "type": "market", "layer": "market", "size": 18, "attributes": { "growth_rate": 0.12 } },
    { "id": "business1", "label": "Financial Services", "type": "industry", "layer": "business", "size": 22, "attributes": { "impact_score": 0.8 } }
  ],
  "edges": [
    { "source": "tech1", "target": "tech2", "value": 0.85, "type": "enables", "directed": true },
    { "source": "tech2", "target": "market1", "value": 0.75, "type": "impacts", "directed": true },
    { "source": "market1", "target": "business1", "value": 0.7, "type": "affects", "directed": true }
  ],
  "layout": "force_directed",
  "clustering": true,
  "cluster_by": "layer",
  "visual_settings": {
    "node_color_field": "layer",
    "node_color_mapping": {
      "tech": "#1890ff",
      "market": "#52c41a",
      "business": "#fa8c16"
    },
    "edge_width_scale": [1, 5],
    "edge_color_field": "type",
    "directed_edges": true,
    "show_labels": true,
    "layer_rendering": true
  },
  "interaction_settings": {
    "zoom": true,
    "pan": true,
    "selection": true,
    "tooltip": true,
    "neighborhood_highlight": true
  },
  "filters": [
    { "field": "layer", "type": "categorical", "default": ["tech", "market", "business"] },
    { "field": "value", "type": "range", "min": 0, "max": 1, "default": [0.6, 1] }
  ]
}
```

**ダッシュボードレイアウトリクエスト例**:
```json
{
  "topic_id": "topic1",
  "layer": "tech",
  "time_range": {
    "start": "2025-01-01",
    "end": "2025-04-10"
  },
  "layout_type": "responsive_grid",
  "widgets": [
    {
      "id": "widget1",
      "type": "timeseries_chart",
      "title": "Technology Adoption Trend",
      "data_source": {
        "metric": "adoption_rate",
        "include_change_points": true,
        "include_predictions": true
      },
      "position": { "x": 0, "y": 0, "w": 8, "h": 4 },
      "refresh_interval": "15m"
    },
    {
      "id": "widget2",
      "type": "relationship_graph",
      "title": "Technology Ecosystem",
      "data_source": {
        "scope": "related_technologies",
        "depth": 2,
        "min_relevance": 0.6
      },
      "position": { "x": 8, "y": 0, "w": 4, "h": 6 },
      "refresh_interval": "1h"
    },
    {
      "id": "widget3",
      "type": "changepoint_list",
      "title": "Recent Technology Changes",
      "data_source": {
        "time_range": "last_30d",
        "min_importance": 3,
        "sort_by": "detected_at",
        "sort_direction": "desc"
      },
      "position": { "x": 0, "y": 4, "w": 4, "h": 4 },
      "refresh_interval": "10m"
    },
    {
      "id": "widget4",
      "type": "heatmap",
      "title": "Cross-Layer Impact Analysis",
      "data_source": {
        "source_layer": "tech",
        "target_layers": ["market", "business"],
        "value_field": "impact_score"
      },
      "position": { "x": 4, "y": 4, "w": 4, "h": 4 },
      "refresh_interval": "1h"
    }
  ],
  "global_filters": [
    {
      "name": "time_range",
      "type": "daterange",
      "default": {
        "start": "2025-01-01",
        "end": "2025-04-10"
      }
    },
    {
      "name": "entity_focus",
      "type": "multiselect",
      "options": [
        { "value": "all", "label": "All Technologies" },
        { "value": "quantum", "label": "Quantum Technologies" },
        { "value": "ai", "label": "AI Technologies" }
      ],
      "default": ["all"]
    }
  ],
  "settings": {
    "theme": "light",
    "auto_refresh": true,
    "show_timestamp": true,
    "collapse_filters": false
  }
}
```

#### 4.5.2 通知管理インターフェース

通知の生成と配信を管理するためのインターフェース。

**エンドポイント**: `http://notification-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/notifications` | POST | 通知生成 | `{ "type": "changepoint_detected", "importance": 4, "topic_id": "topic1", "data": {...}, "channels": ["email", "dashboard"] }` | `{ "notification_id": "notif_123", "status": "queued" }` |
| `/notifications/{id}` | GET | 通知詳細取得 | N/A | `{ "id": "notif_123", "type": "changepoint_detected", "status": "delivered", "delivery_info": {...} }` |
| `/notifications/user/{user_id}` | GET | ユーザー宛通知一覧 | `?status=unread&limit=20` | `{ "notifications": [...], "total_unread": 5 }` |
| `/notifications/settings` | GET | 通知設定取得 | N/A | `{ "email_notifications": true, "push_notifications": true, "notification_preferences": {...} }` |
| `/notifications/settings` | PUT | 通知設定更新 | `{ "email_notifications": false, "notification_preferences": { "changepoint": { "min_importance": 4 } } }` | `{ "status": "updated" }` |
| `/notifications/channels` | GET | 通知チャネル一覧 | N/A | `{ "channels": [{ "id": "email", "name": "Email", "enabled": true, "config": {...} }] }` |

**通知設定スキーマ**:
```json
{
  "delivery_preferences": {
    "email": {
      "enabled": true,
      "address": "user@example.com",
      "format": "html",
      "digest": {
        "enabled": true,
        "frequency": "daily",
        "time": "08:00",
        "timezone": "Asia/Tokyo",
        "min_notifications": 1
      }
    },
    "push": {
      "enabled": true,
      "devices": [
        {
          "id": "device1",
          "platform": "ios",
          "token": "device_token_1"
        }
      ],
      "quiet_hours": {
        "enabled": true,
        "start": "22:00",
        "end": "08:00",
        "timezone": "Asia/Tokyo",
        "exceptions": ["high_importance"]
      }
    },
    "dashboard": {
      "enabled": true,
      "max_unread": 100,
      "expiry": "30d"
    },
    "slack": {
      "enabled": true,
      "workspace": "example",
      "channel": "#radar-alerts",
      "username": "Strategic AI Radar"
    }
  },
  "notification_preferences": {
    "changepoint": {
      "enabled": true,
      "channels": ["email", "dashboard", "push"],
      "min_importance": 3,
      "topic_filter": {
        "included": ["topic1", "topic2"],
        "excluded": []
      },
      "layer_filter": ["tech", "business"]
    },
    "prediction": {
      "enabled": true,
      "channels": ["email", "dashboard"],
      "threshold": {
        "operator": ">",
        "value": 10,
        "field": "percentage_change"
      }
    },
    "system": {
      "enabled": true,
      "channels": ["email"],
      "types": ["workflow_failed", "model_drift_detected"]
    }
  },
  "schedule": {
    "timezone": "Asia/Tokyo",
    "working_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
    "working_hours": {
      "start": "09:00",
      "end": "18:00"
    }
  },
  "alert_escalation": {
    "enabled": true,
    "escalation_rules": [
      {
        "condition": {
          "type": "changepoint",
          "importance": 5
        },
        "escalation_channels": ["sms", "call"],
        "wait_time": "30m"
      }
    ]
  }
}
```

**通知テンプレート定義API**:
```
POST /notifications/templates
Content-Type: application/json

{
  "template_id": "changepoint_alert",
  "name": "Change Point Alert",
  "description": "Template for change point detection alerts",
  "channels": ["email", "push", "dashboard"],
  "versions": [
    {
      "version": "1.0.0",
      "channel_templates": {
        "email": {
          "subject": "Strategic Alert: {{ change_point.importance_level }} change detected in {{ topic.name }}",
          "html": "<html><body><h1>Important Change Detected</h1><p>A {{ change_point.importance_level }} change has been detected in {{ topic.name }} within the {{ change_point.layer }} layer.</p><p><strong>Description:</strong> {{ change_point.description }}</p><p><strong>Detected at:</strong> {{ change_point.detected_at | date('YYYY-MM-DD HH:mm') }}</p><p><strong>Potential impact:</strong> {{ change_point.impact_description }}</p><p><a href=\"{{ change_point.url }}\">View details</a></p></body></html>",
          "text": "Important Change Detected\n\nA {{ change_point.importance_level }} change has been detected in {{ topic.name }} within the {{ change_point.layer }} layer.\n\nDescription: {{ change_point.description }}\n\nDetected at: {{ change_point.detected_at | date('YYYY-MM-DD HH:mm') }}\n\nPotential impact: {{ change_point.impact_description }}\n\nView details: {{ change_point.url }}"
        },
        "push": {
          "title": "{{ change_point.importance_level }} change in {{ topic.name }}",
          "body": "{{ change_point.description }}",
          "data": {
            "type": "changepoint",
            "id": "{{ change_point.id }}",
            "url": "{{ change_point.url }}"
          }
        },
        "dashboard": {
          "title": "{{ change_point.importance_level }} change detected",
          "content": "{{ change_point.description }}",
          "icon": "change_{{ change_point.importance }}",
          "color": "{{ change_point.importance >= 4 ? 'red' : (change_point.importance >= 3 ? 'orange' : 'blue') }}"
        }
      }
    }
  ],
  "default_version": "1.0.0",
  "variables": [
    {
      "name": "topic",
      "description": "Topic information",
      "required": true
    },
    {
      "name": "change_point",
      "description": "Change point information",
      "required": true
    }
  ]
}
```

### 4.6 セキュリティとアクセス制御インターフェース

#### 4.6.1 認証・認可インターフェース

ユーザー認証と認可を管理するためのインターフェース。

**エンドポイント**: `http://auth-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/auth/token` | POST | サービス間トークン発行 | `{ "service_id": "timeseries-service", "audience": "graph-service", "scope": ["read:data", "write:analysis"] }` | `{ "token": "JWT_TOKEN", "expires_in": 3600 }` |
| `/auth/validate` | POST | トークン検証 | `{ "token": "JWT_TOKEN" }` | `{ "valid": true, "claims": { "sub": "service_id", "scope": [...] } }` |
| `/permissions/check` | POST | アクセス権限確認 | `{ "subject": "user123", "resource": "topic:topic1", "action": "read" }` | `{ "allowed": true, "policy_id": "policy123" }` |
| `/permissions/policies` | GET | ポリシー一覧取得 | `?resource_type=topic` | `{ "policies": [{ "id": "policy123", "name": "Topic Reader", "rules": [...] }] }` |
| `/permissions/policies` | POST | ポリシー作成 | `{ "name": "Topic Editor", "description": "...", "rules": [...] }` | `{ "policy_id": "policy124", "status": "created" }` |
| `/permissions/roles` | GET | ロール一覧取得 | N/A | `{ "roles": [{ "id": "role123", "name": "Analyst", "policies": [...] }] }` |
| `/permissions/assignments` | POST | ロール割り当て | `{ "subject_id": "user123", "role_id": "role123" }` | `{ "assignment_id": "assign123", "status": "created" }` |

**RBACポリシー定義例**:
```json
{
  "id": "policy_topic_editor",
  "name": "Topic Editor",
  "description": "Allows editing and management of topics",
  "version": "1.0.0",
  "effect": "allow",
  "subjects": ["role:analyst", "role:admin"],
  "resources": ["topic:*"],
  "actions": ["topic:read", "topic:create", "topic:update"],
  "conditions": {
    "ownership": {
      "type": "StringEquals",
      "field": "owner_id",
      "value": "${subject.id}"
    }
  }
}
```

**ABACポリシー定義例**:
```json
{
  "id": "policy_sensitive_data",
  "name": "Sensitive Data Access",
  "description": "Controls access to sensitive business layer data",
  "version": "1.0.0",
  "effect": "allow",
  "subjects": ["group:executives", "role:senior_analyst"],
  "resources": ["layer:business:*"],
  "actions": ["read", "export"],
  "conditions": {
    "time_based": {
      "type": "TimeRange",
      "start_time": "09:00:00",
      "end_time": "17:00:00",
      "timezone": "Asia/Tokyo",
      "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
    },
    "ip_based": {
      "type": "CIDRMatch",
      "value": "${request.ip}",
      "cidr": ["192.168.1.0/24", "10.0.0.0/8"]
    },
    "clearance_level": {
      "type": "NumberGreaterThanEquals",
      "value": "${subject.clearance_level}",
      "threshold": 3
    }
  }
}
```

#### 4.6.2 監査ログインターフェース

セキュリティ監査ログを管理するためのインターフェース。

**エンドポイント**: `http://audit-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/logs` | POST | 監査ログ記録 | `{ "event_type": "data_access", "subject": "user123", "resource": "topic:topic1", "action": "read", "outcome": "success", "metadata": {...} }` | `{ "log_id": "log123", "status": "recorded" }` |
| `/logs` | GET | 監査ログ検索 | `?event_type=data_access&subject=user123&from=2025-04-01&to=2025-04-10` | `{ "logs": [...], "total": 253, "pagination": {...} }` |
| `/logs/summary` | GET | ログ集計サマリー | `?group_by=event_type&time_interval=day&from=2025-04-01&to=2025-04-10` | `{ "summary": [{ "event_type": "data_access", "count": 1250, "time_series": [...] }] }` |
| `/logs/export` | POST | ログエクスポート | `{ "query": {...}, "format": "csv" }` | `{ "export_id": "export123", "status": "processing" }` |
| `/reports/security` | GET | セキュリティレポート | `?report_type=access_patterns&period=month` | `{ "report": {...}, "insights": [...], "anomalies": [...] }` |

**監査ログスキーマ**:
```json
{
  "id": "log_5f7c3a2e",
  "timestamp": "2025-04-10T15:30:45.123Z",
  "event_type": "data_access",
  "subject": {
    "id": "user123",
    "type": "user",
    "name": "John Doe",
    "roles": ["analyst"]
  },
  "resource": {
    "id": "topic1",
    "type": "topic",
    "name": "Quantum Computing",
    "owner": "user456"
  },
  "action": {
    "type": "read",
    "operation": "api_call",
    "api_path": "/topics/topic1"
  },
  "outcome": {
    "status": "success",
    "reason": null
  },
  "context": {
    "request_id": "req_abc123",
    "correlation_id": "corr_def456",
    "client_ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "session_id": "sess_ghi789"
  },
  "metadata": {
    "data_sensitivity": "confidential",
    "access_reason": "scheduled_analysis",
    "query_params": {
      "fields": "name,description,keywords",
      "include_analysis": true
    }
  },
  "risk_score": 0.2,
  "retention_policy": "1y"
}
```

**セキュリティレポート例**:
```json
{
  "report_id": "sec_report_123",
  "report_type": "access_patterns",
  "period": "month",
  "start_date": "2025-03-01",
  "end_date": "2025-03-31",
  "generated_at": "2025-04-01T00:15:00Z",
  "summary": {
    "total_access_events": 25463,
    "unique_users": 87,
    "unique_resources": 342,
    "access_denied_events": 156,
    "high_risk_events": 42
  },
  "trends": {
    "daily_events": [...],
    "hourly_distribution": [...],
    "top_accessed_resources": [
      { "resource_id": "topic1", "resource_type": "topic", "access_count": 1256 },
      ...
    ],
    "top_active_users": [
      { "user_id": "user123", "access_count": 534, "unique_resources": 45 },
      ...
    ]
  },
  "anomalies": [
    {
      "type": "unusual_access_time",
      "description": "Multiple after-hours access to sensitive business data",
      "severity": "medium",
      "details": {
        "user_id": "user789",
        "resource_type": "layer:business",
        "event_count": 12,
        "time_range": "22:00-02:00",
        "dates": ["2025-03-15", "2025-03-16"]
      },
      "recommendation": "Review user access patterns and confirm business need"
    },
    ...
  ],
  "compliance": {
    "policy_violations": 8,
    "gdpr_relevant_events": 145,
    "data_export_events": 23
  }
}
```

## 5. デプロイメントと運用インターフェース

### 5.1 構成管理インターフェース

システム構成を管理するためのインターフェース。

**エンドポイント**: `http://config-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/config` | GET | 設定取得 | `?component=topic-service&env=production` | `{ "component": "topic-service", "version": "1.2.0", "settings": {...} }` |
| `/config` | PUT | 設定更新 | `{ "component": "topic-service", "settings": { "max_topics_per_user": 50 } }` | `{ "status": "updated", "revision": 5 }` |
| `/config/history` | GET | 設定変更履歴 | `?component=topic-service&limit=10` | `{ "history": [{ "revision": 5, "changed_by": "user123", "timestamp": "2025-04-10T15:30:45Z", "changes": [...] }] }` |
| `/config/validate` | POST | 設定検証 | `{ "component": "topic-service", "settings": {...} }` | `{ "valid": true, "issues": [] }` |
| `/config/import` | POST | 設定インポート | `{ "source": "staging", "components": ["topic-service"], "override": false }` | `{ "import_id": "imp123", "status": "started" }` |
| `/config/export` | POST | 設定エクスポート | `{ "components": ["topic-service", "crawler-service"], "format": "yaml" }` | `{ "export_id": "exp123", "download_url": "..." }` |

**コンポーネント設定例**:
```json
{
  "component": "graph-analysis-service",
  "version": "1.3.0",
  "description": "Graph analysis service configuration",
  "last_updated": "2025-04-01T12:30:45Z",
  "updated_by": "admin",
  "revision": 8,
  "environments": {
    "production": {
      "service": {
        "replicas": 3,
        "resources": {
          "requests": {
            "cpu": "2",
            "memory": "4Gi"
          },
          "limits": {
            "cpu": "4",
            "memory": "8Gi"
          }
        },
        "autoscaling": {
          "enabled": true,
          "min_replicas": 2,
          "max_replicas": 10,
          "target_cpu_utilization": 70
        }
      },
      "database": {
        "connection_string": "${SECRET:neo4j_connection_string}",
        "max_connections": 50,
        "connection_timeout": "5s",
        "query_timeout": "30s"
      },
      "analysis": {
        "algorithms": {
          "pagerank": {
            "max_iterations": 100,
            "damping_factor": 0.85,
            "tolerance": 1e-6
          },
          "community_detection": {
            "algorithm": "louvain",
            "resolution": 1.0,
            "seed": 42
          },
          "path_finding": {
            "max_depth": 5,
            "max_paths": 10,
            "timeout": "10s"
          }
        },
        "caching": {
          "enabled": true,
          "ttl": "1h",
          "max_size": "1Gi"
        },
        "batch_size": 1000
      },
      "api": {
        "rate_limit": 100,
        "timeout": "60s",
        "cors": {
          "allowed_origins": ["https://app.example.com"],
          "allowed_methods": ["GET", "POST"]
        }
      },
      "logging": {
        "level": "info",
        "format": "json",
        "output": ["stdout", "file"],
        "file_path": "/var/log/graph-service.log",
        "rotation": {
          "max_size": "100Mi",
          "max_age": "7d",
          "max_backups": 5
        }
      },
      "tracing": {
        "enabled": true,
        "sampling_rate": 0.1,
        "exporter": "jaeger"
      }
    },
    "staging": {
      "service": {
        "replicas": 1,
        "resources": {
          "requests": {
            "cpu": "1",
            "memory": "2Gi"
          },
          "limits": {
            "cpu": "2",
            "memory": "4Gi"
          }
        }
      },
      "logging": {
        "level": "debug"
      }
    }
  },
  "default_environment": "production"
}
```

### 5.2 モニタリングとアラートインターフェース

システムのモニタリングとアラートを管理するためのインターフェース。

**エンドポイント**: `http://monitoring-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/metrics` | GET | メトリクス取得 | `?service=topic-service&metric=api_latency&from=2025-04-01&to=2025-04-10` | `{ "metric": "api_latency", "data_points": [...], "statistics": {...} }` |
| `/health` | GET | ヘルスステータス取得 | `?service=all` | `{ "overall_status": "healthy", "services": [{ "name": "topic-service", "status": "healthy", "last_check": "..." }] }` |
| `/alerts` | GET | アラート一覧取得 | `?status=active&severity=high` | `{ "alerts": [{ "id": "alert123", "service": "database-service", "severity": "high", "message": "..." }] }` |
| `/alerts` | POST | アラート作成 | `{ "service": "crawler-service", "severity": "medium", "message": "Crawler job failure rate exceeds threshold", "metric": { "name": "job_failure_rate", "value": 0.15, "threshold": 0.1 } }` | `{ "alert_id": "alert124", "status": "created" }` |
| `/alerts/{id}/acknowledge` | POST | アラート承認 | `{ "comment": "Investigating the issue" }` | `{ "status": "acknowledged", "acknowledged_by": "user123" }` |
| `/alerts/{id}/resolve` | POST | アラート解決 | `{ "resolution": "Increased worker count to handle load" }` | `{ "status": "resolved", "resolved_by": "user123" }` |
| `/dashboards/ops` | GET | 運用ダッシュボードデータ | `?view=system_health` | `{ "system_health": {...}, "service_metrics": {...}, "recent_alerts": [...] }` |

**アラートルール定義例**:
```json
{
  "id": "rule_123",
  "name": "High API Latency",
  "description": "Alerts when API latency exceeds threshold",
  "enabled": true,
  "service": "topic-service",
  "metric": {
    "name": "api_latency_p95",
    "aggregation": "avg",
    "period": "5m"
  },
  "condition": {
    "operator": ">",
    "threshold": 500,
    "unit": "ms",
    "for_duration": "10m"
  },
  "severity": "medium",
  "labels": {
    "component": "api",
    "team": "backend"
  },
  "annotations": {
    "summary": "High API latency detected for topic-service",
    "description": "The p95 latency for topic-service API has exceeded 500ms for more than 10 minutes",
    "runbook_url": "https://wiki.example.com/runbooks/high-api-latency"
  },
  "notifications": {
    "channels": ["slack", "email"],
    "throttling": {
      "group_by": ["service"],
      "wait": "30m"
    }
  },
  "actions": {
    "auto_scale": {
      "enabled": true,
      "replicas": "+2",
      "max_replicas": 10
    }
  }
}
```

**サービスヘルスチェック定義例**:
```json
{
  "id": "health_check_db",
  "name": "Database Connectivity Check",
  "service": "database-service",
  "check_type": "http",
  "endpoint": "http://database-service.radar.svc.cluster.local/health",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer ${SECRET:health_check_token}"
  },
  "expected_status": 200,
  "expected_response": {
    "jsonpath": "$.status",
    "value": "healthy"
  },
  "timeout": "5s",
  "interval": "30s",
  "failure_threshold": 3,
  "success_threshold": 1,
  "dependencies": [
    "infrastructure_db"
  ]
}
```

### 5.3 スケーリングとリソース管理インターフェース

システムのスケーリングとリソース管理を行うためのインターフェース。

**エンドポイント**: `http://autoscaler-service.radar.svc.cluster.local/v1`

**主要API**:

| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|--------------|--------|------|----------|-----------|
| `/scaling/status` | GET | スケーリング状態取得 | `?service=topic-service` | `{ "service": "topic-service", "current_replicas": 3, "min_replicas": 2, "max_replicas": 10, "metrics": {...} }` |
| `/scaling/rules` | GET | スケーリングルール取得 | `?service=topic-service` | `{ "rules": [{ "id": "rule123", "metric": "cpu_utilization", "target": 70 }] }` |
| `/scaling/rules` | POST | スケーリングルール作成 | `{ "service": "crawler-service", "metric": "queue_length", "target": 100, "min_replicas": 1, "max_replicas": 20 }` | `{ "rule_id": "rule124", "status": "created" }` |
| `/scaling/manual` | POST | 手動スケーリング | `{ "service": "analysis-service", "replicas": 5, "reason": "Expected load increase" }` | `{ "status": "scaling", "previous_replicas": 3, "target_replicas": 5 }` |
| `/resources/usage` | GET | リソース使用状況取得 | `?namespace=radar&group_by=service` | `{ "cpu": { "total": 45.2, "by_service": {...} }, "memory": { "total": 120.5, "by_service": {...} } }` |
| `/resources/allocation` | GET | リソース割り当て取得 | `?service=all` | `{ "services": [{ "name": "topic-service", "cpu_request": 2, "cpu_limit": 4, "memory_request": "4Gi", "memory_limit": "8Gi" }] }` |
| `/resources/optimize` | POST | リソース最適化提案 | `{ "service": "prediction-service", "time_range": "7d" }` | `{ "recommendations": [{ "resource": "cpu", "current_request": 4, "recommended_request": 2, "confidence": 0.9 }] }` |

**スケーリングルール定義例**:
```json
{
  "id": "scale_rule_123",
  "service": "prediction-service",
  "description": "Scale prediction service based on queue length and CPU usage",
  "enabled": true,
  "min_replicas": 2,
  "max_replicas": 30,
  "stabilization_window": {
    "scale_up": "1m",
    "scale_down": "5m"
  },
  "metrics": [
    {
      "type": "resource",
      "resource": {
        "name": "cpu",
        "target_utilization": 70
      }
    },
    {
      "type": "custom",
      "custom": {
        "metric_name": "prediction_queue_length",
        "target_value": 100,
        "selector": {
          "matchLabels": {
            "service": "prediction-service"
          }
        }
      }
    }
  ],
  "behavior": {
    "scale_up": {
      "select_policy": "max",
      "stabilization_window": "1m",
      "policies": [
        {
          "type": "pods",
          "value": 4,
          "period": "60s"
        },
        {
          "type": "percent",
          "value": 100,
          "period": "60s"
        }
      ]
    },
    "scale_down": {
      "select_policy": "min",
      "stabilization_window": "5m",
      "policies": [
        {
          "type": "pods",
          "value": 2,
          "period": "60s"
        },
        {
          "type": "percent",
          "value": 20,
          "period": "60s"
        }
      ]
    }
  },
  "schedule": {
    "workday_scale_up": {
      "cron": "0 8 * * 1-5",
      "timezone": "Asia/Tokyo",
      "target_replicas": 10,
      "description": "Scale up for business hours"
    },
    "workday_scale_down": {
      "cron": "0 20 * * 1-5",
      "timezone": "Asia/Tokyo",
      "target_replicas": 2,
      "description": "Scale down for non-business hours"
    }
  }
}
```

**リソース最適化提案レスポンス例**:
```json
{
  "service": "prediction-service",
  "analysis_period": {
    "start": "2025-04-01T00:00:00Z",
    "end": "2025-04-07T23:59:59Z"
  },
  "current_configuration": {
    "replicas": 10,
    "resources": {
      "requests": {
        "cpu": "4",
        "memory": "8Gi"
      },
      "limits": {
        "cpu": "8",
        "memory": "16Gi"
      }
    }
  },
  "recommendations": [
    {
      "resource": "cpu",
      "current_request": "4",
      "recommended_request": "2",
      "confidence": 0.92,
      "potential_saving": "20 CPU cores",
      "risk_level": "low",
      "evidence": {
        "peak_usage": "1.8 cores",
        "p95_usage": "1.5 cores",
        "p99_usage": "1.7 cores",
        "usage_trend": "stable"
      }
    },
    {
      "resource": "memory",
      "current_request": "8Gi",
      "recommended_request": "6Gi",
      "confidence": 0.85,
      "potential_saving": "20Gi memory",
      "risk_level": "low",
      "evidence": {
        "peak_usage": "5.2Gi",
        "p95_usage": "4.8Gi",
        "p99_usage": "5.1Gi",
        "usage_trend": "slight increase"
      }
    },
    {
      "resource": "replicas",
      "current_value": 10,
      "recommended_value": 8,
      "confidence": 0.78,
      "potential_saving": "2 replicas",
      "risk_level": "medium",
      "evidence": {
        "peak_load": "7.2 pods worth",
        "avg_load": "5.5 pods worth",
        "usage_pattern": "diurnal with peaks at 14:00-16:00"
      }
    }
  ],
  "implementation_plan": {
    "steps": [
      {
        "step": 1,
        "action": "Update CPU requests",
        "change": "4 cores -> 3 cores",
        "observation_period": "3 days"
      },
      {
        "step": 2,
        "action": "Update memory requests",
        "change": "8Gi -> 7Gi",
        "observation_period": "3 days"
      },
      {
        "step": 3,
        "action": "Further optimizations",
        "condition": "No performance degradation observed"
      }
    ],
    "rollback_plan": "Revert to original configuration if p99 latency increases by more than 10% or any service disruptions occur"
  }
}
```

## 6. まとめ

本文書では、「トリプルパースペクティブ型 戦略AIレーダー」システムの外部・内部インターフェース設計を網羅的に提示した。テクノロジー、マーケット、ビジネスの三層構造に基づく統合的情報収集・分析システムの実装に必要なすべてのインターフェース仕様を詳細に定義している。

主要な設計内容は以下の通りである：

1. **外部インターフェース**
   - ユーザー対話API（REST、GraphQL、WebSocket、SSE）
   - 外部システム統合API
   - データ取得インターフェース
   - サードパーティシステム連携インターフェース

2. **内部インターフェース**
   - マイクロサービス間通信（同期/非同期）
   - データモデルとスキーマ
   - 分析エンジンインターフェース
   - ワークフローと通知インターフェース
   - セキュリティとモニタリングインターフェース

この設計に基づく実装により、高精度な変化点検出と将来予測を実現し、企業の戦略的意思決定を支援する実用的システムの開発が可能となる。