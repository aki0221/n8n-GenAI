### 7.2 パラメータ管理

コンセンサスモデルの管理コンポーネントにおけるパラメータ管理は、モデルの動作を制御し、柔軟性と再現性を確保するための重要な機能です。適切なパラメータ管理により、異なる状況や要件に応じてモデルの挙動を調整することができ、一貫性のある結果を得ることができます。n8nを活用することで、これらのパラメータを効率的に管理することが可能になります。

**パラメータの種類と構造**

コンセンサスモデルでは、様々な種類のパラメータが存在し、それぞれが異なる側面の動作を制御します。これらのパラメータを適切に構造化し、管理することが重要です。

**視点の重み付けパラメータ**:
テクノロジー視点、マーケット視点、ビジネス視点の各視点に対する重み付けを制御するパラメータです。これらの重みは、最終的なコンセンサススコアの計算に直接影響します。

```javascript
// 視点の重み付けパラメータの例
const perspectiveWeights = {
  technology: 0.33,  // テクノロジー視点の重み
  market: 0.33,      // マーケット視点の重み
  business: 0.34     // ビジネス視点の重み
};

// 重みの合計が1になることを検証
function validateWeights(weights) {
  const sum = Object.values(weights).reduce((total, weight) => total + weight, 0);
  const isValid = Math.abs(sum - 1) < 0.001; // 浮動小数点の誤差を考慮
  
  return {
    isValid,
    sum,
    message: isValid ? 'Weights are valid' : `Weights sum to ${sum}, expected 1`
  };
}

// 重みの調整（合計が1になるように正規化）
function normalizeWeights(weights) {
  const sum = Object.values(weights).reduce((total, weight) => total + weight, 0);
  
  if (Math.abs(sum - 1) < 0.001) {
    // すでに正規化されている場合はそのまま返す
    return weights;
  }
  
  // 各重みを合計で割って正規化
  const normalizedWeights = {};
  for (const [perspective, weight] of Object.entries(weights)) {
    normalizedWeights[perspective] = weight / sum;
  }
  
  return normalizedWeights;
}
```

**評価メトリクスパラメータ**:
各視点内の評価メトリクスとその重み付けを制御するパラメータです。これらのパラメータにより、各視点内での評価の詳細度と重点を調整することができます。

```javascript
// 評価メトリクスパラメータの例
const evaluationMetrics = {
  technology: [
    { id: 'tech_feasibility', name: '技術的実現可能性', weight: 0.25 },
    { id: 'innovation_level', name: 'イノベーションレベル', weight: 0.20 },
    { id: 'tech_maturity', name: '技術成熟度', weight: 0.20 },
    { id: 'implementation_complexity', name: '実装複雑性', weight: 0.15 },
    { id: 'scalability', name: 'スケーラビリティ', weight: 0.20 }
  ],
  market: [
    { id: 'market_size', name: '市場規模', weight: 0.20 },
    { id: 'growth_potential', name: '成長ポテンシャル', weight: 0.25 },
    { id: 'competition', name: '競合状況', weight: 0.20 },
    { id: 'customer_fit', name: '顧客ニーズとの適合性', weight: 0.35 }
  ],
  business: [
    { id: 'revenue_potential', name: '収益ポテンシャル', weight: 0.30 },
    { id: 'profitability', name: '収益性', weight: 0.25 },
    { id: 'strategic_fit', name: '戦略的適合性', weight: 0.25 },
    { id: 'resource_requirements', name: 'リソース要件', weight: 0.20 }
  ]
};

// 各視点内のメトリクス重みの検証
function validateMetricsWeights(metrics) {
  const result = {};
  
  for (const [perspective, metricsList] of Object.entries(metrics)) {
    const sum = metricsList.reduce((total, metric) => total + metric.weight, 0);
    const isValid = Math.abs(sum - 1) < 0.001; // 浮動小数点の誤差を考慮
    
    result[perspective] = {
      isValid,
      sum,
      message: isValid ? 'Weights are valid' : `Weights sum to ${sum}, expected 1`
    };
  }
  
  return result;
}

// メトリクス重みの調整（各視点内で合計が1になるように正規化）
function normalizeMetricsWeights(metrics) {
  const normalizedMetrics = {};
  
  for (const [perspective, metricsList] of Object.entries(metrics)) {
    const sum = metricsList.reduce((total, metric) => total + metric.weight, 0);
    
    if (Math.abs(sum - 1) < 0.001) {
      // すでに正規化されている場合はそのまま設定
      normalizedMetrics[perspective] = metricsList;
    } else {
      // 各メトリクスの重みを合計で割って正規化
      normalizedMetrics[perspective] = metricsList.map(metric => ({
        ...metric,
        weight: metric.weight / sum
      }));
    }
  }
  
  return normalizedMetrics;
}
```

