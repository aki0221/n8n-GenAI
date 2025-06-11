# 情報分析と変化点検出の実装（パート1：基本設計と分析フレームワーク）

## 情報分析システムの概要

トリプルパースペクティブ型戦略AIレーダーの中核となる情報分析システムは、収集したデータから意味のあるパターンや変化を検出し、ビジネス上の意思決定に役立つインサイトを生成する役割を担います。このセクションでは、n8nとAIを組み合わせた情報分析システムの実装方法について解説します。

情報分析システムの基本アーキテクチャは以下の通りです：

1. **分析フレームワーク**
   - トリプルパースペクティブ分析モデル
   - 時系列分析エンジン
   - パターン認識エンジン
   - 関連性分析エンジン

2. **変化点検出システム**
   - 統計的変化点検出
   - 意味的変化点検出
   - 複合変化点検出

3. **インサイト生成エンジン**
   - コンテキスト分析
   - 因果関係推論
   - インパクト評価

4. **アラートと通知システム**
   - 重要度評価
   - パーソナライズされた通知
   - アクション推奨

## トリプルパースペクティブ分析モデルの実装

トリプルパースペクティブ分析モデルは、テクノロジー、マーケット、ビジネスの3つの視点からデータを分析し、総合的な見解を生成するフレームワークです。

### 分析モデルの基本構造

トリプルパースペクティブ分析モデルの基本構造は以下の通りです：

```
トリプルパースペクティブ分析モデル
├── テクノロジー視点
│   ├── 技術トレンド分析
│   ├── 技術成熟度評価
│   ├── 技術採用率分析
│   └── 技術インパクト評価
├── マーケット視点
│   ├── 市場トレンド分析
│   ├── 競合分析
│   ├── 顧客ニーズ分析
│   └── 市場機会評価
└── ビジネス視点
    ├── 事業戦略適合性分析
    ├── 収益性分析
    ├── リソース要件分析
    └── リスク評価
```

### n8nによる分析モデルの実装

n8nを活用して、トリプルパースペクティブ分析モデルを実装します。

#### 分析モデル初期化ワークフロー

分析モデルの初期設定を行うワークフローです。

