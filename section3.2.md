### 3.2 データの前処理と構造化

収集したデータをそのまま分析に使用することは、多くの場合適切ではありません。データソースごとに形式や品質が異なり、ノイズや欠損値を含んでいることも少なくありません。データの前処理と構造化は、収集したデータを分析に適した形式に変換し、データ品質を確保するための重要なプロセスです。n8nを活用することで、効率的かつ再現性の高いデータ前処理パイプラインを構築することができます。

**データクレンジングの重要性と実装方法**

データクレンジングは、収集したデータからノイズや異常値を除去し、欠損値を適切に処理することで、分析の精度と信頼性を高めるプロセスです。不適切なデータクレンジングは、誤った分析結果や意思決定につながる可能性があります。

n8nでのデータクレンジング実装方法としては、主にFunctionノードが活用されます。以下に、一般的なデータクレンジングタスクとその実装例を示します：

**欠損値の処理**:
データ内の欠損値（null、undefined、空文字列など）を検出し、適切な方法で処理します。処理方法には、欠損値の除去、平均値や中央値での補完、前後の値からの補間などがあります。

```javascript
// 欠損値処理の実装例
function handleMissingValues(items, options = {}) {
  const defaultOptions = {
    numericStrategy: 'mean', // 'mean', 'median', 'remove', 'zero'
    categoricalStrategy: 'mode', // 'mode', 'remove', 'unknown'
    dateStrategy: 'previous', // 'previous', 'next', 'remove', 'now'
    textStrategy: 'remove' // 'remove', 'empty', 'unknown'
  };
  
  const config = { ...defaultOptions, ...options };
  const processedItems = [];
  
  // 数値フィールドの平均値、中央値、最頻値を計算（必要な場合）
  const stats = {};
  if (['mean', 'median'].includes(config.numericStrategy) || config.categoricalStrategy === 'mode') {
    stats.numericFields = {};
    stats.categoricalFields = {};
    
    // 統計情報を収集
    for (const item of items) {
      for (const [key, value] of Object.entries(item.json)) {
        if (value === null || value === undefined || value === '') continue;
        
        if (typeof value === 'number') {
          if (!stats.numericFields[key]) stats.numericFields[key] = [];
          stats.numericFields[key].push(value);
        } else if (typeof value === 'string' && !isDate(value)) {
          if (!stats.categoricalFields[key]) stats.categoricalFields[key] = {};
          stats.categoricalFields[key][value] = (stats.categoricalFields[key][value] || 0) + 1;
        }
      }
    }
    
    // 統計値を計算
    for (const [key, values] of Object.entries(stats.numericFields)) {
      if (config.numericStrategy === 'mean') {
        stats.numericFields[key] = values.reduce((sum, val) => sum + val, 0) / values.length;
      } else if (config.numericStrategy === 'median') {
        const sorted = [...values].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        stats.numericFields[key] = sorted.length % 2 === 0 
          ? (sorted[mid - 1] + sorted[mid]) / 2 
          : sorted[mid];
      }
    }
    
    // 最頻値を計算
    for (const [key, counts] of Object.entries(stats.categoricalFields)) {
      let maxCount = 0;
      let mode = '';
      for (const [value, count] of Object.entries(counts)) {
        if (count > maxCount) {
          maxCount = count;
          mode = value;
        }
      }
      stats.categoricalFields[key] = mode;
    }
  }
  
  // 各アイテムの欠損値を処理
  for (const item of items) {
    const processedItem = { json: { ...item.json } };
    let shouldRemove = false;
    
    for (const [key, value] of Object.entries(processedItem.json)) {
      if (value === null || value === undefined || value === '') {
        // フィールドの型に基づいて適切な戦略を適用
        if (typeof value === 'number' || (typeof value === 'string' && !isNaN(Number(value)))) {
          // 数値フィールド
          switch (config.numericStrategy) {
            case 'mean':
            case 'median':
              processedItem.json[key] = stats.numericFields[key] || 0;
              break;
            case 'zero':
              processedItem.json[key] = 0;
              break;
            case 'remove':
              shouldRemove = true;
              break;
          }
        } else if (typeof value === 'string' && isDate(value)) {
          // 日付フィールド
          switch (config.dateStrategy) {
            case 'now':
              processedItem.json[key] = new Date().toISOString();
              break;
            case 'previous':
              // 実際の実装では前のレコードの日付を使用
              processedItem.json[key] = new Date().toISOString();
              break;
            case 'next':
              // 実際の実装では次のレコードの日付を使用
              processedItem.json[key] = new Date().toISOString();
              break;
            case 'remove':
              shouldRemove = true;
              break;
          }
        } else if (typeof value === 'string') {
          // カテゴリカルフィールド
          switch (config.categoricalStrategy) {
            case 'mode':
              processedItem.json[key] = stats.categoricalFields[key] || 'unknown';
              break;
            case 'unknown':
              processedItem.json[key] = 'unknown';
              break;
            case 'remove':
              shouldRemove = true;
              break;
          }
        } else {
          // その他のフィールド（テキストなど）
          switch (config.textStrategy) {
            case 'empty':
              processedItem.json[key] = '';
              break;
            case 'unknown':
              processedItem.json[key] = 'unknown';
              break;
            case 'remove':
              shouldRemove = true;
              break;
          }
        }
      }
    }
    
    if (!shouldRemove) {
      processedItems.push(processedItem);
    }
  }
  
  return processedItems;
}

// 日付文字列かどうかを判定するヘルパー関数
function isDate(value) {
  if (typeof value !== 'string') return false;
  const date = new Date(value);
  return !isNaN(date.getTime());
}

// メイン処理
const options = {
  numericStrategy: 'mean',
  categoricalStrategy: 'mode',
  dateStrategy: 'previous',
  textStrategy: 'remove'
};

return handleMissingValues($input.all(), options);
```

