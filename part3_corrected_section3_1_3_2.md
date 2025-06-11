## 3. インターフェース設計と視覚化

コンセンサス基準と重み付けの結果を効果的にユーザーに提示するためには、適切なインターフェース設計と視覚化が不可欠です。本節では、ユーザーがコンセンサスモデルの出力を直感的に理解し、意思決定に活用できるようにするための設計概念と実装方法について詳細に解説します。

### 3.1. 多層的ダッシュボードの設計思想

コンセンサスモデルから得られる情報は多岐にわたり、様々な粒度と視点で分析できます。このような複雑な情報を効果的に提示するためには、ユーザーが必要に応じて情報の詳細度を選択できる多層的なダッシュボード設計が有効です。多層的ダッシュボードとは、情報を階層的に構造化し、ユーザーが必要に応じて掘り下げていける設計アプローチです。

多層的ダッシュボードの最上位層である「概要レベル」では、組織全体や部門全体に関わる主要なトピックの現在のコンセンサス状況を一覧表示します。この層では、各トピックの静止点の有無（安定した解釈が得られているかどうか）、主要スコア（統合スコア、重要度、確信度、整合性）、そして注意が必要なトピックの警告表示などが含まれます。経営層や意思決定者が全体状況を素早く把握し、注目すべきトピックを特定するのに役立ちます。

例えば、概要レベルのダッシュボードでは、以下のような要素が含まれます：

1. トピック一覧テーブル：トピック名、カテゴリ、静止点ステータス（検出済み/未検出）、統合スコア、最終更新日時などを表示
2. 重要度-確信度マトリックス：トピックを重要度と確信度の2軸でプロットし、優先度の高いトピックを視覚的に特定
3. トレンドグラフ：主要指標の時間的変化を示す簡易グラフ
4. アラート領域：閾値を超えた重要なトピックや、急激な変化があったトピックを強調表示

概要レベルのダッシュボードは、情報の網羅性よりも視認性と即時性を重視し、ユーザーが一目で全体状況を把握できるようにデザインされます。色彩やアイコンを効果的に使用し、重要な情報や異常値を直感的に認識できるようにすることが重要です。例えば、静止点が検出されたトピックは緑色、未検出のトピックは黄色、問題のあるトピックは赤色で表示するなど、視覚的な区別を明確にします。

中間層である「詳細レベル」では、ユーザーが選択した特定のトピックについて、より詳細な情報を提供します。この層では、3つの視点（テクノロジー、マーケット、ビジネス）それぞれの評価結果、視点間の重み付け、整合性の詳細、時系列での変化などが表示されます。アナリストや専門家が特定のトピックを深く分析し、判断の根拠を理解するのに適しています。

詳細レベルのダッシュボードには、以下のような要素が含まれます：

1. 視点別評価パネル：テクノロジー、マーケット、ビジネスの各視点からの評価結果（重要度、確信度、スコア）を詳細に表示
2. 重み付け情報パネル：現在の視点別重みとその調整要因（トピックの性質、変化の段階、確信度の差異）を説明
3. 整合性分析パネル：視点間の一致度、論理的整合性、時間的整合性、コンテキスト整合性の詳細スコアと解釈
4. 時系列グラフ：主要指標の時間的変化を詳細に示すグラフ（日次、週次、月次など複数の時間粒度で表示可能）
5. 関連情報パネル：評価の根拠となった主要な情報源、データポイント、専門家の意見などへのリンク

詳細レベルのダッシュボードでは、情報の関連性と文脈を重視し、ユーザーが評価結果の背景や根拠を理解できるようにデザインされます。視覚的な表現と詳細なテキスト説明を組み合わせ、複雑な情報を分かりやすく伝えることが重要です。例えば、レーダーチャートを用いて3つの視点のスコアバランスを視覚化し、その横に各スコアの意味と解釈を説明するテキストを配置するなど、視覚と言語の両面からの理解を促進します。

