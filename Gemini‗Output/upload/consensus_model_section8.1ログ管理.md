### 8.1 ログ管理

コンセンサスモデルの管理コンポーネントにおけるログ管理は、システムの動作状況を監視し、問題の診断や性能の最適化を行うための重要な機能です。適切なログ管理により、システムの透明性が向上し、障害発生時の原因特定や復旧が容易になります。n8nを活用することで、これらのログを効率的に収集、保存、分析することが可能になります。

**ログの収集と構造化**

コンセンサスモデルの様々なコンポーネントから発生するログを効率的に収集し、構造化することが重要です。これにより、ログの検索や分析が容易になり、システムの状態を正確に把握することができます。

**ログレベルの定義**:
ログの重要度に応じたレベル分けを行い、適切な対応を可能にします。

```javascript
// ログレベルの定義例
const logLevels = {
  DEBUG: {
    value: 0,
    label: 'DEBUG',
    description: '開発時のデバッグ情報'
  },
  INFO: {
    value: 1,
    label: 'INFO',
    description: '通常の動作情報'
  },
  WARNING: {
    value: 2,
    label: 'WARNING',
    description: '潜在的な問題の警告'
  },
  ERROR: {
    value: 3,
    label: 'ERROR',
    description: 'エラー情報'
  },
  CRITICAL: {
    value: 4,
    label: 'CRITICAL',
    description: '重大なエラー情報'
  }
};

// 現在のログレベル設定（環境変数から取得するなど）
const currentLogLevel = logLevels.INFO;

// ログレベルに基づくフィルタリング
function shouldLog(level) {
  return level.value >= currentLogLevel.value;
}
```

**ログ構造の定義**:
一貫性のあるログ形式を定義し、ログの解析や検索を容易にします。

```javascript
// ログ構造の定義例
function createLogEntry(level, component, message, details = {}) {
  // ログレベルの検証
  if (!Object.values(logLevels).includes(level)) {
    level = logLevels.INFO;
  }
  
  // ログエントリの作成
  const logEntry = {
    timestamp: new Date().toISOString(),
    level: level.label,
    component: component,
    message: message,
    details: details,
    // 追加のコンテキスト情報
    context: {
      workflow_id: details.workflow_id || null,
      target_id: details.target_id || null,
      session_id: details.session_id || null,
      user_id: details.user_id || null,
      environment: process.env.NODE_ENV || 'development'
    }
  };
  
  return logEntry;
}
```

**ログ収集の実装**:
n8nワークフローの各ノードからログを収集し、一元管理するための仕組みを実装します。

```javascript
// ログ収集の実装例（n8nワークフロー）

// 1. ログ収集トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/logs",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. ログの検証と前処理（Functionノード）
function validateAndProcessLog(items) {
  const logData = items[0].json.body;
  const errors = [];
  
  // 必須フィールドの検証
  if (!logData.level) {
    errors.push("Missing required field: level");
  }
  
  if (!logData.component) {
    errors.push("Missing required field: component");
  }
  
  if (!logData.message) {
    errors.push("Missing required field: message");
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
  
  // ログレベルの正規化
  let normalizedLevel;
  switch (logData.level.toUpperCase()) {
    case 'DEBUG':
      normalizedLevel = logLevels.DEBUG.label;
      break;
    case 'INFO':
      normalizedLevel = logLevels.INFO.label;
      break;
    case 'WARNING':
    case 'WARN':
      normalizedLevel = logLevels.WARNING.label;
      break;
    case 'ERROR':
    case 'ERR':
      normalizedLevel = logLevels.ERROR.label;
      break;
    case 'CRITICAL':
    case 'FATAL':
      normalizedLevel = logLevels.CRITICAL.label;
      break;
    default:
      normalizedLevel = logLevels.INFO.label;
  }
  
  // タイムスタンプの設定
  const timestamp = logData.timestamp ? new Date(logData.timestamp) : new Date();
  
  // 正規化されたログエントリの作成
  const normalizedLogEntry = {
    timestamp: timestamp.toISOString(),
    level: normalizedLevel,
    component: logData.component,
    message: logData.message,
    details: logData.details || {},
    context: {
      workflow_id: logData.workflow_id || logData.details?.workflow_id || null,
      target_id: logData.target_id || logData.details?.target_id || null,
      session_id: logData.session_id || logData.details?.session_id || null,
      user_id: logData.user_id || logData.details?.user_id || null,
      environment: logData.environment || process.env.NODE_ENV || 'development'
    }
  };
  
  return [
    {
      json: {
        success: true,
        log_entry: normalizedLogEntry
      }
    }
  ];
}

// 3. ログの保存（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_logs",
  "columns": "timestamp, level, component, message, details, context",
  "additionalFields": {}
}

// 4. アラート条件の確認（Functionノード）
function checkAlertConditions(items) {
  const logEntry = items[0].json.log_entry;
  
  // アラート条件の定義
  const alertConditions = [
    {
      name: 'critical_error',
      condition: logEntry.level === logLevels.CRITICAL.label,
      message: `Critical error in ${logEntry.component}: ${logEntry.message}`,
      channel: 'email'
    },
    {
      name: 'repeated_errors',
      condition: logEntry.level === logLevels.ERROR.label && 
                 logEntry.details.repeat_count && 
                 logEntry.details.repeat_count > 5,
      message: `Repeated errors in ${logEntry.component}: ${logEntry.message} (${logEntry.details.repeat_count} times)`,
      channel: 'slack'
    },
    {
      name: 'workflow_failure',
      condition: logEntry.level === logLevels.ERROR.label && 
                 logEntry.component === 'workflow_manager' &&
                 logEntry.message.includes('workflow failed'),
      message: `Workflow failure: ${logEntry.context.workflow_id} for target ${logEntry.context.target_id}`,
      channel: 'dashboard'
    }
  ];
  
  // アラート条件のチェック
  const triggeredAlerts = alertConditions.filter(condition => condition.condition);
  
  // アラートがない場合は早期リターン
  if (triggeredAlerts.length === 0) {
    return [
      {
        json: {
          success: true,
          log_entry: logEntry,
          alerts: []
        }
      }
    ];
  }
  
  // アラート情報の作成
  const alerts = triggeredAlerts.map(alert => ({
    name: alert.name,
    message: alert.message,
    channel: alert.channel,
    log_entry: logEntry,
    created_at: new Date().toISOString()
  }));
  
  return [
    {
      json: {
        success: true,
        log_entry: logEntry,
        alerts: alerts
      }
    }
  ];
}

// 5. アラートの送信（条件分岐）
// アラートがある場合のみ実行

// 6. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなログ収集の実装により、コンセンサスモデルの各コンポーネントから発生するログを一元的に収集し、構造化することができます。ログの検証と前処理、保存、アラート条件の確認などの機能を含めることで、効率的なログ管理を実現することができます。

**ログの保存と保持**

収集したログを適切に保存し、必要に応じて参照できるようにすることが重要です。また、ログの肥大化を防ぐために、適切な保持ポリシーを設定する必要があります。

**ログストレージの設計**:
ログの種類や重要度に応じて、適切なストレージを選択し、効率的なアクセスを可能にします。

```javascript
// ログストレージの設計例（n8nワークフロー）

