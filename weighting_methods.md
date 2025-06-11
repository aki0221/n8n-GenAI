# 重み付け方法の比較概念図

## 重み付け方法の比較（静的、動的、コンテキスト依存）

```mermaid
graph TB
    subgraph "重み付け方法の比較"
        subgraph "静的重み付け" 
            style 静的重み付け fill:#d4e6f1,stroke:#3498db,stroke-width:2px
            S1["静的重み付け<br>Static Weighting"]
            S2["特徴: 固定された重み係数<br>• 事前に決定<br>• 変更なし<br>• 単純明快"]
            S3["メリット<br>• 実装が容易<br>• 予測可能な結果<br>• 低計算コスト"]
            S4["デメリット<br>• 状況変化に対応不可<br>• 汎用性に欠ける<br>• 最適化が困難"]
            S5["適用シナリオ<br>• 安定した環境<br>• 単純な評価タスク<br>• リソース制約がある場合"]
            S6["実装複雑性: ★☆☆☆☆<br>(非常に簡単)"]
            
            S1 --> S2 --> S3 --> S4 --> S5 --> S6
        end
        
        subgraph "動的重み付け"
            style 動的重み付け fill:#d5f5e3,stroke:#2ecc71,stroke-width:2px
            D1["動的重み付け<br>Dynamic Weighting"]
            D2["特徴: 時間経過で変化する重み<br>• 定期的に更新<br>• パターン認識<br>• 適応的調整"]
            D3["メリット<br>• 環境変化に対応<br>• 精度向上<br>• 自動最適化"]
            D4["デメリット<br>• 実装が複雑<br>• 予測困難<br>• 計算コスト増加"]
            D5["適用シナリオ<br>• 変化する環境<br>• 時系列データ分析<br>• 長期的な評価"]
            D6["実装複雑性: ★★★☆☆<br>(中程度)"]
            
            D1 --> D2 --> D3 --> D4 --> D5 --> D6
        end
        
        subgraph "コンテキスト依存重み付け"
            style コンテキスト依存重み付け fill:#fdebd0,stroke:#f39c12,stroke-width:2px
            C1["コンテキスト依存重み付け<br>Context-Dependent Weighting"]
            C2["特徴: 状況に応じた重み調整<br>• コンテキスト認識<br>• 多要素考慮<br>• インテリジェント調整"]
            C3["メリット<br>• 高精度な評価<br>• 状況適応性<br>• 複雑な関係性の把握"]
            C4["デメリット<br>• 高度な実装<br>• 高計算コスト<br>• 説明困難性"]
            C5["適用シナリオ<br>• 複雑な意思決定<br>• 多様な要因が影響<br>• 高精度要求"]
            C6["実装複雑性: ★★★★★<br>(非常に複雑)"]
            
            C1 --> C2 --> C3 --> C4 --> C5 --> C6
        end
    end
    
    subgraph "実装フロー比較"
        style 実装フロー比較 fill:#f5f5f5,stroke:#333333,stroke-width:1px
        
        SF["静的実装<br>固定重み設定 → 評価実行"]
        DF["動的実装<br>初期重み設定 → 評価実行 → 結果分析 → 重み更新 → 再評価"]
        CF["コンテキスト依存実装<br>コンテキスト分析 → 状況判断 → 重み動的調整 → 評価実行 → フィードバック"]
        
        SF --> DF --> CF
    end
    
    subgraph "n8n実装複雑性"
        style n8n実装複雑性 fill:#f5f5f5,stroke:#333333,stroke-width:1px
        
        N1["静的: 単一Functionノード<br>固定パラメータ設定"]
        N2["動的: 複数ノード連携<br>Function + If + Database"]
        N3["コンテキスト依存: 複雑ワークフロー<br>Function + If + Database + HTTP + Switch"]
        
        N1 --> N2 --> N3
    end
    
    subgraph "選択ガイドライン"
        style 選択ガイドライン fill:#f5f5f5,stroke:#333333,stroke-width:1px
        
        G1["静的重み付け選択<br>• リソース制約あり<br>• 単純な評価<br>• 安定環境"]
        G2["動的重み付け選択<br>• 変化する環境<br>• 中程度の複雑さ<br>• 自動最適化希望"]
        G3["コンテキスト依存選択<br>• 複雑な意思決定<br>• リソース豊富<br>• 高精度要求"]
        
        G1 --> G2 --> G3
    end
```

## 重み付け方法の特性比較表

| 特性 | 静的重み付け | 動的重み付け | コンテキスト依存重み付け |
|------|------------|------------|-------------------|
| **定義** | 固定された重み係数を使用 | 時間経過で変化する重み | 状況に応じて調整される重み |
| **更新頻度** | 更新なし | 定期的/イベント駆動 | リアルタイム/状況変化時 |
| **入力依存性** | 入力に依存しない | 過去の結果に依存 | 現在のコンテキストに依存 |
| **実装複雑性** | 低 | 中 | 高 |
| **計算コスト** | 低 | 中 | 高 |
| **精度** | 基本的 | 向上 | 最高 |
| **適応性** | なし | 中程度 | 高 |
| **説明可能性** | 高 | 中 | 低〜中 |
| **n8n実装** | 単一Functionノード | 複数ノード連携 | 複雑ワークフロー |