このような欠損値処理ロジックを実装することで、データの完全性を確保しつつ、分析に適した形式に変換することができます。また、欠損値の処理方法はデータの性質や分析目的に応じて調整することが重要です。

**異常値の検出と修正**:
データ内の異常値（外れ値）を統計的手法で検出し、除去または修正します。一般的な異常値検出手法には、Z-スコア法、IQR（四分位範囲）法、DBSCAN（密度ベースクラスタリング）などがあります。

```javascript
// 異常値検出と修正の実装例
function detectAndHandleOutliers(items, options = {}) {
  const defaultOptions = {
    method: 'zscore', // 'zscore', 'iqr', 'percentile'
    threshold: 3.0, // Z-scoreの閾値
    iqrFactor: 1.5, // IQR法の係数
    percentileRange: [0.01, 0.99], // パーセンタイル範囲
    action: 'cap' // 'cap', 'remove', 'replace'
  };
  
  const config = { ...defaultOptions, ...options };
  const processedItems = [];
  
  // 数値フィールドを特定
  const numericFields = new Set();
  for (const item of items) {
    for (const [key, value] of Object.entries(item.json)) {
      if (typeof value === 'number') {
        numericFields.add(key);
      }
    }
  }
  
  // 各数値フィールドの統計情報を計算
  const stats = {};
  for (const field of numericFields) {
    const values = items.map(item => item.json[field]).filter(val => typeof val === 'number');
    
    // 基本統計量を計算
    const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);
    
    // IQR計算用にソート
    const sorted = [...values].sort((a, b) => a - b);
    const q1Index = Math.floor(sorted.length * 0.25);
    const q3Index = Math.floor(sorted.length * 0.75);
    const q1 = sorted[q1Index];
    const q3 = sorted[q3Index];
    const iqr = q3 - q1;
    
    // パーセンタイル計算
    const lowerPercentileIndex = Math.floor(sorted.length * config.percentileRange[0]);
    const upperPercentileIndex = Math.floor(sorted.length * config.percentileRange[1]);
    const lowerPercentile = sorted[lowerPercentileIndex];
    const upperPercentile = sorted[upperPercentileIndex];
    
    stats[field] = {
      mean,
      stdDev,
      q1,
      q3,
      iqr,
      lowerPercentile,
      upperPercentile,
      // 異常値の閾値を計算
      lowerThreshold: config.method === 'zscore' ? mean - config.threshold * stdDev :
                      config.method === 'iqr' ? q1 - config.iqrFactor * iqr :
                      lowerPercentile,
      upperThreshold: config.method === 'zscore' ? mean + config.threshold * stdDev :
                      config.method === 'iqr' ? q3 + config.iqrFactor * iqr :
                      upperPercentile
    };
  }
  
  // 各アイテムの異常値を処理
  for (const item of items) {
    const processedItem = { json: { ...item.json } };
    let shouldRemove = false;
    
    for (const field of numericFields) {
      const value = processedItem.json[field];
      if (typeof value !== 'number') continue;
      
      const fieldStats = stats[field];
      const isOutlier = value < fieldStats.lowerThreshold || value > fieldStats.upperThreshold;
      
      if (isOutlier) {
        switch (config.action) {
          case 'cap':
            // 閾値でキャップ
            processedItem.json[field] = Math.min(Math.max(value, fieldStats.lowerThreshold), fieldStats.upperThreshold);
            processedItem.json[`${field}_outlier`] = true;
            break;
          case 'replace':
            // 平均値で置換
            processedItem.json[field] = fieldStats.mean;
            processedItem.json[`${field}_outlier`] = true;
            break;
          case 'remove':
            shouldRemove = true;
            break;
        }
      }
    }
    
    if (!shouldRemove) {
      processedItems.push(processedItem);
    }
  }
  
  return processedItems;
}

// メイン処理
const options = {
  method: 'iqr',
  iqrFactor: 1.5,
  action: 'cap'
};

return detectAndHandleOutliers($input.all(), options);
```

