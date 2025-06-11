### 6.2 APIインターフェース

コンセンサスモデルの出力コンポーネントにおけるAPIインターフェースは、分析結果や意思決定支援情報を外部システムやアプリケーションに提供するための重要な機能です。適切に設計されたAPIにより、コンセンサスモデルの機能を様々なビジネスプロセスやワークフローに統合することが可能になり、その価値を最大化することができます。n8nを活用することで、このAPIインターフェースを効率的かつ柔軟に実装することができます。

**RESTful APIの設計と実装**

コンセンサスモデルの機能を外部から利用可能にするためには、標準的かつ使いやすいRESTful APIの設計と実装が重要です。これにより、様々なクライアントやシステムからのアクセスが容易になります。

n8nでのRESTful APIの設計と実装方法としては、主にWebhookノードとFunctionノードが活用されます。以下に、具体的な実装例を示します：

**APIエンドポイントの実装**:
コンセンサスモデルの主要機能にアクセスするためのAPIエンドポイントを実装します。

```javascript
// APIエンドポイントの実装例（Webhookノード）
// 設定例
{
  "path": "consensus-model/api/v1/analyze",
  "responseMode": "responseNode",
  "options": {
    "allowedMethods": [
      "POST"
    ],
    "responseHeaders": {
      "Content-Type": "application/json"
    }
  }
}

// リクエスト処理の実装例（Functionノード）
function processAnalysisRequest(items) {
  // リクエストデータを取得
  const requestData = items[0].json.body;
  
  // リクエストの検証
  const validationResult = validateRequest(requestData);
  if (!validationResult.valid) {
    return [
      {
        json: {
          status: "error",
          code: 400,
          message: "Invalid request",
          details: validationResult.errors
        }
      }
    ];
  }
  
  // リクエストパラメータの抽出
  const {
    target_id,
    target_name,
    target_type,
    data_sources,
    analysis_options
  } = requestData;
  
  // 分析パラメータの準備
  const analysisParams = {
    target: {
      id: target_id,
      name: target_name,
      type: target_type
    },
    data_sources: data_sources || [],
    options: {
      perspectives: analysis_options?.perspectives || ["technology", "market", "business"],
      weights: analysis_options?.weights || {
        technology: 0.33,
        market: 0.33,
        business: 0.33
      },
      include_details: analysis_options?.include_details !== false,
      generate_report: analysis_options?.generate_report !== false,
      report_format: analysis_options?.report_format || "json"
    },
    request_id: generateRequestId(),
    timestamp: new Date().toISOString()
  };
  
  // 分析リクエストを返す
  return [
    {
      json: {
        status: "accepted",
        request_id: analysisParams.request_id,
        message: "Analysis request accepted",
        estimated_completion_time: estimateCompletionTime(analysisParams),
        analysis_params: analysisParams
      }
    }
  ];
}

// リクエストの検証
function validateRequest(requestData) {
  const errors = [];
  
  // 必須フィールドの検証
  if (!requestData.target_id) {
    errors.push("Missing required field: target_id");
  }
  
  if (!requestData.target_name) {
    errors.push("Missing required field: target_name");
  }
  
  if (!requestData.target_type) {
    errors.push("Missing required field: target_type");
  }
  
  // データソースの検証（存在する場合）
  if (requestData.data_sources) {
    if (!Array.isArray(requestData.data_sources)) {
      errors.push("data_sources must be an array");
    } else {
      // 各データソースの検証
      requestData.data_sources.forEach((source, index) => {
        if (!source.type) {
          errors.push(`data_sources[${index}]: Missing required field: type`);
        }
        
        if (!source.url && !source.data) {
          errors.push(`data_sources[${index}]: Either url or data must be provided`);
        }
      });
    }
  }
  
  // 分析オプションの検証（存在する場合）
  if (requestData.analysis_options) {
    // 視点の検証
    if (requestData.analysis_options.perspectives) {
      if (!Array.isArray(requestData.analysis_options.perspectives)) {
        errors.push("analysis_options.perspectives must be an array");
      } else {
        const validPerspectives = ["technology", "market", "business"];
        requestData.analysis_options.perspectives.forEach((perspective, index) => {
          if (!validPerspectives.includes(perspective)) {
            errors.push(`analysis_options.perspectives[${index}]: Invalid perspective: ${perspective}`);
          }
        });
      }
    }
    
    // 重みの検証
    if (requestData.analysis_options.weights) {
      const weights = requestData.analysis_options.weights;
      const validPerspectives = ["technology", "market", "business"];
      
      for (const [perspective, weight] of Object.entries(weights)) {
        if (!validPerspectives.includes(perspective)) {
          errors.push(`analysis_options.weights: Invalid perspective: ${perspective}`);
        }
        
        if (typeof weight !== 'number' || weight < 0 || weight > 1) {
          errors.push(`analysis_options.weights.${perspective}: Weight must be a number between 0 and 1`);
        }
      }
      
      // 重みの合計が1になるか検証
      const totalWeight = Object.values(weights).reduce((sum, weight) => sum + weight, 0);
      if (Math.abs(totalWeight - 1) > 0.001) {
        errors.push(`analysis_options.weights: Sum of weights must be 1, got ${totalWeight}`);
      }
    }
    
    // レポート形式の検証
    if (requestData.analysis_options.report_format) {
      const validFormats = ["json", "html", "markdown", "pdf"];
      if (!validFormats.includes(requestData.analysis_options.report_format)) {
        errors.push(`analysis_options.report_format: Invalid format: ${requestData.analysis_options.report_format}`);
      }
    }
  }
  
  return {
    valid: errors.length === 0,
    errors: errors
  };
}

// リクエストIDの生成
function generateRequestId() {
  return 'req_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

// 完了時間の推定
function estimateCompletionTime(params) {
  // データソース数、視点数、詳細度などに基づいて処理時間を推定
  const baseTime = 30; // 基本処理時間（秒）
  
  // データソースによる追加時間
  const dataSourceTime = params.data_sources.length * 10;
  
  // 視点数による追加時間
  const perspectiveTime = params.options.perspectives.length * 15;
  
  // 詳細度による追加時間
  const detailTime = params.options.include_details ? 30 : 0;
  
  // レポート生成による追加時間
  const reportTime = params.options.generate_report ? 20 : 0;
  
  // 合計処理時間（秒）
  const totalTime = baseTime + dataSourceTime + perspectiveTime + detailTime + reportTime;
  
  // 現在時刻に処理時間を加算
  const completionTime = new Date();
  completionTime.setSeconds(completionTime.getSeconds() + totalTime);
  
  return completionTime.toISOString();
}

// メイン処理
return processAnalysisRequest($input.all());
```

