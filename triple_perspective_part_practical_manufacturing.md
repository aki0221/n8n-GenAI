# 実践：製造業向けAIレーダーの構築と運用（パート2：データソースと収集設定）

## 製造業向けAIレーダーのデータソース体系

トリプルパースペクティブ型戦略AIレーダーを製造業に適用するためには、テクノロジー、マーケット、ビジネスの3つの視点それぞれに関連する多様なデータソースを特定し、効率的に収集・統合する必要があります。本セクションでは、製造業向けAIレーダーに必要なデータソースとその収集設定について詳細に解説します。

### テクノロジー視点のデータソース

テクノロジー視点では、製造技術の進化、新技術の出現、技術的競争環境などを把握するためのデータソースが必要です。

#### 1. 内部技術データソース

1. **研究開発データ**
   - 研究プロジェクト管理システム
   - 実験結果データベース
   - 技術ロードマップ
   - 特許出願・管理システム

2. **製造技術データ**
   - 生産設備仕様データ
   - 製造プロセスパラメータ
   - 品質管理システムデータ
   - 設備メンテナンス履歴

3. **製品技術データ**
   - 製品設計データ（CAD/CAM）
   - 材料仕様データ
   - 製品テスト結果
   - 技術的問題報告

#### 2. 外部技術データソース

1. **特許・知財データ**
   - 特許データベース（USPTO、EPO、JPO等）
   - 技術論文データベース（IEEE、Scopus等）
   - オープンイノベーションプラットフォーム

2. **技術トレンドデータ**
   - 業界技術レポート
   - 技術カンファレンス発表
   - 技術ニュースフィード
   - 研究助成金データベース

3. **競合技術データ**
   - 競合他社の製品仕様
   - 競合他社の特許活動
   - リバースエンジニアリングレポート
   - 技術ベンチマーク情報

### マーケット視点のデータソース

マーケット視点では、顧客ニーズ、市場動向、競合状況などを把握するためのデータソースが必要です。

#### 1. 内部市場データソース

1. **販売データ**
   - 受注管理システム
   - 販売実績データベース
   - 顧客関係管理（CRM）システム
   - 販売予測システム

2. **顧客データ**
   - 顧客フィードバックシステム
   - 製品使用データ（IoTデバイスから）
   - カスタマーサポート記録
   - 顧客満足度調査

3. **マーケティングデータ**
   - キャンペーン効果測定データ
   - ウェブサイト分析データ
   - ソーシャルメディア分析
   - 製品認知度調査

#### 2. 外部市場データソース

1. **市場調査データ**
   - 業界市場レポート（Gartner、Forrester等）
   - 消費者行動調査
   - 市場セグメント分析
   - トレンド予測レポート

2. **競合情報**
   - 競合他社の財務報告
   - 競合他社の製品発表
   - 市場シェアデータ
   - 価格情報データベース

3. **マクロ経済指標**
   - GDP成長率
   - 製造業PMI
   - 消費者信頼感指数
   - 地域別経済指標

### ビジネス視点のデータソース

ビジネス視点では、収益性、コスト構造、サプライチェーン、規制環境などを把握するためのデータソースが必要です。

#### 1. 内部ビジネスデータソース

1. **財務データ**
   - 会計システム
   - 予算管理システム
   - コスト分析データベース
   - 投資収益率（ROI）分析

2. **サプライチェーンデータ**
   - 調達管理システム
   - 在庫管理システム
   - サプライヤー評価データ
   - 物流・輸送データ

3. **運用データ**
   - 生産計画システム
   - 資源利用率データ
   - エネルギー消費データ
   - 廃棄物管理データ

#### 2. 外部ビジネスデータソース

1. **業界ベンチマーク**
   - 業界平均コスト構造
   - 生産性指標
   - 品質ベンチマーク
   - 持続可能性指標

2. **規制・コンプライアンスデータ**
   - 法規制データベース
   - 環境規制更新
   - 労働安全衛生規制
   - 国際貿易規制

