# コンセンサスモデルの実装（パート3：コンセンサス基準と重み付け方法）

## コンセンサス基準の設計

コンセンサスモデルの効果的な運用には、適切なコンセンサス基準の設計が不可欠です。コンセンサス基準は、3つの視点（テクノロジー、マーケット、ビジネス）からの情報を統合し、最適な解釈と判断を導き出すための基準となります。このセクションでは、n8nを活用したコンセンサス基準の設計と実装方法について解説します。

### コンセンサス基準の基本原則

コンセンサス基準の設計にあたっては、以下の基本原則を考慮します：

1. **視点間の関係性の尊重**
   - マーケット視点の先行性
   - テクノロジー視点の基盤性
   - ビジネス視点の実効性

2. **多次元評価の統合**
   - 重要度評価
   - 確信度評価
   - 整合性評価

3. **静止点の明確な定義と検出**
   - 3つのレイヤの総合判定における最適解
   - 安定性と堅牢性の評価

4. **透明性と説明可能性の確保**
   - 判断プロセスの透明化
   - 判断根拠の明示

### 視点別の重み付け

3つの視点（テクノロジー、マーケット、ビジネス）には、それぞれ異なる役割と重要性があります。視点別の基本的な重み付けは以下の通りです：

| 視点 | 基本重み | 役割 | 重み付けの根拠 |
|------|----------|------|----------------|
| マーケット | 0.40 | 先行指標 | 市場の受容性・需要が基点となるため、やや高い重みを設定 |
| テクノロジー | 0.30 | 基盤 | 技術的実現可能性が基盤となるため、中程度の重みを設定 |
| ビジネス | 0.30 | 実効性評価 | 事業としての成立性を判断するため、中程度の重みを設定 |

ただし、これらの重みは固定ではなく、以下の要因によって動的に調整されます：

1. **トピックの性質**
   - 技術革新が中心のトピックではテクノロジー視点の重みを増加
   - 市場変化が中心のトピックではマーケット視点の重みを増加
   - ビジネスモデル変革が中心のトピックではビジネス視点の重みを増加

2. **変化の段階**
   - 初期段階ではテクノロジー視点とマーケット視点の重みを増加
   - 成長段階ではマーケット視点の重みを増加
   - 成熟段階ではビジネス視点の重みを増加

3. **確信度の差異**
   - 確信度の高い視点の重みを増加
   - 確信度の低い視点の重みを減少

### 評価要素の重み付け

重要度評価、確信度評価、整合性評価の各要素には、それぞれ異なる重みが設定されています。

#### 重要度評価の要素と重み

| 要素 | 重み | 説明 |
|------|------|------|
| 影響範囲 | 0.25 | 変化が影響を与える範囲の広さ |
| 変化の大きさ | 0.25 | 変化の量的・質的な大きさ |
| 戦略的関連性 | 0.30 | 組織の戦略目標との関連性 |
| 時間的緊急性 | 0.20 | 対応の緊急性 |

#### 確信度評価の要素と重み

| 要素 | 重み | 説明 |
|------|------|------|
| 情報源の信頼性 | 0.30 | 情報源の権威性や過去の正確性 |
| データ量 | 0.20 | 分析に使用されたデータの量 |
| 一貫性 | 0.30 | 複数の情報源や時点での一貫性 |
| 検証可能性 | 0.20 | 情報が独立に検証可能かどうか |

#### 整合性評価の要素と重み

| 要素 | 重み | 説明 |
|------|------|------|
| 視点間の一致度 | 0.40 | 異なる視点からの評価の一致度 |
| 論理的整合性 | 0.30 | 情報間の論理的な矛盾の有無 |
| 時間的整合性 | 0.20 | 時系列での整合性 |
| コンテキスト整合性 | 0.10 | より広いコンテキストとの整合性 |

### 閾値の設定

コンセンサスモデルでは、各評価要素に対して閾値を設定し、評価結果のレベル分けを行います。基本的な閾値は以下の通りです：

| レベル | 閾値 | 説明 |
|--------|------|------|
| 高 | 0.8以上 | 非常に高い評価 |
| 中高 | 0.6〜0.8 | やや高い評価 |
| 中 | 0.4〜0.6 | 中程度の評価 |
| 中低 | 0.2〜0.4 | やや低い評価 |
| 低 | 0.2未満 | 非常に低い評価 |

これらの閾値は、以下の要因によって調整されることがあります：

1. **トピックの重要性**
   - 重要なトピックでは閾値をやや厳しく設定
   - 一般的なトピックでは標準的な閾値を適用

