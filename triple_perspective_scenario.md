# インタラクティブダッシュボードの設計：代替シナリオの可視化

## 代替シナリオ可視化の重要性

トリプルパースペクティブ型戦略AIレーダーにおいて、代替シナリオの可視化は意思決定の柔軟性と堅牢性を高める重要な要素です。特に情報不均衡や不確実性が高い状況では、単一の「最適解」だけでなく、複数の代替シナリオを提示し、それらを比較検討できるようにすることが重要です。

本セクションでは、代替シナリオの可視化に焦点を当て、インタラクティブダッシュボードにおける実装方法を詳細に解説します。

### 代替シナリオ可視化の目的

代替シナリオの可視化には、以下の目的があります：

1. **多角的な視点の提供**
   - 単一の「正解」に固執せず、複数の可能性を提示
   - 異なる前提条件や制約に基づく代替解の探索

2. **不確実性への対応**
   - 情報不足や不確実性が高い状況での意思決定支援
   - 「何が分からないか」を明示的に示す

3. **リスク管理の強化**
   - 最悪のシナリオや極端なケースの検討
   - 意思決定の堅牢性評価

4. **創造的思考の促進**
   - 既存の枠組みを超えた思考の促進
   - 新たな可能性の発見

## 代替シナリオの生成と構造化

代替シナリオを効果的に可視化するためには、まず適切なシナリオを生成し、構造化する必要があります。以下に、n8nを活用した代替シナリオの生成と構造化の方法を示します。

### 代替シナリオの生成