## 重み付け方法の選択基準

重み付け方法の選択は、以下の要因に基づいて行うことが推奨されます：

1. **評価対象の性質**：
   - 安定した対象 → 静的重み付け
   - 時間変化する対象 → 動的重み付け
   - 複雑な相互作用を持つ対象 → コンテキスト依存重み付け

2. **利用可能なリソース**：
   - リソース制約あり → 静的重み付け
   - 中程度のリソース → 動的重み付け
   - リソース豊富 → コンテキスト依存重み付け

3. **精度要求**：
   - 基本的な精度で十分 → 静的重み付け
   - 向上した精度が必要 → 動的重み付け
   - 最高精度が必要 → コンテキスト依存重み付け

4. **実装の容易さ**：
   - 迅速な実装が必要 → 静的重み付け
   - 中程度の開発時間 → 動的重み付け
   - 長期的な開発が可能 → コンテキスト依存重み付け

## n8nでの実装アプローチ

### 静的重み付け実装
```javascript
// Functionノードでの実装例
const weights = {
  tech: 0.33,
  market: 0.33,
  business: 0.34
};

const scores = {
  tech: items.tech_score,
  market: items.market_score,
  business: items.business_score
};

// 重み付け計算
const weightedScore = 
  weights.tech * scores.tech + 
  weights.market * scores.market + 
  weights.business * scores.business;

return { weightedScore };
```

### 動的重み付け実装
```javascript
// Functionノードでの実装例（一部）
// 過去のデータに基づいて重みを調整
const baseWeights = {
  tech: 0.33,
  market: 0.33,
  business: 0.34
};

// 過去の結果から調整係数を計算
const adjustmentFactors = calculateAdjustmentFactors(historicalData);

// 重みの動的調整
const adjustedWeights = {
  tech: baseWeights.tech * adjustmentFactors.tech,
  market: baseWeights.market * adjustmentFactors.market,
  business: baseWeights.business * adjustmentFactors.business
};

// 正規化（合計が1になるように）
const sum = adjustedWeights.tech + adjustedWeights.market + adjustedWeights.business;
const normalizedWeights = {
  tech: adjustedWeights.tech / sum,
  market: adjustedWeights.market / sum,
  business: adjustedWeights.business / sum
};

// 重み付け計算
const weightedScore = 
  normalizedWeights.tech * scores.tech + 
  normalizedWeights.market * scores.market + 
  normalizedWeights.business * scores.business;

return { weightedScore, normalizedWeights };
```

### コンテキスト依存重み付け実装
```javascript
// Functionノードでの実装例（一部）
// コンテキスト情報の分析
const context = {
  topicNature: items.topic_nature,  // 技術駆動型、市場駆動型など
  changeStage: items.change_stage,  // 初期、成長期、成熟期など
  confidenceScores: {
    tech: items.tech_confidence,
    market: items.market_confidence,
    business: items.business_confidence
  },
  externalFactors: items.external_factors  // 外部要因（規制変更、市場混乱など）
};

// コンテキストに基づく重み調整ルール
const weightAdjustmentRules = {
  // 技術駆動型トピックでは技術視点の重みを増加
  techDriven: { tech: 1.5, market: 0.8, business: 0.7 },
  // 市場駆動型トピックでは市場視点の重みを増加
  marketDriven: { tech: 0.7, market: 1.5, business: 0.8 },
  // 初期段階では技術視点を重視
  earlyStage: { tech: 1.3, market: 0.9, business: 0.8 },
  // 成熟期ではビジネス視点を重視
  matureStage: { tech: 0.8, market: 0.9, business: 1.3 },
  // 確信度が低い視点の重みを減少
  lowConfidence: 0.7
};

// コンテキストに基づく重み調整
let contextualWeights = { tech: 0.33, market: 0.33, business: 0.34 };

// トピック性質に基づく調整
if (context.topicNature === 'tech_driven') {
  contextualWeights.tech *= weightAdjustmentRules.techDriven.tech;
  contextualWeights.market *= weightAdjustmentRules.techDriven.market;
  contextualWeights.business *= weightAdjustmentRules.techDriven.business;
} else if (context.topicNature === 'market_driven') {
  // 市場駆動型の調整...
}

// 変化段階に基づく調整
if (context.changeStage === 'early') {
  // 初期段階の調整...
}

// 確信度に基づく調整
if (context.confidenceScores.tech < 0.5) {
  contextualWeights.tech *= weightAdjustmentRules.lowConfidence;
}
// 他の視点の確信度調整...

// 外部要因の考慮
// ...

// 正規化
const sum = contextualWeights.tech + contextualWeights.market + contextualWeights.business;
const normalizedWeights = {
  tech: contextualWeights.tech / sum,
  market: contextualWeights.market / sum,
  business: contextualWeights.business / sum
};

// 重み付け計算
const weightedScore = 
  normalizedWeights.tech * scores.tech + 
  normalizedWeights.market * scores.market + 
  normalizedWeights.business * scores.business;

return { weightedScore, normalizedWeights, contextFactors: context };
```