このような異常値検出・処理ロジックを実装することで、データ内の外れ値による分析結果の歪みを防ぎ、より信頼性の高い分析が可能になります。また、異常値の定義や処理方法はデータの分布特性や分析目的に応じて調整することが重要です。

**データ形式の統一**:
異なるデータソースから収集したデータの形式（日付形式、数値表現、カテゴリ値など）を統一し、一貫性のあるデータセットを作成します。

n8nでのデータ形式統一の実装方法としては、主にSetノードが活用されます。Setノードを使用することで、フィールド名の変更、データ型の変換、フォーマットの統一などを行うことができます。

```javascript
// データ形式統一の実装例
function standardizeDataFormat(items) {
  return items.map(item => {
    const standardizedItem = { ...item.json };
    
    // 日付フィールドの形式統一
    if (standardizedItem.date) {
      standardizedItem.date = new Date(standardizedItem.date).toISOString().split('T')[0];
    }
    if (standardizedItem.timestamp) {
      standardizedItem.timestamp = new Date(standardizedItem.timestamp).toISOString();
    }
    
    // 数値フィールドの形式統一
    if (standardizedItem.revenue) {
      standardizedItem.revenue = typeof standardizedItem.revenue === 'string' 
        ? parseFloat(standardizedItem.revenue.replace(/[^0-9.-]+/g, '')) 
        : standardizedItem.revenue;
    }
    
    // カテゴリフィールドの正規化
    if (standardizedItem.status) {
      const status = standardizedItem.status.toLowerCase().trim();
      if (['active', 'enabled', 'on', 'yes', 'true', '1'].includes(status)) {
        standardizedItem.status = 'active';
      } else if (['inactive', 'disabled', 'off', 'no', 'false', '0'].includes(status)) {
        standardizedItem.status = 'inactive';
      } else {
        standardizedItem.status = 'unknown';
      }
    }
    
    // フィールド名の標準化
    if (standardizedItem.userName) {
      standardizedItem.user_name = standardizedItem.userName;
      delete standardizedItem.userName;
    }
    
    // 単位の統一（例：金額をすべて円に変換）
    if (standardizedItem.amount && standardizedItem.currency) {
      if (standardizedItem.currency === 'USD') {
        standardizedItem.amount = standardizedItem.amount * 110; // 簡易的な換算
        standardizedItem.currency = 'JPY';
      } else if (standardizedItem.currency === 'EUR') {
        standardizedItem.amount = standardizedItem.amount * 130; // 簡易的な換算
        standardizedItem.currency = 'JPY';
      }
    }
    
    return { json: standardizedItem };
  });
}

// メイン処理
return standardizeDataFormat($input.all());
```

