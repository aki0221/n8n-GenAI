### 7.1 ワークフロー管理

コンセンサスモデルの管理コンポーネントにおけるワークフロー管理は、全体のプロセスを効率的に制御し、各コンポーネント間の連携をスムーズに行うための重要な機能です。n8nを活用することで、複雑なワークフローを視覚的に設計し、自動化することができます。

**ワークフロー設計と実装**

コンセンサスモデルのワークフロー管理では、データ収集から分析、評価、統合、出力までの一連のプロセスを効率的に制御する必要があります。n8nでは、これらのプロセスを視覚的なワークフローとして設計し、実装することができます。

**メインワークフローの設計**:
コンセンサスモデルの全体プロセスを制御するメインワークフローを設計します。

```javascript
// メインワークフローの設計例（n8nワークフロー）

// 1. ワークフロートリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/trigger",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. 入力パラメータの検証（Functionノード）
function validateInput(items) {
  const input = items[0].json.body;
  const errors = [];
  
  // 必須パラメータの検証
  if (!input.target_id) {
    errors.push("Missing required parameter: target_id");
  }
  
  if (!input.target_name) {
    errors.push("Missing required parameter: target_name");
  }
  
  // 視点の検証
  const perspectives = input.perspectives || ["technology", "market", "business"];
  const validPerspectives = ["technology", "market", "business"];
  
  for (const perspective of perspectives) {
    if (!validPerspectives.includes(perspective)) {
      errors.push(`Invalid perspective: ${perspective}`);
    }
  }
  
  // エラーがある場合は処理を中止
  if (errors.length > 0) {
    return [
      {
        json: {
          success: false,
          errors: errors
        }
      }
    ];
  }
  
  // 検証済みの入力パラメータを返す
  return [
    {
      json: {
        success: true,
        target_id: input.target_id,
        target_name: input.target_name,
        target_type: input.target_type || "project",
        perspectives: perspectives,
        weights: input.weights || {
          technology: 0.33,
          market: 0.33,
          business: 0.33
        },
        data_sources: input.data_sources || [],
        options: input.options || {},
        workflow_id: generateWorkflowId(),
        timestamp: new Date().toISOString()
      }
    }
  ];
}

// ワークフローIDの生成
function generateWorkflowId() {
  return 'wf_' + Math.random().toString(36).substring(2, 15);
}

// 3. ワークフロー状態の初期化（Functionノード）
function initializeWorkflowState(items) {
  const input = items[0].json;
  
  // ワークフロー状態の初期化
  const workflowState = {
    workflow_id: input.workflow_id,
    target_id: input.target_id,
    target_name: input.target_name,
    target_type: input.target_type,
    status: "initialized",
    start_time: new Date().toISOString(),
    perspectives: input.perspectives,
    weights: input.weights,
    progress: {
      overall: 0,
      data_collection: 0,
      analysis: 0,
      evaluation: 0,
      integration: 0,
      output: 0
    },
    results: {
      data_collection: {},
      analysis: {},
      evaluation: {},
      integration: {},
      output: {}
    },
    errors: [],
    logs: [
      {
        timestamp: new Date().toISOString(),
        level: "info",
        message: "Workflow initialized"
      }
    ]
  };
  
  return [
    {
      json: {
        ...input,
        workflow_state: workflowState
      }
    }
  ];
}

// 4. データ収集サブワークフローの呼び出し（HTTPリクエストノード）
// 設定例
{
  "url": "=https://n8n.example.com/webhook/consensus-model/data-collection",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "n8n-internal-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 60000
  }
}

// 5. ワークフロー状態の更新（Functionノード）
function updateWorkflowState(items) {
  const input = items[0].json;
  const dataCollectionResult = items[0].json.body;
  
  // ワークフロー状態の更新
  const workflowState = input.workflow_state;
  
  // データ収集結果の保存
  workflowState.results.data_collection = dataCollectionResult.data;
  
  // 進捗状況の更新
  workflowState.progress.data_collection = 1;
  workflowState.progress.overall = calculateOverallProgress(workflowState.progress);
  
  // ログの追加
  workflowState.logs.push({
    timestamp: new Date().toISOString(),
    level: "info",
    message: "Data collection completed"
  });
  
  // ステータスの更新
  workflowState.status = "data_collection_completed";
  
  return [
    {
      json: {
        ...input,
        workflow_state: workflowState
      }
    }
  ];
}

// 全体の進捗状況の計算
function calculateOverallProgress(progress) {
  const weights = {
    data_collection: 0.2,
    analysis: 0.3,
    evaluation: 0.2,
    integration: 0.2,
    output: 0.1
  };
  
  let overall = 0;
  for (const [stage, weight] of Object.entries(weights)) {
    overall += progress[stage] * weight;
  }
  
  return overall;
}

// 6. 分析サブワークフローの呼び出し（HTTPリクエストノード）
// 設定例
{
  "url": "=https://n8n.example.com/webhook/consensus-model/analysis",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "n8n-internal-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 120000
  }
}

// 7. ワークフロー状態の更新（Functionノード）
// （同様のパターンで分析結果を保存）

// 8. 評価サブワークフローの呼び出し（HTTPリクエストノード）
// 設定例
{
  "url": "=https://n8n.example.com/webhook/consensus-model/evaluation",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "n8n-internal-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 90000
  }
}

// 9. ワークフロー状態の更新（Functionノード）
// （同様のパターンで評価結果を保存）

// 10. 統合サブワークフローの呼び出し（HTTPリクエストノード）
// 設定例
{
  "url": "=https://n8n.example.com/webhook/consensus-model/integration",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "n8n-internal-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 60000
  }
}

// 11. ワークフロー状態の更新（Functionノード）
// （同様のパターンで統合結果を保存）

// 12. 出力サブワークフローの呼び出し（HTTPリクエストノード）
// 設定例
{
  "url": "=https://n8n.example.com/webhook/consensus-model/output",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "n8n-internal-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 60000
  }
}

// 13. ワークフロー状態の最終更新（Functionノード）
function finalizeWorkflowState(items) {
  const input = items[0].json;
  const outputResult = items[0].json.body;
  
  // ワークフロー状態の更新
  const workflowState = input.workflow_state;
  
  // 出力結果の保存
  workflowState.results.output = outputResult.data;
  
  // 進捗状況の更新
  workflowState.progress.output = 1;
  workflowState.progress.overall = 1;
  
  // 完了時間の記録
  workflowState.end_time = new Date().toISOString();
  
  // ログの追加
  workflowState.logs.push({
    timestamp: new Date().toISOString(),
    level: "info",
    message: "Workflow completed successfully"
  });
  
  // ステータスの更新
  workflowState.status = "completed";
  
  return [
    {
      json: {
        success: true,
        workflow_id: workflowState.workflow_id,
        target_id: workflowState.target_id,
        target_name: workflowState.target_name,
        status: workflowState.status,
        start_time: workflowState.start_time,
        end_time: workflowState.end_time,
        results: {
          consensus_score: workflowState.results.integration.consensus_score,
          perspective_scores: workflowState.results.integration.perspective_scores,
          recommendations: workflowState.results.output.recommendations,
          report_url: workflowState.results.output.report_url
        },
        workflow_state: workflowState
      }
    }
  ];
}

// 14. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなメインワークフローの設計により、コンセンサスモデルの全体プロセスを効率的に制御することができます。各サブワークフローの呼び出し、ワークフロー状態の管理、エラーハンドリングなどの機能を含めることで、堅牢なワークフロー管理を実現することができます。

**サブワークフローの設計**:
各コンポーネント（データ収集、分析、評価、統合、出力）ごとにサブワークフローを設計します。以下に、データ収集サブワークフローの例を示します。

```javascript
// データ収集サブワークフローの設計例（n8nワークフロー）