このようなAPIエンドポイントの実装により、外部システムやアプリケーションからコンセンサスモデルの分析機能を利用することができます。リクエストの検証、パラメータの抽出、処理時間の推定などの機能を含めることで、使いやすく堅牢なAPIを提供することができます。

**分析結果取得APIの実装**:
非同期処理された分析結果を取得するためのAPIエンドポイントを実装します。

```javascript
// 分析結果取得APIの実装例（Webhookノード）
// 設定例
{
  "path": "consensus-model/api/v1/results/:requestId",
  "responseMode": "responseNode",
  "options": {
    "allowedMethods": [
      "GET"
    ],
    "responseHeaders": {
      "Content-Type": "application/json"
    }
  }
}

// 結果取得処理の実装例（Functionノード）
async function getAnalysisResults(items) {
  // リクエストパラメータを取得
  const requestId = items[0].json.params.requestId;
  
  // リクエストIDの検証
  if (!requestId || !requestId.startsWith('req_')) {
    return [
      {
        json: {
          status: "error",
          code: 400,
          message: "Invalid request ID format",
          request_id: requestId
        }
      }
    ];
  }
  
  try {
    // 分析結果を取得
    const result = await fetchAnalysisResult(requestId);
    
    if (!result) {
      return [
        {
          json: {
            status: "error",
            code: 404,
            message: "Analysis result not found",
            request_id: requestId
          }
        }
      ];
    }
    
    // 処理状態に応じたレスポンスを返す
    if (result.status === 'processing') {
      return [
        {
          json: {
            status: "processing",
            message: "Analysis is still in progress",
            request_id: requestId,
            progress: result.progress || 0,
            estimated_completion_time: result.estimated_completion_time
          }
        }
      ];
    } else if (result.status === 'completed') {
      return [
        {
          json: {
            status: "completed",
            message: "Analysis completed successfully",
            request_id: requestId,
            completed_at: result.completed_at,
            results: formatResults(result.data, items[0].json.query.format)
          }
        }
      ];
    } else if (result.status === 'failed') {
      return [
        {
          json: {
            status: "failed",
            code: 500,
            message: "Analysis failed",
            request_id: requestId,
            error: result.error
          }
        }
      ];
    }
    
    // 未知の状態
    return [
      {
        json: {
          status: "unknown",
          code: 500,
          message: "Unknown analysis status",
          request_id: requestId
        }
      }
    ];
  } catch (error) {
    return [
      {
        json: {
          status: "error",
          code: 500,
          message: "Failed to retrieve analysis result",
          request_id: requestId,
          error: error.message
        }
      }
    ];
  }
}

// 分析結果の取得
async function fetchAnalysisResult(requestId) {
  // データベースやキャッシュから結果を取得
  // 実際の実装ではデータベースクエリやAPIコールが行われる
  
  // サンプル実装（実際にはデータベース接続などが必要）
  const results = {
    'req_sample123': {
      status: 'completed',
      completed_at: '2023-06-01T10:30:45Z',
      data: {
        target_id: 'target_001',
        target_name: 'サンプルプロジェクト',
        consensus_score: 0.78,
        perspective_scores: {
          technology: { score: 0.82, weight: 0.33 },
          market: { score: 0.75, weight: 0.33 },
          business: { score: 0.76, weight: 0.33 }
        },
        analysis_details: {
          technology: {
            metrics: [
              { name: '技術的実現可能性', score: 0.85, weight: 0.3 },
              { name: 'イノベーションレベル', score: 0.78, weight: 0.2 },
              { name: '技術成熟度', score: 0.80, weight: 0.2 },
              { name: '実装複雑性', score: 0.85, weight: 0.15 },
              { name: 'スケーラビリティ', score: 0.82, weight: 0.15 }
            ],
            summary: '技術的に実現可能性が高く、十分な成熟度を持っています。'
          },
          market: {
            metrics: [
              { name: '市場規模', score: 0.70, weight: 0.25 },
              { name: '成長ポテンシャル', score: 0.85, weight: 0.25 },
              { name: '競合状況', score: 0.65, weight: 0.2 },
              { name: '顧客ニーズとの適合性', score: 0.80, weight: 0.3 }
            ],
            summary: '成長ポテンシャルが高く、顧客ニーズとの適合性も良好です。'
          },
          business: {
            metrics: [
              { name: '収益ポテンシャル', score: 0.75, weight: 0.3 },
              { name: '収益性', score: 0.70, weight: 0.25 },
              { name: '戦略的適合性', score: 0.85, weight: 0.25 },
              { name: 'リソース要件', score: 0.75, weight: 0.2 }
            ],
            summary: '戦略的適合性が高く、適切な収益ポテンシャルを持っています。'
          }
        },
        consensus_process: {
          contradictions: {
            summary: '視点間の矛盾は少なく、全体的に整合性のある評価結果です。',
            details: []
          },
          formation: {
            summary: '各視点のスコアは比較的近く、自然なコンセンサスが形成されました。'
          }
        },
        recommendations: {
          summary: 'プロジェクトは全体的に有望であり、進行を推奨します。',
          actions: [
            { title: '技術検証の実施', description: '主要技術要素の検証を行い、実装上の課題を特定する', priority: '高' },
            { title: '市場調査の深堀り', description: '特定セグメントの顧客ニーズをより詳細に調査する', priority: '中' },
            { title: 'ビジネスモデルの精緻化', description: '収益構造をより詳細に検討し、収益性を向上させる', priority: '中' }
          ],
          risks: '競合状況の変化に注意が必要です。また、技術実装における複雑性の管理も重要な課題となります。'
        }
      }
    },
    'req_sample456': {
      status: 'processing',
      progress: 0.65,
      estimated_completion_time: '2023-06-01T11:15:00Z'
    },
    'req_sample789': {
      status: 'failed',
      error: 'データソースへの接続に失敗しました。'
    }
  };
  
  return results[requestId];
}

// 結果のフォーマット
function formatResults(data, format) {
  // デフォルトはJSONフォーマット
  if (!format || format === 'json') {
    return data;
  }
  
  // 簡易フォーマット（概要のみ）
  if (format === 'summary') {
    return {
      target_id: data.target_id,
      target_name: data.target_name,
      consensus_score: data.consensus_score,
      perspective_scores: data.perspective_scores,
      summary: {
        technology: data.analysis_details.technology.summary,
        market: data.analysis_details.market.summary,
        business: data.analysis_details.business.summary,
        overall: data.recommendations.summary
      },
      key_recommendations: data.recommendations.actions.map(action => ({
        title: action.title,
        priority: action.priority
      }))
    };
  }
  
  // 詳細フォーマット（すべての情報）
  if (format === 'detailed') {
    return data;
  }
  
  // メトリクスのみ
  if (format === 'metrics') {
    return {
      target_id: data.target_id,
      target_name: data.target_name,
      consensus_score: data.consensus_score,
      perspective_scores: data.perspective_scores,
      metrics: {
        technology: data.analysis_details.technology.metrics,
        market: data.analysis_details.market.metrics,
        business: data.analysis_details.business.metrics
      }
    };
  }
  
  // 推奨事項のみ
  if (format === 'recommendations') {
    return {
      target_id: data.target_id,
      target_name: data.target_name,
      consensus_score: data.consensus_score,
      recommendations: data.recommendations
    };
  }
  
  // 未知のフォーマットの場合はデフォルト（JSON）を返す
  return data;
}

// メイン処理
return getAnalysisResults($input.all());
```

