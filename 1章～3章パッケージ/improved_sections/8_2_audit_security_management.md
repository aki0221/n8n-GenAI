### 8.2 監査・セキュリティ管理

コンセンサスモデルの管理コンポーネントにおける監査・セキュリティ管理は、システムの信頼性、完全性、機密性を確保するための重要な機能です。適切な監査・セキュリティ管理により、システムの利用状況を追跡し、不正アクセスや不適切な操作を防止することができます。n8nを活用することで、これらの監査・セキュリティ機能を効率的に実装することが可能になります。

**監査証跡の記録と管理**

システム内のすべての重要な操作を記録し、後から追跡できるようにすることが重要です。これにより、問題が発生した場合の原因特定や、コンプライアンス要件への対応が容易になります。

**監査イベントの定義**:
監査対象となるイベントの種類と内容を定義します。

```javascript
// 監査イベントの定義例
const auditEventTypes = {
  USER_LOGIN: {
    code: 'USER_LOGIN',
    description: 'ユーザーログイン',
    severity: 'info',
    requires_details: ['user_id', 'ip_address']
  },
  USER_LOGOUT: {
    code: 'USER_LOGOUT',
    description: 'ユーザーログアウト',
    severity: 'info',
    requires_details: ['user_id']
  },
  USER_CREATED: {
    code: 'USER_CREATED',
    description: 'ユーザー作成',
    severity: 'info',
    requires_details: ['user_id', 'created_by']
  },
  USER_UPDATED: {
    code: 'USER_UPDATED',
    description: 'ユーザー情報更新',
    severity: 'info',
    requires_details: ['user_id', 'updated_by', 'changed_fields']
  },
  USER_DELETED: {
    code: 'USER_DELETED',
    description: 'ユーザー削除',
    severity: 'warning',
    requires_details: ['user_id', 'deleted_by']
  },
  ROLE_ASSIGNED: {
    code: 'ROLE_ASSIGNED',
    description: 'ロール割り当て',
    severity: 'info',
    requires_details: ['user_id', 'role_id', 'assigned_by']
  },
  ROLE_REVOKED: {
    code: 'ROLE_REVOKED',
    description: 'ロール剥奪',
    severity: 'info',
    requires_details: ['user_id', 'role_id', 'revoked_by']
  },
  PERMISSION_GRANTED: {
    code: 'PERMISSION_GRANTED',
    description: '権限付与',
    severity: 'info',
    requires_details: ['user_id', 'permission', 'granted_by']
  },
  PERMISSION_REVOKED: {
    code: 'PERMISSION_REVOKED',
    description: '権限剥奪',
    severity: 'info',
    requires_details: ['user_id', 'permission', 'revoked_by']
  },
  WORKFLOW_CREATED: {
    code: 'WORKFLOW_CREATED',
    description: 'ワークフロー作成',
    severity: 'info',
    requires_details: ['workflow_id', 'created_by']
  },
  WORKFLOW_UPDATED: {
    code: 'WORKFLOW_UPDATED',
    description: 'ワークフロー更新',
    severity: 'info',
    requires_details: ['workflow_id', 'updated_by', 'changed_fields']
  },
  WORKFLOW_DELETED: {
    code: 'WORKFLOW_DELETED',
    description: 'ワークフロー削除',
    severity: 'warning',
    requires_details: ['workflow_id', 'deleted_by']
  },
  WORKFLOW_EXECUTED: {
    code: 'WORKFLOW_EXECUTED',
    description: 'ワークフロー実行',
    severity: 'info',
    requires_details: ['workflow_id', 'executed_by', 'execution_id']
  },
  PARAMETER_UPDATED: {
    code: 'PARAMETER_UPDATED',
    description: 'パラメータ更新',
    severity: 'info',
    requires_details: ['parameter_set_id', 'updated_by', 'changed_parameters']
  },
  DATA_EXPORTED: {
    code: 'DATA_EXPORTED',
    description: 'データエクスポート',
    severity: 'warning',
    requires_details: ['data_type', 'exported_by', 'export_format', 'record_count']
  },
  CONFIGURATION_CHANGED: {
    code: 'CONFIGURATION_CHANGED',
    description: '設定変更',
    severity: 'warning',
    requires_details: ['config_section', 'changed_by', 'changed_settings']
  },
  SECURITY_POLICY_CHANGED: {
    code: 'SECURITY_POLICY_CHANGED',
    description: 'セキュリティポリシー変更',
    severity: 'alert',
    requires_details: ['policy_name', 'changed_by', 'changed_settings']
  },
  UNAUTHORIZED_ACCESS_ATTEMPT: {
    code: 'UNAUTHORIZED_ACCESS_ATTEMPT',
    description: '不正アクセス試行',
    severity: 'alert',
    requires_details: ['user_id', 'ip_address', 'resource', 'required_permission']
  },
  API_KEY_CREATED: {
    code: 'API_KEY_CREATED',
    description: 'APIキー作成',
    severity: 'warning',
    requires_details: ['api_key_id', 'created_by', 'expiration_date']
  },
  API_KEY_REVOKED: {
    code: 'API_KEY_REVOKED',
    description: 'APIキー無効化',
    severity: 'warning',
    requires_details: ['api_key_id', 'revoked_by', 'reason']
  }
};
```

**監査イベントの記録**:
定義したイベントを適切に記録するための機能を実装します。

```javascript
// 監査イベントの記録例（n8nワークフロー）

// 1. 監査イベント記録トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/audit/log",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. 監査イベントの検証（Functionノード）
function validateAuditEvent(items) {
  const auditData = items[0].json.body;
  const errors = [];
  
  // イベントタイプの検証
  if (!auditData.event_type) {
    errors.push("Missing required field: event_type");
  } else if (!auditEventTypes[auditData.event_type]) {
    errors.push(`Invalid event type: ${auditData.event_type}`);
  }
  
  // イベントタイプが有効な場合、必須詳細フィールドの検証
  if (auditData.event_type && auditEventTypes[auditData.event_type]) {
    const requiredDetails = auditEventTypes[auditData.event_type].requires_details;
    
    for (const field of requiredDetails) {
      if (!auditData.details || auditData.details[field] === undefined) {
        errors.push(`Missing required detail field for ${auditData.event_type}: ${field}`);
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
  
  // イベントの重要度を取得
  const severity = auditEventTypes[auditData.event_type].severity || 'info';
  
  // 監査イベントの作成
  const auditEvent = {
    event_type: auditData.event_type,
    event_description: auditEventTypes[auditData.event_type].description,
    severity: severity,
    timestamp: new Date().toISOString(),
    user_id: auditData.user_id || auditData.details?.user_id || null,
    ip_address: auditData.ip_address || auditData.details?.ip_address || null,
    details: auditData.details || {},
    session_id: auditData.session_id || null,
    application: auditData.application || 'consensus-model',
    environment: process.env.NODE_ENV || 'development'
  };
  
  return [
    {
      json: {
        success: true,
        audit_event: auditEvent
      }
    }
  ];
}

// 3. 監査イベントの保存（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "consensus_model_audit_logs",
  "columns": "event_type, event_description, severity, timestamp, user_id, ip_address, details, session_id, application, environment",
  "additionalFields": {}
}

// 4. 高重要度イベントの通知（Functionノード）
function checkHighSeverityEvent(items) {
  const auditEvent = items[0].json.audit_event;
  
  // 高重要度イベントの確認
  const isHighSeverity = auditEvent.severity === 'alert' || auditEvent.severity === 'critical';
  
  // 高重要度でない場合は早期リターン
  if (!isHighSeverity) {
    return [
      {
        json: {
          success: true,
          audit_event: auditEvent,
          high_severity: false
        }
      }
    ];
  }
  
  // 通知メッセージの作成
  const notificationMessage = {
    subject: `[${auditEvent.severity.toUpperCase()}] セキュリティイベント: ${auditEvent.event_description}`,
    body: `