**閾値パラメータ**:
コンセンサスモデルの様々な判断や分類に使用される閾値を制御するパラメータです。これらの閾値により、評価結果の解釈や推奨事項の生成方法が決定されます。

```javascript
// 閾値パラメータの例
const thresholdParameters = {
  consensus: {
    high: 0.8,    // 高コンセンサス閾値
    medium: 0.6,  // 中コンセンサス閾値
    low: 0.4      // 低コンセンサス閾値
  },
  contradiction: {
    severe: 0.4,  // 深刻な矛盾閾値
    moderate: 0.3, // 中程度の矛盾閾値
    mild: 0.2     // 軽度の矛盾閾値
  },
  recommendation: {
    strong: 0.75, // 強い推奨閾値
    moderate: 0.6, // 中程度の推奨閾値
    weak: 0.5     // 弱い推奨閾値
  },
  risk: {
    high: 0.7,    // 高リスク閾値
    medium: 0.5,  // 中リスク閾値
    low: 0.3      // 低リスク閾値
  }
};

// 閾値の検証（順序関係の確認）
function validateThresholds(thresholds) {
  const result = {};
  
  // コンセンサス閾値の検証
  const consensus = thresholds.consensus;
  result.consensus = {
    isValid: consensus.high > consensus.medium && consensus.medium > consensus.low,
    message: consensus.high > consensus.medium && consensus.medium > consensus.low
      ? 'Consensus thresholds are valid'
      : 'Consensus thresholds must satisfy: high > medium > low'
  };
  
  // 矛盾閾値の検証
  const contradiction = thresholds.contradiction;
  result.contradiction = {
    isValid: contradiction.severe > contradiction.moderate && contradiction.moderate > contradiction.mild,
    message: contradiction.severe > contradiction.moderate && contradiction.moderate > contradiction.mild
      ? 'Contradiction thresholds are valid'
      : 'Contradiction thresholds must satisfy: severe > moderate > mild'
  };
  
  // 推奨閾値の検証
  const recommendation = thresholds.recommendation;
  result.recommendation = {
    isValid: recommendation.strong > recommendation.moderate && recommendation.moderate > recommendation.weak,
    message: recommendation.strong > recommendation.moderate && recommendation.moderate > recommendation.weak
      ? 'Recommendation thresholds are valid'
      : 'Recommendation thresholds must satisfy: strong > moderate > weak'
  };
  
  // リスク閾値の検証
  const risk = thresholds.risk;
  result.risk = {
    isValid: risk.high > risk.medium && risk.medium > risk.low,
    message: risk.high > risk.medium && risk.medium > risk.low
      ? 'Risk thresholds are valid'
      : 'Risk thresholds must satisfy: high > medium > low'
  };
  
  // 全体の検証結果
  result.overall = {
    isValid: result.consensus.isValid && result.contradiction.isValid && 
             result.recommendation.isValid && result.risk.isValid,
    message: result.consensus.isValid && result.contradiction.isValid && 
             result.recommendation.isValid && result.risk.isValid
      ? 'All thresholds are valid'
      : 'Some thresholds are invalid'
  };
  
  return result;
}
```

**アルゴリズムパラメータ**:
コンセンサス形成アルゴリズムの動作を制御するパラメータです。これらのパラメータにより、視点間の矛盾の検出方法や解消方法が決定されます。

```javascript
// アルゴリズムパラメータの例
const algorithmParameters = {
  consensus_formation: {
    method: 'weighted_average', // コンセンサス形成方法（weighted_average, delphi, ahp）
    iterations: 3,              // 反復回数（デルファイ法の場合）
    convergence_threshold: 0.05, // 収束閾値
    min_agreement_level: 0.7    // 最小合意レベル
  },
  contradiction_resolution: {
    detection_method: 'variance', // 矛盾検出方法（variance, pairwise, clustering）
    resolution_strategy: 'weighted_adjustment', // 解消戦略（weighted_adjustment, expert_override, compromise）
    max_adjustment: 0.2         // 最大調整量
  },
  sensitivity_analysis: {
    method: 'monte_carlo',      // 感度分析方法（monte_carlo, one_at_a_time, factorial）
    samples: 1000,              // サンプル数（モンテカルロ法の場合）
    variation_range: 0.1        // 変動範囲
  }
};

// アルゴリズムパラメータの検証
function validateAlgorithmParameters(params) {
  const result = {};
  
  // コンセンサス形成パラメータの検証
  const consensusFormation = params.consensus_formation;
  result.consensus_formation = {
    isValid: true,
    messages: []
  };
  
  // 方法の検証
  const validMethods = ['weighted_average', 'delphi', 'ahp'];
  if (!validMethods.includes(consensusFormation.method)) {
    result.consensus_formation.isValid = false;
    result.consensus_formation.messages.push(`Invalid method: ${consensusFormation.method}. Must be one of: ${validMethods.join(', ')}`);
  }
  
  // 反復回数の検証
  if (consensusFormation.iterations < 1) {
    result.consensus_formation.isValid = false;
    result.consensus_formation.messages.push(`Invalid iterations: ${consensusFormation.iterations}. Must be at least 1`);
  }
  
  // 収束閾値の検証
  if (consensusFormation.convergence_threshold <= 0 || consensusFormation.convergence_threshold >= 1) {
    result.consensus_formation.isValid = false;
    result.consensus_formation.messages.push(`Invalid convergence threshold: ${consensusFormation.convergence_threshold}. Must be between 0 and 1`);
  }
  
  // 最小合意レベルの検証
  if (consensusFormation.min_agreement_level <= 0 || consensusFormation.min_agreement_level >= 1) {
    result.consensus_formation.isValid = false;
    result.consensus_formation.messages.push(`Invalid min agreement level: ${consensusFormation.min_agreement_level}. Must be between 0 and 1`);
  }
  
  // 矛盾解消パラメータの検証（同様のパターン）
  // 感度分析パラメータの検証（同様のパターン）
  
  // 全体の検証結果
  result.overall = {
    isValid: result.consensus_formation.isValid, // 他のパラメータの検証結果も含める
    message: result.consensus_formation.isValid
      ? 'All algorithm parameters are valid'
      : 'Some algorithm parameters are invalid'
  };
  
  return result;
}
```