最下層である「調整レベル」では、ユーザーがシミュレーション的に重み付けや閾値を変更し、結果の変化をリアルタイムで確認できるインタラクティブなインターフェースを提供します。この層は、「もし〜だったら？」という仮説検証や感度分析を行いたいユーザーに適しており、異なるシナリオや前提条件での結果を比較検討することができます。

調整レベルのダッシュボードには、以下のような要素が含まれます：

1. パラメータ調整パネル：視点別重み、評価要素の重み、閾値などを調整するスライダーや入力フィールド
2. シミュレーション結果パネル：調整したパラメータに基づく新しい評価結果をリアルタイムで表示
3. 比較ビュー：現在の公式パラメータでの結果と、調整後のパラメータでの結果を並べて表示
4. シナリオ保存機能：特定のパラメータ設定をシナリオとして保存し、後で参照や共有が可能
5. 感度分析ツール：特定のパラメータの変化が結果に与える影響を自動的に分析し、視覚化

調整レベルのダッシュボードでは、インタラクティブ性と即時フィードバックを重視し、ユーザーが様々なパラメータの影響を直感的に理解できるようにデザインされます。変更の影響をリアルタイムで視覚化し、ユーザーの探索的な分析を支援することが重要です。例えば、重みを調整するとレーダーチャートの形状がリアルタイムで変化し、統合スコアや静止点の状態も即座に更新されるなど、操作と結果の関係を直接的に体験できるようにします。

これらの3つのレベルを統合した多層的ダッシュボードにより、様々な役割や目的を持つユーザーが、それぞれのニーズに合った方法でコンセンサスモデルの出力にアクセスし、活用することが可能になります。重要なのは、これらのレベル間をシームレスに移動できる導線設計であり、例えば概要レベルでトピックをクリックすると詳細レベルに移動し、詳細レベルで「シミュレーション」ボタンをクリックすると調整レベルに移動するなど、ユーザーの探索フローを自然にサポートする設計が求められます。

### 3.2. 効果的な視覚化コンポーネントの設計と実装

コンセンサスモデルの複雑な出力を理解しやすく伝えるためには、適切な視覚化コンポーネントの選択と実装が重要です。以下では、特に効果的な視覚化コンポーネントとその実装方法について詳細に解説します。

#### 全体フロー図：コンセンサスプロセスの可視化

コンセンサス基準と重み付けプロセスの全体像を示すフロー図は、ユーザーがシステムの動作原理を理解する上で非常に有効です。この図は、データの流れ、処理ステップ、判断ポイントを視覚的に表現し、複雑なプロセスを直感的に理解できるようにします。

全体フロー図の実装には、D3.jsやMermaidなどのライブラリが適しています。以下は、Reactコンポーネントとして実装されたMermaidベースのフロー図の例です。

```jsx
// React component for Consensus Process Flow Diagram
import React, { useEffect } from 'react';
import mermaid from 'mermaid';

const ConsensusFlowDiagram = () => {
  useEffect(() => {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
      }
    });
    mermaid.contentLoaded();
  }, []);

  const flowDefinition = `
    graph TD
      A[データ収集] --> B{視点別評価}
      B --> C[テクノロジー視点評価]
      B --> D[マーケット視点評価]
      B --> E[ビジネス視点評価]
      C --> F[整合性評価]
      D --> F
      E --> F
      F --> G{動的重み付け調整}
      G --> H[トピック性質による調整]
      G --> I[変化段階による調整]
      G --> J[確信度差異による調整]
      H --> K[重み付き統合]
      I --> K
      J --> K
      K --> L[整合性による調整]
      L --> M{静止点検出}
      M -- 検出 --> N[最終判断・アクション]
      M -- 未検出 --> O[代替解生成]
      O --> P[追加情報収集]
      P --> A
  `;

  return (
    <div className="consensus-flow-container">
      <h3>コンセンサスプロセスフロー</h3>
      <div className="mermaid">
        {flowDefinition}
      </div>
      <div className="flow-legend">
        <p><strong>凡例:</strong></p>
        <ul>
          <li><span className="process-node"></span> 処理ステップ</li>
          <li><span className="decision-node"></span> 判断ポイント</li>
          <li><span className="flow-arrow"></span> データフロー</li>
        </ul>
      </div>
    </div>
  );
};

export default ConsensusFlowDiagram;
```

