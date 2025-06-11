# 段階的実装ガイド：n8nによるコンセンサスモデルの実装

このガイドでは、n8nを使用したコンセンサスモデルの実装を、初心者から上級者まで段階的に進められるよう構成しています。各レベルに応じた実装ステップと拡張ポイントを示しています。

## 1. 初心者向け：基本プロトタイプの構築

### ステップ1: 環境準備
```
# n8nのインストール（Docker使用の場合）
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### ステップ2: 単一視点の基本ワークフロー作成

1. **データ収集ワークフロー**
   - HTTPリクエストノードでデータソースに接続
   - JSONノードでデータを整形
   - 出力をファイルに保存

```javascript
// HTTPリクエストノードの設定例
{
  "url": "https://api.example.com/data",
  "method": "GET",
  "authentication": "none"
}

// JSONノードの処理例
return {
  json: {
    processedData: items[0].json.data.map(item => ({
      id: item.id,
      value: item.value,
      timestamp: item.timestamp
    }))
  }
};
```

### ステップ3: 単一視点の評価ロジック追加

1. **基本評価ワークフロー**
   - 前ステップのデータを読み込み
   - Functionノードで単純な評価ロジックを実装
   - 結果をファイルに保存

```javascript
// 基本評価ロジック
return {
  json: {
    evaluationResults: items[0].json.processedData.map(item => ({
      id: item.id,
      value: item.value,
      score: item.value > 50 ? "高" : "低",
      confidence: 0.7
    }))
  }
};
```

### ステップ4: 基本的な可視化

1. **可視化ワークフロー**
   - 評価結果を読み込み
   - HTMLノードで簡易レポート生成
   - メールで送信またはファイルに保存

```javascript
// HTML生成の例
const results = items[0].json.evaluationResults;
let html = '<h1>評価結果</h1><table border="1">';
html += '<tr><th>ID</th><th>値</th><th>評価</th><th>確信度</th></tr>';

results.forEach(item => {
  html += `<tr><td>${item.id}</td><td>${item.value}</td><td>${item.score}</td><td>${item.confidence}</td></tr>`;
});

html += '</table>';

return {
  json: {
    html: html
  }
};
```

### 初心者向け拡張ポイント
- データソースを変更してみる（別のAPIやCSVファイルなど）
- 評価ロジックのパラメータを調整する
- レポート形式をカスタマイズする

## 2. 中級者向け：複数視点の統合と自動化

### ステップ1: 複数視点のワークフロー作成

1. **マスターワークフロー**
   - Scheduleノードで定期実行を設定
   - 複数の視点ワークフローを順次実行

2. **視点別ワークフロー**
   - 各視点ごとに専用のデータ収集・分析ロジックを実装
   - 共通フォーマットで結果を出力

```javascript
// 視点1: 技術的評価
const technicalEvaluation = items[0].json.data.map(item => ({
  id: item.id,
  perspective: "technical",
  score: calculateTechnicalScore(item),
  confidence: calculateConfidence(item.dataPoints)
}));

// 視点2: コスト評価
const costEvaluation = items[0].json.data.map(item => ({
  id: item.id,
  perspective: "cost",
  score: calculateCostScore(item),
  confidence: calculateConfidence(item.dataPoints)
}));

return {
  json: {
    evaluations: [...technicalEvaluation, ...costEvaluation]
  }
};

// スコア計算関数の例
function calculateTechnicalScore(item) {
  return (item.performance * 0.6 + item.reliability * 0.4);
}

function calculateCostScore(item) {
  return (100 - item.initialCost * 0.5 - item.maintenanceCost * 0.5);
}

function calculateConfidence(dataPoints) {
  return Math.min(1, dataPoints.length / 10);
}
```

### ステップ2: 視点統合ロジックの実装

1. **統合ワークフロー**
   - 各視点の評価結果を読み込み
   - Functionノードで重み付け統合ロジックを実装
   - 結果を保存

```javascript
// 視点統合ロジック
const evaluations = items[0].json.evaluations;
const perspectives = ["technical", "cost", "user"];
const weights = {"technical": 0.4, "cost": 0.3, "user": 0.3};