**パラメータの保存と読み込み**

コンセンサスモデルのパラメータを効率的に管理するためには、パラメータの保存と読み込みの仕組みが重要です。n8nでは、データベースやファイルシステムを活用してパラメータを永続化し、必要に応じて読み込むことができます。

**パラメータの保存**:
設定されたパラメータをデータベースやファイルに保存する機能を実装します。

```javascript
// パラメータの保存例（n8nワークフロー）

// 1. パラメータ保存トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/save",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. パラメータの検証（Functionノード）
function validateParameters(items) {
  const parameters = items[0].json.body;
  const errors = [];
  
  // パラメータセットIDの検証
  if (!parameters.parameter_set_id) {
    errors.push("Missing required field: parameter_set_id");
  }
  
  // 視点の重み付けパラメータの検証
  if (parameters.perspective_weights) {
    const weightValidation = validateWeights(parameters.perspective_weights);
    if (!weightValidation.isValid) {
      errors.push(`Invalid perspective weights: ${weightValidation.message}`);
    }
  }
  
  // 評価メトリクスパラメータの検証
  if (parameters.evaluation_metrics) {
    const metricsValidation = validateMetricsWeights(parameters.evaluation_metrics);
    for (const [perspective, result] of Object.entries(metricsValidation)) {
      if (!result.isValid) {
        errors.push(`Invalid metrics weights for ${perspective}: ${result.message}`);
      }
    }
  }
  
  // 閾値パラメータの検証
  if (parameters.thresholds) {
    const thresholdValidation = validateThresholds(parameters.thresholds);
    if (!thresholdValidation.overall.isValid) {
      for (const [category, result] of Object.entries(thresholdValidation)) {
        if (category !== 'overall' && !result.isValid) {
          errors.push(`Invalid thresholds for ${category}: ${result.message}`);
        }
      }
    }
  }
  
  // アルゴリズムパラメータの検証
  if (parameters.algorithm_parameters) {
    const algorithmValidation = validateAlgorithmParameters(parameters.algorithm_parameters);
    if (!algorithmValidation.overall.isValid) {
      for (const [category, result] of Object.entries(algorithmValidation)) {
        if (category !== 'overall' && !result.isValid) {
          result.messages.forEach(message => {
            errors.push(`Invalid algorithm parameter for ${category}: ${message}`);
          });
        }
      }
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
  
  // パラメータのメタデータを追加
  const parametersWithMetadata = {
    ...parameters,
    created_at: parameters.created_at || new Date().toISOString(),
    updated_at: new Date().toISOString(),
    version: parameters.version ? parameters.version + 1 : 1,
    is_default: parameters.is_default || false
  };
  
  return [
    {
      json: {
        success: true,
        parameters: parametersWithMetadata
      }
    }
  ];
}

// 3. パラメータの保存（PostgreSQLノード）
// 設定例
{
  "operation": "upsert",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "parameter_set_id, name, description, perspective_weights, evaluation_metrics, thresholds, algorithm_parameters, created_at, updated_at, version, is_default",
  "additionalFields": {},
  "primaryKey": "parameter_set_id"
}

// 4. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなパラメータの保存機能を実装することで、設定されたパラメータをデータベースに永続化することができます。パラメータの検証、メタデータの追加、データベースへの保存などの機能を含めることで、堅牢なパラメータ管理を実現することができます。

**パラメータの読み込み**:
保存されたパラメータをデータベースやファイルから読み込む機能を実装します。

```javascript
// パラメータの読み込み例（n8nワークフロー）