このような分析結果取得APIの実装により、非同期処理された分析結果を外部システムやアプリケーションから取得することができます。処理状態の確認、結果のフォーマット指定、エラーハンドリングなどの機能を含めることで、使いやすく柔軟なAPIを提供することができます。

**バッチ処理APIの実装**:
複数の対象を一括で分析するためのバッチ処理APIを実装します。

```javascript
// バッチ処理APIの実装例（Webhookノード）
// 設定例
{
  "path": "consensus-model/api/v1/batch",
  "responseMode": "responseNode",
  "options": {
    "allowedMethods": [
      "POST"
    ],
    "responseHeaders": {
      "Content-Type": "application/json"
    }
  }
}

// バッチ処理の実装例（Functionノード）
function processBatchRequest(items) {
  // リクエストデータを取得
  const requestData = items[0].json.body;
  
  // リクエストの検証
  if (!requestData.targets || !Array.isArray(requestData.targets) || requestData.targets.length === 0) {
    return [
      {
        json: {
          status: "error",
          code: 400,
          message: "Invalid request: targets must be a non-empty array",
          details: []
        }
      }
    ];
  }
  
  // バッチサイズの制限チェック
  const maxBatchSize = 50;
  if (requestData.targets.length > maxBatchSize) {
    return [
      {
        json: {
          status: "error",
          code: 400,
          message: `Batch size exceeds maximum limit of ${maxBatchSize} targets`,
          details: []
        }
      }
    ];
  }
  
  // 共通のオプション設定
  const commonOptions = requestData.options || {};
  
  // 各ターゲットの検証と処理
  const validationErrors = [];
  const validTargets = [];
  
  requestData.targets.forEach((target, index) => {
    // 基本的な検証
    if (!target.id || !target.name || !target.type) {
      validationErrors.push({
        index: index,
        target_id: target.id || `unknown_${index}`,
        errors: ["Missing required fields: id, name, or type"]
      });
      return;
    }
    
    // 有効なターゲットを追加
    validTargets.push({
      id: target.id,
      name: target.name,
      type: target.type,
      data_sources: target.data_sources || [],
      options: { ...commonOptions, ...(target.options || {}) }
    });
  });
  
  // 検証エラーがある場合は処理を中止
  if (validationErrors.length > 0) {
    return [
      {
        json: {
          status: "error",
          code: 400,
          message: "Validation errors in batch targets",
          details: validationErrors
        }
      }
    ];
  }
  
  // バッチリクエストの作成
  const batchId = generateBatchId();
  const timestamp = new Date().toISOString();
  
  // 各ターゲットの処理リクエストを作成
  const targetRequests = validTargets.map(target => ({
    target_id: target.id,
    target_name: target.name,
    target_type: target.type,
    request_id: generateRequestId(),
    data_sources: target.data_sources,
    options: target.options,
    status: "queued",
    queued_at: timestamp
  }));
  
  // バッチ情報を返す
  return [
    {
      json: {
        status: "accepted",
        batch_id: batchId,
        message: `Batch request with ${targetRequests.length} targets accepted`,
        timestamp: timestamp,
        estimated_completion_time: estimateBatchCompletionTime(targetRequests),
        targets: targetRequests.map(req => ({
          target_id: req.target_id,
          target_name: req.target_name,
          request_id: req.request_id,
          status: req.status
        }))
      }
    }
  ];
}

// バッチIDの生成
function generateBatchId() {
  return 'batch_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

// リクエストIDの生成
function generateRequestId() {
  return 'req_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

// バッチ完了時間の推定
function estimateBatchCompletionTime(requests) {
  // 基本処理時間（秒）
  const baseTimePerTarget = 60;
  
  // 並列処理数
  const parallelProcessing = 5;
  
  // 合計ターゲット数
  const totalTargets = requests.length;
  
  // 必要なバッチ数
  const batchCount = Math.ceil(totalTargets / parallelProcessing);
  
  // 合計処理時間の推定（秒）
  const totalTime = batchCount * baseTimePerTarget;
  
  // 現在時刻に処理時間を加算
  const completionTime = new Date();
  completionTime.setSeconds(completionTime.getSeconds() + totalTime);
  
  return completionTime.toISOString();
}

// メイン処理
return processBatchRequest($input.all());
```