セキュリティ監査イベントが検出されました。

イベントタイプ: ${auditEvent.event_type}
説明: ${auditEvent.event_description}
重要度: ${auditEvent.severity}
タイムスタンプ: ${new Date(auditEvent.timestamp).toLocaleString()}
ユーザーID: ${auditEvent.user_id || 'N/A'}
IPアドレス: ${auditEvent.ip_address || 'N/A'}

詳細:
${JSON.stringify(auditEvent.details, null, 2)}

環境: ${auditEvent.environment}
アプリケーション: ${auditEvent.application}
    `,
    recipients: ['security@example.com', 'admin@example.com']
  };
  
  return [
    {
      json: {
        success: true,
        audit_event: auditEvent,
        high_severity: true,
        notification: notificationMessage
      }
    }
  ];
}

// 5. 通知の送信（条件分岐）
// 高重要度イベントの場合のみ実行

// 6. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このような監査イベントの記録機能を実装することで、システム内のすべての重要な操作を追跡することができます。監査イベントの検証、保存、高重要度イベントの通知などの機能を含めることで、効果的な監査証跡の管理を実現することができます。

**監査レポートの生成**:
記録された監査イベントを分析し、レポートを生成するための機能を実装します。

```javascript
// 監査レポートの生成例（n8nワークフロー）

// 1. 監査レポート生成トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/audit/report",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. レポートパラメータの処理（Functionノード）
function processReportParameters(items) {
  const query = items[0].json.query;
  
  // デフォルトのパラメータ
  const defaultParams = {
    start_date: null,
    end_date: null,
    event_types: null,
    user_id: null,
    severity: null,
    format: 'json'
  };
  
  // クエリパラメータのマージ
  const reportParams = { ...defaultParams };
  
  for (const [key, value] of Object.entries(query)) {
    if (key in reportParams && value !== undefined && value !== null && value !== '') {
      reportParams[key] = value;
    }
  }
  
  // 日付の処理
  if (!reportParams.start_date) {
    // デフォルトは過去30日
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    reportParams.start_date = startDate.toISOString();
  } else {
    try {
      reportParams.start_date = new Date(reportParams.start_date).toISOString();
    } catch (error) {
      // 無効な日付の場合はデフォルトを使用
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30);
      reportParams.start_date = startDate.toISOString();
    }
  }
  
  if (!reportParams.end_date) {
    // デフォルトは現在
    reportParams.end_date = new Date().toISOString();
  } else {
    try {
      reportParams.end_date = new Date(reportParams.end_date).toISOString();
    } catch (error) {
      // 無効な日付の場合はデフォルトを使用
      reportParams.end_date = new Date().toISOString();
    }
  }
  
  // イベントタイプの処理
  if (reportParams.event_types) {
    reportParams.event_types = reportParams.event_types.split(',');
  }
  
  // 重要度の処理
  if (reportParams.severity) {
    reportParams.severity = reportParams.severity.split(',');
  }
  
  // フォーマットの検証
  if (!['json', 'csv', 'pdf'].includes(reportParams.format)) {
    reportParams.format = 'json';
  }
  
  return [
    {
      json: {
        report_params: reportParams
      }
    }
  ];
}

// 3. レポートクエリの構築（Functionノード）
function buildReportQuery(items) {
  const params = items[0].json.report_params;
  
  // WHERE句の構築
  const whereClauses = [];
  const queryParams = [];
  
  // 日付範囲によるフィルタリング
  whereClauses.push(`timestamp >= $${queryParams.length + 1}`);
  queryParams.push(params.start_date);
  
  whereClauses.push(`timestamp <= $${queryParams.length + 1}`);
  queryParams.push(params.end_date);
  
  // イベントタイプによるフィルタリング
  if (params.event_types && params.event_types.length > 0) {
    const placeholders = params.event_types.map((_, index) => `$${queryParams.length + index + 1}`).join(', ');
    whereClauses.push(`event_type IN (${placeholders})`);
    queryParams.push(...params.event_types);
  }
  
  // ユーザーIDによるフィルタリング
  if (params.user_id) {
    whereClauses.push(`user_id = $${queryParams.length + 1}`);
    queryParams.push(params.user_id);
  }
  
  // 重要度によるフィルタリング
  if (params.severity && params.severity.length > 0) {
    const placeholders = params.severity.map((_, index) => `$${queryParams.length + index + 1}`).join(', ');
    whereClauses.push(`severity IN (${placeholders})`);
    queryParams.push(...params.severity);
  }
  
  // WHERE句の結合
  const whereClause = `WHERE ${whereClauses.join(' AND ')}`;
  
  // 基本クエリの構築
  const baseQuery = `
    SELECT *
    FROM consensus_model_audit_logs
    ${whereClause}
    ORDER BY timestamp DESC
  `;
  
  // 集計クエリの構築
  const summaryQueries = {
    event_type_summary: `
      SELECT event_type, COUNT(*) as count
      FROM consensus_model_audit_logs
      ${whereClause}
      GROUP BY event_type
      ORDER BY count DESC
    `,
    severity_summary: `
      SELECT severity, COUNT(*) as count
      FROM consensus_model_audit_logs
      ${whereClause}
      GROUP BY severity
      ORDER BY CASE severity
        WHEN 'critical' THEN 1
        WHEN 'alert' THEN 2
        WHEN 'warning' THEN 3
        WHEN 'info' THEN 4
        ELSE 5
      END
    `,
    user_summary: `
      SELECT user_id, COUNT(*) as count
      FROM consensus_model_audit_logs
      ${whereClause}
      GROUP BY user_id
      ORDER BY count DESC
      LIMIT 10
    `,
    hourly_activity: `
      SELECT
        date_trunc('hour', timestamp) as hour,
        COUNT(*) as count
      FROM consensus_model_audit_logs
      ${whereClause}
      GROUP BY hour
      ORDER BY hour
    `
  };
  
  return [
    {
      json: {
        report_params: params,
        base_query: baseQuery,
        summary_queries: summaryQueries,
        query_params: queryParams
      }
    }
  ];
}

// 4. 基本データの取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.base_query }}",
  "additionalFields": {}
}

// 5. イベントタイプ集計の取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.summary_queries.event_type_summary }}",
  "additionalFields": {}
}

// 6. 重要度集計の取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.summary_queries.severity_summary }}",
  "additionalFields": {}
}

// 7. ユーザー集計の取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.summary_queries.user_summary }}",
  "additionalFields": {}
}

// 8. 時間帯別アクティビティの取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.summary_queries.hourly_activity }}",
  "additionalFields": {}
}

