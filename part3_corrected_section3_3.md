### 3.3. n8nワークフローとの連携

前節で設計した視覚化コンポーネントを実際のシステムとして機能させるためには、n8nワークフローとの効果的な連携が不可欠です。このセクションでは、n8nワークフローからデータを取得し、視覚化コンポーネントに提供する方法、そして視覚化インターフェースからのフィードバックをn8nワークフローに反映させる方法について詳細に解説します。

#### データ提供APIの設計と実装

視覚化コンポーネントに必要なデータを提供するためのAPIエンドポイントを、n8nワークフローとして設計・実装することが重要です。これらのAPIは、フロントエンドからのリクエストに応じて、必要なデータを適切な形式で返す役割を担います。

以下は、n8nで実装するデータ提供APIの例です。このワークフローは、特定のトピックに関する視点別評価データ、重み付け情報、時系列データなどを提供します。

```javascript
// n8n workflow: Data Provider API for Visualization
// Webhook Node: GET /api/topic/:topicId/visualization-data

// Function Node: Prepare Database Queries
const topicId = $node["Webhook"].json.params.topicId;
if (!topicId) {
  return {
    json: {
      error: true,
      message: "Topic ID is required"
    }
  };
}

// データベースクエリの準備
const queries = {
  perspectiveData: `
    SELECT 
      perspective,
      importance_score,
      confidence_score,
      impact_range,
      strategic_relevance,
      temporal_urgency
    FROM 
      perspective_evaluations
    WHERE 
      topic_id = '${topicId}'
    ORDER BY 
      created_at DESC
    LIMIT 3
  `,
  
  weightData: `
    SELECT 
      weights,
      adjustment_factors
    FROM 
      topic_weights
    WHERE 
      topic_id = '${topicId}'
    ORDER BY 
      created_at DESC
    LIMIT 1
  `,
  
  timeSeriesData: `
    SELECT 
      date_trunc('day', created_at) as date,
      integrated_score,
      weights
    FROM 
      topic_evaluations
    WHERE 
      topic_id = '${topicId}'
    AND
      created_at >= NOW() - INTERVAL '30 days'
    ORDER BY 
      date
  `,
  
  relationshipData: `
    SELECT 
      perspective_pair,
      coherence_score,
      relationship_type
    FROM 
      perspective_relationships
    WHERE 
      topic_id = '${topicId}'
    ORDER BY 
      created_at DESC
    LIMIT 3
  `
};

return { json: { queries } };

// PostgreSQL Node: Execute Queries
// 上記で準備したクエリを実行

// Function Node: Transform Data for Visualization
const perspectiveResults = $node["PostgreSQL"].json.perspectiveData;
const weightResults = $node["PostgreSQL"].json.weightData;
const timeSeriesResults = $node["PostgreSQL"].json.timeSeriesData;
const relationshipResults = $node["PostgreSQL"].json.relationshipData;

// 視点別データの変換
const perspectiveData = {
  technology: [],
  market: [],
  business: []
};

perspectiveResults.forEach(row => {
  const perspective = row.perspective.toLowerCase();
  if (perspectiveData[perspective]) {
    perspectiveData[perspective] = [
      row.importance_score,
      row.confidence_score,
      row.coherence_score || 0.5, // デフォルト値
      row.impact_range,
      row.strategic_relevance,
      row.temporal_urgency
    ];
  }
});

// 重み付けデータの変換
const weightData = weightResults.length > 0 ? {
  weights: weightResults[0].weights,
  adjustmentFactors: weightResults[0].adjustment_factors
} : {
  weights: { technology: 0.33, market: 0.33, business: 0.34 },
  adjustmentFactors: {}
};

// 時系列データの変換
const timeSeriesData = {
  dates: [],
  integratedScores: [],
  weights: {
    technology: [],
    market: [],
    business: []
  }
};

timeSeriesResults.forEach(row => {
  timeSeriesData.dates.push(row.date);
  timeSeriesData.integratedScores.push(row.integrated_score);
  
  if (row.weights) {
    timeSeriesData.weights.technology.push(row.weights.technology || 0.33);
    timeSeriesData.weights.market.push(row.weights.market || 0.33);
    timeSeriesData.weights.business.push(row.weights.business || 0.34);
  }
});

// 関係性データの変換
const relationshipData = {
  technology_market: { coherence: 0.5, type: "neutral" },
  market_business: { coherence: 0.5, type: "neutral" },
  business_technology: { coherence: 0.5, type: "neutral" }
};

relationshipResults.forEach(row => {
  const pair = row.perspective_pair.toLowerCase();
  if (pair === "technology_market" || pair === "market_technology") {
    relationshipData.technology_market = {
      coherence: row.coherence_score,
      type: row.relationship_type
    };
  } else if (pair === "market_business" || pair === "business_market") {
    relationshipData.market_business = {
      coherence: row.coherence_score,
      type: row.relationship_type
    };
  } else if (pair === "business_technology" || pair === "technology_business") {
    relationshipData.business_technology = {
      coherence: row.coherence_score,
      type: row.relationship_type
    };
  }
});

// 最終的なレスポンスデータの構築
const visualizationData = {
  topicId,
  perspectiveData,
  weightData,
  timeSeriesData,
  relationshipData
};

return { json: visualizationData };

// Respond to Webhook
// 上記で構築したデータをJSON形式でレスポンス
```