// 1. パラメータ読み込みトリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/load/:parameterSetId",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. パラメータの取得（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "*",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Webhook.json.params.parameterSetId }}'"
}

// 3. パラメータの処理（Functionノード）
function processParameters(items) {
  // データベースからの結果を取得
  const dbResult = items[0].json;
  
  // パラメータが見つからない場合
  if (!dbResult || dbResult.length === 0) {
    return [
      {
        json: {
          success: false,
          error: "Parameter set not found",
          parameter_set_id: items[0].params.parameterSetId
        }
      }
    ];
  }
  
  // パラメータを取得
  const parameters = dbResult[0];
  
  // JSONフィールドをパース（データベースの実装によっては不要）
  const parsedParameters = {
    ...parameters,
    perspective_weights: typeof parameters.perspective_weights === 'string'
      ? JSON.parse(parameters.perspective_weights)
      : parameters.perspective_weights,
    evaluation_metrics: typeof parameters.evaluation_metrics === 'string'
      ? JSON.parse(parameters.evaluation_metrics)
      : parameters.evaluation_metrics,
    thresholds: typeof parameters.thresholds === 'string'
      ? JSON.parse(parameters.thresholds)
      : parameters.thresholds,
    algorithm_parameters: typeof parameters.algorithm_parameters === 'string'
      ? JSON.parse(parameters.algorithm_parameters)
      : parameters.algorithm_parameters
  };
  
  return [
    {
      json: {
        success: true,
        parameters: parsedParameters
      }
    }
  ];
}

// 4. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなパラメータの読み込み機能を実装することで、保存されたパラメータをデータベースから取得することができます。パラメータの取得、JSONフィールドのパース、結果の返却などの機能を含めることで、効率的なパラメータ管理を実現することができます。

**デフォルトパラメータの管理**:
システム全体で使用されるデフォルトパラメータを管理する機能を実装します。

```javascript
// デフォルトパラメータの管理例（n8nワークフロー）

// 1. デフォルトパラメータ設定トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/set-default/:parameterSetId",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. パラメータの存在確認（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "parameter_set_id",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Webhook.json.params.parameterSetId }}'"
}

// 3. 存在確認の処理（Functionノード）
function checkParameterExists(items) {
  // データベースからの結果を取得
  const dbResult = items[0].json;
  
  // パラメータが見つからない場合
  if (!dbResult || dbResult.length === 0) {
    return [
      {
        json: {
          success: false,
          error: "Parameter set not found",
          parameter_set_id: items[0].params.parameterSetId
        }
      }
    ];
  }
  
  return [
    {
      json: {
        success: true,
        parameter_set_id: items[0].params.parameterSetId
      }
    }
  ];
}

// 4. 現在のデフォルトをリセット（PostgreSQLノード）
// 設定例
{
  "operation": "update",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "is_default",
  "additionalFields": {},
  "updateKey": "is_default",
  "where": "is_default = true",
  "value": "false"
}

// 5. 新しいデフォルトを設定（PostgreSQLノード）
// 設定例
{
  "operation": "update",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "is_default",
  "additionalFields": {},
  "updateKey": "is_default",
  "where": "parameter_set_id = '{{ $node.Function.json.parameter_set_id }}'",
  "value": "true"
}

// 6. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなデフォルトパラメータの管理機能を実装することで、システム全体で使用されるデフォルトパラメータを設定することができます。パラメータの存在確認、現在のデフォルトのリセット、新しいデフォルトの設定などの機能を含めることで、効率的なデフォルトパラメータ管理を実現することができます。

**パラメータのバージョン管理**

コンセンサスモデルのパラメータを効果的に管理するためには、パラメータのバージョン管理が重要です。これにより、パラメータの変更履歴を追跡し、必要に応じて以前のバージョンに戻すことができます。

**パラメータの履歴管理**:
パラメータの変更履歴を記録し、追跡するための機能を実装します。

```javascript
// パラメータの履歴管理例（n8nワークフロー）

// 1. パラメータ履歴取得トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/history/:parameterSetId",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. パラメータ履歴の取得（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameter_history",
  "columns": "*",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Webhook.json.params.parameterSetId }}'",
  "sort": "version DESC"
}

// 3. 履歴の処理（Functionノード）
function processParameterHistory(items) {
  // データベースからの結果を取得
  const dbResult = items[0].json;
  
  // 履歴が見つからない場合
  if (!dbResult || dbResult.length === 0) {
    return [
      {
        json: {
          success: false,
          error: "Parameter history not found",
          parameter_set_id: items[0].params.parameterSetId
        }
      }
    ];
  }
  
  // 履歴エントリを処理
  const historyEntries = dbResult.map(entry => {
    // JSONフィールドをパース（データベースの実装によっては不要）
    return {
      ...entry,
      parameter_data: typeof entry.parameter_data === 'string'
        ? JSON.parse(entry.parameter_data)
        : entry.parameter_data
    };
  });
  
  return [
    {
      json: {
        success: true,
        parameter_set_id: items[0].params.parameterSetId,
        history: historyEntries
      }
    }
  ];
}