このようなバッチ処理APIの実装により、複数の対象を一括で分析することができます。バッチサイズの制限、共通オプションの設定、並列処理の考慮などの機能を含めることで、効率的かつ柔軟なバッチ処理を提供することができます。

**APIドキュメントの生成と提供**

APIを効果的に活用してもらうためには、明確で詳細なAPIドキュメントの提供が不可欠です。これにより、開発者は迅速かつ正確にAPIを理解し、統合することができます。

n8nでのAPIドキュメントの生成と提供方法としては、主にHTTPリクエストノードとTemplateノードが活用されます。以下に、具体的な実装例を示します：

**OpenAPI仕様の生成**:
標準的なOpenAPI（Swagger）仕様に基づくAPIドキュメントを生成します。

```javascript
// OpenAPI仕様の生成例（Functionノード）
function generateOpenAPISpec() {
  // OpenAPI仕様の基本情報
  const openApiSpec = {
    openapi: "3.0.0",
    info: {
      title: "コンセンサスモデルAPI",
      description: "コンセンサスモデルの分析機能を提供するRESTful API",
      version: "1.0.0",
      contact: {
        name: "APIサポートチーム",
        email: "api-support@example.com",
        url: "https://example.com/support"
      }
    },
    servers: [
      {
        url: "https://api.example.com/v1",
        description: "本番環境"
      },
      {
        url: "https://api-staging.example.com/v1",
        description: "ステージング環境"
      }
    ],
    paths: {
      "/consensus-model/api/v1/analyze": {
        post: {
          summary: "コンセンサスモデル分析の実行",
          description: "指定されたターゲットに対してコンセンサスモデル分析を実行します。",
          operationId: "analyzeTarget",
          tags: ["分析"],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  $ref: "#/components/schemas/AnalysisRequest"
                }
              }
            }
          },
          responses: {
            "202": {
              description: "分析リクエストが受け付けられました",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/AnalysisAccepted"
                  }
                }
              }
            },
            "400": {
              description: "無効なリクエスト",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/ErrorResponse"
                  }
                }
              }
            },
            "500": {
              description: "サーバーエラー",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/ErrorResponse"
                  }
                }
              }
            }
          }
        }
      },
      "/consensus-model/api/v1/results/{requestId}": {
        get: {
          summary: "分析結果の取得",
          description: "指定されたリクエストIDに対応する分析結果を取得します。",
          operationId: "getAnalysisResults",
          tags: ["結果"],
          parameters: [
            {
              name: "requestId",
              in: "path",
              required: true,
              schema: {
                type: "string"
              },
              description: "分析リクエストのID"
            },
            {
              name: "format",
              in: "query",
              required: false,
              schema: {
                type: "string",
                enum: ["json", "summary", "detailed", "metrics", "recommendations"]
              },
              description: "結果のフォーマット"
            }
          ],
          responses: {
            "200": {
              description: "分析結果が正常に取得されました",
              content: {
                "application/json": {
                  schema: {
                    oneOf: [
                      { $ref: "#/components/schemas/AnalysisCompleted" },
                      { $ref: "#/components/schemas/AnalysisProcessing" }
                    ]
                  }
                }
              }
            },
            "400": {
              description: "無効なリクエスト",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/ErrorResponse"
                  }
                }
              }
            },
            "404": {
              description: "分析結果が見つかりません",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/ErrorResponse"
                  }
                }
              }
            },
            "500": {
              description: "サーバーエラー",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/ErrorResponse"
                  }
                }
              }
            }
          }
        }
      },
      "/consensus-model/api/v1/batch": {
        post: {
          summary: "バッチ分析の実行",
          description: "複数のターゲットに対して一括でコンセンサスモデル分析を実行します。",
          operationId: "analyzeBatch",
          tags: ["バッチ処理"],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  $ref: "#/components/schemas/BatchRequest"
                }
              }
            }
          },
          responses: {
            "202": {
              description: "バッチリクエストが受け付けられました",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/BatchAccepted"
                  }
                }
              }
            },
            "400": {
              description: "無効なリクエスト",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/ErrorResponse"
                  }
                }
              }
            },
            "500": {
              description: "サーバーエラー",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/ErrorResponse"
                  }
                }
              }
            }
          }
        }
      }
    },
    components: {
      schemas: {
        AnalysisRequest: {
          type: "object",
          required: ["target_id", "target_name", "target_type"],
          properties: {
            target_id: {
              type: "string",
              description: "分析対象のID"
            },
            target_name: {
              type: "string",
              description: "分析対象の名前"
            },
            target_type: {
              type: "string",
              description: "分析対象のタイプ（例: project, product, technology）"
            },
            data_sources: {
              type: "array",
              description: "分析に使用するデータソースのリスト",
              items: {
                $ref: "#/components/schemas/DataSource"
              }
            },
            analysis_options: {
              $ref: "#/components/schemas/AnalysisOptions"
            }
          }
        },
        DataSource: {
          type: "object",
          required: ["type"],
          properties: {
            type: {
              type: "string",
              description: "データソースのタイプ（例: api, database, file）"
            },
            url: {
              type: "string",
              description: "データソースのURL（該当する場合）"
            },
            data: {
              type: "object",
              description: "直接提供されるデータ（URLが提供されない場合）"
            },
            credentials: {
              type: "object",
              description: "データソースへのアクセスに必要な認証情報"
            },
            options: {
              type: "object",
              description: "データソース固有のオプション"
            }
          }
        },
        AnalysisOptions: {
          type: "object",
          properties: {
            perspectives: {
              type: "array",
              description: "分析に含める視点のリスト",
              items: {
                type: "string",
                enum: ["technology", "market", "business"]
              }
            },
            weights: {
              type: "object",
              description: "各視点の重み（合計が1になるように設定）",
              properties: {
                technology: {
                  type: "number",
                  format: "float",
                  minimum: 0,
                  maximum: 1
                },
                market: {
                  type: "number",
                  format: "float",
                  minimum: 0,
                  maximum: 1
                },
                business: {
                  type: "number",
                  format: "float",
                  minimum: 0,
                  maximum: 1
                }
              }
            },
            include_details: {
              type: "boolean",
              description: "詳細な分析結果を含めるかどうか",
              default: true
            },
            generate_report: {
              type: "boolean",
              description: "レポートを生成するかどうか",
              default: true
            },
            report_format: {
              type: "string",
              description: "レポートのフォーマット",
              enum: ["json", "html", "markdown", "pdf"],
              default: "json"
            }
          }
        },
        AnalysisAccepted: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["accepted"],
              description: "リクエストのステータス"
            },
            request_id: {
              type: "string",
              description: "分析リクエストのID"
            },
            message: {
              type: "string",
              description: "ステータスメッセージ"
            },
            estimated_completion_time: {
              type: "string",
              format: "date-time",
              description: "推定完了時間"
            },
            analysis_params: {
              type: "object",
              description: "受け付けられた分析パラメータ"
            }
          }
        },
        AnalysisProcessing: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["processing"],
              description: "処理ステータス"
            },
            message: {
              type: "string",
              description: "ステータスメッセージ"
            },
            request_id: {
              type: "string",
              description: "分析リクエストのID"
            },
            progress: {
              type: "number",
              format: "float",
              minimum: 0,
              maximum: 1,
              description: "処理の進捗状況（0-1）"
            },
            estimated_completion_time: {
              type: "string",
              format: "date-time",
              description: "推定完了時間"
            }
          }
        },
        AnalysisCompleted: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["completed"],
              description: "処理ステータス"
            },
            message: {
              type: "string",
              description: "ステータスメッセージ"
            },
            request_id: {
              type: "string",
              description: "分析リクエストのID"
            },
            completed_at: {
              type: "string",
              format: "date-time",
              description: "完了時間"
            },
            results: {
              type: "object",
              description: "分析結果"
            }
          }
        },
        BatchRequest: {
          type: "object",
          required: ["targets"],
          properties: {
            targets: {
              type: "array",
              description: "分析対象のリスト",
              items: {
                $ref: "#/components/schemas/BatchTarget"
              }
            },
            options: {
              $ref: "#/components/schemas/AnalysisOptions",
              description: "すべてのターゲットに適用される共通オプション"
            }
          }
        },
        BatchTarget: {
          type: "object",
          required: ["id", "name", "type"],
          properties: {
            id: {
              type: "string",
              description: "分析対象のID"
            },
            name: {
              type: "string",
              description: "分析対象の名前"
            },
            type: {
              type: "string",
              description: "分析対象のタイプ"
            },
            data_sources: {
              type: "array",
              description: "分析に使用するデータソースのリスト",
              items: {
                $ref: "#/components/schemas/DataSource"
              }
            },
            options: {
              $ref: "#/components/schemas/AnalysisOptions",
              description: "このターゲット固有のオプション（共通オプションを上書き）"
            }
          }
        },
        BatchAccepted: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["accepted"],
              description: "リクエストのステータス"
            },
            batch_id: {
              type: "string",
              description: "バッチリクエストのID"
            },
            message: {
              type: "string",
              description: "ステータスメッセージ"
            },
            timestamp: {
              type: "string",
              format: "date-time",
              description: "リクエスト受付時間"
            },
            estimated_completion_time: {
              type: "string",
              format: "date-time",
              description: "推定完了時間"
            },
            targets: {
              type: "array",
              description: "バッチ内の各ターゲットの情報",
              items: {
                type: "object",
                properties: {
                  target_id: {
                    type: "string",
                    description: "ターゲットID"
                  },
                  target_name: {
                    type: "string",
                    description: "ターゲット名"
                  },
                  request_id: {
                    type: "string",
                    description: "個別の分析リクエストID"
                  },
                  status: {
                    type: "string",
                    description: "処理ステータス"
                  }
                }
              }
            }
          }
        },
        ErrorResponse: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["error", "failed"],
              description: "エラーステータス"
            },
            code: {
              type: "integer",
              description: "HTTPステータスコード"
            },
            message: {
              type: "string",
              description: "エラーメッセージ"
            },
            details: {
              type: "array",
              description: "詳細なエラー情報",
              items: {
                type: "string"
              }
            }
          }
        }
      }
    }
  };
  
  return [{ json: openApiSpec }];
}

// メイン処理
return generateOpenAPISpec();
```

