# 情報分析と変化点検出の実装（パート2：基本的な変化点検出システム）

## 変化点検出システムの概要

変化点検出システムは、トリプルパースペクティブ型戦略AIレーダーの中核機能の一つであり、収集・分析したデータから重要な変化やシフトを検出する役割を担います。このシステムは、ビジネス環境の変化を早期に察知し、意思決定者に適切なタイミングで通知することで、戦略的な意思決定を支援します。

変化点検出システムの基本アーキテクチャは以下の通りです：

1. **データ前処理モジュール**
   - ノイズ除去
   - 正規化
   - 特徴抽出

2. **統計的変化点検出モジュール**
   - 時系列データの変化点検出
   - 異常値検出
   - トレンド変化検出

3. **意味的変化点検出モジュール**
   - コンテキスト考慮型変化検出
   - 意味的シフト分析
   - 関連性変化分析

4. **コンセンサスモジュール**
   - 複数検出結果の統合
   - 重要度評価
   - 確信度計算

## 基本的な変化点検出の実装

基本的な変化点検出は、主に統計的手法を用いて時系列データの変化を検出します。n8nを活用して、基本的な変化点検出システムを実装する方法を解説します。

### データ前処理ワークフロー

変化点検出の前に、データの前処理を行うワークフローです。

```javascript
// n8n workflow: Data Preprocessing for Change Detection
// Trigger: Schedule (Daily)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "0 1 * * *" // Daily at 1:00 AM
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
    "id": "getTimeSeriesData",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get time series data for the past 90 days
        SELECT
          date,
          topic_aggregations,
          perspective_aggregations
        FROM
          time_series_aggregations
        WHERE
          date <= '{{ $json.date }}'
          AND date >= (DATE '{{ $json.date }}' - INTERVAL '90 days')
        ORDER BY
          date ASC
      `
    }
  },
  {
    "id": "preprocessTimeSeriesData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const timeSeriesData = $input.item.json;
        
        // Extract topic time series
        const topicTimeSeries = {};
        
        for (const dataPoint of timeSeriesData) {
          const date = dataPoint.date;
          const topicAggs = dataPoint.topic_aggregations;
          
          for (const topic of topicAggs) {
            const topicId = topic.topic_id;
            
            if (!topicTimeSeries[topicId]) {
              topicTimeSeries[topicId] = {
                topic_id: topicId,
                topic_name: topic.topic_name,
                perspective_id: topic.perspective_id,
                data: []
              };
            }
            
            topicTimeSeries[topicId].data.push({
              date,
              content_count: parseInt(topic.content_count)
            });
          }
        }
        
        // Normalize and fill missing values
        const normalizedTopicTimeSeries = {};
        
        for (const topicId in topicTimeSeries) {
          const series = topicTimeSeries[topicId];
          const data = series.data;
          
          // Skip if less than 7 data points
          if (data.length < 7) continue;
          
          // Calculate statistics
          let sum = 0;
          let max = data[0].content_count;
          let min = data[0].content_count;
          
          for (const point of data) {
            sum += point.content_count;
            max = Math.max(max, point.content_count);
            min = Math.min(min, point.content_count);
          }
          
          const mean = sum / data.length;
          const range = max - min;
          
          // Normalize data
          const normalizedData = data.map(point => {
            // Avoid division by zero
            const normalizedValue = range > 0 
              ? (point.content_count - min) / range 
              : 0;
            
            return {
              date: point.date,
              raw_value: point.content_count,
              normalized_value: normalizedValue,
              z_score: mean > 0 
                ? (point.content_count - mean) / Math.sqrt(mean) // Using Poisson approximation
                : 0
            };
          });
          
          normalizedTopicTimeSeries[topicId] = {
            ...series,
            statistics: {
              mean,
              min,
              max,
              range
            },
            normalized_data: normalizedData
          };
        }
        
        return {json: {normalizedTopicTimeSeries}};
      `
    }
  },
  {
    "id": "savePreprocessedData",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create preprocessed_time_series table if not exists
        CREATE TABLE IF NOT EXISTS preprocessed_time_series (
          date DATE PRIMARY KEY,
          normalized_topic_time_series JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert or update preprocessed data
        INSERT INTO preprocessed_time_series (date, normalized_topic_time_series)
        VALUES (
          '{{ $json.date }}',
          '{{ $json.normalizedTopicTimeSeries | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (date) DO UPDATE
        SET
          normalized_topic_time_series = '{{ $json.normalizedTopicTimeSeries | json | replace("'", "''") }}'::jsonb,
          created_at = CURRENT_TIMESTAMP
      `
    }
  },
  {
    "id": "triggerChangePointDetection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/detect-change-points",
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

### 統計的変化点検出ワークフロー

統計的手法を用いて時系列データの変化点を検出するワークフローです。

```javascript
// n8n workflow: Statistical Change Point Detection
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "detect-change-points",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getPreprocessedData",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get preprocessed data for the target date
        SELECT
          date,
          normalized_topic_time_series
        FROM
          preprocessed_time_series
        WHERE
          date = '{{ $json.date }}'
      `
    }
  },
  {
    "id": "detectChangePoints",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const preprocessedData = $input.item.json;
        const date = preprocessedData.date;
        const normalizedTopicTimeSeries = preprocessedData.normalized_topic_time_series;
        
        // Detect change points for each topic
        const changePoints = {};
        
        for (const topicId in normalizedTopicTimeSeries) {
          const series = normalizedTopicTimeSeries[topicId];
          const normalizedData = series.normalized_data;
          
          // Skip if less than 14 data points (need history for detection)
          if (normalizedData.length < 14) continue;
          
          // Initialize change point results
          changePoints[topicId] = {
            topic_id: topicId,
            topic_name: series.topic_name,
            perspective_id: series.perspective_id,
            change_points: []
          };
          
          // 1. Detect level shifts using CUSUM
          const cusumResults = detectCUSUM(normalizedData);
          if (cusumResults.isChangePoint) {
            changePoints[topicId].change_points.push({
              type: 'level_shift',
              date: normalizedData[cusumResults.changePointIndex].date,
              confidence: cusumResults.confidence,
              before_mean: cusumResults.beforeMean,
              after_mean: cusumResults.afterMean,
              change_magnitude: cusumResults.changeMagnitude
            });
          }
          
          // 2. Detect trend changes
          const trendResults = detectTrendChange(normalizedData);
          if (trendResults.isChangePoint) {
            changePoints[topicId].change_points.push({
              type: 'trend_change',
              date: normalizedData[trendResults.changePointIndex].date,
              confidence: trendResults.confidence,
              before_trend: trendResults.beforeTrend,
              after_trend: trendResults.afterTrend,
              change_magnitude: trendResults.changeMagnitude
            });
          }
          
          // 3. Detect volatility changes
          const volatilityResults = detectVolatilityChange(normalizedData);
          if (volatilityResults.isChangePoint) {
            changePoints[topicId].change_points.push({
              type: 'volatility_change',
              date: normalizedData[volatilityResults.changePointIndex].date,
              confidence: volatilityResults.confidence,
              before_volatility: volatilityResults.beforeVolatility,
              after_volatility: volatilityResults.afterVolatility,
              change_magnitude: volatilityResults.changeMagnitude
            });
          }
          
          // 4. Detect outliers
          const outlierResults = detectOutliers(normalizedData);
          for (const outlier of outlierResults.outliers) {
            changePoints[topicId].change_points.push({
              type: 'outlier',
              date: normalizedData[outlier.index].date,
              confidence: outlier.confidence,
              expected_value: outlier.expectedValue,
              actual_value: outlier.actualValue,
              z_score: outlier.zScore
            });
          }
        }
        
        // Helper function: CUSUM change point detection
        function detectCUSUM(data) {
          const values = data.map(d => d.normalized_value);
          const n = values.length;
          
          // Parameters
          const h = 0.5; // Threshold for detection
          const k = 0.5; // Reference value (sensitivity parameter)
          
          // CUSUM calculation
          let maxCUSUM = 0;
          let maxIndex = -1;
          let cusum = 0;
          
          for (let i = 0; i < n; i++) {
            cusum = Math.max(0, cusum + values[i] - k);
            if (cusum > maxCUSUM) {
              maxCUSUM = cusum;
              maxIndex = i;
            }
          }
          
          // Determine if change point is significant
          const isChangePoint = maxCUSUM > h && maxIndex > 0 && maxIndex < n - 1;
          
          // Calculate statistics if change point detected
          let beforeMean = 0;
          let afterMean = 0;
          let changeMagnitude = 0;
          let confidence = 0;
          
          if (isChangePoint) {
            // Calculate means before and after change point
            for (let i = 0; i < maxIndex; i++) {
              beforeMean += values[i];
            }
            beforeMean /= maxIndex;
            
            for (let i = maxIndex; i < n; i++) {
              afterMean += values[i];
            }
            afterMean /= (n - maxIndex);
            
            // Calculate change magnitude and confidence
            changeMagnitude = Math.abs(afterMean - beforeMean);
            confidence = Math.min(1, changeMagnitude * 2); // Simple confidence calculation
          }
          
          return {
            isChangePoint,
            changePointIndex: maxIndex,
            beforeMean,
            afterMean,
            changeMagnitude,
            confidence
          };
        }
        
        // Helper function: Trend change detection
        function detectTrendChange(data) {
          const n = data.length;
          const halfPoint = Math.floor(n / 2);
          
          // Calculate trends in first and second half
          let beforeTrend = 0;
          for (let i = 1; i < halfPoint; i++) {
            beforeTrend += data[i].normalized_value - data[i-1].normalized_value;
          }
          beforeTrend /= (halfPoint - 1);
          
          let afterTrend = 0;
          for (let i = halfPoint + 1; i < n; i++) {
            afterTrend += data[i].normalized_value - data[i-1].normalized_value;
          }
          afterTrend /= (n - halfPoint - 1);
          
          // Calculate change magnitude and confidence
          const changeMagnitude = Math.abs(afterTrend - beforeTrend);
          const threshold = 0.05; // Minimum change to be considered significant
          const isChangePoint = changeMagnitude > threshold;
          const confidence = Math.min(1, changeMagnitude * 10); // Simple confidence calculation
          
          return {
            isChangePoint,
            changePointIndex: halfPoint,
            beforeTrend,
            afterTrend,
            changeMagnitude,
            confidence
          };
        }
        
        // Helper function: Volatility change detection
        function detectVolatilityChange(data) {
          const n = data.length;
          const halfPoint = Math.floor(n / 2);
          
          // Calculate volatility in first and second half
          let beforeSum = 0;
          let beforeMean = 0;
          for (let i = 0; i < halfPoint; i++) {
            beforeSum += data[i].normalized_value;
          }
          beforeMean = beforeSum / halfPoint;
          
          let beforeVolatility = 0;
          for (let i = 0; i < halfPoint; i++) {
            beforeVolatility += Math.pow(data[i].normalized_value - beforeMean, 2);
          }
          beforeVolatility = Math.sqrt(beforeVolatility / halfPoint);
          
          let afterSum = 0;
          let afterMean = 0;
          for (let i = halfPoint; i < n; i++) {
            afterSum += data[i].normalized_value;
          }
          afterMean = afterSum / (n - halfPoint);
          
          let afterVolatility = 0;
          for (let i = halfPoint; i < n; i++) {
            afterVolatility += Math.pow(data[i].normalized_value - afterMean, 2);
          }
          afterVolatility = Math.sqrt(afterVolatility / (n - halfPoint));
          
          // Calculate change magnitude and confidence
          const changeMagnitude = Math.abs(afterVolatility - beforeVolatility) / Math.max(0.001, beforeVolatility);
          const threshold = 0.5; // Minimum change to be considered significant
          const isChangePoint = changeMagnitude > threshold;
          const confidence = Math.min(1, changeMagnitude / 2); // Simple confidence calculation
          
          return {
            isChangePoint,
            changePointIndex: halfPoint,
            beforeVolatility,
            afterVolatility,
            changeMagnitude,
            confidence
          };
        }
        
        // Helper function: Outlier detection
        function detectOutliers(data) {
          const values = data.map(d => d.z_score);
          const n = values.length;
          const outliers = [];
          
          // Parameters
          const threshold = 2.5; // Z-score threshold for outlier detection
          
          // Detect outliers
          for (let i = 0; i < n; i++) {
            const zScore = values[i];
            if (Math.abs(zScore) > threshold) {
              // Calculate expected value based on neighboring points
              let expectedValue = 0;
              let count = 0;
              
              // Use up to 3 points before and after
              for (let j = Math.max(0, i - 3); j <= Math.min(n - 1, i + 3); j++) {
                if (j !== i) {
                  expectedValue += data[j].normalized_value;
                  count++;
                }
              }
              
              expectedValue /= count;
              
              outliers.push({
                index: i,
                zScore: zScore,
                expectedValue: expectedValue,
                actualValue: data[i].normalized_value,
                confidence: Math.min(1, (Math.abs(zScore) - threshold) / 3)
              });
            }
          }
          
          return {
            outliers
          };
        }
        
        return {
          json: {
            date,
            change_points: changePoints
          }
        };
      `
    }
  },
  {
    "id": "saveChangePoints",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create change_points table if not exists
        CREATE TABLE IF NOT EXISTS change_points (
          date DATE PRIMARY KEY,
          change_points JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert or update change points
        INSERT INTO change_points (date, change_points)
        VALUES (
          '{{ $json.date }}',
          '{{ $json.change_points | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (date) DO UPDATE
        SET
          change_points = '{{ $json.change_points | json | replace("'", "''") }}'::jsonb,
          created_at = CURRENT_TIMESTAMP
      `
    }
  },
  {
    "id": "triggerSemanticChangeDetection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/detect-semantic-changes",
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

## 意味的変化点検出の実装

意味的変化点検出は、コンテンツの意味的な変化を検出するための手法です。n8nとAIを組み合わせて、意味的変化点検出システムを実装する方法を解説します。

### 意味的変化点検出ワークフロー

コンテンツの意味的な変化を検出するワークフローです。

```javascript
// n8n workflow: Semantic Change Detection
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "detect-semantic-changes",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getDateRange",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get date range for analysis
        const targetDate = new Date($json.date);
        const startDate = new Date(targetDate);
        startDate.setDate(startDate.getDate() - 30); // 30 days before
        
        // Format as YYYY-MM-DD
        const formatDate = (date) => {
          const year = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const day = String(date.getDate()).padStart(2, '0');
          return \`\${year}-\${month}-\${day}\`;
        };
        
        const formattedTargetDate = formatDate(targetDate);
        const formattedStartDate = formatDate(startDate);
        
        return {
          json: {
            target_date: formattedTargetDate,
            start_date: formattedStartDate,
            start_timestamp: \`\${formattedStartDate}T00:00:00Z\`,
            end_timestamp: \`\${formattedTargetDate}T23:59:59Z\`
          }
        };
      `
    }
  },
  {
    "id": "getTopicContent",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get content for each topic in the date range
        WITH topic_content AS (
          SELECT
            t.id AS topic_id,
            t.name AS topic_name,
            t.perspective_id,
            c.id AS content_id,
            c.title,
            c.normalized_body,
            c.summary,
            c.published_at,
            c.collected_at
          FROM
            content c
          JOIN
            content_topics ct ON c.id = ct.content_id
          JOIN
            topics t ON ct.topic_id = t.id
          WHERE
            c.collected_at >= '{{ $json.start_timestamp }}'
            AND c.collected_at <= '{{ $json.end_timestamp }}'
        )
        SELECT
          topic_id,
          topic_name,
          perspective_id,
          jsonb_agg(
            jsonb_build_object(
              'content_id', content_id,
              'title', title,
              'normalized_body', normalized_body,
              'summary', summary,
              'published_at', published_at,
              'collected_at', collected_at
            )
            ORDER BY collected_at
          ) AS content_items
        FROM
          topic_content
        GROUP BY
          topic_id, topic_name, perspective_id
      `
    }
  },
  {
    "id": "detectSemanticChanges",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:8000/api/detect_semantic_changes",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_content",
            "value": "={{ $json }}"
          }
        ]
      }
    }
  },
  {
    "id": "processSemanticChanges",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const semanticChanges = $input.item.json.results;
        const targetDate = $input.item.json.target_date;
        
        // Process semantic changes
        const processedChanges = {};
        
        for (const topicId in semanticChanges) {
          const changes = semanticChanges[topicId];
          
          processedChanges[topicId] = {
            topic_id: changes.topic_id,
            topic_name: changes.topic_name,
            perspective_id: changes.perspective_id,
            semantic_changes: []
          };
          
          // Process each type of semantic change
          if (changes.topic_drift && changes.topic_drift.is_significant) {
            processedChanges[topicId].semantic_changes.push({
              type: 'topic_drift',
              confidence: changes.topic_drift.confidence,
              before_keywords: changes.topic_drift.before_keywords,
              after_keywords: changes.topic_drift.after_keywords,
              drift_magnitude: changes.topic_drift.magnitude
            });
          }
          
          if (changes.sentiment_shift && changes.sentiment_shift.is_significant) {
            processedChanges[topicId].semantic_changes.push({
              type: 'sentiment_shift',
              confidence: changes.sentiment_shift.confidence,
              before_sentiment: changes.sentiment_shift.before_sentiment,
              after_sentiment: changes.sentiment_shift.after_sentiment,
              shift_magnitude: changes.sentiment_shift.magnitude
            });
          }
          
          if (changes.narrative_change && changes.narrative_change.is_significant) {
            processedChanges[topicId].semantic_changes.push({
              type: 'narrative_change',
              confidence: changes.narrative_change.confidence,
              before_narrative: changes.narrative_change.before_narrative,
              after_narrative: changes.narrative_change.after_narrative,
              change_description: changes.narrative_change.description
            });
          }
          
          if (changes.entity_relationship_change && changes.entity_relationship_change.is_significant) {
            processedChanges[topicId].semantic_changes.push({
              type: 'entity_relationship_change',
              confidence: changes.entity_relationship_change.confidence,
              changed_entities: changes.entity_relationship_change.changed_entities,
              change_description: changes.entity_relationship_change.description
            });
          }
        }
        
        return {
          json: {
            date: targetDate,
            semantic_changes: processedChanges
          }
        };
      `
    }
  },
  {
    "id": "saveSemanticChanges",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create semantic_changes table if not exists
        CREATE TABLE IF NOT EXISTS semantic_changes (
          date DATE PRIMARY KEY,
          semantic_changes JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert or update semantic changes
        INSERT INTO semantic_changes (date, semantic_changes)
        VALUES (
          '{{ $json.date }}',
          '{{ $json.semantic_changes | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (date) DO UPDATE
        SET
          semantic_changes = '{{ $json.semantic_changes | json | replace("'", "''") }}'::jsonb,
          created_at = CURRENT_TIMESTAMP
      `
    }
  },
  {
    "id": "triggerConsensusFormation",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/form-consensus",
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

## 変化点検出システムの評価と最適化

変化点検出システムの性能を評価し、最適化するための方法を解説します。

### 評価指標

変化点検出システムの評価には、以下の指標が用いられます：

1. **検出精度**
   - 真陽性率（TPR）：実際の変化点を正しく検出できた割合
   - 偽陽性率（FPR）：変化点でないものを誤って検出した割合
   - F1スコア：精度と再現率の調和平均

2. **検出遅延**
   - 変化点発生から検出までの時間的遅延

3. **実用性指標**
   - 検出された変化点の重要度評価の正確さ
   - 検出結果の解釈可能性

### 最適化ワークフロー

変化点検出システムのパラメータを最適化するワークフローです。

```javascript
// n8n workflow: Change Detection Optimization
// Trigger: Manual
[
  {
    "id": "start",
    "type": "n8n-nodes-base.manualTrigger",
    "parameters": {}
  },
  {
    "id": "getHistoricalData",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get historical data for optimization
        SELECT
          date,
          normalized_topic_time_series
        FROM
          preprocessed_time_series
        ORDER BY
          date ASC
      `
    }
  },
  {
    "id": "getKnownChangePoints",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get manually labeled change points for evaluation
        SELECT
          *
        FROM
          labeled_change_points
      `
    }
  },
  {
    "id": "optimizeParameters",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const historicalData = $input.item.json;
        const labeledChangePoints = $input.item.json;
        
        // Parameter ranges to test
        const parameterRanges = {
          cusum_threshold: [0.3, 0.4, 0.5, 0.6, 0.7],
          cusum_sensitivity: [0.3, 0.4, 0.5, 0.6, 0.7],
          trend_threshold: [0.03, 0.04, 0.05, 0.06, 0.07],
          volatility_threshold: [0.3, 0.4, 0.5, 0.6, 0.7],
          outlier_threshold: [2.0, 2.5, 3.0, 3.5]
        };
        
        // Grid search for optimal parameters
        let bestParameters = {};
        let bestF1Score = 0;
        
        // Simplified grid search (in practice, this would be more comprehensive)
        for (const cusumThreshold of parameterRanges.cusum_threshold) {
          for (const cusumSensitivity of parameterRanges.cusum_sensitivity) {
            for (const trendThreshold of parameterRanges.trend_threshold) {
              for (const volatilityThreshold of parameterRanges.volatility_threshold) {
                for (const outlierThreshold of parameterRanges.outlier_threshold) {
                  // Create parameter set
                  const parameters = {
                    cusum_threshold: cusumThreshold,
                    cusum_sensitivity: cusumSensitivity,
                    trend_threshold: trendThreshold,
                    volatility_threshold: volatilityThreshold,
                    outlier_threshold: outlierThreshold
                  };
                  
                  // Evaluate parameters
                  const evaluationResults = evaluateParameters(
                    historicalData,
                    labeledChangePoints,
                    parameters
                  );
                  
                  // Update best parameters if better F1 score
                  if (evaluationResults.f1Score > bestF1Score) {
                    bestF1Score = evaluationResults.f1Score;
                    bestParameters = parameters;
                  }
                }
              }
            }
          }
        }
        
        // Helper function to evaluate parameters
        function evaluateParameters(historicalData, labeledChangePoints, parameters) {
          // In a real implementation, this would run the change detection algorithm
          // with the given parameters and compare results with labeled data
          
          // Placeholder for evaluation logic
          // This would calculate true positives, false positives, false negatives
          // and derive precision, recall, and F1 score
          
          // Simplified placeholder implementation
          const truePositives = 10;
          const falsePositives = 2;
          const falseNegatives = 3;
          
          const precision = truePositives / (truePositives + falsePositives);
          const recall = truePositives / (truePositives + falseNegatives);
          const f1Score = 2 * (precision * recall) / (precision + recall);
          
          return {
            precision,
            recall,
            f1Score
          };
        }
        
        return {
          json: {
            best_parameters: bestParameters,
            best_f1_score: bestF1Score
          }
        };
      `
    }
  },
  {
    "id": "saveOptimalParameters",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create change_detection_parameters table if not exists
        CREATE TABLE IF NOT EXISTS change_detection_parameters (
          id SERIAL PRIMARY KEY,
          parameters JSONB NOT NULL,
          f1_score FLOAT NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert optimal parameters
        INSERT INTO change_detection_parameters (parameters, f1_score)
        VALUES (
          '{{ $json.best_parameters | json | replace("'", "''") }}'::jsonb,
          {{ $json.best_f1_score }}
        )
      `
    }
  },
  {
    "id": "updateActiveParameters",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create active_parameters table if not exists
        CREATE TABLE IF NOT EXISTS active_parameters (
          id INTEGER PRIMARY KEY DEFAULT 1,
          parameters JSONB NOT NULL,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Update active parameters
        INSERT INTO active_parameters (id, parameters)
        VALUES (
          1,
          '{{ $json.best_parameters | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (id) DO UPDATE
        SET
          parameters = '{{ $json.best_parameters | json | replace("'", "''") }}'::jsonb,
          updated_at = CURRENT_TIMESTAMP
      `
    }
  }
]
```

## まとめ

このセクションでは、トリプルパースペクティブ型戦略AIレーダーの基本的な変化点検出システムの実装方法について解説しました。n8nを活用することで、データ前処理、統計的変化点検出、意味的変化点検出、システム評価と最適化を実装し、ビジネス環境の重要な変化を検出することができます。

次のセクションでは、コンセンサスモデルの実装方法について詳しく解説します。