// 1. サブワークフロートリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/data-collection",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. データソースの分類（Functionノード）
function classifyDataSources(items) {
  const input = items[0].json.body;
  const workflowState = input.workflow_state;
  const dataSources = input.data_sources || [];
  
  // データソースを視点ごとに分類
  const classifiedSources = {
    technology: [],
    market: [],
    business: []
  };
  
  // 明示的に分類されているデータソース
  dataSources.forEach(source => {
    if (source.perspective && classifiedSources[source.perspective]) {
      classifiedSources[source.perspective].push(source);
    } else if (source.type) {
      // タイプに基づいて分類
      switch (source.type.toLowerCase()) {
        case 'patent':
        case 'technical_report':
        case 'research_paper':
        case 'github':
        case 'stackoverflow':
          classifiedSources.technology.push(source);
          break;
        case 'market_report':
        case 'news':
        case 'social_media':
        case 'competitor':
        case 'customer_feedback':
          classifiedSources.market.push(source);
          break;
        case 'financial_report':
        case 'business_plan':
        case 'strategic_document':
        case 'resource_plan':
          classifiedSources.business.push(source);
          break;
        default:
          // デフォルトは全ての視点に追加
          classifiedSources.technology.push(source);
          classifiedSources.market.push(source);
          classifiedSources.business.push(source);
          break;
      }
    } else {
      // 分類情報がない場合は全ての視点に追加
      classifiedSources.technology.push(source);
      classifiedSources.market.push(source);
      classifiedSources.business.push(source);
    }
  });
  
  // デフォルトのデータソースを追加
  const targetId = workflowState.target_id;
  const targetType = workflowState.target_type;
  
  // テクノロジー視点のデフォルトデータソース
  if (classifiedSources.technology.length === 0) {
    classifiedSources.technology.push({
      type: 'default_technology',
      url: `https://api.example.com/data/technology/${targetType}/${targetId}`,
      perspective: 'technology'
    });
  }
  
  // マーケット視点のデフォルトデータソース
  if (classifiedSources.market.length === 0) {
    classifiedSources.market.push({
      type: 'default_market',
      url: `https://api.example.com/data/market/${targetType}/${targetId}`,
      perspective: 'market'
    });
  }
  
  // ビジネス視点のデフォルトデータソース
  if (classifiedSources.business.length === 0) {
    classifiedSources.business.push({
      type: 'default_business',
      url: `https://api.example.com/data/business/${targetType}/${targetId}`,
      perspective: 'business'
    });
  }
  
  return [
    {
      json: {
        ...input,
        classified_sources: classifiedSources
      }
    }
  ];
}