このようなOpenAPI仕様の生成ロジックを実装することで、標準的なOpenAPI（Swagger）仕様に基づくAPIドキュメントを生成することができます。この仕様は、Swagger UIなどのツールで表示したり、クライアントコードの自動生成に利用したりすることができます。

**APIドキュメントページの提供**:
開発者向けのAPIドキュメントページを提供し、APIの使用方法を詳細に説明します。

```javascript
// APIドキュメントページの提供例（Webhookノード）
// 設定例
{
  "path": "consensus-model/api/docs",
  "responseMode": "responseNode",
  "options": {
    "allowedMethods": [
      "GET"
    ],
    "responseHeaders": {
      "Content-Type": "text/html"
    }
  }
}

// ドキュメントページの生成例（Templateノード）
const openApiSpec = $input.item.json;

// Swagger UIのHTMLテンプレート
const htmlTemplate = `
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>コンセンサスモデルAPI ドキュメント</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui.css" />
  <style>
    body {
      margin: 0;
      padding: 0;
    }
    .header {
      background-color: #2c3e50;
      color: white;
      padding: 20px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 24px;
    }
    .header p {
      margin: 10px 0 0;
      font-size: 16px;
    }
    .swagger-ui .topbar {
      display: none;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>コンセンサスモデルAPI ドキュメント</h1>
    <p>コンセンサスモデルの分析機能を提供するRESTful APIの使用方法</p>
  </div>
  
  <div id="swagger-ui"></div>
  
  <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      const ui = SwaggerUIBundle({
        spec: ${JSON.stringify(openApiSpec)},
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        docExpansion: "list",
        defaultModelsExpandDepth: 1,
        defaultModelExpandDepth: 1,
        syntaxHighlight: {
          activate: true,
          theme: "agate"
        }
      });
      
      window.ui = ui;
    };
  </script>