// 4. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなパラメータの履歴管理機能を実装することで、パラメータの変更履歴を追跡することができます。履歴の取得、JSONフィールドのパース、結果の返却などの機能を含めることで、効率的なパラメータのバージョン管理を実現することができます。

**パラメータの復元**:
以前のバージョンのパラメータを復元するための機能を実装します。

```javascript
// パラメータの復元例（n8nワークフロー）

// 1. パラメータ復元トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/restore",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. 復元パラメータの検証（Functionノード）
function validateRestoreRequest(items) {
  const request = items[0].json.body;
  const errors = [];
  
  // パラメータセットIDの検証
  if (!request.parameter_set_id) {
    errors.push("Missing required field: parameter_set_id");
  }
  
  // バージョンの検証
  if (!request.version) {
    errors.push("Missing required field: version");
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
  
  return [
    {
      json: {
        success: true,
        parameter_set_id: request.parameter_set_id,
        version: request.version
      }
    }
  ];
}

// 3. 履歴からパラメータを取得（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameter_history",
  "columns": "*",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Function.json.parameter_set_id }}' AND version = {{ $node.Function.json.version }}"
}

// 4. 復元処理（Functionノード）
function processRestoration(items) {
  // データベースからの結果を取得
  const dbResult = items[0].json;
  
  // 履歴エントリが見つからない場合
  if (!dbResult || dbResult.length === 0) {
    return [
      {
        json: {
          success: false,
          error: "Parameter version not found",
          parameter_set_id: items[0].parameter_set_id,
          version: items[0].version
        }
      }
    ];
  }
  
  // 履歴エントリを取得
  const historyEntry = dbResult[0];
  
  // JSONフィールドをパース（データベースの実装によっては不要）
  const parameterData = typeof historyEntry.parameter_data === 'string'
    ? JSON.parse(historyEntry.parameter_data)
    : historyEntry.parameter_data;
  
  // 復元用のパラメータを作成
  const restoredParameters = {
    ...parameterData,
    restored_from_version: historyEntry.version,
    restored_at: new Date().toISOString(),
    version: null // 新しいバージョンは保存時に設定される
  };
  
  return [
    {
      json: {
        success: true,
        parameter_set_id: items[0].parameter_set_id,
        restored_from_version: historyEntry.version,
        parameters: restoredParameters
      }
    }
  ];
}

// 5. パラメータの保存（PostgreSQLノード）
// 設定例
{
  "operation": "update",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "perspective_weights, evaluation_metrics, thresholds, algorithm_parameters, updated_at, version, restored_from_version, restored_at",
  "additionalFields": {},
  "updateKey": "parameter_set_id",
  "where": "parameter_set_id = '{{ $node.Function1.json.parameter_set_id }}'",
  "value": "{{ $node.Function1.json.parameters }}"
}

// 6. 履歴の記録（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_parameter_history",
  "columns": "parameter_set_id, version, parameter_data, created_at, restored_from_version",
  "additionalFields": {}
}

// 7. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなパラメータの復元機能を実装することで、以前のバージョンのパラメータを復元することができます。復元リクエストの検証、履歴からのパラメータ取得、パラメータの保存、履歴の記録などの機能を含めることで、効率的なパラメータのバージョン管理を実現することができます。

**パラメータの比較**:
異なるバージョンのパラメータを比較するための機能を実装します。

```javascript
// パラメータの比較例（n8nワークフロー）

// 1. パラメータ比較トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/compare",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. 比較リクエストの検証（Functionノード）
function validateCompareRequest(items) {
  const request = items[0].json.body;
  const errors = [];
  
  // パラメータセットIDの検証
  if (!request.parameter_set_id) {
    errors.push("Missing required field: parameter_set_id");
  }
  
  // バージョンの検証
  if (!request.version_a) {
    errors.push("Missing required field: version_a");
  }
  
  if (!request.version_b) {
    errors.push("Missing required field: version_b");
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
  
  return [
    {
      json: {
        success: true,
        parameter_set_id: request.parameter_set_id,
        version_a: request.version_a,
        version_b: request.version_b
      }
    }
  ];
}

// 3. バージョンAのパラメータを取得（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameter_history",
  "columns": "*",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Function.json.parameter_set_id }}' AND version = {{ $node.Function.json.version_a }}"
}

// 4. バージョンBのパラメータを取得（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameter_history",
  "columns": "*",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Function.json.parameter_set_id }}' AND version = {{ $node.Function.json.version_b }}"
}

