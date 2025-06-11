# シナリオ生成と予測の活用（パート3-2：意思決定支援の方法論）

## 意思決定支援の基本フレームワーク

トリプルパースペクティブ型戦略AIレーダーにおける予測とシナリオは、それ自体が目的ではなく、より良い意思決定を支援するための手段です。本セクションでは、生成された予測とシナリオを活用して意思決定を支援する方法論について詳細に解説します。

### 意思決定支援の目的と価値

トリプルパースペクティブ型戦略AIレーダーによる意思決定支援の主な目的と価値は以下の通りです：

1. **情報の非対称性の解消**: 意思決定者が持つ情報の偏りや不足を補完
2. **認知バイアスの軽減**: データに基づく客観的な視点を提供し、人間の認知バイアスを軽減
3. **複雑性の縮減**: 複雑な状況を構造化し、理解可能な形で提示
4. **意思決定の質の向上**: より多くの選択肢と結果の可能性を考慮した意思決定を促進
5. **意思決定プロセスの透明化**: 決定の根拠と論理を明示的に示すことで、説明責任を向上

### 意思決定支援の基本アプローチ

トリプルパースペクティブ型戦略AIレーダーでは、以下の3つの基本アプローチを組み合わせて意思決定を支援します：

1. **情報提供型アプローチ**: 予測とシナリオを通じて、意思決定に必要な情報を提供
2. **選択肢生成型アプローチ**: 複数の選択肢（アクション）とその潜在的な結果を生成
3. **評価支援型アプローチ**: 各選択肢の評価基準と比較方法を提供

これらのアプローチを組み合わせることで、意思決定者は情報に基づいた、バランスの取れた意思決定を行うことができます。

## 意思決定マトリクスの構築

意思決定支援の中核となるのが、意思決定マトリクスの構築です。意思決定マトリクスは、選択肢（アクション）とシナリオの組み合わせに対する結果を構造化して表現するフレームワークです。n8nを使用した意思決定マトリクスの構築例を示します。