2. **データの質と量**
   - データの質と量が高い場合は閾値を厳しく設定
   - データの質と量が低い場合は閾値を緩和

3. **意思決定の重要性**
   - 重要な意思決定に関わる場合は閾値を厳しく設定
   - 探索的な分析の場合は閾値を緩和

## 重み付け方法の実装

n8nを活用して、コンセンサス基準の重み付け方法を実装します。以下では、動的な重み付け調整を行うワークフローを示します。

```javascript
// n8n workflow: Dynamic Weight Adjustment
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "adjust-weights",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getTopicInfo",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get topic information
        SELECT
          t.id,
          t.name,
          t.description,
          t.keywords,
          t.perspective_id AS primary_perspective,
          (
            SELECT jsonb_agg(
              jsonb_build_object(
                'date', pe.date,
                'perspective_id', pe.perspective_id,
                'importance', pe.importance,
                'confidence', pe.confidence,
                'overall_score', pe.overall_score
              )
            )
            FROM perspective_evaluations pe
            WHERE pe.topic_id = t.id
            ORDER BY pe.date DESC
            LIMIT 10
          ) AS recent_evaluations
        FROM
          topics t
        WHERE
          t.id = '{{ $json.topic_id }}'
      `
    }
  },
  {
    "id": "getConsensusParameters",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get active consensus parameters
        SELECT parameters
        FROM consensus_parameters
        WHERE is_active = TRUE
        ORDER BY created_at DESC
        LIMIT 1
      `
    }
  },
  {
    "id": "adjustWeights",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const topicInfo = $input.item.json;
        const consensusParameters = $input.item.json.parameters;
        
        // Extract base weights
        const baseWeights = {
          technology: consensusParameters.perspectiveWeights.technology,
          market: consensusParameters.perspectiveWeights.market,
          business: consensusParameters.perspectiveWeights.business
        };
        
        // Adjust weights based on topic nature
        const adjustedWeights = adjustWeightsByTopicNature(baseWeights, topicInfo);
        
        // Adjust weights based on change stage
        const furtherAdjustedWeights = adjustWeightsByChangeStage(adjustedWeights, topicInfo);
        
        // Adjust weights based on confidence differences
        const finalWeights = adjustWeightsByConfidence(furtherAdjustedWeights, topicInfo);
        
        // Normalize weights to ensure they sum to 1.0
        const normalizedWeights = normalizeWeights(finalWeights);
        
        return {
          json: {
            topic_id: topicInfo.id,
            topic_name: topicInfo.name,
            base_weights: baseWeights,
            adjusted_weights: normalizedWeights,
            adjustment_factors: {
              topic_nature: getTopicNature(topicInfo),
              change_stage: getChangeStage(topicInfo),
              confidence_differences: getConfidenceDifferences(topicInfo)
            }
          }
        };
        
        // Helper function: Adjust weights by topic nature
        function adjustWeightsByTopicNature(weights, topicInfo) {
          const topicNature = getTopicNature(topicInfo);
          const adjustedWeights = {...weights};
          
          if (topicNature === 'technology_driven') {
            adjustedWeights.technology *= 1.2;
            adjustedWeights.market *= 0.9;
            adjustedWeights.business *= 0.9;
          } else if (topicNature === 'market_driven') {
            adjustedWeights.technology *= 0.9;
            adjustedWeights.market *= 1.2;
            adjustedWeights.business *= 0.9;
          } else if (topicNature === 'business_driven') {
            adjustedWeights.technology *= 0.9;
            adjustedWeights.market *= 0.9;
            adjustedWeights.business *= 1.2;
          }
          
          return adjustedWeights;
        }
        
        // Helper function: Get topic nature
        function getTopicNature(topicInfo) {
          // Determine topic nature based on primary perspective and keywords
          const primaryPerspective = topicInfo.primary_perspective;
          const keywords = topicInfo.keywords || [];
          
          // Technology-driven keywords
          const techKeywords = ['技術', '革新', 'AI', '人工知能', '機械学習', 'ブロックチェーン', 'IoT', '量子', '5G', '6G'];
          
          // Market-driven keywords
          const marketKeywords = ['市場', '顧客', 'ニーズ', 'トレンド', '競合', '需要', 'シェア', '成長', '普及'];
          
          // Business-driven keywords
          const businessKeywords = ['事業', '戦略', '収益', '利益', 'コスト', 'ROI', '投資', 'リスク', '組織'];
          
          // Count keyword matches
          let techCount = 0;
          let marketCount = 0;
          let businessCount = 0;
          
          for (const keyword of keywords) {
            if (techKeywords.some(k => keyword.includes(k))) techCount++;
            if (marketKeywords.some(k => keyword.includes(k))) marketCount++;
            if (businessKeywords.some(k => keyword.includes(k))) businessCount++;
          }
          
          // Determine nature based on keyword counts and primary perspective
          if (techCount > marketCount && techCount > businessCount) {
            return 'technology_driven';
          } else if (marketCount > techCount && marketCount > businessCount) {
            return 'market_driven';
          } else if (businessCount > techCount && businessCount > marketCount) {
            return 'business_driven';
          } else {
            // If counts are equal, use primary perspective
            return primaryPerspective ? \`\${primaryPerspective}_driven\` : 'balanced';
          }
        }
        
        // Helper function: Adjust weights by change stage
        function adjustWeightsByChangeStage(weights, topicInfo) {
          const changeStage = getChangeStage(topicInfo);
          const adjustedWeights = {...weights};
          
          if (changeStage === 'early') {
            adjustedWeights.technology *= 1.1;
            adjustedWeights.market *= 1.1;
            adjustedWeights.business *= 0.8;
          } else if (changeStage === 'growth') {
            adjustedWeights.technology *= 0.9;
            adjustedWeights.market *= 1.2;
            adjustedWeights.business *= 0.9;
          } else if (changeStage === 'mature') {
            adjustedWeights.technology *= 0.8;
            adjustedWeights.market *= 0.9;
            adjustedWeights.business *= 1.3;
          }
          
          return adjustedWeights;
        }
        
        // Helper function: Get change stage
        function getChangeStage(topicInfo) {
          // Determine change stage based on recent evaluations
          const recentEvaluations = topicInfo.recent_evaluations || [];
          
          if (recentEvaluations.length === 0) {
            return 'unknown';
          }
          
          // Analyze trends in evaluations
          let growthCount = 0;
          let stabilityCount = 0;
          
          for (let i = 1; i < recentEvaluations.length; i++) {
            const current = recentEvaluations[i - 1];
            const previous = recentEvaluations[i];
            
            // Compare market perspective scores
            const currentMarket = current.find(e => e.perspective_id === 'market');
            const previousMarket = previous.find(e => e.perspective_id === 'market');
            
            if (currentMarket && previousMarket) {
              const change = currentMarket.overall_score - previousMarket.overall_score;
              
              if (change > 0.1) {
                growthCount++;
              } else if (Math.abs(change) <= 0.05) {
                stabilityCount++;
              }
            }
          }
          
          // Determine stage based on growth and stability counts
          if (growthCount > recentEvaluations.length / 3) {
            return 'growth';
          } else if (stabilityCount > recentEvaluations.length / 2) {
            return 'mature';
          } else {
            return 'early';
          }
        }
        
        // Helper function: Adjust weights by confidence differences
        function adjustWeightsByConfidence(weights, topicInfo) {
          const confidenceDifferences = getConfidenceDifferences(topicInfo);
          const adjustedWeights = {...weights};
          
          // Boost weights of high-confidence perspectives
          for (const perspective in confidenceDifferences) {
            const confidenceDiff = confidenceDifferences[perspective];
            
            if (confidenceDiff > 0.2) {
              adjustedWeights[perspective] *= 1.1;
            } else if (confidenceDiff < -0.2) {
              adjustedWeights[perspective] *= 0.9;
            }
          }
          
          return adjustedWeights;
        }
        
        // Helper function: Get confidence differences
        function getConfidenceDifferences(topicInfo) {
          // Calculate confidence differences from average
          const recentEvaluations = topicInfo.recent_evaluations || [];
          
          if (recentEvaluations.length === 0) {
            return {
              technology: 0,
              market: 0,
              business: 0
            };
          }
          
          // Get most recent evaluation
          const latestEvaluation = recentEvaluations[0];
          
          // Extract confidence scores
          const confidenceScores = {
            technology: 0,
            market: 0,
            business: 0
          };
          
          let count = 0;
          
          for (const eval of latestEvaluation) {
            const perspectiveId = eval.perspective_id;
            if (perspectiveId in confidenceScores) {
              confidenceScores[perspectiveId] = eval.confidence.score;
              count++;
            }
          }
          
          if (count === 0) {
            return {
              technology: 0,
              market: 0,
              business: 0
            };
          }
          
          // Calculate average confidence
          const avgConfidence = (confidenceScores.technology + confidenceScores.market + confidenceScores.business) / count;
          
          // Calculate differences from average
          return {
            technology: confidenceScores.technology - avgConfidence,
            market: confidenceScores.market - avgConfidence,
            business: confidenceScores.business - avgConfidence
          };
        }
        
        // Helper function: Normalize weights
        function normalizeWeights(weights) {
          const sum = weights.technology + weights.market + weights.business;
          
          return {
            technology: weights.technology / sum,
            market: weights.market / sum,
            business: weights.business / sum
          };
        }
      `
    }
  },
  {
    "id": "saveAdjustedWeights",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create topic_weights table if not exists
        CREATE TABLE IF NOT EXISTS topic_weights (
          id SERIAL PRIMARY KEY,
          topic_id VARCHAR(50) NOT NULL,
          weights JSONB NOT NULL,
          adjustment_factors JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          
          CONSTRAINT unique_topic UNIQUE (topic_id)
        );
        
        -- Insert or update topic weights
        INSERT INTO topic_weights (
          topic_id,
          weights,
          adjustment_factors
        )
        VALUES (
          '{{ $json.topic_id }}',
          '{{ $json.adjusted_weights | json | replace("'", "''") }}'::jsonb,
          '{{ $json.adjustment_factors | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (topic_id)
        DO UPDATE SET
          weights = '{{ $json.adjusted_weights | json | replace("'", "''") }}'::jsonb,
          adjustment_factors = '{{ $json.adjustment_factors | json | replace("'", "''") }}'::jsonb,
          created_at = CURRENT_TIMESTAMP;
      `
    }
  }
]
```

このワークフローでは、トピックの性質、変化の段階、確信度の差異に基づいて、視点別の重みを動的に調整しています。調整された重みはデータベースに保存され、コンセンサス統合プロセスで使用されます。

## コンセンサス基準の適用

コンセンサス基準は、コンセンサスモデルの統合レイヤで適用されます。以下では、コンセンサス基準を適用するプロセスの概要を示します。

### 1. 視点別評価の取得

まず、3つの視点（テクノロジー、マーケット、ビジネス）からの評価結果を取得します。各視点の評価結果には、重要度評価、確信度評価、全体スコアが含まれます。

### 2. 整合性評価の取得

次に、3つの視点間の整合性評価結果を取得します。整合性評価には、視点間の一致度、論理的整合性、時間的整合性、コンテキスト整合性が含まれます。

### 3. トピック別の重み付け取得

トピックの性質、変化の段階、確信度の差異に基づいて調整された視点別の重みを取得します。

### 4. 重み付き統合スコアの計算

視点別の評価結果と重みを使用して、重み付き統合スコアを計算します。

```
統合スコア = (テクノロジー視点のスコア × テクノロジー視点の重み)
           + (マーケット視点のスコア × マーケット視点の重み)
           + (ビジネス視点のスコア × ビジネス視点の重み)
```

### 5. 整合性による調整

整合性評価結果に基づいて、統合スコアを調整します。整合性が高い場合はスコアを維持または強化し、整合性が低い場合はスコアを減少させます。

```
調整後統合スコア = 統合スコア × (0.7 + 0.3 × 整合性スコア)
```

### 6. 静止点の検出

調整後統合スコア、重要度、確信度、整合性に基づいて、静止点（最適解）を検出します。静止点の検出基準は以下の通りです：

- 調整後統合スコアが閾値（例：0.7）以上
- 重要度が閾値（例：0.6）以上
- 確信度が閾値（例：0.7）以上
- 整合性が閾値（例：0.65）以上

### 7. 代替解の生成

静止点が検出されない場合や、複数の解釈の可能性がある場合は、代替解を生成します。代替解は、異なる重み付けや視点の組み合わせに基づいて生成されます。

## コンセンサス基準の評価と最適化

コンセンサス基準は、定期的に評価され、最適化される必要があります。評価と最適化のプロセスは以下の通りです：

### 1. 予測精度の評価

コンセンサスモデルの予測結果と実際の結果を比較し、予測精度を評価します。

### 2. ユーザーフィードバックの収集

コンセンサスモデルの出力に対するユーザーフィードバックを収集し、モデルの有用性と正確性を評価します。

### 3. パラメータの最適化

予測精度とユーザーフィードバックに基づいて、コンセンサス基準のパラメータ（重み、閾値など）を最適化します。

### 4. モデルの更新

最適化されたパラメータを使用して、コンセンサスモデルを更新します。

このプロセスを繰り返すことで、コンセンサスモデルの精度と有用性を継続的に向上させることができます。

次のセクションでは、静止点検出のアルゴリズムと評価方法について詳細に解説します。