// 1. ログローテーションスケジュールトリガー（Cronノード）
// 設定例（毎日午前2時に実行）
{
  "triggerTimes": {
    "item": [
      {
        "mode": "everyDay"
      }
    ]
  },
  "cronExpression": "0 2 * * *"
}

// 2. ログローテーションの実行（Functionノード）
async function executeLogRotation() {
  // 現在の日時
  const now = new Date();
  
  // ログローテーションの設定
  const rotationConfig = {
    debug_logs: {
      retention_days: 7,
      archive: false
    },
    info_logs: {
      retention_days: 30,
      archive: true
    },
    warning_logs: {
      retention_days: 90,
      archive: true
    },
    error_logs: {
      retention_days: 365,
      archive: true
    },
    critical_logs: {
      retention_days: 730,
      archive: true
    }
  };
  
  // 各ログレベルの処理
  const results = {};
  
  for (const [logType, config] of Object.entries(rotationConfig)) {
    // 削除日時の計算
    const deleteBefore = new Date(now);
    deleteBefore.setDate(deleteBefore.getDate() - config.retention_days);
    
    // ログレベルの取得
    const logLevel = logType.split('_')[0].toUpperCase();
    
    try {
      // アーカイブが必要な場合
      if (config.archive) {
        // アーカイブ対象のログを取得
        const logsToArchive = await fetchLogsForArchive(logLevel, deleteBefore);
        
        // アーカイブの実行
        if (logsToArchive.length > 0) {
          await archiveLogs(logLevel, logsToArchive);
        }
      }
      
      // 古いログの削除
      const deleteResult = await deleteOldLogs(logLevel, deleteBefore);
      
      // 結果の記録
      results[logType] = {
        retention_days: config.retention_days,
        delete_before: deleteBefore.toISOString(),
        archived: config.archive ? true : false,
        archived_count: config.archive ? logsToArchive.length : 0,
        deleted_count: deleteResult.deleted_count
      };
    } catch (error) {
      // エラーの記録
      results[logType] = {
        error: error.message,
        retention_days: config.retention_days,
        delete_before: deleteBefore.toISOString()
      };
    }
  }
  
  return [
    {
      json: {
        success: true,
        rotation_date: now.toISOString(),
        results: results
      }
    }
  ];
}

// アーカイブ対象のログを取得
async function fetchLogsForArchive(logLevel, deleteBefore) {
  // データベースからアーカイブ対象のログを取得
  // （実際の実装ではデータベース接続などが必要）
  
  // サンプル実装
  console.log(`Fetching logs for archive: level=${logLevel}, before=${deleteBefore.toISOString()}`);
  return []; // 実際にはデータベースからのクエリ結果
}

// ログのアーカイブ
async function archiveLogs(logLevel, logs) {
  // ログのアーカイブ処理
  // （実際の実装ではファイル出力やクラウドストレージへの保存などが必要）
  
  // サンプル実装
  console.log(`Archiving ${logs.length} logs for level ${logLevel}`);
  return true;
}

// 古いログの削除
async function deleteOldLogs(logLevel, deleteBefore) {
  // データベースから古いログを削除
  // （実際の実装ではデータベース接続などが必要）
  
  // サンプル実装
  console.log(`Deleting logs: level=${logLevel}, before=${deleteBefore.toISOString()}`);
  return { deleted_count: 0 }; // 実際にはデータベースからの削除結果
}