3. **サプライチェーン外部要因**
   - 原材料価格指数
   - 物流コスト指標
   - サプライヤー業界動向
   - 地政学的リスク指標

## データ収集設定とn8nワークフロー

製造業向けAIレーダーのデータ収集を効率的に行うためには、n8nを活用した自動化ワークフローの構築が効果的です。以下に、主要なデータ収集ワークフローの設計と実装例を示します。

### 1. 内部システムからのデータ収集ワークフロー

内部システム（ERP、MES、PLM、CRMなど）からのデータ収集は、AIレーダーの基盤となる重要なプロセスです。

#### ERPシステムからのデータ収集ワークフロー

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

#### MESシステムからの生産データ収集ワークフロー

製造実行システム（MES）からの生産データ収集は、製造プロセスの効率性や品質に関する重要な指標を提供します。

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

### 2. 外部データソースからの収集ワークフロー

外部データソースからの情報収集は、市場動向や技術トレンドを把握するために不可欠です。

#### 特許データベースからの技術トレンド収集ワークフロー

```javascript
// n8nワークフロー例：特許データベースからの技術トレンド収集

// トリガーノード：週次スケジュール
{
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "days",
              "hoursInterval": 0,
              "daysInterval": 7
            }
          ]
        }
      },
      "name": "Weekly Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    
    // 検索キーワード設定ノード
    {
      "parameters": {
        "jsCode": "// 製造業関連の技術キーワードリスト\nconst techKeywords = [\n  'additive manufacturing',\n  'industrial IoT',\n  'digital twin',\n  'predictive maintenance',\n  'smart factory',\n  'industrial robotics',\n  'manufacturing automation'\n];\n\n// 検索対象期間の設定\nconst today = new Date();\nconst lastMonth = new Date();\nlastMonth.setMonth(today.getMonth() - 1);\n\nconst fromDate = lastMonth.toISOString().split('T')[0];\nconst toDate = today.toISOString().split('T')[0];\n\n// 各キーワードに対する検索クエリを生成\nconst searchQueries = techKeywords.map(keyword => {\n  return {\n    keyword: keyword,\n    query: `?q=${encodeURIComponent(keyword)}&filing_date=${fromDate}:${toDate}`\n  };\n});\n\nreturn {json: {searchQueries}};"
      },
      "name": "Generate Search Queries",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    
    // 特許API呼び出しノード
    {
      "parameters": {
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "url": "=https://api.patents.example.com/search{{$json.query}}",
        "options": {
          "limit": 100
        }
      },
      "name": "Patent API Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        650,
        300
      ]
    },
    
    // データ分析ノード
    {
      "parameters": {
        "jsCode": "// 特許データの分析\nconst patentData = $input.item.json.results;\nconst keyword = $input.item.json.keyword;\n\n// 出願企業別の集計\nconst companyStats = {};\npatentData.forEach(patent => {\n  const company = patent.applicant_name || 'Unknown';\n  if (!companyStats[company]) {\n    companyStats[company] = 0;\n  }\n  companyStats[company]++;\n});\n\n// 技術分野別の集計\nconst fieldStats = {};\npatentData.forEach(patent => {\n  const field = patent.classification_code || 'Unclassified';\n  if (!fieldStats[field]) {\n    fieldStats[field] = 0;\n  }\n  fieldStats[field]++;\n});\n\n// 結果の集約\nreturn {\n  json: {\n    keyword: keyword,\n    total_patents: patentData.length,\n    company_distribution: companyStats,\n    field_distribution: fieldStats,\n    timestamp: new Date().toISOString()\n  }\n};"
      },
      "name": "Analyze Patent Data",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        850,
        300
      ]
    },
    
    // データ保存ノード
    {
      "parameters": {
        "operation": "insert",
        "schema": "radar_data",
        "table": "tech_trends",
        "columns": "keyword, total_patents, company_distribution, field_distribution, timestamp",
        "additionalFields": {}
      },
      "name": "Save Tech Trends",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        1050,
        300
      ]
    }
  ],
  "connections": {
    "Weekly Schedule": {
      "main": [
        [
          {
            "node": "Generate Search Queries",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Search Queries": {
      "main": [
        [
          {
            "node": "Patent API Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Patent API Request": {
      "main": [
        [
          {
            "node": "Analyze Patent Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Analyze Patent Data": {
      "main": [
        [
          {
            "node": "Save Tech Trends",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

#### 市場調査レポートからのマーケットトレンド収集ワークフロー

```javascript
// n8nワークフロー例：市場調査レポートからのマーケットトレンド収集