// IDごとにグループ化
const groupedById = {};
evaluations.forEach(eval => {
  if (!groupedById[eval.id]) {
    groupedById[eval.id] = {};
  }
  groupedById[eval.id][eval.perspective] = {
    score: eval.score,
    confidence: eval.confidence
  };
});

// 統合スコア計算
const integratedResults = Object.keys(groupedById).map(id => {
  const item = groupedById[id];
  let weightedSum = 0;
  let totalWeight = 0;
  
  perspectives.forEach(perspective => {
    if (item[perspective]) {
      const weight = weights[perspective] * item[perspective].confidence;
      weightedSum += item[perspective].score * weight;
      totalWeight += weight;
    }
  });
  
  const finalScore = totalWeight > 0 ? weightedSum / totalWeight : 0;
  
  return {
    id: id,
    integratedScore: finalScore,
    perspectiveScores: item,
    confidence: totalWeight / Object.keys(weights).reduce((sum, key) => sum + weights[key], 0)
  };
});

return {
  json: {
    integratedResults: integratedResults
  }
};
```

### ステップ3: 静止点検出の基本実装

1. **静止点検出ワークフロー**
   - 過去の統合結果と現在の結果を比較
   - 変化率が閾値以下なら静止点と判定

```javascript
// 静止点検出ロジック
const currentResults = items[0].json.integratedResults;
const previousResults = items[1].json.integratedResults || [];

const fixedPointThreshold = 0.05; // 5%以下の変化で静止点と判定
const fixedPoints = [];

currentResults.forEach(current => {
  const previous = previousResults.find(p => p.id === current.id);
  
  if (previous) {
    const changeRate = Math.abs((current.integratedScore - previous.integratedScore) / previous.integratedScore);
    
    if (changeRate <= fixedPointThreshold) {
      fixedPoints.push({
        id: current.id,
        score: current.integratedScore,
        isFixedPoint: true,
        changeRate: changeRate,
        confidence: current.confidence
      });
    }
  }
});

return {
  json: {
    fixedPoints: fixedPoints,
    nonFixedPoints: currentResults.filter(r => !fixedPoints.some(fp => fp.id === r.id))
  }
};
```

### 中級者向け拡張ポイント
- 視点の数を増やす
- 重み付けロジックを動的に調整する
- 静止点検出アルゴリズムを改良する
- エラーハンドリングを追加する

## 3. 上級者向け：完全なシステム構築と最適化

### ステップ1: 完全なオーケストレーション設計

1. **マスターオーケストレーションワークフロー**
   - 全体の実行フローを制御
   - エラーハンドリングとリトライロジック
   - パラメータ管理と最適化

```javascript
// マスターオーケストレーションの例
const workflowIds = {
  dataCollection: "123",
  perspectiveAnalysis: "456",
  integration: "789",
  fixedPointDetection: "012",
  visualization: "345"
};

const parameters = {
  weights: {"technical": 0.4, "cost": 0.3, "user": 0.3},
  thresholds: {
    fixedPoint: 0.05,
    confidence: 0.7,
    action: 0.8
  },
  retryCount: 3,
  retryDelay: 60000 // 1分
};

// ワークフロー実行関数
async function executeWorkflow(id, input) {
  let retries = 0;
  let success = false;
  let result;
  
  while (!success && retries < parameters.retryCount) {
    try {
      // n8n APIを使用してワークフロー実行
      const response = await n8n.executeWorkflow(id, input);
      result = response.data;
      success = true;
    } catch (error) {
      retries++;
      if (retries >= parameters.retryCount) {
        throw new Error(`Workflow ${id} execution failed after ${retries} attempts: ${error.message}`);
      }
      // リトライ前に待機
      await new Promise(resolve => setTimeout(resolve, parameters.retryDelay));
    }
  }
  
  return result;
}

