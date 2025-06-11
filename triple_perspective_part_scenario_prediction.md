# シナリオ生成と予測の活用（パート3-1：シナリオ生成メカニズム）

## シナリオ生成の基本概念

トリプルパースペクティブ型戦略AIレーダーにおいて、シナリオ生成は単なる予測値の提示を超えた重要な機能です。シナリオ生成とは、複数の可能性のある未来状態を構造化された形で提示し、意思決定者が不確実性を考慮した戦略立案を行えるようにするプロセスです。本セクションでは、n8nを活用したシナリオ生成メカニズムの実装について詳細に解説します。

### シナリオ生成の目的と価値

シナリオ生成には以下のような目的と価値があります：

1. **不確実性の構造化**: 未来の不確実性を単一の予測値ではなく、複数の可能性として構造化して提示
2. **リスク認識の向上**: 潜在的なリスクとチャンスを明示的に可視化
3. **意思決定の堅牢性**: 複数のシナリオに対して堅牢な戦略を立案可能に
4. **思考の拡張**: 意思決定者の思考範囲を広げ、盲点を減少

特にトリプルパースペクティブ（テクノロジー、マーケット、ビジネス）の視点を持つAIレーダーでは、各視点の相互作用から生まれる複雑なシナリオを生成し、多角的な分析を可能にします。

### シナリオ生成の基本アプローチ

シナリオ生成には主に以下の3つのアプローチがあります：

1. **確率論的シナリオ生成**: 確率分布に基づいて複数のシナリオを生成
2. **構造的シナリオ生成**: 重要な不確実性要因の組み合わせに基づいてシナリオを構造化
3. **ナラティブシナリオ生成**: ストーリーテリングの手法を用いて、論理的に一貫したシナリオを構築

トリプルパースペクティブ型戦略AIレーダーでは、これらのアプローチを組み合わせることで、より包括的で実用的なシナリオを生成します。

## 確率論的シナリオ生成の実装

確率論的シナリオ生成は、予測モデルの出力する確率分布に基づいて複数のシナリオを生成する手法です。n8nを使用した確率論的シナリオ生成の実装例を示します。