// 3. テクノロジーデータの収集（HTTPリクエストノード）
// 設定例
{
  "url": "=https://api.example.com/data/technology/collect",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "data-api-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 60000
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "target_id",
        "value": "={{ $json.workflow_state.target_id }}"
      },
      {
        "name": "target_type",
        "value": "={{ $json.workflow_state.target_type }}"
      },
      {
        "name": "data_sources",
        "value": "={{ $json.classified_sources.technology }}"
      }
    ]
  }
}

// 4. マーケットデータの収集（HTTPリクエストノード）
// （テクノロジーデータの収集と同様のパターン）

// 5. ビジネスデータの収集（HTTPリクエストノード）
// （テクノロジーデータの収集と同様のパターン）

// 6. データの統合と構造化（Functionノード）
function integrateAndStructureData(items) {
  const input = items[0].json;
  const technologyData = items[0].json.body;
  const marketData = items[1].json.body;
  const businessData = items[2].json.body;
  
  // 収集したデータの統合
  const integratedData = {
    technology: technologyData.data,
    market: marketData.data,
    business: businessData.data
  };
  
  // データの構造化
  const structuredData = structureData(integratedData);
  
  // ワークフロー状態の更新
  const workflowState = input.workflow_state;
  
  // 進捗状況の更新
  workflowState.progress.data_collection = 1;
  workflowState.progress.overall = calculateOverallProgress(workflowState.progress);
  
  // ログの追加
  workflowState.logs.push({
    timestamp: new Date().toISOString(),
    level: "info",
    message: "Data collection and structuring completed"
  });
  
  return [
    {
      json: {
        success: true,
        workflow_id: workflowState.workflow_id,
        data: structuredData,
        workflow_state: workflowState
      }
    }
  ];
}

// データの構造化
function structureData(integratedData) {
  // データの構造化ロジック
  // （実際の実装ではより複雑な処理が行われる）
  
  return {
    technology: {
      trends: integratedData.technology.trends || [],
      patents: integratedData.technology.patents || [],
      technical_feasibility: integratedData.technology.technical_feasibility || {},
      metadata: integratedData.technology.metadata || {}
    },
    market: {
      trends: integratedData.market.trends || [],
      competitors: integratedData.market.competitors || [],
      customer_needs: integratedData.market.customer_needs || [],
      metadata: integratedData.market.metadata || {}
    },
    business: {
      revenue_potential: integratedData.business.revenue_potential || {},
      strategic_fit: integratedData.business.strategic_fit || {},
      resource_requirements: integratedData.business.resource_requirements || {},
      metadata: integratedData.business.metadata || {}
    }
  };
}

// 全体の進捗状況の計算
function calculateOverallProgress(progress) {
  const weights = {
    data_collection: 0.2,
    analysis: 0.3,
    evaluation: 0.2,
    integration: 0.2,
    output: 0.1
  };
  
  let overall = 0;
  for (const [stage, weight] of Object.entries(weights)) {
    overall += progress[stage] * weight;
  }
  
  return overall;
}

// 7. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなサブワークフローの設計により、各コンポーネントの処理を効率的に実行することができます。データソースの分類、データの収集、統合と構造化などの機能を含めることで、堅牢なデータ収集プロセスを実現することができます。

**ワークフロー監視と制御**

コンセンサスモデルのワークフロー管理では、実行中のワークフローを監視し、必要に応じて制御することが重要です。n8nでは、ワークフロー監視と制御のための機能を実装することができます。

**ワークフロー状態の監視**:
実行中のワークフローの状態を監視し、進捗状況やエラーを確認するための機能を実装します。