// 9. レポートの生成（Functionノード）
function generateReport(items) {
  const reportParams = items[0].json.report_params;
  const baseData = items[1].json;
  const eventTypeSummary = items[2].json;
  const severitySummary = items[3].json;
  const userSummary = items[4].json;
  const hourlyActivity = items[5].json;
  
  // レポートのメタデータ
  const reportMetadata = {
    title: 'コンセンサスモデル監査レポート',
    generated_at: new Date().toISOString(),
    period: {
      start_date: reportParams.start_date,
      end_date: reportParams.end_date
    },
    filters: {
      event_types: reportParams.event_types,
      user_id: reportParams.user_id,
      severity: reportParams.severity
    }
  };
  
  // レポートの概要
  const reportSummary = {
    total_events: baseData.length,
    event_type_distribution: eventTypeSummary,
    severity_distribution: severitySummary,
    top_users: userSummary,
    hourly_activity: hourlyActivity.map(item => ({
      hour: item.hour,
      count: parseInt(item.count, 10)
    }))
  };
  
  // 詳細データの処理
  const detailedData = baseData.map(event => {
    // JSONフィールドのパース（データベースの実装によっては不要）
    return {
      ...event,
      details: typeof event.details === 'string' ? JSON.parse(event.details) : event.details,
      formatted_time: new Date(event.timestamp).toLocaleString()
    };
  });
  
  // レポートの作成
  const report = {
    metadata: reportMetadata,
    summary: reportSummary,
    detailed_data: detailedData
  };
  
  // フォーマットに応じた処理
  let formattedReport;
  let contentType;
  
  switch (reportParams.format) {
    case 'csv':
      formattedReport = convertToCSV(report);
      contentType = 'text/csv';
      break;
    case 'pdf':
      formattedReport = report; // PDF変換は別途処理
      contentType = 'application/pdf';
      break;
    case 'json':
    default:
      formattedReport = report;
      contentType = 'application/json';
  }
  
  return [
    {
      json: {
        success: true,
        report: formattedReport,
        format: reportParams.format,
        content_type: contentType
      }
    }
  ];
}

// CSVへの変換
function convertToCSV(report) {
  // 詳細データのCSV変換
  const headers = ['event_type', 'event_description', 'severity', 'timestamp', 'user_id', 'ip_address', 'details', 'session_id', 'application', 'environment'];
  
  const rows = [
    headers.join(','),
    ...report.detailed_data.map(event => {
      return headers.map(header => {
        if (header === 'details') {
          return `"${JSON.stringify(event[header]).replace(/"/g, '""')}"`;
        } else {
          return `"${(event[header] || '').toString().replace(/"/g, '""')}"`;
        }
      }).join(',');
    })
  ];
  
  return rows.join('\n');
}

// 10. フォーマット別の処理（条件分岐）
// フォーマットに応じて異なる処理を実行

// 11. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200,
  "responseHeaders": {
    "Content-Type": "={{ $json.content_type }}",
    "Content-Disposition": "attachment; filename=\"audit_report_{{ $json.report.metadata.generated_at.split('T')[0] }}.{{ $json.format }}\""
  }
}
```

このような監査レポートの生成機能を実装することで、記録された監査イベントを分析し、有用なレポートを生成することができます。レポートパラメータの処理、レポートクエリの構築、各種データの取得、レポートの生成などの機能を含めることで、効果的な監査分析を実現することができます。

**アクセス制御と認証**

システムへのアクセスを適切に制御し、認証された利用者のみがシステムを利用できるようにすることが重要です。これにより、不正アクセスや不適切な操作を防止することができます。

**ロールベースのアクセス制御**:
ユーザーのロールに基づいて、システムの機能やデータへのアクセスを制御する仕組みを実装します。

```javascript
// ロールベースのアクセス制御の定義例
const roles = {
  ADMIN: {
    name: '管理者',
    description: 'システム全体の管理権限を持つロール',
    permissions: [
      'user:create', 'user:read', 'user:update', 'user:delete',
      'role:create', 'role:read', 'role:update', 'role:delete',
      'workflow:create', 'workflow:read', 'workflow:update', 'workflow:delete', 'workflow:execute',
      'parameter:create', 'parameter:read', 'parameter:update', 'parameter:delete',
      'data:read', 'data:export',
      'audit:read',
      'config:read', 'config:update',
      'security:read', 'security:update'
    ]
  },
  MANAGER: {
    name: 'マネージャー',
    description: 'ワークフローとパラメータの管理権限を持つロール',
    permissions: [
      'user:read',
      'role:read',
      'workflow:create', 'workflow:read', 'workflow:update', 'workflow:delete', 'workflow:execute',
      'parameter:create', 'parameter:read', 'parameter:update', 'parameter:delete',
      'data:read', 'data:export',
      'audit:read',
      'config:read'
    ]
  },
  ANALYST: {
    name: 'アナリスト',
    description: 'ワークフローの実行とデータ分析権限を持つロール',
    permissions: [
      'workflow:read', 'workflow:execute',
      'parameter:read',
      'data:read', 'data:export'
    ]
  },
  VIEWER: {
    name: 'ビューアー',
    description: '参照のみの権限を持つロール',
    permissions: [
      'workflow:read',
      'parameter:read',
      'data:read'
    ]
  }
};

// パーミッションの定義例
const permissions = {
  'user:create': {
    name: 'ユーザー作成',
    description: 'ユーザーを作成する権限'
  },
  'user:read': {
    name: 'ユーザー参照',
    description: 'ユーザー情報を参照する権限'
  },
  'user:update': {
    name: 'ユーザー更新',
    description: 'ユーザー情報を更新する権限'
  },
  'user:delete': {
    name: 'ユーザー削除',
    description: 'ユーザーを削除する権限'
  },
  'role:create': {
    name: 'ロール作成',
    description: 'ロールを作成する権限'
  },
  'role:read': {
    name: 'ロール参照',
    description: 'ロール情報を参照する権限'
  },
  'role:update': {
    name: 'ロール更新',
    description: 'ロール情報を更新する権限'
  },
  'role:delete': {
    name: 'ロール削除',
    description: 'ロールを削除する権限'
  },
  'workflow:create': {
    name: 'ワークフロー作成',
    description: 'ワークフローを作成する権限'
  },
  'workflow:read': {
    name: 'ワークフロー参照',
    description: 'ワークフロー情報を参照する権限'
  },
  'workflow:update': {
    name: 'ワークフロー更新',
    description: 'ワークフロー情報を更新する権限'
  },
  'workflow:delete': {
    name: 'ワークフロー削除',
    description: 'ワークフローを削除する権限'
  },
  'workflow:execute': {
    name: 'ワークフロー実行',
    description: 'ワークフローを実行する権限'
  },
  'parameter:create': {
    name: 'パラメータ作成',
    description: 'パラメータを作成する権限'
  },
  'parameter:read': {
    name: 'パラメータ参照',
    description: 'パラメータ情報を参照する権限'
  },
  'parameter:update': {
    name: 'パラメータ更新',
    description: 'パラメータ情報を更新する権限'
  },
  'parameter:delete': {
    name: 'パラメータ削除',
    description: 'パラメータを削除する権限'
  },
  'data:read': {
    name: 'データ参照',
    description: 'データを参照する権限'
  },
  'data:export': {
    name: 'データエクスポート',
    description: 'データをエクスポートする権限'
  },
  'audit:read': {
    name: '監査ログ参照',
    description: '監査ログを参照する権限'
  },
  'config:read': {
    name: '設定参照',
    description: '設定情報を参照する権限'
  },
  'config:update': {
    name: '設定更新',
    description: '設定情報を更新する権限'
  },
  'security:read': {
    name: 'セキュリティ設定参照',
    description: 'セキュリティ設定を参照する権限'
  },
  'security:update': {
    name: 'セキュリティ設定更新',
    description: 'セキュリティ設定を更新する権限'
  }
};
```

**アクセス制御の実装**:
定義したロールとパーミッションに基づいて、アクセス制御を実装します。

```javascript
// アクセス制御の実装例（n8nワークフロー）