// 5. パラメータの比較（Functionノード）
function compareParameters(items) {
  // データベースからの結果を取得
  const versionAResult = items[0].json;
  const versionBResult = items[1].json;
  
  // いずれかのバージョンが見つからない場合
  if (!versionAResult || versionAResult.length === 0) {
    return [
      {
        json: {
          success: false,
          error: "Version A not found",
          parameter_set_id: items[0].parameter_set_id,
          version_a: items[0].version_a
        }
      }
    ];
  }
  
  if (!versionBResult || versionBResult.length === 0) {
    return [
      {
        json: {
          success: false,
          error: "Version B not found",
          parameter_set_id: items[0].parameter_set_id,
          version_b: items[0].version_b
        }
      }
    ];
  }
  
  // パラメータデータを取得
  const parameterA = typeof versionAResult[0].parameter_data === 'string'
    ? JSON.parse(versionAResult[0].parameter_data)
    : versionAResult[0].parameter_data;
  
  const parameterB = typeof versionBResult[0].parameter_data === 'string'
    ? JSON.parse(versionBResult[0].parameter_data)
    : versionBResult[0].parameter_data;
  
  // パラメータの差分を計算
  const differences = compareParameterObjects(parameterA, parameterB);
  
  return [
    {
      json: {
        success: true,
        parameter_set_id: items[0].parameter_set_id,
        version_a: items[0].version_a,
        version_b: items[0].version_b,
        differences: differences
      }
    }
  ];
}

// パラメータオブジェクトの比較
function compareParameterObjects(objA, objB) {
  const differences = {};
  
  // 視点の重み付けパラメータの比較
  if (objA.perspective_weights && objB.perspective_weights) {
    differences.perspective_weights = compareObjects(objA.perspective_weights, objB.perspective_weights);
  }
  
  // 評価メトリクスパラメータの比較
  if (objA.evaluation_metrics && objB.evaluation_metrics) {
    differences.evaluation_metrics = {};
    
    // 各視点のメトリクスを比較
    for (const perspective of ['technology', 'market', 'business']) {
      if (objA.evaluation_metrics[perspective] && objB.evaluation_metrics[perspective]) {
        differences.evaluation_metrics[perspective] = compareArrays(
          objA.evaluation_metrics[perspective],
          objB.evaluation_metrics[perspective],
          'id'
        );
      }
    }
  }
  
  // 閾値パラメータの比較
  if (objA.thresholds && objB.thresholds) {
    differences.thresholds = {};
    
    // 各カテゴリの閾値を比較
    for (const category of ['consensus', 'contradiction', 'recommendation', 'risk']) {
      if (objA.thresholds[category] && objB.thresholds[category]) {
        differences.thresholds[category] = compareObjects(objA.thresholds[category], objB.thresholds[category]);
      }
    }
  }
  
  // アルゴリズムパラメータの比較
  if (objA.algorithm_parameters && objB.algorithm_parameters) {
    differences.algorithm_parameters = {};
    
    // 各カテゴリのアルゴリズムパラメータを比較
    for (const category of ['consensus_formation', 'contradiction_resolution', 'sensitivity_analysis']) {
      if (objA.algorithm_parameters[category] && objB.algorithm_parameters[category]) {
        differences.algorithm_parameters[category] = compareObjects(
          objA.algorithm_parameters[category],
          objB.algorithm_parameters[category]
        );
      }
    }
  }
  
  return differences;
}

// オブジェクトの比較
function compareObjects(objA, objB) {
  const differences = {};
  
  // objAのプロパティを確認
  for (const key in objA) {
    if (objB[key] === undefined) {
      // objBに存在しないプロパティ
      differences[key] = {
        type: 'removed',
        value_a: objA[key],
        value_b: undefined
      };
    } else if (JSON.stringify(objA[key]) !== JSON.stringify(objB[key])) {
      // 値が異なるプロパティ
      differences[key] = {
        type: 'changed',
        value_a: objA[key],
        value_b: objB[key]
      };
    }
  }
  
  // objBのプロパティを確認（objAに存在しないもの）
  for (const key in objB) {
    if (objA[key] === undefined) {
      // objAに存在しないプロパティ
      differences[key] = {
        type: 'added',
        value_a: undefined,
        value_b: objB[key]
      };
    }
  }
  
  return differences;
}

// 配列の比較
function compareArrays(arrA, arrB, idField) {
  const differences = {
    added: [],
    removed: [],
    changed: []
  };
  
  // arrAの要素を確認
  for (const itemA of arrA) {
    const id = itemA[idField];
    const itemB = arrB.find(item => item[idField] === id);
    
    if (!itemB) {
      // arrBに存在しない要素
      differences.removed.push(itemA);
    } else if (JSON.stringify(itemA) !== JSON.stringify(itemB)) {
      // 値が異なる要素
      differences.changed.push({
        id: id,
        value_a: itemA,
        value_b: itemB
      });
    }
  }
  
  // arrBの要素を確認（arrAに存在しないもの）
  for (const itemB of arrB) {
    const id = itemB[idField];
    const itemA = arrA.find(item => item[idField] === id);
    
    if (!itemA) {
      // arrAに存在しない要素
      differences.added.push(itemB);
    }
  }
  
  return differences;
}