// メイン実行フロー
try {
  // 1. データ収集
  const collectionResult = await executeWorkflow(workflowIds.dataCollection, {});
  
  // 2. 視点分析
  const analysisResult = await executeWorkflow(workflowIds.perspectiveAnalysis, {
    data: collectionResult.data
  });
  
  // 3. 統合
  const integrationResult = await executeWorkflow(workflowIds.integration, {
    evaluations: analysisResult.evaluations,
    weights: parameters.weights
  });
  
  // 4. 静止点検出
  const fixedPointResult = await executeWorkflow(workflowIds.fixedPointDetection, {
    currentResults: integrationResult.integratedResults,
    threshold: parameters.thresholds.fixedPoint
  });
  
  // 5. 可視化と出力
  const visualizationResult = await executeWorkflow(workflowIds.visualization, {
    fixedPoints: fixedPointResult.fixedPoints,
    nonFixedPoints: fixedPointResult.nonFixedPoints,
    thresholds: parameters.thresholds
  });
  
  return {
    json: {
      executionId: Date.now(),
      status: "success",
      results: {
        fixedPoints: fixedPointResult.fixedPoints,
        visualizationUrl: visualizationResult.reportUrl
      }
    }
  };
} catch (error) {
  // エラーログ記録
  await logError(error);
  
  return {
    json: {
      executionId: Date.now(),
      status: "error",
      error: error.message
    }
  };
}
```

### ステップ2: パフォーマンス最適化

1. **バッチ処理の実装**
   - 大量データを分割処理
   - 並列実行の活用

```javascript
// バッチ処理の実装例
const data = items[0].json.data;
const batchSize = 100;
const batches = [];

// データをバッチに分割
for (let i = 0; i < data.length; i += batchSize) {
  batches.push(data.slice(i, i + batchSize));
}

// 並列処理の準備
const processedBatches = [];
for (const batch of batches) {
  // 各バッチを別々のワークフローで処理
  const result = await executeWorkflow(workflowIds.batchProcessor, { batch });
  processedBatches.push(result.processedData);
}

// 結果を統合
const combinedResults = [].concat(...processedBatches);

return {
  json: {
    processedData: combinedResults
  }
};
```

2. **キャッシュ戦略の実装**
   - 頻繁に使用されるデータのキャッシュ
   - 計算結果の再利用

```javascript
// キャッシュ戦略の実装例
const cacheKey = generateCacheKey(items[0].json.request);
let result;

// キャッシュ確認
const cachedResult = await checkCache(cacheKey);
if (cachedResult) {
  // キャッシュヒット
  result = cachedResult;
} else {
  // キャッシュミス - 計算実行
  result = await performExpensiveCalculation(items[0].json.request);
  
  // キャッシュ保存
  await saveToCache(cacheKey, result, 3600); // 1時間有効
}

return {
  json: {
    result: result,
    fromCache: !!cachedResult
  }
};

