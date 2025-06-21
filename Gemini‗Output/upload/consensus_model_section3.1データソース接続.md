### 3.1 データソース接続

コンセンサスモデルの基盤となるのは、多様なデータソースからの情報収集です。データソース接続コンポーネントは、各視点（テクノロジー、マーケット、ビジネス）に関連する情報を効率的かつ信頼性高く取得するための重要な役割を担っています。n8nを活用することで、様々なデータソースに柔軟に接続し、統合的なデータ収集基盤を構築することができます。

**テクノロジー視点のデータソース接続**

テクノロジー視点では、技術トレンド、研究開発動向、特許情報、技術ブログなど、技術の進化や新興技術に関する情報を収集します。これらのデータソースは、企業の技術戦略や製品開発の方向性を決定する上で重要な指標となります。

n8nでのテクノロジー視点データソース接続の実装方法としては、主に以下のノードが活用されます：

**HTTP Requestノードによる技術トレンドAPIの活用**:
技術トレンド分析を提供する専門APIサービス（例：GitHub API、Stack Overflow API、特許データベースAPI）に接続し、最新の技術動向データを取得します。HTTP Requestノードの設定例は以下の通りです：

```javascript
// GitHub APIから特定の技術領域のリポジトリトレンドを取得する例
const techKeywords = ['artificial-intelligence', 'machine-learning', 'blockchain', 'quantum-computing'];
const apiRequests = techKeywords.map(keyword => ({
  method: 'GET',
  url: `https://api.github.com/search/repositories`,
  qs: {
    q: `${keyword} in:name,description,readme`,
    sort: 'stars',
    order: 'desc',
    per_page: 100
  },
  headers: {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'n8n-workflow'
  },
  json: true
}));

// 各キーワードごとにAPIリクエストを実行
const results = [];
for (const request of apiRequests) {
  try {
    const response = await $http.request(request);
    
    // レスポンスを処理
    if (response.statusCode === 200) {
      const keyword = request.qs.q.split(' ')[0];
      results.push({
        keyword: keyword,
        total_count: response.body.total_count,
        items: response.body.items.map(repo => ({
          id: repo.id,
          name: repo.name,
          full_name: repo.full_name,
          description: repo.description,
          stars: repo.stargazers_count,
          forks: repo.forks_count,
          created_at: repo.created_at,
          updated_at: repo.updated_at
        })),
        collected_at: new Date().toISOString()
      });
    } else {
      console.log(`API呼び出しエラー: ${response.statusCode} - ${JSON.stringify(response.body)}`);
    }
  } catch (error) {
    console.log(`リクエスト実行エラー: ${error.message}`);
  }
}

return results.map(result => ({ json: result }));
```

このようなHTTP Requestノードを使用することで、複数の技術キーワードに関するトレンドデータを一度に収集し、後続の分析プロセスに渡すことができます。また、APIレート制限や認証要件に対応するため、適切なヘッダー設定やリクエスト間隔の調整も重要です。

**RSS Feedノードによる技術ブログやニュースの収集**:
技術ブログやニュースサイトのRSSフィードを定期的に取得し、最新の技術動向や専門家の見解を収集します。RSS Feedノードの設定例は以下の通りです：

```javascript
// 技術ブログやニュースサイトのRSSフィードを取得する例
const techFeeds = [
  { url: 'https://www.technologyreview.com/feed/', source: 'MIT Technology Review' },
  { url: 'https://www.wired.com/feed/rss', source: 'Wired' },
  { url: 'https://feeds.feedburner.com/TechCrunch/', source: 'TechCrunch' },
  { url: 'https://www.theverge.com/rss/index.xml', source: 'The Verge' }
];

// 各フィードを取得して処理
const allItems = [];
for (const feed of techFeeds) {
  try {
    // RSSフィードを取得
    const response = await $http.request({
      method: 'GET',
      url: feed.url,
      headers: {
        'User-Agent': 'n8n-workflow'
      }
    });
    
    // XMLをパース
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(response.body, 'text/xml');
    
    // 記事アイテムを抽出
    const items = Array.from(xmlDoc.getElementsByTagName('item')).map(item => {
      const title = item.getElementsByTagName('title')[0]?.textContent || '';
      const link = item.getElementsByTagName('link')[0]?.textContent || '';
      const description = item.getElementsByTagName('description')[0]?.textContent || '';
      const pubDate = item.getElementsByTagName('pubDate')[0]?.textContent || '';
      
      return {
        title: title,
        link: link,
        description: description,
        publication_date: pubDate,
        source: feed.source,
        collected_at: new Date().toISOString()
      };
    });
    
    allItems.push(...items);
  } catch (error) {
    console.log(`フィード取得エラー (${feed.source}): ${error.message}`);
  }
}

// 日付でソート（最新順）
allItems.sort((a, b) => new Date(b.publication_date) - new Date(a.publication_date));