// 6. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなパラメータの比較機能を実装することで、異なるバージョンのパラメータを比較することができます。比較リクエストの検証、パラメータの取得、差分の計算、結果の返却などの機能を含めることで、効率的なパラメータのバージョン管理を実現することができます。

**パラメータのエクスポートとインポート**

コンセンサスモデルのパラメータを異なる環境間で共有するためには、パラメータのエクスポートとインポートの機能が重要です。これにより、開発環境から本番環境へのパラメータの移行や、バックアップの作成などが可能になります。

**パラメータのエクスポート**:
パラメータをJSONファイルとしてエクスポートする機能を実装します。

```javascript
// パラメータのエクスポート例（n8nワークフロー）

// 1. パラメータエクスポートトリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/export/:parameterSetId",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. パラメータの取得（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "*",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Webhook.json.params.parameterSetId }}'"
}

// 3. エクスポートデータの作成（Functionノード）
function createExportData(items) {
  // データベースからの結果を取得
  const dbResult = items[0].json;
  
  // パラメータが見つからない場合
  if (!dbResult || dbResult.length === 0) {
    return [
      {
        json: {
          success: false,
          error: "Parameter set not found",
          parameter_set_id: items[0].params.parameterSetId
        }
      }
    ];
  }
  
  // パラメータを取得
  const parameters = dbResult[0];
  
  // JSONフィールドをパース（データベースの実装によっては不要）
  const parsedParameters = {
    ...parameters,
    perspective_weights: typeof parameters.perspective_weights === 'string'
      ? JSON.parse(parameters.perspective_weights)
      : parameters.perspective_weights,
    evaluation_metrics: typeof parameters.evaluation_metrics === 'string'
      ? JSON.parse(parameters.evaluation_metrics)
      : parameters.evaluation_metrics,
    thresholds: typeof parameters.thresholds === 'string'
      ? JSON.parse(parameters.thresholds)
      : parameters.thresholds,
    algorithm_parameters: typeof parameters.algorithm_parameters === 'string'
      ? JSON.parse(parameters.algorithm_parameters)
      : parameters.algorithm_parameters
  };
  
  // エクスポートデータの作成
  const exportData = {
    export_format_version: "1.0",
    export_date: new Date().toISOString(),
    parameter_set: parsedParameters
  };
  
  return [
    {
      json: {
        success: true,
        export_data: exportData
      }
    }
  ];
}

// 4. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200,
  "responseHeaders": {
    "Content-Type": "application/json",
    "Content-Disposition": "attachment; filename=\"parameter_set_{{ $node.Webhook.json.params.parameterSetId }}.json\""
  }
}
```

このようなパラメータのエクスポート機能を実装することで、パラメータをJSONファイルとしてエクスポートすることができます。パラメータの取得、エクスポートデータの作成、ファイルとしての返却などの機能を含めることで、効率的なパラメータの共有を実現することができます。

**パラメータのインポート**:
JSONファイルからパラメータをインポートする機能を実装します。