この全体フロー図は、データ収集から最終判断までの一連のプロセスを視覚化し、各ステップの関係性と流れを明確に示しています。特に、3つの視点からの評価が整合性評価に集約され、動的重み付け調整を経て統合されるプロセスや、静止点検出の結果に応じた分岐など、システムの核心部分を理解しやすく表現しています。

フロー図の実装においては、色彩やアイコンを効果的に使用して情報の種類や重要度を区別することが重要です。また、インタラクティブな要素を追加し、各ノードをクリックすると詳細情報が表示されるなど、ユーザーの探索をサポートする機能も有効です。

#### レーダーチャート：多次元データの視覚化

3つの視点のスコアと重みを視覚的に比較するためのレーダーチャート（スパイダーチャートとも呼ばれる）は、バランスや偏りを直感的に把握するのに適しています。このチャートは、複数の軸（ディメンション）上の値を多角形として表現し、形状の特徴から全体的なパターンを読み取ることができます。

レーダーチャートの実装には、Chart.jsやHighchartsなどのライブラリが適しています。以下は、Chart.jsを使用したReactコンポーネントの例です。

```jsx
// React component for Perspective Radar Chart
import React from 'react';
import { Radar } from 'react-chartjs-2';

const PerspectiveRadarChart = ({ perspectiveData, weights }) => {
  const data = {
    labels: ['重要度', '確信度', '整合性', '影響範囲', '戦略的関連性', '時間的緊急性'],
    datasets: [
      {
        label: 'テクノロジー視点',
        data: perspectiveData.technology,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        pointBackgroundColor: 'rgb(54, 162, 235)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(54, 162, 235)'
      },
      {
        label: 'マーケット視点',
        data: perspectiveData.market,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        pointBackgroundColor: 'rgb(255, 99, 132)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(255, 99, 132)'
      },
      {
        label: 'ビジネス視点',
        data: perspectiveData.business,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgb(75, 192, 192)',
        pointBackgroundColor: 'rgb(75, 192, 192)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(75, 192, 192)'
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        angleLines: {
          display: true
        },
        suggestedMin: 0,
        suggestedMax: 1
      }
    },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '視点別評価比較'
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.dataset.label || '';
            const value = context.raw || 0;
            return `${label}: ${value.toFixed(2)}`;
          }
        }
      }
    }
  };

  return (
    <div className="radar-chart-container">
      <Radar data={data} options={options} height={300} />
      <div className="weights-display">
        <h4>現在の重み付け:</h4>
        <ul>
          <li>テクノロジー: {(weights.technology * 100).toFixed(0)}%</li>
          <li>マーケット: {(weights.market * 100).toFixed(0)}%</li>
          <li>ビジネス: {(weights.business * 100).toFixed(0)}%</li>
        </ul>
      </div>
    </div>
  );
};

export default PerspectiveRadarChart;
```

このレーダーチャートは、3つの視点それぞれの評価結果を6つの軸（重要度、確信度、整合性、影響範囲、戦略的関連性、時間的緊急性）上にプロットし、各視点の特性と強みを視覚的に比較できるようにしています。また、チャートの下部には現在の重み付け情報も表示し、視点間のバランスを理解する助けとなります。

レーダーチャートの実装においては、適切な軸の選択と配置が重要です。関連性の高い指標を隣接させ、全体的な形状から意味のあるパターンを読み取りやすくすることが望ましいです。また、チャートの大きさや色彩も重要な要素であり、視認性と情報の区別のバランスを考慮して設計する必要があります。

