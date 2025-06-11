# シナリオ生成と予測の活用（パート3-3：アクション推奨の生成方法）

## アクション推奨の基本概念

トリプルパースペクティブ型戦略AIレーダーの最終的な目標は、単に予測やシナリオを提供するだけでなく、具体的なアクションの推奨を通じて意思決定者を支援することです。本セクションでは、予測とシナリオに基づいたアクション推奨の生成方法について詳細に解説します。

### アクション推奨の目的と価値

アクション推奨の主な目的と価値は以下の通りです：

1. **意思決定の具体化**: 抽象的な予測やシナリオを具体的な行動に変換
2. **選択肢の明確化**: 取りうる選択肢とその潜在的な結果を明示
3. **優先順位の提案**: 複数のアクションの中から優先すべきものを提案
4. **リスク・リターンの最適化**: リスクとリターンのバランスを考慮したアクションの提案
5. **実行可能性の評価**: 組織の能力と制約を考慮した実行可能なアクションの提案

### アクション推奨の種類

トリプルパースペクティブ型戦略AIレーダーでは、以下の3つの種類のアクション推奨を生成します：

1. **戦略的アクション**: 長期的な方向性や大きな意思決定に関するアクション
   - 例：新規事業への参入、大規模な投資、組織再編

2. **戦術的アクション**: 中期的な計画や具体的な施策に関するアクション
   - 例：特定市場でのマーケティング強化、製品ラインの拡充、パートナーシップの構築

3. **運用的アクション**: 短期的な対応や日常的な業務に関するアクション
   - 例：価格調整、在庫管理の最適化、顧客対応の改善

これらの異なるレベルのアクション推奨を組み合わせることで、包括的な意思決定支援を提供します。

## アクション生成エンジンの実装

アクション推奨を生成するためのエンジンを実装する方法について解説します。n8nを使用したアクション生成エンジンの実装例を示します。