このn8nワークフローは、WebhookノードでHTTPリクエストを受け取り、Function Nodeでデータベースクエリを準備し、PostgreSQLノードでクエリを実行し、別のFunction Nodeでデータを視覚化コンポーネント用に変換し、最終的にWebhookレスポンスとして返します。

このAPIは、フロントエンドアプリケーションから以下のように呼び出すことができます。

```javascript
// React component: Data Fetching Example
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PerspectiveRadarChart from './PerspectiveRadarChart';
import TimeSeriesGraph from './TimeSeriesGraph';
import PerspectiveRelationshipGraph from './PerspectiveRelationshipGraph';

const VisualizationDashboard = ({ topicId }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [visualizationData, setVisualizationData] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/topic/${topicId}/visualization-data`);
        setVisualizationData(response.data);
        setError(null);
      } catch (err) {
        console.error('Error fetching visualization data:', err);
        setError('データの取得中にエラーが発生しました。');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    
    // 定期的な更新（オプション）
    const intervalId = setInterval(fetchData, 60000); // 1分ごとに更新
    
    return () => clearInterval(intervalId); // コンポーネントのアンマウント時にクリア
  }, [topicId]);
  
  if (loading) return <div className="loading-spinner">データを読み込み中...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!visualizationData) return null;
  
  return (
    <div className="visualization-dashboard">
      <h2>トピック分析ダッシュボード</h2>
      
      <div className="dashboard-grid">
        <div className="grid-item">
          <PerspectiveRadarChart 
            perspectiveData={visualizationData.perspectiveData} 
            weights={visualizationData.weightData.weights} 
          />
        </div>
        
        <div className="grid-item">
          <TimeSeriesGraph 
            timeSeriesData={visualizationData.timeSeriesData}
            timeRange="month"
          />
        </div>
        
        <div className="grid-item">
          <PerspectiveRelationshipGraph 
            relationshipData={visualizationData.relationshipData} 
          />
        </div>
      </div>
    </div>
  );
};

export default VisualizationDashboard;
```

このReactコンポーネントは、指定されたトピックIDに基づいてAPIからデータを取得し、3つの視覚化コンポーネント（レーダーチャート、時系列グラフ、関係性グラフ）にデータを提供します。データの読み込み中はローディングスピナーを表示し、エラーが発生した場合はエラーメッセージを表示します。また、定期的な更新機能も実装されており、最新のデータを自動的に取得します。

データ提供APIの設計と実装においては、パフォーマンスとスケーラビリティを考慮することが重要です。大量のデータや頻繁なリクエストが予想される場合は、キャッシュ機構の導入や、データの事前集計、ページネーションなどの最適化技術を検討すべきです。また、セキュリティ面でも、適切な認証・認可の仕組みを実装し、不正アクセスやデータ漏洩を防止することが必要です。

#### フィードバック処理ワークフローの実装

視覚化インターフェースからのフィードバック（重み調整、閾値変更など）をn8nワークフローで処理し、システムに反映させる仕組みも重要です。これにより、ユーザーの判断や調整がシステムの動作に直接影響を与えることができます。

以下は、n8nで実装するフィードバック処理ワークフローの例です。このワークフローは、ユーザーが調整した重みや閾値を受け取り、システムに反映します。

```javascript
// n8n workflow: Feedback Processing API
// Webhook Node: POST /api/topic/:topicId/adjust-parameters