return allItems.map(item => ({ json: item }));
```

このようなRSS Feedノードを使用することで、複数の技術情報源から最新の記事やニュースを収集し、テキスト分析や技術トレンド抽出の入力として活用できます。また、収集したデータにはソース情報や取得日時などのメタデータを付与することで、後続の分析での信頼性評価に役立てることができます。

**マーケット視点のデータソース接続**

マーケット視点では、市場規模、成長率、競合情報、顧客ニーズ、価格動向など、市場環境や競争状況に関する情報を収集します。これらのデータは、事業機会の特定やマーケティング戦略の策定に不可欠です。

n8nでのマーケット視点データソース接続の実装方法としては、主に以下のノードが活用されます：

**HTTP Requestノードによる市場データAPIの活用**:
市場データを提供する専門APIサービス（例：金融データAPI、市場調査レポートAPI、ソーシャルメディア分析API）に接続し、最新の市場動向データを取得します。HTTP Requestノードの設定例は以下の通りです：

```javascript
// 市場データAPIから特定の業界の市場規模と成長率を取得する例
const industries = ['healthcare', 'fintech', 'e-commerce', 'renewable-energy'];
const apiRequests = industries.map(industry => ({
  method: 'GET',
  url: 'https://api.marketdata.example/v1/industry-metrics',
  qs: {
    industry: industry,
    metrics: 'market_size,growth_rate,competition_index',
    period: 'quarterly',
    from_date: '2024-01-01',
    to_date: '2025-06-01'
  },
  headers: {
    'Authorization': `Bearer ${$credentials.marketDataApiKey}`,
    'Content-Type': 'application/json'
  },
  json: true
}));

// 各業界ごとにAPIリクエストを実行
const results = [];
for (const request of apiRequests) {
  try {
    const response = await $http.request(request);
    
    // レスポンスを処理
    if (response.statusCode === 200) {
      const industry = request.qs.industry;
      results.push({
        industry: industry,
        metrics: response.body.data,
        metadata: {
          source: 'MarketData API',
          coverage: response.body.coverage,
          reliability_score: response.body.reliability_score,
          collected_at: new Date().toISOString()
        }
      });
    } else {
      console.log(`API呼び出しエラー: ${response.statusCode} - ${JSON.stringify(response.body)}`);
    }
  } catch (error) {
    console.log(`リクエスト実行エラー: ${error.message}`);
  }
}

return results.map(result => ({ json: result }));
```

このようなHTTP Requestノードを使用することで、複数の業界に関する市場データを体系的に収集し、後続の分析プロセスに渡すことができます。また、データの信頼性や網羅性に関するメタデータも収集することで、分析結果の信頼度評価に役立てることができます。

**Google Sheetsノードによる市場調査データの取得**:
社内で実施した市場調査結果や、外部調査会社から提供されたデータをGoogle Sheetsに格納し、それらを定期的に取得して分析に活用します。Google Sheetsノードの設定例は以下の通りです：

```javascript
// Google Sheetsから市場調査データを取得する例
// 注: 実際の実装ではGoogle Sheetsノードを使用

// シート情報の設定
const spreadsheetId = '1AbCdEfGhIjKlMnOpQrStUvWxYz';
const sheetName = 'MarketSurveyResults';
const range = 'A1:G100';

// データを取得
const response = await $http.request({
  method: 'GET',
  url: `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/${sheetName}!${range}`,
  headers: {
    'Authorization': `Bearer ${$credentials.googleSheetsToken}`
  },
  json: true
});

