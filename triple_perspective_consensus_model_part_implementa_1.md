# コンセンサスモデルの実装（パート5：n8nによる全体オーケストレーション）

## コンセンサスモデルの全体アーキテクチャ

トリプルパースペクティブ型戦略AIレーダーのコンセンサスモデルは、複数のコンポーネントが連携して動作する複雑なシステムです。このセクションでは、n8nを活用したコンセンサスモデルの全体オーケストレーションについて解説します。

### システム全体の構成

コンセンサスモデルのシステム全体は、以下のコンポーネントで構成されます：

1. **データ収集コンポーネント**
   - 各視点（テクノロジー、マーケット、ビジネス）のデータソースからデータを収集
   - データの前処理と構造化

2. **分析コンポーネント**
   - 各視点でのデータ分析
   - 変化点検出
   - 重要度・確信度の初期評価

3. **評価コンポーネント**
   - 視点別の重要度・確信度評価
   - 視点間の整合性評価

4. **統合コンポーネント**
   - 視点統合
   - 静止点検出
   - 代替解生成

5. **出力コンポーネント**
   - インサイト生成
   - アクション推奨
   - 可視化

6. **管理コンポーネント**
   - パラメータ管理
   - ルール管理
   - モデル評価と最適化

### コンポーネント間の連携

コンポーネント間の連携は、n8nのワークフロー間の連携によって実現されます。主な連携フローは以下の通りです：

1. **データ収集 → 分析**
   - 収集されたデータが分析コンポーネントに渡される
   - 各視点で独立に分析が実行される

2. **分析 → 評価**
   - 分析結果が評価コンポーネントに渡される
   - 各視点で重要度・確信度が評価される
   - 視点間の整合性が評価される

3. **評価 → 統合**
   - 評価結果が統合コンポーネントに渡される
   - 視点統合と静止点検出が実行される
   - 必要に応じて代替解が生成される

4. **統合 → 出力**
   - 統合結果が出力コンポーネントに渡される
   - インサイトとアクション推奨が生成される
   - 結果が可視化される

5. **全コンポーネント ↔ 管理**
   - 管理コンポーネントがすべてのコンポーネントのパラメータとルールを管理
   - 各コンポーネントの実行結果が管理コンポーネントに報告される
   - 管理コンポーネントがモデルの評価と最適化を行う

## n8nによる全体オーケストレーション

n8nを活用して、コンセンサスモデルの全体オーケストレーションを実装します。以下では、主要なワークフローとその連携方法を示します。

### マスターオーケストレーションワークフロー

マスターオーケストレーションワークフローは、全体のプロセスを制御し、各コンポーネント間の連携を管理します。

