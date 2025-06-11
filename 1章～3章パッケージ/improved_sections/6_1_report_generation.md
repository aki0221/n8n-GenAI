### 6.1 レポート生成

コンセンサスモデルの出力コンポーネントの中核となるレポート生成機能は、分析結果や意思決定の根拠を明確かつ分かりやすく伝えるための重要な役割を担っています。適切に設計されたレポートは、意思決定者や関係者に対して、複雑な分析プロセスの結果を理解しやすい形で提示し、情報に基づいた判断を促進します。n8nを活用することで、このレポート生成プロセスを効率的かつカスタマイズ性高く実装することができます。

**レポートテンプレートの設計と実装**

レポート生成の基盤となるのは、目的や対象者に応じて最適化されたレポートテンプレートです。これにより、一貫性のある情報提示と、必要な情報の漏れのない伝達が可能になります。

n8nでのレポートテンプレートの設計と実装方法としては、主にHTTPリクエストノード、FunctionノードおよびTemplateノードが活用されます。以下に、具体的な実装例を示します：

**HTMLテンプレートの実装**:
視覚的に整理された情報を提供するHTMLベースのレポートテンプレートを実装します。

```javascript
// HTMLテンプレートの実装例（Templateノード）
const data = $input.item.json;

// レポートのメタデータ
const reportMeta = {
  title: "コンセンサスモデル分析レポート",
  generated_date: new Date().toLocaleString('ja-JP'),
  version: "1.0",
  target_name: data.target_name || "未指定",
  target_id: data.target_id || "未指定"
};

// HTMLテンプレートの構築
const htmlTemplate = `
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${reportMeta.title} - ${reportMeta.target_name}</title>
  <style>
    body {
      font-family: 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }
    .report-header {
      border-bottom: 2px solid #2c3e50;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }
    .report-title {
      color: #2c3e50;
      font-size: 28px;
      margin-bottom: 10px;
    }
    .report-meta {
      color: #7f8c8d;
      font-size: 14px;
    }
    .section {
      margin-bottom: 30px;
    }
    .section-title {
      color: #2c3e50;
      font-size: 22px;
      border-bottom: 1px solid #eee;
      padding-bottom: 10px;
      margin-bottom: 15px;
    }
    .subsection-title {
      color: #34495e;
      font-size: 18px;
      margin-top: 20px;
      margin-bottom: 10px;
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
    }
    .data-table th, .data-table td {
      border: 1px solid #ddd;
      padding: 12px;
      text-align: left;
    }
    .data-table th {
      background-color: #f2f2f2;
      color: #333;
    }
    .data-table tr:nth-child(even) {
      background-color: #f9f9f9;
    }
    .chart-container {
      margin: 20px 0;
      max-width: 100%;
      height: 400px;
    }
    .score-card {
      display: inline-block;
      width: 30%;
      margin: 1%;
      padding: 15px;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      text-align: center;
    }
    .score-card.technology {
      background-color: #e8f4f8;
      border-left: 5px solid #3498db;
    }
    .score-card.market {
      background-color: #f8f4e8;
      border-left: 5px solid #f39c12;
    }
    .score-card.business {
      background-color: #e8f8e8;
      border-left: 5px solid #2ecc71;
    }
    .score-value {
      font-size: 32px;
      font-weight: bold;
      margin: 10px 0;
    }
    .score-label {
      font-size: 16px;
      color: #7f8c8d;
    }
    .consensus-score {
      font-size: 42px;
      font-weight: bold;
      text-align: center;
      color: #2c3e50;
      margin: 30px 0;
    }
    .recommendation {
      background-color: #f8f9fa;
      border-left: 5px solid #5bc0de;
      padding: 15px;
      margin: 20px 0;
    }
    .footer {
      margin-top: 50px;
      padding-top: 20px;
      border-top: 1px solid #eee;
      font-size: 12px;
      color: #7f8c8d;
      text-align: center;
    }
  </style>
</head>
<body>
  <!-- レポートヘッダー -->
  <div class="report-header">
    <h1 class="report-title">${reportMeta.title}</h1>
    <div class="report-meta">
      <p>対象: ${reportMeta.target_name} (ID: ${reportMeta.target_id})</p>
      <p>生成日時: ${reportMeta.generated_date}</p>
      <p>レポートバージョン: ${reportMeta.version}</p>
    </div>
  </div>

  <!-- エグゼクティブサマリー -->
  <div class="section">
    <h2 class="section-title">エグゼクティブサマリー</h2>
    <p>${data.executive_summary || "エグゼクティブサマリーは生成されていません。"}</p>
    
    <!-- 総合スコア -->
    <div class="consensus-score">
      総合評価: ${(data.consensus_score * 100).toFixed(1)}点
    </div>
    
    <!-- 視点別スコアカード -->
    <div class="score-cards">
      <div class="score-card technology">
        <div class="score-label">テクノロジー視点</div>
        <div class="score-value">${(data.perspective_scores?.technology?.score * 100).toFixed(1) || "N/A"}</div>
      </div>
      <div class="score-card market">
        <div class="score-label">マーケット視点</div>
        <div class="score-value">${(data.perspective_scores?.market?.score * 100).toFixed(1) || "N/A"}</div>
      </div>
      <div class="score-card business">
        <div class="score-label">ビジネス視点</div>
        <div class="score-value">${(data.perspective_scores?.business?.score * 100).toFixed(1) || "N/A"}</div>
      </div>
    </div>
    
    <!-- 主な推奨事項 -->
    <div class="recommendation">
      <h3>主な推奨事項</h3>
      <p>${data.key_recommendations || "推奨事項は生成されていません。"}</p>
    </div>
  </div>

  <!-- 詳細分析結果 -->
  <div class="section">
    <h2 class="section-title">詳細分析結果</h2>
    
    <!-- テクノロジー視点 -->
    <div class="subsection">
      <h3 class="subsection-title">テクノロジー視点の分析</h3>
      <p>${data.technology_analysis?.summary || "テクノロジー視点の分析結果は利用できません。"}</p>
      
      <!-- テクノロジー指標テーブル -->
      <table class="data-table">
        <thead>
          <tr>
            <th>評価指標</th>
            <th>スコア</th>
            <th>重み</th>
            <th>コメント</th>
          </tr>
        </thead>
        <tbody>
          ${generateMetricsTableRows(data.technology_analysis?.metrics)}
        </tbody>
      </table>
    </div>
    
    <!-- マーケット視点 -->
    <div class="subsection">
      <h3 class="subsection-title">マーケット視点の分析</h3>
      <p>${data.market_analysis?.summary || "マーケット視点の分析結果は利用できません。"}</p>
      
      <!-- マーケット指標テーブル -->
      <table class="data-table">
        <thead>
          <tr>
            <th>評価指標</th>
            <th>スコア</th>
            <th>重み</th>
            <th>コメント</th>
          </tr>
        </thead>
        <tbody>
          ${generateMetricsTableRows(data.market_analysis?.metrics)}
        </tbody>
      </table>
    </div>
    
    <!-- ビジネス視点 -->
    <div class="subsection">
      <h3 class="subsection-title">ビジネス視点の分析</h3>
      <p>${data.business_analysis?.summary || "ビジネス視点の分析結果は利用できません。"}</p>
      
      <!-- ビジネス指標テーブル -->
      <table class="data-table">
        <thead>
          <tr>
            <th>評価指標</th>
            <th>スコア</th>
            <th>重み</th>
            <th>コメント</th>
          </tr>
        </thead>
        <tbody>
          ${generateMetricsTableRows(data.business_analysis?.metrics)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- コンセンサス形成プロセス -->
  <div class="section">
    <h2 class="section-title">コンセンサス形成プロセス</h2>
    <p>${data.consensus_process?.summary || "コンセンサス形成プロセスの詳細は利用できません。"}</p>
    
    <!-- 視点間の矛盾・対立 -->
    <div class="subsection">
      <h3 class="subsection-title">視点間の矛盾・対立</h3>
      <p>${data.consensus_process?.contradictions?.summary || "視点間の矛盾・対立は検出されませんでした。"}</p>
      
      <!-- 矛盾テーブル -->
      ${generateContradictionsTable(data.consensus_process?.contradictions?.details)}
    </div>
    
    <!-- 合意形成の経緯 -->
    <div class="subsection">
      <h3 class="subsection-title">合意形成の経緯</h3>
      <p>${data.consensus_process?.formation?.summary || "合意形成の経緯の詳細は利用できません。"}</p>
    </div>
  </div>

  <!-- 推奨事項と次のステップ -->
  <div class="section">
    <h2 class="section-title">推奨事項と次のステップ</h2>
    <p>${data.recommendations?.summary || "推奨事項の詳細は利用できません。"}</p>
    
    <!-- 推奨アクション -->
    <div class="subsection">
      <h3 class="subsection-title">推奨アクション</h3>
      <ul>
        ${generateRecommendationsList(data.recommendations?.actions)}
      </ul>
    </div>
    
    <!-- リスクと考慮事項 -->
    <div class="subsection">
      <h3 class="subsection-title">リスクと考慮事項</h3>
      <p>${data.recommendations?.risks || "リスクと考慮事項の詳細は利用できません。"}</p>
    </div>
  </div>

  <!-- フッター -->
  <div class="footer">
    <p>このレポートはコンセンサスモデルによって自動生成されました。</p>
    <p>© ${new Date().getFullYear()} コンセンサスモデル分析システム</p>
  </div>
</body>
</html>
`;

// ヘルパー関数：メトリクステーブル行の生成
function generateMetricsTableRows(metrics) {
  if (!metrics || metrics.length === 0) {
    return '<tr><td colspan="4">データがありません</td></tr>';
  }
  
  return metrics.map(metric => `
    <tr>
      <td>${metric.name || "未指定"}</td>
      <td>${(metric.score * 100).toFixed(1) || "N/A"}</td>
      <td>${(metric.weight * 100).toFixed(0) || "N/A"}%</td>
      <td>${metric.comment || ""}</td>
    </tr>
  `).join('');
}

// ヘルパー関数：矛盾テーブルの生成
function generateContradictionsTable(contradictions) {
  if (!contradictions || contradictions.length === 0) {
    return '<p>検出された矛盾はありません。</p>';
  }
  
  return `
    <table class="data-table">
      <thead>
        <tr>
          <th>矛盾ID</th>
          <th>関連視点</th>
          <th>矛盾の内容</th>
          <th>解決方法</th>
        </tr>
      </thead>
      <tbody>
        ${contradictions.map((contradiction, index) => `
          <tr>
            <td>C${index + 1}</td>
            <td>${contradiction.perspectives?.join(' vs ') || "未指定"}</td>
            <td>${contradiction.description || "未指定"}</td>
            <td>${contradiction.resolution || "未解決"}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

// ヘルパー関数：推奨事項リストの生成
function generateRecommendationsList(actions) {
  if (!actions || actions.length === 0) {
    return '<li>推奨アクションはありません</li>';
  }
  
  return actions.map(action => `
    <li>
      <strong>${action.title || "未指定"}</strong>: 
      ${action.description || ""}
      ${action.priority ? `<em>(優先度: ${action.priority})</em>` : ""}
    </li>
  `).join('');
}

return { html: htmlTemplate };
```

このようなHTMLテンプレートを実装することで、視覚的に整理された情報を提供するレポートを生成することができます。CSSスタイリングにより、重要な情報が強調され、データテーブルや視点別スコアカードなどの要素により、情報が構造化されて提示されます。

**マークダウンテンプレートの実装**:
テキストベースの環境でも読みやすいマークダウン形式のレポートテンプレートを実装します。

```javascript
// マークダウンテンプレートの実装例（Templateノード）
const data = $input.item.json;

// レポートのメタデータ
const reportMeta = {
  title: "コンセンサスモデル分析レポート",
  generated_date: new Date().toLocaleString('ja-JP'),
  version: "1.0",
  target_name: data.target_name || "未指定",
  target_id: data.target_id || "未指定"
};

// マークダウンテンプレートの構築
const markdownTemplate = `
# ${reportMeta.title}

## レポート情報
- **対象**: ${reportMeta.target_name} (ID: ${reportMeta.target_id})
- **生成日時**: ${reportMeta.generated_date}
- **レポートバージョン**: ${reportMeta.version}

## エグゼクティブサマリー

${data.executive_summary || "エグゼクティブサマリーは生成されていません。"}

### 総合評価: ${(data.consensus_score * 100).toFixed(1)}点

| 視点 | スコア |
|------|--------|
| テクノロジー視点 | ${(data.perspective_scores?.technology?.score * 100).toFixed(1) || "N/A"} |
| マーケット視点 | ${(data.perspective_scores?.market?.score * 100).toFixed(1) || "N/A"} |
| ビジネス視点 | ${(data.perspective_scores?.business?.score * 100).toFixed(1) || "N/A"} |

### 主な推奨事項

${data.key_recommendations || "推奨事項は生成されていません。"}

## 詳細分析結果

### テクノロジー視点の分析

${data.technology_analysis?.summary || "テクノロジー視点の分析結果は利用できません。"}

#### 評価指標

${generateMetricsTableMd(data.technology_analysis?.metrics)}

### マーケット視点の分析

${data.market_analysis?.summary || "マーケット視点の分析結果は利用できません。"}

#### 評価指標

${generateMetricsTableMd(data.market_analysis?.metrics)}

### ビジネス視点の分析

${data.business_analysis?.summary || "ビジネス視点の分析結果は利用できません。"}

#### 評価指標

${generateMetricsTableMd(data.business_analysis?.metrics)}

## コンセンサス形成プロセス

${data.consensus_process?.summary || "コンセンサス形成プロセスの詳細は利用できません。"}

### 視点間の矛盾・対立

${data.consensus_process?.contradictions?.summary || "視点間の矛盾・対立は検出されませんでした。"}

${generateContradictionsTableMd(data.consensus_process?.contradictions?.details)}

### 合意形成の経緯

${data.consensus_process?.formation?.summary || "合意形成の経緯の詳細は利用できません。"}

## 推奨事項と次のステップ

${data.recommendations?.summary || "推奨事項の詳細は利用できません。"}

### 推奨アクション

${generateRecommendationsListMd(data.recommendations?.actions)}

### リスクと考慮事項

${data.recommendations?.risks || "リスクと考慮事項の詳細は利用できません。"}

---

*このレポートはコンセンサスモデルによって自動生成されました。*  
*© ${new Date().getFullYear()} コンセンサスモデル分析システム*
`;

// ヘルパー関数：メトリクステーブルの生成（マークダウン形式）
function generateMetricsTableMd(metrics) {
  if (!metrics || metrics.length === 0) {
    return 'データがありません';
  }
  
  let table = '| 評価指標 | スコア | 重み | コメント |\n';
  table += '|----------|--------|------|----------|\n';
  
  metrics.forEach(metric => {
    table += `| ${metric.name || "未指定"} | ${(metric.score * 100).toFixed(1) || "N/A"} | ${(metric.weight * 100).toFixed(0) || "N/A"}% | ${metric.comment || ""} |\n`;
  });
  
  return table;
}

// ヘルパー関数：矛盾テーブルの生成（マークダウン形式）
function generateContradictionsTableMd(contradictions) {
  if (!contradictions || contradictions.length === 0) {
    return '検出された矛盾はありません。';
  }
  
  let table = '| 矛盾ID | 関連視点 | 矛盾の内容 | 解決方法 |\n';
  table += '|---------|----------|------------|----------|\n';
  
  contradictions.forEach((contradiction, index) => {
    table += `| C${index + 1} | ${contradiction.perspectives?.join(' vs ') || "未指定"} | ${contradiction.description || "未指定"} | ${contradiction.resolution || "未解決"} |\n`;
  });
  
  return table;
}

// ヘルパー関数：推奨事項リストの生成（マークダウン形式）
function generateRecommendationsListMd(actions) {
  if (!actions || actions.length === 0) {
    return '- 推奨アクションはありません';
  }
  
  let list = '';
  actions.forEach(action => {
    list += `- **${action.title || "未指定"}**: ${action.description || ""} ${action.priority ? `*(優先度: ${action.priority})*` : ""}\n`;
  });
  
  return list;
}

return { markdown: markdownTemplate };
```

このようなマークダウンテンプレートを実装することで、テキストベースの環境でも読みやすいレポートを生成することができます。マークダウン形式は、メール送信やドキュメント管理システムへの統合など、様々な用途に適しています。

**PDFレポート生成の実装**:
HTMLテンプレートをベースに、印刷や保存に適したPDF形式のレポートを生成します。

```javascript
// PDFレポート生成の実装例（Functionノード）
async function generatePdfReport(items) {
  // HTMLテンプレートを取得
  const htmlTemplate = items[0].json.html;
  
  // PDFの設定
  const pdfOptions = {
    format: 'A4',
    margin: {
      top: '20mm',
      right: '20mm',
      bottom: '20mm',
      left: '20mm'
    },
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<div style="font-size: 8px; text-align: center; width: 100%;">コンセンサスモデル分析レポート</div>',
    footerTemplate: '<div style="font-size: 8px; text-align: center; width: 100%;">ページ <span class="pageNumber"></span> / <span class="totalPages"></span></div>'
  };
  
  // PDF生成のためのHTTPリクエスト
  const response = await fetch('http://pdf-service:3000/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      html: htmlTemplate,
      options: pdfOptions
    })
  });
  
  if (!response.ok) {
    throw new Error(`PDF生成に失敗しました: ${response.statusText}`);
  }
  
  // PDFデータを取得
  const pdfBuffer = await response.arrayBuffer();
  const pdfBase64 = Buffer.from(pdfBuffer).toString('base64');
  
  return [{ json: { pdf_base64: pdfBase64 } }];
}

// メイン処理
return generatePdfReport($input.all());
```

このようなPDFレポート生成ロジックを実装することで、HTMLテンプレートをベースに、印刷や保存に適したPDF形式のレポートを生成することができます。PDFは、公式文書や印刷物として配布する場合に適しています。

**データ可視化の実装方法**

レポートの理解を促進するためには、データの可視化が重要です。グラフやチャートにより、複雑なデータの傾向やパターンを直感的に把握することができます。

n8nでのデータ可視化の実装方法としては、主にHTTPリクエストノードとFunctionノードが活用されます。以下に、具体的な実装例を示します：

**レーダーチャートの実装**:
各視点のスコアをレーダーチャート（スパイダーチャート）で可視化し、バランスを直感的に把握できるようにします。

```javascript
// レーダーチャートの実装例（Functionノード）
function generateRadarChartData(items) {
  // 分析データを取得
  const data = items[0].json;
  
  // 視点別スコアを取得
  const perspectives = ['technology', 'market', 'business'];
  const scores = perspectives.map(p => {
    return data.perspective_scores && data.perspective_scores[p] ? 
      data.perspective_scores[p].score : 0;
  });
  
  // Chart.jsのデータ形式に変換
  const chartData = {
    type: 'radar',
    data: {
      labels: ['テクノロジー視点', 'マーケット視点', 'ビジネス視点'],
      datasets: [{
        label: '視点別スコア',
        data: scores.map(s => s * 100), // 0-1のスコアを0-100に変換
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        pointBackgroundColor: 'rgb(54, 162, 235)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(54, 162, 235)'
      }]
    },
    options: {
      scales: {
        r: {
          angleLines: {
            display: true
          },
          suggestedMin: 0,
          suggestedMax: 100
        }
      }
    }
  };
  
  return [{ json: { chart_data: chartData } }];
}

// メイン処理
return generateRadarChartData($input.all());
```

このようなレーダーチャートのデータ生成ロジックを実装することで、各視点のスコアをレーダーチャートで可視化し、バランスを直感的に把握できるようにすることができます。Chart.jsなどのライブラリと組み合わせることで、インタラクティブなチャートを生成することも可能です。

**棒グラフの実装**:
各評価指標のスコアを棒グラフで可視化し、強みと弱みを明確に把握できるようにします。

```javascript
// 棒グラフの実装例（Functionノード）
function generateBarChartData(items) {
  // 分析データを取得
  const data = items[0].json;
  
  // 視点ごとの評価指標を取得
  const perspectives = ['technology', 'market', 'business'];
  const metricsByPerspective = {};
  
  perspectives.forEach(p => {
    const analysisKey = `${p}_analysis`;
    if (data[analysisKey] && data[analysisKey].metrics) {
      metricsByPerspective[p] = data[analysisKey].metrics;
    } else {
      metricsByPerspective[p] = [];
    }
  });
  
  // 各視点の棒グラフデータを生成
  const chartDataByPerspective = {};
  
  for (const [perspective, metrics] of Object.entries(metricsByPerspective)) {
    // メトリクス名とスコアを抽出
    const labels = metrics.map(m => m.name || '未指定');
    const scores = metrics.map(m => (m.score || 0) * 100); // 0-1のスコアを0-100に変換
    
    // 視点ごとの色を設定
    let backgroundColor, borderColor;
    switch (perspective) {
      case 'technology':
        backgroundColor = 'rgba(54, 162, 235, 0.2)';
        borderColor = 'rgb(54, 162, 235)';
        break;
      case 'market':
        backgroundColor = 'rgba(255, 159, 64, 0.2)';
        borderColor = 'rgb(255, 159, 64)';
        break;
      case 'business':
        backgroundColor = 'rgba(75, 192, 192, 0.2)';
        borderColor = 'rgb(75, 192, 192)';
        break;
      default:
        backgroundColor = 'rgba(201, 203, 207, 0.2)';
        borderColor = 'rgb(201, 203, 207)';
    }
    
    // Chart.jsのデータ形式に変換
    chartDataByPerspective[perspective] = {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: getPerspectiveLabel(perspective),
          data: scores,
          backgroundColor: backgroundColor,
          borderColor: borderColor,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    };
  }
  
  return [{ json: { chart_data_by_perspective: chartDataByPerspective } }];
}

// 視点のラベルを取得
function getPerspectiveLabel(perspective) {
  switch (perspective) {
    case 'technology': return 'テクノロジー視点の評価指標';
    case 'market': return 'マーケット視点の評価指標';
    case 'business': return 'ビジネス視点の評価指標';
    default: return '評価指標';
  }
}

// メイン処理
return generateBarChartData($input.all());
```

このような棒グラフのデータ生成ロジックを実装することで、各評価指標のスコアを棒グラフで可視化し、強みと弱みを明確に把握できるようにすることができます。視点ごとに色分けすることで、情報の整理と理解を促進します。

**ヒートマップの実装**:
視点間の矛盾や対立を色の濃淡で表現するヒートマップを実装し、注目すべき領域を視覚的に強調します。

```javascript
// ヒートマップの実装例（Functionノード）
function generateHeatmapData(items) {
  // 分析データを取得
  const data = items[0].json;
  
  // 視点間の矛盾データを取得
  const contradictions = data.consensus_process?.contradictions?.details || [];
  
  // 視点のリスト
  const perspectives = ['technology', 'market', 'business'];
  
  // 矛盾の強度マトリックスを初期化
  const contradictionMatrix = [];
  for (let i = 0; i < perspectives.length; i++) {
    contradictionMatrix[i] = [];
    for (let j = 0; j < perspectives.length; j++) {
      // 同じ視点同士の場合は0、それ以外は初期値0
      contradictionMatrix[i][j] = 0;
    }
  }
  
  // 矛盾データから強度マトリックスを構築
  for (const contradiction of contradictions) {
    if (contradiction.perspectives && contradiction.perspectives.length === 2) {
      const p1Index = perspectives.indexOf(contradiction.perspectives[0]);
      const p2Index = perspectives.indexOf(contradiction.perspectives[1]);
      
      if (p1Index !== -1 && p2Index !== -1) {
        // 矛盾の強度（0-1の範囲）
        const intensity = contradiction.intensity || 0.5;
        
        // マトリックスの対称位置に強度を設定
        contradictionMatrix[p1Index][p2Index] += intensity;
        contradictionMatrix[p2Index][p1Index] += intensity;
      }
    }
  }
  
  // 最大値で正規化
  let maxIntensity = 0;
  for (let i = 0; i < perspectives.length; i++) {
    for (let j = 0; j < perspectives.length; j++) {
      maxIntensity = Math.max(maxIntensity, contradictionMatrix[i][j]);
    }
  }
  
  if (maxIntensity > 0) {
    for (let i = 0; i < perspectives.length; i++) {
      for (let j = 0; j < perspectives.length; j++) {
        contradictionMatrix[i][j] = contradictionMatrix[i][j] / maxIntensity;
      }
    }
  }
  
  // Chart.jsのヒートマップデータ形式に変換
  const chartData = {
    type: 'heatmap',
    data: {
      labels: perspectives.map(getPerspectiveLabel),
      datasets: perspectives.map((p, i) => ({
        label: getPerspectiveLabel(p),
        data: contradictionMatrix[i].map((value, j) => ({
          x: j,
          y: i,
          v: value
        }))
      }))
    },
    options: {
      plugins: {
        colorschemes: {
          scheme: 'brewer.YlOrRd9'
        }
      },
      scales: {
        x: {
          type: 'category',
          labels: perspectives.map(getPerspectiveLabel)
        },
        y: {
          type: 'category',
          labels: perspectives.map(getPerspectiveLabel)
        }
      }
    }
  };
  
  return [{ json: { heatmap_data: chartData } }];
}

// 視点のラベルを取得
function getPerspectiveLabel(perspective) {
  switch (perspective) {
    case 'technology': return 'テクノロジー';
    case 'market': return 'マーケット';
    case 'business': return 'ビジネス';
    default: return perspective;
  }
}

// メイン処理
return generateHeatmapData($input.all());
```

このようなヒートマップのデータ生成ロジックを実装することで、視点間の矛盾や対立を色の濃淡で表現するヒートマップを生成し、注目すべき領域を視覚的に強調することができます。これにより、コンセンサス形成プロセスにおける重要なポイントを直感的に把握することが可能になります。

**レポート配信の実装方法**

生成されたレポートを適切な形式で関係者に配信することも、レポート生成機能の重要な要素です。配信方法は、用途や対象者に応じて最適化する必要があります。

n8nでのレポート配信の実装方法としては、主にEmailノード、HTTPリクエストノード、Slackノードなどが活用されます。以下に、具体的な実装例を示します：

**メール配信の実装**:
生成されたレポートをメールに添付して配信します。

```javascript
// メール配信の実装例（Emailノード）
// 設定例
{
  "fromEmail": "consensus-model@example.com",
  "fromName": "コンセンサスモデル分析システム",
  "to": "{{$node.GetRecipients.json.recipients}}",
  "cc": "{{$node.GetRecipients.json.cc_recipients}}",
  "subject": "コンセンサスモデル分析レポート: {{$node.GetReportData.json.target_name}}",
  "text": "添付のレポートをご確認ください。\n\n対象: {{$node.GetReportData.json.target_name}}\n生成日時: {{$node.GetReportData.json.generated_date}}\n\nこのメールはコンセンサスモデル分析システムによって自動送信されています。",
  "html": "<p>添付のレポートをご確認ください。</p><p><strong>対象:</strong> {{$node.GetReportData.json.target_name}}<br><strong>生成日時:</strong> {{$node.GetReportData.json.generated_date}}</p><p>このメールはコンセンサスモデル分析システムによって自動送信されています。</p>",
  "attachments": [
    {
      "filename": "consensus_report_{{$node.GetReportData.json.target_id}}.pdf",
      "content": "{{$node.GeneratePDF.json.pdf_base64}}",
      "contentType": "application/pdf",
      "contentDisposition": "attachment"
    },
    {
      "filename": "consensus_report_{{$node.GetReportData.json.target_id}}.md",
      "content": "{{$node.GenerateMarkdown.json.markdown}}",
      "contentType": "text/markdown",
      "contentDisposition": "attachment"
    }
  ]
}
```

このようなメール配信の設定を実装することで、生成されたレポートをPDFやマークダウン形式でメールに添付して配信することができます。宛先リストを動的に生成することで、関係者に応じた配信先の管理も可能です。

**Slack通知の実装**:
レポートの要約をSlackチャンネルに投稿し、詳細レポートへのリンクを提供します。

```javascript
// Slack通知の実装例（Slackノード）
// 設定例
{
  "channel": "{{$node.GetChannelConfig.json.channel}}",
  "text": "新しいコンセンサスモデル分析レポートが生成されました",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "コンセンサスモデル分析レポート",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*対象:* {{$node.GetReportData.json.target_name}}\n*生成日時:* {{$node.GetReportData.json.generated_date}}\n*総合評価:* {{$node.GetReportData.json.consensus_score_formatted}}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*エグゼクティブサマリー*\n{{$node.GetReportData.json.executive_summary_short}}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*視点別スコア*\n• テクノロジー視点: {{$node.GetReportData.json.technology_score_formatted}}\n• マーケット視点: {{$node.GetReportData.json.market_score_formatted}}\n• ビジネス視点: {{$node.GetReportData.json.business_score_formatted}}"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "詳細レポートを表示",
            "emoji": true
          },
          "url": "{{$node.GetReportData.json.report_url}}"
        }
      ]
    }
  ]
}
```

このようなSlack通知の設定を実装することで、レポートの要約をSlackチャンネルに投稿し、詳細レポートへのリンクを提供することができます。これにより、チーム内での情報共有と議論を促進することができます。

**ダッシュボード連携の実装**:
レポートデータをダッシュボードシステムに送信し、リアルタイムな可視化と分析を可能にします。

```javascript
// ダッシュボード連携の実装例（HTTPリクエストノード）
// 設定例
{
  "url": "https://dashboard-api.example.com/api/reports",
  "method": "POST",
  "authentication": "basicAuth",
  "username": "{{$node.GetDashboardConfig.json.api_username}}",
  "password": "{{$node.GetDashboardConfig.json.api_password}}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "report_type": "consensus_model",
    "target_id": "{{$node.GetReportData.json.target_id}}",
    "target_name": "{{$node.GetReportData.json.target_name}}",
    "generated_date": "{{$node.GetReportData.json.generated_date}}",
    "consensus_score": "{{$node.GetReportData.json.consensus_score}}",
    "perspective_scores": "{{$node.GetReportData.json.perspective_scores}}",
    "metrics_data": "{{$node.GetReportData.json.metrics_data}}",
    "chart_data": {
      "radar": "{{$node.GenerateRadarChart.json.chart_data}}",
      "bar_charts": "{{$node.GenerateBarCharts.json.chart_data_by_perspective}}",
      "heatmap": "{{$node.GenerateHeatmap.json.heatmap_data}}"
    }
  }
}
```

このようなダッシュボード連携の設定を実装することで、レポートデータをダッシュボードシステムに送信し、リアルタイムな可視化と分析を可能にすることができます。これにより、時系列での傾向分析や、複数の評価対象の比較など、より高度な分析が可能になります。

これらのレポート生成機能の実装により、コンセンサスモデルは分析結果や意思決定の根拠を明確かつ分かりやすく伝えることができます。目的や対象者に応じて最適化されたレポートテンプレート、効果的なデータ可視化、適切な配信方法を組み合わせることで、情報に基づいた判断を促進し、意思決定プロセスの透明性と説得力を高めることが可能になります。