```javascript
// ワークフロー状態の監視例（n8nワークフロー）

// 1. ワークフロー監視トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/monitor/:workflowId",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. ワークフロー状態の取得（Functionノード）
async function getWorkflowState(items) {
  const workflowId = items[0].json.params.workflowId;
  
  try {
    // ワークフロー状態の取得
    // （実際の実装ではデータベースやキャッシュからの取得が行われる）
    const workflowState = await fetchWorkflowState(workflowId);
    
    if (!workflowState) {
      return [
        {
          json: {
            success: false,
            error: "Workflow not found",
            workflow_id: workflowId
          }
        }
      ];
    }
    
    // 監視情報の作成
    const monitorInfo = {
      workflow_id: workflowState.workflow_id,
      target_id: workflowState.target_id,
      target_name: workflowState.target_name,
      status: workflowState.status,
      start_time: workflowState.start_time,
      end_time: workflowState.end_time,
      progress: workflowState.progress,
      errors: workflowState.errors,
      recent_logs: workflowState.logs.slice(-10) // 最新の10件のログ
    };
    
    return [
      {
        json: {
          success: true,
          monitor_info: monitorInfo
        }
      }
    ];
  } catch (error) {
    return [
      {
        json: {
          success: false,
          error: "Failed to retrieve workflow state",
          message: error.message,
          workflow_id: workflowId
        }
      }
    ];
  }
}

// ワークフロー状態の取得
async function fetchWorkflowState(workflowId) {
  // データベースやキャッシュからワークフロー状態を取得
  // （実際の実装ではデータベース接続などが必要）
  
  // サンプル実装（実際にはデータベース接続などが必要）
  const workflowStates = {
    'wf_sample123': {
      workflow_id: 'wf_sample123',
      target_id: 'target_001',
      target_name: 'サンプルプロジェクト',
      target_type: 'project',
      status: 'analysis_completed',
      start_time: '2023-06-01T10:00:00Z',
      end_time: null,
      perspectives: ['technology', 'market', 'business'],
      weights: {
        technology: 0.33,
        market: 0.33,
        business: 0.33
      },
      progress: {
        overall: 0.6,
        data_collection: 1,
        analysis: 1,
        evaluation: 0.8,
        integration: 0,
        output: 0
      },
      results: {
        data_collection: { /* データ収集結果 */ },
        analysis: { /* 分析結果 */ },
        evaluation: { /* 評価結果（一部） */ },
        integration: {},
        output: {}
      },
      errors: [],
      logs: [
        {
          timestamp: '2023-06-01T10:00:00Z',
          level: 'info',
          message: 'Workflow initialized'
        },
        {
          timestamp: '2023-06-01T10:01:30Z',
          level: 'info',
          message: 'Data collection started'
        },
        {
          timestamp: '2023-06-01T10:05:45Z',
          level: 'info',
          message: 'Data collection completed'
        },
        {
          timestamp: '2023-06-01T10:06:00Z',
          level: 'info',
          message: 'Analysis started'
        },
        {
          timestamp: '2023-06-01T10:15:30Z',
          level: 'info',
          message: 'Analysis completed'
        },
        {
          timestamp: '2023-06-01T10:16:00Z',
          level: 'info',
          message: 'Evaluation started'
        },
        {
          timestamp: '2023-06-01T10:20:00Z',
          level: 'info',
          message: 'Technology perspective evaluation completed'
        },
        {
          timestamp: '2023-06-01T10:22:30Z',
          level: 'info',
          message: 'Market perspective evaluation completed'
        },
        {
          timestamp: '2023-06-01T10:25:00Z',
          level: 'info',
          message: 'Business perspective evaluation in progress'
        }
      ]
    },
    'wf_sample456': {
      workflow_id: 'wf_sample456',
      target_id: 'target_002',
      target_name: '別のサンプルプロジェクト',
      target_type: 'project',
      status: 'completed',
      start_time: '2023-06-01T09:30:00Z',
      end_time: '2023-06-01T10:15:00Z',
      perspectives: ['technology', 'market', 'business'],
      weights: {
        technology: 0.4,
        market: 0.3,
        business: 0.3
      },
      progress: {
        overall: 1,
        data_collection: 1,
        analysis: 1,
        evaluation: 1,
        integration: 1,
        output: 1
      },
      results: {
        data_collection: { /* データ収集結果 */ },
        analysis: { /* 分析結果 */ },
        evaluation: { /* 評価結果 */ },
        integration: { /* 統合結果 */ },
        output: { /* 出力結果 */ }
      },
      errors: [],
      logs: [
        /* ログエントリ */
      ]
    },
    'wf_sample789': {
      workflow_id: 'wf_sample789',
      target_id: 'target_003',
      target_name: 'エラーが発生したプロジェクト',
      target_type: 'project',
      status: 'failed',
      start_time: '2023-06-01T11:00:00Z',
      end_time: '2023-06-01T11:05:30Z',
      perspectives: ['technology', 'market', 'business'],
      weights: {
        technology: 0.33,
        market: 0.33,
        business: 0.33
      },
      progress: {
        overall: 0.1,
        data_collection: 0.5,
        analysis: 0,
        evaluation: 0,
        integration: 0,
        output: 0
      },
      results: {
        data_collection: { /* 一部のデータ収集結果 */ },
        analysis: {},
        evaluation: {},
        integration: {},
        output: {}
      },
      errors: [
        {
          timestamp: '2023-06-01T11:05:30Z',
          component: 'data_collection',
          message: 'Failed to connect to data source',
          details: 'Connection timeout after 30 seconds'
        }
      ],
      logs: [
        /* ログエントリ */
      ]
    }
  };
  
  return workflowStates[workflowId];
}

// 3. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなワークフロー状態の監視機能を実装することで、実行中のワークフローの進捗状況やエラーを確認することができます。ワークフロー状態の取得、監視情報の作成などの機能を含めることで、効果的なワークフロー監視を実現することができます。

**ワークフロー制御**:
実行中のワークフローを制御（一時停止、再開、中止など）するための機能を実装します。

```javascript
// ワークフロー制御例（n8nワークフロー）