// 3. ログローテーション結果の記録（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_log_rotations",
  "columns": "rotation_date, results",
  "additionalFields": {}
}
```

このようなログストレージの設計により、ログの種類や重要度に応じて適切な保存期間を設定し、効率的なストレージ管理を実現することができます。ログローテーションの実行、アーカイブ、古いログの削除などの機能を含めることで、ログの肥大化を防ぎつつ、必要なログを適切に保持することができます。

**ログの圧縮とアーカイブ**:
長期保存が必要なログを圧縮してアーカイブし、ストレージの効率化を図ります。

```javascript
// ログの圧縮とアーカイブ例（n8nワークフロー）

// 1. アーカイブ処理（Functionノード）
async function archiveLogsToFile(logs, logLevel, archiveDate) {
  // アーカイブファイル名の生成
  const dateStr = archiveDate.toISOString().split('T')[0];
  const fileName = `logs_${logLevel.toLowerCase()}_${dateStr}.json`;
  const filePath = `/path/to/archives/${fileName}`;
  
  // ログデータのJSON形式への変換
  const logData = JSON.stringify(logs, null, 2);
  
  // ファイルへの書き込み
  // （実際の実装ではファイルシステム操作が必要）
  
  // 圧縮処理
  // （実際の実装では圧縮ライブラリの使用が必要）
  
  // 圧縮ファイル名
  const compressedFileName = `${fileName}.gz`;
  const compressedFilePath = `/path/to/archives/${compressedFileName}`;
  
  // 圧縮結果の情報
  const archiveInfo = {
    original_file: filePath,
    compressed_file: compressedFilePath,
    log_level: logLevel,
    archive_date: archiveDate.toISOString(),
    log_count: logs.length,
    original_size: logData.length,
    compressed_size: 0, // 実際の圧縮サイズ
    compression_ratio: 0 // 圧縮率
  };
  
  return archiveInfo;
}

// 2. クラウドストレージへのアップロード（S3ノード）
// 設定例
{
  "operation": "upload",
  "bucket": "{{ $json.bucket_name }}",
  "fileName": "{{ $json.key }}",
  "filePath": "{{ $json.compressed_file }}",
  "options": {
    "region": "us-east-1",
    "storageClass": "STANDARD_IA"
  }
}

// 3. アーカイブ情報の記録（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_log_archives",
  "columns": "archive_date, log_level, log_count, original_size, compressed_size, compression_ratio, storage_location, storage_class",
  "additionalFields": {}
}
```

このようなログの圧縮とアーカイブ機能を実装することで、長期保存が必要なログを効率的に管理することができます。ログのJSON形式への変換、圧縮処理、クラウドストレージへのアップロード、アーカイブ情報の記録などの機能を含めることで、ストレージの効率化を図りつつ、必要に応じてログを参照できるようにすることができます。

**ログの検索と分析**

収集したログを効率的に検索し、分析することで、システムの動作状況を把握し、問題の診断や性能の最適化を行うことができます。

**ログ検索インターフェースの実装**:
ログを効率的に検索するためのインターフェースを実装します。

```javascript
// ログ検索インターフェースの実装例（n8nワークフロー）

// 1. ログ検索トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/logs/search",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. 検索パラメータの処理（Functionノード）
function processSearchParameters(items) {
  const query = items[0].json.query;
  
  // デフォルトのパラメータ
  const defaultParams = {
    level: null,
    component: null,
    start_date: null,
    end_date: null,
    message_contains: null,
    workflow_id: null,
    target_id: null,
    limit: 100,
    offset: 0,
    sort_by: 'timestamp',
    sort_order: 'desc'
  };
  
  // クエリパラメータのマージ
  const searchParams = { ...defaultParams };
  
  for (const [key, value] of Object.entries(query)) {
    if (key in searchParams && value !== undefined && value !== null && value !== '') {
      searchParams[key] = value;
    }
  }
  
  // 日付の処理
  if (searchParams.start_date) {
    try {
      searchParams.start_date = new Date(searchParams.start_date).toISOString();
    } catch (error) {
      searchParams.start_date = null;
    }
  }
  
  if (searchParams.end_date) {
    try {
      searchParams.end_date = new Date(searchParams.end_date).toISOString();
    } catch (error) {
      searchParams.end_date = null;
    }
  }
  
  // 数値パラメータの処理
  searchParams.limit = parseInt(searchParams.limit, 10);
  searchParams.offset = parseInt(searchParams.offset, 10);
  
  // 不正な値の修正
  if (isNaN(searchParams.limit) || searchParams.limit <= 0) {
    searchParams.limit = 100;
  }
  
  if (isNaN(searchParams.offset) || searchParams.offset < 0) {
    searchParams.offset = 0;
  }
  
  // ソート順の検証
  if (!['asc', 'desc'].includes(searchParams.sort_order.toLowerCase())) {
    searchParams.sort_order = 'desc';
  }
  
  // ソートフィールドの検証
  const validSortFields = ['timestamp', 'level', 'component'];
  if (!validSortFields.includes(searchParams.sort_by)) {
    searchParams.sort_by = 'timestamp';
  }
  
  return [
    {
      json: {
        search_params: searchParams
      }
    }
  ];
}