// Function Node: Validate Input
const topicId = $node["Webhook"].json.params.topicId;
const adjustedParameters = $node["Webhook"].json.body;

// 入力バリデーション
if (!topicId) {
  return {
    json: {
      error: true,
      message: "Topic ID is required"
    }
  };
}

if (!adjustedParameters) {
  return {
    json: {
      error: true,
      message: "Adjusted parameters are required"
    }
  };
}

// 重みのバリデーション
if (adjustedParameters.weights) {
  const weights = adjustedParameters.weights;
  if (!weights.technology || !weights.market || !weights.business) {
    return {
      json: {
        error: true,
        message: "All perspective weights (technology, market, business) are required"
      }
    };
  }
  
  const sum = weights.technology + weights.market + weights.business;
  if (Math.abs(sum - 1.0) > 0.01) {
    return {
      json: {
        error: true,
        message: "Sum of weights must be 1.0"
      }
    };
  }
}

// 閾値のバリデーション
if (adjustedParameters.thresholds) {
  const thresholds = adjustedParameters.thresholds;
  ['high', 'medium_high', 'medium', 'medium_low', 'low'].forEach(level => {
    if (thresholds[level] === undefined || thresholds[level] < 0 || thresholds[level] > 1) {
      return {
        json: {
          error: true,
          message: `Invalid threshold for level ${level}`
        }
      };
    }
  });
  
  // 閾値の順序チェック
  if (!(thresholds.high > thresholds.medium_high && 
        thresholds.medium_high > thresholds.medium && 
        thresholds.medium > thresholds.medium_low && 
        thresholds.medium_low > thresholds.low)) {
    return {
      json: {
        error: true,
        message: "Thresholds must be in descending order: high > medium_high > medium > medium_low > low"
      }
    };
  }
}

// 調整理由の記録（オプション）
const adjustmentReason = adjustedParameters.reason || "Manual adjustment by user";
const userId = adjustedParameters.user_id || "anonymous";

return { 
  json: { 
    topicId,
    adjustedParameters,
    adjustmentReason,
    userId,
    timestamp: new Date().toISOString()
  } 
};

// PostgreSQL Node: Save Adjusted Parameters
// 調整されたパラメータをデータベースに保存

// Function Node: Apply Adjustments
// 調整されたパラメータをシステムに適用し、必要に応じて再評価を実行

// 重みの適用
if (adjustedParameters.weights) {
  // 重みを適用するロジック
  // ...
}

// 閾値の適用
if (adjustedParameters.thresholds) {
  // 閾値を適用するロジック
  // ...
}

// 調整履歴の記録
const adjustmentHistory = {
  topic_id: topicId,
  user_id: userId,
  timestamp: new Date().toISOString(),
  parameters: adjustedParameters,
  reason: adjustmentReason
};

// 再評価の実行（必要に応じて）
let reevaluationResults = null;
if (adjustedParameters.run_reevaluation) {
  // トピックの再評価を実行するロジック
  // ...
  reevaluationResults = {
    // 再評価結果
  };
}

return {
  json: {
    success: true,
    message: "Parameters adjusted successfully",
    adjustment_id: $node["PostgreSQL"].json.id,
    reevaluation_results: reevaluationResults
  }
};

// Respond to Webhook
// 処理結果をJSON形式でレスポンス
```

このn8nワークフローは、WebhookノードでHTTPリクエストを受け取り、Function Nodeで入力をバリデーションし、PostgreSQLノードで調整されたパラメータをデータベースに保存し、別のFunction Nodeでパラメータを適用して必要に応じて再評価を実行し、最終的にWebhookレスポンスとして結果を返します。

このAPIは、フロントエンドアプリケーションから以下のように呼び出すことができます。

```javascript
// React component: Parameter Adjustment Example
import React, { useState } from 'react';
import axios from 'axios';
import WeightAdjustmentInterface from './WeightAdjustmentInterface';