// 1. ワークフロー制御トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/control/:workflowId",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. ワークフロー制御の実行（Functionノード）
async function controlWorkflow(items) {
  const workflowId = items[0].json.params.workflowId;
  const action = items[0].json.body.action;
  
  // 有効なアクションの検証
  const validActions = ['pause', 'resume', 'abort', 'retry'];
  if (!action || !validActions.includes(action)) {
    return [
      {
        json: {
          success: false,
          error: "Invalid action",
          valid_actions: validActions,
          workflow_id: workflowId
        }
      }
    ];
  }
  
  try {
    // ワークフロー状態の取得
    const workflowState = await fetchWorkflowState(workflowId);
    
    if (!workflowState) {
      return [
        {
          json: {
            success: false,
            error: "Workflow not found",
            workflow_id: workflowId
          }
        }
      ];
    }
    
    // アクションの実行
    let result;
    switch (action) {
      case 'pause':
        result = await pauseWorkflow(workflowState);
        break;
      case 'resume':
        result = await resumeWorkflow(workflowState);
        break;
      case 'abort':
        result = await abortWorkflow(workflowState);
        break;
      case 'retry':
        result = await retryWorkflow(workflowState);
        break;
    }
    
    return [
      {
        json: {
          success: true,
          action: action,
          result: result,
          workflow_id: workflowId
        }
      }
    ];
  } catch (error) {
    return [
      {
        json: {
          success: false,
          error: `Failed to ${action} workflow`,
          message: error.message,
          workflow_id: workflowId
        }
      }
    ];
  }
}

// ワークフローの一時停止
async function pauseWorkflow(workflowState) {
  // ワークフローの一時停止処理
  // （実際の実装ではワークフローエンジンへの制御命令が送信される）
  
  // 現在のステータスの検証
  if (['completed', 'failed', 'aborted', 'paused'].includes(workflowState.status)) {
    throw new Error(`Cannot pause workflow in ${workflowState.status} status`);
  }
  
  // ワークフロー状態の更新
  const previousStatus = workflowState.status;
  workflowState.status = 'paused';
  workflowState.logs.push({
    timestamp: new Date().toISOString(),
    level: 'info',
    message: `Workflow paused (previous status: ${previousStatus})`
  });
  
  // 更新されたワークフロー状態の保存
  await saveWorkflowState(workflowState);
  
  return {
    previous_status: previousStatus,
    current_status: workflowState.status,
    paused_at: new Date().toISOString()
  };
}

// ワークフローの再開
async function resumeWorkflow(workflowState) {
  // ワークフローの再開処理
  // （実際の実装ではワークフローエンジンへの制御命令が送信される）
  
  // 現在のステータスの検証
  if (workflowState.status !== 'paused') {
    throw new Error(`Cannot resume workflow in ${workflowState.status} status`);
  }
  
  // 一時停止前のステータスを特定
  const previousLogs = workflowState.logs.filter(log => 
    log.message.startsWith('Workflow paused (previous status:')
  );
  
  let resumeStatus = 'running';
  if (previousLogs.length > 0) {
    const lastPauseLog = previousLogs[previousLogs.length - 1];
    const match = lastPauseLog.message.match(/previous status: ([a-z_]+)/);
    if (match && match[1]) {
      resumeStatus = match[1];
    }
  }
  
  // ワークフロー状態の更新
  workflowState.status = resumeStatus;
  workflowState.logs.push({
    timestamp: new Date().toISOString(),
    level: 'info',
    message: `Workflow resumed (new status: ${resumeStatus})`
  });
  
  // 更新されたワークフロー状態の保存
  await saveWorkflowState(workflowState);
  
  return {
    previous_status: 'paused',
    current_status: workflowState.status,
    resumed_at: new Date().toISOString()
  };
}

// ワークフローの中止
async function abortWorkflow(workflowState) {
  // ワークフローの中止処理
  // （実際の実装ではワークフローエンジンへの制御命令が送信される）
  
  // 現在のステータスの検証
  if (['completed', 'failed', 'aborted'].includes(workflowState.status)) {
    throw new Error(`Cannot abort workflow in ${workflowState.status} status`);
  }
  
  // ワークフロー状態の更新
  const previousStatus = workflowState.status;
  workflowState.status = 'aborted';
  workflowState.end_time = new Date().toISOString();
  workflowState.logs.push({
    timestamp: new Date().toISOString(),
    level: 'warning',
    message: `Workflow aborted (previous status: ${previousStatus})`
  });
  
  // 更新されたワークフロー状態の保存
  await saveWorkflowState(workflowState);
  
  return {
    previous_status: previousStatus,
    current_status: workflowState.status,
    aborted_at: workflowState.end_time
  };
}