// 3. 検索クエリの構築（Functionノード）
function buildSearchQuery(items) {
  const params = items[0].json.search_params;
  
  // WHERE句の構築
  const whereClauses = [];
  const queryParams = [];
  
  // レベルによるフィルタリング
  if (params.level) {
    whereClauses.push(`level = $${queryParams.length + 1}`);
    queryParams.push(params.level);
  }
  
  // コンポーネントによるフィルタリング
  if (params.component) {
    whereClauses.push(`component = $${queryParams.length + 1}`);
    queryParams.push(params.component);
  }
  
  // 日付範囲によるフィルタリング
  if (params.start_date) {
    whereClauses.push(`timestamp >= $${queryParams.length + 1}`);
    queryParams.push(params.start_date);
  }
  
  if (params.end_date) {
    whereClauses.push(`timestamp <= $${queryParams.length + 1}`);
    queryParams.push(params.end_date);
  }
  
  // メッセージ内容によるフィルタリング
  if (params.message_contains) {
    whereClauses.push(`message ILIKE $${queryParams.length + 1}`);
    queryParams.push(`%${params.message_contains}%`);
  }
  
  // ワークフローIDによるフィルタリング
  if (params.workflow_id) {
    whereClauses.push(`context->>'workflow_id' = $${queryParams.length + 1}`);
    queryParams.push(params.workflow_id);
  }
  
  // ターゲットIDによるフィルタリング
  if (params.target_id) {
    whereClauses.push(`context->>'target_id' = $${queryParams.length + 1}`);
    queryParams.push(params.target_id);
  }
  
  // WHERE句の結合
  const whereClause = whereClauses.length > 0
    ? `WHERE ${whereClauses.join(' AND ')}`
    : '';
  
  // ORDER BY句の構築
  const orderByClause = `ORDER BY ${params.sort_by} ${params.sort_order}`;
  
  // LIMIT/OFFSET句の構築
  const limitOffsetClause = `LIMIT ${params.limit} OFFSET ${params.offset}`;
  
  // 完全なSQLクエリの構築
  const sqlQuery = `
    SELECT *
    FROM consensus_model_logs
    ${whereClause}
    ${orderByClause}
    ${limitOffsetClause}
  `;
  
  // カウントクエリの構築
  const countQuery = `
    SELECT COUNT(*) as total_count
    FROM consensus_model_logs
    ${whereClause}
  `;
  
  return [
    {
      json: {
        search_params: params,
        sql_query: sqlQuery,
        count_query: countQuery,
        query_params: queryParams
      }
    }
  ];
}

// 4. 総件数の取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.count_query }}",
  "additionalFields": {}
}

// 5. ログの検索（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.sql_query }}",
  "additionalFields": {}
}

// 6. 検索結果の処理（Functionノード）
function processSearchResults(items) {
  const searchParams = items[0].json.search_params;
  const countResult = items[1].json;
  const searchResult = items[2].json;
  
  // 総件数の取得
  const totalCount = countResult[0].total_count;
  
  // ページネーション情報の計算
  const currentPage = Math.floor(searchParams.offset / searchParams.limit) + 1;
  const totalPages = Math.ceil(totalCount / searchParams.limit);
  const hasNextPage = currentPage < totalPages;
  const hasPreviousPage = currentPage > 1;
  
  // 次のページと前のページのオフセット
  const nextPageOffset = hasNextPage ? searchParams.offset + searchParams.limit : null;
  const previousPageOffset = hasPreviousPage ? Math.max(0, searchParams.offset - searchParams.limit) : null;
  
  // 検索結果の整形
  const formattedResults = searchResult.map(log => {
    // JSONフィールドのパース（データベースの実装によっては不要）
    return {
      ...log,
      details: typeof log.details === 'string' ? JSON.parse(log.details) : log.details,
      context: typeof log.context === 'string' ? JSON.parse(log.context) : log.context
    };
  });
  
  return [
    {
      json: {
        success: true,
        search_params: searchParams,
        pagination: {
          total_count: parseInt(totalCount, 10),
          total_pages: totalPages,
          current_page: currentPage,
          has_next_page: hasNextPage,
          has_previous_page: hasPreviousPage,
          next_page_offset: nextPageOffset,
          previous_page_offset: previousPageOffset
        },
        results: formattedResults
      }
    }
  ];
}

// 7. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなログ検索インターフェースの実装により、収集したログを効率的に検索することができます。検索パラメータの処理、検索クエリの構築、総件数の取得、ログの検索、検索結果の処理などの機能を含めることで、柔軟なログ検索を実現することができます。

**ログ分析ダッシュボードの実装**:
ログデータを視覚化し、システムの動作状況を一目で把握するためのダッシュボードを実装します。

