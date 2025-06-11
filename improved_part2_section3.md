# 実践：製造業向けAIレーダーの構築と運用（パート2：データソースと収集設定）

## データ収集設定とn8nワークフロー

製造業向けAIレーダーのデータ収集を効率的に行うためには、n8nを活用した自動化ワークフローの構築が効果的です。n8nは柔軟性が高く、様々なシステムとの連携が容易なため、製造業の複雑なシステム環境に適しています。

本セクションでは、主要なデータ収集ワークフローの設計と実装例を示すとともに、段階的な実装アプローチについても解説します。

### データ収集の段階的実装ガイド

製造業向けAIレーダーのデータ収集システムは、一度にすべてを構築するのではなく、段階的に実装することで、リスクを最小化しながら価値を早期に創出することができます。以下に、段階的な実装ステップを示します。

#### ステップ1：基盤構築とデータソース特定（1-2ヶ月）

初期段階では、AIレーダーの基盤となるデータ収集インフラを構築し、優先度の高いデータソースを特定します。

1. **データ収集基盤の構築**
   - n8nサーバーのセットアップと基本設定
   - データベーススキーマの設計と作成
   - 認証・セキュリティ設定の構成

2. **優先データソースの特定と接続**
   - 企業規模と業種に基づく優先データソースの選定
   - 内部システム（ERP、MES等）との接続設定
   - 基本的なデータ収集ワークフローの作成

3. **初期データモデルの定義**
   - 共通データモデルの設計
   - データマッピングルールの定義
   - メタデータ管理フレームワークの構築

#### ステップ2：内部データソース統合（2-3ヶ月）

次の段階では、社内の主要なデータソースを統合し、基本的なデータ収集ワークフローを確立します。

1. **主要内部システムの統合**
   - ERPシステムからの財務・生産データ収集ワークフロー実装
   - MESシステムからの品質・生産データ収集ワークフロー実装
   - PLM/PDMシステムからの製品データ収集ワークフロー実装

2. **データ前処理パイプラインの構築**
   - データクレンジングルーチンの実装
   - 標準化・正規化プロセスの確立
   - 基本的な特徴量エンジニアリングの実装

3. **初期ダッシュボードの作成**
   - 収集データの可視化設定
   - 基本的なKPI監視ダッシュボードの構築
   - データ品質モニタリングの実装

#### ステップ3：外部データソース拡張（2-3ヶ月）

内部データソースの統合が進んだ後、外部データソースを段階的に追加していきます。

1. **構造化外部データの統合**
   - 市場データAPIとの接続設定
   - 特許データベースとの連携ワークフロー実装
   - 業界レポートデータの収集自動化

2. **非構造化データ収集の実装**
   - ニュースフィードとソーシャルメディアの監視設定
   - テキスト分析パイプラインの構築
   - 画像・文書データの収集と処理

3. **データ統合レイヤーの強化**
   - 内部・外部データの統合モデルの拡張
   - クロスソースデータ検証の実装
   - メタデータ管理の強化

#### ステップ4：リアルタイムデータ統合（2-3ヶ月）

最終段階では、リアルタイムデータソースを統合し、AIレーダーの即時性を高めます。

1. **IoTデバイス統合**
   - センサーデータ収集ワークフローの実装
   - リアルタイムデータ処理パイプラインの構築
   - 異常検出システムの実装

2. **イベントドリブン処理の実装**
   - イベントベースのトリガー設定
   - リアルタイムアラートシステムの構築
   - 条件付きワークフロー分岐の実装

3. **システム最適化と拡張**
   - パフォーマンス監視と最適化
   - スケーラビリティの確保
   - 障害復旧メカニズムの強化

### 1. 内部システムからのデータ収集ワークフロー

内部システム（ERP、MES、PLM、CRMなど）からのデータ収集は、AIレーダーの基盤となる重要なプロセスです。これらのシステムは製造業の中核的な業務データを保持しており、戦略的意思決定の基礎となります。

#### ERPシステムからのデータ収集ワークフロー

ERPシステムは、財務、生産、調達、販売など、企業の基幹業務データを管理しています。これらのデータは、ビジネス視点とマーケット視点の分析に不可欠です。