#### 時系列グラフ：変化の可視化

各視点のスコアや重みの時間変化を表示する時系列グラフは、トレンドや変化点を把握するのに役立ちます。このグラフは、過去の変化パターンを分析し、将来の予測や異常検出の基盤となる重要な視覚化ツールです。

時系列グラフの実装には、D3.jsやApexChartsなどのライブラリが適しています。以下は、ApexChartsを使用したReactコンポーネントの例です。

```jsx
// React component for Time Series Graph
import React from 'react';
import Chart from 'react-apexcharts';

const TimeSeriesGraph = ({ timeSeriesData, timeRange }) => {
  const options = {
    chart: {
      type: 'line',
      zoom: {
        enabled: true
      },
      toolbar: {
        show: true,
        tools: {
          download: true,
          selection: true,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: true,
          reset: true
        }
      }
    },
    stroke: {
      curve: 'smooth',
      width: 2
    },
    colors: ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6'],
    dataLabels: {
      enabled: false
    },
    markers: {
      size: 4,
      hover: {
        size: 6
      }
    },
    title: {
      text: 'スコアと重みの時間変化',
      align: 'left'
    },
    grid: {
      borderColor: '#e7e7e7',
      row: {
        colors: ['#f3f3f3', 'transparent'],
        opacity: 0.5
      }
    },
    xaxis: {
      categories: timeSeriesData.dates,
      title: {
        text: '日付'
      }
    },
    yaxis: {
      title: {
        text: 'スコア / 重み'
      },
      min: 0,
      max: 1
    },
    legend: {
      position: 'top',
      horizontalAlign: 'right',
      floating: true,
      offsetY: -25,
      offsetX: -5
    },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function (y) {
          if(typeof y !== "undefined") {
            return y.toFixed(3);
          }
          return y;
        }
      }
    }
  };

  const series = [
    {
      name: "統合スコア",
      data: timeSeriesData.integratedScores
    },
    {
      name: "テクノロジー重み",
      data: timeSeriesData.weights.technology
    },
    {
      name: "マーケット重み",
      data: timeSeriesData.weights.market
    },
    {
      name: "ビジネス重み",
      data: timeSeriesData.weights.business
    }
  ];

  // 時間範囲に応じたデータのフィルタリング
  const filterDataByTimeRange = () => {
    // timeRangeに応じたデータフィルタリングのロジック
    // 例: 'week', 'month', 'quarter', 'year'などの範囲でデータを絞り込む
    // ...
  };

  return (
    <div className="time-series-container">
      <div className="time-range-selector">
        <button className={timeRange === 'week' ? 'active' : ''}>週</button>
        <button className={timeRange === 'month' ? 'active' : ''}>月</button>
        <button className={timeRange === 'quarter' ? 'active' : ''}>四半期</button>
        <button className={timeRange === 'year' ? 'active' : ''}>年</button>
      </div>
      <Chart
        options={options}
        series={series}
        type="line"
        height={350}
      />
      <div className="time-series-insights">
        <h4>トレンド分析:</h4>
        <p>過去30日間で、テクノロジー視点の重みが10%増加し、統合スコアも0.05ポイント上昇しています。これは、技術的な実現可能性の向上を示唆しています。</p>
      </div>
    </div>
  );
};

export default TimeSeriesGraph;
```

この時系列グラフは、統合スコアと3つの視点の重みの時間変化を線グラフとして表示し、トレンドや相関関係を視覚的に把握できるようにしています。ズームや範囲選択などのインタラクティブな機能も備えており、ユーザーが特定の期間に焦点を当てて詳細に分析することができます。また、グラフの下部にはトレンド分析の要約も表示し、データの解釈をサポートしています。