```javascript
// ログ分析ダッシュボードの実装例（n8nワークフロー）

// 1. ダッシュボードデータ取得トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/logs/dashboard",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. 期間パラメータの処理（Functionノード）
function processTimeRangeParameters(items) {
  const query = items[0].json.query;
  
  // デフォルトの期間（過去24時間）
  let startDate = new Date();
  startDate.setHours(startDate.getHours() - 24);
  
  let endDate = new Date();
  
  // クエリパラメータからの期間指定
  if (query.time_range) {
    switch (query.time_range) {
      case 'hour':
        startDate = new Date();
        startDate.setHours(startDate.getHours() - 1);
        break;
      case 'day':
        startDate = new Date();
        startDate.setDate(startDate.getDate() - 1);
        break;
      case 'week':
        startDate = new Date();
        startDate.setDate(startDate.getDate() - 7);
        break;
      case 'month':
        startDate = new Date();
        startDate.setMonth(startDate.getMonth() - 1);
        break;
      case 'custom':
        if (query.start_date) {
          try {
            startDate = new Date(query.start_date);
          } catch (error) {
            // 無効な日付の場合はデフォルトを使用
          }
        }
        
        if (query.end_date) {
          try {
            endDate = new Date(query.end_date);
          } catch (error) {
            // 無効な日付の場合はデフォルトを使用
          }
        }
        break;
    }
  }
  
  return [
    {
      json: {
        time_range: query.time_range || 'day',
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString()
      }
    }
  ];
}

// 3. ログレベル別の集計（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT level, COUNT(*) as count FROM consensus_model_logs WHERE timestamp BETWEEN '{{ $json.start_date }}' AND '{{ $json.end_date }}' GROUP BY level ORDER BY CASE level WHEN 'CRITICAL' THEN 1 WHEN 'ERROR' THEN 2 WHEN 'WARNING' THEN 3 WHEN 'INFO' THEN 4 WHEN 'DEBUG' THEN 5 ELSE 6 END",
  "additionalFields": {}
}

// 4. コンポーネント別の集計（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT component, COUNT(*) as count FROM consensus_model_logs WHERE timestamp BETWEEN '{{ $json.start_date }}' AND '{{ $json.end_date }}' GROUP BY component ORDER BY count DESC LIMIT 10",
  "additionalFields": {}
}

// 5. 時間帯別のエラー数（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT date_trunc('hour', timestamp) as hour, COUNT(*) as count FROM consensus_model_logs WHERE timestamp BETWEEN '{{ $json.start_date }}' AND '{{ $json.end_date }}' AND level IN ('ERROR', 'CRITICAL') GROUP BY hour ORDER BY hour",
  "additionalFields": {}
}

// 6. 最近のクリティカルエラー（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT * FROM consensus_model_logs WHERE level = 'CRITICAL' AND timestamp BETWEEN '{{ $json.start_date }}' AND '{{ $json.end_date }}' ORDER BY timestamp DESC LIMIT 5",
  "additionalFields": {}
}

// 7. ダッシュボードデータの統合（Functionノード）
function integrateDashboardData(items) {
  const timeRange = items[0].json;
  const logLevelStats = items[1].json;
  const componentStats = items[2].json;
  const errorTimeStats = items[3].json;
  const recentCriticalErrors = items[4].json;
  
  // ログレベル統計の処理
  const logLevelData = {
    labels: logLevelStats.map(item => item.level),
    values: logLevelStats.map(item => parseInt(item.count, 10)),
    colors: logLevelStats.map(item => {
      switch (item.level) {
        case 'CRITICAL': return '#d9534f';
        case 'ERROR': return '#f0ad4e';
        case 'WARNING': return '#ffd700';
        case 'INFO': return '#5bc0de';
        case 'DEBUG': return '#5cb85c';
        default: return '#777777';
      }
    })
  };
  
  // コンポーネント統計の処理
  const componentData = {
    labels: componentStats.map(item => item.component),
    values: componentStats.map(item => parseInt(item.count, 10))
  };
  
  // 時間帯別エラー統計の処理
  const errorTimeData = {
    labels: errorTimeStats.map(item => {
      const date = new Date(item.hour);
      return date.toLocaleString();
    }),
    values: errorTimeStats.map(item => parseInt(item.count, 10))
  };
  
  // 最近のクリティカルエラーの処理
  const formattedCriticalErrors = recentCriticalErrors.map(log => {
    // JSONフィールドのパース（データベースの実装によっては不要）
    return {
      ...log,
      details: typeof log.details === 'string' ? JSON.parse(log.details) : log.details,
      context: typeof log.context === 'string' ? JSON.parse(log.context) : log.context,
      formatted_time: new Date(log.timestamp).toLocaleString()
    };
  });
  
  // ダッシュボードデータの統合
  const dashboardData = {
    time_range: timeRange,
    log_level_stats: {
      data: logLevelData,
      total: logLevelData.values.reduce((sum, value) => sum + value, 0)
    },
    component_stats: {
      data: componentData,
      total: componentData.values.reduce((sum, value) => sum + value, 0)
    },
    error_time_stats: {
      data: errorTimeData,
      total: errorTimeData.values.reduce((sum, value) => sum + value, 0)
    },
    recent_critical_errors: formattedCriticalErrors
  };
  
  return [
    {
      json: {
        success: true,
        dashboard_data: dashboardData
      }
    }
  ];
}

// 8. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなログ分析ダッシュボードの実装により、ログデータを視覚化し、システムの動作状況を一目で把握することができます。期間パラメータの処理、ログレベル別の集計、コンポーネント別の集計、時間帯別のエラー数、最近のクリティカルエラーの取得、ダッシュボードデータの統合などの機能を含めることで、効果的なログ分析を実現することができます。

**異常検知と通知**

ログデータから異常を検知し、適切な通知を行うことで、問題の早期発見と対応を可能にします。

**異常検知ルールの定義**:
ログデータから異常を検知するためのルールを定義します。

```javascript
// 異常検知ルールの定義例
const anomalyRules = [
  {
    id: 'critical_error_spike',
    name: 'クリティカルエラーの急増',
    description: '短時間内にクリティカルエラーが急増した場合に検知',
    condition: {
      log_level: 'CRITICAL',
      threshold: 5,
      time_window: 60 * 5, // 5分間
      comparison: 'greater_than'
    },
    severity: 'high',
    notification_channels: ['email', 'slack']
  },
  {
    id: 'repeated_workflow_failures',
    name: 'ワークフロー失敗の繰り返し',
    description: '同じワークフローが繰り返し失敗した場合に検知',
    condition: {
      log_level: 'ERROR',
      component: 'workflow_manager',
      message_pattern: 'workflow failed',
      threshold: 3,
      time_window: 60 * 60, // 1時間
      group_by: 'workflow_id',
      comparison: 'greater_than'
    },
    severity: 'medium',
    notification_channels: ['slack']
  },
  {
    id: 'data_source_connection_failures',
    name: 'データソース接続失敗',
    description: 'データソースへの接続が繰り返し失敗した場合に検知',
    condition: {
      log_level: 'ERROR',
      component: 'data_collection',
      message_pattern: 'connection failed',
      threshold: 3,
      time_window: 60 * 15, // 15分間
      group_by: 'data_source',
      comparison: 'greater_than'
    },
    severity: 'medium',
    notification_channels: ['slack']
  },
  {
    id: 'api_rate_limit_exceeded',
    name: 'APIレート制限超過',
    description: 'APIのレート制限を超過した場合に検知',
    condition: {
      log_level: 'WARNING',
      message_pattern: 'rate limit exceeded',
      threshold: 1,
      time_window: 60 * 5, // 5分間
      comparison: 'greater_than_or_equal'
    },
    severity: 'low',
    notification_channels: ['slack']
  },
  {
    id: 'long_running_workflow',
    name: '長時間実行ワークフロー',
    description: 'ワークフローの実行時間が異常に長い場合に検知',
    condition: {
      component: 'workflow_manager',
      message_pattern: 'workflow execution time',
      custom_condition: 'execution_time > 300', // 5分以上
      threshold: 1,
      time_window: 60 * 60, // 1時間
      comparison: 'greater_than_or_equal'
    },
    severity: 'low',
    notification_channels: ['slack']
  }
];
```

**異常検知の実装**:
定義したルールに基づいて、ログデータから異常を検知する機能を実装します。

```javascript
// 異常検知の実装例（n8nワークフロー）