```javascript
// n8n workflow: Alternative Scenario Generation
// Function node for generating alternative scenarios
[
  {
    "id": "generateAlternativeScenarios",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Equilibrium detection results and perspective evaluations
        const equilibriumData = $input.item.json.equilibrium_data || {
          topic_id: 'topic-001',
          topic_name: 'AI自動運転技術',
          is_equilibrium: false,
          adjusted_score: 0.65,
          contributing_factors: {
            perspectives: {
              technology: { score: 0.8, weight: 0.3 },
              market: { score: 0.6, weight: 0.4 },
              business: { score: 0.5, weight: 0.3 }
            }
          }
        };
        
        const perspectiveEvaluations = $input.item.json.perspective_evaluations || [
          {
            perspective_id: 'technology',
            importance: { score: 0.8, level: 'high' },
            confidence: { score: 0.7, level: 'medium' },
            overall_score: 0.75
          },
          {
            perspective_id: 'market',
            importance: { score: 0.7, level: 'high' },
            confidence: { score: 0.6, level: 'medium' },
            overall_score: 0.65
          },
          {
            perspective_id: 'business',
            importance: { score: 0.6, level: 'medium' },
            confidence: { score: 0.5, level: 'medium' },
            overall_score: 0.55
          }
        ];
        
        // Generate alternative scenarios
        const alternativeScenarios = [];
        
        // Add baseline scenario
        alternativeScenarios.push({
          scenario_id: 'baseline',
          name: 'ベースラインシナリオ',
          description: '現在の情報に基づく最も可能性の高いシナリオ',
          probability: 0.6,
          adjusted_score: equilibriumData.adjusted_score,
          is_equilibrium: equilibriumData.is_equilibrium,
          perspective_scores: {
            technology: perspectiveEvaluations.find(p => p.perspective_id === 'technology').overall_score,
            market: perspectiveEvaluations.find(p => p.perspective_id === 'market').overall_score,
            business: perspectiveEvaluations.find(p => p.perspective_id === 'business').overall_score
          },
          key_assumptions: [
            '現在の技術トレンドが継続する',
            '市場の成長率は現在の予測通りに推移する',
            'ビジネスモデルに大きな変化はない'
          ],
          is_current: true
        });
        
        // Generate optimistic scenario
        const optimisticScenario = generateOptimisticScenario(
          equilibriumData,
          perspectiveEvaluations
        );
        alternativeScenarios.push(optimisticScenario);
        
        // Generate pessimistic scenario
        const pessimisticScenario = generatePessimisticScenario(
          equilibriumData,
          perspectiveEvaluations
        );
        alternativeScenarios.push(pessimisticScenario);
        
        // Generate technology-driven scenario
        const technologyDrivenScenario = generatePerspectiveDrivenScenario(
          equilibriumData,
          perspectiveEvaluations,
          'technology',
          '技術主導シナリオ',
          '技術的ブレークスルーが市場とビジネスをリードする状況'
        );
        alternativeScenarios.push(technologyDrivenScenario);
        
        // Generate market-driven scenario
        const marketDrivenScenario = generatePerspectiveDrivenScenario(
          equilibriumData,
          perspectiveEvaluations,
          'market',
          '市場主導シナリオ',
          '市場需要が技術開発とビジネスモデルを牽引する状況'
        );
        alternativeScenarios.push(marketDrivenScenario);
        
        // Generate business-driven scenario
        const businessDrivenScenario = generatePerspectiveDrivenScenario(
          equilibriumData,
          perspectiveEvaluations,
          'business',
          'ビジネス主導シナリオ',
          '新たなビジネスモデルが技術と市場を変革する状況'
        );
        alternativeScenarios.push(businessDrivenScenario);
        
        // Generate disruptive scenario
        const disruptiveScenario = generateDisruptiveScenario(
          equilibriumData,
          perspectiveEvaluations
        );
        alternativeScenarios.push(disruptiveScenario);
        
        return {
          json: {
            topic_id: equilibriumData.topic_id,
            topic_name: equilibriumData.topic_name,
            baseline_scenario: alternativeScenarios[0],
            alternative_scenarios: alternativeScenarios.slice(1),
            all_scenarios: alternativeScenarios
          }
        };
        
        // Helper function: Generate optimistic scenario
        function generateOptimisticScenario(equilibriumData, perspectiveEvaluations) {
          // Extract perspective scores
          const perspectiveScores = {};
          for (const eval of perspectiveEvaluations) {
            perspectiveScores[eval.perspective_id] = eval.overall_score;
          }
          
          // Enhance scores for optimistic scenario
          const enhancedScores = {};
          for (const perspectiveId in perspectiveScores) {
            enhancedScores[perspectiveId] = Math.min(1.0, perspectiveScores[perspectiveId] * 1.2);
          }
          
          // Calculate new adjusted score
          const weights = {
            technology: 0.3,
            market: 0.4,
            business: 0.3
          };
          
          const newAdjustedScore = Object.keys(weights).reduce((sum, perspectiveId) => {
            return sum + enhancedScores[perspectiveId] * weights[perspectiveId];
          }, 0);
          
          // Determine if this would be an equilibrium
          const isEquilibrium = newAdjustedScore > 0.75;
          
          return {
            scenario_id: 'optimistic',
            name: '楽観的シナリオ',
            description: '好条件が重なり、相乗効果が生まれる状況',
            probability: 0.2,
            adjusted_score: newAdjustedScore,
            is_equilibrium: isEquilibrium,
            perspective_scores: enhancedScores,
            key_assumptions: [
              '技術開発が予想以上に進展する',
              '市場の受容性が高まる',
              'ビジネスモデルの収益性が向上する'
            ],
            is_current: false
          };
        }
        
        // Helper function: Generate pessimistic scenario
        function generatePessimisticScenario(equilibriumData, perspectiveEvaluations) {
          // Extract perspective scores
          const perspectiveScores = {};
          for (const eval of perspectiveEvaluations) {
            perspectiveScores[eval.perspective_id] = eval.overall_score;
          }
          
          // Reduce scores for pessimistic scenario
          const reducedScores = {};
          for (const perspectiveId in perspectiveScores) {
            reducedScores[perspectiveId] = Math.max(0.0, perspectiveScores[perspectiveId] * 0.8);
          }
          
          // Calculate new adjusted score
          const weights = {
            technology: 0.3,
            market: 0.4,
            business: 0.3
          };
          
          const newAdjustedScore = Object.keys(weights).reduce((sum, perspectiveId) => {
            return sum + reducedScores[perspectiveId] * weights[perspectiveId];
          }, 0);
          
          // This would not be an equilibrium
          const isEquilibrium = false;
          
          return {
            scenario_id: 'pessimistic',
            name: '悲観的シナリオ',
            description: '障壁や制約が予想以上に大きい状況',
            probability: 0.2,
            adjusted_score: newAdjustedScore,
            is_equilibrium: isEquilibrium,
            perspective_scores: reducedScores,
            key_assumptions: [
              '技術的な課題が予想以上に難しい',
              '市場の成長が鈍化する',
              'ビジネスモデルの収益性が低下する'
            ],
            is_current: false
          };
        }
        
        // Helper function: Generate perspective-driven scenario
        function generatePerspectiveDrivenScenario(
          equilibriumData,
          perspectiveEvaluations,
          drivingPerspective,
          name,
          description
        ) {
          // Extract perspective scores
          const perspectiveScores = {};
          for (const eval of perspectiveEvaluations) {
            perspectiveScores[eval.perspective_id] = eval.overall_score;
          }
          
          // Modify scores based on driving perspective
          const modifiedScores = {};
          for (const perspectiveId in perspectiveScores) {
            if (perspectiveId === drivingPerspective) {
              // Enhance driving perspective
              modifiedScores[perspectiveId] = Math.min(1.0, perspectiveScores[perspectiveId] * 1.3);
            } else {
              // Slightly reduce other perspectives
              modifiedScores[perspectiveId] = Math.max(0.0, perspectiveScores[perspectiveId] * 0.9);
            }
          }
          
          // Calculate new adjusted score
          const weights = {
            technology: 0.3,
            market: 0.4,
            business: 0.3
          };
          
          // Adjust weights to emphasize driving perspective
          const modifiedWeights = { ...weights };
          for (const perspectiveId in modifiedWeights) {
            if (perspectiveId === drivingPerspective) {
              modifiedWeights[perspectiveId] *= 1.5;
            } else {
              modifiedWeights[perspectiveId] *= 0.75;
            }
          }
          
          // Normalize weights
          const weightSum = Object.values(modifiedWeights).reduce((sum, weight) => sum + weight, 0);
          for (const perspectiveId in modifiedWeights) {
            modifiedWeights[perspectiveId] /= weightSum;
          }
          
          const newAdjustedScore = Object.keys(modifiedWeights).reduce((sum, perspectiveId) => {
            return sum + modifiedScores[perspectiveId] * modifiedWeights[perspectiveId];
          }, 0);
          
          // Determine if this would be an equilibrium
          const isEquilibrium = newAdjustedScore > 0.75;
          
          // Generate key assumptions
          const keyAssumptions = [];
          
          if (drivingPerspective === 'technology') {
            keyAssumptions.push(
              '技術革新が加速する',
              '技術的ブレークスルーが発生する',
              '技術的障壁が低減する'
            );
          } else if (drivingPerspective === 'market') {
            keyAssumptions.push(
              '市場需要が急増する',
              '顧客の受容性が高まる',
              '市場の成熟度が向上する'
            );
          } else if (drivingPerspective === 'business') {
            keyAssumptions.push(
              '新たなビジネスモデルが登場する',
              '収益構造が改善される',
              '戦略的提携が進展する'
            );
          }
          
          return {
            scenario_id: \`\${drivingPerspective}_driven\`,
            name,
            description,
            probability: 0.1,
            adjusted_score: newAdjustedScore,
            is_equilibrium: isEquilibrium,
            perspective_scores: modifiedScores,
            perspective_weights: modifiedWeights,
            key_assumptions: keyAssumptions,
            is_current: false,
            driving_perspective: drivingPerspective
          };
        }
        
        // Helper function: Generate disruptive scenario
        function generateDisruptiveScenario(equilibriumData, perspectiveEvaluations) {
          // Extract perspective scores
          const perspectiveScores = {};
          for (const eval of perspectiveEvaluations) {
            perspectiveScores[eval.perspective_id] = eval.overall_score;
          }
          
          // Create highly varied scores for disruptive scenario
          const disruptiveScores = {
            technology: Math.min(1.0, perspectiveScores.technology * 1.5), // Technology leaps forward
            market: Math.max(0.2, perspectiveScores.market * 0.7),         // Market is disrupted
            business: Math.min(1.0, perspectiveScores.business * 1.2)      // Business models adapt
          };
          
          // Calculate new adjusted score
          const weights = {
            technology: 0.5,  // Technology becomes more important
            market: 0.2,      // Market becomes less important
            business: 0.3     // Business importance stays the same
          };
          
          const newAdjustedScore = Object.keys(weights).reduce((sum, perspectiveId) => {
            return sum + disruptiveScores[perspectiveId] * weights[perspectiveId];
          }, 0);
          
          // This could be an equilibrium if score is high enough
          const isEquilibrium = newAdjustedScore > 0.75;
          
          return {
            scenario_id: 'disruptive',
            name: '破壊的シナリオ',
            description: '既存の枠組みが根本から変わる状況',
            probability: 0.05,
            adjusted_score: newAdjustedScore,
            is_equilibrium: isEquilibrium,
            perspective_scores: disruptiveScores,
            perspective_weights: weights,
            key_assumptions: [
              '破壊的技術革新が発生する',
              '市場構造が根本的に変化する',
              '既存のビジネスモデルが陳腐化する'
            ],
            is_current: false
          };
        }
      `
    }
  }
]
```

### 代替シナリオの構造化

```javascript
// n8n workflow: Alternative Scenario Structuring
// Function node for structuring alternative scenarios
[
  {
    "id": "structureAlternativeScenarios",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Generated alternative scenarios
        const scenarioData = $input.item.json;
        
        // Structure scenarios for visualization
        const structuredScenarios = {
          topic_id: scenarioData.topic_id,
          topic_name: scenarioData.topic_name,
          
          // Group scenarios by type
          scenario_groups: [
            {
              group_id: 'baseline',
              name: 'ベースライン',
              description: '現在の情報に基づく最も可能性の高いシナリオ',
              scenarios: [scenarioData.baseline_scenario]
            },
            {
              group_id: 'probability_based',
              name: '確率ベース',
              description: '発生確率に基づく楽観的・悲観的シナリオ',
              scenarios: scenarioData.all_scenarios.filter(s => 
                s.scenario_id === 'optimistic' || s.scenario_id === 'pessimistic'
              )
            },
            {
              group_id: 'perspective_driven',
              name: '視点主導',
              description: '特定の視点が主導するシナリオ',
              scenarios: scenarioData.all_scenarios.filter(s => 
                s.scenario_id === 'technology_driven' || 
                s.scenario_id === 'market_driven' || 
                s.scenario_id === 'business_driven'
              )
            },
            {
              group_id: 'disruptive',
              name: '破壊的',
              description: '既存の枠組みを根本から変えるシナリオ',
              scenarios: scenarioData.all_scenarios.filter(s => 
                s.scenario_id === 'disruptive'
              )
            }
          ],
          
          // Prepare comparison data
          comparison_metrics: [
            {
              metric_id: 'adjusted_score',
              name: '調整スコア',
              description: '総合的な評価スコア',
              format: 'percentage'
            },
            {
              metric_id: 'probability',
              name: '発生確率',
              description: 'シナリオの発生確率',
              format: 'percentage'
            },
            {
              metric_id: 'is_equilibrium',
              name: '静止点',
              description: '静止点として検出されるか',
              format: 'boolean'
            }
          ],
          
          // Prepare perspective metrics
          perspective_metrics: [
            {
              perspective_id: 'technology',
              name: 'テクノロジー視点',
              description: '技術的実現可能性と革新性'
            },
            {
              perspective_id: 'market',
              name: 'マーケット視点',
              description: '市場需要と成長性'
            },
            {
              perspective_id: 'business',
              name: 'ビジネス視点',
              description: 'ビジネスモデルと収益性'
            }
          ],
          
          // Prepare scenario actions
          scenario_actions: scenarioData.all_scenarios.map(scenario => {
            // Generate actions based on scenario
            const actions = [];
            
            if (scenario.is_equilibrium) {
              actions.push({
                action_id: \`strategic_initiative_\${scenario.scenario_id}\`,
                name: '戦略的イニシアチブ',
                description: \`「\${scenario.name}」に向けた戦略的イニシアチブを開始する\`,
                priority: scenario.probability * 0.9 + 0.1
              });
            }
            
            if (scenario.scenario_id === 'baseline') {
              actions.push({
                action_id: 'continuous_monitoring',
                name: '継続的モニタリング',
                description: 'ベースラインシナリオの前提条件を継続的にモニタリングする',
                priority: 0.8
              });
            } else if (scenario.scenario_id === 'optimistic') {
              actions.push({
                action_id: 'opportunity_preparation',
                name: '機会準備',
                description: '楽観的シナリオの実現に向けた準備を行う',
                priority: scenario.probability * 0.8
              });
            } else if (scenario.scenario_id === 'pessimistic') {
              actions.push({
                action_id: 'risk_mitigation',
                name: 'リスク軽減',
                description: '悲観的シナリオに対するリスク軽減策を講じる',
                priority: scenario.probability * 0.7
              });
            } else if (scenario.scenario_id.includes('_driven')) {
              const perspective = scenario.driving_perspective;
              const perspectiveNames = {
                technology: 'テクノロジー',
                market: 'マーケット',
                business: 'ビジネス'
              };
              
              actions.push({
                action_id: \`\${perspective}_investment\`,
                name: \`\${perspectiveNames[perspective]}投資\`,
                description: \`\${perspectiveNames[perspective]}視点の強化に投資する\`,
                priority: scenario.probability * 0.6
              });
            } else if (scenario.scenario_id === 'disruptive') {
              actions.push({
                action_id: 'innovation_exploration',
                name: '革新探索',
                description: '破壊的イノベーションの可能性を探索する',
                priority: scenario.probability * 0.5
              });
            }
            
            return {
              scenario_id: scenario.scenario_id,
              actions: actions
            };
          })
        };
        
        return {
          json: structuredScenarios
        };
      `
    }
  }
]
```

## 代替シナリオの可視化手法

代替シナリオを効果的に可視化するための手法として、以下のアプローチを提案します。

### 1. シナリオ比較テーブル

シナリオ比較テーブルは、複数のシナリオを一覧で比較するための基本的な可視化手法です。

#### 実装方法

```javascript
// n8n workflow: Scenario Comparison Table
// Function node for generating comparison table data
[
  {
    "id": "generateComparisonTableData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Structured scenario data
        const structuredScenarios = $input.item.json;
        
        // Flatten scenarios for table view
        const tableData = {
          headers: [
            { id: 'name', label: 'シナリオ名', type: 'text' },
            { id: 'probability', label: '発生確率', type: 'percentage' },
            { id: 'adjusted_score', label: '調整スコア', type: 'percentage' },
            { id: 'is_equilibrium', label: '静止点', type: 'boolean' },
            { id: 'technology_score', label: 'テクノロジー', type: 'percentage' },
            { id: 'market_score', label: 'マーケット', type: 'percentage' },
            { id: 'business_score', label: 'ビジネス', type: 'percentage' }
          ],
          rows: []
        };
        
        // Add all scenarios to table
        structuredScenarios.scenario_groups.forEach(group => {
          group.scenarios.forEach(scenario => {
            tableData.rows.push({
              id: scenario.scenario_id,
              name: scenario.name,
              probability: scenario.probability,
              adjusted_score: scenario.adjusted_score,
              is_equilibrium: scenario.is_equilibrium,
              technology_score: scenario.perspective_scores.technology,
              market_score: scenario.perspective_scores.market,
              business_score: scenario.perspective_scores.business,
              is_current: scenario.is_current,
              group_id: group.group_id
            });
          });
        });
        
        // Sort rows by probability (descending)
        tableData.rows.sort((a, b) => b.probability - a.probability);
        
        return {
          json: {
            topic_id: structuredScenarios.topic_id,
            topic_name: structuredScenarios.topic_name,
            table_data: tableData
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（React）

```jsx
// React component for scenario comparison table
function ScenarioComparisonTable({ data }) {
  const { table_data } = data;
  
  // Define cell renderers
  const renderCell = (row, header) => {
    const value = row[header.id];
    
    switch (header.type) {
      case 'percentage':
        return `${Math.round(value * 100)}%`;
      
      case 'boolean':
        return value ? '✓' : '✗';
      
      default:
        return value;
    }
  };
  
  return (
    <div className="scenario-comparison-table">
      <h3>{data.topic_name}のシナリオ比較</h3>
      
      <table className="comparison-table">
        <thead>
          <tr>
            {table_data.headers.map(header => (
              <th key={header.id}>{header.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {table_data.rows.map(row => (
            <tr 
              key={row.id} 
              className={`
                scenario-row 
                ${row.is_current ? 'current-scenario' : ''}
                ${row.group_id}
              `}
            >
              {table_data.headers.map(header => (
                <td key={`${row.id}-${header.id}`}>
                  {renderCell(row, header)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      
      <div className="table-legend">
        <div className="legend-item current-scenario">
          <span className="legend-marker"></span>
          <span className="legend-label">現在のシナリオ</span>
        </div>
        {['baseline', 'probability_based', 'perspective_driven', 'disruptive'].map(groupId => (
          <div key={groupId} className={`legend-item ${groupId}`}>
            <span className="legend-marker"></span>
            <span className="legend-label">
              {groupId === 'baseline' ? 'ベースライン' : 
               groupId === 'probability_based' ? '確率ベース' : 
               groupId === 'perspective_driven' ? '視点主導' : '破壊的'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 2. レーダーチャート比較

レーダーチャート比較は、各シナリオの視点別スコアを視覚的に比較するための効果的な手法です。

#### 実装方法

```javascript
// n8n workflow: Scenario Radar Chart Comparison
// Function node for generating radar chart data
[
  {
    "id": "generateRadarChartData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Structured scenario data
        const structuredScenarios = $input.item.json;
        
        // Prepare radar chart data
        const radarData = {
          labels: ['テクノロジー', 'マーケット', 'ビジネス'],
          datasets: []
        };
        
        // Add baseline scenario
        const baselineScenario = structuredScenarios.scenario_groups
          .find(g => g.group_id === 'baseline')
          .scenarios[0];
        
        radarData.datasets.push({
          label: baselineScenario.name,
          data: [
            baselineScenario.perspective_scores.technology,
            baselineScenario.perspective_scores.market,
            baselineScenario.perspective_scores.business
          ],
          scenario_id: baselineScenario.scenario_id,
          is_current: true
        });
        
        // Add other scenarios (limit to 4 for readability)
        const otherScenarios = structuredScenarios.scenario_groups
          .filter(g => g.group_id !== 'baseline')
          .flatMap(g => g.scenarios)
          .sort((a, b) => b.probability - a.probability)
          .slice(0, 4);
        
        otherScenarios.forEach(scenario => {
          radarData.datasets.push({
            label: scenario.name,
            data: [
              scenario.perspective_scores.technology,
              scenario.perspective_scores.market,
              scenario.perspective_scores.business
            ],
            scenario_id: scenario.scenario_id,
            is_current: false
          });
        });
        
        return {
          json: {
            topic_id: structuredScenarios.topic_id,
            topic_name: structuredScenarios.topic_name,
            radar_data: radarData
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（Chart.js）

```javascript
// Chart.js implementation for radar chart comparison
function renderScenarioRadarChart(data, containerId) {
  // Create canvas element
  const canvas = document.createElement('canvas');
  document.getElementById(containerId).appendChild(canvas);
  
  // Define colors for different scenario types
  const colors = {
    baseline: {
      background: 'rgba(54, 162, 235, 0.2)',
      border: 'rgba(54, 162, 235, 1)'
    },
    optimistic: {
      background: 'rgba(75, 192, 192, 0.2)',
      border: 'rgba(75, 192, 192, 1)'
    },
    pessimistic: {
      background: 'rgba(255, 99, 132, 0.2)',
      border: 'rgba(255, 99, 132, 1)'
    },
    technology_driven: {
      background: 'rgba(153, 102, 255, 0.2)',
      border: 'rgba(153, 102, 255, 1)'
    },
    market_driven: {
      background: 'rgba(255, 159, 64, 0.2)',
      border: 'rgba(255, 159, 64, 1)'
    },
    business_driven: {
      background: 'rgba(255, 205, 86, 0.2)',
      border: 'rgba(255, 205, 86, 1)'
    },
    disruptive: {
      background: 'rgba(201, 203, 207, 0.2)',
      border: 'rgba(201, 203, 207, 1)'
    }
  };
  
  // Apply colors to datasets
  data.radar_data.datasets.forEach(dataset => {
    const scenarioType = dataset.scenario_id;
    const color = colors[scenarioType] || colors.baseline;
    
    dataset.backgroundColor = color.background;
    dataset.borderColor = color.border;
    dataset.pointBackgroundColor = color.border;
    dataset.pointBorderColor = '#fff';
    dataset.pointHoverBackgroundColor = '#fff';
    dataset.pointHoverBorderColor = color.border;
    
    // Make current scenario line thicker
    if (dataset.is_current) {
      dataset.borderWidth = 3;
    }
  });
  
  // Create chart
  new Chart(canvas, {
    type: 'radar',
    data: data.radar_data,
    options: {
      scales: {
        r: {
          angleLines: {
            display: true
          },
          suggestedMin: 0,
          suggestedMax: 1,
          ticks: {
            callback: function(value) {
              return value * 100 + '%';
            }
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `${data.topic_name}のシナリオ比較`
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.dataset.label || '';
              const value = context.raw;
              return `${label}: ${Math.round(value * 100)}%`;
            }
          }
        },
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}
```

### 3. パラレルコーディネートプロット

パラレルコーディネートプロットは、複数の次元にわたるシナリオの特性を視覚化するための効果的な手法です。

#### 実装方法

```javascript
// n8n workflow: Parallel Coordinates Plot
// Function node for generating parallel coordinates data
[
  {
    "id": "generateParallelCoordinatesData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Structured scenario data
        const structuredScenarios = $input.item.json;
        
        // Prepare parallel coordinates data
        const dimensions = [
          {
            id: 'probability',
            name: '発生確率',
            domain: [0, 1]
          },
          {
            id: 'technology',
            name: 'テクノロジー',
            domain: [0, 1]
          },
          {
            id: 'market',
            name: 'マーケット',
            domain: [0, 1]
          },
          {
            id: 'business',
            name: 'ビジネス',
            domain: [0, 1]
          },
          {
            id: 'adjusted_score',
            name: '調整スコア',
            domain: [0, 1]
          }
        ];
        
        // Extract data for each scenario
        const scenarios = structuredScenarios.scenario_groups
          .flatMap(g => g.scenarios)
          .map(scenario => ({
            id: scenario.scenario_id,
            name: scenario.name,
            group: scenario.scenario_id === 'baseline' ? 'baseline' :
                   scenario.scenario_id === 'optimistic' || scenario.scenario_id === 'pessimistic' ? 'probability_based' :
                   scenario.scenario_id === 'disruptive' ? 'disruptive' : 'perspective_driven',
            values: {
              probability: scenario.probability,
              technology: scenario.perspective_scores.technology,
              market: scenario.perspective_scores.market,
              business: scenario.perspective_scores.business,
              adjusted_score: scenario.adjusted_score
            },
            is_current: scenario.is_current,
            is_equilibrium: scenario.is_equilibrium
          }));
        
        return {
          json: {
            topic_id: structuredScenarios.topic_id,
            topic_name: structuredScenarios.topic_name,
            dimensions,
            scenarios
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（D3.js）

```javascript
// D3.js implementation for parallel coordinates plot
function renderParallelCoordinatesPlot(data, containerId) {
  // Clear previous content
  d3.select(`#${containerId}`).html("");
  
  // Set dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 50, right: 50, bottom: 30, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Create SVG
  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  
  // Create group for the visualization
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // Define colors for different scenario groups
  const colors = {
    baseline: '#36a2eb',
    probability_based: '#ff6384',
    perspective_driven: '#4bc0c0',
    disruptive: '#9966ff'
  };
  
  // Create scales for each dimension
  const dimensionScales = {};
  const dimensionPositions = {};
  
  data.dimensions.forEach((dimension, i) => {
    const position = innerWidth * i / (data.dimensions.length - 1);
    dimensionPositions[dimension.id] = position;
    
    dimensionScales[dimension.id] = d3.scaleLinear()
      .domain(dimension.domain)
      .range([innerHeight, 0]);
  });
  
  // Create axes
  data.dimensions.forEach(dimension => {
    const axis = d3.axisLeft(dimensionScales[dimension.id])
      .tickFormat(d => `${Math.round(d * 100)}%`);
    
    g.append("g")
      .attr("transform", `translate(${dimensionPositions[dimension.id]},0)`)
      .call(axis)
      .append("text")
      .attr("y", -10)
      .attr("text-anchor", "middle")
      .attr("fill", "black")
      .text(dimension.name);
  });
  
  // Create line generator
  const line = d3.line()
    .defined(d => d !== null)
    .x(d => d.position)
    .y(d => d.value);
  
  // Draw lines for each scenario
  data.scenarios.forEach(scenario => {
    const points = data.dimensions.map(dimension => {
      const value = scenario.values[dimension.id];
      return {
        position: dimensionPositions[dimension.id],
        value: dimensionScales[dimension.id](value)
      };
    });
    
    g.append("path")
      .datum(points)
      .attr("fill", "none")
      .attr("stroke", colors[scenario.group])
      .attr("stroke-width", scenario.is_current ? 3 : 1.5)
      .attr("stroke-opacity", 0.7)
      .attr("d", line);
    
    // Add circles at each point
    points.forEach((point, i) => {
      g.append("circle")
        .attr("cx", point.position)
        .attr("cy", point.value)
        .attr("r", 4)
        .attr("fill", colors[scenario.group])
        .attr("stroke", "white")
        .attr("stroke-width", 1)
        .append("title")
        .text(`${scenario.name}: ${Math.round(scenario.values[data.dimensions[i].id] * 100)}%`);
    });
  });
  
  // Add title
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", margin.top / 2)
    .attr("text-anchor", "middle")
    .attr("font-weight", "bold")
    .text(`${data.topic_name}のシナリオ比較`);
  
  // Add legend
  const legend = svg.append("g")
    .attr("transform", `translate(${width - margin.right - 150}, ${margin.top})`);
  
  Object.entries(colors).forEach(([group, color], i) => {
    const groupNames = {
      baseline: 'ベースライン',
      probability_based: '確率ベース',
      perspective_driven: '視点主導',
      disruptive: '破壊的'
    };
    
    legend.append("rect")
      .attr("x", 0)
      .attr("y", i * 20)
      .attr("width", 15)
      .attr("height", 15)
      .attr("fill", color);
    
    legend.append("text")
      .attr("x", 20)
      .attr("y", i * 20 + 12)
      .text(groupNames[group]);
  });
}
```

### 4. シナリオフローチャート

シナリオフローチャートは、シナリオ間の関係性や移行経路を視覚化するための効果的な手法です。

#### 実装方法

```javascript
// n8n workflow: Scenario Flow Chart
// Function node for generating flow chart data
[
  {
    "id": "generateFlowChartData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Structured scenario data
        const structuredScenarios = $input.item.json;
        
        // Prepare flow chart data
        const nodes = [];
        const links = [];
        
        // Add nodes for each scenario
        structuredScenarios.scenario_groups.forEach(group => {
          group.scenarios.forEach(scenario => {
            nodes.push({
              id: scenario.scenario_id,
              name: scenario.name,
              group: group.group_id,
              score: scenario.adjusted_score,
              probability: scenario.probability,
              is_current: scenario.is_current,
              is_equilibrium: scenario.is_equilibrium
            });
          });
        });
        
        // Find baseline scenario
        const baselineScenario = nodes.find(node => node.id === 'baseline');
        
        // Add links from baseline to other scenarios
        nodes.forEach(node => {
          if (node.id !== 'baseline') {
            links.push({
              source: 'baseline',
              target: node.id,
              value: node.probability,
              type: node.is_equilibrium ? 'positive' : 'neutral'
            });
          }
        });
        
        // Add additional links between related scenarios
        if (nodes.find(n => n.id === 'optimistic') && nodes.find(n => n.id === 'technology_driven')) {
          links.push({
            source: 'optimistic',
            target: 'technology_driven',
            value: 0.3,
            type: 'related'
          });
        }
        
        if (nodes.find(n => n.id === 'pessimistic') && nodes.find(n => n.id === 'market_driven')) {
          links.push({
            source: 'pessimistic',
            target: 'market_driven',
            value: 0.2,
            type: 'related'
          });
        }
        
        if (nodes.find(n => n.id === 'disruptive') && nodes.find(n => n.id === 'technology_driven')) {
          links.push({
            source: 'disruptive',
            target: 'technology_driven',
            value: 0.4,
            type: 'related'
          });
        }
        
        return {
          json: {
            topic_id: structuredScenarios.topic_id,
            topic_name: structuredScenarios.topic_name,
            nodes,
            links
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（D3.js）

```javascript
// D3.js implementation for scenario flow chart
function renderScenarioFlowChart(data, containerId) {
  // Clear previous content
  d3.select(`#${containerId}`).html("");
  
  // Set dimensions
  const width = 800;
  const height = 600;
  const margin = { top: 50, right: 50, bottom: 30, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Create SVG
  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  
  // Create group for the visualization
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // Define colors for different scenario groups
  const colors = {
    baseline: '#36a2eb',
    probability_based: '#ff6384',
    perspective_driven: '#4bc0c0',
    disruptive: '#9966ff'
  };
  
  // Define link types
  const linkTypes = {
    positive: {
      color: '#4caf50',
      dashArray: null
    },
    neutral: {
      color: '#9e9e9e',
      dashArray: null
    },
    negative: {
      color: '#f44336',
      dashArray: null
    },
    related: {
      color: '#9e9e9e',
      dashArray: '5,5'
    }
  };
  
  // Create force simulation
  const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(innerWidth / 2, innerHeight / 2))
    .force("x", d3.forceX(innerWidth / 2).strength(0.1))
    .force("y", d3.forceY(innerHeight / 2).strength(0.1));
  
  // Draw links
  const link = g.append("g")
    .selectAll("line")
    .data(data.links)
    .enter()
    .append("line")
    .attr("stroke", d => linkTypes[d.type].color)
    .attr("stroke-width", d => Math.max(1, d.value * 5))
    .attr("stroke-opacity", 0.6)
    .attr("stroke-dasharray", d => linkTypes[d.type].dashArray);
  
  // Draw nodes
  const node = g.append("g")
    .selectAll("g")
    .data(data.nodes)
    .enter()
    .append("g")
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));
  
  // Add circles for nodes
  node.append("circle")
    .attr("r", d => 20 + d.probability * 20)
    .attr("fill", d => colors[d.group])
    .attr("stroke", d => d.is_current ? "#000" : "white")
    .attr("stroke-width", d => d.is_current ? 3 : 1)
    .attr("stroke-dasharray", d => d.is_equilibrium ? null : "3,3");
  
  // Add text labels
  node.append("text")
    .attr("text-anchor", "middle")
    .attr("dy", ".35em")
    .attr("fill", "white")
    .text(d => d.name.substring(0, 3));
  
  // Add title for tooltips
  node.append("title")
    .text(d => `${d.name}\n調整スコア: ${Math.round(d.score * 100)}%\n発生確率: ${Math.round(d.probability * 100)}%\n${d.is_equilibrium ? '静止点: はい' : '静止点: いいえ'}`);
  
  // Update positions on simulation tick
  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);
    
    node
      .attr("transform", d => `translate(${d.x},${d.y})`);
  });
  
  // Add title
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", margin.top / 2)
    .attr("text-anchor", "middle")
    .attr("font-weight", "bold")
    .text(`${data.topic_name}のシナリオフロー`);
  
  // Add legend for node groups
  const nodeLegend = svg.append("g")
    .attr("transform", `translate(${width - margin.right - 150}, ${margin.top})`);
  
  Object.entries(colors).forEach(([group, color], i) => {
    const groupNames = {
      baseline: 'ベースライン',
      probability_based: '確率ベース',
      perspective_driven: '視点主導',
      disruptive: '破壊的'
    };
    
    nodeLegend.append("circle")
      .attr("cx", 7.5)
      .attr("cy", i * 25)
      .attr("r", 7.5)
      .attr("fill", color);
    
    nodeLegend.append("text")
      .attr("x", 20)
      .attr("y", i * 25 + 5)
      .text(groupNames[group]);
  });
  
  // Add legend for link types
  const linkLegend = svg.append("g")
    .attr("transform", `translate(${width - margin.right - 150}, ${margin.top + 120})`);
  
  Object.entries(linkTypes).forEach(([type, style], i) => {
    const typeNames = {
      positive: '肯定的',
      neutral: '中立的',
      negative: '否定的',
      related: '関連性'
    };
    
    linkLegend.append("line")
      .attr("x1", 0)
      .attr("y1", i * 25)
      .attr("x2", 15)
      .attr("y2", i * 25)
      .attr("stroke", style.color)
      .attr("stroke-width", 2)
      .attr("stroke-dasharray", style.dashArray);
    
    linkLegend.append("text")
      .attr("x", 20)
      .attr("y", i * 25 + 5)
      .text(typeNames[type]);
  });
  
  // Drag functions
  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  
  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }
  
  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
}
```

### 5. シナリオカード

シナリオカードは、各シナリオの詳細情報を直感的に表示するための効果的な手法です。

#### 実装方法

```javascript
// n8n workflow: Scenario Cards
// Function node for generating card data
[
  {
    "id": "generateCardData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Structured scenario data
        const structuredScenarios = $input.item.json;
        
        // Prepare card data
        const cards = structuredScenarios.scenario_groups
          .flatMap(group => group.scenarios)
          .map(scenario => ({
            id: scenario.scenario_id,
            name: scenario.name,
            description: scenario.description,
            group: scenario.scenario_id === 'baseline' ? 'baseline' :
                   scenario.scenario_id === 'optimistic' || scenario.scenario_id === 'pessimistic' ? 'probability_based' :
                   scenario.scenario_id === 'disruptive' ? 'disruptive' : 'perspective_driven',
            probability: scenario.probability,
            adjusted_score: scenario.adjusted_score,
            is_equilibrium: scenario.is_equilibrium,
            perspective_scores: scenario.perspective_scores,
            key_assumptions: scenario.key_assumptions,
            is_current: scenario.is_current,
            actions: structuredScenarios.scenario_actions
              .find(sa => sa.scenario_id === scenario.scenario_id)
              ?.actions || []
          }));
        
        return {
          json: {
            topic_id: structuredScenarios.topic_id,
            topic_name: structuredScenarios.topic_name,
            cards
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（React）

```jsx
// React component for scenario cards
function ScenarioCards({ data }) {
  const { cards } = data;
  
  // Group cards
  const groupedCards = {
    baseline: cards.filter(card => card.group === 'baseline'),
    probability_based: cards.filter(card => card.group === 'probability_based'),
    perspective_driven: cards.filter(card => card.group === 'perspective_driven'),
    disruptive: cards.filter(card => card.group === 'disruptive')
  };
  
  // Define group titles
  const groupTitles = {
    baseline: 'ベースラインシナリオ',
    probability_based: '確率ベースシナリオ',
    perspective_driven: '視点主導シナリオ',
    disruptive: '破壊的シナリオ'
  };
  
  // Define colors for different scenario groups
  const colors = {
    baseline: '#36a2eb',
    probability_based: '#ff6384',
    perspective_driven: '#4bc0c0',
    disruptive: '#9966ff'
  };
  
  return (
    <div className="scenario-cards">
      <h3>{data.topic_name}のシナリオカード</h3>
      
      {Object.entries(groupedCards).map(([group, cards]) => (
        <div key={group} className="card-group">
          <h4 style={{ color: colors[group] }}>{groupTitles[group]}</h4>
          
          <div className="cards-container">
            {cards.map(card => (
              <div 
                key={card.id} 
                className={`scenario-card ${card.is_current ? 'current-card' : ''}`}
                style={{ borderColor: colors[card.group] }}
              >
                <div 
                  className="card-header"
                  style={{ backgroundColor: colors[card.group] }}
                >
                  <h5>{card.name}</h5>
                  {card.is_current && (
                    <span className="current-badge">現在</span>
                  )}
                </div>
                
                <div className="card-body">
                  <p className="card-description">{card.description}</p>
                  
                  <div className="card-metrics">
                    <div className="metric">
                      <span className="metric-label">発生確率:</span>
                      <span className="metric-value">{Math.round(card.probability * 100)}%</span>
                    </div>
                    
                    <div className="metric">
                      <span className="metric-label">調整スコア:</span>
                      <span className="metric-value">{Math.round(card.adjusted_score * 100)}%</span>
                    </div>
                    
                    <div className="metric">
                      <span className="metric-label">静止点:</span>
                      <span className="metric-value">{card.is_equilibrium ? '✓' : '✗'}</span>
                    </div>
                  </div>
                  
                  <div className="perspective-scores">
                    <h6>視点別スコア</h6>
                    <div className="score-bars">
                      <div className="score-bar">
                        <span className="bar-label">テクノロジー</span>
                        <div className="bar-container">
                          <div 
                            className="bar-fill"
                            style={{ 
                              width: `${card.perspective_scores.technology * 100}%`,
                              backgroundColor: '#9c27b0'
                            }}
                          ></div>
                        </div>
                        <span className="bar-value">
                          {Math.round(card.perspective_scores.technology * 100)}%
                        </span>
                      </div>
                      
                      <div className="score-bar">
                        <span className="bar-label">マーケット</span>
                        <div className="bar-container">
                          <div 
                            className="bar-fill"
                            style={{ 
                              width: `${card.perspective_scores.market * 100}%`,
                              backgroundColor: '#2196f3'
                            }}
                          ></div>
                        </div>
                        <span className="bar-value">
                          {Math.round(card.perspective_scores.market * 100)}%
                        </span>
                      </div>
                      
                      <div className="score-bar">
                        <span className="bar-label">ビジネス</span>
                        <div className="bar-container">
                          <div 
                            className="bar-fill"
                            style={{ 
                              width: `${card.perspective_scores.business * 100}%`,
                              backgroundColor: '#4caf50'
                            }}
                          ></div>
                        </div>
                        <span className="bar-value">
                          {Math.round(card.perspective_scores.business * 100)}%
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="key-assumptions">
                    <h6>主要な前提条件</h6>
                    <ul>
                      {card.key_assumptions.map((assumption, index) => (
                        <li key={index}>{assumption}</li>
                      ))}
                    </ul>
                  </div>
                  
                  {card.actions.length > 0 && (
                    <div className="recommended-actions">
                      <h6>推奨アクション</h6>
                      <ul>
                        {card.actions.map(action => (
                          <li key={action.action_id}>
                            <strong>{action.name}:</strong> {action.description}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

## 代替シナリオ可視化の統合

上記の可視化手法を組み合わせることで、代替シナリオの効果的な可視化が可能になります。以下に、これらの手法を統合したダッシュボードの例を示します。

### 統合ダッシュボードの構成

1. **概要表示**
   - シナリオ比較テーブル（簡潔な概要）
   - 現在のシナリオと代替シナリオの関係

2. **詳細表示**
   - レーダーチャート比較（視点別スコアの比較）
   - パラレルコーディネートプロット（多次元データの比較）
   - シナリオフローチャート（シナリオ間の関係性）
   - シナリオカード（各シナリオの詳細情報）

3. **インタラクティブ要素**
   - シナリオの選択と比較
   - シナリオの詳細表示
   - シナリオ間の切り替え

### 実装例（React）

```jsx
// React component for integrated alternative scenario visualization
function AlternativeScenarioVisualization({ topicId, date }) {
  const [scenarioData, setScenarioData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedScenarios, setSelectedScenarios] = useState([]);
  const [activeTab, setActiveTab] = useState('table');
  
  useEffect(() => {
    // Fetch scenario data
    async function fetchData() {
      try {
        setLoading(true);
        
        // In a real implementation, this would be an API call
        const response = await fetch(`/api/scenarios?topic_id=${topicId}&date=${date}`);
        const data = await response.json();
        
        setScenarioData(data);
        
        // Select baseline and optimistic scenarios by default
        const baselineScenario = data.all_scenarios.find(s => s.scenario_id === 'baseline');
        const optimisticScenario = data.all_scenarios.find(s => s.scenario_id === 'optimistic');
        
        if (baselineScenario && optimisticScenario) {
          setSelectedScenarios([baselineScenario.scenario_id, optimisticScenario.scenario_id]);
        } else if (data.all_scenarios.length >= 2) {
          setSelectedScenarios([
            data.all_scenarios[0].scenario_id,
            data.all_scenarios[1].scenario_id
          ]);
        } else if (data.all_scenarios.length === 1) {
          setSelectedScenarios([data.all_scenarios[0].scenario_id]);
        }
      } catch (error) {
        console.error('Error fetching scenario data:', error);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, [topicId, date]);
  
  if (loading) {
    return <div>Loading scenario data...</div>;
  }
  
  if (!scenarioData) {
    return <div>No scenario data available</div>;
  }
  
  // Filter scenarios based on selection
  const filteredScenarios = scenarioData.all_scenarios.filter(
    scenario => selectedScenarios.includes(scenario.scenario_id)
  );
  
  // Handle scenario selection
  const handleScenarioSelection = (scenarioId) => {
    if (selectedScenarios.includes(scenarioId)) {
      // Remove if already selected
      setSelectedScenarios(selectedScenarios.filter(id => id !== scenarioId));
    } else {
      // Add if not selected (limit to 5 for readability)
      if (selectedScenarios.length < 5) {
        setSelectedScenarios([...selectedScenarios, scenarioId]);
      }
    }
  };
  
  return (
    <div className="alternative-scenario-visualization">
      <div className="visualization-header">
        <h2>{scenarioData.topic_name}の代替シナリオ</h2>
        
        <div className="scenario-selector">
          <h4>シナリオ選択</h4>
          <div className="scenario-checkboxes">
            {scenarioData.all_scenarios.map(scenario => (
              <label key={scenario.scenario_id} className="scenario-checkbox">
                <input
                  type="checkbox"
                  checked={selectedScenarios.includes(scenario.scenario_id)}
                  onChange={() => handleScenarioSelection(scenario.scenario_id)}
                />
                <span className={`checkbox-label ${scenario.is_current ? 'current-scenario' : ''}`}>
                  {scenario.name}
                  {scenario.is_current && <span className="current-badge">現在</span>}
                </span>
              </label>
            ))}
          </div>
        </div>
        
        <div className="visualization-tabs">
          <button
            className={`tab-button ${activeTab === 'table' ? 'active' : ''}`}
            onClick={() => setActiveTab('table')}
          >
            テーブル
          </button>
          <button
            className={`tab-button ${activeTab === 'radar' ? 'active' : ''}`}
            onClick={() => setActiveTab('radar')}
          >
            レーダーチャート
          </button>
          <button
            className={`tab-button ${activeTab === 'parallel' ? 'active' : ''}`}
            onClick={() => setActiveTab('parallel')}
          >
            パラレルプロット
          </button>
          <button
            className={`tab-button ${activeTab === 'flow' ? 'active' : ''}`}
            onClick={() => setActiveTab('flow')}
          >
            フローチャート
          </button>
          <button
            className={`tab-button ${activeTab === 'cards' ? 'active' : ''}`}
            onClick={() => setActiveTab('cards')}
          >
            カード
          </button>
        </div>
      </div>
      
      <div className="visualization-content">
        {activeTab === 'table' && (
          <ScenarioComparisonTable 
            data={{
              topic_id: scenarioData.topic_id,
              topic_name: scenarioData.topic_name,
              table_data: {
                headers: [
                  { id: 'name', label: 'シナリオ名', type: 'text' },
                  { id: 'probability', label: '発生確率', type: 'percentage' },
                  { id: 'adjusted_score', label: '調整スコア', type: 'percentage' },
                  { id: 'is_equilibrium', label: '静止点', type: 'boolean' },
                  { id: 'technology_score', label: 'テクノロジー', type: 'percentage' },
                  { id: 'market_score', label: 'マーケット', type: 'percentage' },
                  { id: 'business_score', label: 'ビジネス', type: 'percentage' }
                ],
                rows: filteredScenarios.map(scenario => ({
                  id: scenario.scenario_id,
                  name: scenario.name,
                  probability: scenario.probability,
                  adjusted_score: scenario.adjusted_score,
                  is_equilibrium: scenario.is_equilibrium,
                  technology_score: scenario.perspective_scores.technology,
                  market_score: scenario.perspective_scores.market,
                  business_score: scenario.perspective_scores.business,
                  is_current: scenario.is_current,
                  group_id: scenario.scenario_id === 'baseline' ? 'baseline' :
                           scenario.scenario_id === 'optimistic' || scenario.scenario_id === 'pessimistic' ? 'probability_based' :
                           scenario.scenario_id === 'disruptive' ? 'disruptive' : 'perspective_driven'
                }))
              }
            }}
          />
        )}
        
        {activeTab === 'radar' && (
          <div id="radar-chart-container" className="chart-container">
            {/* Radar chart will be rendered here using D3 or Chart.js */}
            {/* This would call renderScenarioRadarChart with filtered data */}
          </div>
        )}
        
        {activeTab === 'parallel' && (
          <div id="parallel-plot-container" className="chart-container">
            {/* Parallel coordinates plot will be rendered here using D3 */}
            {/* This would call renderParallelCoordinatesPlot with filtered data */}
          </div>
        )}
        
        {activeTab === 'flow' && (
          <div id="flow-chart-container" className="chart-container">
            {/* Flow chart will be rendered here using D3 */}
            {/* This would call renderScenarioFlowChart with filtered data */}
          </div>
        )}
        
        {activeTab === 'cards' && (
          <ScenarioCards
            data={{
              topic_id: scenarioData.topic_id,
              topic_name: scenarioData.topic_name,
              cards: filteredScenarios.map(scenario => ({
                id: scenario.scenario_id,
                name: scenario.name,
                description: scenario.description,
                group: scenario.scenario_id === 'baseline' ? 'baseline' :
                       scenario.scenario_id === 'optimistic' || scenario.scenario_id === 'pessimistic' ? 'probability_based' :
                       scenario.scenario_id === 'disruptive' ? 'disruptive' : 'perspective_driven',
                probability: scenario.probability,
                adjusted_score: scenario.adjusted_score,
                is_equilibrium: scenario.is_equilibrium,
                perspective_scores: scenario.perspective_scores,
                key_assumptions: scenario.key_assumptions,
                is_current: scenario.is_current,
                actions: scenario.actions || []
              }))
            }}
          />
        )}
      </div>
      
      <div className="scenario-insights">
        <h4>シナリオインサイト</h4>
        <div className="insights-content">
          {generateScenarioInsights(filteredScenarios)}
        </div>
      </div>
    </div>
  );
}

// Helper function to generate insights based on selected scenarios
function generateScenarioInsights(scenarios) {
  if (scenarios.length === 0) {
    return <p>シナリオを選択してください。</p>;
  }
  
  if (scenarios.length === 1) {
    const scenario = scenarios[0];
    return (
      <div>
        <p>
          <strong>{scenario.name}</strong>は
          {scenario.is_equilibrium ? 
            '静止点として検出され、' : 
            '静止点として検出されず、'}
          発生確率は<strong>{Math.round(scenario.probability * 100)}%</strong>です。
        </p>
        <p>
          このシナリオでは、
          {Object.entries(scenario.perspective_scores)
            .sort((a, b) => b[1] - a[1])
            .map(([perspective, score], index) => {
              const perspectiveNames = {
                technology: 'テクノロジー',
                market: 'マーケット',
                business: 'ビジネス'
              };
              return index === 0 ? 
                `${perspectiveNames[perspective]}視点が最も高く（${Math.round(score * 100)}%）` : 
                '';
            })}
          評価されています。
        </p>
      </div>
    );
  }
  
  // Compare multiple scenarios
  const baselineScenario = scenarios.find(s => s.scenario_id === 'baseline');
  const otherScenarios = scenarios.filter(s => s.scenario_id !== 'baseline');
  
  if (baselineScenario && otherScenarios.length > 0) {
    return (
      <div>
        <p>
          ベースラインシナリオと比較して、
          {otherScenarios.map((scenario, index) => {
            const scoreDiff = scenario.adjusted_score - baselineScenario.adjusted_score;
            const scoreDiffText = scoreDiff > 0 ? 
              `${Math.round(scoreDiff * 100)}%高く` : 
              `${Math.round(Math.abs(scoreDiff * 100))}%低く`;
            
            return (
              <span key={scenario.scenario_id}>
                {index > 0 && '、'}
                <strong>{scenario.name}</strong>は調整スコアが{scoreDiffText}
              </span>
            );
          })}
          評価されています。
        </p>
        
        {otherScenarios.some(s => s.is_equilibrium) && (
          <p>
            選択されたシナリオのうち、
            {otherScenarios
              .filter(s => s.is_equilibrium)
              .map((scenario, index, arr) => (
                <span key={scenario.scenario_id}>
                  {index > 0 && index === arr.length - 1 ? 'および' : index > 0 ? '、' : ''}
                  <strong>{scenario.name}</strong>
                </span>
              ))}
            は静止点として検出されています。
          </p>
        )}
      </div>
    );
  }
  
  return (
    <p>
      選択された{scenarios.length}つのシナリオの中で、
      {scenarios
        .sort((a, b) => b.adjusted_score - a.adjusted_score)
        .slice(0, 1)
        .map(scenario => (
          <strong key={scenario.scenario_id}>{scenario.name}</strong>
        ))}
      が最も高い調整スコア（{Math.round(scenarios[0].adjusted_score * 100)}%）を持っています。
    </p>
  );
}
```

## 代替シナリオ可視化のベストプラクティス

代替シナリオの可視化を効果的に実装するためのベストプラクティスを以下に示します：

### 1. 明確な区別と比較

- 各シナリオを視覚的に明確に区別（色、形、ラベルなど）
- ベースラインシナリオと代替シナリオの関係を明示
- 主要な指標に基づく直接比較の提供

### 2. 多次元データの効果的な表現

- 複数の視点や指標を同時に表示
- 相互関係や依存関係の可視化
- 重要な次元の強調

### 3. コンテキストと前提条件の提供

- 各シナリオの前提条件を明示
- 発生確率や信頼度の表示
- 静止点との関係の説明

### 4. インタラクティブな探索の促進

- シナリオの選択と比較機能
- 詳細情報へのドリルダウン
- カスタム視点の設定

### 5. アクションへの連携

- 各シナリオに関連する推奨アクションの提示
- アクションの優先順位付け
- モニタリングポイントの明示

### 6. 時間的変化の表現

- シナリオの時間的進化の可視化
- トリガーポイントやマイルストーンの表示
- 将来の分岐点の明示

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおける代替シナリオの可視化について詳細に解説しました。シナリオ比較テーブル、レーダーチャート比較、パラレルコーディネートプロット、シナリオフローチャート、シナリオカードなど、様々な可視化手法を紹介し、それらの実装方法を示しました。

これらの手法を組み合わせることで、代替シナリオの効果的な可視化が可能になり、ユーザーは複数の可能性を比較検討し、より堅牢な意思決定を行うことができます。特に情報不均衡や不確実性が高い状況では、代替シナリオの可視化が意思決定の質を大きく左右します。

次のセクションでは、インタラクティブダッシュボードの全体設計と実装について詳細に解説します。