// レスポンスを処理
if (response.statusCode === 200 && response.body.values) {
  const headers = response.body.values[0];
  const rows = response.body.values.slice(1);
  
  // ヘッダーと行データからJSONオブジェクトを作成
  const surveyData = rows.map(row => {
    const item = {};
    headers.forEach((header, index) => {
      item[header] = row[index] || null;
    });
    return item;
  });
  
  // メタデータを追加
  const result = {
    survey_name: sheetName,
    data_count: surveyData.length,
    survey_data: surveyData,
    metadata: {
      source: 'Google Sheets',
      spreadsheet_id: spreadsheetId,
      last_updated: response.body.valueRanges?.[0]?.updatedDate || new Date().toISOString(),
      collected_at: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
} else {
  console.log(`シートデータ取得エラー: ${response.statusCode} - ${JSON.stringify(response.body)}`);
  return [{ json: { error: 'Failed to fetch sheet data' } }];
}
```

このようなGoogle Sheetsノードを使用することで、社内外の市場調査データを柔軟に取得し、分析プロセスに統合することができます。また、スプレッドシートの更新日時を確認することで、データの鮮度を評価することも可能です。

**ビジネス視点のデータソース接続**

ビジネス視点では、財務データ、事業KPI、組織情報、リソース配分など、企業の内部状況や事業パフォーマンスに関する情報を収集します。これらのデータは、事業戦略の評価や経営資源の最適配分を決定する上で重要な指標となります。

n8nでのビジネス視点データソース接続の実装方法としては、主に以下のノードが活用されます：

**HTTP Requestノードによる企業財務データAPIの活用**:
企業財務データを提供する専門APIサービス（例：財務報告API、株価データAPI、経済指標API）に接続し、最新の財務・経済データを取得します。HTTP Requestノードの設定例は以下の通りです：

```javascript
// 企業財務データAPIから四半期財務情報を取得する例
const companies = ['AAPL', 'MSFT', 'GOOGL', 'AMZN'];
const apiRequests = companies.map(ticker => ({
  method: 'GET',
  url: 'https://api.financialdata.example/v2/quarterly-financials',
  qs: {
    ticker: ticker,
    metrics: 'revenue,operating_income,net_income,cash_flow,debt_ratio',
    periods: 8  // 過去8四半期分
  },
  headers: {
    'Authorization': `ApiKey ${$credentials.financialDataApiKey}`,
    'Accept': 'application/json'
  },
  json: true
}));

// 各企業ごとにAPIリクエストを実行
const results = [];
for (const request of apiRequests) {
  try {
    const response = await $http.request(request);
    
    // レスポンスを処理
    if (response.statusCode === 200) {
      const ticker = request.qs.ticker;
      results.push({
        company_ticker: ticker,
        company_name: response.body.company_name,
        quarterly_data: response.body.quarterly_data,
        financial_ratios: response.body.financial_ratios,
        metadata: {
          source: 'Financial Data API',
          currency: response.body.currency,
          last_updated: response.body.last_updated,
          collected_at: new Date().toISOString()
        }
      });
    } else {
      console.log(`API呼び出しエラー: ${response.statusCode} - ${JSON.stringify(response.body)}`);
    }
  } catch (error) {
    console.log(`リクエスト実行エラー: ${error.message}`);
  }
}

return results.map(result => ({ json: result }));
```

このようなHTTP Requestノードを使用することで、複数の企業の財務データを体系的に収集し、財務分析や競合比較の基礎データとして活用できます。また、データの通貨単位や更新日時などのメタデータも収集することで、分析の正確性を高めることができます。

**Database（PostgreSQL/MySQL）ノードによる社内データの取得**:
社内の業務システムやデータウェアハウスに蓄積された事業KPIや組織データを取得し、内部視点からの分析に活用します。Databaseノードの設定例は以下の通りです：

```javascript
// 社内データベースから事業KPIデータを取得する例
// 注: 実際の実装ではDatabaseノードを使用

// クエリの設定
const query = `
  SELECT 
    d.department_name,
    p.project_name,
    p.project_status,
    k.kpi_name,
    k.target_value,
    k.actual_value,
    k.measurement_date,
    k.achievement_rate
  FROM 
    business_kpis k
  JOIN 
    projects p ON k.project_id = p.id
  JOIN 
    departments d ON p.department_id = d.id
  WHERE 
    k.measurement_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
  ORDER BY 
    d.department_name, p.project_name, k.measurement_date DESC
`;

// データベース接続とクエリ実行
try {
  // 注: 実際の実装ではDatabaseノードがこの処理を行う
  const connection = await mysql.createConnection({
    host: $credentials.database.host,
    user: $credentials.database.user,
    password: $credentials.database.password,
    database: $credentials.database.database
  });
  
  const [rows] = await connection.execute(query);
  await connection.end();
  
  // 部門ごとにデータを整理
  const departmentData = {};
  rows.forEach(row => {
    if (!departmentData[row.department_name]) {
      departmentData[row.department_name] = {
        department_name: row.department_name,
        projects: {}
      };
    }
    
    if (!departmentData[row.department_name].projects[row.project_name]) {
      departmentData[row.department_name].projects[row.project_name] = {
        project_name: row.project_name,
        project_status: row.project_status,
        kpis: []
      };
    }
    
    departmentData[row.department_name].projects[row.project_name].kpis.push({
      kpi_name: row.kpi_name,
      target_value: row.target_value,
      actual_value: row.actual_value,
      measurement_date: row.measurement_date,
      achievement_rate: row.achievement_rate
    });
  });
  
  // 結果を配列形式に変換
  const result = Object.values(departmentData).map(dept => {
    dept.projects = Object.values(dept.projects);
    return dept;
  });
  
  return result.map(dept => ({ json: dept }));
} catch (error) {
  console.log(`データベースクエリエラー: ${error.message}`);
  return [{ json: { error: 'Failed to fetch business KPI data' } }];
}
```

このようなDatabaseノードを使用することで、社内の業務データを体系的に取得し、ビジネス視点の分析基盤として活用できます。また、データベースのスキーマ設計や最適化されたクエリを活用することで、大量のデータでも効率的に処理することが可能です。

これらのデータソース接続の実装により、コンセンサスモデルは多角的な視点からの情報を継続的に収集し、統合的な分析の基盤を構築することができます。各データソースの特性や更新頻度に応じて適切な接続方法を選択し、データの鮮度と品質を確保することが重要です。また、データソースの認証情報やアクセス権限の管理も、セキュリティ上の重要な考慮事項となります。