// 1. 異常検知スケジュールトリガー（Cronノード）
// 設定例（5分ごとに実行）
{
  "triggerTimes": {
    "item": [
      {
        "mode": "everyX"
      }
    ]
  },
  "cronExpression": "*/5 * * * *"
}

// 2. 異常検知ルールの取得（Functionノード）
function getAnomalyRules() {
  // 異常検知ルールの取得
  // （実際の実装ではデータベースやファイルからの取得が行われる）
  
  return [
    {
      json: {
        rules: anomalyRules
      }
    }
  ];
}

// 3. ルールごとの処理（SplitInBatchesノード）
// 設定例
{
  "batchSize": 1,
  "options": {}
}

// 4. ルールに基づくログの取得（Functionノード）
function buildAnomalyDetectionQuery(items) {
  const rule = items[0].json;
  
  // 現在の時刻
  const now = new Date();
  
  // 時間枠の計算
  const timeWindowStart = new Date(now.getTime() - rule.condition.time_window * 1000);
  
  // WHERE句の構築
  const whereClauses = [];
  const queryParams = [];
  
  // タイムスタンプの条件
  whereClauses.push(`timestamp >= $${queryParams.length + 1}`);
  queryParams.push(timeWindowStart.toISOString());
  
  whereClauses.push(`timestamp <= $${queryParams.length + 1}`);
  queryParams.push(now.toISOString());
  
  // ログレベルの条件
  if (rule.condition.log_level) {
    whereClauses.push(`level = $${queryParams.length + 1}`);
    queryParams.push(rule.condition.log_level);
  }
  
  // コンポーネントの条件
  if (rule.condition.component) {
    whereClauses.push(`component = $${queryParams.length + 1}`);
    queryParams.push(rule.condition.component);
  }
  
  // メッセージパターンの条件
  if (rule.condition.message_pattern) {
    whereClauses.push(`message ILIKE $${queryParams.length + 1}`);
    queryParams.push(`%${rule.condition.message_pattern}%`);
  }
  
  // GROUP BY句の構築
  let groupByClause = '';
  if (rule.condition.group_by) {
    // グループ化フィールドの取得
    const groupByField = rule.condition.group_by;
    
    // JSONフィールドの場合
    if (groupByField.includes('.')) {
      const [jsonField, jsonPath] = groupByField.split('.');
      groupByClause = `GROUP BY ${jsonField}->>'${jsonPath}'`;
    } else if (groupByField === 'workflow_id' || groupByField === 'target_id' || groupByField === 'data_source') {
      // コンテキストフィールドの場合
      groupByClause = `GROUP BY context->>'${groupByField}'`;
    } else {
      // 通常のフィールドの場合
      groupByClause = `GROUP BY ${groupByField}`;
    }
  }
  
  // HAVING句の構築
  let havingClause = '';
  if (rule.condition.threshold) {
    const comparison = rule.condition.comparison || 'greater_than';
    let operator;
    
    switch (comparison) {
      case 'greater_than':
        operator = '>';
        break;
      case 'greater_than_or_equal':
        operator = '>=';
        break;
      case 'less_than':
        operator = '<';
        break;
      case 'less_than_or_equal':
        operator = '<=';
        break;
      case 'equal':
        operator = '=';
        break;
      case 'not_equal':
        operator = '!=';
        break;
      default:
        operator = '>';
    }
    
    havingClause = `HAVING COUNT(*) ${operator} ${rule.condition.threshold}`;
  }
  
  // カスタム条件の構築
  if (rule.condition.custom_condition) {
    // カスタム条件の解析と適用
    // （実際の実装ではより複雑な処理が必要）
  }
  
  // 完全なSQLクエリの構築
  let sqlQuery;
  if (groupByClause) {
    // グループ化がある場合
    sqlQuery = `
      SELECT
        ${rule.condition.group_by.includes('.') ? `${rule.condition.group_by.split('.')[0]}->>'${rule.condition.group_by.split('.')[1]}'` : 
          rule.condition.group_by === 'workflow_id' || rule.condition.group_by === 'target_id' || rule.condition.group_by === 'data_source' ? 
          `context->>'${rule.condition.group_by}'` : rule.condition.group_by} as group_value,
        COUNT(*) as count
      FROM consensus_model_logs
      WHERE ${whereClauses.join(' AND ')}
      ${groupByClause}
      ${havingClause}
      ORDER BY count DESC
    `;
  } else {
    // グループ化がない場合
    sqlQuery = `
      SELECT COUNT(*) as count
      FROM consensus_model_logs
      WHERE ${whereClauses.join(' AND ')}
    `;
  }
  
  return [
    {
      json: {
        rule: rule,
        sql_query: sqlQuery,
        query_params: queryParams,
        time_window_start: timeWindowStart.toISOString(),
        time_window_end: now.toISOString()
      }
    }
  ];
}