```javascript
// n8nワークフロー例：ERPシステムからの財務・生産データ収集

// トリガーノード：スケジュール設定（毎日深夜に実行）
{
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "minutesInterval": 0,
              "hoursInterval": 24
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    
    // ERPシステム接続ノード（例：SAPシステム）
    {
      "parameters": {
        "authentication": "basicAuth",
        "url": "https://erp-api.example.com/financial-data",
        "options": {
          "timeout": 5000
        }
      },
      "name": "ERP API Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    
    // データ変換ノード
    {
      "parameters": {
        "jsCode": "// データ構造の標準化処理\nconst rawData = $input.item.json.data;\n\n// 日付フォーマットの統一\nconst processedData = rawData.map(item => {\n  return {\n    ...item,\n    date: new Date(item.timestamp).toISOString().split('T')[0],\n    revenue: parseFloat(item.revenue),\n    cost: parseFloat(item.cost),\n    profit_margin: parseFloat(item.revenue) - parseFloat(item.cost)\n  };\n});\n\nreturn {json: {data: processedData}};"
      },
      "name": "Transform Data",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        650,
        300
      ]
    },
    
    // データ保存ノード
    {
      "parameters": {
        "operation": "insert",
        "schema": "radar_data",
        "table": "financial_metrics",
        "columns": "date, revenue, cost, profit_margin, product_line, region",
        "additionalFields": {}
      },
      "name": "Save to Database",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        850,
        300
      ]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "ERP API Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "ERP API Request": {
      "main": [
        [
          {
            "node": "Transform Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Transform Data": {
      "main": [
        [
          {
            "node": "Save to Database",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

このワークフローは、毎日定時にERPシステムから財務データを取得し、データ形式を標準化した上でデータベースに保存します。製造業では、製品ライン別や地域別の収益性分析が重要であるため、これらの属性も含めてデータを構造化しています。

#### MESシステムからの生産データ収集ワークフロー

製造実行システム（MES）からの生産データ収集は、製造プロセスの効率性や品質に関する重要な指標を提供します。これらのデータは、テクノロジー視点とビジネス視点の分析に活用されます。

```javascript
// n8nワークフロー例：MESシステムからの生産データ収集

// トリガーノード：Webhookトリガー（生産バッチ完了時）
{
  "nodes": [
    {
      "parameters": {
        "path": "production-complete",
        "responseMode": "lastNode",
        "options": {}
      },
      "name": "Production Complete Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    
    // 追加データ取得ノード
    {
      "parameters": {
        "authentication": "basicAuth",
        "url": "=https://mes-api.example.com/batch-details/{{$json.batch_id}}",
        "options": {}
      },
      "name": "Get Batch Details",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    
    // 品質データ取得ノード
    {
      "parameters": {
        "authentication": "basicAuth",
        "url": "=https://mes-api.example.com/quality-data/{{$json.batch_id}}",
        "options": {}
      },
      "name": "Get Quality Data",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        450
      ]
    },
    
    // データ結合ノード
    {
      "parameters": {
        "mode": "merge",
        "mergeByFields": {
          "values": [
            {
              "field1": "batch_id",
              "field2": "batch_id"
            }
          ]
        },
        "options": {}
      },
      "name": "Merge Data",
      "type": "n8n-nodes-base.merge",
      "typeVersion": 2,
      "position": [
        650,
        375
      ]
    },
    
    // データ変換・エンリッチメントノード
    {
      "parameters": {
        "jsCode": "// 生産効率と品質指標の計算\nconst batchData = $input.item.json;\n\n// 生産効率の計算\nconst plannedTime = parseFloat(batchData.planned_production_time);\nconst actualTime = parseFloat(batchData.actual_production_time);\nconst efficiency = plannedTime > 0 ? (plannedTime / actualTime) * 100 : 0;\n\n// 品質指標の計算\nconst totalUnits = parseInt(batchData.total_units);\nconst defectiveUnits = parseInt(batchData.defective_units);\nconst qualityRate = totalUnits > 0 ? ((totalUnits - defectiveUnits) / totalUnits) * 100 : 0;\n\n// エネルギー効率の計算\nconst energyUsed = parseFloat(batchData.energy_consumption);\nconst energyPerUnit = totalUnits > 0 ? energyUsed / totalUnits : 0;\n\n// 結果の返却\nreturn {\n  json: {\n    ...batchData,\n    production_efficiency: efficiency.toFixed(2),\n    quality_rate: qualityRate.toFixed(2),\n    energy_per_unit: energyPerUnit.toFixed(4),\n    timestamp: new Date().toISOString()\n  }\n};"
      },
      "name": "Calculate Metrics",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        850,
        375
      ]
    },
    
    // データ保存ノード
    {
      "parameters": {
        "operation": "insert",
        "schema": "radar_data",
        "table": "production_metrics",
        "columns": "batch_id, product_id, production_line, production_efficiency, quality_rate, energy_per_unit, timestamp",
        "additionalFields": {}
      },
      "name": "Save Production Metrics",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        1050,
        375
      ]
    }
  ],
  "connections": {
    "Production Complete Webhook": {
      "main": [
        [
          {
            "node": "Get Batch Details",
            "type": "main",
            "index": 0
          },
          {
            "node": "Get Quality Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Batch Details": {
      "main": [
        [
          {
            "node": "Merge Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Quality Data": {
      "main": [
        [
          {
            "node": "Merge Data",
            "type": "main",
            "index": 1
          }
        ]
      ]
    },
    "Merge Data": {
      "main": [
        [
          {
            "node": "Calculate Metrics",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Calculate Metrics": {
      "main": [
        [
          {
            "node": "Save Production Metrics",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

このワークフローは、生産バッチが完了するたびにWebhookを通じて通知を受け取り、関連する詳細データと品質データを取得・結合します。さらに、生産効率、品質率、エネルギー効率などの重要KPIを計算し、データベースに保存します。製造業では、これらの指標が競争力と収益性に直結するため、リアルタイムでの把握が重要です。