// 1. アクセス制御チェックトリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/auth/check-permission",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. アクセス制御リクエストの検証（Functionノード）
function validateAccessControlRequest(items) {
  const request = items[0].json.body;
  const errors = [];
  
  // 必須フィールドの検証
  if (!request.user_id) {
    errors.push("Missing required field: user_id");
  }
  
  if (!request.permission) {
    errors.push("Missing required field: permission");
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
        user_id: request.user_id,
        permission: request.permission,
        resource_id: request.resource_id || null
      }
    }
  ];
}

// 3. ユーザーのロール取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT role_id FROM user_roles WHERE user_id = $1",
  "additionalFields": {}
}

// 4. パーミッションチェック（Functionノード）
function checkPermission(items) {
  const request = items[0].json;
  const userRoles = items[1].json;
  
  // ユーザーのロールが見つからない場合
  if (!userRoles || userRoles.length === 0) {
    return [
      {
        json: {
          success: false,
          has_permission: false,
          message: "User has no roles assigned"
        }
      }
    ];
  }
  
  // ユーザーのロールIDを取得
  const roleIds = userRoles.map(role => role.role_id);
  
  // ユーザーのパーミッションを取得
  const userPermissions = new Set();
  
  for (const roleId of roleIds) {
    if (roles[roleId]) {
      for (const permission of roles[roleId].permissions) {
        userPermissions.add(permission);
      }
    }
  }
  
  // リクエストされたパーミッションをチェック
  const hasPermission = userPermissions.has(request.permission);
  
  // リソース固有のパーミッションチェック
  let resourceSpecificCheck = true;
  
  if (request.resource_id && hasPermission) {
    // リソース固有のパーミッションチェックロジック
    // （実際の実装ではデータベースクエリなどが必要）
    
    // サンプル実装
    if (request.permission.startsWith('workflow:') && request.permission !== 'workflow:create') {
      // ワークフローの所有者チェックなど
      resourceSpecificCheck = true; // 実際には適切なチェックが必要
    } else if (request.permission.startsWith('parameter:') && request.permission !== 'parameter:create') {
      // パラメータの所有者チェックなど
      resourceSpecificCheck = true; // 実際には適切なチェックが必要
    }
  }
  
  // 監査ログの記録
  const auditEvent = {
    event_type: hasPermission && resourceSpecificCheck ? 'PERMISSION_CHECK_SUCCESS' : 'PERMISSION_CHECK_FAILURE',
    user_id: request.user_id,
    details: {
      permission: request.permission,
      resource_id: request.resource_id,
      roles: roleIds,
      result: hasPermission && resourceSpecificCheck
    }
  };
  
  return [
    {
      json: {
        success: true,
        has_permission: hasPermission && resourceSpecificCheck,
        roles: roleIds,
        audit_event: auditEvent
      }
    }
  ];
}

// 5. 監査ログの記録（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/audit/log",
  "method": "POST",
  "authentication": "none",
  "options": {}
}

// 6. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなアクセス制御の実装により、ユーザーのロールに基づいてシステムの機能やデータへのアクセスを制御することができます。アクセス制御リクエストの検証、ユーザーのロール取得、パーミッションチェック、監査ログの記録などの機能を含めることで、効果的なアクセス制御を実現することができます。

**認証の実装**:
ユーザーの認証を行い、正当なユーザーのみがシステムを利用できるようにする機能を実装します。

```javascript
// 認証の実装例（n8nワークフロー）

// 1. ログイントリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/auth/login",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "POST"
    ]
  }
}

// 2. ログインリクエストの検証（Functionノード）
function validateLoginRequest(items) {
  const request = items[0].json.body;
  const errors = [];
  
  // 必須フィールドの検証
  if (!request.username) {
    errors.push("Missing required field: username");
  }
  
  if (!request.password) {
    errors.push("Missing required field: password");
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
        username: request.username,
        password: request.password,
        ip_address: items[0].json.headers['x-forwarded-for'] || items[0].json.headers['x-real-ip'] || '0.0.0.0'
      }
    }
  ];
}

// 3. ユーザー情報の取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT * FROM users WHERE username = $1",
  "additionalFields": {}
}

// 4. パスワードの検証（Functionノード）
function verifyPassword(items) {
  const request = items[0].json;
  const userResult = items[1].json;
  
  // ユーザーが見つからない場合
  if (!userResult || userResult.length === 0) {
    // 監査ログの記録
    const auditEvent = {
      event_type: 'USER_LOGIN_FAILURE',
      details: {
        username: request.username,
        reason: 'user_not_found',
        ip_address: request.ip_address
      }
    };
    
    return [
      {
        json: {
          success: false,
          message: "Invalid username or password",
          audit_event: auditEvent
        }
      }
    ];
  }
  
  const user = userResult[0];
  
  // アカウントが無効化されている場合
  if (user.is_disabled) {
    // 監査ログの記録
    const auditEvent = {
      event_type: 'USER_LOGIN_FAILURE',
      user_id: user.id,
      details: {
        username: request.username,
        reason: 'account_disabled',
        ip_address: request.ip_address
      }
    };
    
    return [
      {
        json: {
          success: false,
          message: "Account is disabled",
          audit_event: auditEvent
        }
      }
    ];
  }
  
  // パスワードの検証
  // （実際の実装ではbcryptなどのハッシュ関数を使用）
  const isPasswordValid = verifyPasswordHash(request.password, user.password_hash);
  
  if (!isPasswordValid) {
    // 監査ログの記録
    const auditEvent = {
      event_type: 'USER_LOGIN_FAILURE',
      user_id: user.id,
      details: {
        username: request.username,
        reason: 'invalid_password',
        ip_address: request.ip_address
      }
    };
    
    return [
      {
        json: {
          success: false,
          message: "Invalid username or password",
          audit_event: auditEvent
        }
      }
    ];
  }
  
  // セッションの作成
  const sessionId = generateSessionId();
  const expiresAt = new Date();
  expiresAt.setHours(expiresAt.getHours() + 24); // 24時間有効
  
  // 監査ログの記録
  const auditEvent = {
    event_type: 'USER_LOGIN',
    user_id: user.id,
    details: {
      username: request.username,
      ip_address: request.ip_address,
      session_id: sessionId
    }
  };
  
  return [
    {
      json: {
        success: true,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          name: user.name
        },
        session: {
          id: sessionId,
          expires_at: expiresAt.toISOString()
        },
        audit_event: auditEvent
      }
    }
  ];
}

// パスワードハッシュの検証（サンプル実装）
function verifyPasswordHash(password, hash) {
  // 実際の実装ではbcryptなどのハッシュ関数を使用
  return true; // サンプルでは常にtrueを返す
}

// セッションIDの生成
function generateSessionId() {
  return 'sess_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

// 5. セッションの保存（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "user_sessions",
  "columns": "id, user_id, expires_at, ip_address",
  "additionalFields": {}
}

// 6. 監査ログの記録（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/audit/log",
  "method": "POST",
  "authentication": "none",
  "options": {}
}

// 7. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このような認証の実装により、ユーザーの認証を行い、正当なユーザーのみがシステムを利用できるようにすることができます。ログインリクエストの検証、ユーザー情報の取得、パスワードの検証、セッションの保存、監査ログの記録などの機能を含めることで、効果的な認証を実現することができます。

**セキュリティ設定の管理**

システムのセキュリティ設定を適切に管理し、セキュリティリスクを最小化するための機能を実装します。

**セキュリティポリシーの定義**:
システムのセキュリティポリシーを定義し、適切に管理するための機能を実装します。

```javascript
// セキュリティポリシーの定義例
const securityPolicies = {
  password: {
    min_length: 8,
    require_uppercase: true,
    require_lowercase: true,
    require_number: true,
    require_special_char: true,
    max_age_days: 90,
    history_count: 5
  },
  session: {
    timeout_minutes: 30,
    max_concurrent: 3,
    remember_me_days: 30
  },
  login: {
    max_attempts: 5,
    lockout_minutes: 15,
    require_captcha_after_failures: 3
  },
  api: {
    key_expiry_days: 180,
    rate_limit_per_minute: 60,
    require_https: true
  },
  audit: {
    retention_days: 365,
    high_severity_notification: true
  },
  data: {
    encryption_enabled: true,
    export_approval_required: true,
    max_export_records: 10000
  }
};
```

**セキュリティ設定の管理**:
定義したセキュリティポリシーを管理するための機能を実装します。

```javascript
// セキュリティ設定の管理例（n8nワークフロー）