時系列グラフの実装においては、適切な時間粒度の選択と切り替え機能が重要です。日次、週次、月次など、異なる時間スケールでのデータ表示を可能にし、短期的な変動と長期的なトレンドの両方を分析できるようにすることが望ましいです。また、重要なイベントや変化点にマーカーを付けるなど、コンテキスト情報の追加も有効です。

#### 重み調整インターフェース：インタラクティブな探索

ユーザーが重みや閾値を調整し、結果の変化をリアルタイムで確認できるインタラクティブなインターフェースは、「もし〜だったら？」という仮説検証や感度分析に不可欠です。このインターフェースにより、ユーザーは様々なシナリオを探索し、パラメータの影響を直感的に理解することができます。

重み調整インターフェースの実装には、ReactやVueなどのフロントエンドフレームワークと、スライダーやインプットフィールドなどのUIコンポーネントが適しています。以下は、Reactを使用した実装例です。

```jsx
// React component for Weight Adjustment Interface
import React, { useState, useEffect } from 'react';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';
import PerspectiveRadarChart from './PerspectiveRadarChart';

const WeightAdjustmentInterface = ({ initialWeights, perspectiveData, onWeightsChange }) => {
  const [weights, setWeights] = useState(initialWeights);
  const [normalizedWeights, setNormalizedWeights] = useState(initialWeights);
  const [simulationResults, setSimulationResults] = useState(null);
  
  // 重みの合計が1.0になるように正規化
  const normalizeWeights = (newWeights) => {
    const sum = Object.values(newWeights).reduce((a, b) => a + b, 0);
    const normalized = {};
    Object.keys(newWeights).forEach(key => {
      normalized[key] = newWeights[key] / sum;
    });
    return normalized;
  };
  
  // 重みが変更されたときの処理
  const handleWeightChange = (perspective, value) => {
    const newWeights = { ...weights, [perspective]: value };
    setWeights(newWeights);
    const normalized = normalizeWeights(newWeights);
    setNormalizedWeights(normalized);
    
    // 親コンポーネントに正規化された重みを通知
    if (onWeightsChange) {
      onWeightsChange(normalized);
    }
    
    // シミュレーション結果の計算（実際のアプリケーションではAPIリクエストなどで取得）
    simulateResults(normalized);
  };
  
  // シミュレーション結果の計算（簡易版）
  const simulateResults = (normalizedWeights) => {
    // 実際のアプリケーションでは、APIを呼び出して結果を取得
    // ここでは簡易的な計算を行う
    const techScore = perspectiveData.technology.reduce((a, b) => a + b, 0) / perspectiveData.technology.length;
    const marketScore = perspectiveData.market.reduce((a, b) => a + b, 0) / perspectiveData.market.length;
    const businessScore = perspectiveData.business.reduce((a, b) => a + b, 0) / perspectiveData.business.length;
    
    const integratedScore = 
      techScore * normalizedWeights.technology + 
      marketScore * normalizedWeights.market + 
      businessScore * normalizedWeights.business;
    
    const coherenceScore = 0.8; // 実際のアプリケーションでは計算される値
    const adjustedScore = integratedScore * (0.7 + 0.3 * coherenceScore);
    
    setSimulationResults({
      integratedScore,
      adjustedScore,
      staticPointDetected: adjustedScore > 0.75 // 簡易的な静止点検出
    });
  };
  
  // 初期化時にシミュレーション結果を計算
  useEffect(() => {
    simulateResults(normalizedWeights);
  }, []);
  
  return (
    <div className="weight-adjustment-container">
      <h3>重み付け調整シミュレーション</h3>
      
      <div className="weight-sliders">
        <div className="weight-slider-item">
          <label>テクノロジー視点の重み: {(normalizedWeights.technology * 100).toFixed(0)}%</label>
          <Slider
            min={1}
            max={100}
            value={weights.technology * 100}
            onChange={(value) => handleWeightChange('technology', value / 100)}
          />
        </div>
        
        <div className="weight-slider-item">
          <label>マーケット視点の重み: {(normalizedWeights.market * 100).toFixed(0)}%</label>
          <Slider
            min={1}
            max={100}
            value={weights.market * 100}
            onChange={(value) => handleWeightChange('market', value / 100)}
          />
        </div>
        
        <div className="weight-slider-item">
          <label>ビジネス視点の重み: {(normalizedWeights.business * 100).toFixed(0)}%</label>
          <Slider
            min={1}
            max={100}
            value={weights.business * 100}
            onChange={(value) => handleWeightChange('business', value / 100)}
          />
        </div>
      </div>
      
      <div className="simulation-results">
        <h4>シミュレーション結果:</h4>
        {simulationResults && (
          <>
            <p>統合スコア: <strong>{simulationResults.integratedScore.toFixed(3)}</strong></p>
            <p>調整後スコア: <strong>{simulationResults.adjustedScore.toFixed(3)}</strong></p>
            <p>静止点検出: <strong>{simulationResults.staticPointDetected ? '検出' : '未検出'}</strong></p>
          </>
        )}
      </div>
      
      <div className="visualization-container">
        <PerspectiveRadarChart perspectiveData={perspectiveData} weights={normalizedWeights} />
      </div>
      
      <div className="action-buttons">
        <button className="save-scenario-btn">現在の設定をシナリオとして保存</button>
        <button className="reset-btn">デフォルト設定にリセット</button>
      </div>
    </div>
  );
};

export default WeightAdjustmentInterface;
```