```javascript
// n8n workflow: Decision Matrix Construction
// Function node for constructing decision matrix
[
  {
    "id": "loadIntegratedScenarios",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "scenarios",
      "filter": {
        "execution_id": "={{ $node[\"loadExecutionId\"].json.execution_id }}",
        "scenario_type": "integrated"
      },
      "options": {
        "sort": {
          "timestamp": -1
        }
      }
    }
  },
  {
    "id": "generateActionOptions",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get integrated scenarios
        const integratedScenarios = $input.item.json;
        const scenarios = integratedScenarios.scenarios;
        const executionId = integratedScenarios.execution_id;
        
        // Generate action options
        const generateActions = () => {
          const actions = [];
          const actionCategories = ['technology', 'market', 'business', 'combined'];
          
          // Collect all strategic options from scenarios
          const allOptions = [];
          scenarios.forEach(scenario => {
            if (scenario.strategic_options) {
              allOptions.push(...scenario.strategic_options);
            }
          });
          
          // Group options by category
          const optionsByCategory = {};
          actionCategories.forEach(category => {
            optionsByCategory[category] = allOptions.filter(option => option.category === category);
          });
          
          // Select top options from each category
          actionCategories.forEach(category => {
            const categoryOptions = optionsByCategory[category];
            
            // Sort by frequency (how many scenarios suggest this option)
            const optionCounts = {};
            categoryOptions.forEach(option => {
              const key = option.name;
              optionCounts[key] = (optionCounts[key] || 0) + 1;
            });
            
            // Get unique options
            const uniqueOptions = [];
            const addedNames = new Set();
            
            categoryOptions.forEach(option => {
              if (!addedNames.has(option.name)) {
                uniqueOptions.push(option);
                addedNames.add(option.name);
              }
            });
            
            // Sort by frequency
            uniqueOptions.sort((a, b) => {
              return (optionCounts[b.name] || 0) - (optionCounts[a.name] || 0);
            });
            
            // Select top 3 options
            const topOptions = uniqueOptions.slice(0, 3);
            
            // Add to actions
            topOptions.forEach(option => {
              actions.push({
                id: \`action_\${actions.length + 1}\`,
                name: option.name,
                description: option.description,
                category: option.category,
                impact: option.impact
              });
            });
          });
          
          return actions;
        };
        
        const actions = generateActions();
        
        return {
          json: {
            execution_id: executionId,
            actions: actions,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "constructDecisionMatrix",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get scenarios and actions
        const scenarios = $input.item(0).json.scenarios;
        const actions = $input.item(1).json.actions;
        const executionId = $input.item(0).json.execution_id;
        
        // Construct decision matrix
        const constructMatrix = () => {
          const matrix = [];
          
          // For each action
          actions.forEach(action => {
            const actionRow = {
              action_id: action.id,
              action_name: action.name,
              action_description: action.description,
              action_category: action.category,
              scenarios: []
            };
            
            // For each scenario
            scenarios.forEach(scenario => {
              // Evaluate action under this scenario
              const evaluateActionUnderScenario = (action, scenario) => {
                // In a real implementation, this would use a more sophisticated evaluation model
                // For demonstration, we'll use a simple rule-based approach
                
                let alignment = 0;
                let risk = 0;
                let opportunity = 0;
                
                // Check alignment with scenario factors
                if (scenario.factors) {
                  scenario.factors.forEach(factor => {
                    // Technology alignment
                    if (factor.perspective === 'technology' && action.category === 'technology') {
                      if (factor.state === 'high' && action.name.includes('技術投資')) {
                        alignment += 2;
                        opportunity += 2;
                      } else if (factor.state === 'low' && action.name.includes('技術投資')) {
                        alignment -= 1;
                        risk += 2;
                      }
                    }
                    
                    // Market alignment
                    if (factor.perspective === 'market' && action.category === 'market') {
                      if (factor.state === 'high' && action.name.includes('市場拡大')) {
                        alignment += 2;
                        opportunity += 2;
                      } else if (factor.state === 'low' && action.name.includes('市場拡大')) {
                        alignment -= 1;
                        risk += 2;
                      }
                    }
                    
                    // Business alignment
                    if (factor.perspective === 'business' && action.category === 'business') {
                      if (factor.state === 'high' && action.name.includes('スケール')) {
                        alignment += 2;
                        opportunity += 2;
                      } else if (factor.state === 'low' && action.name.includes('スケール')) {
                        alignment -= 1;
                        risk += 2;
                      }
                    }
                  });
                }
                
                // Check alignment with scenario name
                if (scenario.name.includes('高成長') && action.name.includes('拡大')) {
                  alignment += 1;
                  opportunity += 1;
                }
                
                if (scenario.name.includes('低迷') && action.name.includes('再構築')) {
                  alignment += 1;
                  opportunity += 1;
                }
                
                // Calculate overall score
                const score = alignment + opportunity - risk;
                
                // Determine recommendation
                let recommendation;
                let recommendationReason;
                
                if (score >= 3) {
                  recommendation = 'highly_recommended';
                  recommendationReason = '高い整合性と機会があり、リスクが低い';
                } else if (score >= 1) {
                  recommendation = 'recommended';
                  recommendationReason = '一定の整合性と機会があり、リスクは管理可能';
                } else if (score >= -1) {
                  recommendation = 'neutral';
                  recommendationReason = '整合性、機会、リスクがバランスしている';
                } else if (score >= -3) {
                  recommendation = 'not_recommended';
                  recommendationReason = 'リスクが高く、整合性と機会が限られている';
                } else {
                  recommendation = 'strongly_against';
                  recommendationReason = '非常に高いリスクと低い整合性、限られた機会';
                }
                
                return {
                  alignment: alignment,
                  risk: risk,
                  opportunity: opportunity,
                  score: score,
                  recommendation: recommendation,
                  recommendation_reason: recommendationReason
                };
              };
              
              const evaluation = evaluateActionUnderScenario(action, scenario);
              
              actionRow.scenarios.push({
                scenario_id: scenario.id,
                scenario_name: scenario.name,
                probability: scenario.probability,
                evaluation: evaluation
              });
            });
            
            // Calculate expected value across all scenarios
            const calculateExpectedValue = (actionRow) => {
              let weightedScore = 0;
              let totalProbability = 0;
              
              actionRow.scenarios.forEach(scenario => {
                weightedScore += scenario.evaluation.score * scenario.probability;
                totalProbability += scenario.probability;
              });
              
              const expectedScore = totalProbability > 0 ? weightedScore / totalProbability : 0;
              
              // Determine overall recommendation
              let overallRecommendation;
              
              if (expectedScore >= 2) {
                overallRecommendation = 'highly_recommended';
              } else if (expectedScore >= 0.5) {
                overallRecommendation = 'recommended';
              } else if (expectedScore >= -0.5) {
                overallRecommendation = 'neutral';
              } else if (expectedScore >= -2) {
                overallRecommendation = 'not_recommended';
              } else {
                overallRecommendation = 'strongly_against';
              }
              
              return {
                expected_score: expectedScore,
                overall_recommendation: overallRecommendation
              };
            };
            
            const expectedValue = calculateExpectedValue(actionRow);
            actionRow.expected_value = expectedValue;
            
            matrix.push(actionRow);
          });
          
          return matrix;
        };
        
        const decisionMatrix = constructMatrix();
        
        return {
          json: {
            execution_id: executionId,
            decision_matrix: decisionMatrix,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveDecisionMatrix",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "decision_matrices",
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

## 意思決定支援ダッシュボードの構築

意思決定マトリクスを構築したら、次のステップは意思決定支援ダッシュボードの構築です。意思決定支援ダッシュボードは、意思決定マトリクスの情報を視覚的に表現し、意思決定者が直感的に理解できるようにするためのインターフェースです。n8nを使用した意思決定支援ダッシュボードの構築例を示します。

```javascript
// n8n workflow: Decision Support Dashboard Construction
// Function node for constructing decision support dashboard
[
  {
    "id": "loadDecisionMatrix",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "decision_matrices",
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
    "id": "generateDashboardData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get decision matrix
        const decisionMatrix = $input.item.json;
        const matrix = decisionMatrix.decision_matrix;
        const executionId = decisionMatrix.execution_id;
        
        // Generate dashboard data
        const generateDashboardData = () => {
          // Action recommendation summary
          const actionSummary = matrix.map(action => ({
            action_id: action.action_id,
            action_name: action.action_name,
            action_category: action.action_category,
            expected_score: action.expected_value.expected_score,
            overall_recommendation: action.expected_value.overall_recommendation
          }));
          
          // Sort actions by expected score (descending)
          actionSummary.sort((a, b) => b.expected_score - a.expected_score);
          
          // Scenario impact analysis
          const scenarioImpact = [];
          
          // Get unique scenario IDs
          const scenarioIds = new Set();
          matrix.forEach(action => {
            action.scenarios.forEach(scenario => {
              scenarioIds.add(scenario.scenario_id);
            });
          });
          
          // For each scenario
          Array.from(scenarioIds).forEach(scenarioId => {
            const scenarioActions = [];
            
            // For each action
            matrix.forEach(action => {
              const scenario = action.scenarios.find(s => s.scenario_id === scenarioId);
              
              if (scenario) {
                scenarioActions.push({
                  action_id: action.action_id,
                  action_name: action.action_name,
                  score: scenario.evaluation.score,
                  recommendation: scenario.evaluation.recommendation
                });
              }
            });
            
            // Sort actions by score (descending)
            scenarioActions.sort((a, b) => b.score - a.score);
            
            // Get scenario name and probability
            const scenarioName = matrix[0].scenarios.find(s => s.scenario_id === scenarioId).scenario_name;
            const scenarioProbability = matrix[0].scenarios.find(s => s.scenario_id === scenarioId).probability;
            
            scenarioImpact.push({
              scenario_id: scenarioId,
              scenario_name: scenarioName,
              probability: scenarioProbability,
              actions: scenarioActions
            });
          });
          
          // Sort scenarios by probability (descending)
          scenarioImpact.sort((a, b) => b.probability - a.probability);
          
          // Risk-opportunity analysis
          const riskOpportunityAnalysis = matrix.map(action => {
            // Calculate average risk and opportunity across all scenarios
            let totalRisk = 0;
            let totalOpportunity = 0;
            let totalProbability = 0;
            
            action.scenarios.forEach(scenario => {
              totalRisk += scenario.evaluation.risk * scenario.probability;
              totalOpportunity += scenario.evaluation.opportunity * scenario.probability;
              totalProbability += scenario.probability;
            });
            
            const avgRisk = totalProbability > 0 ? totalRisk / totalProbability : 0;
            const avgOpportunity = totalProbability > 0 ? totalOpportunity / totalProbability : 0;
            
            return {
              action_id: action.action_id,
              action_name: action.action_name,
              risk: avgRisk,
              opportunity: avgOpportunity,
              risk_opportunity_ratio: avgRisk > 0 ? avgOpportunity / avgRisk : avgOpportunity
            };
          });
          
          // Sort by risk-opportunity ratio (descending)
          riskOpportunityAnalysis.sort((a, b) => b.risk_opportunity_ratio - a.risk_opportunity_ratio);
          
          return {
            action_summary: actionSummary,
            scenario_impact: scenarioImpact,
            risk_opportunity_analysis: riskOpportunityAnalysis
          };
        };
        
        const dashboardData = generateDashboardData();
        
        return {
          json: {
            execution_id: executionId,
            dashboard_data: dashboardData,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "generateDashboardHTML",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get dashboard data
        const dashboardData = $input.item.json.dashboard_data;
        const executionId = $input.item.json.execution_id;
        
        // Generate HTML dashboard
        const generateHTML = () => {
          // Helper function to get recommendation color
          const getRecommendationColor = (recommendation) => {
            switch (recommendation) {
              case 'highly_recommended':
                return '#2e7d32'; // Dark green
              case 'recommended':
                return '#388e3c'; // Green
              case 'neutral':
                return '#f9a825'; // Amber
              case 'not_recommended':
                return '#e65100'; // Orange
              case 'strongly_against':
                return '#c62828'; // Red
              default:
                return '#757575'; // Grey
            }
          };
          
          // Helper function to get recommendation label
          const getRecommendationLabel = (recommendation) => {
            switch (recommendation) {
              case 'highly_recommended':
                return '強く推奨';
              case 'recommended':
                return '推奨';
              case 'neutral':
                return '中立';
              case 'not_recommended':
                return '非推奨';
              case 'strongly_against':
                return '強く非推奨';
              default:
                return '不明';
            }
          };
          
          // Generate action summary table
          const generateActionSummaryTable = () => {
            const rows = dashboardData.action_summary.map(action => {
              const recommendationColor = getRecommendationColor(action.overall_recommendation);
              const recommendationLabel = getRecommendationLabel(action.overall_recommendation);
              
              return \`
                <tr>
                  <td>\${action.action_name}</td>
                  <td>\${action.action_category}</td>
                  <td>\${action.expected_score.toFixed(2)}</td>
                  <td style="color: \${recommendationColor}; font-weight: bold;">\${recommendationLabel}</td>
                </tr>
              \`;
            }).join('');
            
            return \`
              <table class="action-summary-table">
                <thead>
                  <tr>
                    <th>アクション</th>
                    <th>カテゴリ</th>
                    <th>期待スコア</th>
                    <th>推奨度</th>
                  </tr>
                </thead>
                <tbody>
                  \${rows}
                </tbody>
              </table>
            \`;
          };
          
          // Generate scenario impact tables
          const generateScenarioImpactTables = () => {
            return dashboardData.scenario_impact.map(scenario => {
              const rows = scenario.actions.map(action => {
                const recommendationColor = getRecommendationColor(action.recommendation);
                const recommendationLabel = getRecommendationLabel(action.recommendation);
                
                return \`
                  <tr>
                    <td>\${action.action_name}</td>
                    <td>\${action.score.toFixed(2)}</td>
                    <td style="color: \${recommendationColor}; font-weight: bold;">\${recommendationLabel}</td>
                  </tr>
                \`;
              }).join('');
              
              return \`
                <div class="scenario-impact-section">
                  <h3>\${scenario.scenario_name} (確率: \${(scenario.probability * 100).toFixed(1)}%)</h3>
                  <table class="scenario-impact-table">
                    <thead>
                      <tr>
                        <th>アクション</th>
                        <th>スコア</th>
                        <th>推奨度</th>
                      </tr>
                    </thead>
                    <tbody>
                      \${rows}
                    </tbody>
                  </table>
                </div>
              \`;
            }).join('');
          };
          
          // Generate risk-opportunity chart data
          const generateRiskOpportunityChartData = () => {
            const chartData = dashboardData.risk_opportunity_analysis.map(action => {
              return {
                name: action.action_name,
                risk: action.risk,
                opportunity: action.opportunity
              };
            });
            
            return JSON.stringify(chartData);
          };
          
          // Complete HTML
          return \`
            <!DOCTYPE html>
            <html>
            <head>
              <title>意思決定支援ダッシュボード</title>
              <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2, h3 { color: #333; }
                .section { margin-bottom: 30px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f5f5f5; }
                .chart-container { height: 400px; margin-bottom: 20px; }
              </style>
              <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
              <h1>意思決定支援ダッシュボード</h1>
              
              <div class="section">
                <h2>アクション推奨サマリー</h2>
                \${generateActionSummaryTable()}
              </div>
              
              <div class="section">
                <h2>リスク・機会分析</h2>
                <div class="chart-container">
                  <canvas id="riskOpportunityChart"></canvas>
                </div>
              </div>
              
              <div class="section">
                <h2>シナリオ別影響分析</h2>
                \${generateScenarioImpactTables()}
              </div>
              
              <script>
                // Risk-Opportunity Chart
                const riskOpportunityData = \${generateRiskOpportunityChartData()};
                
                const ctx = document.getElementById('riskOpportunityChart').getContext('2d');
                new Chart(ctx, {
                  type: 'scatter',
                  data: {
                    datasets: [{
                      label: 'アクション',
                      data: riskOpportunityData.map(item => ({
                        x: item.risk,
                        y: item.opportunity,
                        name: item.name
                      })),
                      backgroundColor: 'rgba(54, 162, 235, 0.7)',
                      borderColor: 'rgba(54, 162, 235, 1)',
                      borderWidth: 1,
                      pointRadius: 8,
                      pointHoverRadius: 10
                    }]
                  },
                  options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                      x: {
                        title: {
                          display: true,
                          text: 'リスク'
                        },
                        min: 0
                      },
                      y: {
                        title: {
                          display: true,
                          text: '機会'
                        },
                        min: 0
                      }
                    },
                    plugins: {
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            const point = context.raw;
                            return \`\${point.name} (リスク: \${point.x.toFixed(2)}, 機会: \${point.y.toFixed(2)})\`;
                          }
                        }
                      }
                    }
                  }
                });
              </script>
            </body>
            </html>
          \`;
        };
        
        const dashboardHTML = generateHTML();
        
        return {
          json: {
            execution_id: executionId,
            dashboard_html: dashboardHTML,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveDashboardHTML",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "dashboards",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "writeHTMLToFile",
    "type": "n8n-nodes-base.writeFile",
    "parameters": {
      "fileName": "={{ 'decision_dashboard_' + $json.execution_id + '.html' }}",
      "fileContent": "={{ $json.dashboard_html }}",
      "directory": "/tmp"
    }
  }
]
```

## 意思決定支援のベストプラクティス

トリプルパースペクティブ型戦略AIレーダーを活用した意思決定支援を効果的に行うためのベストプラクティスを以下に示します。

### 1. 人間とAIの適切な役割分担

意思決定支援システムは、人間の意思決定者を置き換えるものではなく、補完するものです。以下の役割分担を意識することが重要です：

- **AIの役割**:
  - データの収集と分析
  - パターンの検出と予測
  - 複数のシナリオの生成
  - 選択肢の評価と比較

- **人間の役割**:
  - 価値判断と優先順位の設定
  - 倫理的・社会的影響の考慮
  - 直感と経験の活用
  - 最終的な意思決定

### 2. 透明性と説明可能性の確保

意思決定支援システムの推奨事項は、その根拠と論理が明確に説明できることが重要です：

- 推奨の根拠となるデータと分析を明示
- 使用したモデルとアルゴリズムの特性と限界を理解
- 不確実性と信頼区間を明示的に表現
- 代替シナリオと「What-if」分析の提供

### 3. 継続的なフィードバックと学習

意思決定支援システムは、実際の意思決定結果からフィードバックを得て継続的に改善することが重要です：

- 予測と実際の結果の比較と分析
- 意思決定者からのフィードバックの収集と反映
- モデルとアルゴリズムの定期的な更新と改善
- 新たな情報源とデータの継続的な追加

### 4. コンテキストの考慮

意思決定支援システムは、組織や業界の特定のコンテキストを考慮することが重要です：

- 組織の戦略目標と価値観の反映
- 業界特有の動向と規制環境の考慮
- 組織の能力と制約の現実的な評価
- 文化的・地理的要因の考慮

### 5. 多様な視点の統合

トリプルパースペクティブ型戦略AIレーダーの強みを活かすために、多様な視点を統合することが重要です：

- テクノロジー、マーケット、ビジネスの3つの視点のバランス
- 短期的視点と長期的視点の両方の考慮
- 定量的分析と定性的分析の組み合わせ
- 異なる専門分野や部門からの視点の統合

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおける意思決定支援の方法論について詳細に解説しました。意思決定支援の基本フレームワーク、意思決定マトリクスの構築、意思決定支援ダッシュボードの構築、そして意思決定支援のベストプラクティスについて説明しました。これらの方法論を活用することで、予測とシナリオを効果的に意思決定に活かすことができます。

次のセクションでは、アクション推奨の生成方法について詳細に解説します。