</body>
</html>
`;

return { html: htmlTemplate };
```

このようなAPIドキュメントページの提供ロジックを実装することで、開発者向けのインタラクティブなAPIドキュメントページを提供することができます。Swagger UIを活用することで、APIの仕様を視覚的に表示し、実際にAPIをテストすることも可能になります。

**コード例の提供**:
様々なプログラミング言語でのAPI利用例を提供し、開発者の統合作業を支援します。

```javascript
// コード例の提供例（Webhookノード）
// 設定例
{
  "path": "consensus-model/api/examples/:language",
  "responseMode": "responseNode",
  "options": {
    "allowedMethods": [
      "GET"
    ],
    "responseHeaders": {
      "Content-Type": "text/plain"
    }
  }
}

// コード例の生成例（Functionノード）
function generateCodeExample(items) {
  // リクエストパラメータを取得
  const language = items[0].json.params.language.toLowerCase();
  
  // サポートされている言語のリスト
  const supportedLanguages = ['javascript', 'python', 'java', 'csharp', 'php', 'ruby', 'go', 'curl'];
  
  // 言語が未指定または未サポートの場合はエラー
  if (!language || !supportedLanguages.includes(language)) {
    return [
      {
        json: {
          error: "Unsupported language",
          supported_languages: supportedLanguages
        },
        responseCode: 400
      }
    ];
  }
  
  // 言語に応じたコード例を生成
  let codeExample;
  
  switch (language) {
    case 'javascript':
      codeExample = generateJavaScriptExample();
      break;
    case 'python':
      codeExample = generatePythonExample();
      break;
    case 'java':
      codeExample = generateJavaExample();
      break;
    case 'csharp':
      codeExample = generateCSharpExample();
      break;
    case 'php':
      codeExample = generatePHPExample();
      break;
    case 'ruby':
      codeExample = generateRubyExample();
      break;
    case 'go':
      codeExample = generateGoExample();
      break;
    case 'curl':
      codeExample = generateCurlExample();
      break;
    default:
      codeExample = "Code example not available for this language.";
  }
  
  return [
    {
      json: codeExample,
      responseCode: 200
    }
  ];
}

// JavaScript例の生成
function generateJavaScriptExample() {
  return `// コンセンサスモデルAPI - JavaScript例