```javascript
// n8n workflow: Initialize Analysis Model
// Trigger: Manual
[
  {
    "id": "start",
    "type": "n8n-nodes-base.manualTrigger",
    "parameters": {},
    "typeVersion": 1
  },
  {
    "id": "createPerspectives",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Define the three perspectives
        const perspectives = [
          {
            id: 'technology',
            name: 'テクノロジー視点',
            description: '技術トレンド、成熟度、採用率、インパクトを分析',
            weight: 0.33,
            dimensions: [
              {
                id: 'tech_trends',
                name: '技術トレンド分析',
                description: '新興技術や技術トレンドの動向を分析',
                weight: 0.25
              },
              {
                id: 'tech_maturity',
                name: '技術成熟度評価',
                description: '技術の成熟度と実用性を評価',
                weight: 0.25
              },
              {
                id: 'tech_adoption',
                name: '技術採用率分析',
                description: '業界や市場における技術採用の状況を分析',
                weight: 0.25
              },
              {
                id: 'tech_impact',
                name: '技術インパクト評価',
                description: '技術がビジネスや市場に与える影響を評価',
                weight: 0.25
              }
            ]
          },
          {
            id: 'market',
            name: 'マーケット視点',
            description: '市場トレンド、競合、顧客ニーズ、市場機会を分析',
            weight: 0.33,
            dimensions: [
              {
                id: 'market_trends',
                name: '市場トレンド分析',
                description: '市場の動向や変化を分析',
                weight: 0.25
              },
              {
                id: 'competition',
                name: '競合分析',
                description: '競合企業の動向や戦略を分析',
                weight: 0.25
              },
              {
                id: 'customer_needs',
                name: '顧客ニーズ分析',
                description: '顧客の要求や行動の変化を分析',
                weight: 0.25
              },
              {
                id: 'market_opportunities',
                name: '市場機会評価',
                description: '新たな市場機会や成長領域を評価',
                weight: 0.25
              }
            ]
          },
          {
            id: 'business',
            name: 'ビジネス視点',
            description: '事業戦略、収益性、リソース要件、リスクを分析',
            weight: 0.34,
            dimensions: [
              {
                id: 'strategy_fit',
                name: '事業戦略適合性分析',
                description: '事業戦略との整合性を分析',
                weight: 0.25
              },
              {
                id: 'profitability',
                name: '収益性分析',
                description: '収益性や投資対効果を分析',
                weight: 0.25
              },
              {
                id: 'resource_requirements',
                name: 'リソース要件分析',
                description: '必要なリソースや能力を分析',
                weight: 0.25
              },
              {
                id: 'risk_assessment',
                name: 'リスク評価',
                description: 'リスクや不確実性を評価',
                weight: 0.25
              }
            ]
          }
        ];
        
        return {json: {perspectives}};
      `
    }
  },
  {
    "id": "savePerspectives",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create perspectives table if not exists
        CREATE TABLE IF NOT EXISTS perspectives (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(100) NOT NULL,
          description TEXT,
          weight FLOAT NOT NULL
        );
        
        -- Create dimensions table if not exists
        CREATE TABLE IF NOT EXISTS dimensions (
          id VARCHAR(50) PRIMARY KEY,
          perspective_id VARCHAR(50) NOT NULL REFERENCES perspectives(id),
          name VARCHAR(100) NOT NULL,
          description TEXT,
          weight FLOAT NOT NULL
        );
        
        -- Clear existing data
        DELETE FROM dimensions;
        DELETE FROM perspectives;
        
        -- Insert perspectives
        {% for perspective in $json.perspectives %}
        INSERT INTO perspectives (id, name, description, weight)
        VALUES (
          '{{ perspective.id }}',
          '{{ perspective.name }}',
          '{{ perspective.description }}',
          {{ perspective.weight }}
        );
        
        -- Insert dimensions for this perspective
        {% for dimension in perspective.dimensions %}
        INSERT INTO dimensions (id, perspective_id, name, description, weight)
        VALUES (
          '{{ dimension.id }}',
          '{{ perspective.id }}',
          '{{ dimension.name }}',
          '{{ dimension.description }}',
          {{ dimension.weight }}
        );
        {% endfor %}
        {% endfor %}
      `
    }
  },
  {
    "id": "createAnalysisRules",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Define analysis rules for each dimension
        const rules = [
          // Technology perspective rules
          {
            dimension_id: 'tech_trends',
            rules: [
              {
                id: 'emerging_tech_mention',
                name: '新興技術の言及',
                description: '新興技術に関する言及を検出',
                pattern: 'keyword_match',
                parameters: {
                  keywords: [
                    'AI', '人工知能', '機械学習', 'ブロックチェーン', 'IoT', '量子コンピューティング',
                    '5G', '6G', 'エッジコンピューティング', 'AR', 'VR', 'XR', 'メタバース',
                    'デジタルツイン', '自動運転', 'ロボティクス', '3Dプリンティング'
                  ],
                  threshold: 0.6
                },
                weight: 0.5
              },
              {
                id: 'tech_trend_growth',
                name: '技術トレンドの成長',
                description: '技術トレンドの言及頻度の増加を検出',
                pattern: 'frequency_change',
                parameters: {
                  min_change_rate: 0.2,
                  time_window_days: 30
                },
                weight: 0.5
              }
            ]
          },
          // More rules for other dimensions...
          {
            dimension_id: 'tech_maturity',
            rules: [
              {
                id: 'tech_maturity_indicators',
                name: '技術成熟度指標',
                description: '技術の成熟度を示す指標を検出',
                pattern: 'keyword_match',
                parameters: {
                  keywords: [
                    '実用化', '商用化', 'プロダクション', '標準化', '普及', '採用',
                    'PoC', '実証実験', 'パイロット', 'ベータ版', 'アルファ版', '研究段階'
                  ],
                  threshold: 0.6
                },
                weight: 0.5
              },
              {
                id: 'tech_maturity_change',
                name: '技術成熟度の変化',
                description: '技術の成熟度の変化を検出',
                pattern: 'sentiment_change',
                parameters: {
                  min_change: 0.2,
                  time_window_days: 90
                },
                weight: 0.5
              }
            ]
          }
          // More rules for other dimensions...
        ];
        
        return {json: {rules}};
      `
    }
  },
  {
    "id": "saveAnalysisRules",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create rules table if not exists
        CREATE TABLE IF NOT EXISTS analysis_rules (
          id VARCHAR(50) PRIMARY KEY,
          dimension_id VARCHAR(50) NOT NULL REFERENCES dimensions(id),
          name VARCHAR(100) NOT NULL,
          description TEXT,
          pattern VARCHAR(50) NOT NULL,
          parameters JSONB NOT NULL,
          weight FLOAT NOT NULL
        );
        
        -- Clear existing rules
        DELETE FROM analysis_rules;
        
        -- Insert rules
        {% for dimension_rules in $json.rules %}
        {% for rule in dimension_rules.rules %}
        INSERT INTO analysis_rules (id, dimension_id, name, description, pattern, parameters, weight)
        VALUES (
          '{{ rule.id }}',
          '{{ dimension_rules.dimension_id }}',
          '{{ rule.name }}',
          '{{ rule.description }}',
          '{{ rule.pattern }}',
          '{{ rule.parameters | json | replace("'", "''") }}'::jsonb,
          {{ rule.weight }}
        );
        {% endfor %}
        {% endfor %}
      `
    }
  },
  {
    "id": "createTopics",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Define example topics for analysis
        const topics = [
          // Technology topics
          {
            id: 'ai_ml',
            name: 'AI・機械学習',
            description: '人工知能と機械学習に関するトピック',
            keywords: ['AI', '人工知能', '機械学習', 'ディープラーニング', 'ニューラルネットワーク', 'LLM', '大規模言語モデル'],
            perspective_id: 'technology'
          },
          {
            id: 'blockchain',
            name: 'ブロックチェーン',
            description: 'ブロックチェーン技術に関するトピック',
            keywords: ['ブロックチェーン', '分散台帳', 'スマートコントラクト', 'NFT', '暗号資産', '仮想通貨'],
            perspective_id: 'technology'
          },
          // Market topics
          {
            id: 'digital_transformation',
            name: 'デジタルトランスフォーメーション',
            description: 'デジタルトランスフォーメーションに関するトピック',
            keywords: ['DX', 'デジタルトランスフォーメーション', 'デジタル化', 'デジタルシフト', 'ビジネス変革'],
            perspective_id: 'market'
          },
          {
            id: 'sustainability',
            name: 'サステナビリティ',
            description: '持続可能性に関するトピック',
            keywords: ['サステナビリティ', 'SDGs', 'ESG', '脱炭素', 'カーボンニュートラル', '再生可能エネルギー'],
            perspective_id: 'market'
          },
          // Business topics
          {
            id: 'remote_work',
            name: 'リモートワーク',
            description: 'リモートワークに関するトピック',
            keywords: ['リモートワーク', 'テレワーク', 'ハイブリッドワーク', 'ワークフロムホーム', '分散型組織'],
            perspective_id: 'business'
          },
          {
            id: 'supply_chain',
            name: 'サプライチェーン',
            description: 'サプライチェーンに関するトピック',
            keywords: ['サプライチェーン', 'ロジスティクス', '物流', '調達', 'SCM', 'サプライチェーン管理'],
            perspective_id: 'business'
          }
        ];
        
        return {json: {topics}};
      `
    }
  },
  {
    "id": "saveTopics",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create topics table if not exists
        CREATE TABLE IF NOT EXISTS topics (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(100) NOT NULL,
          description TEXT,
          keywords JSONB NOT NULL,
          perspective_id VARCHAR(50) NOT NULL REFERENCES perspectives(id)
        );
        
        -- Clear existing topics
        DELETE FROM topics;
        
        -- Insert topics
        {% for topic in $json.topics %}
        INSERT INTO topics (id, name, description, keywords, perspective_id)
        VALUES (
          '{{ topic.id }}',
          '{{ topic.name }}',
          '{{ topic.description }}',
          '{{ topic.keywords | json | replace("'", "''") }}'::jsonb,
          '{{ topic.perspective_id }}'
        );
        {% endfor %}
      `
    }
  }
]
```

## 時系列分析エンジンの実装

時系列分析エンジンは、収集したデータの時間的な変化を分析し、トレンドや周期性、異常値を検出する役割を担います。

### 時系列分析の基本設計

時系列分析エンジンの基本設計は以下の通りです：

1. **データ集約**
   - 時間単位でのデータ集約
   - トピック別のデータ集約
   - 視点別のデータ集約

2. **トレンド分析**
   - 移動平均の計算
   - トレンドの方向性検出
   - 変化率の計算

3. **周期性分析**
   - 周期パターンの検出
   - 季節性の分析
   - 周期的イベントの予測

4. **異常値検出**
   - 統計的異常値の検出
   - コンテキスト考慮型異常値検出
   - 複合異常パターンの検出

### n8nによる時系列分析の実装

n8nを活用して、時系列分析エンジンを実装します。

#### データ集約ワークフロー

収集したデータを時間単位で集約するワークフローです。

```javascript
// n8n workflow: Aggregate Time Series Data
// Trigger: Schedule (Daily)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "0 0 * * *" // Daily at midnight
    }
  },
  {
    "id": "getYesterdayDate",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get yesterday's date
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        
        // Format as YYYY-MM-DD
        const year = yesterday.getFullYear();
        const month = String(yesterday.getMonth() + 1).padStart(2, '0');
        const day = String(yesterday.getDate()).padStart(2, '0');
        
        const formattedDate = \`\${year}-\${month}-\${day}\`;
        
        return {
          json: {
            date: formattedDate,
            start_timestamp: \`\${formattedDate}T00:00:00Z\`,
            end_timestamp: \`\${formattedDate}T23:59:59Z\`
          }
        };
      `
    }
  },
  {
    "id": "aggregateContentByTopic",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Aggregate content by topic for yesterday
        WITH daily_content AS (
          SELECT
            c.id,
            c.title,
            c.normalized_body,
            c.published_at,
            c.collected_at,
            c.language,
            c.entities,
            c.keywords,
            c.summary
          FROM
            content c
          WHERE
            c.collected_at >= '{{ $json.start_timestamp }}'
            AND c.collected_at <= '{{ $json.end_timestamp }}'
        ),
        topic_content AS (
          SELECT
            t.id AS topic_id,
            t.name AS topic_name,
            t.perspective_id,
            dc.id AS content_id,
            dc.title,
            dc.summary,
            dc.published_at,
            dc.collected_at
          FROM
            daily_content dc
          JOIN
            content_topics ct ON dc.id = ct.content_id
          JOIN
            topics t ON ct.topic_id = t.id
        )
        SELECT
          topic_id,
          topic_name,
          perspective_id,
          COUNT(*) AS content_count,
          jsonb_agg(
            jsonb_build_object(
              'content_id', content_id,
              'title', title,
              'summary', summary,
              'published_at', published_at,
              'collected_at', collected_at
            )
          ) AS content_items
        FROM
          topic_content
        GROUP BY
          topic_id, topic_name, perspective_id
      `
    }
  },
  {
    "id": "aggregateByPerspective",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const topicAggregations = $input.item.json;
        
        // Group by perspective
        const perspectiveAggregations = {};
        
        for (const topic of topicAggregations) {
          const perspectiveId = topic.perspective_id;
          
          if (!perspectiveAggregations[perspectiveId]) {
            perspectiveAggregations[perspectiveId] = {
              perspective_id: perspectiveId,
              topic_count: 0,
              content_count: 0,
              topics: []
            };
          }
          
          perspectiveAggregations[perspectiveId].topic_count++;
          perspectiveAggregations[perspectiveId].content_count += parseInt(topic.content_count);
          perspectiveAggregations[perspectiveId].topics.push({
            topic_id: topic.topic_id,
            topic_name: topic.topic_name,
            content_count: parseInt(topic.content_count)
          });
        }
        
        // Convert to array
        const perspectiveArray = Object.values(perspectiveAggregations);
        
        return {
          json: {
            date: $input.item.json.date,
            topic_aggregations: topicAggregations,
            perspective_aggregations: perspectiveArray
          }
        };
      `
    }
  },
  {
    "id": "saveAggregations",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create time_series_aggregations table if not exists
        CREATE TABLE IF NOT EXISTS time_series_aggregations (
          date DATE PRIMARY KEY,
          topic_aggregations JSONB NOT NULL,
          perspective_aggregations JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert or update aggregation
        INSERT INTO time_series_aggregations (date, topic_aggregations, perspective_aggregations)
        VALUES (
          '{{ $json.date }}',
          '{{ $json.topic_aggregations | json | replace("'", "''") }}'::jsonb,
          '{{ $json.perspective_aggregations | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (date) DO UPDATE
        SET
          topic_aggregations = '{{ $json.topic_aggregations | json | replace("'", "''") }}'::jsonb,
          perspective_aggregations = '{{ $json.perspective_aggregations | json | replace("'", "''") }}'::jsonb,
          created_at = CURRENT_TIMESTAMP
      `
    }
  },
  {
    "id": "triggerTrendAnalysis",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/analyze-trends",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "date",
            "value": "={{ $json.date }}"
          }
        ]
      }
    }
  }
]
```

#### トレンド分析ワークフロー

時系列データからトレンドを分析するワークフローです。

```javascript
// n8n workflow: Analyze Trends
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "analyze-trends",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getRecentAggregations",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get recent aggregations (last 30 days)
        SELECT
          date,
          topic_aggregations,
          perspective_aggregations
        FROM
          time_series_aggregations
        WHERE
          date <= '{{ $json.date }}'
          AND date >= (DATE '{{ $json.date }}' - INTERVAL '30 days')
        ORDER BY
          date ASC
      `
    }
  },
  {
    "id": "calculateTopicTrends",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const aggregations = $input.item.json;
        
        // Extract all unique topics
        const allTopics = new Set();
        for (const agg of aggregations) {
          const topicAggs = agg.topic_aggregations;
          for (const topic of topicAggs) {
            allTopics.add(topic.topic_id);
          }
        }
        
        // Initialize topic time series
        const topicTimeSeries = {};
        for (const topicId of allTopics) {
          topicTimeSeries[topicId] = {
            topic_id: topicId,
            topic_name: '',
            perspective_id: '',
            time_series: []
          };
        }
        
        // Populate time series data
        for (const agg of aggregations) {
          const date = agg.date;
          const topicAggs = agg.topic_aggregations;
          
          // Set default value of 0 for all topics on this date
          for (const topicId of allTopics) {
            topicTimeSeries[topicId].time_series.push({
              date,
              content_count: 0
            });
          }
          
          // Update with actual values
          for (const topic of topicAggs) {
            const topicId = topic.topic_id;
            const lastIndex = topicTimeSeries[topicId].time_series.length - 1;
            
            topicTimeSeries[topicId].topic_name = topic.topic_name;
            topicTimeSeries[topicId].perspective_id = topic.perspective_id;
            topicTimeSeries[topicId].time_series[lastIndex].content_count = parseInt(topic.content_count);
          }
        }
        
        // Calculate trends
        const topicTrends = [];
        
        for (const topicId of allTopics) {
          const series = topicTimeSeries[topicId];
          const timeSeriesData = series.time_series;
          
          // Need at least 7 data points for meaningful trend analysis
          if (timeSeriesData.length < 7) continue;
          
          // Calculate 7-day moving average
          const movingAverages = [];
          for (let i = 6; i < timeSeriesData.length; i++) {
            let sum = 0;
            for (let j = i - 6; j <= i; j++) {
              sum += timeSeriesData[j].content_count;
            }
            const avg = sum / 7;
            movingAverages.push({
              date: timeSeriesData[i].date,
              value: avg
            });
          }
          
          // Calculate trend direction and strength
          let trendDirection = 0;
          let trendStrength = 0;
          
          if (movingAverages.length >= 2) {
            const firstMA = movingAverages[0].value;
            const lastMA = movingAverages[movingAverages.length - 1].value;
            
            // Avoid division by zero
            if (firstMA > 0) {
              const changeRate = (lastMA - firstMA) / firstMA;
              trendDirection = Math.sign(changeRate);
              trendStrength = Math.abs(changeRate);
            } else if (lastMA > 0) {
              // If starting from zero, any increase is positive
              trendDirection = 1;
              trendStrength = 1; // Arbitrary value for starting from zero
            }
          }
          
          topicTrends.push({
            topic_id: topicId,
            topic_name: series.topic_name,
            perspective_id: series.perspective_id,
            trend_direction: trendDirection,
            trend_strength: trendStrength,
            moving_averages: movingAverages,
            raw_data: timeSeriesData
          });
        }
        
        return {json: {topicTrends}};
      `
    }
  },
  {
    "id": "calculatePerspectiveTrends",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const aggregations = $input.item.json;
        const topicTrends = $input.item.json.topicTrends;
        
        // Extract all unique perspectives
        const allPerspectives = new Set();
        for (const agg of aggregations) {
          const perspectiveAggs = agg.perspective_aggregations;
          for (const perspective of perspectiveAggs) {
            allPerspectives.add(perspective.perspective_id);
          }
        }
        
        // Initialize perspective time series
        const perspectiveTimeSeries = {};
        for (const perspectiveId of allPerspectives) {
          perspectiveTimeSeries[perspectiveId] = {
            perspective_id: perspectiveId,
            time_series: []
          };
        }
        
        // Populate time series data
        for (const agg of aggregations) {
          const date = agg.date;
          const perspectiveAggs = agg.perspective_aggregations;
          
          // Set default value of 0 for all perspectives on this date
          for (const perspectiveId of allPerspectives) {
            perspectiveTimeSeries[perspectiveId].time_series.push({
              date,
              content_count: 0,
              topic_count: 0
            });
          }
          
          // Update with actual values
          for (const perspective of perspectiveAggs) {
            const perspectiveId = perspective.perspective_id;
            const lastIndex = perspectiveTimeSeries[perspectiveId].time_series.length - 1;
            
            perspectiveTimeSeries[perspectiveId].time_series[lastIndex].content_count = parseInt(perspective.content_count);
            perspectiveTimeSeries[perspectiveId].time_series[lastIndex].topic_count = parseInt(perspective.topic_count);
          }
        }
        
        // Calculate trends
        const perspectiveTrends = [];
        
        for (const perspectiveId of allPerspectives) {
          const series = perspectiveTimeSeries[perspectiveId];
          const timeSeriesData = series.time_series;
          
          // Need at least 7 data points for meaningful trend analysis
          if (timeSeriesData.length < 7) continue;
          
          // Calculate 7-day moving average for content count
          const contentMovingAverages = [];
          for (let i = 6; i < timeSeriesData.length; i++) {
            let sum = 0;
            for (let j = i - 6; j <= i; j++) {
              sum += timeSeriesData[j].content_count;
            }
            const avg = sum / 7;
            contentMovingAverages.push({
              date: timeSeriesData[i].date,
              value: avg
            });
          }
          
          // Calculate trend direction and strength
          let trendDirection = 0;
          let trendStrength = 0;
          
          if (contentMovingAverages.length >= 2) {
            const firstMA = contentMovingAverages[0].value;
            const lastMA = contentMovingAverages[contentMovingAverages.length - 1].value;
            
            // Avoid division by zero
            if (firstMA > 0) {
              const changeRate = (lastMA - firstMA) / firstMA;
              trendDirection = Math.sign(changeRate);
              trendStrength = Math.abs(changeRate);
            } else if (lastMA > 0) {
              // If starting from zero, any increase is positive
              trendDirection = 1;
              trendStrength = 1; // Arbitrary value for starting from zero
            }
          }
          
          perspectiveTrends.push({
            perspective_id: perspectiveId,
            trend_direction: trendDirection,
            trend_strength: trendStrength,
            content_moving_averages: contentMovingAverages,
            raw_data: timeSeriesData
          });
        }
        
        return {
          json: {
            topic_trends: topicTrends,
            perspective_trends: perspectiveTrends
          }
        };
      `
    }
  },
  {
    "id": "saveTrends",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create trends table if not exists
        CREATE TABLE IF NOT EXISTS trends (
          date DATE PRIMARY KEY,
          topic_trends JSONB NOT NULL,
          perspective_trends JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert or update trends
        INSERT INTO trends (date, topic_trends, perspective_trends)
        VALUES (
          '{{ $json.date }}',
          '{{ $json.topic_trends | json | replace("'", "''") }}'::jsonb,
          '{{ $json.perspective_trends | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (date) DO UPDATE
        SET
          topic_trends = '{{ $json.topic_trends | json | replace("'", "''") }}'::jsonb,
          perspective_trends = '{{ $json.perspective_trends | json | replace("'", "''") }}'::jsonb,
          created_at = CURRENT_TIMESTAMP
      `
    }
  },
  {
    "id": "triggerAnomalyDetection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/detect-anomalies",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "date",
            "value": "={{ $json.date }}"
          }
        ]
      }
    }
  }
]
```

## パターン認識エンジンの実装

パターン認識エンジンは、データ内の特定のパターンや関連性を検出し、意味のあるインサイトを生成する役割を担います。

### パターン認識の基本設計

パターン認識エンジンの基本設計は以下の通りです：

1. **キーワードベースのパターン認識**
   - キーワード出現頻度分析
   - キーワード共起分析
   - キーワードクラスタリング

2. **意味ベースのパターン認識**
   - トピックモデリング
   - 意味的類似性分析
   - コンテキスト分析

3. **時間的パターン認識**
   - イベントシーケンス分析
   - 周期的パターン検出
   - 因果関係分析

### n8nによるパターン認識の実装

n8nを活用して、パターン認識エンジンを実装します。

#### キーワード共起分析ワークフロー

キーワードの共起関係を分析するワークフローです。

```javascript
// n8n workflow: Keyword Co-occurrence Analysis
// Trigger: Schedule (Weekly)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "0 0 * * 0" // Weekly on Sunday
    }
  },
  {
    "id": "getDateRange",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get date range for the past week
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - 7);
        
        // Format as YYYY-MM-DD
        const formatDate = (date) => {
          const year = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const day = String(date.getDate()).padStart(2, '0');
          return \`\${year}-\${month}-\${day}\`;
        };
        
        const formattedStartDate = formatDate(startDate);
        const formattedEndDate = formatDate(endDate);
        
        return {
          json: {
            start_date: formattedStartDate,
            end_date: formattedEndDate,
            start_timestamp: \`\${formattedStartDate}T00:00:00Z\`,
            end_timestamp: \`\${formattedEndDate}T23:59:59Z\`
          }
        };
      `
    }
  },
  {
    "id": "getContentKeywords",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get content keywords for the past week
        SELECT
          c.id AS content_id,
          c.title,
          c.keywords,
          c.collected_at
        FROM
          content c
        WHERE
          c.collected_at >= '{{ $json.start_timestamp }}'
          AND c.collected_at <= '{{ $json.end_timestamp }}'
          AND c.keywords IS NOT NULL
          AND jsonb_array_length(c.keywords) > 0
      `
    }
  },
  {
    "id": "extractKeywordPairs",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const contentItems = $input.item.json;
        
        // Extract all keywords
        const allKeywords = new Set();
        const keywordPairs = {};
        
        for (const content of contentItems) {
          const keywords = content.keywords;
          
          // Skip if keywords is not an array
          if (!Array.isArray(keywords)) continue;
          
          // Extract keyword texts
          const contentKeywords = keywords.map(k => k.text.toLowerCase());
          
          // Add to all keywords set
          for (const keyword of contentKeywords) {
            allKeywords.add(keyword);
          }
          
          // Generate all pairs of keywords
          for (let i = 0; i < contentKeywords.length; i++) {
            for (let j = i + 1; j < contentKeywords.length; j++) {
              const keyword1 = contentKeywords[i];
              const keyword2 = contentKeywords[j];
              
              // Create a consistent key for the pair
              const pairKey = [keyword1, keyword2].sort().join('|');
              
              if (!keywordPairs[pairKey]) {
                keywordPairs[pairKey] = {
                  keyword1: keyword1,
                  keyword2: keyword2,
                  count: 0,
                  content_ids: []
                };
              }
              
              keywordPairs[pairKey].count++;
              keywordPairs[pairKey].content_ids.push(content.content_id);
            }
          }
        }
        
        // Convert to array and sort by count
        const keywordPairsArray = Object.values(keywordPairs)
          .sort((a, b) => b.count - a.count)
          .slice(0, 100); // Top 100 pairs
        
        return {
          json: {
            start_date: $input.item.json.start_date,
            end_date: $input.item.json.end_date,
            keyword_pairs: keywordPairsArray,
            keyword_count: allKeywords.size
          }
        };
      `
    }
  },
  {
    "id": "saveKeywordCooccurrence",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create keyword_cooccurrence table if not exists
        CREATE TABLE IF NOT EXISTS keyword_cooccurrence (
          id SERIAL PRIMARY KEY,
          start_date DATE NOT NULL,
          end_date DATE NOT NULL,
          keyword_pairs JSONB NOT NULL,
          keyword_count INTEGER NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert keyword co-occurrence data
        INSERT INTO keyword_cooccurrence (start_date, end_date, keyword_pairs, keyword_count)
        VALUES (
          '{{ $json.start_date }}',
          '{{ $json.end_date }}',
          '{{ $json.keyword_pairs | json | replace("'", "''") }}'::jsonb,
          {{ $json.keyword_count }}
        )
      `
    }
  },
  {
    "id": "generateKeywordNetwork",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {keyword_pairs} = $input.item.json;
        
        // Generate network data
        const nodes = new Set();
        const edges = [];
        
        for (const pair of keyword_pairs) {
          nodes.add(pair.keyword1);
          nodes.add(pair.keyword2);
          
          edges.push({
            source: pair.keyword1,
            target: pair.keyword2,
            weight: pair.count
          });
        }
        
        const network = {
          nodes: Array.from(nodes).map(keyword => ({
            id: keyword,
            label: keyword
          })),
          edges: edges
        };
        
        return {
          json: {
            start_date: $input.item.json.start_date,
            end_date: $input.item.json.end_date,
            network: network
          }
        };
      `
    }
  },
  {
    "id": "saveKeywordNetwork",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create keyword_networks table if not exists
        CREATE TABLE IF NOT EXISTS keyword_networks (
          id SERIAL PRIMARY KEY,
          start_date DATE NOT NULL,
          end_date DATE NOT NULL,
          network JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert keyword network data
        INSERT INTO keyword_networks (start_date, end_date, network)
        VALUES (
          '{{ $json.start_date }}',
          '{{ $json.end_date }}',
          '{{ $json.network | json | replace("'", "''") }}'::jsonb
        )
      `
    }
  }
]
```

## 関連性分析エンジンの実装

関連性分析エンジンは、異なるデータ間の関連性を分析し、隠れたパターンや関係性を検出する役割を担います。

### 関連性分析の基本設計

関連性分析エンジンの基本設計は以下の通りです：

1. **エンティティ関連性分析**
   - エンティティ抽出
   - エンティティ関係グラフ構築
   - 関連性スコアリング

2. **クロスパースペクティブ分析**
   - 視点間の関連性分析
   - 視点間のギャップ分析
   - 統合インサイト生成

3. **コンテキスト関連性分析**
   - コンテキスト抽出
   - コンテキスト間の関連性分析
   - コンテキスト拡張

### n8nによる関連性分析の実装

n8nを活用して、関連性分析エンジンを実装します。

#### エンティティ関連性分析ワークフロー

エンティティ間の関連性を分析するワークフローです。

```javascript
// n8n workflow: Entity Relationship Analysis
// Trigger: Schedule (Weekly)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "0 0 * * 1" // Weekly on Monday
    }
  },
  {
    "id": "getDateRange",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get date range for the past week
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - 7);
        
        // Format as YYYY-MM-DD
        const formatDate = (date) => {
          const year = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const day = String(date.getDate()).padStart(2, '0');
          return \`\${year}-\${month}-\${day}\`;
        };
        
        const formattedStartDate = formatDate(startDate);
        const formattedEndDate = formatDate(endDate);
        
        return {
          json: {
            start_date: formattedStartDate,
            end_date: formattedEndDate,
            start_timestamp: \`\${formattedStartDate}T00:00:00Z\`,
            end_timestamp: \`\${formattedEndDate}T23:59:59Z\`
          }
        };
      `
    }
  },
  {
    "id": "getContentEntities",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get content entities for the past week
        SELECT
          c.id AS content_id,
          c.title,
          c.entities,
          c.collected_at
        FROM
          content c
        WHERE
          c.collected_at >= '{{ $json.start_timestamp }}'
          AND c.collected_at <= '{{ $json.end_timestamp }}'
          AND c.entities IS NOT NULL
          AND jsonb_array_length(c.entities) > 0
      `
    }
  },
  {
    "id": "extractEntityRelationships",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const contentItems = $input.item.json;
        
        // Extract all entities
        const allEntities = new Set();
        const entityPairs = {};
        const entityTypes = {};
        
        for (const content of contentItems) {
          const entities = content.entities;
          
          // Skip if entities is not an array
          if (!Array.isArray(entities)) continue;
          
          // Extract entity texts and types
          const contentEntities = entities.map(e => ({
            text: e.text.toLowerCase(),
            type: e.type
          }));
          
          // Add to all entities set and track types
          for (const entity of contentEntities) {
            allEntities.add(entity.text);
            
            if (!entityTypes[entity.text]) {
              entityTypes[entity.text] = entity.type;
            }
          }
          
          // Generate all pairs of entities
          for (let i = 0; i < contentEntities.length; i++) {
            for (let j = i + 1; j < contentEntities.length; j++) {
              const entity1 = contentEntities[i].text;
              const entity2 = contentEntities[j].text;
              
              // Create a consistent key for the pair
              const pairKey = [entity1, entity2].sort().join('|');
              
              if (!entityPairs[pairKey]) {
                entityPairs[pairKey] = {
                  entity1: entity1,
                  entity2: entity2,
                  entity1_type: contentEntities[i].type,
                  entity2_type: contentEntities[j].type,
                  count: 0,
                  content_ids: []
                };
              }
              
              entityPairs[pairKey].count++;
              entityPairs[pairKey].content_ids.push(content.content_id);
            }
          }
        }
        
        // Convert to array and sort by count
        const entityPairsArray = Object.values(entityPairs)
          .sort((a, b) => b.count - a.count)
          .slice(0, 100); // Top 100 pairs
        
        return {
          json: {
            start_date: $input.item.json.start_date,
            end_date: $input.item.json.end_date,
            entity_pairs: entityPairsArray,
            entity_count: allEntities.size,
            entity_types: entityTypes
          }
        };
      `
    }
  },
  {
    "id": "saveEntityRelationships",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create entity_relationships table if not exists
        CREATE TABLE IF NOT EXISTS entity_relationships (
          id SERIAL PRIMARY KEY,
          start_date DATE NOT NULL,
          end_date DATE NOT NULL,
          entity_pairs JSONB NOT NULL,
          entity_count INTEGER NOT NULL,
          entity_types JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert entity relationship data
        INSERT INTO entity_relationships (start_date, end_date, entity_pairs, entity_count, entity_types)
        VALUES (
          '{{ $json.start_date }}',
          '{{ $json.end_date }}',
          '{{ $json.entity_pairs | json | replace("'", "''") }}'::jsonb,
          {{ $json.entity_count }},
          '{{ $json.entity_types | json | replace("'", "''") }}'::jsonb
        )
      `
    }
  },
  {
    "id": "generateEntityNetwork",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {entity_pairs, entity_types} = $input.item.json;
        
        // Generate network data
        const nodes = new Set();
        const edges = [];
        
        for (const pair of entity_pairs) {
          nodes.add(pair.entity1);
          nodes.add(pair.entity2);
          
          edges.push({
            source: pair.entity1,
            target: pair.entity2,
            weight: pair.count
          });
        }
        
        const network = {
          nodes: Array.from(nodes).map(entity => ({
            id: entity,
            label: entity,
            type: entity_types[entity] || 'UNKNOWN'
          })),
          edges: edges
        };
        
        return {
          json: {
            start_date: $input.item.json.start_date,
            end_date: $input.item.json.end_date,
            network: network
          }
        };
      `
    }
  },
  {
    "id": "saveEntityNetwork",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create entity_networks table if not exists
        CREATE TABLE IF NOT EXISTS entity_networks (
          id SERIAL PRIMARY KEY,
          start_date DATE NOT NULL,
          end_date DATE NOT NULL,
          network JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert entity network data
        INSERT INTO entity_networks (start_date, end_date, network)
        VALUES (
          '{{ $json.start_date }}',
          '{{ $json.end_date }}',
          '{{ $json.network | json | replace("'", "''") }}'::jsonb
        )
      `
    }
  }
]
```

## まとめ

このセクションでは、トリプルパースペクティブ型戦略AIレーダーの情報分析システムの基本設計と分析フレームワークの実装方法について解説しました。n8nを活用することで、トリプルパースペクティブ分析モデル、時系列分析エンジン、パターン認識エンジン、関連性分析エンジンを実装し、収集したデータから意味のあるパターンや変化を検出することができます。

次のセクションでは、変化点検出システムの実装方法について詳しく解説します。