このようなデータ形式統一ロジックを実装することで、異なるデータソースからのデータを一貫性のある形式に変換し、分析の正確性と効率性を高めることができます。

**データ変換の実装方法**

データ変換は、クレンジングされたデータを分析に最適な形式に変換するプロセスです。これには、特徴量の生成、データの集約、次元削減などが含まれます。適切なデータ変換は、分析の精度と効率を大幅に向上させることができます。

n8nでのデータ変換実装方法としては、主にFunctionノードが活用されます。以下に、一般的なデータ変換タスクとその実装例を示します：

**特徴量エンジニアリング**:
既存のデータから新しい特徴量（分析に有用な変数）を生成します。例えば、日付から曜日や月を抽出したり、テキストデータから単語頻度を計算したりします。

```javascript
// 特徴量エンジニアリングの実装例
function createFeatures(items) {
  return items.map(item => {
    const enhancedItem = { ...item.json };
    
    // 日付関連の特徴量
    if (enhancedItem.date) {
      const date = new Date(enhancedItem.date);
      enhancedItem.day_of_week = date.getDay(); // 0-6 (日-土)
      enhancedItem.month = date.getMonth() + 1; // 1-12
      enhancedItem.quarter = Math.ceil((date.getMonth() + 1) / 3); // 1-4
      enhancedItem.is_weekend = [0, 6].includes(date.getDay()); // 土日判定
      
      // 季節の特徴量
      const month = date.getMonth() + 1;
      if ([3, 4, 5].includes(month)) enhancedItem.season = 'spring';
      else if ([6, 7, 8].includes(month)) enhancedItem.season = 'summer';
      else if ([9, 10, 11].includes(month)) enhancedItem.season = 'autumn';
      else enhancedItem.season = 'winter';
    }
    
    // 数値データの変換
    if (typeof enhancedItem.age === 'number') {
      // 年齢層のカテゴリ化
      if (enhancedItem.age < 18) enhancedItem.age_group = 'under_18';
      else if (enhancedItem.age < 30) enhancedItem.age_group = '18_29';
      else if (enhancedItem.age < 50) enhancedItem.age_group = '30_49';
      else if (enhancedItem.age < 65) enhancedItem.age_group = '50_64';
      else enhancedItem.age_group = '65_plus';
      
      // Z-スコア正規化
      enhancedItem.age_normalized = (enhancedItem.age - 40) / 15; // 仮の平均40、標準偏差15
    }
    
    // 複数フィールドの組み合わせ特徴量
    if (enhancedItem.income && enhancedItem.expense) {
      enhancedItem.savings_ratio = enhancedItem.income > 0 
        ? (enhancedItem.income - enhancedItem.expense) / enhancedItem.income 
        : 0;
    }
    
    // テキストデータからの特徴量抽出
    if (enhancedItem.description) {
      const text = enhancedItem.description.toLowerCase();
      
      // 単語カウント
      enhancedItem.word_count = text.split(/\s+/).filter(word => word.length > 0).length;
      
      // 感情分析（簡易版）
      const positiveWords = ['good', 'great', 'excellent', 'positive', 'happy', 'satisfied'];
      const negativeWords = ['bad', 'poor', 'negative', 'unhappy', 'dissatisfied', 'problem'];
      
      let positiveCount = 0;
      let negativeCount = 0;
      
      positiveWords.forEach(word => {
        const regex = new RegExp(`\\b${word}\\b`, 'gi');
        const matches = text.match(regex);
        if (matches) positiveCount += matches.length;
      });
      
      negativeWords.forEach(word => {
        const regex = new RegExp(`\\b${word}\\b`, 'gi');
        const matches = text.match(regex);
        if (matches) negativeCount += matches.length;
      });
      
      enhancedItem.sentiment_score = positiveCount - negativeCount;
      enhancedItem.sentiment = enhancedItem.sentiment_score > 0 ? 'positive' : 
                              enhancedItem.sentiment_score < 0 ? 'negative' : 'neutral';
    }
    
    return { json: enhancedItem };
  });
}

// メイン処理
return createFeatures($input.all());
```

