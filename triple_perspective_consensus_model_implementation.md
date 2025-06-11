# インタラクティブダッシュボードの全体設計と実装要件

## インタラクティブダッシュボードの目的と役割

トリプルパースペクティブ型戦略AIレーダーにおけるインタラクティブダッシュボードは、複雑な情報を直感的に理解し、効果的な意思決定を支援するための中核的なインターフェースです。本セクションでは、ダッシュボードの全体設計と実装要件について詳細に解説します。

### ダッシュボードの主要目的

1. **情報の統合と可視化**
   - 複数の情報源からのデータを統合
   - 複雑な関係性を直感的に理解できる形で可視化
   - 情報の重要度と確信度を明示

2. **意思決定支援**
   - 代替シナリオの比較検討を促進
   - 不確実性と情報不均衡の影響を明示
   - アクションの優先順位付けを支援

3. **継続的モニタリング**
   - 重要指標の時間的変化を追跡
   - 変化点と異常値を検出
   - 予測と実績の乖離を監視

4. **コラボレーション促進**
   - 知見の共有と議論の活性化
   - 異なる視点からの評価の統合
   - 組織的な意思決定プロセスの支援

## ダッシュボードのアーキテクチャ設計

インタラクティブダッシュボードは、以下のアーキテクチャに基づいて設計されます。

### 全体アーキテクチャ

```
+----------------------------------+
|           フロントエンド           |
|  +----------------------------+  |
|  |      React アプリケーション     |  |
|  +----------------------------+  |
|  |   可視化コンポーネント群       |  |
|  | (D3.js, Chart.js, React-vis) |  |
|  +----------------------------+  |
+----------------------------------+
              ↑↓
+----------------------------------+
|          ミドルウェア             |
|  +----------------------------+  |
|  |     n8n ワークフロー         |  |
|  +----------------------------+  |
|  |    データ処理・変換ノード     |  |
|  +----------------------------+  |
+----------------------------------+
              ↑↓
+----------------------------------+
|          バックエンド             |
|  +----------------------------+  |
|  |    コンセンサスモデル        |  |
|  +----------------------------+  |
|  |    情報収集・分析システム    |  |
|  +----------------------------+  |
|  |    予測エンジン             |  |
|  +----------------------------+  |
+----------------------------------+
```

### コンポーネント構成

1. **フロントエンドコンポーネント**
   - ダッシュボードコンテナ
   - ナビゲーションシステム
   - 可視化コンポーネント群
   - インタラクションコントローラ
   - 設定・カスタマイズパネル

2. **ミドルウェアコンポーネント**
   - データ取得・変換ワークフロー
   - リアルタイム更新ハンドラ
   - キャッシュ・パフォーマンス最適化
   - セキュリティ・認証レイヤー

3. **バックエンドコンポーネント**
   - データストレージ・管理
   - 分析・予測エンジン
   - コンセンサスモデル
   - API・インテグレーションレイヤー

## ダッシュボードのレイアウトとナビゲーション

### 基本レイアウト

```
+--------------------------------------------------+
|                  ヘッダー                         |
| [ロゴ] [タイトル]        [設定] [ユーザー] [通知] |
+--------------------------------------------------+
|        |                                         |
|        |                                         |
|  サイド |              メインコンテンツ            |
|  バー  |                                         |
|        |                                         |
|        |                                         |
+--------------------------------------------------+
|                  フッター                         |
| [ステータス] [更新情報]        [ヘルプ] [フィードバック] |
+--------------------------------------------------+
```

### ナビゲーション構造

```
トップレベルナビゲーション
├── ホーム / 概要
├── 視点別分析
│   ├── テクノロジー視点
│   ├── マーケット視点
│   └── ビジネス視点
├── 統合分析
│   ├── コンセンサスモデル
│   ├── 静止点分析
│   └── 情報不均衡評価
├── シナリオ分析
│   ├── シナリオ比較
│   ├── 時間的推移
│   └── 予測シミュレーション
└── 設定 / カスタマイズ
    ├── ダッシュボード設定
    ├── アラート設定
    └── データソース管理
```

### レスポンシブデザイン

ダッシュボードは以下のデバイスタイプに対応するレスポンシブデザインを採用します：

1. **デスクトップ（1200px以上）**
   - フル機能表示
   - 複数の可視化を同時表示
   - 詳細な分析ツール

2. **タブレット（768px〜1199px）**
   - 主要機能の維持
   - 一部可視化の簡略化
   - タッチ操作の最適化

3. **モバイル（767px以下）**
   - 必須機能のみ表示
   - 縦長レイアウトへの再構成
   - シンプルな操作性重視

## ダッシュボードの主要セクション

インタラクティブダッシュボードは、以下の主要セクションで構成されます。

### 1. 概要ダッシュボード

概要ダッシュボードは、システム全体の状態を一目で把握するためのトップレベルビューを提供します。

#### 実装要件