const ParameterAdjustmentPanel = ({ topicId, initialParameters, onAdjustmentComplete }) => {
  const [adjusting, setAdjusting] = useState(false);
  const [error, setError] = useState(null);
  const [adjustmentResult, setAdjustmentResult] = useState(null);
  
  const handleAdjustment = async (adjustedParameters) => {
    try {
      setAdjusting(true);
      setError(null);
      
      // 調整理由と実行オプションを追加
      const payload = {
        ...adjustedParameters,
        reason: adjustedParameters.reason || "Manual adjustment",
        user_id: "current_user_id", // 実際のユーザーIDに置き換え
        run_reevaluation: adjustedParameters.run_reevaluation || false
      };
      
      const response = await axios.post(`/api/topic/${topicId}/adjust-parameters`, payload);
      setAdjustmentResult(response.data);
      
      if (onAdjustmentComplete) {
        onAdjustmentComplete(response.data);
      }
    } catch (err) {
      console.error('Error adjusting parameters:', err);
      setError('パラメータの調整中にエラーが発生しました。');
    } finally {
      setAdjusting(false);
    }
  };
  
  return (
    <div className="parameter-adjustment-panel">
      <h3>パラメータ調整</h3>
      
      {error && <div className="error-message">{error}</div>}
      
      <WeightAdjustmentInterface 
        initialWeights={initialParameters.weights}
        onWeightsChange={(weights) => handleAdjustment({ weights })}
        disabled={adjusting}
      />
      
      {/* 閾値調整インターフェース（別コンポーネント） */}
      
      <div className="adjustment-options">
        <label>
          <input 
            type="checkbox" 
            checked={initialParameters.run_reevaluation || false}
            onChange={(e) => handleAdjustment({ 
              ...initialParameters, 
              run_reevaluation: e.target.checked 
            })}
            disabled={adjusting}
          />
          調整後に再評価を実行
        </label>
        
        <div className="reason-input">
          <label>調整理由:</label>
          <input 
            type="text" 
            value={initialParameters.reason || ""}
            onChange={(e) => handleAdjustment({ 
              ...initialParameters, 
              reason: e.target.value 
            })}
            placeholder="例: マーケット視点の重要性が増したため"
            disabled={adjusting}
          />
        </div>
      </div>
      
      {adjusting && <div className="loading-spinner">調整中...</div>}
      
      {adjustmentResult && (
        <div className="adjustment-result">
          <p>調整が完了しました（ID: {adjustmentResult.adjustment_id}）</p>
          {adjustmentResult.reevaluation_results && (
            <div className="reevaluation-results">
              <h4>再評価結果:</h4>
              {/* 再評価結果の表示 */}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ParameterAdjustmentPanel;
```

このReactコンポーネントは、重み調整インターフェースを表示し、ユーザーが調整した重みをAPIに送信します。また、再評価の実行オプションや調整理由の入力フィールドも提供し、調整プロセスの透明性と追跡可能性を高めています。調整中はローディングスピナーを表示し、エラーが発生した場合はエラーメッセージを表示します。調整が完了すると、結果と再評価結果（実行された場合）を表示します。

フィードバック処理ワークフローの実装においては、ユーザーの意図を正確に反映することと、システムの整合性を維持することのバランスが重要です。ユーザーの調整が不適切な結果を招く可能性がある場合は、警告を表示したり、調整範囲に制限を設けたりすることも検討すべきです。また、調整履歴を記録し、必要に応じて以前の設定に戻せるようにすることも有用です。

#### リアルタイム更新の実装

コンセンサスモデルの評価結果や重み付けが更新された際に、視覚化インターフェースをリアルタイムで更新する仕組みも重要です。これにより、ユーザーは常に最新の情報に基づいて判断を行うことができます。

リアルタイム更新の実装には、WebSocketやServer-Sent Events（SSE）などの技術が適しています。以下は、n8nとWebSocketを使用したリアルタイム更新の実装例です。

```javascript
// n8n workflow: Real-time Update Notification
// Function Node: Send WebSocket Notification
const WebSocket = require('ws');

async function sendWebSocketNotification(event) {
  try {
    // WebSocketサーバーに接続
    const ws = new WebSocket('ws://websocket-server:8080');
    
    // 接続が開いたらメッセージを送信
    ws.on('open', function open() {
      const message = JSON.stringify({
        type: 'update',
        topic_id: event.topic_id,
        update_type: event.update_type,
        timestamp: new Date().toISOString(),
        data: event.data
      });
      
      ws.send(message);
      console.log(`WebSocket notification sent for topic ${event.topic_id}`);
      
      // メッセージ送信後に接続を閉じる
      ws.close();
    });
    
    // エラーハンドリング
    ws.on('error', function error(err) {
      console.error(`WebSocket error: ${err.message}`);
    });
    
    // 一定時間後にタイムアウト
    setTimeout(() => {
      if (ws.readyState === WebSocket.CONNECTING) {
        ws.terminate();
        console.error('WebSocket connection timed out');
      }
    }, 5000);
    
    return true;
  } catch (error) {
    console.error(`Error sending WebSocket notification: ${error.message}`);
    return false;
  }
}

// イベントデータ（他のノードから渡される）
const event = {
  topic_id: $node["Trigger"].json.topic_id,
  update_type: $node["Trigger"].json.update_type,
  data: $node["Trigger"].json.data
};

// WebSocket通知を送信
const result = await sendWebSocketNotification(event);

return { json: { notification_sent: result } };
```

このn8nワークフローは、トピックの更新イベントが発生した際に、WebSocketサーバーを通じてクライアントに通知を送信します。この通知を受け取ったクライアントは、必要に応じてデータを再取得し、視覚化コンポーネントを更新します。

フロントエンドでのWebSocket接続と更新処理は、以下のように実装できます。

```javascript
// React component: Real-time Update Example
import React, { useState, useEffect } from 'react';
import VisualizationDashboard from './VisualizationDashboard';

const RealtimeTopicMonitor = ({ topicId }) => {
  const [lastUpdate, setLastUpdate] = useState(null);
  const [updateCount, setUpdateCount] = useState(0);
  const [key, setKey] = useState(0); // コンポーネントの強制再レンダリング用
  
  useEffect(() => {
    // WebSocketサーバーに接続
    const ws = new WebSocket('ws://websocket-server:8080');
    
    ws.onopen = () => {
      console.log('WebSocket connection established');
      
      // トピック監視のサブスクリプションを送信
      ws.send(JSON.stringify({
        type: 'subscribe',
        topic_id: topicId
      }));
    };
    
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        
        // 関連するトピックの更新通知のみ処理
        if (message.type === 'update' && message.topic_id === topicId) {
          console.log(`Received update for topic ${topicId}:`, message);
          
          // 最終更新情報を更新
          setLastUpdate({
            timestamp: message.timestamp,
            type: message.update_type
          });
          
          // 更新カウンターをインクリメント
          setUpdateCount(prev => prev + 1);
          
          // ダッシュボードコンポーネントを強制的に再レンダリング
          setKey(prev => prev + 1);
        }
      } catch (error) {
        console.error('Error processing WebSocket message:', error);
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };
    
    // コンポーネントのアンマウント時に接続をクローズ
    return () => {
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close();
      }
    };
  }, [topicId]);
  
  return (
    <div className="realtime-topic-monitor">
      <div className="update-status">
        <span className="update-indicator"></span>
        {lastUpdate ? (
          <p>
            最終更新: {new Date(lastUpdate.timestamp).toLocaleString()} 
            ({lastUpdate.type})
          </p>
        ) : (
          <p>更新を監視中...</p>
        )}
        <p>更新回数: {updateCount}</p>
      </div>
      
      {/* キーを変更することで強制的に再レンダリング */}
      <VisualizationDashboard key={key} topicId={topicId} />
    </div>
  );
};

export default RealtimeTopicMonitor;
```

このReactコンポーネントは、WebSocketサーバーに接続し、指定されたトピックの更新通知を監視します。更新通知を受信すると、最終更新情報を表示し、VisualizationDashboardコンポーネントを強制的に再レンダリングして最新のデータを表示します。また、更新回数も表示し、システムが正常に動作していることをユーザーに示します。

リアルタイム更新の実装においては、接続の安定性とリソース効率のバランスが重要です。接続が切断された場合の再接続メカニズムや、不要な更新を減らすためのフィルタリング機能を実装することが望ましいです。また、多数のクライアントが同時に接続する場合は、スケーラブルなWebSocketサーバーの構築や、メッセージブローカー（RabbitMQ、Kafkaなど）の活用も検討すべきです。

以上のように、n8nワークフローと視覚化コンポーネントを効果的に連携させることで、コンセンサスモデルの出力を直感的に理解し、活用するための強力なインターフェースを実現することができます。次のセクションでは、このインターフェースを用いた実際の運用例とユースケースについて解説します。