この重み調整インターフェースは、3つの視点の重みをスライダーで調整でき、調整結果がリアルタイムで反映されます。重みの合計は常に1.0（100%）になるように正規化され、調整に応じてシミュレーション結果（統合スコア、調整後スコア、静止点検出状態）が更新されます。また、レーダーチャートも連動して更新され、視覚的なフィードバックを提供します。

重み調整インターフェースの実装においては、直感的な操作性とリアルタイムフィードバックが重要です。スライダーの動きに合わせて即座に結果が更新されることで、ユーザーはパラメータと結果の関係を直感的に理解できます。また、現在の設定をシナリオとして保存し、後で比較できる機能も有用です。

#### 視点間関係図：関係性の可視化

視点間の整合性や影響度をノードとエッジで表現する関係図は、3つの視点の相互関係を理解するのに役立ちます。このグラフは、どの視点が他の視点と強く関連しているか、あるいは矛盾しているかを視覚的に示し、整合性の高い領域や問題領域を特定するのに有効です。

視点間関係図の実装には、D3.jsやSigmaJSなどのグラフ可視化ライブラリが適しています。以下は、D3.jsを使用したReactコンポーネントの例です。

```jsx
// React component for Perspective Relationship Graph
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const PerspectiveRelationshipGraph = ({ relationshipData }) => {
  const svgRef = useRef(null);
  
  useEffect(() => {
    if (!relationshipData || !svgRef.current) return;
    
    // SVG要素のサイズを設定
    const width = 600;
    const height = 400;
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    
    // SVG要素をクリア
    d3.select(svgRef.current).selectAll("*").remove();
    
    // SVG要素を作成
    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height);
    
    // ノードとリンクのデータを準備
    const nodes = [
      { id: "technology", name: "テクノロジー", group: 1 },
      { id: "market", name: "マーケット", group: 2 },
      { id: "business", name: "ビジネス", group: 3 }
    ];
    
    const links = [
      { 
        source: "technology", 
        target: "market", 
        value: relationshipData.technology_market.coherence,
        type: relationshipData.technology_market.type
      },
      { 
        source: "market", 
        target: "business", 
        value: relationshipData.market_business.coherence,
        type: relationshipData.market_business.type
      },
      { 
        source: "business", 
        target: "technology", 
        value: relationshipData.business_technology.coherence,
        type: relationshipData.business_technology.type
      }
    ];
    
    // フォースシミュレーションを作成
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));
    
    // リンク（エッジ）を描画
    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .enter().append("line")
      .attr("stroke-width", d => Math.max(1, d.value * 5))
      .attr("stroke", d => {
        switch(d.type) {
          case "reinforcing": return "#2ecc71"; // 強化関係（緑）
          case "conflicting": return "#e74c3c"; // 対立関係（赤）
          default: return "#3498db"; // 中立関係（青）
        }
      })
      .attr("stroke-dasharray", d => d.type === "conflicting" ? "5,5" : "none");
    
    // リンクのラベルを描画
    const linkText = svg.append("g")
      .selectAll("text")
      .data(links)
      .enter().append("text")
      .text(d => d.value.toFixed(2))
      .attr("font-size", 10)
      .attr("text-anchor", "middle")
      .attr("dy", -5);
    
    // ノードを描画
    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .enter().append("circle")
      .attr("r", 30)
      .attr("fill", d => {
        switch(d.group) {
          case 1: return "#3498db"; // テクノロジー（青）
          case 2: return "#e74c3c"; // マーケット（赤）
          case 3: return "#2ecc71"; // ビジネス（緑）
          default: return "#95a5a6"; // その他（灰色）
        }
      })
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));
    
    // ノードのラベルを描画
    const nodeText = svg.append("g")
      .selectAll("text")
      .data(nodes)
      .enter().append("text")
      .text(d => d.name)
      .attr("font-size", 12)
      .attr("text-anchor", "middle")
      .attr("dy", 5);
    
    // シミュレーションの更新関数
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      
      linkText
        .attr("x", d => (d.source.x + d.target.x) / 2)
        .attr("y", d => (d.source.y + d.target.y) / 2);
      
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
      
      nodeText
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });
    
    // ドラッグ関連の関数
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
    
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    
  }, [relationshipData]);
  
  return (
    <div className="relationship-graph-container">
      <h3>視点間の関係性</h3>
      <svg ref={svgRef}></svg>
      <div className="graph-legend">
        <h4>凡例:</h4>
        <div className="legend-item">
          <span className="line reinforcing"></span> 強化関係（整合性高）
        </div>
        <div className="legend-item">
          <span className="line neutral"></span> 中立関係（整合性中）
        </div>
        <div className="legend-item">
          <span className="line conflicting"></span> 対立関係（整合性低）
        </div>
      </div>
      <div className="relationship-insights">
        <p>テクノロジー視点とマーケット視点の間に強い整合性（0.85）があり、両者が相互に強化し合っています。一方、ビジネス視点とテクノロジー視点の間には中程度の整合性（0.62）があります。</p>
      </div>
    </div>
  );
};

export default PerspectiveRelationshipGraph;
```

この視点間関係図は、3つの視点をノードとして表現し、それらの間の関係性をエッジとして視覚化しています。エッジの太さは整合性の強さを、色と線種は関係の種類（強化、中立、対立）を示しています。また、ノードはドラッグして移動でき、ユーザーが最も見やすい配置に調整することができます。グラフの下部には凡例と関係性の解釈も表示し、データの理解をサポートしています。

視点間関係図の実装においては、視覚的な明確さと情報の豊かさのバランスが重要です。ノードとエッジの視覚的属性（サイズ、色、形状など）を効果的に使用して、複数の次元の情報を同時に伝えることができます。また、インタラクティブな要素（ホバー時の詳細表示、ズーム、フィルタリングなど）を追加することで、ユーザーの探索をさらにサポートすることができます。

以上のように、適切に設計された視覚化コンポーネントは、コンセンサスモデルの複雑な出力を理解しやすく伝え、ユーザーの意思決定をサポートする強力なツールとなります。次のセクションでは、これらの視覚化コンポーネントをn8nワークフローと連携させる方法について解説します。