```javascript
// n8n workflow: Master Orchestration
// Trigger: Schedule (Daily)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.cron",
    "parameters": {
      "triggerTimes": {
        "item": [
          {
            "mode": "everyDay",
            "hour": 1,
            "minute": 0
          }
        ]
      }
    }
  },
  {
    "id": "getActiveTopics",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get active topics for analysis
        SELECT
          id,
          name,
          description,
          keywords,
          perspective_id AS primary_perspective,
          is_active
        FROM
          topics
        WHERE
          is_active = TRUE
      `
    }
  },
  {
    "id": "loopTopics",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1
    }
  },
  {
    "id": "getCurrentDate",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get current date in YYYY-MM-DD format
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const currentDate = \`\${year}-\${month}-\${day}\`;
        
        return {
          json: {
            ...item,
            current_date: currentDate
          }
        };
      `
    }
  },
  {
    "id": "triggerDataCollection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/collect-data",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.id }}"
          },
          {
            "name": "topic_name",
            "value": "={{ $json.name }}"
          },
          {
            "name": "date",
            "value": "={{ $json.current_date }}"
          }
        ]
      },
      "options": {
        "response": {
          "response": {
            "fullResponse": true
          }
        }
      }
    }
  },
  {
    "id": "waitForDataCollection",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Wait for data collection to complete (in a real system, this would be more sophisticated)
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({json: $input.item.json});
          }, 5000);
        });
      `
    }
  },
  {
    "id": "triggerPerspectiveAnalysis",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/analyze-perspectives",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.current_date }}"
          }
        ]
      },
      "options": {
        "response": {
          "response": {
            "fullResponse": true
          }
        }
      }
    }
  },
  {
    "id": "waitForPerspectiveAnalysis",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Wait for perspective analysis to complete
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({json: $input.item.json});
          }, 10000);
        });
      `
    }
  },
  {
    "id": "checkPerspectiveEvaluations",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Check if all perspective evaluations are complete
        SELECT
          COUNT(*) AS completed_count
        FROM
          perspective_evaluations
        WHERE
          topic_id = '{{ $json.id }}'
          AND date = '{{ $json.current_date }}'
      `
    }
  },
  {
    "id": "checkIfAllPerspectivesEvaluated",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": [
        {
          "value1": "={{ $json.completed_count }}",
          "operation": "equal",
          "value2": 3
        }
      ]
    }
  },
  {
    "id": "triggerCoherenceEvaluation",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/check-coherence",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.current_date }}"
          }
        ]
      },
      "options": {
        "response": {
          "response": {
            "fullResponse": true
          }
        }
      }
    }
  },
  {
    "id": "waitForCoherenceEvaluation",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Wait for coherence evaluation to complete
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({json: $input.item.json});
          }, 5000);
        });
      `
    }
  },
  {
    "id": "triggerEquilibriumDetection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/detect-equilibrium",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.current_date }}"
          }
        ]
      },
      "options": {
        "response": {
          "response": {
            "fullResponse": true
          }
        }
      }
    }
  },
  {
    "id": "waitForEquilibriumDetection",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Wait for equilibrium detection to complete
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({json: $input.item.json});
          }, 5000);
        });
      `
    }
  },
  {
    "id": "triggerActionRecommendation",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/generate-actions",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.current_date }}"
          }
        ]
      },
      "options": {
        "response": {
          "response": {
            "fullResponse": true
          }
        }
      }
    }
  },
  {
    "id": "waitForActionRecommendation",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Wait for action recommendation to complete
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({json: $input.item.json});
          }, 5000);
        });
      `
    }
  },
  {
    "id": "triggerResultVisualization",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/visualize-results",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.current_date }}"
          }
        ]
      },
      "options": {
        "response": {
          "response": {
            "fullResponse": true
          }
        }
      }
    }
  },
  {
    "id": "logCompletionStatus",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Log completion status
        INSERT INTO analysis_logs (
          topic_id,
          date,
          status,
          message
        )
        VALUES (
          '{{ $json.id }}',
          '{{ $json.current_date }}',
          'completed',
          'Analysis completed successfully'
        );
      `
    }
  },
  {
    "id": "notifyCompletion",
    "type": "n8n-nodes-base.slack",
    "parameters": {
      "text": "トピック「{{ $json.name }}」の分析が完了しました。日付: {{ $json.current_date }}",
      "channel": "#ai-radar-alerts",
      "otherOptions": {
        "attachments": [
          {
            "title": "分析結果を確認",
            "title_link": "http://dashboard.example.com/topics/{{ $json.id }}/date/{{ $json.current_date }}"
          }
        ]
      }
    }
  }
]
```

このマスターオーケストレーションワークフローは、以下のステップで全体のプロセスを制御します：

1. アクティブなトピックを取得
2. 各トピックに対して：
   a. データ収集をトリガー
   b. 視点分析をトリガー
   c. すべての視点の評価が完了したことを確認
   d. 整合性評価をトリガー
   e. 静止点検出をトリガー
   f. アクション推奨生成をトリガー
   g. 結果可視化をトリガー
3. 完了ステータスをログに記録
4. 完了通知を送信

### アクション推奨生成ワークフロー

アクション推奨生成ワークフローは、静止点検出の結果に基づいて、具体的なアクション推奨を生成します。

```javascript
// n8n workflow: Action Recommendation Generation
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "generate-actions",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getEquilibriumData",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get equilibrium detection results
        SELECT
          er.topic_id,
          er.date,
          er.integrated_score,
          er.adjusted_score,
          er.is_equilibrium,
          er.equilibrium_score,
          er.contributing_factors,
          t.name AS topic_name,
          t.description AS topic_description,
          (
            SELECT jsonb_agg(
              jsonb_build_object(
                'perspective_id', pe.perspective_id,
                'importance', pe.importance,
                'confidence', pe.confidence,
                'overall_score', pe.overall_score
              )
            )
            FROM perspective_evaluations pe
            WHERE pe.topic_id = er.topic_id AND pe.date = er.date
          ) AS perspective_evaluations,
          (
            SELECT solutions
            FROM alternative_solutions als
            WHERE als.topic_id = er.topic_id AND als.date = er.date
          ) AS alternative_solutions
        FROM
          equilibrium_results er
        JOIN
          topics t ON er.topic_id = t.id
        WHERE
          er.topic_id = '{{ $json.topic_id }}'
          AND er.date = '{{ $json.date }}'
      `
    }
  },
  {
    "id": "generateActions",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const equilibriumData = $input.item.json;
        
        // Generate actions based on equilibrium status
        const actions = [];
        
        if (equilibriumData.is_equilibrium) {
          // Generate actions for equilibrium point
          actions.push(...generateEquilibriumActions(equilibriumData));
        } else {
          // Generate actions for non-equilibrium point
          actions.push(...generateNonEquilibriumActions(equilibriumData));
        }
        
        // Sort actions by priority
        actions.sort((a, b) => b.priority - a.priority);
        
        return {
          json: {
            topic_id: equilibriumData.topic_id,
            topic_name: equilibriumData.topic_name,
            date: equilibriumData.date,
            is_equilibrium: equilibriumData.is_equilibrium,
            actions: actions
          }
        };
        
        // Helper function: Generate actions for equilibrium point
        function generateEquilibriumActions(data) {
          const actions = [];
          
          // Extract perspective evaluations
          const perspectives = {};
          for (const eval of data.perspective_evaluations) {
            perspectives[eval.perspective_id] = eval;
          }
          
          // Generate action based on high importance and confidence
          if (data.equilibrium_score > 0.7) {
            actions.push({
              action_type: 'strategic_initiative',
              action_description: \`トピック「\${data.topic_name}」に関する戦略的イニシアチブを開始する\`,
              priority: 0.9,
              recommended_timing: 'immediate',
              expected_impact: '高い戦略的優位性の獲得'
            });
          }
          
          // Generate technology-related action
          if (perspectives.technology && perspectives.technology.importance.score > 0.7) {
            actions.push({
              action_type: 'technology_investment',
              action_description: \`関連技術への投資を増加させる\`,
              priority: 0.8,
              recommended_timing: 'short_term',
              expected_impact: '技術的優位性の確立'
            });
          }
          
          // Generate market-related action
          if (perspectives.market && perspectives.market.importance.score > 0.7) {
            actions.push({
              action_type: 'market_expansion',
              action_description: \`市場展開を加速する\`,
              priority: 0.85,
              recommended_timing: 'short_term',
              expected_impact: '市場シェアの拡大'
            });
          }
          
          // Generate business-related action
          if (perspectives.business && perspectives.business.importance.score > 0.7) {
            actions.push({
              action_type: 'business_model_optimization',
              action_description: \`ビジネスモデルを最適化する\`,
              priority: 0.75,
              recommended_timing: 'medium_term',
              expected_impact: '収益性の向上'
            });
          }
          
          // Generate monitoring action
          actions.push({
            action_type: 'continuous_monitoring',
            action_description: \`トピック「\${data.topic_name}」の動向を継続的にモニタリングする\`,
            priority: 0.7,
            recommended_timing: 'ongoing',
            expected_impact: '変化の早期検出'
          });
          
          return actions;
        }
        
        // Helper function: Generate actions for non-equilibrium point
        function generateNonEquilibriumActions(data) {
          const actions = [];
          
          // Extract perspective evaluations
          const perspectives = {};
          for (const eval of data.perspective_evaluations) {
            perspectives[eval.perspective_id] = eval;
          }
          
          // Generate action for additional research
          actions.push({
            action_type: 'additional_research',
            action_description: \`トピック「\${data.topic_name}」に関する追加調査を実施する\`,
            priority: 0.8,
            recommended_timing: 'immediate',
            expected_impact: '情報の質と量の向上'
          });
          
          // Generate action based on alternative solutions
          if (data.alternative_solutions && data.alternative_solutions.length > 0) {
            const bestAlternative = data.alternative_solutions[0];
            
            actions.push({
              action_type: 'alternative_approach',
              action_description: \`代替アプローチ「\${bestAlternative.name}」を検討する\`,
              priority: 0.75,
              recommended_timing: 'short_term',
              expected_impact: '代替視点からの価値創出'
            });
          }
          
          // Generate action for perspective with lowest confidence
          let lowestConfidencePerspective = null;
          let lowestConfidence = 1.0;
          
          for (const perspectiveId in perspectives) {
            const perspective = perspectives[perspectiveId];
            if (perspective.confidence.score < lowestConfidence) {
              lowestConfidence = perspective.confidence.score;
              lowestConfidencePerspective = perspectiveId;
            }
          }
          
          if (lowestConfidencePerspective) {
            const perspectiveNames = {
              technology: 'テクノロジー',
              market: 'マーケット',
              business: 'ビジネス'
            };
            
            actions.push({
              action_type: 'improve_confidence',
              action_description: \`\${perspectiveNames[lowestConfidencePerspective]}視点の確信度を向上させるための情報収集を強化する\`,
              priority: 0.7,
              recommended_timing: 'immediate',
              expected_impact: '判断の確信度向上'
            });
          }
          
          // Generate monitoring action
          actions.push({
            action_type: 'continuous_monitoring',
            action_description: \`トピック「\${data.topic_name}」の動向を継続的にモニタリングする\`,
            priority: 0.65,
            recommended_timing: 'ongoing',
            expected_impact: '変化の早期検出'
          });
          
          return actions;
        }
      `
    }
  },
  {
    "id": "saveActions",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get consensus result ID
        WITH consensus_id AS (
          SELECT id
          FROM consensus_results
          WHERE topic_id = '{{ $json.topic_id }}' AND date = '{{ $json.date }}'
        )
        
        -- Delete existing actions
        DELETE FROM consensus_actions
        WHERE consensus_result_id IN (SELECT id FROM consensus_id);
        
        {% for action in $json.actions %}
        -- Insert new actions
        INSERT INTO consensus_actions (
          consensus_result_id,
          action_type,
          action_description,
          priority,
          recommended_timing,
          expected_impact
        )
        SELECT
          id,
          '{{ action.action_type }}',
          '{{ action.action_description }}',
          {{ action.priority }},
          '{{ action.recommended_timing }}',
          '{{ action.expected_impact }}'
        FROM consensus_id;
        {% endfor %}
      `
    }
  }
]
```

このワークフローでは、静止点検出の結果に基づいて、具体的なアクション推奨を生成しています。静止点が検出された場合と検出されなかった場合で、異なるアクション推奨が生成されます。

### 結果可視化ワークフロー

結果可視化ワークフローは、コンセンサスモデルの結果を可視化し、ダッシュボードに表示します。

```javascript
// n8n workflow: Result Visualization
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "visualize-results",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getResultData",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get all result data for visualization
        WITH perspective_data AS (
          SELECT
            pe.topic_id,
            pe.date,
            pe.perspective_id,
            pe.importance,
            pe.confidence,
            pe.overall_score
          FROM
            perspective_evaluations pe
          WHERE
            pe.topic_id = '{{ $json.topic_id }}'
            AND pe.date = '{{ $json.date }}'
        ),
        coherence_data AS (
          SELECT
            ce.topic_id,
            ce.date,
            ce.coherence
          FROM
            coherence_evaluations ce
          WHERE
            ce.topic_id = '{{ $json.topic_id }}'
            AND ce.date = '{{ $json.date }}'
        ),
        equilibrium_data AS (
          SELECT
            er.topic_id,
            er.date,
            er.integrated_score,
            er.adjusted_score,
            er.is_equilibrium,
            er.equilibrium_score,
            er.contributing_factors
          FROM
            equilibrium_results er
          WHERE
            er.topic_id = '{{ $json.topic_id }}'
            AND er.date = '{{ $json.date }}'
        ),
        action_data AS (
          SELECT
            ca.action_type,
            ca.action_description,
            ca.priority,
            ca.recommended_timing,
            ca.expected_impact
          FROM
            consensus_actions ca
          JOIN
            consensus_results cr ON ca.consensus_result_id = cr.id
          WHERE
            cr.topic_id = '{{ $json.topic_id }}'
            AND cr.date = '{{ $json.date }}'
        ),
        alternative_data AS (
          SELECT
            als.solutions
          FROM
            alternative_solutions als
          WHERE
            als.topic_id = '{{ $json.topic_id }}'
            AND als.date = '{{ $json.date }}'
        ),
        topic_data AS (
          SELECT
            t.id,
            t.name,
            t.description
          FROM
            topics t
          WHERE
            t.id = '{{ $json.topic_id }}'
        )
        SELECT
          td.id AS topic_id,
          td.name AS topic_name,
          td.description AS topic_description,
          '{{ $json.date }}' AS date,
          (
            SELECT jsonb_agg(
              jsonb_build_object(
                'perspective_id', pd.perspective_id,
                'importance', pd.importance,
                'confidence', pd.confidence,
                'overall_score', pd.overall_score
              )
            )
            FROM perspective_data pd
          ) AS perspective_evaluations,
          (
            SELECT coherence
            FROM coherence_data
          ) AS coherence,
          (
            SELECT jsonb_build_object(
              'integrated_score', ed.integrated_score,
              'adjusted_score', ed.adjusted_score,
              'is_equilibrium', ed.is_equilibrium,
              'equilibrium_score', ed.equilibrium_score,
              'contributing_factors', ed.contributing_factors
            )
            FROM equilibrium_data ed
          ) AS equilibrium,
          (
            SELECT jsonb_agg(
              jsonb_build_object(
                'action_type', ad.action_type,
                'action_description', ad.action_description,
                'priority', ad.priority,
                'recommended_timing', ad.recommended_timing,
                'expected_impact', ad.expected_impact
              )
            )
            FROM action_data ad
          ) AS actions,
          (
            SELECT solutions
            FROM alternative_data
          ) AS alternatives
        FROM
          topic_data td
      `
    }
  },
  {
    "id": "prepareVisualizationData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const resultData = $input.item.json;
        
        // Prepare data for radar chart
        const radarData = prepareRadarChartData(resultData);
        
        // Prepare data for perspective comparison chart
        const perspectiveData = preparePerspectiveComparisonData(resultData);
        
        // Prepare data for action priority chart
        const actionData = prepareActionPriorityData(resultData);
        
        // Prepare summary text
        const summaryText = generateSummaryText(resultData);
        
        return {
          json: {
            topic_id: resultData.topic_id,
            topic_name: resultData.topic_name,
            date: resultData.date,
            visualization_data: {
              radar_chart: radarData,
              perspective_chart: perspectiveData,
              action_chart: actionData,
              summary_text: summaryText
            },
            raw_data: resultData
          }
        };
        
        // Helper function: Prepare radar chart data
        function prepareRadarChartData(data) {
          // Extract perspective evaluations
          const perspectives = {};
          for (const eval of data.perspective_evaluations) {
            perspectives[eval.perspective_id] = eval;
          }
          
          // Prepare radar chart data
          return {
            labels: ['重要度', '確信度', '整合性', '安定性', '総合評価'],
            datasets: [
              {
                label: 'テクノロジー視点',
                data: [
                  perspectives.technology?.importance.score || 0,
                  perspectives.technology?.confidence.score || 0,
                  data.coherence?.score || 0,
                  data.equilibrium?.is_equilibrium ? data.equilibrium.contributing_factors.perspectives.technology?.score || 0 : 0,
                  perspectives.technology?.overall_score || 0
                ]
              },
              {
                label: 'マーケット視点',
                data: [
                  perspectives.market?.importance.score || 0,
                  perspectives.market?.confidence.score || 0,
                  data.coherence?.score || 0,
                  data.equilibrium?.is_equilibrium ? data.equilibrium.contributing_factors.perspectives.market?.score || 0 : 0,
                  perspectives.market?.overall_score || 0
                ]
              },
              {
                label: 'ビジネス視点',
                data: [
                  perspectives.business?.importance.score || 0,
                  perspectives.business?.confidence.score || 0,
                  data.coherence?.score || 0,
                  data.equilibrium?.is_equilibrium ? data.equilibrium.contributing_factors.perspectives.business?.score || 0 : 0,
                  perspectives.business?.overall_score || 0
                ]
              }
            ]
          };
        }
        
        // Helper function: Prepare perspective comparison data
        function preparePerspectiveComparisonData(data) {
          // Extract perspective evaluations
          const perspectives = {};
          for (const eval of data.perspective_evaluations) {
            perspectives[eval.perspective_id] = eval;
          }
          
          // Prepare perspective comparison data
          return {
            labels: ['テクノロジー', 'マーケット', 'ビジネス'],
            datasets: [
              {
                label: '重要度',
                data: [
                  perspectives.technology?.importance.score || 0,
                  perspectives.market?.importance.score || 0,
                  perspectives.business?.importance.score || 0
                ]
              },
              {
                label: '確信度',
                data: [
                  perspectives.technology?.confidence.score || 0,
                  perspectives.market?.confidence.score || 0,
                  perspectives.business?.confidence.score || 0
                ]
              },
              {
                label: '総合評価',
                data: [
                  perspectives.technology?.overall_score || 0,
                  perspectives.market?.overall_score || 0,
                  perspectives.business?.overall_score || 0
                ]
              }
            ]
          };
        }
        
        // Helper function: Prepare action priority data
        function prepareActionPriorityData(data) {
          // Extract actions
          const actions = data.actions || [];
          
          // Sort actions by priority
          actions.sort((a, b) => b.priority - a.priority);
          
          // Prepare action priority data
          return {
            labels: actions.map(a => a.action_description.substring(0, 20) + '...'),
            datasets: [
              {
                label: '優先度',
                data: actions.map(a => a.priority)
              }
            ]
          };
        }
        
        // Helper function: Generate summary text
        function generateSummaryText(data) {
          let summary = \`トピック「\${data.topic_name}」の分析結果（\${data.date}）\\n\\n\`;
          
          // Add equilibrium status
          if (data.equilibrium?.is_equilibrium) {
            summary += \`このトピックは静止点として検出されました。静止点スコア: \${(data.equilibrium.equilibrium_score * 100).toFixed(1)}%\\n\\n\`;
          } else {
            summary += \`このトピックは静止点として検出されませんでした。調整後統合スコア: \${(data.equilibrium?.adjusted_score * 100).toFixed(1)}%\\n\\n\`;
          }
          
          // Add perspective summary
          summary += \`視点別評価:\\n\`;
          for (const eval of data.perspective_evaluations) {
            const perspectiveNames = {
              technology: 'テクノロジー',
              market: 'マーケット',
              business: 'ビジネス'
            };
            
            summary += \`- \${perspectiveNames[eval.perspective_id]}視点: 重要度 \${(eval.importance.score * 100).toFixed(1)}%, 確信度 \${(eval.confidence.score * 100).toFixed(1)}%, 総合 \${(eval.overall_score * 100).toFixed(1)}%\\n\`;
          }
          
          summary += \`\\n整合性: \${(data.coherence?.score * 100).toFixed(1)}%\\n\\n\`;
          
          // Add action recommendations
          summary += \`推奨アクション:\\n\`;
          if (data.actions && data.actions.length > 0) {
            for (const action of data.actions) {
              summary += \`- \${action.action_description} (優先度: \${(action.priority * 100).toFixed(1)}%)\\n\`;
            }
          } else {
            summary += \`- 推奨アクションはありません\\n\`;
          }
          
          // Add alternatives if not equilibrium
          if (!data.equilibrium?.is_equilibrium && data.alternatives && data.alternatives.length > 0) {
            summary += \`\\n代替解:\\n\`;
            for (const alt of data.alternatives) {
              summary += \`- \${alt.name}: スコア \${(alt.adjusted_score * 100).toFixed(1)}%\\n\`;
            }
          }
          
          return summary;
        }
      `
    }
  },
  {
    "id": "generateVisualization",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://visualization-service:3000/generate",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "data",
            "value": "={{ $json.visualization_data }}"
          },
          {
            "name": "topic_id",
            "value": "={{ $json.topic_id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.date }}"
          }
        ]
      }
    }
  },
  {
    "id": "saveVisualizationResult",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create visualization_results table if not exists
        CREATE TABLE IF NOT EXISTS visualization_results (
          id SERIAL PRIMARY KEY,
          topic_id VARCHAR(50) NOT NULL,
          date DATE NOT NULL,
          visualization_data JSONB NOT NULL,
          summary_text TEXT NOT NULL,
          visualization_url VARCHAR(255),
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          
          CONSTRAINT unique_topic_date UNIQUE (topic_id, date)
        );
        
        -- Insert or update visualization result
        INSERT INTO visualization_results (
          topic_id,
          date,
          visualization_data,
          summary_text,
          visualization_url
        )
        VALUES (
          '{{ $json.topic_id }}',
          '{{ $json.date }}',
          '{{ $json.visualization_data | json | replace("'", "''") }}'::jsonb,
          '{{ $json.visualization_data.summary_text | replace("'", "''") }}',
          '{{ $json.visualization_url }}'
        )
        ON CONFLICT (topic_id, date)
        DO UPDATE SET
          visualization_data = '{{ $json.visualization_data | json | replace("'", "''") }}'::jsonb,
          summary_text = '{{ $json.visualization_data.summary_text | replace("'", "''") }}',
          visualization_url = '{{ $json.visualization_url }}',
          created_at = CURRENT_TIMESTAMP;
      `
    }
  }
]
```

このワークフローでは、コンセンサスモデルの結果を可視化し、ダッシュボードに表示するためのデータを生成しています。レーダーチャート、視点比較チャート、アクション優先度チャートなどの可視化データと、結果の要約テキストが生成されます。

## 実運用のためのベストプラクティス

コンセンサスモデルを実運用するためのベストプラクティスを以下に示します：

### 1. パラメータの定期的な最適化

コンセンサスモデルのパラメータ（重み、閾値など）は、定期的に評価され、最適化される必要があります。以下のプロセスを定期的に実施することをお勧めします：

1. モデルの予測結果と実際の結果を比較
2. パラメータの感度分析を実施
3. 最適なパラメータセットを特定
4. パラメータを更新

### 2. データソースの多様化と品質管理

コンセンサスモデルの精度は、入力データの質と量に大きく依存します。以下の点に注意してデータソースを管理することをお勧めします：

1. 複数の信頼性の高いデータソースを使用
2. データの鮮度を確保
3. データの前処理と品質チェックを徹底
4. データソースの信頼性を定期的に評価

### 3. モデルの透明性と説明可能性の確保

コンセンサスモデルの判断プロセスは、透明で説明可能であるべきです。以下の点に注意してモデルの透明性を確保することをお勧めします：

1. 判断に至った根拠を明示
2. 各視点の貢献度を可視化
3. 確信度と整合性を明示
4. 代替解を提示

### 4. フィードバックループの構築

コンセンサスモデルの継続的な改善のために、フィードバックループを構築することをお勧めします：

1. ユーザーからのフィードバックを収集
2. モデルの予測精度を定期的に評価
3. フィードバックに基づいてモデルを改善
4. 改善結果を検証

### 5. エラー処理とロギングの強化

実運用環境では、エラー処理とロギングを強化することが重要です：

1. すべてのワークフローにエラーハンドリングを実装
2. 詳細なログを記録
3. アラート機能を実装
4. 定期的なシステムヘルスチェックを実施

## まとめ

このセクションでは、n8nを活用したコンセンサスモデルの全体オーケストレーションについて解説しました。マスターオーケストレーションワークフロー、アクション推奨生成ワークフロー、結果可視化ワークフローなど、主要なワークフローとその連携方法を示しました。また、実運用のためのベストプラクティスについても解説しました。

コンセンサスモデルは、3つの視点（テクノロジー、マーケット、ビジネス）からの情報を統合し、最適な解釈と判断を導き出すための強力なツールです。n8nを活用することで、このモデルを柔軟かつ効率的に実装し、運用することができます。

次のセクションでは、コンセンサスモデルの評価と最適化について詳細に解説します。