```javascript
// パラメータのインポート例（n8nワークフロー）

// 1. パラメータインポートトリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/parameters/import",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. インポートデータの検証（Functionノード）
function validateImportData(items) {
  const importData = items[0].json.body;
  const errors = [];
  
  // エクスポート形式バージョンの検証
  if (!importData.export_format_version) {
    errors.push("Missing export format version");
  } else if (importData.export_format_version !== "1.0") {
    errors.push(`Unsupported export format version: ${importData.export_format_version}`);
  }
  
  // パラメータセットの検証
  if (!importData.parameter_set) {
    errors.push("Missing parameter set data");
  } else {
    // パラメータセットIDの検証
    if (!importData.parameter_set.parameter_set_id) {
      errors.push("Missing parameter set ID");
    }
    
    // 必須フィールドの検証
    const requiredFields = ['name', 'perspective_weights', 'evaluation_metrics', 'thresholds', 'algorithm_parameters'];
    for (const field of requiredFields) {
      if (!importData.parameter_set[field]) {
        errors.push(`Missing required field: ${field}`);
      }
    }
    
    // 視点の重み付けパラメータの検証
    if (importData.parameter_set.perspective_weights) {
      const weightValidation = validateWeights(importData.parameter_set.perspective_weights);
      if (!weightValidation.isValid) {
        errors.push(`Invalid perspective weights: ${weightValidation.message}`);
      }
    }
    
    // 評価メトリクスパラメータの検証
    if (importData.parameter_set.evaluation_metrics) {
      const metricsValidation = validateMetricsWeights(importData.parameter_set.evaluation_metrics);
      for (const [perspective, result] of Object.entries(metricsValidation)) {
        if (!result.isValid) {
          errors.push(`Invalid metrics weights for ${perspective}: ${result.message}`);
        }
      }
    }
    
    // 閾値パラメータの検証
    if (importData.parameter_set.thresholds) {
      const thresholdValidation = validateThresholds(importData.parameter_set.thresholds);
      if (!thresholdValidation.overall.isValid) {
        for (const [category, result] of Object.entries(thresholdValidation)) {
          if (category !== 'overall' && !result.isValid) {
            errors.push(`Invalid thresholds for ${category}: ${result.message}`);
          }
        }
      }
    }
    
    // アルゴリズムパラメータの検証
    if (importData.parameter_set.algorithm_parameters) {
      const algorithmValidation = validateAlgorithmParameters(importData.parameter_set.algorithm_parameters);
      if (!algorithmValidation.overall.isValid) {
        for (const [category, result] of Object.entries(algorithmValidation)) {
          if (category !== 'overall' && !result.isValid) {
            result.messages.forEach(message => {
              errors.push(`Invalid algorithm parameter for ${category}: ${message}`);
            });
          }
        }
      }
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
  
  // インポートオプションの取得
  const options = items[0].json.body.options || {};
  
  // パラメータセットの準備
  const parameterSet = {
    ...importData.parameter_set,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    version: 1,
    is_default: options.set_as_default || false,
    imported_at: new Date().toISOString(),
    import_source: options.import_source || 'manual'
  };
  
  // 既存のパラメータセットIDを上書きする場合
  if (options.overwrite_existing) {
    parameterSet.parameter_set_id = importData.parameter_set.parameter_set_id;
  } else {
    // 新しいパラメータセットIDを生成
    parameterSet.parameter_set_id = `${importData.parameter_set.parameter_set_id}_imported_${Date.now()}`;
    parameterSet.name = `${parameterSet.name} (Imported)`;
  }
  
  return [
    {
      json: {
        success: true,
        parameter_set: parameterSet,
        options: options
      }
    }
  ];
}

// 3. 既存パラメータの確認（PostgreSQLノード）
// 設定例
{
  "operation": "select",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "parameter_set_id",
  "additionalFields": {},
  "where": "parameter_set_id = '{{ $node.Function.json.parameter_set.parameter_set_id }}'"
}

// 4. インポート処理の決定（Functionノード）
function decideImportAction(items) {
  const parameterSet = items[0].json.parameter_set;
  const options = items[0].json.options;
  const existingResult = items[1].json;
  
  // 既存のパラメータセットが存在するか確認
  const exists = existingResult && existingResult.length > 0;
  
  // 上書きオプションの確認
  if (exists && !options.overwrite_existing) {
    return [
      {
        json: {
          success: false,
          error: "Parameter set already exists and overwrite_existing option is not set",
          parameter_set_id: parameterSet.parameter_set_id
        }
      }
    ];
  }
  
  // インポート操作の決定
  const operation = exists ? 'update' : 'insert';
  
  return [
    {
      json: {
        success: true,
        parameter_set: parameterSet,
        operation: operation,
        options: options
      }
    }
  ];
}

// 5. パラメータの保存（PostgreSQLノード - 条件分岐）
// 設定例（挿入の場合）
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "parameter_set_id, name, description, perspective_weights, evaluation_metrics, thresholds, algorithm_parameters, created_at, updated_at, version, is_default, imported_at, import_source",
  "additionalFields": {}
}

// 設定例（更新の場合）
{
  "operation": "update",
  "schema": "public",
  "table": "consensus_model_parameters",
  "columns": "name, description, perspective_weights, evaluation_metrics, thresholds, algorithm_parameters, updated_at, version, is_default, imported_at, import_source",
  "additionalFields": {},
  "updateKey": "parameter_set_id",
  "where": "parameter_set_id = '{{ $node.Function1.json.parameter_set.parameter_set_id }}'",
  "value": "{{ $node.Function1.json.parameter_set }}"
}

// 6. デフォルト設定の処理（条件分岐）
// デフォルトとして設定する場合は、現在のデフォルトをリセットする

// 7. 履歴の記録（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_parameter_history",
  "columns": "parameter_set_id, version, parameter_data, created_at, import_source",
  "additionalFields": {}
}

// 8. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなパラメータのインポート機能を実装することで、JSONファイルからパラメータをインポートすることができます。インポートデータの検証、既存パラメータの確認、インポート処理の決定、パラメータの保存、履歴の記録などの機能を含めることで、効率的なパラメータの共有を実現することができます。

これらのパラメータ管理機能により、コンセンサスモデルの動作を制御し、柔軟性と再現性を確保することができます。n8nを活用することで、これらのパラメータを効率的に管理することが可能になり、異なる状況や要件に応じてモデルの挙動を調整することができます。