// 1. セキュリティ設定取得トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/security/settings",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "GET"
    ]
  }
}

// 2. アクセス権限の確認（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/auth/check-permission",
  "method": "POST",
  "authentication": "none",
  "options": {}
}

// 3. 権限チェック結果の処理（Functionノード）
function processPermissionCheck(items) {
  const permissionResult = items[1].json;
  
  // 権限がない場合
  if (!permissionResult.has_permission) {
    return [
      {
        json: {
          success: false,
          message: "Permission denied: security:read required"
        }
      }
    ];
  }
  
  return [
    {
      json: {
        success: true
      }
    }
  ];
}

// 4. セキュリティ設定の取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT * FROM security_settings",
  "additionalFields": {}
}

// 5. セキュリティ設定の処理（Functionノード）
function processSecuritySettings(items) {
  const settingsResult = items[1].json;
  
  // デフォルト設定
  const defaultSettings = securityPolicies;
  
  // 保存された設定がない場合はデフォルト設定を使用
  if (!settingsResult || settingsResult.length === 0) {
    return [
      {
        json: {
          success: true,
          settings: defaultSettings,
          is_default: true
        }
      }
    ];
  }
  
  // 保存された設定を処理
  const savedSettings = {};
  
  for (const setting of settingsResult) {
    if (!savedSettings[setting.category]) {
      savedSettings[setting.category] = {};
    }
    
    savedSettings[setting.category][setting.name] = setting.value;
  }
  
  // デフォルト設定とマージ
  const mergedSettings = {};
  
  for (const category in defaultSettings) {
    mergedSettings[category] = {
      ...defaultSettings[category],
      ...(savedSettings[category] || {})
    };
  }
  
  return [
    {
      json: {
        success: true,
        settings: mergedSettings,
        is_default: false
      }
    }
  ];
}

// 6. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなセキュリティ設定の管理機能を実装することで、システムのセキュリティポリシーを適切に管理することができます。アクセス権限の確認、セキュリティ設定の取得、セキュリティ設定の処理などの機能を含めることで、効果的なセキュリティ管理を実現することができます。

**セキュリティ設定の更新**:
セキュリティ設定を更新するための機能を実装します。