// ワークフローの再試行
async function retryWorkflow(workflowState) {
  // ワークフローの再試行処理
  // （実際の実装ではワークフローエンジンへの制御命令が送信される）
  
  // 現在のステータスの検証
  if (!['failed', 'aborted'].includes(workflowState.status)) {
    throw new Error(`Cannot retry workflow in ${workflowState.status} status`);
  }
  
  // 失敗したコンポーネントの特定
  let failedComponent = 'data_collection';
  if (workflowState.errors.length > 0) {
    failedComponent = workflowState.errors[0].component;
  } else {
    // 進捗状況から失敗したコンポーネントを推測
    const progress = workflowState.progress;
    if (progress.data_collection < 1) {
      failedComponent = 'data_collection';
    } else if (progress.analysis < 1) {
      failedComponent = 'analysis';
    } else if (progress.evaluation < 1) {
      failedComponent = 'evaluation';
    } else if (progress.integration < 1) {
      failedComponent = 'integration';
    } else if (progress.output < 1) {
      failedComponent = 'output';
    }
  }
  
  // ワークフロー状態の更新
  const previousStatus = workflowState.status;
  workflowState.status = `${failedComponent}_retry`;
  workflowState.logs.push({
    timestamp: new Date().toISOString(),
    level: 'info',
    message: `Workflow retry initiated for component: ${failedComponent}`
  });
  
  // エラー情報のクリア
  workflowState.errors = [];
  
  // 更新されたワークフロー状態の保存
  await saveWorkflowState(workflowState);
  
  return {
    previous_status: previousStatus,
    current_status: workflowState.status,
    retry_component: failedComponent,
    retry_initiated_at: new Date().toISOString()
  };
}

// ワークフロー状態の保存
async function saveWorkflowState(workflowState) {
  // ワークフロー状態の保存処理
  // （実際の実装ではデータベースやキャッシュへの保存が行われる）
  
  // サンプル実装（実際にはデータベース接続などが必要）
  console.log(`Saving workflow state for ${workflowState.workflow_id}`);
  return true;
}

// 3. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなワークフロー制御機能を実装することで、実行中のワークフローを一時停止、再開、中止、再試行することができます。各制御アクションの実装、ワークフロー状態の更新などの機能を含めることで、効果的なワークフロー制御を実現することができます。

**ワークフロースケジューリング**

コンセンサスモデルのワークフロー管理では、定期的な実行や特定のイベントに基づく実行など、ワークフローのスケジューリングも重要です。n8nでは、様々なトリガーを使用してワークフローのスケジューリングを実装することができます。

**定期実行の設定**:
コンセンサスモデルのワークフローを定期的に実行するためのスケジューリングを設定します。

```javascript
// 定期実行の設定例（n8nワークフロー）

// 1. スケジュールトリガー（Cronノード）
// 設定例（毎日午前9時に実行）
{
  "triggerTimes": {
    "item": [
      {
        "mode": "everyDay"
      }
    ]
  },
  "cronExpression": "0 9 * * *"
}

// 2. 実行対象の取得（Functionノード）
async function getExecutionTargets() {
  // 実行対象の取得
  // （実際の実装ではデータベースやAPIからの取得が行われる）
  
  // サンプル実装（実際にはデータベース接続などが必要）
  const targets = [
    {
      target_id: 'project_001',
      target_name: '定期分析プロジェクト1',
      target_type: 'project',
      schedule: {
        frequency: 'daily',
        last_execution: '2023-05-31T09:00:00Z'
      }
    },
    {
      target_id: 'product_002',
      target_name: '定期分析製品2',
      target_type: 'product',
      schedule: {
        frequency: 'weekly',
        last_execution: '2023-05-25T09:00:00Z'
      }
    },
    {
      target_id: 'technology_003',
      target_name: '定期分析技術3',
      target_type: 'technology',
      schedule: {
        frequency: 'monthly',
        last_execution: '2023-05-01T09:00:00Z'
      }
    }
  ];
  
  // 今日実行すべき対象をフィルタリング
  const today = new Date();
  const filteredTargets = targets.filter(target => {
    const lastExecution = new Date(target.schedule.last_execution);
    const daysSinceLastExecution = Math.floor((today - lastExecution) / (1000 * 60 * 60 * 24));
    
    switch (target.schedule.frequency) {
      case 'daily':
        return daysSinceLastExecution >= 1;
      case 'weekly':
        return daysSinceLastExecution >= 7;
      case 'monthly':
        return daysSinceLastExecution >= 30;
      default:
        return false;
    }
  });
  
  return [
    {
      json: {
        execution_date: today.toISOString(),
        targets: filteredTargets
      }
    }
  ];
}

// 3. 各対象の分析実行（SplitInBatchesノード）
// 設定例
{
  "batchSize": 1,
  "options": {}
}

// 4. コンセンサスモデル分析の実行（HTTPリクエストノード）
// 設定例
{
  "url": "=https://n8n.example.com/webhook/consensus-model/trigger",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "n8n-internal-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 30000
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "target_id",
        "value": "={{ $json.target_id }}"
      },
      {
        "name": "target_name",
        "value": "={{ $json.target_name }}"
      },
      {
        "name": "target_type",
        "value": "={{ $json.target_type }}"
      },
      {
        "name": "scheduled_execution",
        "value": true
      },
      {
        "name": "execution_date",
        "value": "={{ $parent.json.execution_date }}"
      }
    ]
  }
}

// 5. 実行結果の記録（Functionノード）
async function recordExecutionResults(items) {
  const results = items.map(item => {
    const target = item.json.body;
    const response = item.json.body;
    
    return {
      target_id: target.target_id,
      target_name: target.target_name,
      execution_date: item.json.execution_date,
      workflow_id: response.workflow_id,
      status: response.success ? 'initiated' : 'failed',
      error: response.success ? null : response.error
    };
  });
  
  // 実行結果の記録
  // （実際の実装ではデータベースやログへの記録が行われる）
  
  // サンプル実装（実際にはデータベース接続などが必要）
  console.log('Scheduled execution results:', JSON.stringify(results, null, 2));
  
  return [
    {
      json: {
        execution_date: items[0].json.execution_date,
        results: results
      }
    }
  ];
}
```