```javascript
// n8n workflow: Action Recommendation Engine
// Function node for generating action recommendations
[
  {
    "id": "loadScenarios",
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
    "id": "loadPredictions",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "predictions",
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
    "id": "loadOrganizationContext",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "organization_context",
      "filter": {
        "organization_id": "={{ $node[\"loadOrganizationId\"].json.organization_id }}"
      }
    }
  },
  {
    "id": "generateActionRecommendations",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get scenarios, predictions, and organization context
        const scenarios = $input.item(0).json;
        const predictions = $input.item(1).json;
        const orgContext = $input.item(2).json;
        const executionId = scenarios.execution_id;
        
        // Generate action recommendations
        const generateActions = () => {
          // Helper function to generate strategic actions
          const generateStrategicActions = () => {
            const strategicActions = [];
            
            // Analyze scenarios for strategic implications
            const scenarioList = scenarios.scenarios || [];
            
            // Extract key trends and patterns
            const keyTrends = {};
            
            // Analyze technology perspective
            const techFactors = [];
            scenarioList.forEach(scenario => {
              if (scenario.factors) {
                const techFactorsInScenario = scenario.factors.filter(f => f.perspective === 'technology');
                techFactors.push(...techFactorsInScenario);
              }
            });
            
            // Group by factor name and calculate average state
            const techFactorGroups = {};
            techFactors.forEach(factor => {
              if (!techFactorGroups[factor.name]) {
                techFactorGroups[factor.name] = {
                  count: 0,
                  stateSum: 0,
                  probability: 0
                };
              }
              
              // Convert state to numeric value
              let stateValue;
              switch (factor.state) {
                case 'very_high':
                  stateValue = 2;
                  break;
                case 'high':
                  stateValue = 1;
                  break;
                case 'medium':
                  stateValue = 0;
                  break;
                case 'low':
                  stateValue = -1;
                  break;
                case 'very_low':
                  stateValue = -2;
                  break;
                default:
                  stateValue = 0;
              }
              
              techFactorGroups[factor.name].count++;
              techFactorGroups[factor.name].stateSum += stateValue;
              
              // Find scenario probability
              const scenarioProbability = scenarioList.find(s => s.id === factor.scenario_id)?.probability || 0;
              techFactorGroups[factor.name].probability += scenarioProbability;
            });
            
            // Calculate average state for each factor
            const techTrends = [];
            Object.keys(techFactorGroups).forEach(factorName => {
              const group = techFactorGroups[factorName];
              const avgState = group.count > 0 ? group.stateSum / group.count : 0;
              const weightedProbability = group.probability / scenarioList.length;
              
              techTrends.push({
                name: factorName,
                average_state: avgState,
                weighted_probability: weightedProbability
              });
            });
            
            // Sort by weighted probability * absolute average state
            techTrends.sort((a, b) => {
              return (b.weighted_probability * Math.abs(b.average_state)) - 
                     (a.weighted_probability * Math.abs(a.average_state));
            });
            
            // Get top technology trends
            const topTechTrends = techTrends.slice(0, 3);
            keyTrends.technology = topTechTrends;
            
            // Similar analysis for market and business perspectives
            // ... (similar code for market and business perspectives)
            
            // Generate strategic actions based on key trends
            if (keyTrends.technology) {
              keyTrends.technology.forEach(trend => {
                if (trend.average_state > 0.5) {
                  // Positive technology trend
                  strategicActions.push({
                    id: \`strategic_\${strategicActions.length + 1}\`,
                    type: 'strategic',
                    category: 'technology',
                    name: \`\${trend.name}への戦略的投資\`,
                    description: \`\${trend.name}の成長トレンドを活かすための長期的な技術投資と能力構築\`,
                    rationale: \`複数のシナリオ分析から、\${trend.name}が重要な成長領域として特定されました。加重確率は\${(trend.weighted_probability * 100).toFixed(1)}%です。\`,
                    impact: 'high',
                    time_horizon: 'long_term',
                    risk_level: 'medium'
                  });
                } else if (trend.average_state < -0.5) {
                  // Negative technology trend
                  strategicActions.push({
                    id: \`strategic_\${strategicActions.length + 1}\`,
                    type: 'strategic',
                    category: 'technology',
                    name: \`\${trend.name}からの戦略的撤退\`,
                    description: \`\${trend.name}の衰退トレンドに対応するための投資削減と代替技術の探索\`,
                    rationale: \`複数のシナリオ分析から、\${trend.name}が衰退領域として特定されました。加重確率は\${(trend.weighted_probability * 100).toFixed(1)}%です。\`,
                    impact: 'high',
                    time_horizon: 'long_term',
                    risk_level: 'medium'
                  });
                }
              });
            }
            
            // Consider organization context for strategic actions
            if (orgContext.strategic_priorities) {
              orgContext.strategic_priorities.forEach(priority => {
                // Check if priority aligns with trends
                const alignedTechTrends = keyTrends.technology ? 
                  keyTrends.technology.filter(t => t.name.toLowerCase().includes(priority.toLowerCase())) : [];
                
                if (alignedTechTrends.length > 0) {
                  strategicActions.push({
                    id: \`strategic_\${strategicActions.length + 1}\`,
                    type: 'strategic',
                    category: 'alignment',
                    name: \`\${priority}の戦略的強化\`,
                    description: \`組織の戦略的優先事項である\${priority}を強化し、予測されるトレンドと整合させる\`,
                    rationale: \`組織の戦略的優先事項と予測されるトレンドの整合性が確認されました。\`,
                    impact: 'high',
                    time_horizon: 'long_term',
                    risk_level: 'low'
                  });
                }
              });
            }
            
            return strategicActions;
          };
          
          // Helper function to generate tactical actions
          const generateTacticalActions = () => {
            const tacticalActions = [];
            
            // Analyze predictions for tactical implications
            const predictionData = predictions.predictions || {};
            
            // Extract key metrics and their forecasted values
            const keyMetrics = [];
            
            if (predictionData.technology_metrics) {
              Object.keys(predictionData.technology_metrics).forEach(metricName => {
                const metric = predictionData.technology_metrics[metricName];
                
                // Calculate trend
                const values = metric.forecasted_values || [];
                if (values.length >= 2) {
                  const currentValue = values[0].value;
                  const futureValue = values[values.length - 1].value;
                  const trend = (futureValue - currentValue) / currentValue;
                  
                  keyMetrics.push({
                    name: metricName,
                    perspective: 'technology',
                    current_value: currentValue,
                    future_value: futureValue,
                    trend: trend,
                    confidence: metric.confidence || 0.5
                  });
                }
              });
            }
            
            // Similar extraction for market and business metrics
            // ... (similar code for market and business metrics)
            
            // Sort metrics by absolute trend * confidence
            keyMetrics.sort((a, b) => {
              return (Math.abs(b.trend) * b.confidence) - (Math.abs(a.trend) * a.confidence);
            });
            
            // Get top metrics
            const topMetrics = keyMetrics.slice(0, 5);
            
            // Generate tactical actions based on top metrics
            topMetrics.forEach(metric => {
              if (metric.trend > 0.1) {
                // Positive trend
                tacticalActions.push({
                  id: \`tactical_\${tacticalActions.length + 1}\`,
                  type: 'tactical',
                  category: metric.perspective,
                  name: \`\${metric.name}の活用強化\`,
                  description: \`\${metric.name}の上昇トレンド(\${(metric.trend * 100).toFixed(1)}%)を活かすための戦術的施策の実施\`,
                  rationale: \`予測分析から、\${metric.name}が\${(metric.trend * 100).toFixed(1)}%の上昇トレンドを示しています。信頼度は\${(metric.confidence * 100).toFixed(1)}%です。\`,
                  impact: 'medium',
                  time_horizon: 'medium_term',
                  risk_level: 'low'
                });
              } else if (metric.trend < -0.1) {
                // Negative trend
                tacticalActions.push({
                  id: \`tactical_\${tacticalActions.length + 1}\`,
                  type: 'tactical',
                  category: metric.perspective,
                  name: \`\${metric.name}の対応策実施\`,
                  description: \`\${metric.name}の下降トレンド(\${(Math.abs(metric.trend) * 100).toFixed(1)}%)に対応するための戦術的施策の実施\`,
                  rationale: \`予測分析から、\${metric.name}が\${(Math.abs(metric.trend) * 100).toFixed(1)}%の下降トレンドを示しています。信頼度は\${(metric.confidence * 100).toFixed(1)}%です。\`,
                  impact: 'medium',
                  time_horizon: 'medium_term',
                  risk_level: 'medium'
                });
              }
            });
            
            // Consider organization capabilities for tactical actions
            if (orgContext.capabilities) {
              // Match capabilities with metrics
              topMetrics.forEach(metric => {
                const relatedCapabilities = orgContext.capabilities.filter(cap => 
                  cap.name.toLowerCase().includes(metric.name.toLowerCase()) ||
                  metric.name.toLowerCase().includes(cap.name.toLowerCase())
                );
                
                relatedCapabilities.forEach(capability => {
                  if (metric.trend > 0 && capability.maturity < 0.7) {
                    // Need to improve capability for positive trend
                    tacticalActions.push({
                      id: \`tactical_\${tacticalActions.length + 1}\`,
                      type: 'tactical',
                      category: 'capability',
                      name: \`\${capability.name}能力の強化\`,
                      description: \`\${metric.name}の上昇トレンドを活かすために必要な\${capability.name}能力の強化\`,
                      rationale: \`組織の\${capability.name}能力の成熟度(\${(capability.maturity * 100).toFixed(1)}%)が、\${metric.name}の上昇トレンドを活かすには不十分です。\`,
                      impact: 'medium',
                      time_horizon: 'medium_term',
                      risk_level: 'medium'
                    });
                  }
                });
              });
            }
            
            return tacticalActions;
          };
          
          // Helper function to generate operational actions
          const generateOperationalActions = () => {
            const operationalActions = [];
            
            // Analyze short-term predictions for operational implications
            const predictionData = predictions.predictions || {};
            
            // Extract short-term metrics
            const shortTermMetrics = [];
            
            if (predictionData.technology_metrics) {
              Object.keys(predictionData.technology_metrics).forEach(metricName => {
                const metric = predictionData.technology_metrics[metricName];
                
                // Get short-term values (next 3 months)
                const values = metric.forecasted_values || [];
                if (values.length >= 2) {
                  const shortTermValues = values.slice(0, 3);
                  const currentValue = shortTermValues[0].value;
                  const shortTermValue = shortTermValues[shortTermValues.length - 1].value;
                  const shortTermTrend = (shortTermValue - currentValue) / currentValue;
                  
                  shortTermMetrics.push({
                    name: metricName,
                    perspective: 'technology',
                    current_value: currentValue,
                    short_term_value: shortTermValue,
                    short_term_trend: shortTermTrend,
                    confidence: metric.confidence || 0.5
                  });
                }
              });
            }
            
            // Similar extraction for market and business metrics
            // ... (similar code for market and business metrics)
            
            // Sort metrics by absolute short-term trend * confidence
            shortTermMetrics.sort((a, b) => {
              return (Math.abs(b.short_term_trend) * b.confidence) - (Math.abs(a.short_term_trend) * a.confidence);
            });
            
            // Get top short-term metrics
            const topShortTermMetrics = shortTermMetrics.slice(0, 5);
            
            // Generate operational actions based on top short-term metrics
            topShortTermMetrics.forEach(metric => {
              if (metric.short_term_trend > 0.05) {
                // Positive short-term trend
                operationalActions.push({
                  id: \`operational_\${operationalActions.length + 1}\`,
                  type: 'operational',
                  category: metric.perspective,
                  name: \`\${metric.name}の短期的活用\`,
                  description: \`\${metric.name}の短期的上昇トレンド(\${(metric.short_term_trend * 100).toFixed(1)}%)を活かすための運用施策の実施\`,
                  rationale: \`短期予測から、\${metric.name}が\${(metric.short_term_trend * 100).toFixed(1)}%の上昇トレンドを示しています。信頼度は\${(metric.confidence * 100).toFixed(1)}%です。\`,
                  impact: 'low',
                  time_horizon: 'short_term',
                  risk_level: 'low'
                });
              } else if (metric.short_term_trend < -0.05) {
                // Negative short-term trend
                operationalActions.push({
                  id: \`operational_\${operationalActions.length + 1}\`,
                  type: 'operational',
                  category: metric.perspective,
                  name: \`\${metric.name}の短期的対応\`,
                  description: \`\${metric.name}の短期的下降トレンド(\${(Math.abs(metric.short_term_trend) * 100).toFixed(1)}%)に対応するための運用施策の実施\`,
                  rationale: \`短期予測から、\${metric.name}が\${(Math.abs(metric.short_term_trend) * 100).toFixed(1)}%の下降トレンドを示しています。信頼度は\${(metric.confidence * 100).toFixed(1)}%です。\`,
                  impact: 'low',
                  time_horizon: 'short_term',
                  risk_level: 'medium'
                });
              }
            });
            
            // Consider organization resources for operational actions
            if (orgContext.resources) {
              // Match resources with metrics
              topShortTermMetrics.forEach(metric => {
                const relatedResources = orgContext.resources.filter(res => 
                  res.name.toLowerCase().includes(metric.name.toLowerCase()) ||
                  metric.name.toLowerCase().includes(res.name.toLowerCase())
                );
                
                relatedResources.forEach(resource => {
                  if (metric.short_term_trend > 0 && resource.availability < 0.3) {
                    // Need to allocate more resources for positive trend
                    operationalActions.push({
                      id: \`operational_\${operationalActions.length + 1}\`,
                      type: 'operational',
                      category: 'resource',
                      name: \`\${resource.name}リソースの増強\`,
                      description: \`\${metric.name}の短期的上昇トレンドを活かすために必要な\${resource.name}リソースの増強\`,
                      rationale: \`組織の\${resource.name}リソースの可用性(\${(resource.availability * 100).toFixed(1)}%)が、\${metric.name}の短期的上昇トレンドを活かすには不十分です。\`,
                      impact: 'low',
                      time_horizon: 'short_term',
                      risk_level: 'low'
                    });
                  }
                });
              });
            }
            
            return operationalActions;
          };
          
          // Generate all types of actions
          const strategicActions = generateStrategicActions();
          const tacticalActions = generateTacticalActions();
          const operationalActions = generateOperationalActions();
          
          // Combine all actions
          const allActions = [
            ...strategicActions,
            ...tacticalActions,
            ...operationalActions
          ];
          
          return allActions;
        };
        
        const actionRecommendations = generateActions();
        
        return {
          json: {
            execution_id: executionId,
            action_recommendations: actionRecommendations,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveActionRecommendations",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "action_recommendations",
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

## アクション推奨の優先順位付け

生成された複数のアクション推奨に優先順位を付ける方法について解説します。n8nを使用したアクション推奨の優先順位付けの実装例を示します。

```javascript
// n8n workflow: Action Recommendation Prioritization
// Function node for prioritizing action recommendations
[
  {
    "id": "loadActionRecommendations",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "action_recommendations",
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
    "id": "loadOrganizationContext",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "organization_context",
      "filter": {
        "organization_id": "={{ $node[\"loadOrganizationId\"].json.organization_id }}"
      }
    }
  },
  {
    "id": "prioritizeActions",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get action recommendations and organization context
        const actionRecs = $input.item(0).json;
        const orgContext = $input.item(1).json;
        const executionId = actionRecs.execution_id;
        const actions = actionRecs.action_recommendations || [];
        
        // Prioritize actions
        const prioritizeActions = () => {
          // Calculate base score for each action
          const actionsWithScore = actions.map(action => {
            // Base score calculation
            let baseScore = 0;
            
            // Score based on impact
            switch (action.impact) {
              case 'high':
                baseScore += 5;
                break;
              case 'medium':
                baseScore += 3;
                break;
              case 'low':
                baseScore += 1;
                break;
            }
            
            // Score based on time horizon (higher for shorter time horizon)
            switch (action.time_horizon) {
              case 'short_term':
                baseScore += 3;
                break;
              case 'medium_term':
                baseScore += 2;
                break;
              case 'long_term':
                baseScore += 1;
                break;
            }
            
            // Score based on risk level (higher for lower risk)
            switch (action.risk_level) {
              case 'low':
                baseScore += 3;
                break;
              case 'medium':
                baseScore += 2;
                break;
              case 'high':
                baseScore += 1;
                break;
            }
            
            return {
              ...action,
              base_score: baseScore
            };
          });
          
          // Apply organization context to adjust scores
          const actionsWithAdjustedScore = actionsWithScore.map(action => {
            let adjustedScore = action.base_score;
            
            // Adjust based on strategic priorities
            if (orgContext.strategic_priorities) {
              orgContext.strategic_priorities.forEach(priority => {
                if (action.name.toLowerCase().includes(priority.toLowerCase()) ||
                    action.description.toLowerCase().includes(priority.toLowerCase())) {
                  adjustedScore *= 1.5; // 50% boost for alignment with strategic priorities
                }
              });
            }
            
            // Adjust based on capabilities
            if (orgContext.capabilities) {
              const relatedCapabilities = orgContext.capabilities.filter(cap => 
                action.name.toLowerCase().includes(cap.name.toLowerCase()) ||
                action.description.toLowerCase().includes(cap.name.toLowerCase())
              );
              
              if (relatedCapabilities.length > 0) {
                // Average maturity of related capabilities
                const avgMaturity = relatedCapabilities.reduce((sum, cap) => sum + cap.maturity, 0) / relatedCapabilities.length;
                
                // Higher maturity means better ability to execute
                adjustedScore *= (0.5 + avgMaturity); // Scale from 0.5x to 1.5x based on maturity
              }
            }
            
            // Adjust based on resources
            if (orgContext.resources) {
              const relatedResources = orgContext.resources.filter(res => 
                action.name.toLowerCase().includes(res.name.toLowerCase()) ||
                action.description.toLowerCase().includes(res.name.toLowerCase())
              );
              
              if (relatedResources.length > 0) {
                // Average availability of related resources
                const avgAvailability = relatedResources.reduce((sum, res) => sum + res.availability, 0) / relatedResources.length;
                
                // Higher availability means better ability to execute
                adjustedScore *= (0.5 + avgAvailability); // Scale from 0.5x to 1.5x based on availability
              }
            }
            
            return {
              ...action,
              base_score: action.base_score,
              adjusted_score: adjustedScore
            };
          });
          
          // Sort by adjusted score (descending)
          actionsWithAdjustedScore.sort((a, b) => b.adjusted_score - a.adjusted_score);
          
          // Assign priority rank
          const prioritizedActions = actionsWithAdjustedScore.map((action, index) => ({
            ...action,
            priority_rank: index + 1
          }));
          
          return prioritizedActions;
        };
        
        const prioritizedActions = prioritizeActions();
        
        return {
          json: {
            execution_id: executionId,
            prioritized_actions: prioritizedActions,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "savePrioritizedActions",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "prioritized_actions",
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

## アクション推奨の可視化

生成されたアクション推奨を効果的に可視化する方法について解説します。n8nを使用したアクション推奨の可視化の実装例を示します。

```javascript
// n8n workflow: Action Recommendation Visualization
// Function node for visualizing action recommendations
[
  {
    "id": "loadPrioritizedActions",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "prioritized_actions",
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
    "id": "generateVisualizationData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get prioritized actions
        const prioritizedActions = $input.item.json;
        const actions = prioritizedActions.prioritized_actions || [];
        const executionId = prioritizedActions.execution_id;
        
        // Generate visualization data
        const generateVisualizationData = () => {
          // Action summary by type
          const actionsByType = {
            strategic: actions.filter(a => a.type === 'strategic'),
            tactical: actions.filter(a => a.type === 'tactical'),
            operational: actions.filter(a => a.type === 'operational')
          };
          
          // Action summary by category
          const categoryCounts = {};
          actions.forEach(action => {
            if (!categoryCounts[action.category]) {
              categoryCounts[action.category] = 0;
            }
            categoryCounts[action.category]++;
          });
          
          const actionsByCategory = Object.keys(categoryCounts).map(category => ({
            category: category,
            count: categoryCounts[category]
          }));
          
          // Sort by count (descending)
          actionsByCategory.sort((a, b) => b.count - a.count);
          
          // Top 10 prioritized actions
          const top10Actions = actions.slice(0, 10);
          
          // Impact-effort matrix data
          const impactEffortMatrix = {
            high_impact_low_effort: [],
            high_impact_high_effort: [],
            low_impact_low_effort: [],
            low_impact_high_effort: []
          };
          
          actions.forEach(action => {
            // Determine impact (high/low)
            const highImpact = action.impact === 'high' || 
                              (action.impact === 'medium' && action.adjusted_score > 5);
            
            // Determine effort (high/low) based on risk level and time horizon
            const highEffort = action.risk_level === 'high' || 
                              action.time_horizon === 'long_term' ||
                              (action.risk_level === 'medium' && action.time_horizon === 'medium_term');
            
            // Assign to appropriate quadrant
            if (highImpact && !highEffort) {
              impactEffortMatrix.high_impact_low_effort.push(action);
            } else if (highImpact && highEffort) {
              impactEffortMatrix.high_impact_high_effort.push(action);
            } else if (!highImpact && !highEffort) {
              impactEffortMatrix.low_impact_low_effort.push(action);
            } else {
              impactEffortMatrix.low_impact_high_effort.push(action);
            }
          });
          
          return {
            actions_by_type: actionsByType,
            actions_by_category: actionsByCategory,
            top_10_actions: top10Actions,
            impact_effort_matrix: impactEffortMatrix
          };
        };
        
        const visualizationData = generateVisualizationData();
        
        return {
          json: {
            execution_id: executionId,
            visualization_data: visualizationData,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "generateVisualizationHTML",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get visualization data
        const visualizationData = $input.item.json.visualization_data;
        const executionId = $input.item.json.execution_id;
        
        // Generate HTML visualization
        const generateHTML = () => {
          // Helper function to get impact color
          const getImpactColor = (impact) => {
            switch (impact) {
              case 'high':
                return '#2e7d32'; // Dark green
              case 'medium':
                return '#f9a825'; // Amber
              case 'low':
                return '#e65100'; // Orange
              default:
                return '#757575'; // Grey
            }
          };
          
          // Helper function to get time horizon label
          const getTimeHorizonLabel = (timeHorizon) => {
            switch (timeHorizon) {
              case 'short_term':
                return '短期';
              case 'medium_term':
                return '中期';
              case 'long_term':
                return '長期';
              default:
                return '不明';
            }
          };
          
          // Generate top 10 actions table
          const generateTop10Table = () => {
            const rows = visualizationData.top_10_actions.map(action => {
              const impactColor = getImpactColor(action.impact);
              const timeHorizonLabel = getTimeHorizonLabel(action.time_horizon);
              
              return \`
                <tr>
                  <td>\${action.priority_rank}</td>
                  <td>\${action.name}</td>
                  <td>\${action.type === 'strategic' ? '戦略的' : action.type === 'tactical' ? '戦術的' : '運用的'}</td>
                  <td style="color: \${impactColor}; font-weight: bold;">\${action.impact === 'high' ? '高' : action.impact === 'medium' ? '中' : '低'}</td>
                  <td>\${timeHorizonLabel}</td>
                  <td>\${action.adjusted_score.toFixed(2)}</td>
                </tr>
              \`;
            }).join('');
            
            return \`
              <table class="action-table">
                <thead>
                  <tr>
                    <th>優先順位</th>
                    <th>アクション</th>
                    <th>タイプ</th>
                    <th>影響度</th>
                    <th>時間軸</th>
                    <th>スコア</th>
                  </tr>
                </thead>
                <tbody>
                  \${rows}
                </tbody>
              </table>
            \`;
          };
          
          // Generate actions by type chart data
          const generateActionsByTypeChartData = () => {
            const data = {
              strategic: visualizationData.actions_by_type.strategic.length,
              tactical: visualizationData.actions_by_type.tactical.length,
              operational: visualizationData.actions_by_type.operational.length
            };
            
            return JSON.stringify(data);
          };
          
          // Generate actions by category chart data
          const generateActionsByCategoryChartData = () => {
            const data = visualizationData.actions_by_category.map(item => ({
              category: item.category,
              count: item.count
            }));
            
            return JSON.stringify(data);
          };
          
          // Generate impact-effort matrix
          const generateImpactEffortMatrix = () => {
            // Helper function to generate action list for a quadrant
            const generateQuadrantList = (actions) => {
              if (actions.length === 0) {
                return '<p>該当するアクションはありません。</p>';
              }
              
              return \`
                <ul class="action-list">
                  \${actions.map(action => \`
                    <li>
                      <strong>\${action.name}</strong> (優先順位: \${action.priority_rank})
                      <br>
                      <small>\${action.description}</small>
                    </li>
                  \`).join('')}
                </ul>
              \`;
            };
            
            return \`
              <div class="impact-effort-matrix">
                <div class="matrix-row">
                  <div class="matrix-cell high-impact-high-effort">
                    <h4>高影響・高労力</h4>
                    \${generateQuadrantList(visualizationData.impact_effort_matrix.high_impact_high_effort)}
                  </div>
                  <div class="matrix-cell high-impact-low-effort">
                    <h4>高影響・低労力</h4>
                    \${generateQuadrantList(visualizationData.impact_effort_matrix.high_impact_low_effort)}
                  </div>
                </div>
                <div class="matrix-row">
                  <div class="matrix-cell low-impact-high-effort">
                    <h4>低影響・高労力</h4>
                    \${generateQuadrantList(visualizationData.impact_effort_matrix.low_impact_high_effort)}
                  </div>
                  <div class="matrix-cell low-impact-low-effort">
                    <h4>低影響・低労力</h4>
                    \${generateQuadrantList(visualizationData.impact_effort_matrix.low_impact_low_effort)}
                  </div>
                </div>
              </div>
            \`;
          };
          
          // Complete HTML
          return \`
            <!DOCTYPE html>
            <html>
            <head>
              <title>アクション推奨可視化</title>
              <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2, h3, h4 { color: #333; }
                .section { margin-bottom: 30px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f5f5f5; }
                .chart-container { height: 300px; margin-bottom: 20px; }
                .impact-effort-matrix { display: flex; flex-direction: column; }
                .matrix-row { display: flex; }
                .matrix-cell { flex: 1; padding: 15px; margin: 5px; border: 1px solid #ddd; }
                .high-impact-high-effort { background-color: #ffecb3; }
                .high-impact-low-effort { background-color: #c8e6c9; }
                .low-impact-high-effort { background-color: #ffccbc; }
                .low-impact-low-effort { background-color: #e1f5fe; }
                .action-list { padding-left: 20px; }
                .action-list li { margin-bottom: 10px; }
              </style>
              <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
              <h1>アクション推奨可視化</h1>
              
              <div class="section">
                <h2>トップ10アクション</h2>
                \${generateTop10Table()}
              </div>
              
              <div class="section">
                <h2>アクションタイプ分布</h2>
                <div class="chart-container">
                  <canvas id="actionTypeChart"></canvas>
                </div>
              </div>
              
              <div class="section">
                <h2>アクションカテゴリ分布</h2>
                <div class="chart-container">
                  <canvas id="actionCategoryChart"></canvas>
                </div>
              </div>
              
              <div class="section">
                <h2>影響度-労力マトリクス</h2>
                \${generateImpactEffortMatrix()}
              </div>
              
              <script>
                // Action Type Chart
                const actionTypeData = \${generateActionsByTypeChartData()};
                
                const typeCtx = document.getElementById('actionTypeChart').getContext('2d');
                new Chart(typeCtx, {
                  type: 'pie',
                  data: {
                    labels: ['戦略的', '戦術的', '運用的'],
                    datasets: [{
                      data: [actionTypeData.strategic, actionTypeData.tactical, actionTypeData.operational],
                      backgroundColor: ['#4caf50', '#2196f3', '#ff9800']
                    }]
                  },
                  options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'right'
                      }
                    }
                  }
                });
                
                // Action Category Chart
                const actionCategoryData = \${generateActionsByCategoryChartData()};
                
                const categoryCtx = document.getElementById('actionCategoryChart').getContext('2d');
                new Chart(categoryCtx, {
                  type: 'bar',
                  data: {
                    labels: actionCategoryData.map(item => item.category),
                    datasets: [{
                      label: 'アクション数',
                      data: actionCategoryData.map(item => item.count),
                      backgroundColor: '#2196f3'
                    }]
                  },
                  options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true,
                        ticks: {
                          precision: 0
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
        
        const visualizationHTML = generateHTML();
        
        return {
          json: {
            execution_id: executionId,
            visualization_html: visualizationHTML,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveVisualizationHTML",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "action_visualizations",
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
      "fileName": "={{ 'action_visualization_' + $json.execution_id + '.html' }}",
      "fileContent": "={{ $json.visualization_html }}",
      "directory": "/tmp"
    }
  }
]
```

## アクション推奨のベストプラクティス

トリプルパースペクティブ型戦略AIレーダーを活用したアクション推奨を効果的に行うためのベストプラクティスを以下に示します。

### 1. コンテキスト適応型の推奨

アクション推奨は、組織の特定のコンテキストに適応させることが重要です：

- 組織の戦略目標と優先事項を考慮
- 組織の能力と制約を現実的に評価
- 組織文化と意思決定プロセスに合わせた推奨スタイル
- 業界特有の動向と規制環境を考慮

### 2. バランスの取れた推奨ポートフォリオ

単一のアクションではなく、バランスの取れたアクションのポートフォリオを推奨することが重要です：

- 短期・中期・長期のアクションのバランス
- 低リスク・高リスクのアクションのバランス
- 防御的・攻撃的なアクションのバランス
- 3つの視点（テクノロジー、マーケット、ビジネス）のバランス

### 3. 実行可能性の重視

推奨されるアクションは、実際に実行可能であることが重要です：

- 必要なリソースと能力の現実的な評価
- 具体的で明確なアクションの定義
- 段階的な実装計画の提案
- 実行の障壁と対策の特定

### 4. 継続的な更新と学習

アクション推奨は、新たな情報と結果に基づいて継続的に更新することが重要です：

- 実行結果のフィードバックの収集と反映
- 予測とシナリオの更新に基づく推奨の見直し
- 成功事例と失敗事例からの学習
- 推奨プロセスの継続的な改善

### 5. 透明性と説明可能性

アクション推奨の根拠と論理を明確に説明することが重要です：

- 推奨の根拠となるデータと分析の明示
- 期待される結果とリスクの明確な説明
- 代替アクションとトレードオフの提示
- 不確実性と信頼区間の明示的な表現

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおけるアクション推奨の生成方法について詳細に解説しました。アクション推奨の基本概念、アクション生成エンジンの実装、アクション推奨の優先順位付け、アクション推奨の可視化、そしてアクション推奨のベストプラクティスについて説明しました。これらの方法を活用することで、予測とシナリオに基づいた具体的なアクション推奨を生成し、意思決定者を効果的に支援することができます。

次のセクションでは、予測結果の実践的な活用例について詳細に解説します。