```javascript
// セキュリティ設定の更新例（n8nワークフロー）

// 1. セキュリティ設定更新トリガー（Webhookノード）
// 設定例
{
  "path": "consensus-model/security/settings",
  "responseMode": "onReceived",
  "options": {
    "allowedMethods": [
      "PUT"
    ]
  }
}

// 2. アクセス権限の確認（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/auth/check-permission",
  "method": "POST",
  "authentication": "none",
  "options": {}
}

// 3. 権限チェック結果の処理（Functionノード）
function processPermissionCheck(items) {
  const permissionResult = items[1].json;
  
  // 権限がない場合
  if (!permissionResult.has_permission) {
    return [
      {
        json: {
          success: false,
          message: "Permission denied: security:update required"
        }
      }
    ];
  }
  
  return [
    {
      json: {
        success: true,
        settings: items[0].json.body.settings,
        user_id: items[0].json.body.user_id
      }
    }
  ];
}

// 4. 設定の検証（Functionノード）
function validateSettings(items) {
  const settings = items[0].json.settings;
  const errors = [];
  
  // パスワードポリシーの検証
  if (settings.password) {
    if (settings.password.min_length !== undefined && (typeof settings.password.min_length !== 'number' || settings.password.min_length < 6)) {
      errors.push("Password minimum length must be at least 6");
    }
    
    if (settings.password.max_age_days !== undefined && (typeof settings.password.max_age_days !== 'number' || settings.password.max_age_days < 1)) {
      errors.push("Password maximum age must be at least 1 day");
    }
    
    if (settings.password.history_count !== undefined && (typeof settings.password.history_count !== 'number' || settings.password.history_count < 0)) {
      errors.push("Password history count must be non-negative");
    }
  }
  
  // セッションポリシーの検証
  if (settings.session) {
    if (settings.session.timeout_minutes !== undefined && (typeof settings.session.timeout_minutes !== 'number' || settings.session.timeout_minutes < 5)) {
      errors.push("Session timeout must be at least 5 minutes");
    }
    
    if (settings.session.max_concurrent !== undefined && (typeof settings.session.max_concurrent !== 'number' || settings.session.max_concurrent < 1)) {
      errors.push("Maximum concurrent sessions must be at least 1");
    }
    
    if (settings.session.remember_me_days !== undefined && (typeof settings.session.remember_me_days !== 'number' || settings.session.remember_me_days < 1)) {
      errors.push("Remember me duration must be at least 1 day");
    }
  }
  
  // ログインポリシーの検証
  if (settings.login) {
    if (settings.login.max_attempts !== undefined && (typeof settings.login.max_attempts !== 'number' || settings.login.max_attempts < 1)) {
      errors.push("Maximum login attempts must be at least 1");
    }
    
    if (settings.login.lockout_minutes !== undefined && (typeof settings.login.lockout_minutes !== 'number' || settings.login.lockout_minutes < 1)) {
      errors.push("Lockout duration must be at least 1 minute");
    }
    
    if (settings.login.require_captcha_after_failures !== undefined && (typeof settings.login.require_captcha_after_failures !== 'number' || settings.login.require_captcha_after_failures < 0)) {
      errors.push("Captcha requirement threshold must be non-negative");
    }
  }
  
  // APIポリシーの検証
  if (settings.api) {
    if (settings.api.key_expiry_days !== undefined && (typeof settings.api.key_expiry_days !== 'number' || settings.api.key_expiry_days < 1)) {
      errors.push("API key expiry must be at least 1 day");
    }
    
    if (settings.api.rate_limit_per_minute !== undefined && (typeof settings.api.rate_limit_per_minute !== 'number' || settings.api.rate_limit_per_minute < 1)) {
      errors.push("API rate limit must be at least 1 request per minute");
    }
  }
  
  // 監査ポリシーの検証
  if (settings.audit) {
    if (settings.audit.retention_days !== undefined && (typeof settings.audit.retention_days !== 'number' || settings.audit.retention_days < 30)) {
      errors.push("Audit log retention must be at least 30 days");
    }
  }
  
  // データポリシーの検証
  if (settings.data) {
    if (settings.data.max_export_records !== undefined && (typeof settings.data.max_export_records !== 'number' || settings.data.max_export_records < 1)) {
      errors.push("Maximum export records must be at least 1");
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
  
  return [
    {
      json: {
        success: true,
        settings: settings,
        user_id: items[0].json.user_id
      }
    }
  ];
}

// 5. 現在の設定の取得（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "SELECT * FROM security_settings",
  "additionalFields": {}
}

// 6. 設定の更新（Functionノード）
function prepareSettingsUpdate(items) {
  const newSettings = items[0].json.settings;
  const currentSettingsResult = items[1].json;
  const userId = items[0].json.user_id;
  
  // 現在の設定をマップに変換
  const currentSettings = {};
  
  if (currentSettingsResult && currentSettingsResult.length > 0) {
    for (const setting of currentSettingsResult) {
      if (!currentSettings[setting.category]) {
        currentSettings[setting.category] = {};
      }
      
      currentSettings[setting.category][setting.name] = setting.value;
    }
  }
  
  // 変更された設定を特定
  const changedSettings = [];
  
  for (const category in newSettings) {
    for (const name in newSettings[category]) {
      const newValue = newSettings[category][name];
      const currentValue = currentSettings[category]?.[name];
      
      // 値が変更された場合
      if (JSON.stringify(newValue) !== JSON.stringify(currentValue)) {
        changedSettings.push({
          category: category,
          name: name,
          old_value: currentValue,
          new_value: newValue
        });
      }
    }
  }
  
  // 更新用のレコードを作成
  const updateRecords = [];
  
  for (const category in newSettings) {
    for (const name in newSettings[category]) {
      updateRecords.push({
        category: category,
        name: name,
        value: newSettings[category][name],
        updated_at: new Date().toISOString(),
        updated_by: userId
      });
    }
  }
  
  // 監査イベントの作成
  const auditEvent = {
    event_type: 'SECURITY_POLICY_CHANGED',
    user_id: userId,
    details: {
      changed_settings: changedSettings
    }
  };
  
  return [
    {
      json: {
        success: true,
        update_records: updateRecords,
        changed_settings: changedSettings,
        audit_event: auditEvent
      }
    }
  ];
}

// 7. 設定の保存（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "DELETE FROM security_settings",
  "additionalFields": {}
}

// 8. 新しい設定の挿入（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "security_settings",
  "columns": "category, name, value, updated_at, updated_by",
  "additionalFields": {}
}

// 9. 監査ログの記録（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/audit/log",
  "method": "POST",
  "authentication": "none",
  "options": {}
}

// 10. 結果の返却（Respondノード）
// 設定例
{
  "respondWith": "json",
  "responseCode": 200
}
```

このようなセキュリティ設定の更新機能を実装することで、システムのセキュリティポリシーを適切に更新することができます。アクセス権限の確認、設定の検証、現在の設定の取得、設定の更新、監査ログの記録などの機能を含めることで、効果的なセキュリティ管理を実現することができます。

**セキュリティ監視と脅威検出**

システムのセキュリティ状態を監視し、潜在的な脅威を検出するための機能を実装します。

**セキュリティ監視の実装**:
システムのセキュリティ状態を監視するための機能を実装します。

```javascript
// セキュリティ監視の実装例（n8nワークフロー）

// 1. セキュリティ監視スケジュールトリガー（Cronノード）
// 設定例（15分ごとに実行）
{
  "triggerTimes": {
    "item": [
      {
        "mode": "everyX"
      }
    ]
  },
  "cronExpression": "*/15 * * * *"
}

// 2. 監視対象の取得（Functionノード）
function getMonitoringTargets() {
  // 監視対象の定義
  const monitoringTargets = [
    {
      id: 'failed_logins',
      name: 'ログイン失敗',
      description: '短時間内の複数回のログイン失敗を検出',
      query: `
        SELECT user_id, COUNT(*) as count
        FROM consensus_model_audit_logs
        WHERE event_type = 'USER_LOGIN_FAILURE'
        AND timestamp >= NOW() - INTERVAL '1 hour'
        GROUP BY user_id
        HAVING COUNT(*) >= 5
      `,
      threshold: 5,
      severity: 'warning'
    },
    {
      id: 'unauthorized_access',
      name: '不正アクセス試行',
      description: '権限のないリソースへのアクセス試行を検出',
      query: `
        SELECT user_id, COUNT(*) as count
        FROM consensus_model_audit_logs
        WHERE event_type = 'UNAUTHORIZED_ACCESS_ATTEMPT'
        AND timestamp >= NOW() - INTERVAL '1 hour'
        GROUP BY user_id
        HAVING COUNT(*) >= 3
      `,
      threshold: 3,
      severity: 'alert'
    },
    {
      id: 'api_rate_limit',
      name: 'APIレート制限超過',
      description: 'APIレート制限を超過したリクエストを検出',
      query: `
        SELECT user_id, COUNT(*) as count
        FROM consensus_model_audit_logs
        WHERE event_type = 'API_RATE_LIMIT_EXCEEDED'
        AND timestamp >= NOW() - INTERVAL '15 minutes'
        GROUP BY user_id
        HAVING COUNT(*) >= 2
      `,
      threshold: 2,
      severity: 'warning'
    },
    {
      id: 'security_changes',
      name: 'セキュリティ設定変更',
      description: 'セキュリティ設定の変更を検出',
      query: `
        SELECT *
        FROM consensus_model_audit_logs
        WHERE event_type = 'SECURITY_POLICY_CHANGED'
        AND timestamp >= NOW() - INTERVAL '1 day'
      `,
      threshold: 1,
      severity: 'info'
    },
    {
      id: 'admin_actions',
      name: '管理者アクション',
      description: '管理者による重要なアクションを検出',
      query: `
        SELECT *
        FROM consensus_model_audit_logs
        WHERE (
          event_type = 'USER_CREATED' OR
          event_type = 'USER_DELETED' OR
          event_type = 'ROLE_ASSIGNED' OR
          event_type = 'ROLE_REVOKED' OR
          event_type = 'PERMISSION_GRANTED' OR
          event_type = 'PERMISSION_REVOKED'
        )
        AND timestamp >= NOW() - INTERVAL '1 day'
      `,
      threshold: 1,
      severity: 'info'
    }
  ];
  
  return [
    {
      json: {
        monitoring_targets: monitoringTargets
      }
    }
  ];
}

// 3. 監視対象ごとの処理（SplitInBatchesノード）
// 設定例
{
  "batchSize": 1,
  "options": {}
}

// 4. 監視クエリの実行（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.query }}",
  "additionalFields": {}
}

// 5. 監視結果の処理（Functionノード）
function processMonitoringResult(items) {
  const target = items[0].json;
  const queryResult = items[1].json;
  
  // 結果がない場合は早期リターン
  if (!queryResult || queryResult.length === 0) {
    return [
      {
        json: {
          target_id: target.id,
          detected: false
        }
      }
    ];
  }
  
  // 検出フラグの設定
  const detected = queryResult.length > 0;
  
  // 検出された場合の処理
  if (detected) {
    // 通知メッセージの作成
    const notificationMessage = {
      subject: `[${target.severity.toUpperCase()}] セキュリティ監視アラート: ${target.name}`,
      body: `