// 5. ログの集計（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.sql_query }}",
  "additionalFields": {}
}

// 6. 異常の検出（Functionノード）
function detectAnomalies(items) {
  const rule = items[0].json.rule;
  const queryResult = items[1].json;
  
  // 異常の検出
  let anomaliesDetected = false;
  let anomalyDetails = [];
  
  if (rule.condition.group_by) {
    // グループ化がある場合
    for (const result of queryResult) {
      const count = parseInt(result.count, 10);
      const threshold = rule.condition.threshold;
      const comparison = rule.condition.comparison || 'greater_than';
      
      let anomalyDetected = false;
      switch (comparison) {
        case 'greater_than':
          anomalyDetected = count > threshold;
          break;
        case 'greater_than_or_equal':
          anomalyDetected = count >= threshold;
          break;
        case 'less_than':
          anomalyDetected = count < threshold;
          break;
        case 'less_than_or_equal':
          anomalyDetected = count <= threshold;
          break;
        case 'equal':
          anomalyDetected = count === threshold;
          break;
        case 'not_equal':
          anomalyDetected = count !== threshold;
          break;
      }
      
      if (anomalyDetected) {
        anomaliesDetected = true;
        anomalyDetails.push({
          group_value: result.group_value,
          count: count,
          threshold: threshold,
          comparison: comparison
        });
      }
    }
  } else {
    // グループ化がない場合
    const count = parseInt(queryResult[0].count, 10);
    const threshold = rule.condition.threshold;
    const comparison = rule.condition.comparison || 'greater_than';
    
    switch (comparison) {
      case 'greater_than':
        anomaliesDetected = count > threshold;
        break;
      case 'greater_than_or_equal':
        anomaliesDetected = count >= threshold;
        break;
      case 'less_than':
        anomaliesDetected = count < threshold;
        break;
      case 'less_than_or_equal':
        anomaliesDetected = count <= threshold;
        break;
      case 'equal':
        anomaliesDetected = count === threshold;
        break;
      case 'not_equal':
        anomaliesDetected = count !== threshold;
        break;
    }
    
    if (anomaliesDetected) {
      anomalyDetails.push({
        count: count,
        threshold: threshold,
        comparison: comparison
      });
    }
  }
  
  // 異常が検出されなかった場合は早期リターン
  if (!anomaliesDetected) {
    return [
      {
        json: {
          rule_id: rule.id,
          anomalies_detected: false
        }
      }
    ];
  }
  
  // 異常情報の作成
  const anomalyInfo = {
    rule_id: rule.id,
    rule_name: rule.name,
    rule_description: rule.description,
    severity: rule.severity,
    anomalies_detected: true,
    detection_time: new Date().toISOString(),
    time_window_start: items[0].json.time_window_start,
    time_window_end: items[0].json.time_window_end,
    anomaly_details: anomalyDetails,
    notification_channels: rule.notification_channels
  };
  
  return [
    {
      json: anomalyInfo
    }
  ];
}

// 7. 通知の送信（条件分岐）
// 異常が検出された場合のみ実行

// 8. 異常情報の記録（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_anomalies",
  "columns": "rule_id, rule_name, severity, detection_time, time_window_start, time_window_end, anomaly_details",
  "additionalFields": {}
}
```

このような異常検知の実装により、定義したルールに基づいてログデータから異常を検知することができます。異常検知ルールの取得、ルールに基づくログの取得、ログの集計、異常の検出、異常情報の記録などの機能を含めることで、効果的な異常検知を実現することができます。

**通知チャネルの実装**:
検知した異常を適切なチャネルに通知する機能を実装します。

```javascript
// 通知チャネルの実装例（n8nワークフロー）

// 1. 通知チャネルの選択（SwitchノードまたはIF）
// 設定例
{
  "rules": {
    "rules": [
      {
        "value1": "={{ $json.notification_channels.includes('email') }}",
        "operation": "equal",
        "value2": true
      },
      {
        "value1": "={{ $json.notification_channels.includes('slack') }}",
        "operation": "equal",
        "value2": true
      }
    ]
  },
  "options": {}
}