このような定期実行の設定により、コンセンサスモデルのワークフローを定期的に実行することができます。スケジュールトリガーの設定、実行対象の取得、分析の実行、結果の記録などの機能を含めることで、効果的なワークフロースケジューリングを実現することができます。

**イベントベースの実行**:
特定のイベント（例：データソースの更新、外部システムからの通知など）に基づいてコンセンサスモデルのワークフローを実行するための設定を行います。

```javascript
// イベントベースの実行例（n8nワークフロー）

// 1. イベントトリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/event-trigger",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. イベントの検証と分類（Functionノード）
function validateAndClassifyEvent(items) {
  const event = items[0].json.body;
  
  // 必須フィールドの検証
  if (!event.event_type) {
    return [
      {
        json: {
          success: false,
          error: "Missing required field: event_type"
        }
      }
    ];
  }
  
  if (!event.target_id) {
    return [
      {
        json: {
          success: false,
          error: "Missing required field: target_id"
        }
      }
    ];
  }
  
  // イベントタイプの分類
  let eventCategory;
  switch (event.event_type) {
    case 'data_source_updated':
    case 'new_data_available':
    case 'data_refresh_requested':
      eventCategory = 'data_event';
      break;
    case 'analysis_requested':
    case 'evaluation_requested':
    case 'report_requested':
      eventCategory = 'analysis_event';
      break;
    case 'schedule_triggered':
    case 'manual_trigger':
    case 'system_trigger':
      eventCategory = 'trigger_event';
      break;
    default:
      eventCategory = 'unknown_event';
      break;
  }
  
  return [
    {
      json: {
        success: true,
        event: event,
        event_category: eventCategory,
        timestamp: new Date().toISOString()
      }
    }
  ];
}

// 3. イベントに基づく処理の分岐（SwitchNode）
// 設定例
{
  "rules": {
    "rules": [
      {
        "value1": "={{ $json.event_category }}",
        "operation": "equal",
        "value2": "data_event"
      },
      {
        "value1": "={{ $json.event_category }}",
        "operation": "equal",
        "value2": "analysis_event"
      },
      {
        "value1": "={{ $json.event_category }}",
        "operation": "equal",
        "value2": "trigger_event"
      }
    ]
  },
  "options": {
    "fallbackOutput": "={{ $json.event_category === 'unknown_event' }}"
  }
}

// 4. データイベント処理（Functionノード）
async function processDataEvent(items) {
  const event = items[0].json.event;
  
  // ターゲット情報の取得
  const targetInfo = await fetchTargetInfo(event.target_id);
  
  if (!targetInfo) {
    return [
      {
        json: {
          success: false,
          error: "Target not found",
          target_id: event.target_id
        }
      }
    ];
  }
  
  // データソース情報の更新
  let dataSourceUpdate = {
    target_id: event.target_id,
    target_name: targetInfo.name,
    target_type: targetInfo.type,
    data_sources: []
  };
  
  // イベントタイプに基づくデータソースの設定
  switch (event.event_type) {
    case 'data_source_updated':
      if (event.data_source) {
        dataSourceUpdate.data_sources.push(event.data_source);
      }
      break;
    case 'new_data_available':
      if (event.data_sources) {
        dataSourceUpdate.data_sources = event.data_sources;
      }
      break;
    case 'data_refresh_requested':
      // デフォルトのデータソースを使用
      dataSourceUpdate.refresh_all = true;
      break;
  }
  
  // データ収集のみを実行するフラグ
  dataSourceUpdate.data_collection_only = event.data_collection_only !== false;
  
  return [
    {
      json: {
        success: true,
        event_type: event.event_type,
        target_id: event.target_id,
        data_source_update: dataSourceUpdate
      }
    }
  ];
}

// 5. 分析イベント処理（Functionノード）
async function processAnalysisEvent(items) {
  const event = items[0].json.event;
  
  // ターゲット情報の取得
  const targetInfo = await fetchTargetInfo(event.target_id);
  
  if (!targetInfo) {
    return [
      {
        json: {
          success: false,
          error: "Target not found",
          target_id: event.target_id
        }
      }
    ];
  }
  
  // 分析パラメータの設定
  let analysisParams = {
    target_id: event.target_id,
    target_name: targetInfo.name,
    target_type: targetInfo.type,
    perspectives: event.perspectives || ["technology", "market", "business"],
    weights: event.weights || {
      technology: 0.33,
      market: 0.33,
      business: 0.33
    },
    options: event.options || {}
  };
  
  // イベントタイプに基づく追加パラメータの設定
  switch (event.event_type) {
    case 'analysis_requested':
      // 全プロセスを実行
      break;
    case 'evaluation_requested':
      // 分析結果を使用して評価から開始
      analysisParams.start_from = 'evaluation';
      analysisParams.analysis_results = event.analysis_results;
      break;
    case 'report_requested':
      // 統合結果を使用してレポート生成のみ実行
      analysisParams.start_from = 'output';
      analysisParams.integration_results = event.integration_results;
      break;
  }
  
  return [
    {
      json: {
        success: true,
        event_type: event.event_type,
        target_id: event.target_id,
        analysis_params: analysisParams
      }
    }
  ];
}

// 6. トリガーイベント処理（Functionノード）
async function processTriggerEvent(items) {
  const event = items[0].json.event;
  
  // ターゲット情報の取得
  const targetInfo = await fetchTargetInfo(event.target_id);
  
  if (!targetInfo) {
    return [
      {
        json: {
          success: false,
          error: "Target not found",
          target_id: event.target_id
        }
      }
    ];
  }
  
  // トリガーパラメータの設定
  let triggerParams = {
    target_id: event.target_id,
    target_name: targetInfo.name,
    target_type: targetInfo.type,
    trigger_type: event.event_type,
    trigger_source: event.source || 'external',
    trigger_time: new Date().toISOString(),
    options: event.options || {}
  };
  
  return [
    {
      json: {
        success: true,
        event_type: event.event_type,
        target_id: event.target_id,
        trigger_params: triggerParams
      }
    }
  ];
}

// ターゲット情報の取得
async function fetchTargetInfo(targetId) {
  // ターゲット情報の取得
  // （実際の実装ではデータベースやAPIからの取得が行われる）
  
  // サンプル実装（実際にはデータベース接続などが必要）
  const targets = {
    'project_001': {
      id: 'project_001',
      name: 'イベントトリガープロジェクト1',
      type: 'project'
    },
    'product_002': {
      id: 'product_002',
      name: 'イベントトリガー製品2',
      type: 'product'
    },
    'technology_003': {
      id: 'technology_003',
      name: 'イベントトリガー技術3',
      type: 'technology'
    }
  };
  
  return targets[targetId];
}

// 7. コンセンサスモデル分析の実行（HTTPリクエストノード）
// 設定例
{
  "url": "=https://n8n.example.com/webhook/consensus-model/trigger",
  "method": "POST",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "nodeCredentialName": "n8n-internal-auth",
  "options": {
    "allowUnauthorizedCerts": false,
    "bodyContentType": "json",
    "fullResponse": true,
    "followRedirect": true,
    "ignoreResponseCode": false,
    "timeout": 30000
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "target_id",
        "value": "={{ $json.target_id }}"
      },
      {
        "name": "target_name",
        "value": "={{ $json.target_name }}"
      },
      {
        "name": "target_type",
        "value": "={{ $json.target_type }}"
      },
      {
        "name": "event_triggered",
        "value": true
      },
      {
        "name": "event_type",
        "value": "={{ $json.event_type }}"
      },
      {
        "name": "event_params",
        "value": "={{ $json }}"
      }
    ]
  }
}

// 8. イベント処理結果の記録（Functionノード）
async function recordEventProcessingResult(items) {
  const event = items[0].json.event;
  const response = items[0].json.body;
  
  // イベント処理結果の記録
  const result = {
    event_id: event.event_id || `event_${Date.now()}`,
    event_type: event.event_type,
    target_id: event.target_id,
    processing_time: new Date().toISOString(),
    workflow_id: response.workflow_id,
    status: response.success ? 'processed' : 'failed',
    error: response.success ? null : response.error
  };
  
  // イベント処理結果の記録
  // （実際の実装ではデータベースやログへの記録が行われる）
  
  // サンプル実装（実際にはデータベース接続などが必要）
  console.log('Event processing result:', JSON.stringify(result, null, 2));
  
  return [
    {
      json: {
        success: true,
        event_processing_result: result
      }
    }
  ];
}

// 9. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなイベントベースの実行設定により、特定のイベントに基づいてコンセンサスモデルのワークフローを実行することができます。イベントの検証と分類、イベントタイプに基づく処理の分岐、各種イベント処理、分析の実行、結果の記録などの機能を含めることで、効果的なイベントベースのワークフロー実行を実現することができます。

これらのワークフロー管理機能により、コンセンサスモデルの全体プロセスを効率的に制御し、各コンポーネント間の連携をスムーズに行うことができます。n8nを活用することで、複雑なワークフローを視覚的に設計し、自動化することが可能になります。