セキュリティ監視システムによりアラートが検出されました。

アラート: ${target.name}
説明: ${target.description}
重要度: ${target.severity}
検出時刻: ${new Date().toLocaleString()}

検出詳細:
${JSON.stringify(queryResult, null, 2)}

このアラートは自動生成されたものです。
      `,
      recipients: ['security@example.com']
    };
    
    // 監査イベントの作成
    const auditEvent = {
      event_type: 'SECURITY_ALERT_DETECTED',
      details: {
        alert_id: target.id,
        alert_name: target.name,
        severity: target.severity,
        detection_count: queryResult.length,
        detection_details: queryResult
      }
    };
    
    return [
      {
        json: {
          target_id: target.id,
          detected: true,
          severity: target.severity,
          results: queryResult,
          notification: notificationMessage,
          audit_event: auditEvent
        }
      }
    ];
  }
  
  return [
    {
      json: {
        target_id: target.id,
        detected: false
      }
    }
  ];
}

// 6. 検出結果のフィルタリング（IFノード）
// 設定例
{
  "conditions": {
    "boolean": [
      {
        "value1": "={{ $json.detected }}",
        "value2": true
      }
    ]
  }
}

// 7. 通知の送信（Emailノード）
// 設定例
{
  "fromEmail": "security-monitor@example.com",
  "fromName": "セキュリティ監視システム",
  "toEmail": "={{ $json.notification.recipients.join(',') }}",
  "subject": "={{ $json.notification.subject }}",
  "text": "={{ $json.notification.body }}",
  "options": {}
}

// 8. 監査ログの記録（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/audit/log",
  "method": "POST",
  "authentication": "none",
  "options": {}
}

// 9. セキュリティアラートの保存（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "security_alerts",
  "columns": "alert_id, alert_name, severity, detection_time, detection_count, detection_details",
  "additionalFields": {}
}
```

このようなセキュリティ監視の実装により、システムのセキュリティ状態を定期的に監視し、潜在的な脅威を検出することができます。監視対象の取得、監視クエリの実行、監視結果の処理、通知の送信、監査ログの記録などの機能を含めることで、効果的なセキュリティ監視を実現することができます。

**脅威インテリジェンスの統合**:
外部の脅威インテリジェンスソースと統合し、既知の脅威を検出するための機能を実装します。

```javascript
// 脅威インテリジェンスの統合例（n8nワークフロー）

// 1. 脅威インテリジェンス更新スケジュールトリガー（Cronノード）
// 設定例（毎日午前3時に実行）
{
  "triggerTimes": {
    "item": [
      {
        "mode": "everyDay"
      }
    ]
  },
  "cronExpression": "0 3 * * *"
}

// 2. 脅威インテリジェンスソースの取得（Functionノード）
function getThreatIntelligenceSources() {
  // 脅威インテリジェンスソースの定義
  const threatIntelSources = [
    {
      id: 'malicious_ips',
      name: '悪意のあるIPアドレス',
      url: 'https://example.com/threat-intel/malicious-ips.txt',
      format: 'text',
      type: 'ip'
    },
    {
      id: 'tor_exit_nodes',
      name: 'Tor出口ノード',
      url: 'https://example.com/threat-intel/tor-exit-nodes.json',
      format: 'json',
      type: 'ip'
    },
    {
      id: 'malware_domains',
      name: 'マルウェアドメイン',
      url: 'https://example.com/threat-intel/malware-domains.csv',
      format: 'csv',
      type: 'domain'
    }
  ];
  
  return [
    {
      json: {
        threat_intel_sources: threatIntelSources
      }
    }
  ];
}

// 3. ソースごとの処理（SplitInBatchesノード）
// 設定例
{
  "batchSize": 1,
  "options": {}
}

// 4. 脅威データの取得（HTTPリクエストノード）
// 設定例
{
  "url": "={{ $json.url }}",
  "method": "GET",
  "authentication": "none",
  "options": {}
}

// 5. 脅威データの処理（Functionノード）
function processThreatData(items) {
  const source = items[0].json;
  const response = items[1].json;
  
  // フォーマットに応じた処理
  let threatEntries = [];
  
  switch (source.format) {
    case 'text':
      // テキスト形式の処理
      // 各行を1つのエントリとして扱う
      threatEntries = response.split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('#'));
      break;
    
    case 'json':
      // JSON形式の処理
      // レスポンスの構造に応じて適切に処理
      if (Array.isArray(response)) {
        threatEntries = response;
      } else if (response.data && Array.isArray(response.data)) {
        threatEntries = response.data;
      } else {
        // その他のJSON構造に応じて処理
        threatEntries = [];
      }
      break;
    
    case 'csv':
      // CSV形式の処理
      // 各行をカンマで分割して処理
      threatEntries = response.split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('#'))
        .map(line => {
          const parts = line.split(',');
          return parts[0]; // 最初のカラムを使用
        });
      break;
  }
  
  // 重複の除去
  threatEntries = [...new Set(threatEntries)];
  
  // 脅威データの作成
  const threatData = {
    source_id: source.id,
    source_name: source.name,
    type: source.type,
    entries: threatEntries,
    count: threatEntries.length,
    updated_at: new Date().toISOString()
  };
  
  return [
    {
      json: {
        threat_data: threatData
      }
    }
  ];
}

// 6. 脅威データの保存（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "DELETE FROM threat_intelligence WHERE source_id = $1",
  "additionalFields": {}
}

// 7. 新しい脅威データの挿入（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "threat_intelligence",
  "columns": "source_id, source_name, type, entry, updated_at",
  "additionalFields": {}
}

// 8. 更新ログの記録（Functionノード）
function createUpdateLog(items) {
  const threatData = items[0].json.threat_data;
  
  // 監査イベントの作成
  const auditEvent = {
    event_type: 'THREAT_INTELLIGENCE_UPDATED',
    details: {
      source_id: threatData.source_id,
      source_name: threatData.source_name,
      type: threatData.type,
      entry_count: threatData.count,
      updated_at: threatData.updated_at
    }
  };
  
  return [
    {
      json: {
        audit_event: auditEvent
      }
    }
  ];
}

// 9. 監査ログの記録（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/audit/log",
  "method": "POST",
  "authentication": "none",
  "options": {}
}
```

このような脅威インテリジェンスの統合により、外部の脅威インテリジェンスソースからデータを取得し、システムに統合することができます。脅威インテリジェンスソースの取得、脅威データの取得、脅威データの処理、脅威データの保存、更新ログの記録などの機能を含めることで、効果的な脅威検出を実現することができます。