// キャッシュキー生成関数
function generateCacheKey(request) {
  return `${request.type}_${JSON.stringify(request.parameters)}_${request.version || '1.0'}`;
}
```

### ステップ3: 高度なエラーハンドリングとロギング

1. **包括的なエラーハンドリング**
   - エラータイプ別の対応
   - グレースフルデグラデーション（機能低下時の対応）

```javascript
// 高度なエラーハンドリング
try {
  // メイン処理
  const result = await processData(items[0].json.data);
  return { json: { result } };
} catch (error) {
  // エラータイプ別の対応
  if (error.name === 'ConnectionError') {
    // 接続エラーの場合
    const cachedData = await getFallbackData();
    await logError('ConnectionError', error, 'Using cached data');
    return {
      json: {
        result: cachedData,
        warning: 'Using cached data due to connection error',
        errorDetails: error.message
      }
    };
  } else if (error.name === 'ValidationError') {
    // データ検証エラーの場合
    await logError('ValidationError', error, 'Attempting data repair');
    const repairedData = await repairData(items[0].json.data);
    const result = await processData(repairedData);
    return {
      json: {
        result: result,
        warning: 'Data was repaired before processing',
        errorDetails: error.message
      }
    };
  } else if (error.name === 'TimeoutError') {
    // タイムアウトエラーの場合
    await logError('TimeoutError', error, 'Retrying with simplified processing');
    const result = await processDataSimplified(items[0].json.data);
    return {
      json: {
        result: result,
        warning: 'Used simplified processing due to timeout',
        errorDetails: error.message
      }
    };
  } else {
    // その他のエラー
    await logError('UnhandledError', error);
    throw error; // 再スロー
  }
}
```

2. **詳細なロギングシステム**
   - 実行ステップごとのログ
   - パフォーマンスメトリクス収集

```javascript
// 詳細なロギングシステム
async function executeWithLogging(stepName, func, params) {
  const startTime = Date.now();
  const executionId = items[0].json.executionId || Date.now();
  
  // 開始ログ
  await logEvent({
    executionId,
    step: stepName,
    status: 'started',
    timestamp: new Date().toISOString(),
    params: JSON.stringify(params)
  });
  
  try {
    // 関数実行
    const result = await func(params);
    
    // 成功ログ
    const duration = Date.now() - startTime;
    await logEvent({
      executionId,
      step: stepName,
      status: 'completed',
      timestamp: new Date().toISOString(),
      duration,
      resultSize: JSON.stringify(result).length
    });
    
    return result;
  } catch (error) {
    // エラーログ
    const duration = Date.now() - startTime;
    await logEvent({
      executionId,
      step: stepName,
      status: 'error',
      timestamp: new Date().toISOString(),
      duration,
      error: error.message,
      stack: error.stack
    });
    
    throw error;
  }
}
```

### ステップ4: セキュリティ対策の実装

1. **データ保護**
   - 機密データのマスキング
   - 暗号化の適用

```javascript
// データ保護の実装例
function maskSensitiveData(data) {
  // ディープコピーを作成
  const maskedData = JSON.parse(JSON.stringify(data));
  
  // 機密フィールドをマスク
  const sensitiveFields = ['email', 'phone', 'address', 'creditCard'];
  
  function recursiveMask(obj) {
    if (!obj || typeof obj !== 'object') return;
    
    Object.keys(obj).forEach(key => {
      if (sensitiveFields.includes(key)) {
        if (typeof obj[key] === 'string') {
          // 文字列の場合はマスク
          const value = obj[key];
          if (key === 'email') {
            const parts = value.split('@');
            if (parts.length === 2) {
              obj[key] = `${parts[0].substring(0, 2)}***@${parts[1]}`;
            }
          } else if (key === 'creditCard') {
            obj[key] = `****-****-****-${value.slice(-4)}`;
          } else {
            obj[key] = `${value.substring(0, 2)}${'*'.repeat(value.length - 4)}${value.slice(-2)}`;
          }
        }
      } else if (typeof obj[key] === 'object') {
        // オブジェクトや配列の場合は再帰的に処理
        recursiveMask(obj[key]);
      }
    });
  }
  
  recursiveMask(maskedData);
  return maskedData;
}
```

2. **アクセス制御**
   - APIキー管理
   - 権限設定

```javascript
// アクセス制御の実装例
async function validateAccess(apiKey, requiredPermissions) {
  // APIキーの検証
  const keyInfo = await getApiKeyInfo(apiKey);
  
  if (!keyInfo) {
    throw new Error('Invalid API key');
  }
  
  if (keyInfo.expired) {
    throw new Error('API key has expired');
  }
  
  // 権限チェック
  const hasAllPermissions = requiredPermissions.every(
    permission => keyInfo.permissions.includes(permission)
  );
  
  if (!hasAllPermissions) {
    throw new Error('Insufficient permissions');
  }
  
  // アクセスログ記録
  await logAccess({
    apiKey: maskApiKey(apiKey),
    userId: keyInfo.userId,
    timestamp: new Date().toISOString(),
    permissions: requiredPermissions
  });
  
  return {
    userId: keyInfo.userId,
    permissions: keyInfo.permissions
  };
}

function maskApiKey(apiKey) {
  return `${apiKey.substring(0, 4)}${'*'.repeat(apiKey.length - 8)}${apiKey.slice(-4)}`;
}
```

### 上級者向け拡張ポイント
- 分散処理アーキテクチャの実装
- 機械学習モデルの統合
- リアルタイムモニタリングとアラート
- A/Bテストフレームワークの構築
- 自動パラメータ最適化の実装

## 実装ステップのまとめ

### 初心者レベル
1. 単一視点の基本ワークフロー作成
2. 単純な評価ロジック実装
3. 基本的な可視化

### 中級者レベル
1. 複数視点のワークフロー作成
2. 視点統合ロジックの実装
3. 静止点検出の基本実装
4. 基本的なエラーハンドリング

### 上級者レベル
1. 完全なオーケストレーション設計
2. パフォーマンス最適化（バッチ処理、キャッシュ）
3. 高度なエラーハンドリングとロギング
4. セキュリティ対策の実装
5. 分散処理と自動最適化