このような特徴量エンジニアリングを実装することで、生データから分析に有用な情報を抽出し、モデルの予測力や解釈可能性を向上させることができます。また、ドメイン知識を活用した特徴量設計は、分析の質を大きく左右する重要な要素です。

**データ集約と要約**:
詳細なデータを特定の基準（時間、カテゴリなど）で集約し、要約統計量（合計、平均、最大値など）を計算します。これにより、データの全体像を把握しやすくなります。

```javascript
// データ集約と要約の実装例
function aggregateData(items, groupByFields, aggregations) {
  // グループ化
  const groups = {};
  
  for (const item of items) {
    // グループキーを生成
    const groupKey = groupByFields.map(field => item.json[field]).join('|');
    
    if (!groups[groupKey]) {
      groups[groupKey] = {
        // グループ化フィールドの値を保持
        ...groupByFields.reduce((obj, field) => {
          obj[field] = item.json[field];
          return obj;
        }, {}),
        // 集計用の初期値
        _count: 0,
        _items: []
      };
    }
    
    groups[groupKey]._count++;
    groups[groupKey]._items.push(item.json);
  }
  
  // 各グループに対して集計処理を実行
  const results = Object.values(groups).map(group => {
    const result = { ...group };
    delete result._items; // 元のアイテムリストは削除
    
    // 指定された集計を実行
    for (const agg of aggregations) {
      const { field, operations } = agg;
      
      for (const op of operations) {
        switch (op) {
          case 'sum':
            result[`${field}_sum`] = group._items.reduce((sum, item) => 
              sum + (typeof item[field] === 'number' ? item[field] : 0), 0);
            break;
          case 'avg':
            const validValues = group._items.filter(item => typeof item[field] === 'number');
            result[`${field}_avg`] = validValues.length > 0 
              ? validValues.reduce((sum, item) => sum + item[field], 0) / validValues.length 
              : null;
            break;
          case 'min':
            result[`${field}_min`] = Math.min(...group._items
              .filter(item => typeof item[field] === 'number')
              .map(item => item[field]));
            break;
          case 'max':
            result[`${field}_max`] = Math.max(...group._items
              .filter(item => typeof item[field] === 'number')
              .map(item => item[field]));
            break;
          case 'count':
            result[`${field}_count`] = group._items.filter(item => item[field] !== undefined && item[field] !== null).length;
            break;
          case 'distinct':
            result[`${field}_distinct`] = [...new Set(group._items
              .filter(item => item[field] !== undefined && item[field] !== null)
              .map(item => item[field]))];
            break;
          case 'first':
            result[`${field}_first`] = group._items[0]?.[field];
            break;
          case 'last':
            result[`${field}_last`] = group._items[group._items.length - 1]?.[field];
            break;
        }
      }
    }
    
    return { json: result };
  });
  
  return results;
}

// メイン処理
const groupByFields = ['region', 'product_category'];
const aggregations = [
  { field: 'sales', operations: ['sum', 'avg', 'min', 'max'] },
  { field: 'customer_id', operations: ['count', 'distinct'] },
  { field: 'transaction_date', operations: ['first', 'last'] }
];

return aggregateData($input.all(), groupByFields, aggregations);
```

このようなデータ集約ロジックを実装することで、詳細なトランザクションデータから地域別・製品カテゴリ別の売上サマリーを生成するなど、分析に適した集約データを作成することができます。また、集約の粒度や集計関数はビジネス要件や分析目的に応じて柔軟に調整することが重要です。

**データ保存の実装方法**

前処理・変換されたデータは、後続の分析プロセスで利用するために適切な形式で保存する必要があります。データ保存の方法は、データ量、アクセス頻度、クエリパターンなどによって最適な選択が異なります。

n8nでのデータ保存実装方法としては、主にWriteノードとDatabaseノードが活用されます。以下に、一般的なデータ保存タスクとその実装例を示します：

**ファイルへの保存**:
処理済みデータをCSV、JSON、Excelなどの形式でファイルに保存します。これは、中間結果の保存や、他システムとのデータ交換に適しています。