**脅威検出の実装**:
統合された脅威インテリジェンスを活用して、システム内の潜在的な脅威を検出するための機能を実装します。

```javascript
// 脅威検出の実装例（n8nワークフロー）

// 1. 脅威検出スケジュールトリガー（Cronノード）
// 設定例（1時間ごとに実行）
{
  "triggerTimes": {
    "item": [
      {
        "mode": "everyX"
      }
    ]
  },
  "cronExpression": "0 * * * *"
}

// 2. 検出ルールの取得（Functionノード）
function getDetectionRules() {
  // 検出ルールの定義
  const detectionRules = [
    {
      id: 'malicious_ip_login',
      name: '悪意のあるIPからのログイン',
      description: '既知の悪意のあるIPアドレスからのログイン試行を検出',
      query: `
        SELECT a.*, t.source_name as threat_source
        FROM consensus_model_audit_logs a
        JOIN threat_intelligence t ON a.ip_address = t.entry
        WHERE a.event_type IN ('USER_LOGIN', 'USER_LOGIN_FAILURE')
        AND a.timestamp >= NOW() - INTERVAL '1 day'
        AND t.type = 'ip'
      `,
      severity: 'critical'
    },
    {
      id: 'tor_access',
      name: 'Tor経由のアクセス',
      description: 'Tor出口ノードからのアクセスを検出',
      query: `
        SELECT a.*, t.source_name as threat_source
        FROM consensus_model_audit_logs a
        JOIN threat_intelligence t ON a.ip_address = t.entry
        WHERE a.timestamp >= NOW() - INTERVAL '1 day'
        AND t.source_id = 'tor_exit_nodes'
      `,
      severity: 'alert'
    },
    {
      id: 'malware_domain_access',
      name: 'マルウェアドメインへのアクセス',
      description: '既知のマルウェアドメインへのアクセスを検出',
      query: `
        SELECT a.*, t.source_name as threat_source
        FROM consensus_model_audit_logs a
        JOIN threat_intelligence t ON a.details->>'domain' = t.entry
        WHERE a.event_type = 'EXTERNAL_REQUEST'
        AND a.timestamp >= NOW() - INTERVAL '1 day'
        AND t.type = 'domain'
      `,
      severity: 'critical'
    },
    {
      id: 'account_takeover',
      name: 'アカウント乗っ取り',
      description: '同一アカウントの異なるIPアドレスからの短時間内のログインを検出',
      query: `
        SELECT
          a1.user_id,
          a1.ip_address as ip_address_1,
          a2.ip_address as ip_address_2,
          a1.timestamp as timestamp_1,
          a2.timestamp as timestamp_2
        FROM consensus_model_audit_logs a1
        JOIN consensus_model_audit_logs a2 ON a1.user_id = a2.user_id
        WHERE a1.event_type = 'USER_LOGIN'
        AND a2.event_type = 'USER_LOGIN'
        AND a1.ip_address != a2.ip_address
        AND a1.timestamp >= NOW() - INTERVAL '1 day'
        AND a2.timestamp >= NOW() - INTERVAL '1 day'
        AND a2.timestamp - a1.timestamp < INTERVAL '30 minutes'
      `,
      severity: 'alert'
    },
    {
      id: 'privilege_escalation',
      name: '権限昇格',
      description: '短時間内の権限の変更を検出',
      query: `
        SELECT *
        FROM consensus_model_audit_logs
        WHERE event_type IN ('ROLE_ASSIGNED', 'PERMISSION_GRANTED')
        AND timestamp >= NOW() - INTERVAL '1 day'
        AND details->>'role_id' = 'ADMIN'
      `,
      severity: 'alert'
    }
  ];
  
  return [
    {
      json: {
        detection_rules: detectionRules
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

// 4. 検出クエリの実行（PostgreSQLノード）
// 設定例
{
  "operation": "executeQuery",
  "query": "={{ $json.query }}",
  "additionalFields": {}
}

// 5. 検出結果の処理（Functionノード）
function processDetectionResult(items) {
  const rule = items[0].json;
  const queryResult = items[1].json;
  
  // 結果がない場合は早期リターン
  if (!queryResult || queryResult.length === 0) {
    return [
      {
        json: {
          rule_id: rule.id,
          detected: false
        }
      }
    ];
  }
  
  // 検出フラグの設定
  const detected = queryResult.length > 0;
  
  // 検出された場合の処理
  if (detected) {
    // 通知メッセージの作成
    const notificationMessage = {
      subject: `[${rule.severity.toUpperCase()}] セキュリティ脅威検出: ${rule.name}`,
      body: `
セキュリティ脅威検出システムにより脅威が検出されました。

脅威: ${rule.name}
説明: ${rule.description}
重要度: ${rule.severity}
検出時刻: ${new Date().toLocaleString()}
検出数: ${queryResult.length}

検出詳細:
${JSON.stringify(queryResult, null, 2)}

このアラートは自動生成されたものです。緊急の対応が必要な場合があります。
      `,
      recipients: ['security@example.com', 'admin@example.com']
    };
    
    // 監査イベントの作成
    const auditEvent = {
      event_type: 'SECURITY_THREAT_DETECTED',
      details: {
        rule_id: rule.id,
        rule_name: rule.name,
        severity: rule.severity,
        detection_count: queryResult.length,
        detection_details: queryResult
      }
    };
    
    return [
      {
        json: {
          rule_id: rule.id,
          detected: true,
          severity: rule.severity,
          results: queryResult,
          notification: notificationMessage,
          audit_event: auditEvent
        }
      }
    ];
  }
  
  return [
    {
      json: {
        rule_id: rule.id,
        detected: false
      }
    }
  ];
}

// 6. 検出結果のフィルタリング（IFノード）
// 設定例
{
  "conditions": {
    "boolean": [
      {
        "value1": "={{ $json.detected }}",
        "value2": true
      }
    ]
  }
}

// 7. 通知の送信（Emailノード）
// 設定例
{
  "fromEmail": "security-threat@example.com",
  "fromName": "セキュリティ脅威検出システム",
  "toEmail": "={{ $json.notification.recipients.join(',') }}",
  "subject": "={{ $json.notification.subject }}",
  "text": "={{ $json.notification.body }}",
  "options": {}
}

// 8. 監査ログの記録（HTTPリクエストノード）
// 設定例
{
  "url": "http://localhost:5678/webhook/consensus-model/audit/log",
  "method": "POST",
  "authentication": "none",
  "options": {}
}

// 9. セキュリティ脅威の保存（PostgreSQLノード）
// 設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "security_threats",
  "columns": "rule_id, rule_name, severity, detection_time, detection_count, detection_details, status",
  "additionalFields": {}
}
```

このような脅威検出の実装により、統合された脅威インテリジェンスを活用して、システム内の潜在的な脅威を検出することができます。検出ルールの取得、検出クエリの実行、検出結果の処理、通知の送信、監査ログの記録などの機能を含めることで、効果的な脅威検出を実現することができます。

これらの監査・セキュリティ管理機能により、コンセンサスモデルの信頼性、完全性、機密性を確保することができます。n8nを活用することで、これらの監査・セキュリティ機能を効率的に実装することが可能になり、システムの利用状況を追跡し、不正アクセスや不適切な操作を防止することができます。