// 分析リクエストの送信
async function requestAnalysis() {
  const apiUrl = 'https://api.example.com/v1/consensus-model/api/v1/analyze';
  
  const requestData = {
    target_id: 'project_123',
    target_name: 'サンプルプロジェクト',
    target_type: 'project',
    data_sources: [
      {
        type: 'api',
        url: 'https://example.com/data/technology/project_123'
      },
      {
        type: 'api',
        url: 'https://example.com/data/market/project_123'
      },
      {
        type: 'api',
        url: 'https://example.com/data/business/project_123'
      }
    ],
    analysis_options: {
      perspectives: ['technology', 'market', 'business'],
      weights: {
        technology: 0.4,
        market: 0.3,
        business: 0.3
      },
      include_details: true,
      generate_report: true,
      report_format: 'json'
    }
  };
  
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'
      },
      body: JSON.stringify(requestData)
    });
    
    const result = await response.json();
    
    if (response.ok) {
      console.log('分析リクエスト送信成功:', result);
      return result.request_id;
    } else {
      console.error('分析リクエスト送信失敗:', result);
      throw new Error(result.message || '分析リクエストの送信に失敗しました');
    }
  } catch (error) {
    console.error('エラー:', error);
    throw error;
  }
}

// 分析結果の取得
async function getAnalysisResults(requestId, format = 'json') {
  const apiUrl = \`https://api.example.com/v1/consensus-model/api/v1/results/\${requestId}?format=\${format}\`;
  
  try {
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY'
      }
    });
    
    const result = await response.json();
    
    if (response.ok) {
      if (result.status === 'completed') {
        console.log('分析完了:', result);
        return result.results;
      } else if (result.status === 'processing') {
        console.log('処理中...', result.progress * 100, '%完了');
        return null;
      } else {
        console.error('予期しないステータス:', result);
        throw new Error(result.message || '予期しないステータスが返されました');
      }
    } else {
      console.error('分析結果取得失敗:', result);
      throw new Error(result.message || '分析結果の取得に失敗しました');
    }
  } catch (error) {
    console.error('エラー:', error);
    throw error;
  }
}

// ポーリングによる結果取得
async function pollForResults(requestId, interval = 5000, timeout = 300000) {
  const startTime = Date.now();
  
  while (Date.now() - startTime < timeout) {
    const results = await getAnalysisResults(requestId);
    
    if (results) {
      return results;
    }
    
    // 指定された間隔だけ待機
    await new Promise(resolve => setTimeout(resolve, interval));
  }
  
  throw new Error('タイムアウト: 分析結果の取得に失敗しました');
}

// 使用例
async function main() {
  try {
    // 分析リクエストを送信
    const requestId = await requestAnalysis();
    console.log('リクエストID:', requestId);
    
    // 結果が完了するまでポーリング
    const results = await pollForResults(requestId);
    console.log('分析結果:', results);
    
    // 結果の処理
    const consensusScore = results.consensus_score;
    console.log('コンセンサススコア:', consensusScore);
    
    // 推奨事項の表示
    if (results.recommendations && results.recommendations.actions) {
      console.log('推奨アクション:');
      results.recommendations.actions.forEach(action => {
        console.log(\`- \${action.title} (優先度: \${action.priority})\`);
        console.log(\`  \${action.description}\`);
      });
    }
  } catch (error) {
    console.error('処理中にエラーが発生しました:', error);
  }
}

main();
`;
}