```javascript
// n8n workflow: Probabilistic Scenario Generation
// Function node for generating probabilistic scenarios
[
  {
    "id": "loadPredictionResults",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "integrated_results",
      "filter": {
        "execution_id": "={{ $node[\"loadExecutionId\"].json.execution_id }}"
      },
      "options": {
        "sort": {
          "timestamp": -1
        }
      }
    }
  },
  {
    "id": "generateProbabilisticScenarios",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get prediction results
        const predictionResults = $input.item.json;
        const finalResult = predictionResults.final_result;
        const executionId = predictionResults.execution_id;
        
        // Extract prediction and confidence
        const prediction = finalResult.final_prediction;
        const confidence = finalResult.confidence;
        
        // Generate probabilistic scenarios
        const generateScenarios = () => {
          // Calculate standard deviation based on confidence
          // Lower confidence means higher standard deviation (more uncertainty)
          const stdDev = (1 - confidence) * prediction * 0.5;
          
          // Generate scenarios based on normal distribution
          const scenarios = [];
          
          // Base scenario (expected)
          scenarios.push({
            type: 'expected',
            value: prediction,
            probability: 0.5,
            description: '最も可能性の高い予測シナリオ'
          });
          
          // Optimistic scenario (+1 std dev)
          scenarios.push({
            type: 'optimistic',
            value: prediction + stdDev,
            probability: 0.16,
            description: '楽観的シナリオ（上位16%の確率）'
          });
          
          // Very optimistic scenario (+2 std dev)
          scenarios.push({
            type: 'very_optimistic',
            value: prediction + (2 * stdDev),
            probability: 0.025,
            description: '非常に楽観的シナリオ（上位2.5%の確率）'
          });
          
          // Pessimistic scenario (-1 std dev)
          scenarios.push({
            type: 'pessimistic',
            value: prediction - stdDev,
            probability: 0.16,
            description: '悲観的シナリオ（下位16%の確率）'
          });
          
          // Very pessimistic scenario (-2 std dev)
          scenarios.push({
            type: 'very_pessimistic',
            value: prediction - (2 * stdDev),
            probability: 0.025,
            description: '非常に悲観的シナリオ（下位2.5%の確率）'
          });
          
          return scenarios;
        };
        
        const scenarios = generateScenarios();
        
        return {
          json: {
            execution_id: executionId,
            prediction: prediction,
            confidence: confidence,
            scenario_type: 'probabilistic',
            scenarios: scenarios,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveProbabilisticScenarios",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "scenarios",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## 構造的シナリオ生成の実装

構造的シナリオ生成は、重要な不確実性要因の組み合わせに基づいてシナリオを構造化する手法です。トリプルパースペクティブ型戦略AIレーダーでは、テクノロジー、マーケット、ビジネスの3つの視点から重要な不確実性要因を特定し、それらの組み合わせに基づいてシナリオを生成します。n8nを使用した構造的シナリオ生成の実装例を示します。

```javascript
// n8n workflow: Structural Scenario Generation
// Function node for generating structural scenarios
[
  {
    "id": "loadPerspectiveData",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "find",
      "collection": "perspective_analysis",
      "filter": {
        "execution_id": "={{ $node[\"loadExecutionId\"].json.execution_id }}"
      }
    }
  },
  {
    "id": "identifyUncertaintyFactors",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get perspective data
        const perspectiveData = $input.items.map(item => item.json);
        const executionId = perspectiveData[0].execution_id;
        
        // Identify key uncertainty factors for each perspective
        const identifyFactors = () => {
          const factors = {
            technology: [],
            market: [],
            business: []
          };
          
          // Process technology perspective
          const techData = perspectiveData.find(p => p.perspective === 'technology');
          if (techData) {
            // Extract factors with high uncertainty (low confidence)
            techData.factors.forEach(factor => {
              if (factor.confidence < 0.6) {
                factors.technology.push({
                  name: factor.name,
                  current_value: factor.value,
                  uncertainty: 1 - factor.confidence,
                  possible_states: [
                    { state: 'high', value: factor.value * 1.5, description: factor.name + 'が高い状態' },
                    { state: 'medium', value: factor.value, description: factor.name + 'が中程度の状態' },
                    { state: 'low', value: factor.value * 0.5, description: factor.name + 'が低い状態' }
                  ]
                });
              }
            });
          }
          
          // Process market perspective
          const marketData = perspectiveData.find(p => p.perspective === 'market');
          if (marketData) {
            // Extract factors with high uncertainty (low confidence)
            marketData.factors.forEach(factor => {
              if (factor.confidence < 0.6) {
                factors.market.push({
                  name: factor.name,
                  current_value: factor.value,
                  uncertainty: 1 - factor.confidence,
                  possible_states: [
                    { state: 'high', value: factor.value * 1.5, description: factor.name + 'が高い状態' },
                    { state: 'medium', value: factor.value, description: factor.name + 'が中程度の状態' },
                    { state: 'low', value: factor.value * 0.5, description: factor.name + 'が低い状態' }
                  ]
                });
              }
            });
          }
          
          // Process business perspective
          const businessData = perspectiveData.find(p => p.perspective === 'business');
          if (businessData) {
            // Extract factors with high uncertainty (low confidence)
            businessData.factors.forEach(factor => {
              if (factor.confidence < 0.6) {
                factors.business.push({
                  name: factor.name,
                  current_value: factor.value,
                  uncertainty: 1 - factor.confidence,
                  possible_states: [
                    { state: 'high', value: factor.value * 1.5, description: factor.name + 'が高い状態' },
                    { state: 'medium', value: factor.value, description: factor.name + 'が中程度の状態' },
                    { state: 'low', value: factor.value * 0.5, description: factor.name + 'が低い状態' }
                  ]
                });
              }
            });
          }
          
          return factors;
        };
        
        const uncertaintyFactors = identifyFactors();
        
        // Select top 2 uncertainty factors from each perspective
        const selectTopFactors = (factors, count) => {
          const result = {};
          
          Object.keys(factors).forEach(perspective => {
            // Sort by uncertainty (descending)
            const sorted = [...factors[perspective]].sort((a, b) => b.uncertainty - a.uncertainty);
            // Select top factors
            result[perspective] = sorted.slice(0, count);
          });
          
          return result;
        };
        
        const topFactors = selectTopFactors(uncertaintyFactors, 2);
        
        return {
          json: {
            execution_id: executionId,
            uncertainty_factors: uncertaintyFactors,
            top_factors: topFactors,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "generateStructuralScenarios",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get top uncertainty factors
        const data = $input.item.json;
        const topFactors = data.top_factors;
        const executionId = data.execution_id;
        
        // Generate structural scenarios
        const generateScenarios = () => {
          // Select one top factor from each perspective
          const techFactor = topFactors.technology[0];
          const marketFactor = topFactors.market[0];
          const businessFactor = topFactors.business[0];
          
          // Generate scenarios based on combinations of factor states
          const scenarios = [];
          
          // Define key scenarios
          
          // Scenario 1: All factors high
          scenarios.push({
            id: 'scenario_1',
            name: '全要素高成長シナリオ',
            description: 'テクノロジー、マーケット、ビジネスの全ての要素が高い成長を示すシナリオ',
            factors: [
              { perspective: 'technology', factor: techFactor.name, state: 'high' },
              { perspective: 'market', factor: marketFactor.name, state: 'high' },
              { perspective: 'business', factor: businessFactor.name, state: 'high' }
            ],
            implications: '全ての視点で高い成長が見込まれるため、積極的な投資と拡大戦略が有効',
            probability: 0.1
          });
          
          // Scenario 2: Tech high, Market high, Business low
          scenarios.push({
            id: 'scenario_2',
            name: 'テクノロジー主導シナリオ',
            description: 'テクノロジーとマーケットは高い成長を示すが、ビジネス要素が低いシナリオ',
            factors: [
              { perspective: 'technology', factor: techFactor.name, state: 'high' },
              { perspective: 'market', factor: marketFactor.name, state: 'high' },
              { perspective: 'business', factor: businessFactor.name, state: 'low' }
            ],
            implications: 'テクノロジーとマーケットの成長を活かしつつ、ビジネスモデルの見直しが必要',
            probability: 0.15
          });
          
          // Scenario 3: Tech low, Market high, Business high
          scenarios.push({
            id: 'scenario_3',
            name: 'マーケット・ビジネス主導シナリオ',
            description: 'マーケットとビジネス要素は高いが、テクノロジー要素が低いシナリオ',
            factors: [
              { perspective: 'technology', factor: techFactor.name, state: 'low' },
              { perspective: 'market', factor: marketFactor.name, state: 'high' },
              { perspective: 'business', factor: businessFactor.name, state: 'high' }
            ],
            implications: 'テクノロジー投資を強化しつつ、現在のマーケットとビジネス優位性を活用',
            probability: 0.2
          });
          
          // Scenario 4: Tech high, Market low, Business low
          scenarios.push({
            id: 'scenario_4',
            name: 'テクノロジー過剰シナリオ',
            description: 'テクノロジーは高いが、マーケットとビジネス要素が低いシナリオ',
            factors: [
              { perspective: 'technology', factor: techFactor.name, state: 'high' },
              { perspective: 'market', factor: marketFactor.name, state: 'low' },
              { perspective: 'business', factor: businessFactor.name, state: 'low' }
            ],
            implications: 'テクノロジーの市場適合性を再検討し、ビジネスモデルの抜本的見直しが必要',
            probability: 0.15
          });
          
          // Scenario 5: All factors medium
          scenarios.push({
            id: 'scenario_5',
            name: '現状維持シナリオ',
            description: '全ての要素が中程度の成長を維持するシナリオ',
            factors: [
              { perspective: 'technology', factor: techFactor.name, state: 'medium' },
              { perspective: 'market', factor: marketFactor.name, state: 'medium' },
              { perspective: 'business', factor: businessFactor.name, state: 'medium' }
            ],
            implications: '現在の戦略を継続しつつ、徐々に各要素の強化を図る',
            probability: 0.3
          });
          
          // Scenario 6: All factors low
          scenarios.push({
            id: 'scenario_6',
            name: '全要素低迷シナリオ',
            description: 'テクノロジー、マーケット、ビジネスの全ての要素が低迷するシナリオ',
            factors: [
              { perspective: 'technology', factor: techFactor.name, state: 'low' },
              { perspective: 'market', factor: marketFactor.name, state: 'low' },
              { perspective: 'business', factor: businessFactor.name, state: 'low' }
            ],
            implications: '防御的戦略への転換と、コスト削減、リスク管理の強化が必要',
            probability: 0.1
          });
          
          return scenarios;
        };
        
        const scenarios = generateScenarios();
        
        return {
          json: {
            execution_id: executionId,
            scenario_type: 'structural',
            scenarios: scenarios,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveStructuralScenarios",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "scenarios",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## ナラティブシナリオ生成の実装

ナラティブシナリオ生成は、ストーリーテリングの手法を用いて、論理的に一貫したシナリオを構築する手法です。トリプルパースペクティブ型戦略AIレーダーでは、テクノロジー、マーケット、ビジネスの3つの視点から一貫したストーリーを構築し、より具体的で実用的なシナリオを生成します。n8nを使用したナラティブシナリオ生成の実装例を示します。

```javascript
// n8n workflow: Narrative Scenario Generation
// Function node for generating narrative scenarios
[
  {
    "id": "loadStructuralScenarios",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "scenarios",
      "filter": {
        "execution_id": "={{ $node[\"loadExecutionId\"].json.execution_id }}",
        "scenario_type": "structural"
      },
      "options": {
        "sort": {
          "timestamp": -1
        }
      }
    }
  },
  {
    "id": "generateNarrativeScenarios",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get structural scenarios
        const structuralScenarios = $input.item.json;
        const scenarios = structuralScenarios.scenarios;
        const executionId = structuralScenarios.execution_id;
        
        // Generate narrative scenarios
        const generateNarratives = () => {
          const narratives = [];
          
          scenarios.forEach(scenario => {
            // Extract factor states
            const techState = scenario.factors.find(f => f.perspective === 'technology').state;
            const marketState = scenario.factors.find(f => f.perspective === 'market').state;
            const businessState = scenario.factors.find(f => f.perspective === 'business').state;
            
            // Generate timeline events
            const generateTimelineEvents = () => {
              const events = [];
              const currentYear = new Date().getFullYear();
              
              // Short-term events (1 year)
              if (techState === 'high') {
                events.push({
                  time: \`\${currentYear + 1}年第2四半期\`,
                  event: '技術革新が加速し、新たな製品プロトタイプが完成',
                  impact: 'テクノロジー視点での競争優位性が向上'
                });
              } else if (techState === 'low') {
                events.push({
                  time: \`\${currentYear + 1}年第2四半期\`,
                  event: '技術開発の遅延により、製品ロードマップの見直しが必要に',
                  impact: 'テクノロジー視点での競争力低下のリスク'
                });
              }
              
              if (marketState === 'high') {
                events.push({
                  time: \`\${currentYear + 1}年第3四半期\`,
                  event: '市場需要が予想を上回り、新規顧客セグメントが出現',
                  impact: 'マーケット視点での成長機会の拡大'
                });
              } else if (marketState === 'low') {
                events.push({
                  time: \`\${currentYear + 1}年第3四半期\`,
                  event: '市場成長の鈍化により、顧客獲得コストが上昇',
                  impact: 'マーケット視点での戦略見直しの必要性'
                });
              }
              
              // Mid-term events (2 years)
              if (techState === 'high' && marketState === 'high') {
                events.push({
                  time: \`\${currentYear + 2}年第1四半期\`,
                  event: '技術革新と市場需要の相乗効果により、新製品カテゴリーが確立',
                  impact: 'テクノロジーとマーケット視点での優位性強化'
                });
              }
              
              if (businessState === 'high') {
                events.push({
                  time: \`\${currentYear + 2}年第2四半期\`,
                  event: 'ビジネスモデルの最適化により、収益性が大幅に向上',
                  impact: 'ビジネス視点での持続可能な成長基盤の確立'
                });
              } else if (businessState === 'low') {
                events.push({
                  time: \`\${currentYear + 2}年第2四半期\`,
                  event: 'ビジネスモデルの課題が顕在化し、収益性が低下',
                  impact: 'ビジネス視点での構造改革の必要性'
                });
              }
              
              // Long-term events (3 years)
              const overallState = [techState, marketState, businessState].filter(s => s === 'high').length;
              
              if (overallState >= 2) {
                events.push({
                  time: \`\${currentYear + 3}年第1四半期\`,
                  event: '持続的な成長により、業界内でのポジションが強化',
                  impact: '全視点での競争優位性の確立'
                });
              } else if (overallState <= 1) {
                events.push({
                  time: \`\${currentYear + 3}年第1四半期\`,
                  event: '複数の課題が重なり、業界内でのポジションが弱体化',
                  impact: '全視点での抜本的な戦略見直しの必要性'
                });
              }
              
              return events;
            };
            
            // Generate key indicators
            const generateKeyIndicators = () => {
              const indicators = [];
              
              // Technology indicators
              if (techState === 'high') {
                indicators.push({
                  category: 'technology',
                  name: '技術革新速度',
                  trend: '上昇',
                  impact: '製品開発サイクルの短縮'
                });
                indicators.push({
                  category: 'technology',
                  name: '特許取得数',
                  trend: '大幅増加',
                  impact: '知的財産ポートフォリオの強化'
                });
              } else if (techState === 'medium') {
                indicators.push({
                  category: 'technology',
                  name: '技術革新速度',
                  trend: '安定',
                  impact: '現行製品の段階的改良'
                });
                indicators.push({
                  category: 'technology',
                  name: '特許取得数',
                  trend: '緩やかな増加',
                  impact: '知的財産の維持'
                });
              } else {
                indicators.push({
                  category: 'technology',
                  name: '技術革新速度',
                  trend: '低下',
                  impact: '製品競争力の低下'
                });
                indicators.push({
                  category: 'technology',
                  name: '特許取得数',
                  trend: '減少',
                  impact: '知的財産ポジションの弱体化'
                });
              }
              
              // Market indicators
              if (marketState === 'high') {
                indicators.push({
                  category: 'market',
                  name: '市場成長率',
                  trend: '急成長',
                  impact: '売上機会の大幅拡大'
                });
                indicators.push({
                  category: 'market',
                  name: '顧客獲得コスト',
                  trend: '低下',
                  impact: 'マーケティング効率の向上'
                });
              } else if (marketState === 'medium') {
                indicators.push({
                  category: 'market',
                  name: '市場成長率',
                  trend: '安定成長',
                  impact: '予測可能な売上拡大'
                });
                indicators.push({
                  category: 'market',
                  name: '顧客獲得コスト',
                  trend: '安定',
                  impact: 'マーケティング効率の維持'
                });
              } else {
                indicators.push({
                  category: 'market',
                  name: '市場成長率',
                  trend: '鈍化',
                  impact: '売上成長の制約'
                });
                indicators.push({
                  category: 'market',
                  name: '顧客獲得コスト',
                  trend: '上昇',
                  impact: 'マーケティング効率の低下'
                });
              }
              
              // Business indicators
              if (businessState === 'high') {
                indicators.push({
                  category: 'business',
                  name: '利益率',
                  trend: '上昇',
                  impact: '財務体質の強化'
                });
                indicators.push({
                  category: 'business',
                  name: '運用効率',
                  trend: '向上',
                  impact: 'コスト構造の最適化'
                });
              } else if (businessState === 'medium') {
                indicators.push({
                  category: 'business',
                  name: '利益率',
                  trend: '安定',
                  impact: '財務状況の維持'
                });
                indicators.push({
                  category: 'business',
                  name: '運用効率',
                  trend: '横ばい',
                  impact: '現行コスト構造の継続'
                });
              } else {
                indicators.push({
                  category: 'business',
                  name: '利益率',
                  trend: '低下',
                  impact: '財務圧力の増大'
                });
                indicators.push({
                  category: 'business',
                  name: '運用効率',
                  trend: '悪化',
                  impact: 'コスト増加の圧力'
                });
              }
              
              return indicators;
            };
            
            // Generate strategic options
            const generateStrategicOptions = () => {
              const options = [];
              
              // Technology strategies
              if (techState === 'high') {
                options.push({
                  category: 'technology',
                  name: '技術投資の加速',
                  description: '競争優位性をさらに強化するため、R&D投資を増加',
                  impact: '長期的な技術リーダーシップの確立'
                });
              } else if (techState === 'low') {
                options.push({
                  category: 'technology',
                  name: '技術提携の強化',
                  description: '外部パートナーとの協業により技術ギャップを埋める',
                  impact: '短期間での技術力向上'
                });
              }
              
              // Market strategies
              if (marketState === 'high') {
                options.push({
                  category: 'market',
                  name: '市場拡大戦略',
                  description: '新規市場セグメントへの積極展開',
                  impact: '成長機会の最大化'
                });
              } else if (marketState === 'low') {
                options.push({
                  category: 'market',
                  name: 'ニッチ特化戦略',
                  description: '特定の高収益セグメントへのリソース集中',
                  impact: '限られた市場での競争力強化'
                });
              }
              
              // Business strategies
              if (businessState === 'high') {
                options.push({
                  category: 'business',
                  name: 'スケール拡大戦略',
                  description: '現行ビジネスモデルの拡大と最適化',
                  impact: '収益性と市場シェアの同時拡大'
                });
              } else if (businessState === 'low') {
                options.push({
                  category: 'business',
                  name: 'ビジネスモデル再構築',
                  description: '収益構造の抜本的見直しと再構築',
                  impact: '持続可能な収益基盤の確立'
                });
              }
              
              // Combined strategies
              if (techState === 'high' && marketState === 'high') {
                options.push({
                  category: 'combined',
                  name: 'イノベーション主導型成長戦略',
                  description: '技術革新と市場拡大の相乗効果を最大化',
                  impact: '業界変革者としてのポジション確立'
                });
              }
              
              if (marketState === 'high' && businessState === 'high') {
                options.push({
                  category: 'combined',
                  name: '収益性重視の拡大戦略',
                  description: '市場機会の活用と収益構造の最適化を同時推進',
                  impact: '持続的な高収益成長'
                });
              }
              
              if (techState === 'low' && marketState === 'low' && businessState === 'low') {
                options.push({
                  category: 'combined',
                  name: '防御的再構築戦略',
                  description: '全面的な事業再構築と選択と集中の徹底',
                  impact: '生存基盤の確保と将来の成長に向けた再出発'
                });
              }
              
              return options;
            };
            
            // Create narrative scenario
            const timelineEvents = generateTimelineEvents();
            const keyIndicators = generateKeyIndicators();
            const strategicOptions = generateStrategicOptions();
            
            narratives.push({
              id: scenario.id + '_narrative',
              base_scenario: scenario.id,
              name: scenario.name,
              description: scenario.description,
              narrative_summary: `このシナリオでは、${scenario.description}。主要な不確実性要因の状態として、${scenario.factors.map(f => `${f.perspective}視点の${f.factor}が${f.state === 'high' ? '高い' : f.state === 'medium' ? '中程度' : '低い'}`).join('、')}という状況を想定しています。このような状況下では、${scenario.implications}`,
              timeline_events: timelineEvents,
              key_indicators: keyIndicators,
              strategic_options: strategicOptions,
              probability: scenario.probability
            });
          });
          
          return narratives;
        };
        
        const narrativeScenarios = generateNarratives();
        
        return {
          json: {
            execution_id: executionId,
            scenario_type: 'narrative',
            scenarios: narrativeScenarios,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveNarrativeScenarios",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "scenarios",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## シナリオ統合と優先順位付け

複数のアプローチで生成されたシナリオを統合し、優先順位付けを行うことで、より包括的で実用的なシナリオセットを提供します。n8nを使用したシナリオ統合と優先順位付けの実装例を示します。

```javascript
// n8n workflow: Scenario Integration and Prioritization
// Function node for integrating and prioritizing scenarios
[
  {
    "id": "loadAllScenarios",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "find",
      "collection": "scenarios",
      "filter": {
        "execution_id": "={{ $node[\"loadExecutionId\"].json.execution_id }}"
      }
    }
  },
  {
    "id": "integrateAndPrioritizeScenarios",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get all scenarios
        const allScenarios = $input.items.map(item => item.json);
        const executionId = allScenarios[0].execution_id;
        
        // Extract scenarios by type
        const probabilisticScenarios = allScenarios.find(s => s.scenario_type === 'probabilistic')?.scenarios || [];
        const structuralScenarios = allScenarios.find(s => s.scenario_type === 'structural')?.scenarios || [];
        const narrativeScenarios = allScenarios.find(s => s.scenario_type === 'narrative')?.scenarios || [];
        
        // Integrate scenarios
        const integrateScenarios = () => {
          const integratedScenarios = [];
          
          // Start with narrative scenarios as they are most comprehensive
          narrativeScenarios.forEach(narrative => {
            // Find corresponding structural scenario
            const structural = structuralScenarios.find(s => s.id === narrative.base_scenario);
            
            // Find corresponding probabilistic scenario based on type
            let probabilistic;
            if (narrative.name.includes('高成長')) {
              probabilistic = probabilisticScenarios.find(s => s.type === 'optimistic' || s.type === 'very_optimistic');
            } else if (narrative.name.includes('低迷')) {
              probabilistic = probabilisticScenarios.find(s => s.type === 'pessimistic' || s.type === 'very_pessimistic');
            } else {
              probabilistic = probabilisticScenarios.find(s => s.type === 'expected');
            }
            
            // Create integrated scenario
            integratedScenarios.push({
              id: narrative.id,
              name: narrative.name,
              description: narrative.description,
              narrative_summary: narrative.narrative_summary,
              timeline_events: narrative.timeline_events,
              key_indicators: narrative.key_indicators,
              strategic_options: narrative.strategic_options,
              factors: structural ? structural.factors : [],
              quantitative_prediction: probabilistic ? probabilistic.value : null,
              probability: narrative.probability,
              confidence: probabilistic ? probabilistic.probability : narrative.probability
            });
          });
          
          return integratedScenarios;
        };
        
        // Prioritize scenarios
        const prioritizeScenarios = (scenarios) => {
          // Calculate impact score
          scenarios.forEach(scenario => {
            // Impact is based on deviation from expected scenario
            const expectedScenario = scenarios.find(s => s.name.includes('現状維持'));
            const expectedValue = expectedScenario ? expectedScenario.quantitative_prediction : 0;
            
            const deviation = scenario.quantitative_prediction ? 
              Math.abs(scenario.quantitative_prediction - expectedValue) : 0;
            
            // Normalize deviation to 0-1 scale
            const maxDeviation = expectedValue * 0.5; // Assume max deviation is 50% of expected value
            const normalizedDeviation = Math.min(deviation / maxDeviation, 1);
            
            // Impact score combines deviation and probability
            scenario.impact_score = normalizedDeviation * 0.7 + scenario.probability * 0.3;
            
            // Priority is based on impact score and probability
            scenario.priority_score = scenario.impact_score * 0.6 + scenario.probability * 0.4;
            
            // Assign priority level
            if (scenario.priority_score >= 0.8) {
              scenario.priority_level = 'very_high';
              scenario.priority_label = '最優先';
            } else if (scenario.priority_score >= 0.6) {
              scenario.priority_level = 'high';
              scenario.priority_label = '高';
            } else if (scenario.priority_score >= 0.4) {
              scenario.priority_level = 'medium';
              scenario.priority_label = '中';
            } else if (scenario.priority_score >= 0.2) {
              scenario.priority_level = 'low';
              scenario.priority_label = '低';
            } else {
              scenario.priority_level = 'very_low';
              scenario.priority_label = '最低';
            }
          });
          
          // Sort by priority score (descending)
          return scenarios.sort((a, b) => b.priority_score - a.priority_score);
        };
        
        const integratedScenarios = integrateScenarios();
        const prioritizedScenarios = prioritizeScenarios(integratedScenarios);
        
        return {
          json: {
            execution_id: executionId,
            scenario_type: 'integrated',
            scenarios: prioritizedScenarios,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveIntegratedScenarios",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "scenarios",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## シナリオ生成のマスターワークフロー

最後に、上記のすべてのシナリオ生成ワークフローを統合するマスターワークフローを示します。このワークフローは、予測結果からシナリオ生成、統合、優先順位付けまでのエンドツーエンドのプロセスを自動化します。

```javascript
// n8n workflow: Scenario Generation Master Workflow
// Webhook node to trigger the workflow
[
  {
    "id": "webhookTrigger",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "scenario-generation",
      "responseMode": "lastNode",
      "options": {}
    }
  },
  {
    "id": "extractExecutionId",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Extract execution ID from webhook payload
        const payload = $input.item.json;
        const executionId = payload.execution_id;
        
        if (!executionId) {
          throw new Error('Execution ID is required');
        }
        
        return {
          json: {
            execution_id: executionId,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "generateProbabilisticScenarios",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/probabilistic-scenarios",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "generateStructuralScenarios",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/structural-scenarios",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "generateNarrativeScenarios",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/narrative-scenarios",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "integrateAndPrioritizeScenarios",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/integrate-scenarios",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "generateScenarioReport",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get execution ID
        const executionId = $input.item.json.execution_id;
        
        // Generate report URL
        const reportUrl = \`http://localhost:3000/scenarios/\${executionId}\`;
        
        return {
          json: {
            execution_id: executionId,
            message: 'Scenario generation completed successfully',
            report_url: reportUrl,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  }
]
```

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおけるシナリオ生成メカニズムの実装について詳細に解説しました。確率論的シナリオ生成、構造的シナリオ生成、ナラティブシナリオ生成の3つのアプローチを組み合わせることで、より包括的で実用的なシナリオを生成する方法を示しました。また、シナリオの統合と優先順位付けを行うことで、意思決定者にとって有用なシナリオセットを提供する方法も解説しました。

これらのシナリオ生成メカニズムを活用することで、トリプルパースペクティブ型戦略AIレーダーは単なる予測ツールを超え、戦略的意思決定を支援する強力なツールとなります。次のセクションでは、これらのシナリオを活用した意思決定支援の方法について解説します。