// トリガーノード：月次スケジュール
{
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "months",
              "daysInterval": 0,
              "monthsInterval": 1
            }
          ]
        }
      },
      "name": "Monthly Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    
    // 市場レポートAPI呼び出しノード
    {
      "parameters": {
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "url": "https://api.marketresearch.example.com/reports/manufacturing",
        "options": {
          "limit": 20
        }
      },
      "name": "Market Reports API",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    
    // レポート詳細取得ノード
    {
      "parameters": {
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "url": "=https://api.marketresearch.example.com/reports/{{$json.report_id}}/summary",
        "options": {}
      },
      "name": "Get Report Details",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        650,
        300
      ]
    },
    
    // テキスト分析ノード
    {
      "parameters": {
        "jsCode": "// レポート要約からのキーインサイト抽出\nconst reportData = $input.item.json;\nconst summary = reportData.summary || '';\n\n// キーワード出現頻度分析\nconst keywordCounts = {};\nconst keywords = [\n  'demand', 'growth', 'decline', 'innovation', 'competition',\n  'disruption', 'trend', 'emerging', 'consumer', 'regulation'\n];\n\nkeywords.forEach(keyword => {\n  const regex = new RegExp(keyword, 'gi');\n  const matches = summary.match(regex);\n  keywordCounts[keyword] = matches ? matches.length : 0;\n});\n\n// 市場成長率の抽出（例：「5.7% CAGR」のようなパターンを検索）\nlet growthRate = null;\nconst growthPattern = /(\\d+\\.?\\d*)\\s*%\\s*(?:CAGR|growth|annual)/i;\nconst growthMatch = summary.match(growthPattern);\nif (growthMatch) {\n  growthRate = parseFloat(growthMatch[1]);\n}\n\n// 市場規模の抽出（例：「$50 billion market」のようなパターンを検索）\nlet marketSize = null;\nconst sizePattern = /\\$(\\d+\\.?\\d*)\\s*(?:billion|million|trillion)/i;\nconst sizeMatch = summary.match(sizePattern);\nif (sizeMatch) {\n  marketSize = parseFloat(sizeMatch[1]);\n  // 単位の調整\n  if (sizeMatch[0].includes('billion')) {\n    marketSize *= 1000000000;\n  } else if (sizeMatch[0].includes('million')) {\n    marketSize *= 1000000;\n  } else if (sizeMatch[0].includes('trillion')) {\n    marketSize *= 1000000000000;\n  }\n}\n\nreturn {\n  json: {\n    report_id: reportData.report_id,\n    title: reportData.title,\n    publication_date: reportData.publication_date,\n    keyword_analysis: keywordCounts,\n    extracted_growth_rate: growthRate,\n    extracted_market_size: marketSize,\n    timestamp: new Date().toISOString()\n  }\n};"
      },
      "name": "Analyze Report Content",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        850,
        300
      ]
    },
    
    // データ保存ノード
    {
      "parameters": {
        "operation": "insert",
        "schema": "radar_data",
        "table": "market_trends",
        "columns": "report_id, title, publication_date, keyword_analysis, extracted_growth_rate, extracted_market_size, timestamp",
        "additionalFields": {}
      },
      "name": "Save Market Trends",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        1050,
        300
      ]
    }
  ],
  "connections": {
    "Monthly Schedule": {
      "main": [
        [
          {
            "node": "Market Reports API",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Market Reports API": {
      "main": [
        [
          {
            "node": "Get Report Details",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Report Details": {
      "main": [
        [
          {
            "node": "Analyze Report Content",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Analyze Report Content": {
      "main": [
        [
          {
            "node": "Save Market Trends",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### 3. IoTデバイスからのリアルタイムデータ収集ワークフロー

製造業では、IoTデバイスからのリアルタイムデータ収集が重要な役割を果たします。

```javascript
// n8nワークフロー例：IoTデバイスからのリアルタイムデータ収集

// トリガーノード：MQTTトリガー
{
  "nodes": [
    {
      "parameters": {
        "authentication": "basicAuth",
        "topic": "factory/sensors/#",
        "options": {
          "qos": 1
        }
      },
      "name": "MQTT Trigger",
      "type": "n8n-nodes-base.mqttTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    
    // メッセージパース・フィルタリングノード
    {
      "parameters": {
        "jsCode": "// IoTセンサーデータのパースと検証\nconst message = $input.item.json;\nlet parsedData;\n\ntry {\n  // JSONメッセージの場合\n  if (typeof message.payload === 'string') {\n    parsedData = JSON.parse(message.payload);\n  } else {\n    parsedData = message.payload;\n  }\n  \n  // 必須フィールドの検証\n  const requiredFields = ['device_id', 'timestamp', 'readings'];\n  const missingFields = requiredFields.filter(field => !parsedData[field]);\n  \n  if (missingFields.length > 0) {\n    // 必須フィールドが欠けている場合はスキップ\n    return {json: {valid: false, reason: `Missing fields: ${missingFields.join(', ')}`}};\n  }\n  \n  // タイムスタンプの検証と標準化\n  const timestamp = new Date(parsedData.timestamp);\n  if (isNaN(timestamp.getTime())) {\n    return {json: {valid: false, reason: 'Invalid timestamp'}};\n  }\n  \n  // センサー読み取り値の検証\n  if (!Array.isArray(parsedData.readings)) {\n    return {json: {valid: false, reason: 'Readings must be an array'}};\n  }\n  \n  // 有効なデータを返す\n  return {\n    json: {\n      valid: true,\n      device_id: parsedData.device_id,\n      device_type: parsedData.device_type || 'unknown',\n      location: parsedData.location || 'unknown',\n      timestamp: timestamp.toISOString(),\n      readings: parsedData.readings\n    }\n  };\n} catch (error) {\n  return {json: {valid: false, reason: `Parse error: ${error.message}`}};\n}"
      },
      "name": "Parse and Validate",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    
    // 条件分岐ノード
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.valid}}",
              "operation": "equal",
              "value2": "true"
            }
          ]
        }
      },
      "name": "Is Valid Data?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        650,
        300
      ]
    },
    
    // 異常値検出ノード
    {
      "parameters": {
        "jsCode": "// センサーデータの異常値検出\nconst data = $input.item.json;\nconst readings = data.readings;\n\n// センサータイプごとの正常範囲定義\nconst normalRanges = {\n  'temperature': { min: -10, max: 100 },\n  'pressure': { min: 0, max: 500 },\n  'vibration': { min: 0, max: 50 },\n  'humidity': { min: 0, max: 100 },\n  'noise': { min: 0, max: 120 }\n};\n\n// 異常値の検出\nconst anomalies = [];\nreadings.forEach(reading => {\n  const sensorType = reading.type;\n  const value = reading.value;\n  \n  // センサータイプの正常範囲が定義されている場合\n  if (normalRanges[sensorType]) {\n    const range = normalRanges[sensorType];\n    if (value < range.min || value > range.max) {\n      anomalies.push({\n        sensor_type: sensorType,\n        value: value,\n        min: range.min,\n        max: range.max,\n        deviation: value < range.min ? value - range.min : value - range.max\n      });\n    }\n  }\n});\n\n// 結果の返却\nreturn {\n  json: {\n    ...data,\n    has_anomalies: anomalies.length > 0,\n    anomalies: anomalies,\n    processed_at: new Date().toISOString()\n  }\n};"
      },
      "name": "Detect Anomalies",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        850,
        250
      ]
    },
    
    // データ保存ノード
    {
      "parameters": {
        "operation": "insert",
        "schema": "radar_data",
        "table": "iot_sensor_data",
        "columns": "device_id, device_type, location, timestamp, readings, has_anomalies, anomalies, processed_at",
        "additionalFields": {}
      },
      "name": "Save Sensor Data",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        1050,
        250
      ]
    },
    
    // 異常値アラートノード
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.has_anomalies}}",
              "operation": "equal",
              "value2": "true"
            }
          ]
        }
      },
      "name": "Has Anomalies?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        1250,
        250
      ]
    },
    
    // アラート送信ノード
    {
      "parameters": {
        "to": "operations@example.com",
        "subject": "=IoT Sensor Anomaly Alert: {{$json.device_id}} ({{$json.location}})",
        "text": "=Anomalies detected in sensor readings:\n\nDevice ID: {{$json.device_id}}\nDevice Type: {{$json.device_type}}\nLocation: {{$json.location}}\nTimestamp: {{$json.timestamp}}\n\nAnomalies:\n{{#each $json.anomalies}}\n- Sensor: {{this.sensor_type}}, Value: {{this.value}} (Normal range: {{this.min}} - {{this.max}})\n{{/each}}\n\nPlease investigate immediately.",
        "options": {
          "priority": "high"
        }
      },
      "name": "Send Alert Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 1,
      "position": [
        1450,
        200
      ]
    },
    
    // エラーログノード
    {
      "parameters": {
        "operation": "insert",
        "schema": "radar_data",
        "table": "data_collection_errors",
        "columns": "source, error_reason, raw_data, timestamp",
        "additionalFields": {}
      },
      "name": "Log Error",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        850,
        400
      ]
    }
  ],
  "connections": {
    "MQTT Trigger": {
      "main": [
        [
          {
            "node": "Parse and Validate",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse and Validate": {
      "main": [
        [
          {
            "node": "Is Valid Data?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Is Valid Data?": {
      "main": [
        [
          {
            "node": "Detect Anomalies",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Log Error",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Detect Anomalies": {
      "main": [
        [
          {
            "node": "Save Sensor Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Save Sensor Data": {
      "main": [
        [
          {
            "node": "Has Anomalies?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Has Anomalies?": {
      "main": [
        [
          {
            "node": "Send Alert Email",
            "type": "main",
            "index": 0
          }
        ],
        []
      ]
    }
  }
}
```

## データ統合と前処理のベストプラクティス

製造業向けAIレーダーのデータ収集を効果的に行うためのベストプラクティスを以下に示します。

### 1. データ統合のベストプラクティス

1. **共通データモデルの定義**
   - 異なるシステムからのデータを統一的に扱うための共通データモデルを定義
   - 各データソースからのマッピングルールを明確化
   - 標準化されたメタデータスキーマの採用

2. **増分データ収集の実装**
   - 全データの再取得ではなく、前回の収集以降に変更されたデータのみを取得
   - タイムスタンプや変更フラグを活用した効率的な収集
   - データ収集履歴の管理と追跡

3. **エラー処理と再試行メカニズム**
   - 一時的な接続エラーに対する指数バックオフ再試行
   - 永続的なエラーの適切なログ記録と通知
   - 部分的な失敗からの回復メカニズム

4. **データリネージの追跡**
   - データの出所と変換履歴の記録
   - 各データポイントの信頼性と鮮度の評価
   - 上流の変更がもたらす影響の追跡

### 2. データ前処理のベストプラクティス

1. **データクレンジング**
   - 欠損値の検出と処理（補完、削除、または特殊値での置換）
   - 外れ値の検出と処理
   - 重複データの排除

2. **データ標準化**
   - 単位の統一（メートル法への変換など）
   - 日付・時刻形式の標準化（ISO 8601形式の採用）
   - 名称や識別子の正規化

3. **特徴量エンジニアリング**
   - 製造業特有の派生指標の計算（OEE、MTBF、MTTRなど）
   - 時系列データからの傾向・季節性・周期性の抽出
   - テキストデータからのキーワードと感情の抽出

4. **データ集約**
   - 適切な時間粒度での集約（時間別、日別、週別など）
   - 製品、生産ライン、工場などの階層に沿った集約
   - 集約統計量の計算（平均、中央値、標準偏差、最小値、最大値など）

### 3. n8nを活用したデータパイプライン管理

1. **モジュール化されたワークフロー設計**
   - 機能ごとに分離されたワークフローの作成
   - 再利用可能なサブワークフローの定義
   - 共通処理の抽象化

2. **ワークフロー実行の監視と管理**
   - 実行ステータスとパフォーマンスの監視
   - エラー通知と自動リカバリー
   - 実行履歴の保存と分析

3. **データ品質チェックの組み込み**
   - 収集データの自動検証ルールの実装
   - 品質メトリクスの計算と追跡
   - 品質問題の自動通知

4. **スケーラビリティの確保**
   - 大量データ処理のためのバッチ処理
   - 並列実行の活用
   - リソース使用量の最適化

## データ収集設定のカスタマイズポイント

製造業向けAIレーダーのデータ収集設定は、企業の特性や目的に応じてカスタマイズする必要があります。以下に主要なカスタマイズポイントを示します。

### 1. 業種別のカスタマイズ

1. **自動車製造業**
   - 車両モデルのライフサイクルデータ
   - サプライヤー品質データ
   - 排出規制コンプライアンスデータ
   - コネクテッドカーからのフィードバックデータ

2. **電子機器製造業**
   - 部品サプライチェーンのリードタイムデータ
   - 製品ライフサイクルの短縮トレンド
   - 消費者技術採用率データ
   - 電子廃棄物とリサイクルデータ

3. **食品・飲料製造業**
   - 原材料価格と供給安定性データ
   - 消費者嗜好の変化データ
   - 食品安全規制データ
   - 賞味期限と在庫回転率データ

### 2. 企業規模別のカスタマイズ

1. **大企業向け**
   - グローバルデータソースの統合
   - 複数工場間のベンチマーキング
   - 複雑なサプライチェーンの可視化
   - 大規模なデータウェアハウスとの連携

2. **中小企業向け**
   - 限られたデータソースの最大活用
   - 低コストの外部データソースの活用
   - クラウドベースのデータ統合ソリューション
   - 段階的な実装アプローチ

### 3. 目的別のカスタマイズ

1. **コスト削減重視**
   - エネルギー消費データの詳細収集
   - 材料使用効率データ
   - 労働生産性データ
   - 設備稼働率データ

2. **品質向上重視**
   - 詳細な品質検査データ
   - 顧客クレームと返品データ
   - プロセス変動データ
   - サプライヤー品質評価データ

3. **イノベーション重視**
   - 研究開発パイプラインデータ
   - 特許・知財活動データ
   - 競合製品分析データ
   - 新技術採用トレンドデータ

## まとめ

製造業向けトリプルパースペクティブ型戦略AIレーダーの効果的な実装には、適切なデータソースの特定と効率的な収集設定が不可欠です。本セクションでは、テクノロジー、マーケット、ビジネスの3つの視点それぞれに関連するデータソースと、n8nを活用した収集ワークフローの実装例を示しました。

内部システム（ERP、MES、PLM、CRMなど）からのデータ、外部データソース（特許データベース、市場調査レポートなど）、IoTデバイスからのリアルタイムデータなど、多様なデータソースを統合することで、製造業の複雑な環境における戦略的意思決定を支援する包括的な情報基盤を構築できます。

データ統合と前処理のベストプラクティスを適用し、企業の特性や目的に応じたカスタマイズを行うことで、AIレーダーの有効性と価値を最大化することができます。

次のセクションでは、収集したデータを活用した視点別評価指標の設定について詳細に解説します。