// Python例の生成
function generatePythonExample() {
  return `# コンセンサスモデルAPI - Python例

import requests
import json
import time

# APIの設定
API_BASE_URL = 'https://api.example.com/v1'
API_KEY = 'YOUR_API_KEY'

# 分析リクエストの送信
def request_analysis():
    url = f'{API_BASE_URL}/consensus-model/api/v1/analyze'
    
    request_data = {
        'target_id': 'project_123',
        'target_name': 'サンプルプロジェクト',
        'target_type': 'project',
        'data_sources': [
            {
                'type': 'api',
                'url': 'https://example.com/data/technology/project_123'
            },
            {
                'type': 'api',
                'url': 'https://example.com/data/market/project_123'
            },
            {
                'type': 'api',
                'url': 'https://example.com/data/business/project_123'
            }
        ],
        'analysis_options': {
            'perspectives': ['technology', 'market', 'business'],
            'weights': {
                'technology': 0.4,
                'market': 0.3,
                'business': 0.3
            },
            'include_details': True,
            'generate_report': True,
            'report_format': 'json'
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    try:
        response = requests.post(url, headers=headers, json=request_data)
        response.raise_for_status()  # エラーレスポンスの場合は例外を発生
        
        result = response.json()
        print(f'分析リクエスト送信成功: {result}')
        return result.get('request_id')
    except requests.exceptions.RequestException as e:
        print(f'分析リクエスト送信失敗: {e}')
        if hasattr(e, 'response') and e.response is not None:
            print(f'エラーレスポンス: {e.response.text}')
        raise

# 分析結果の取得
def get_analysis_results(request_id, format='json'):
    url = f'{API_BASE_URL}/consensus-model/api/v1/results/{request_id}'
    params = {'format': format}
    
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('status') == 'completed':
            print('分析完了')
            return result.get('results')
        elif result.get('status') == 'processing':
            progress = result.get('progress', 0) * 100
            print(f'処理中... {progress:.1f}%完了')
            return None
        else:
            print(f'予期しないステータス: {result}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'分析結果取得失敗: {e}')
        if hasattr(e, 'response') and e.response is not None:
            print(f'エラーレスポンス: {e.response.text}')
        raise

# ポーリングによる結果取得
def poll_for_results(request_id, interval=5, timeout=300):
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        results = get_analysis_results(request_id)
        
        if results:
            return results
        
        # 指定された間隔だけ待機
        time.sleep(interval)
    
    raise TimeoutError('タイムアウト: 分析結果の取得に失敗しました')

# 使用例
def main():
    try:
        # 分析リクエストを送信
        request_id = request_analysis()
        print(f'リクエストID: {request_id}')
        
        # 結果が完了するまでポーリング
        results = poll_for_results(request_id)
        print(f'分析結果: {json.dumps(results, indent=2, ensure_ascii=False)}')
        
        # 結果の処理
        consensus_score = results.get('consensus_score')
        print(f'コンセンサススコア: {consensus_score}')
        
        # 推奨事項の表示
        recommendations = results.get('recommendations', {})
        actions = recommendations.get('actions', [])
        
        if actions:
            print('推奨アクション:')
            for action in actions:
                print(f"- {action.get('title')} (優先度: {action.get('priority')})")
                print(f"  {action.get('description')}")
    except Exception as e:
        print(f'処理中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
`;
}

// cURLの例の生成
function generateCurlExample() {
  return `# コンセンサスモデルAPI - cURL例

# 分析リクエストの送信
curl -X POST "https://api.example.com/v1/consensus-model/api/v1/analyze" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "target_id": "project_123",
    "target_name": "サンプルプロジェクト",
    "target_type": "project",
    "data_sources": [
      {
        "type": "api",
        "url": "https://example.com/data/technology/project_123"
      },
      {
        "type": "api",
        "url": "https://example.com/data/market/project_123"
      },
      {
        "type": "api",
        "url": "https://example.com/data/business/project_123"
      }
    ],
    "analysis_options": {
      "perspectives": ["technology", "market", "business"],
      "weights": {
        "technology": 0.4,
        "market": 0.3,
        "business": 0.3
      },
      "include_details": true,
      "generate_report": true,
      "report_format": "json"
    }
  }'

# 分析結果の取得
curl -X GET "https://api.example.com/v1/consensus-model/api/v1/results/req_abc123?format=json" \\
  -H "Authorization: Bearer YOUR_API_KEY"

# バッチ分析リクエストの送信
curl -X POST "https://api.example.com/v1/consensus-model/api/v1/batch" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "targets": [
      {
        "id": "project_123",
        "name": "サンプルプロジェクト1",
        "type": "project",
        "data_sources": [
          {
            "type": "api",
            "url": "https://example.com/data/technology/project_123"
          }
        ]
      },
      {
        "id": "project_456",
        "name": "サンプルプロジェクト2",
        "type": "project",
        "data_sources": [
          {
            "type": "api",
            "url": "https://example.com/data/technology/project_456"
          }
        ]
      }
    ],
    "options": {
      "perspectives": ["technology", "market", "business"],
      "weights": {
        "technology": 0.33,
        "market": 0.33,
        "business": 0.33
      }
    }
  }'
`;
}

// メイン処理
return generateCodeExample($input.all());
```

このようなコード例の提供ロジックを実装することで、様々なプログラミング言語でのAPI利用例を提供し、開発者の統合作業を支援することができます。実際のユースケースに基づいた具体的なコード例により、APIの使い方を直感的に理解することが可能になります。

これらのAPIインターフェースの実装により、コンセンサスモデルの機能を外部システムやアプリケーションに提供することができます。RESTful APIの設計と実装、APIドキュメントの生成と提供により、開発者は迅速かつ正確にコンセンサスモデルの機能を理解し、様々なビジネスプロセスやワークフローに統合することが可能になります。これにより、コンセンサスモデルの価値を最大化し、より広範な活用を促進することができます。