```javascript
// ファイル保存の実装例（JSONファイル）
// 注: 実際の実装ではWriteノードを使用

// データを整形
const dataToSave = $input.all().map(item => item.json);

// メタデータを追加
const outputData = {
  metadata: {
    generated_at: new Date().toISOString(),
    record_count: dataToSave.length,
    source: 'n8n data processing workflow',
    version: '1.0'
  },
  data: dataToSave
};

// JSONとして整形
const jsonContent = JSON.stringify(outputData, null, 2);

// ファイルに書き込み
// 注: 実際の実装ではWriteノードがこの処理を行う
const fs = require('fs');
const filePath = '/path/to/processed_data.json';
fs.writeFileSync(filePath, jsonContent);

return [{ json: { success: true, file_path: filePath, record_count: dataToSave.length } }];
```

このようなファイル保存ロジックを実装することで、処理済みデータを構造化された形式で保存し、後続の分析プロセスや他システムとの連携に活用することができます。また、メタデータを含めることで、データの出所や生成時刻などの重要な情報も保持できます。

**データベースへの保存**:
処理済みデータをリレーショナルデータベース（PostgreSQL、MySQL）やNoSQLデータベース（MongoDB）に保存します。これは、構造化されたデータの永続化や、複雑なクエリによるデータ分析に適しています。

```javascript
// データベース保存の実装例（PostgreSQL）
// 注: 実際の実装ではDatabaseノードを使用

// データを整形
const recordsToInsert = $input.all().map(item => ({
  perspective: item.json.perspective,
  category: item.json.category,
  value: item.json.value,
  confidence: item.json.confidence,
  timestamp: item.json.timestamp || new Date().toISOString(),
  source: item.json.source,
  metadata: JSON.stringify(item.json.metadata || {})
}));

// バッチ処理のためにレコードを分割
const batchSize = 100;
const batches = [];
for (let i = 0; i < recordsToInsert.length; i += batchSize) {
  batches.push(recordsToInsert.slice(i, i + batchSize));
}

// 各バッチをデータベースに挿入
// 注: 実際の実装ではDatabaseノードがこの処理を行う
const results = [];
for (const batch of batches) {
  try {
    // PostgreSQLへの接続とデータ挿入
    const { Client } = require('pg');
    const client = new Client({
      host: $credentials.database.host,
      port: $credentials.database.port,
      database: $credentials.database.database,
      user: $credentials.database.user,
      password: $credentials.database.password
    });
    
    await client.connect();
    
    // トランザクション開始
    await client.query('BEGIN');
    
    // バッチ内の各レコードを挿入
    for (const record of batch) {
      const query = `
        INSERT INTO processed_data 
        (perspective, category, value, confidence, timestamp, source, metadata)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
      `;
      
      const values = [
        record.perspective,
        record.category,
        record.value,
        record.confidence,
        record.timestamp,
        record.source,
        record.metadata
      ];
      
      const res = await client.query(query, values);
      results.push({ id: res.rows[0].id, ...record });
    }
    
    // トランザクションコミット
    await client.query('COMMIT');
    
    // 接続終了
    await client.end();
  } catch (error) {
    console.log(`データベース挿入エラー: ${error.message}`);
    
    // エラー発生時はロールバック
    if (client) {
      await client.query('ROLLBACK');
      await client.end();
    }
    
    throw error;
  }
}

return results.map(result => ({ json: result }));
```

このようなデータベース保存ロジックを実装することで、処理済みデータを構造化された形式でデータベースに保存し、後続の分析プロセスでの柔軟なクエリや集計を可能にします。また、トランザクション処理やバッチ処理を活用することで、大量データの安全かつ効率的な保存が可能になります。

これらのデータ前処理と構造化の実装により、コンセンサスモデルは高品質なデータを基盤とした信頼性の高い分析を実現することができます。データの品質は分析結果の質を直接左右するため、適切なデータクレンジング、変換、保存のプロセスを設計・実装することが重要です。また、これらのプロセスは再現性と透明性を確保するために、明確に文書化し、必要に応じて調整できるようにすることが望ましいです。