// 2. メール通知の作成（Functionノード）
function createEmailNotification(items) {
  const anomalyInfo = items[0].json;
  
  // 重要度に応じた件名プレフィックス
  let subjectPrefix;
  switch (anomalyInfo.severity) {
    case 'high':
      subjectPrefix = '[緊急]';
      break;
    case 'medium':
      subjectPrefix = '[警告]';
      break;
    case 'low':
      subjectPrefix = '[注意]';
      break;
    default:
      subjectPrefix = '[通知]';
  }
  
  // メール件名の作成
  const subject = `${subjectPrefix} コンセンサスモデル異常検知: ${anomalyInfo.rule_name}`;
  
  // 異常詳細の整形
  const anomalyDetailsText = anomalyInfo.anomaly_details.map(detail => {
    if (detail.group_value) {
      return `- グループ値: ${detail.group_value}, 件数: ${detail.count}, 閾値: ${detail.threshold}`;
    } else {
      return `- 件数: ${detail.count}, 閾値: ${detail.threshold}`;
    }
  }).join('\n');
  
  // メール本文の作成
  const body = `
コンセンサスモデルで異常が検知されました。

ルール: ${anomalyInfo.rule_name}
説明: ${anomalyInfo.rule_description}
重要度: ${anomalyInfo.severity}
検知時刻: ${new Date(anomalyInfo.detection_time).toLocaleString()}
期間: ${new Date(anomalyInfo.time_window_start).toLocaleString()} ～ ${new Date(anomalyInfo.time_window_end).toLocaleString()}

異常詳細:
${anomalyDetailsText}

ダッシュボードURL: https://example.com/consensus-model/dashboard?rule_id=${anomalyInfo.rule_id}
  `;
  
  return [
    {
      json: {
        ...anomalyInfo,
        email_notification: {
          to: ['admin@example.com', 'alert@example.com'],
          subject: subject,
          body: body
        }
      }
    }
  ];
}

// 3. メール送信（Emailノード）
// 設定例
{
  "fromEmail": "consensus-model@example.com",
  "fromName": "コンセンサスモデル監視システム",
  "toEmail": "={{ $json.email_notification.to.join(',') }}",
  "subject": "={{ $json.email_notification.subject }}",
  "text": "={{ $json.email_notification.body }}",
  "options": {}
}

// 4. Slack通知の作成（Functionノード）
function createSlackNotification(items) {
  const anomalyInfo = items[0].json;
  
  // 重要度に応じた絵文字とカラー
  let emoji, color;
  switch (anomalyInfo.severity) {
    case 'high':
      emoji = ':red_circle:';
      color = '#d9534f';
      break;
    case 'medium':
      emoji = ':large_orange_diamond:';
      color = '#f0ad4e';
      break;
    case 'low':
      emoji = ':large_blue_circle:';
      color = '#5bc0de';
      break;
    default:
      emoji = ':information_source:';
      color = '#777777';
  }
  
  // 異常詳細の整形
  const anomalyDetailsText = anomalyInfo.anomaly_details.map(detail => {
    if (detail.group_value) {
      return `• グループ値: ${detail.group_value}, 件数: ${detail.count}, 閾値: ${detail.threshold}`;
    } else {
      return `• 件数: ${detail.count}, 閾値: ${detail.threshold}`;
    }
  }).join('\n');
  
  // Slackメッセージの作成
  const slackMessage = {
    text: `${emoji} *コンセンサスモデル異常検知*: ${anomalyInfo.rule_name}`,
    blocks: [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `${emoji} コンセンサスモデル異常検知: ${anomalyInfo.rule_name}`,
          emoji: true
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*説明:* ${anomalyInfo.rule_description}\n*重要度:* ${anomalyInfo.severity}\n*検知時刻:* ${new Date(anomalyInfo.detection_time).toLocaleString()}`
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*期間:* ${new Date(anomalyInfo.time_window_start).toLocaleString()} ～ ${new Date(anomalyInfo.time_window_end).toLocaleString()}`
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*異常詳細:*\n${anomalyDetailsText}`
        }
      },
      {
        type: 'actions',
        elements: [
          {
            type: 'button',
            text: {
              type: 'plain_text',
              text: 'ダッシュボードを表示',
              emoji: true
            },
            url: `https://example.com/consensus-model/dashboard?rule_id=${anomalyInfo.rule_id}`
          }
        ]
      }
    ],
    attachments: [
      {
        color: color,
        blocks: [
          {
            type: 'context',
            elements: [
              {
                type: 'mrkdwn',
                text: `*ルールID:* ${anomalyInfo.rule_id}`
              }
            ]
          }
        ]
      }
    ]
  };
  
  return [
    {
      json: {
        ...anomalyInfo,
        slack_notification: slackMessage
      }
    }
  ];
}

// 5. Slack送信（Slackノード）
// 設定例
{
  "channel": "monitoring",
  "text": "={{ $json.slack_notification.text }}",
  "blocks": "={{ $json.slack_notification.blocks }}",
  "attachments": "={{ $json.slack_notification.attachments }}",
  "otherOptions": {}
}
```

このような通知チャネルの実装により、検知した異常を適切なチャネルに通知することができます。通知チャネルの選択、メール通知の作成、メール送信、Slack通知の作成、Slack送信などの機能を含めることで、効果的な通知を実現することができます。

これらのログ管理機能により、コンセンサスモデルの動作状況を監視し、問題の診断や性能の最適化を行うことができます。n8nを活用することで、これらのログを効率的に収集、保存、分析することが可能になり、システムの透明性が向上し、障害発生時の原因特定や復旧が容易になります。