```javascript
// n8n workflow: Overview Dashboard Data
// Function node for generating overview data
[
  {
    "id": "generateOverviewData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Various data from different sources
        const topicData = $input.item.json.topic_data || [];
        const perspectiveScores = $input.item.json.perspective_scores || {};
        const equilibriumStatus = $input.item.json.equilibrium_status || {};
        const recentChanges = $input.item.json.recent_changes || [];
        
        // Prepare overview data
        const overviewData = {
          // Summary metrics
          summary_metrics: {
            total_topics: topicData.length,
            equilibrium_topics: topicData.filter(t => t.is_equilibrium).length,
            high_confidence_topics: topicData.filter(t => t.confidence > 0.7).length,
            information_imbalance_topics: topicData.filter(t => t.has_information_imbalance).length
          },
          
          // Perspective summary
          perspective_summary: {
            technology: {
              average_score: calculateAverageScore(perspectiveScores.technology || []),
              trend: calculateTrend(perspectiveScores.technology || []),
              top_topics: getTopTopics(topicData, 'technology', 3)
            },
            market: {
              average_score: calculateAverageScore(perspectiveScores.market || []),
              trend: calculateTrend(perspectiveScores.market || []),
              top_topics: getTopTopics(topicData, 'market', 3)
            },
            business: {
              average_score: calculateAverageScore(perspectiveScores.business || []),
              trend: calculateTrend(perspectiveScores.business || []),
              top_topics: getTopTopics(topicData, 'business', 3)
            }
          },
          
          // Recent changes
          recent_changes: recentChanges.slice(0, 5).map(change => ({
            topic_id: change.topic_id,
            topic_name: change.topic_name,
            change_type: change.change_type,
            perspective: change.perspective,
            magnitude: change.magnitude,
            timestamp: change.timestamp,
            description: change.description
          })),
          
          // Equilibrium status
          equilibrium_status: {
            current_equilibrium_topics: equilibriumStatus.current_equilibrium_topics || [],
            potential_equilibrium_topics: equilibriumStatus.potential_equilibrium_topics || [],
            equilibrium_trend: equilibriumStatus.trend || 'stable'
          }
        };
        
        return {
          json: overviewData
        };
        
        // Helper function: Calculate average score
        function calculateAverageScore(scores) {
          if (!scores || scores.length === 0) return 0;
          return scores.reduce((sum, score) => sum + score, 0) / scores.length;
        }
        
        // Helper function: Calculate trend
        function calculateTrend(scores) {
          if (!scores || scores.length < 2) return 'stable';
          
          const recentScores = scores.slice(-5);
          const firstScore = recentScores[0];
          const lastScore = recentScores[recentScores.length - 1];
          
          const difference = lastScore - firstScore;
          
          if (difference > 0.05) return 'increasing';
          if (difference < -0.05) return 'decreasing';
          return 'stable';
        }
        
        // Helper function: Get top topics
        function getTopTopics(topics, perspective, count) {
          if (!topics || topics.length === 0) return [];
          
          return topics
            .filter(topic => topic.perspective_scores && topic.perspective_scores[perspective])
            .sort((a, b) => b.perspective_scores[perspective] - a.perspective_scores[perspective])
            .slice(0, count)
            .map(topic => ({
              topic_id: topic.topic_id,
              topic_name: topic.topic_name,
              score: topic.perspective_scores[perspective]
            }));
        }
      `
    }
  }
]
```

#### フロントエンド実装（React）

```jsx
// React component for overview dashboard
function OverviewDashboard({ data }) {
  const { summary_metrics, perspective_summary, recent_changes, equilibrium_status } = data;
  
  // Define trend icons and colors
  const trendIcons = {
    increasing: '↑',
    decreasing: '↓',
    stable: '→'
  };
  
  const trendColors = {
    increasing: '#4caf50',
    decreasing: '#f44336',
    stable: '#9e9e9e'
  };
  
  return (
    <div className="overview-dashboard">
      <h2>戦略AIレーダー概要</h2>
      
      <div className="dashboard-grid">
        {/* Summary metrics */}
        <div className="grid-item summary-metrics">
          <h3>サマリー</h3>
          <div className="metrics-container">
            <div className="metric-card">
              <div className="metric-value">{summary_metrics.total_topics}</div>
              <div className="metric-label">トピック総数</div>
            </div>
            
            <div className="metric-card">
              <div className="metric-value">{summary_metrics.equilibrium_topics}</div>
              <div className="metric-label">静止点トピック</div>
            </div>
            
            <div className="metric-card">
              <div className="metric-value">{summary_metrics.high_confidence_topics}</div>
              <div className="metric-label">高確信度トピック</div>
            </div>
            
            <div className="metric-card">
              <div className="metric-value">{summary_metrics.information_imbalance_topics}</div>
              <div className="metric-label">情報不均衡トピック</div>
            </div>
          </div>
        </div>
        
        {/* Perspective summary */}
        <div className="grid-item perspective-summary">
          <h3>視点別サマリー</h3>
          <div className="perspective-container">
            {Object.entries(perspective_summary).map(([perspective, data]) => {
              const perspectiveNames = {
                technology: 'テクノロジー',
                market: 'マーケット',
                business: 'ビジネス'
              };
              
              return (
                <div key={perspective} className="perspective-card">
                  <div className="perspective-header">
                    <h4>{perspectiveNames[perspective]}</h4>
                    <div 
                      className="perspective-trend"
                      style={{ color: trendColors[data.trend] }}
                    >
                      {trendIcons[data.trend]} {Math.round(data.average_score * 100)}%
                    </div>
                  </div>
                  
                  <div className="top-topics">
                    <h5>トップトピック</h5>
                    <ul>
                      {data.top_topics.map(topic => (
                        <li key={topic.topic_id}>
                          <span className="topic-name">{topic.topic_name}</span>
                          <span className="topic-score">{Math.round(topic.score * 100)}%</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        
        {/* Recent changes */}
        <div className="grid-item recent-changes">
          <h3>最近の変化</h3>
          <div className="changes-container">
            {recent_changes.length > 0 ? (
              <ul className="changes-list">
                {recent_changes.map((change, index) => (
                  <li key={index} className={`change-item ${change.change_type}`}>
                    <div className="change-header">
                      <span className="change-topic">{change.topic_name}</span>
                      <span className="change-time">
                        {new Date(change.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <div className="change-description">{change.description}</div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="no-changes">最近の変化はありません</p>
            )}
          </div>
        </div>
        
        {/* Equilibrium status */}
        <div className="grid-item equilibrium-status">
          <h3>静止点ステータス</h3>
          <div className="equilibrium-container">
            <div className="equilibrium-trend">
              <span className="trend-label">トレンド:</span>
              <span 
                className={`trend-value ${equilibrium_status.equilibrium_trend}`}
                style={{ color: trendColors[equilibrium_status.equilibrium_trend] }}
              >
                {equilibrium_status.equilibrium_trend === 'increasing' ? '増加中' :
                 equilibrium_status.equilibrium_trend === 'decreasing' ? '減少中' : '安定'}
              </span>
            </div>
            
            <div className="equilibrium-topics">
              <h5>現在の静止点トピック</h5>
              {equilibrium_status.current_equilibrium_topics.length > 0 ? (
                <ul>
                  {equilibrium_status.current_equilibrium_topics.map(topic => (
                    <li key={topic.topic_id}>{topic.topic_name}</li>
                  ))}
                </ul>
              ) : (
                <p className="no-topics">現在の静止点トピックはありません</p>
              )}
            </div>
            
            <div className="potential-topics">
              <h5>潜在的静止点トピック</h5>
              {equilibrium_status.potential_equilibrium_topics.length > 0 ? (
                <ul>
                  {equilibrium_status.potential_equilibrium_topics.map(topic => (
                    <li key={topic.topic_id}>{topic.topic_name}</li>
                  ))}
                </ul>
              ) : (
                <p className="no-topics">潜在的静止点トピックはありません</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### 2. 視点別分析ダッシュボード

視点別分析ダッシュボードは、テクノロジー、マーケット、ビジネスの各視点からの分析結果を詳細に表示します。

#### 実装要件

```javascript
// n8n workflow: Perspective Analysis Dashboard Data
// Function node for generating perspective analysis data
[
  {
    "id": "generatePerspectiveAnalysisData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Perspective-specific data
        const perspectiveId = $input.item.json.perspective_id || 'technology';
        const topicData = $input.item.json.topic_data || [];
        const timeSeriesData = $input.item.json.time_series_data || {};
        const relationshipData = $input.item.json.relationship_data || {};
        
        // Define perspective-specific metadata
        const perspectiveMetadata = {
          technology: {
            name: 'テクノロジー視点',
            description: '技術的実現可能性と革新性の分析',
            key_metrics: ['技術成熟度', '革新性', '実装難易度', '拡張性'],
            color: '#9c27b0'
          },
          market: {
            name: 'マーケット視点',
            description: '市場需要と成長性の分析',
            key_metrics: ['市場規模', '成長率', '顧客ニーズ', '競合状況'],
            color: '#2196f3'
          },
          business: {
            name: 'ビジネス視点',
            description: 'ビジネスモデルと収益性の分析',
            key_metrics: ['収益性', '投資効率', '持続可能性', '戦略的適合性'],
            color: '#4caf50'
          }
        };
        
        // Get metadata for the specified perspective
        const metadata = perspectiveMetadata[perspectiveId] || perspectiveMetadata.technology;
        
        // Filter topics for the specified perspective
        const perspectiveTopics = topicData.filter(topic => 
          topic.perspective_scores && topic.perspective_scores[perspectiveId] !== undefined
        );
        
        // Sort topics by score (descending)
        const sortedTopics = [...perspectiveTopics].sort(
          (a, b) => b.perspective_scores[perspectiveId] - a.perspective_scores[perspectiveId]
        );
        
        // Get time series data for the specified perspective
        const perspectiveTimeSeries = timeSeriesData[perspectiveId] || [];
        
        // Get relationship data for the specified perspective
        const perspectiveRelationships = relationshipData[perspectiveId] || [];
        
        // Prepare perspective analysis data
        const perspectiveAnalysisData = {
          perspective_id: perspectiveId,
          metadata,
          
          // Topic rankings
          topic_rankings: sortedTopics.map(topic => ({
            topic_id: topic.topic_id,
            topic_name: topic.topic_name,
            score: topic.perspective_scores[perspectiveId],
            confidence: topic.confidence || 0.5,
            is_equilibrium: topic.is_equilibrium || false,
            has_information_imbalance: topic.has_information_imbalance || false
          })),
          
          // Time series data
          time_series: perspectiveTimeSeries,
          
          // Relationship data
          relationships: perspectiveRelationships,
          
          // Key insights
          key_insights: generateKeyInsights(
            perspectiveId,
            sortedTopics,
            perspectiveTimeSeries,
            perspectiveRelationships
          )
        };
        
        return {
          json: perspectiveAnalysisData
        };
        
        // Helper function: Generate key insights
        function generateKeyInsights(perspectiveId, topics, timeSeries, relationships) {
          const insights = [];
          
          // Add top topics insight
          if (topics.length > 0) {
            const topTopics = topics.slice(0, 3);
            insights.push({
              type: 'top_topics',
              title: 'トップトピック',
              description: \`\${perspectiveMetadata[perspectiveId].name}において最も高いスコアを持つトピックは \${topTopics.map(t => t.topic_name).join('、')} です。\`
            });
          }
          
          // Add trend insight
          if (timeSeries.length > 0) {
            const latestTimeSeries = timeSeries[timeSeries.length - 1];
            const trend = latestTimeSeries.trend || 'stable';
            
            insights.push({
              type: 'trend',
              title: 'トレンド',
              description: \`\${perspectiveMetadata[perspectiveId].name}の全体的なトレンドは \${
                trend === 'increasing' ? '上昇' : 
                trend === 'decreasing' ? '下降' : '安定'
              } しています。\`
            });
          }
          
          // Add relationship insight
          if (relationships.length > 0) {
            insights.push({
              type: 'relationships',
              title: '関連性',
              description: \`\${perspectiveMetadata[perspectiveId].name}において \${relationships.length} の重要な関連性が検出されました。\`
            });
          }
          
          // Add equilibrium insight
          const equilibriumTopics = topics.filter(t => t.is_equilibrium);
          if (equilibriumTopics.length > 0) {
            insights.push({
              type: 'equilibrium',
              title: '静止点',
              description: \`\${perspectiveMetadata[perspectiveId].name}において \${equilibriumTopics.length} のトピックが静止点として検出されました。\`
            });
          }
          
          return insights;
        }
      `
    }
  }
]
```

#### フロントエンド実装（React）

```jsx
// React component for perspective analysis dashboard
function PerspectiveAnalysisDashboard({ data }) {
  const { perspective_id, metadata, topic_rankings, time_series, relationships, key_insights } = data;
  const [selectedTab, setSelectedTab] = useState('rankings');
  
  return (
    <div className="perspective-analysis-dashboard">
      <div className="perspective-header" style={{ borderColor: metadata.color }}>
        <h2>{metadata.name}</h2>
        <p className="perspective-description">{metadata.description}</p>
      </div>
      
      <div className="key-insights-section">
        <h3>主要インサイト</h3>
        <div className="insights-container">
          {key_insights.map((insight, index) => (
            <div key={index} className={`insight-card ${insight.type}`}>
              <h4>{insight.title}</h4>
              <p>{insight.description}</p>
            </div>
          ))}
        </div>
      </div>
      
      <div className="perspective-tabs">
        <button
          className={`tab-button ${selectedTab === 'rankings' ? 'active' : ''}`}
          onClick={() => setSelectedTab('rankings')}
        >
          トピックランキング
        </button>
        <button
          className={`tab-button ${selectedTab === 'trends' ? 'active' : ''}`}
          onClick={() => setSelectedTab('trends')}
        >
          時間的推移
        </button>
        <button
          className={`tab-button ${selectedTab === 'relationships' ? 'active' : ''}`}
          onClick={() => setSelectedTab('relationships')}
        >
          関連性分析
        </button>
      </div>
      
      <div className="tab-content">
        {selectedTab === 'rankings' && (
          <div className="rankings-content">
            <h3>トピックランキング</h3>
            <div className="rankings-table-container">
              <table className="rankings-table">
                <thead>
                  <tr>
                    <th>順位</th>
                    <th>トピック</th>
                    <th>スコア</th>
                    <th>確信度</th>
                    <th>静止点</th>
                    <th>情報不均衡</th>
                  </tr>
                </thead>
                <tbody>
                  {topic_rankings.map((topic, index) => (
                    <tr key={topic.topic_id}>
                      <td>{index + 1}</td>
                      <td>{topic.topic_name}</td>
                      <td>{Math.round(topic.score * 100)}%</td>
                      <td>{Math.round(topic.confidence * 100)}%</td>
                      <td>{topic.is_equilibrium ? '✓' : '✗'}</td>
                      <td>{topic.has_information_imbalance ? '⚠️' : '✓'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
        
        {selectedTab === 'trends' && (
          <div className="trends-content">
            <h3>時間的推移</h3>
            <div id="time-series-chart" className="chart-container">
              {/* Time series chart will be rendered here using D3 or Chart.js */}
              {/* This would call renderTimeSeriesChart with time_series data */}
            </div>
          </div>
        )}
        
        {selectedTab === 'relationships' && (
          <div className="relationships-content">
            <h3>関連性分析</h3>
            <div id="relationship-graph" className="chart-container">
              {/* Relationship graph will be rendered here using D3 */}
              {/* This would call renderRelationshipGraph with relationships data */}
            </div>
          </div>
        )}
      </div>
      
      <div className="key-metrics-section">
        <h3>主要メトリクス</h3>
        <div className="metrics-container">
          {metadata.key_metrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <h4>{metric}</h4>
              <div className="metric-chart" id={`metric-chart-${index}`}>
                {/* Metric chart will be rendered here */}
                {/* This would call renderMetricChart with metric-specific data */}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### 3. 統合分析ダッシュボード

統合分析ダッシュボードは、コンセンサスモデルの結果と静止点分析を表示します。

#### 実装要件

```javascript
// n8n workflow: Integrated Analysis Dashboard Data
// Function node for generating integrated analysis data
[
  {
    "id": "generateIntegratedAnalysisData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Consensus model and equilibrium data
        const topicData = $input.item.json.topic_data || [];
        const consensusData = $input.item.json.consensus_data || {};
        const equilibriumData = $input.item.json.equilibrium_data || {};
        
        // Prepare integrated analysis data
        const integratedAnalysisData = {
          // Consensus model results
          consensus_results: topicData.map(topic => ({
            topic_id: topic.topic_id,
            topic_name: topic.topic_name,
            consensus_score: topic.consensus_score || 0,
            perspective_scores: topic.perspective_scores || {},
            perspective_weights: topic.perspective_weights || {
              technology: 0.3,
              market: 0.4,
              business: 0.3
            },
            confidence: topic.confidence || 0.5,
            is_equilibrium: topic.is_equilibrium || false
          })),
          
          // Equilibrium analysis
          equilibrium_analysis: {
            current_equilibrium_topics: equilibriumData.current_equilibrium_topics || [],
            potential_equilibrium_topics: equilibriumData.potential_equilibrium_topics || [],
            equilibrium_distribution: equilibriumData.distribution || {},
            stability_metrics: equilibriumData.stability_metrics || {}
          },
          
          // Information imbalance analysis
          information_imbalance: {
            topics_with_imbalance: topicData.filter(t => t.has_information_imbalance).map(topic => ({
              topic_id: topic.topic_id,
              topic_name: topic.topic_name,
              imbalance_type: topic.imbalance_type || 'unknown',
              imbalance_severity: topic.imbalance_severity || 'medium',
              affected_perspectives: topic.affected_perspectives || []
            })),
            imbalance_distribution: consensusData.imbalance_distribution || {},
            correction_suggestions: consensusData.correction_suggestions || []
          },
          
          // Cross-perspective insights
          cross_perspective_insights: consensusData.cross_perspective_insights || []
        };
        
        return {
          json: integratedAnalysisData
        };
      `
    }
  }
]
```

#### フロントエンド実装（React）

```jsx
// React component for integrated analysis dashboard
function IntegratedAnalysisDashboard({ data }) {
  const { consensus_results, equilibrium_analysis, information_imbalance, cross_perspective_insights } = data;
  const [selectedTab, setSelectedTab] = useState('consensus');
  
  return (
    <div className="integrated-analysis-dashboard">
      <h2>統合分析ダッシュボード</h2>
      
      <div className="dashboard-tabs">
        <button
          className={`tab-button ${selectedTab === 'consensus' ? 'active' : ''}`}
          onClick={() => setSelectedTab('consensus')}
        >
          コンセンサスモデル
        </button>
        <button
          className={`tab-button ${selectedTab === 'equilibrium' ? 'active' : ''}`}
          onClick={() => setSelectedTab('equilibrium')}
        >
          静止点分析
        </button>
        <button
          className={`tab-button ${selectedTab === 'imbalance' ? 'active' : ''}`}
          onClick={() => setSelectedTab('imbalance')}
        >
          情報不均衡
        </button>
        <button
          className={`tab-button ${selectedTab === 'insights' ? 'active' : ''}`}
          onClick={() => setSelectedTab('insights')}
        >
          クロス視点インサイト
        </button>
      </div>
      
      <div className="tab-content">
        {selectedTab === 'consensus' && (
          <div className="consensus-content">
            <h3>コンセンサスモデル結果</h3>
            
            <div className="consensus-table-container">
              <table className="consensus-table">
                <thead>
                  <tr>
                    <th>トピック</th>
                    <th>コンセンサススコア</th>
                    <th>テクノロジー</th>
                    <th>マーケット</th>
                    <th>ビジネス</th>
                    <th>確信度</th>
                    <th>静止点</th>
                  </tr>
                </thead>
                <tbody>
                  {consensus_results.map(topic => (
                    <tr key={topic.topic_id}>
                      <td>{topic.topic_name}</td>
                      <td>{Math.round(topic.consensus_score * 100)}%</td>
                      <td>{Math.round(topic.perspective_scores.technology * 100)}%</td>
                      <td>{Math.round(topic.perspective_scores.market * 100)}%</td>
                      <td>{Math.round(topic.perspective_scores.business * 100)}%</td>
                      <td>{Math.round(topic.confidence * 100)}%</td>
                      <td>{topic.is_equilibrium ? '✓' : '✗'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="consensus-visualization">
              <h4>視点別重み付け</h4>
              <div id="weights-chart" className="chart-container">
                {/* Weights chart will be rendered here */}
                {/* This would call renderWeightsChart with perspective weights data */}
              </div>
            </div>
          </div>
        )}
        
        {selectedTab === 'equilibrium' && (
          <div className="equilibrium-content">
            <h3>静止点分析</h3>
            
            <div className="equilibrium-grid">
              <div className="grid-item current-equilibrium">
                <h4>現在の静止点</h4>
                {equilibrium_analysis.current_equilibrium_topics.length > 0 ? (
                  <ul className="equilibrium-list">
                    {equilibrium_analysis.current_equilibrium_topics.map(topic => (
                      <li key={topic.topic_id} className="equilibrium-item">
                        <span className="topic-name">{topic.topic_name}</span>
                        <span className="topic-score">{Math.round(topic.score * 100)}%</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="no-data">現在の静止点はありません</p>
                )}
              </div>
              
              <div className="grid-item potential-equilibrium">
                <h4>潜在的静止点</h4>
                {equilibrium_analysis.potential_equilibrium_topics.length > 0 ? (
                  <ul className="equilibrium-list">
                    {equilibrium_analysis.potential_equilibrium_topics.map(topic => (
                      <li key={topic.topic_id} className="equilibrium-item">
                        <span className="topic-name">{topic.topic_name}</span>
                        <span className="topic-score">{Math.round(topic.score * 100)}%</span>
                        <span className="distance-to-equilibrium">
                          {Math.round(topic.distance_to_equilibrium * 100)}%
                        </span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="no-data">潜在的静止点はありません</p>
                )}
              </div>
              
              <div className="grid-item equilibrium-distribution">
                <h4>静止点分布</h4>
                <div id="distribution-chart" className="chart-container">
                  {/* Distribution chart will be rendered here */}
                  {/* This would call renderDistributionChart with equilibrium distribution data */}
                </div>
              </div>
              
              <div className="grid-item stability-metrics">
                <h4>安定性メトリクス</h4>
                <div className="metrics-list">
                  {Object.entries(equilibrium_analysis.stability_metrics).map(([key, value]) => (
                    <div key={key} className="metric-item">
                      <span className="metric-name">{key}</span>
                      <span className="metric-value">{typeof value === 'number' ? Math.round(value * 100) + '%' : value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
        
        {selectedTab === 'imbalance' && (
          <div className="imbalance-content">
            <h3>情報不均衡分析</h3>
            
            <div className="imbalance-grid">
              <div className="grid-item imbalance-topics">
                <h4>情報不均衡のあるトピック</h4>
                {information_imbalance.topics_with_imbalance.length > 0 ? (
                  <ul className="imbalance-list">
                    {information_imbalance.topics_with_imbalance.map(topic => (
                      <li key={topic.topic_id} className={`imbalance-item ${topic.imbalance_severity}`}>
                        <div className="topic-header">
                          <span className="topic-name">{topic.topic_name}</span>
                          <span className="imbalance-type">{topic.imbalance_type}</span>
                        </div>
                        <div className="affected-perspectives">
                          影響を受ける視点: {topic.affected_perspectives.join(', ')}
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="no-data">情報不均衡のあるトピックはありません</p>
                )}
              </div>
              
              <div className="grid-item imbalance-distribution">
                <h4>不均衡分布</h4>
                <div id="imbalance-chart" className="chart-container">
                  {/* Imbalance chart will be rendered here */}
                  {/* This would call renderImbalanceChart with imbalance distribution data */}
                </div>
              </div>
              
              <div className="grid-item correction-suggestions">
                <h4>修正提案</h4>
                {information_imbalance.correction_suggestions.length > 0 ? (
                  <ul className="suggestions-list">
                    {information_imbalance.correction_suggestions.map((suggestion, index) => (
                      <li key={index} className="suggestion-item">
                        <div className="suggestion-header">
                          <span className="suggestion-title">{suggestion.title}</span>
                          <span className="suggestion-priority">{suggestion.priority}</span>
                        </div>
                        <div className="suggestion-description">
                          {suggestion.description}
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="no-data">修正提案はありません</p>
                )}
              </div>
            </div>
          </div>
        )}
        
        {selectedTab === 'insights' && (
          <div className="insights-content">
            <h3>クロス視点インサイト</h3>
            
            {cross_perspective_insights.length > 0 ? (
              <div className="insights-grid">
                {cross_perspective_insights.map((insight, index) => (
                  <div key={index} className="insight-card">
                    <h4>{insight.title}</h4>
                    <p className="insight-description">{insight.description}</p>
                    <div className="insight-perspectives">
                      関連する視点: {insight.related_perspectives.join(', ')}
                    </div>
                    <div className="insight-topics">
                      関連するトピック: {insight.related_topics.join(', ')}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">クロス視点インサイトはありません</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
```

### 4. シナリオ分析ダッシュボード

シナリオ分析ダッシュボードは、代替シナリオの比較と予測シミュレーションを提供します。

#### 実装要件

```javascript
// n8n workflow: Scenario Analysis Dashboard Data
// Function node for generating scenario analysis data
[
  {
    "id": "generateScenarioAnalysisData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Scenario data
        const topicId = $input.item.json.topic_id || 'topic-001';
        const scenarioData = $input.item.json.scenario_data || {};
        const predictionData = $input.item.json.prediction_data || {};
        
        // Prepare scenario analysis data
        const scenarioAnalysisData = {
          topic_id: topicId,
          topic_name: scenarioData.topic_name || 'Unknown Topic',
          
          // Baseline scenario
          baseline_scenario: scenarioData.baseline_scenario || {
            scenario_id: 'baseline',
            name: 'ベースラインシナリオ',
            description: '現在の情報に基づく最も可能性の高いシナリオ',
            probability: 0.6,
            adjusted_score: 0.65,
            is_equilibrium: false,
            perspective_scores: {
              technology: 0.7,
              market: 0.6,
              business: 0.65
            },
            key_assumptions: [
              '現在の技術トレンドが継続する',
              '市場の成長率は現在の予測通りに推移する',
              'ビジネスモデルに大きな変化はない'
            ],
            is_current: true
          },
          
          // Alternative scenarios
          alternative_scenarios: scenarioData.alternative_scenarios || [],
          
          // Scenario comparison metrics
          comparison_metrics: scenarioData.comparison_metrics || [],
          
          // Prediction data
          predictions: {
            time_horizons: predictionData.time_horizons || ['3ヶ月後', '6ヶ月後', '1年後'],
            scenario_predictions: predictionData.scenario_predictions || []
          },
          
          // Recommended actions
          recommended_actions: scenarioData.recommended_actions || []
        };
        
        return {
          json: scenarioAnalysisData
        };
      `
    }
  }
]
```

#### フロントエンド実装（React）

```jsx
// React component for scenario analysis dashboard
function ScenarioAnalysisDashboard({ data }) {
  const { 
    topic_name, 
    baseline_scenario, 
    alternative_scenarios, 
    comparison_metrics, 
    predictions, 
    recommended_actions 
  } = data;
  
  const [selectedTab, setSelectedTab] = useState('comparison');
  const [selectedScenarios, setSelectedScenarios] = useState(['baseline']);
  
  // Handle scenario selection
  const handleScenarioSelection = (scenarioId) => {
    if (selectedScenarios.includes(scenarioId)) {
      // Remove if already selected (but keep at least one)
      if (selectedScenarios.length > 1) {
        setSelectedScenarios(selectedScenarios.filter(id => id !== scenarioId));
      }
    } else {
      // Add if not selected (limit to 5 for readability)
      if (selectedScenarios.length < 5) {
        setSelectedScenarios([...selectedScenarios, scenarioId]);
      }
    }
  };
  
  // Get all scenarios (baseline + alternatives)
  const allScenarios = [baseline_scenario, ...alternative_scenarios];
  
  // Filter selected scenarios
  const filteredScenarios = allScenarios.filter(
    scenario => selectedScenarios.includes(scenario.scenario_id)
  );
  
  return (
    <div className="scenario-analysis-dashboard">
      <h2>{topic_name}のシナリオ分析</h2>
      
      <div className="scenario-selector">
        <h3>シナリオ選択</h3>
        <div className="scenario-checkboxes">
          {allScenarios.map(scenario => (
            <label key={scenario.scenario_id} className="scenario-checkbox">
              <input
                type="checkbox"
                checked={selectedScenarios.includes(scenario.scenario_id)}
                onChange={() => handleScenarioSelection(scenario.scenario_id)}
              />
              <span className={`checkbox-label ${scenario.is_current ? 'current-scenario' : ''}`}>
                {scenario.name}
                {scenario.is_current && <span className="current-badge">現在</span>}
              </span>
            </label>
          ))}
        </div>
      </div>
      
      <div className="dashboard-tabs">
        <button
          className={`tab-button ${selectedTab === 'comparison' ? 'active' : ''}`}
          onClick={() => setSelectedTab('comparison')}
        >
          シナリオ比較
        </button>
        <button
          className={`tab-button ${selectedTab === 'prediction' ? 'active' : ''}`}
          onClick={() => setSelectedTab('prediction')}
        >
          予測シミュレーション
        </button>
        <button
          className={`tab-button ${selectedTab === 'actions' ? 'active' : ''}`}
          onClick={() => setSelectedTab('actions')}
        >
          推奨アクション
        </button>
      </div>
      
      <div className="tab-content">
        {selectedTab === 'comparison' && (
          <div className="comparison-content">
            <h3>シナリオ比較</h3>
            
            <div className="comparison-grid">
              <div className="grid-item comparison-table">
                <h4>比較テーブル</h4>
                <table className="scenario-table">
                  <thead>
                    <tr>
                      <th>シナリオ</th>
                      <th>発生確率</th>
                      <th>調整スコア</th>
                      <th>静止点</th>
                      <th>テクノロジー</th>
                      <th>マーケット</th>
                      <th>ビジネス</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredScenarios.map(scenario => (
                      <tr 
                        key={scenario.scenario_id}
                        className={scenario.is_current ? 'current-scenario' : ''}
                      >
                        <td>{scenario.name}</td>
                        <td>{Math.round(scenario.probability * 100)}%</td>
                        <td>{Math.round(scenario.adjusted_score * 100)}%</td>
                        <td>{scenario.is_equilibrium ? '✓' : '✗'}</td>
                        <td>{Math.round(scenario.perspective_scores.technology * 100)}%</td>
                        <td>{Math.round(scenario.perspective_scores.market * 100)}%</td>
                        <td>{Math.round(scenario.perspective_scores.business * 100)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="grid-item radar-chart">
                <h4>レーダーチャート比較</h4>
                <div id="scenario-radar-chart" className="chart-container">
                  {/* Radar chart will be rendered here */}
                  {/* This would call renderScenarioRadarChart with filtered scenarios data */}
                </div>
              </div>
              
              <div className="grid-item parallel-plot">
                <h4>パラレルコーディネートプロット</h4>
                <div id="parallel-coordinates-plot" className="chart-container">
                  {/* Parallel coordinates plot will be rendered here */}
                  {/* This would call renderParallelCoordinatesPlot with filtered scenarios data */}
                </div>
              </div>
              
              <div className="grid-item key-assumptions">
                <h4>主要な前提条件</h4>
                <div className="assumptions-container">
                  {filteredScenarios.map(scenario => (
                    <div key={scenario.scenario_id} className="scenario-assumptions">
                      <h5>{scenario.name}</h5>
                      <ul>
                        {scenario.key_assumptions.map((assumption, index) => (
                          <li key={index}>{assumption}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
        
        {selectedTab === 'prediction' && (
          <div className="prediction-content">
            <h3>予測シミュレーション</h3>
            
            <div className="prediction-grid">
              <div className="grid-item prediction-chart">
                <h4>時間軸予測</h4>
                <div id="prediction-chart" className="chart-container">
                  {/* Prediction chart will be rendered here */}
                  {/* This would call renderPredictionChart with predictions data */}
                </div>
              </div>
              
              <div className="grid-item prediction-table">
                <h4>予測値テーブル</h4>
                <table className="prediction-table">
                  <thead>
                    <tr>
                      <th>シナリオ</th>
                      {predictions.time_horizons.map((horizon, index) => (
                        <th key={index}>{horizon}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {filteredScenarios.map(scenario => {
                      const scenarioPrediction = predictions.scenario_predictions.find(
                        p => p.scenario_id === scenario.scenario_id
                      ) || { values: Array(predictions.time_horizons.length).fill(0) };
                      
                      return (
                        <tr 
                          key={scenario.scenario_id}
                          className={scenario.is_current ? 'current-scenario' : ''}
                        >
                          <td>{scenario.name}</td>
                          {scenarioPrediction.values.map((value, index) => (
                            <td key={index}>{Math.round(value * 100)}%</td>
                          ))}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              
              <div className="grid-item confidence-intervals">
                <h4>確信度区間</h4>
                <div id="confidence-intervals-chart" className="chart-container">
                  {/* Confidence intervals chart will be rendered here */}
                  {/* This would call renderConfidenceIntervalsChart with predictions data */}
                </div>
              </div>
              
              <div className="grid-item prediction-insights">
                <h4>予測インサイト</h4>
                <div className="insights-container">
                  {predictions.insights ? (
                    <ul className="insights-list">
                      {predictions.insights.map((insight, index) => (
                        <li key={index} className="insight-item">
                          {insight}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="no-data">予測インサイトはありません</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
        
        {selectedTab === 'actions' && (
          <div className="actions-content">
            <h3>推奨アクション</h3>
            
            {recommended_actions.length > 0 ? (
              <div className="actions-grid">
                {recommended_actions.map((action, index) => (
                  <div key={index} className={`action-card priority-${action.priority_level}`}>
                    <div className="action-header">
                      <h4>{action.title}</h4>
                      <span className="priority-badge">
                        優先度: {action.priority_level}
                      </span>
                    </div>
                    <p className="action-description">{action.description}</p>
                    <div className="action-details">
                      <div className="related-scenarios">
                        <h5>関連シナリオ:</h5>
                        <ul>
                          {action.related_scenarios.map((scenario, idx) => (
                            <li key={idx}>{scenario}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="expected-impact">
                        <h5>期待される影響:</h5>
                        <p>{action.expected_impact}</p>
                      </div>
                      <div className="implementation-timeline">
                        <h5>実装タイムライン:</h5>
                        <p>{action.implementation_timeline}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">推奨アクションはありません</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
```

## インタラクティブ機能の実装

インタラクティブダッシュボードには、以下のインタラクティブ機能を実装します。

### 1. フィルタリングとソート

```javascript
// React component for filtering and sorting
function FilterSortControls({ data, onFilterChange, onSortChange }) {
  const [filterValues, setFilterValues] = useState({});
  const [sortField, setSortField] = useState('name');
  const [sortDirection, setSortDirection] = useState('asc');
  
  // Handle filter change
  const handleFilterChange = (field, value) => {
    const newFilterValues = {
      ...filterValues,
      [field]: value
    };
    
    setFilterValues(newFilterValues);
    onFilterChange(newFilterValues);
  };
  
  // Handle sort change
  const handleSortChange = (field) => {
    let newDirection = 'asc';
    
    if (field === sortField) {
      // Toggle direction if same field
      newDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    }
    
    setSortField(field);
    setSortDirection(newDirection);
    onSortChange(field, newDirection);
  };
  
  return (
    <div className="filter-sort-controls">
      <div className="filter-controls">
        <h4>フィルター</h4>
        
        <div className="filter-group">
          <label>確信度:</label>
          <select
            value={filterValues.confidence || ''}
            onChange={(e) => handleFilterChange('confidence', e.target.value)}
          >
            <option value="">すべて</option>
            <option value="high">高 (70%以上)</option>
            <option value="medium">中 (40%-70%)</option>
            <option value="low">低 (40%未満)</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>静止点:</label>
          <select
            value={filterValues.equilibrium || ''}
            onChange={(e) => handleFilterChange('equilibrium', e.target.value)}
          >
            <option value="">すべて</option>
            <option value="true">静止点のみ</option>
            <option value="false">非静止点のみ</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>情報不均衡:</label>
          <select
            value={filterValues.imbalance || ''}
            onChange={(e) => handleFilterChange('imbalance', e.target.value)}
          >
            <option value="">すべて</option>
            <option value="true">不均衡あり</option>
            <option value="false">不均衡なし</option>
          </select>
        </div>
      </div>
      
      <div className="sort-controls">
        <h4>ソート</h4>
        
        <div className="sort-buttons">
          <button
            className={`sort-button ${sortField === 'name' ? 'active' : ''}`}
            onClick={() => handleSortChange('name')}
          >
            名前
            {sortField === 'name' && (
              <span className="sort-direction">
                {sortDirection === 'asc' ? '↑' : '↓'}
              </span>
            )}
          </button>
          
          <button
            className={`sort-button ${sortField === 'score' ? 'active' : ''}`}
            onClick={() => handleSortChange('score')}
          >
            スコア
            {sortField === 'score' && (
              <span className="sort-direction">
                {sortDirection === 'asc' ? '↑' : '↓'}
              </span>
            )}
          </button>
          
          <button
            className={`sort-button ${sortField === 'confidence' ? 'active' : ''}`}
            onClick={() => handleSortChange('confidence')}
          >
            確信度
            {sortField === 'confidence' && (
              <span className="sort-direction">
                {sortDirection === 'asc' ? '↑' : '↓'}
              </span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
```

### 2. ドリルダウンと詳細表示

```javascript
// React component for drill-down and detail view
function DrillDownView({ data, onBack }) {
  const { topic_id, topic_name, details } = data;
  
  return (
    <div className="drill-down-view">
      <div className="drill-down-header">
        <button className="back-button" onClick={onBack}>
          ← 戻る
        </button>
        <h2>{topic_name}の詳細</h2>
      </div>
      
      <div className="detail-tabs">
        <Tabs>
          <TabList>
            <Tab>概要</Tab>
            <Tab>視点別分析</Tab>
            <Tab>時間的推移</Tab>
            <Tab>関連トピック</Tab>
          </TabList>
          
          <TabPanel>
            <div className="overview-panel">
              <div className="detail-card">
                <h3>トピック概要</h3>
                <div className="topic-metrics">
                  <div className="metric">
                    <span className="metric-label">調整スコア:</span>
                    <span className="metric-value">{Math.round(details.adjusted_score * 100)}%</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">確信度:</span>
                    <span className="metric-value">{Math.round(details.confidence * 100)}%</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">静止点:</span>
                    <span className="metric-value">{details.is_equilibrium ? '✓' : '✗'}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">情報不均衡:</span>
                    <span className="metric-value">{details.has_information_imbalance ? '⚠️' : '✓'}</span>
                  </div>
                </div>
                
                <div className="topic-description">
                  <h4>説明</h4>
                  <p>{details.description}</p>
                </div>
                
                <div className="key-insights">
                  <h4>主要インサイト</h4>
                  <ul>
                    {details.key_insights.map((insight, index) => (
                      <li key={index}>{insight}</li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div className="detail-card">
                <h3>視点別スコア</h3>
                <div id="perspective-chart" className="chart-container">
                  {/* Perspective chart will be rendered here */}
                  {/* This would call renderPerspectiveChart with perspective scores data */}
                </div>
              </div>
            </div>
          </TabPanel>
          
          <TabPanel>
            <div className="perspectives-panel">
              <div className="perspective-tabs">
                <Tabs>
                  <TabList>
                    <Tab>テクノロジー</Tab>
                    <Tab>マーケット</Tab>
                    <Tab>ビジネス</Tab>
                  </TabList>
                  
                  {['technology', 'market', 'business'].map(perspective => (
                    <TabPanel key={perspective}>
                      <div className="perspective-detail">
                        <h3>{perspective === 'technology' ? 'テクノロジー' : 
                             perspective === 'market' ? 'マーケット' : 'ビジネス'}視点</h3>
                        
                        <div className="perspective-metrics">
                          <div className="metric">
                            <span className="metric-label">スコア:</span>
                            <span className="metric-value">
                              {Math.round(details.perspective_scores[perspective] * 100)}%
                            </span>
                          </div>
                          <div className="metric">
                            <span className="metric-label">確信度:</span>
                            <span className="metric-value">
                              {Math.round(details.perspective_confidence[perspective] * 100)}%
                            </span>
                          </div>
                          <div className="metric">
                            <span className="metric-label">トレンド:</span>
                            <span className="metric-value">
                              {details.perspective_trends[perspective]}
                            </span>
                          </div>
                        </div>
                        
                        <div className="perspective-factors">
                          <h4>主要因子</h4>
                          <ul>
                            {details.perspective_factors[perspective].map((factor, index) => (
                              <li key={index}>
                                <span className="factor-name">{factor.name}</span>
                                <span className="factor-score">{Math.round(factor.score * 100)}%</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <div className="perspective-insights">
                          <h4>インサイト</h4>
                          <p>{details.perspective_insights[perspective]}</p>
                        </div>
                      </div>
                    </TabPanel>
                  ))}
                </Tabs>
              </div>
            </div>
          </TabPanel>
          
          <TabPanel>
            <div className="timeline-panel">
              <h3>時間的推移</h3>
              <div id="timeline-chart" className="chart-container">
                {/* Timeline chart will be rendered here */}
                {/* This would call renderTimelineChart with timeline data */}
              </div>
              
              <div className="key-events">
                <h4>主要イベント</h4>
                <ul className="events-timeline">
                  {details.key_events.map((event, index) => (
                    <li key={index} className="event-item">
                      <div className="event-date">{event.date}</div>
                      <div className="event-content">
                        <div className="event-title">{event.title}</div>
                        <div className="event-description">{event.description}</div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </TabPanel>
          
          <TabPanel>
            <div className="related-topics-panel">
              <h3>関連トピック</h3>
              <div id="relationship-graph" className="chart-container">
                {/* Relationship graph will be rendered here */}
                {/* This would call renderRelationshipGraph with related topics data */}
              </div>
              
              <div className="related-topics-list">
                <h4>関連トピック一覧</h4>
                <ul>
                  {details.related_topics.map((topic, index) => (
                    <li key={index} className="related-topic-item">
                      <div className="topic-name">{topic.name}</div>
                      <div className="relationship-type">{topic.relationship_type}</div>
                      <div className="relationship-strength">
                        関連度: {Math.round(topic.relationship_strength * 100)}%
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </TabPanel>
        </Tabs>
      </div>
    </div>
  );
}
```

### 3. カスタマイズと設定

```javascript
// React component for customization and settings
function DashboardSettings({ settings, onSettingsChange }) {
  const [currentSettings, setCurrentSettings] = useState(settings);
  
  // Handle settings change
  const handleSettingChange = (category, setting, value) => {
    const newSettings = {
      ...currentSettings,
      [category]: {
        ...currentSettings[category],
        [setting]: value
      }
    };
    
    setCurrentSettings(newSettings);
    onSettingsChange(newSettings);
  };
  
  return (
    <div className="dashboard-settings">
      <h2>ダッシュボード設定</h2>
      
      <div className="settings-grid">
        <div className="settings-category">
          <h3>表示設定</h3>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.display.showConfidenceIndicators}
                onChange={(e) => handleSettingChange('display', 'showConfidenceIndicators', e.target.checked)}
              />
              確信度インジケーターを表示
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.display.showInformationImbalance}
                onChange={(e) => handleSettingChange('display', 'showInformationImbalance', e.target.checked)}
              />
              情報不均衡を表示
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.display.highlightEquilibrium}
                onChange={(e) => handleSettingChange('display', 'highlightEquilibrium', e.target.checked)}
              />
              静止点を強調表示
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              デフォルトビュー:
              <select
                value={currentSettings.display.defaultView}
                onChange={(e) => handleSettingChange('display', 'defaultView', e.target.value)}
              >
                <option value="overview">概要</option>
                <option value="technology">テクノロジー視点</option>
                <option value="market">マーケット視点</option>
                <option value="business">ビジネス視点</option>
                <option value="integrated">統合分析</option>
                <option value="scenarios">シナリオ分析</option>
              </select>
            </label>
          </div>
        </div>
        
        <div className="settings-category">
          <h3>データ設定</h3>
          
          <div className="setting-item">
            <label>
              更新頻度:
              <select
                value={currentSettings.data.refreshInterval}
                onChange={(e) => handleSettingChange('data', 'refreshInterval', e.target.value)}
              >
                <option value="none">手動更新</option>
                <option value="1min">1分</option>
                <option value="5min">5分</option>
                <option value="15min">15分</option>
                <option value="30min">30分</option>
                <option value="1hour">1時間</option>
              </select>
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              データ範囲:
              <select
                value={currentSettings.data.timeRange}
                onChange={(e) => handleSettingChange('data', 'timeRange', e.target.value)}
              >
                <option value="1week">1週間</option>
                <option value="1month">1ヶ月</option>
                <option value="3months">3ヶ月</option>
                <option value="6months">6ヶ月</option>
                <option value="1year">1年</option>
                <option value="all">すべて</option>
              </select>
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.data.includeHistoricalData}
                onChange={(e) => handleSettingChange('data', 'includeHistoricalData', e.target.checked)}
              />
              履歴データを含める
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.data.includePredictions}
                onChange={(e) => handleSettingChange('data', 'includePredictions', e.target.checked)}
              />
              予測データを含める
            </label>
          </div>
        </div>
        
        <div className="settings-category">
          <h3>通知設定</h3>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.notifications.enableNotifications}
                onChange={(e) => handleSettingChange('notifications', 'enableNotifications', e.target.checked)}
              />
              通知を有効化
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.notifications.notifyOnEquilibrium}
                onChange={(e) => handleSettingChange('notifications', 'notifyOnEquilibrium', e.target.checked)}
              />
              静止点検出時に通知
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.notifications.notifyOnSignificantChange}
                onChange={(e) => handleSettingChange('notifications', 'notifyOnSignificantChange', e.target.checked)}
              />
              重要な変化時に通知
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.notifications.notifyOnInformationImbalance}
                onChange={(e) => handleSettingChange('notifications', 'notifyOnInformationImbalance', e.target.checked)}
              />
              情報不均衡検出時に通知
            </label>
          </div>
        </div>
        
        <div className="settings-category">
          <h3>視覚化設定</h3>
          
          <div className="setting-item">
            <label>
              カラーテーマ:
              <select
                value={currentSettings.visualization.colorTheme}
                onChange={(e) => handleSettingChange('visualization', 'colorTheme', e.target.value)}
              >
                <option value="default">デフォルト</option>
                <option value="light">ライト</option>
                <option value="dark">ダーク</option>
                <option value="colorblind">カラーブラインド対応</option>
              </select>
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              チャートタイプ:
              <select
                value={currentSettings.visualization.chartType}
                onChange={(e) => handleSettingChange('visualization', 'chartType', e.target.value)}
              >
                <option value="radar">レーダーチャート</option>
                <option value="bar">棒グラフ</option>
                <option value="line">折れ線グラフ</option>
              </select>
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.visualization.showAnimations}
                onChange={(e) => handleSettingChange('visualization', 'showAnimations', e.target.checked)}
              />
              アニメーションを表示
            </label>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={currentSettings.visualization.showTooltips}
                onChange={(e) => handleSettingChange('visualization', 'showTooltips', e.target.checked)}
              />
              ツールチップを表示
            </label>
          </div>
        </div>
      </div>
      
      <div className="settings-actions">
        <button className="reset-button" onClick={() => setCurrentSettings(settings)}>
          リセット
        </button>
        <button className="save-button" onClick={() => onSettingsChange(currentSettings)}>
          保存
        </button>
      </div>
    </div>
  );
}
```

## n8nによるダッシュボード統合

n8nを活用して、インタラクティブダッシュボードの各コンポーネントを統合します。

### 1. マスターワークフロー

```javascript
// n8n workflow: Dashboard Master Workflow
// This workflow orchestrates the entire dashboard
[
  {
    "id": "start",
    "type": "n8n-nodes-base.start",
    "position": [100, 300]
  },
  {
    "id": "fetchTopicData",
    "type": "n8n-nodes-base.function",
    "position": [300, 300],
    "parameters": {
      "functionCode": `
        // Fetch topic data from database or API
        // In a real implementation, this would be a database or API node
        
        // For demonstration, we'll generate sample data
        const topicData = generateSampleTopicData();
        
        return {
          json: {
            topic_data: topicData
          }
        };
        
        // Helper function: Generate sample topic data
        function generateSampleTopicData() {
          // Generate sample data
          // ...
        }
      `
    }
  },
  {
    "id": "fetchPerspectiveData",
    "type": "n8n-nodes-base.function",
    "position": [300, 400],
    "parameters": {
      "functionCode": `
        // Fetch perspective data from database or API
        // In a real implementation, this would be a database or API node
        
        // For demonstration, we'll generate sample data
        const perspectiveData = generateSamplePerspectiveData();
        
        return {
          json: {
            perspective_data: perspectiveData
          }
        };
        
        // Helper function: Generate sample perspective data
        function generateSamplePerspectiveData() {
          // Generate sample data
          // ...
        }
      `
    }
  },
  {
    "id": "fetchConsensusData",
    "type": "n8n-nodes-base.function",
    "position": [300, 500],
    "parameters": {
      "functionCode": `
        // Fetch consensus data from database or API
        // In a real implementation, this would be a database or API node
        
        // For demonstration, we'll generate sample data
        const consensusData = generateSampleConsensusData();
        
        return {
          json: {
            consensus_data: consensusData
          }
        };
        
        // Helper function: Generate sample consensus data
        function generateSampleConsensusData() {
          // Generate sample data
          // ...
        }
      `
    }
  },
  {
    "id": "fetchScenarioData",
    "type": "n8n-nodes-base.function",
    "position": [300, 600],
    "parameters": {
      "functionCode": `
        // Fetch scenario data from database or API
        // In a real implementation, this would be a database or API node
        
        // For demonstration, we'll generate sample data
        const scenarioData = generateSampleScenarioData();
        
        return {
          json: {
            scenario_data: scenarioData
          }
        };
        
        // Helper function: Generate sample scenario data
        function generateSampleScenarioData() {
          // Generate sample data
          // ...
        }
      `
    }
  },
  {
    "id": "mergeData",
    "type": "n8n-nodes-base.merge",
    "position": [500, 300],
    "parameters": {
      "mode": "mergeByPosition"
    }
  },
  {
    "id": "generateOverviewData",
    "type": "n8n-nodes-base.function",
    "position": [700, 200],
    "parameters": {
      "functionCode": `
        // Generate overview dashboard data
        // ...
      `
    }
  },
  {
    "id": "generatePerspectiveData",
    "type": "n8n-nodes-base.function",
    "position": [700, 300],
    "parameters": {
      "functionCode": `
        // Generate perspective analysis dashboard data
        // ...
      `
    }
  },
  {
    "id": "generateIntegratedData",
    "type": "n8n-nodes-base.function",
    "position": [700, 400],
    "parameters": {
      "functionCode": `
        // Generate integrated analysis dashboard data
        // ...
      `
    }
  },
  {
    "id": "generateScenarioData",
    "type": "n8n-nodes-base.function",
    "position": [700, 500],
    "parameters": {
      "functionCode": `
        // Generate scenario analysis dashboard data
        // ...
      `
    }
  },
  {
    "id": "prepareApiResponse",
    "type": "n8n-nodes-base.function",
    "position": [900, 300],
    "parameters": {
      "functionCode": `
        // Prepare API response with all dashboard data
        const items = $input.all();
        
        const dashboardData = {
          overview: items[0].json,
          perspective: items[1].json,
          integrated: items[2].json,
          scenario: items[3].json,
          timestamp: new Date().toISOString(),
          version: '1.0.0'
        };
        
        return {
          json: dashboardData
        };
      `
    }
  },
  {
    "id": "respondWithData",
    "type": "n8n-nodes-base.respondWithData",
    "position": [1100, 300],
    "parameters": {}
  }
]
```

### 2. データ更新ワークフロー

```javascript
// n8n workflow: Dashboard Data Update Workflow
// This workflow handles data updates for the dashboard
[
  {
    "id": "start",
    "type": "n8n-nodes-base.start",
    "position": [100, 300]
  },
  {
    "id": "scheduleTrigger",
    "type": "n8n-nodes-base.scheduleTrigger",
    "position": [300, 300],
    "parameters": {
      "rule": {
        "interval": [
          {
            "field": "minutes",
            "minutesInterval": 15
          }
        ]
      }
    }
  },
  {
    "id": "httpRequest",
    "type": "n8n-nodes-base.httpRequest",
    "position": [500, 300],
    "parameters": {
      "url": "https://api.example.com/data",
      "method": "GET",
      "authentication": "basicAuth",
      "username": "={{ $env.API_USERNAME }}",
      "password": "={{ $env.API_PASSWORD }}"
    }
  },
  {
    "id": "processData",
    "type": "n8n-nodes-base.function",
    "position": [700, 300],
    "parameters": {
      "functionCode": `
        // Process the fetched data
        const data = $input.item.json;
        
        // Transform data for dashboard
        const transformedData = {
          // Transform data
          // ...
        };
        
        return {
          json: transformedData
        };
      `
    }
  },
  {
    "id": "detectChanges",
    "type": "n8n-nodes-base.function",
    "position": [900, 300],
    "parameters": {
      "functionCode": `
        // Detect changes in the data
        const newData = $input.item.json;
        
        // Get previous data from database or storage
        // In a real implementation, this would be a database or storage node
        const previousData = getPreviousData();
        
        // Compare data and detect changes
        const changes = detectDataChanges(previousData, newData);
        
        return {
          json: {
            new_data: newData,
            previous_data: previousData,
            changes: changes
          }
        };
        
        // Helper function: Get previous data
        function getPreviousData() {
          // Get previous data
          // ...
        }
        
        // Helper function: Detect data changes
        function detectDataChanges(previousData, newData) {
          // Detect changes
          // ...
        }
      `
    }
  },
  {
    "id": "ifChangesDetected",
    "type": "n8n-nodes-base.if",
    "position": [1100, 300],
    "parameters": {
      "conditions": [
        {
          "name": "changes",
          "value1": "={{ $json.changes.length }}",
          "operation": "larger",
          "value2": 0
        }
      ]
    }
  },
  {
    "id": "updateDatabase",
    "type": "n8n-nodes-base.function",
    "position": [1300, 200],
    "parameters": {
      "functionCode": `
        // Update database with new data
        // In a real implementation, this would be a database node
        
        const data = $input.item.json.new_data;
        
        // Update database
        // ...
        
        return {
          json: {
            success: true,
            message: "Database updated successfully",
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "sendNotifications",
    "type": "n8n-nodes-base.function",
    "position": [1500, 200],
    "parameters": {
      "functionCode": `
        // Send notifications for significant changes
        const changes = $input.item.json.changes;
        
        // Filter significant changes
        const significantChanges = changes.filter(change => change.is_significant);
        
        if (significantChanges.length > 0) {
          // Send notifications
          // In a real implementation, this would be a notification node
          
          // For demonstration, we'll just log the notifications
          console.log("Sending notifications for significant changes:", significantChanges);
        }
        
        return {
          json: {
            notifications_sent: significantChanges.length,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "noChanges",
    "type": "n8n-nodes-base.noOp",
    "position": [1300, 400],
    "parameters": {}
  }
]
```

## ダッシュボードのデプロイと運用

インタラクティブダッシュボードのデプロイと運用に関する要件を以下に示します。

### 1. デプロイ要件

1. **フロントエンドデプロイ**
   - React アプリケーションのビルドと最適化
   - 静的ファイルのホスティング（Netlify, Vercel, AWS S3など）
   - CDNの活用によるグローバルな高速アクセス

2. **バックエンドデプロイ**
   - n8nワークフローのデプロイ（n8n.io Cloud, Docker, Kubernetes）
   - APIエンドポイントの公開と認証の設定
   - データベースの設定と最適化

3. **セキュリティ要件**
   - HTTPS通信の強制
   - API認証（JWT, OAuth）
   - データアクセス制御
   - 監査ログの記録

### 2. 運用要件

1. **パフォーマンスモニタリング**
   - レスポンスタイムの監視
   - リソース使用率の監視
   - エラー率の監視

2. **データバックアップ**
   - 定期的なデータバックアップ
   - 障害復旧計画
   - データ整合性チェック

3. **更新とメンテナンス**
   - 定期的な機能更新
   - セキュリティパッチの適用
   - 依存ライブラリの更新

4. **ユーザーサポート**
   - ヘルプドキュメントの提供
   - フィードバック収集メカニズム
   - 問題報告と解決プロセス

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおけるインタラクティブダッシュボードの全体設計と実装要件について詳細に解説しました。ダッシュボードのアーキテクチャ、レイアウト、主要セクション、インタラクティブ機能、n8nによる統合、デプロイと運用要件など、多岐にわたる側面を網羅しました。

これらの設計と実装要件に基づいて、ユーザーは複雑な情報を直感的に理解し、効果的な意思決定を行うことができるインタラクティブダッシュボードを構築することができます。特に確信度の視覚的表現と代替シナリオの可視化を統合することで、情報不均衡が存在する状況でも堅牢な意思決定を支援することが可能になります。

次のセクションでは、実践的な例として特定業界向けAIレーダーの構築と運用について詳細に解説します。
