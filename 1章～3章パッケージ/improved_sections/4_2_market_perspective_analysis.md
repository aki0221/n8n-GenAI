### 4.2 マーケット視点の分析

マーケット視点の分析は、コンセンサスモデルにおいて市場環境や競争状況を理解するための重要なコンポーネントです。この分析では、市場規模、成長率、顧客ニーズ、競合情報などを体系的に分析し、事業機会やリスクを特定します。n8nを活用することで、マーケット視点の分析プロセスを効率的かつ再現性高く実装することができます。

**市場動向分析の実装方法**

市場動向分析は、市場の規模、成長率、セグメント構成などの定量的データと、トレンド、顧客行動、規制環境などの定性的情報を組み合わせて、市場の現状と将来の方向性を評価するプロセスです。この分析により、企業は成長機会の特定や、市場参入戦略の策定に役立つ洞察を得ることができます。

n8nでの市場動向分析の実装方法としては、主にFunctionノードとHTTP Requestノードが活用されます。以下に、具体的な実装例を示します：

**市場規模と成長率の分析**:
業界レポートや市場データベースから収集した情報を基に、市場規模と成長率を地域別、セグメント別に分析します。

```javascript
// 市場規模と成長率分析の実装例
function analyzeMarketSizeAndGrowth(items) {
  // 地域とセグメントでデータをグループ化
  const marketData = {};
  
  for (const item of items) {
    const region = item.json.region;
    const segment = item.json.segment;
    const year = item.json.year;
    
    if (!marketData[region]) {
      marketData[region] = {};
    }
    
    if (!marketData[region][segment]) {
      marketData[region][segment] = {};
    }
    
    marketData[region][segment][year] = {
      market_size: item.json.market_size,
      growth_rate: item.json.growth_rate,
      unit: item.json.unit || 'USD Million',
      source: item.json.source,
      confidence: item.json.confidence || 0.8
    };
  }
  
  // 分析結果を整形
  const results = [];
  
  for (const [region, regionData] of Object.entries(marketData)) {
    for (const [segment, yearData] of Object.entries(regionData)) {
      // 年次データを時系列順にソート
      const years = Object.keys(yearData).sort();
      
      // 時系列データの整形
      const timeSeriesData = years.map(year => ({
        year: parseInt(year),
        market_size: yearData[year].market_size,
        growth_rate: yearData[year].growth_rate,
        unit: yearData[year].unit,
        source: yearData[year].source,
        confidence: yearData[year].confidence
      }));
      
      // 成長予測（簡易的な線形回帰）
      const futureYears = 5;
      const forecastData = [];
      
      if (timeSeriesData.length >= 2) {
        // 最新の市場規模と成長率を取得
        const latestData = timeSeriesData[timeSeriesData.length - 1];
        const latestYear = latestData.year;
        const latestSize = latestData.market_size;
        const avgGrowthRate = timeSeriesData.reduce((sum, data) => sum + (data.growth_rate || 0), 0) / timeSeriesData.length;
        
        // 将来の市場規模を予測
        for (let i = 1; i <= futureYears; i++) {
          const forecastYear = latestYear + i;
          const forecastSize = latestSize * Math.pow(1 + avgGrowthRate, i);
          
          forecastData.push({
            year: forecastYear,
            market_size: forecastSize,
            growth_rate: avgGrowthRate,
            unit: latestData.unit,
            is_forecast: true,
            confidence: Math.max(0.3, latestData.confidence - (i * 0.1)) // 予測の信頼度は時間とともに低下
          });
        }
      }
      
      // CAGR（年平均成長率）の計算
      let cagr = null;
      if (timeSeriesData.length >= 2) {
        const firstYear = timeSeriesData[0];
        const lastYear = timeSeriesData[timeSeriesData.length - 1];
        const years = lastYear.year - firstYear.year;
        
        if (years > 0 && firstYear.market_size > 0) {
          cagr = Math.pow(lastYear.market_size / firstYear.market_size, 1 / years) - 1;
        }
      }
      
      // 市場シェアの計算（同じ年の全セグメントに対する割合）
      const marketShares = {};
      for (const data of timeSeriesData) {
        const year = data.year;
        
        if (!marketShares[year]) {
          // 同じ地域・同じ年の全セグメントの市場規模を合計
          let totalMarketSize = 0;
          for (const otherSegment of Object.keys(regionData)) {
            if (regionData[otherSegment][year]) {
              totalMarketSize += regionData[otherSegment][year].market_size;
            }
          }
          
          marketShares[year] = {
            total_market_size: totalMarketSize,
            shares: {}
          };
        }
        
        marketShares[year].shares[segment] = data.market_size / marketShares[year].total_market_size;
      }
      
      results.push({
        region: region,
        segment: segment,
        cagr: cagr,
        latest_market_size: timeSeriesData.length > 0 ? timeSeriesData[timeSeriesData.length - 1].market_size : null,
        latest_growth_rate: timeSeriesData.length > 0 ? timeSeriesData[timeSeriesData.length - 1].growth_rate : null,
        historical_data: timeSeriesData,
        forecast_data: forecastData,
        market_shares: Object.entries(marketShares).map(([year, data]) => ({
          year: parseInt(year),
          total_market_size: data.total_market_size,
          segment_share: data.shares[segment]
        })),
        analysis_date: new Date().toISOString()
      });
    }
  }
  
  return results.map(result => ({ json: result }));
}

// メイン処理
return analyzeMarketSizeAndGrowth($input.all());
```

このような市場規模と成長率分析ロジックを実装することで、地域別・セグメント別の市場動向を時系列で把握し、将来の市場規模予測や成長機会の特定に役立てることができます。また、CAGRや市場シェアなどの指標も算出することで、市場の魅力度や競争環境も分析できます。

**市場トレンド分析**:
ニュース記事、業界レポート、ソーシャルメディアなどから収集したテキストデータを分析し、市場トレンドやホットトピックを特定します。

```javascript
// 市場トレンド分析の実装例
function analyzeMarketTrends(items) {
  // トレンドキーワードの辞書（簡易版）
  const trendKeywords = [
    { term: 'digital transformation', aliases: ['dx', 'digitalization', 'digital shift'], category: 'Digital' },
    { term: 'sustainability', aliases: ['esg', 'green', 'eco-friendly', 'carbon neutral'], category: 'Sustainability' },
    { term: 'remote work', aliases: ['work from home', 'telework', 'hybrid work'], category: 'Work Style' },
    { term: 'subscription model', aliases: ['saas', 'recurring revenue', 'subscription economy'], category: 'Business Model' },
    { term: 'personalization', aliases: ['customization', 'tailored experience', 'one-to-one marketing'], category: 'Customer Experience' },
    { term: 'data privacy', aliases: ['gdpr', 'ccpa', 'privacy protection', 'data security'], category: 'Regulation' },
    { term: 'supply chain resilience', aliases: ['supply chain risk', 'nearshoring', 'reshoring'], category: 'Supply Chain' },
    { term: 'circular economy', aliases: ['recycling', 'upcycling', 'zero waste'], category: 'Sustainability' },
    { term: 'direct to consumer', aliases: ['d2c', 'dtc', 'direct sales'], category: 'Business Model' },
    { term: 'contactless', aliases: ['touchless', 'no-touch', 'self-service'], category: 'Customer Experience' }
  ];
  
  // 各アイテムからトレンドを抽出
  const trendMentions = {};
  const sourceTypes = new Set();
  const timeframes = new Set();
  
  for (const item of items) {
    // テキストフィールドを結合
    const text = [
      item.json.title || '',
      item.json.content || '',
      item.json.summary || ''
    ].join(' ').toLowerCase();
    
    // メタデータを記録
    const sourceType = item.json.source_type || 'unknown';
    const publicationDate = item.json.publication_date ? new Date(item.json.publication_date) : new Date();
    const timeframe = `${publicationDate.getFullYear()}-${(publicationDate.getMonth() + 1).toString().padStart(2, '0')}`;
    
    sourceTypes.add(sourceType);
    timeframes.add(timeframe);
    
    // キーワードの出現をカウント
    for (const keyword of trendKeywords) {
      // メインの用語をチェック
      const mainRegex = new RegExp(`\\b${keyword.term}\\b`, 'gi');
      const mainMatches = text.match(mainRegex);
      const mainCount = mainMatches ? mainMatches.length : 0;
      
      // 別名をチェック
      let aliasCount = 0;
      for (const alias of keyword.aliases) {
        const aliasRegex = new RegExp(`\\b${alias}\\b`, 'gi');
        const aliasMatches = text.match(aliasRegex);
        aliasCount += aliasMatches ? aliasMatches.length : 0;
      }
      
      // 合計カウントを記録
      const totalCount = mainCount + aliasCount;
      if (totalCount > 0) {
        const key = keyword.term;
        
        if (!trendMentions[key]) {
          trendMentions[key] = {
            term: keyword.term,
            category: keyword.category,
            aliases: keyword.aliases,
            total_mentions: 0,
            by_source: {},
            by_timeframe: {}
          };
        }
        
        trendMentions[key].total_mentions += totalCount;
        
        // ソースタイプ別のカウント
        if (!trendMentions[key].by_source[sourceType]) {
          trendMentions[key].by_source[sourceType] = 0;
        }
        trendMentions[key].by_source[sourceType] += totalCount;
        
        // 時間枠別のカウント
        if (!trendMentions[key].by_timeframe[timeframe]) {
          trendMentions[key].by_timeframe[timeframe] = 0;
        }
        trendMentions[key].by_timeframe[timeframe] += totalCount;
      }
    }
  }
  
  // ソースタイプと時間枠を配列に変換
  const sourceTypeArray = Array.from(sourceTypes);
  const timeframeArray = Array.from(timeframes).sort();
  
  // トレンドスコアの計算
  const trends = Object.values(trendMentions).map(trend => {
    // 時間的な成長率を計算
    const timeframeCounts = [];
    for (const timeframe of timeframeArray) {
      timeframeCounts.push(trend.by_timeframe[timeframe] || 0);
    }
    
    let growthRate = 0;
    if (timeframeCounts.length >= 2) {
      const oldestCount = timeframeCounts[0];
      const newestCount = timeframeCounts[timeframeCounts.length - 1];
      
      if (oldestCount > 0) {
        growthRate = (newestCount - oldestCount) / oldestCount;
      } else if (newestCount > 0) {
        growthRate = 1; // 新しく出現したトレンド
      }
    }
    
    // ソースの多様性を計算
    const sourceDiversity = Object.keys(trend.by_source).length / sourceTypeArray.length;
    
    // トレンドスコアの計算（言及数、成長率、ソース多様性を考慮）
    const mentionScore = Math.min(1, trend.total_mentions / 100); // 言及数のスコア（最大1）
    const growthScore = Math.max(0, Math.min(1, growthRate)); // 成長率のスコア（0～1）
    const diversityScore = sourceDiversity; // 多様性スコア（0～1）
    
    const trendScore = (mentionScore * 0.4) + (growthScore * 0.4) + (diversityScore * 0.2);
    
    // 時系列データの整形
    const timeSeriesData = timeframeArray.map(timeframe => ({
      timeframe,
      mentions: trend.by_timeframe[timeframe] || 0
    }));
    
    return {
      term: trend.term,
      category: trend.category,
      aliases: trend.aliases,
      trend_score: trendScore,
      total_mentions: trend.total_mentions,
      growth_rate: growthRate,
      source_diversity: sourceDiversity,
      by_source: trend.by_source,
      time_series: timeSeriesData
    };
  });
  
  // トレンドスコアでソート（降順）
  trends.sort((a, b) => b.trend_score - a.trend_score);
  
  // カテゴリ別のトレンド集計
  const categoryTrends = {};
  for (const trend of trends) {
    if (!categoryTrends[trend.category]) {
      categoryTrends[trend.category] = {
        category: trend.category,
        total_mentions: 0,
        trend_terms: [],
        avg_trend_score: 0
      };
    }
    
    categoryTrends[trend.category].total_mentions += trend.total_mentions;
    categoryTrends[trend.category].trend_terms.push(trend.term);
  }
  
  // カテゴリごとの平均トレンドスコアを計算
  for (const category of Object.keys(categoryTrends)) {
    const categoryTrends = trends.filter(t => t.category === category);
    if (categoryTrends.length > 0) {
      categoryTrends[category].avg_trend_score = categoryTrends.reduce((sum, t) => sum + t.trend_score, 0) / categoryTrends.length;
    }
  }
  
  // 結果を整形
  const result = {
    trends: trends,
    categories: Object.values(categoryTrends).sort((a, b) => b.total_mentions - a.total_mentions),
    metadata: {
      source_types: sourceTypeArray,
      timeframes: timeframeArray,
      total_documents: items.length,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeMarketTrends($input.all());
```

このようなトレンド分析ロジックを実装することで、大量のテキストデータから市場トレンドを自動的に抽出し、その重要度や成長性を評価することができます。また、カテゴリ別の分析や時系列分析により、トレンドの全体像や変化の方向性も把握できます。

**競合分析の実装方法**

競合分析は、主要な競合企業の戦略、製品・サービス、市場ポジション、強み・弱みなどを体系的に分析し、競争環境を理解するプロセスです。この分析により、企業は競争優位性の構築や、差別化戦略の策定に役立つ洞察を得ることができます。

n8nでの競合分析の実装方法としては、主にFunctionノードとHTTP Requestノードが活用されます。以下に、具体的な実装例を示します：

**競合ポジショニング分析**:
競合企業の製品・サービス、価格、品質、機能などの属性を評価し、市場内での相対的なポジションを分析します。

```javascript
// 競合ポジショニング分析の実装例
function analyzeCompetitorPositioning(items) {
  // 評価軸の定義
  const evaluationAxes = [
    { id: 'price', name: '価格', description: '製品・サービスの価格水準', high_is_good: false },
    { id: 'quality', name: '品質', description: '製品・サービスの品質水準', high_is_good: true },
    { id: 'features', name: '機能性', description: '機能の豊富さと先進性', high_is_good: true },
    { id: 'ux', name: 'ユーザー体験', description: '使いやすさと顧客満足度', high_is_good: true },
    { id: 'market_share', name: '市場シェア', description: '対象市場での占有率', high_is_good: true },
    { id: 'brand', name: 'ブランド力', description: '認知度と評判', high_is_good: true },
    { id: 'innovation', name: '革新性', description: '新技術・新サービスの導入速度', high_is_good: true },
    { id: 'ecosystem', name: 'エコシステム', description: '補完製品・サービスの充実度', high_is_good: true }
  ];
  
  // 競合企業データの整理
  const competitors = {};
  
  for (const item of items) {
    const competitor = item.json;
    const companyId = competitor.company_id;
    
    if (!competitors[companyId]) {
      competitors[companyId] = {
        company_id: companyId,
        company_name: competitor.company_name,
        company_type: competitor.company_type || 'competitor',
        evaluations: {},
        strengths: competitor.strengths || [],
        weaknesses: competitor.weaknesses || [],
        recent_moves: competitor.recent_moves || [],
        products: competitor.products || []
      };
    }
    
    // 評価データを記録
    if (competitor.evaluation_axis && competitor.evaluation_score !== undefined) {
      competitors[companyId].evaluations[competitor.evaluation_axis] = {
        score: competitor.evaluation_score,
        notes: competitor.evaluation_notes || '',
        data_source: competitor.data_source || 'manual',
        confidence: competitor.confidence || 0.7
      };
    }
  }
  
  // 各評価軸の統計情報を計算
  const axisStats = {};
  for (const axis of evaluationAxes) {
    const scores = Object.values(competitors)
      .filter(c => c.evaluations[axis.id])
      .map(c => c.evaluations[axis.id].score);
    
    if (scores.length > 0) {
      const min = Math.min(...scores);
      const max = Math.max(...scores);
      const avg = scores.reduce((sum, score) => sum + score, 0) / scores.length;
      
      axisStats[axis.id] = { min, max, avg };
    }
  }
  
  // 競合企業の総合評価とポジショニングを計算
  const competitorAnalysis = Object.values(competitors).map(competitor => {
    // 各評価軸のスコアを正規化（0～1）
    const normalizedScores = {};
    let totalScore = 0;
    let scoreCount = 0;
    
    for (const axis of evaluationAxes) {
      if (competitor.evaluations[axis.id] && axisStats[axis.id]) {
        const rawScore = competitor.evaluations[axis.id].score;
        const { min, max } = axisStats[axis.id];
        
        // スコアの正規化
        let normalizedScore = 0;
        if (max > min) {
          normalizedScore = (rawScore - min) / (max - min);
        }
        
        // 「高いほど良い」が false の場合は反転
        if (!axis.high_is_good) {
          normalizedScore = 1 - normalizedScore;
        }
        
        normalizedScores[axis.id] = {
          raw_score: rawScore,
          normalized_score: normalizedScore,
          confidence: competitor.evaluations[axis.id].confidence
        };
        
        totalScore += normalizedScore;
        scoreCount++;
      }
    }
    
    // 総合スコアの計算
    const overallScore = scoreCount > 0 ? totalScore / scoreCount : null;
    
    // 主要な2軸でのポジショニング（例：価格と品質）
    const positioning = {};
    const primaryAxes = ['price', 'quality']; // 主要な2軸
    
    for (const axisId of primaryAxes) {
      if (normalizedScores[axisId]) {
        positioning[axisId] = normalizedScores[axisId].normalized_score;
      }
    }
    
    // 競合企業の相対的な強みと弱みを特定
    const relativeStrengths = [];
    const relativeWeaknesses = [];
    
    for (const axis of evaluationAxes) {
      if (normalizedScores[axis.id]) {
        const score = normalizedScores[axis.id].normalized_score;
        const avgScore = Object.values(competitors)
          .filter(c => c.company_id !== competitor.company_id && c.evaluations[axis.id])
          .map(c => {
            const rawScore = c.evaluations[axis.id].score;
            const { min, max } = axisStats[axis.id];
            let norm = 0;
            if (max > min) {
              norm = (rawScore - min) / (max - min);
            }
            return axis.high_is_good ? norm : 1 - norm;
          })
          .reduce((sum, s) => sum + s, 0) / 
          Object.values(competitors).filter(c => c.company_id !== competitor.company_id && c.evaluations[axis.id]).length || 0;
        
        const difference = score - avgScore;
        
        if (difference > 0.2) {
          relativeStrengths.push({
            axis: axis.id,
            axis_name: axis.name,
            score: score,
            avg_score: avgScore,
            difference: difference
          });
        } else if (difference < -0.2) {
          relativeWeaknesses.push({
            axis: axis.id,
            axis_name: axis.name,
            score: score,
            avg_score: avgScore,
            difference: difference
          });
        }
      }
    }
    
    return {
      company_id: competitor.company_id,
      company_name: competitor.company_name,
      company_type: competitor.company_type,
      overall_score: overallScore,
      positioning: positioning,
      normalized_scores: normalizedScores,
      relative_strengths: relativeStrengths.sort((a, b) => b.difference - a.difference),
      relative_weaknesses: relativeWeaknesses.sort((a, b) => a.difference - b.difference),
      strengths: competitor.strengths,
      weaknesses: competitor.weaknesses,
      recent_moves: competitor.recent_moves,
      products: competitor.products
    };
  });
  
  // 総合スコアでソート（降順）
  competitorAnalysis.sort((a, b) => {
    if (a.overall_score === null) return 1;
    if (b.overall_score === null) return -1;
    return b.overall_score - a.overall_score;
  });
  
  // 結果を整形
  const result = {
    competitors: competitorAnalysis,
    evaluation_axes: evaluationAxes,
    axis_stats: axisStats,
    metadata: {
      competitor_count: competitorAnalysis.length,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeCompetitorPositioning($input.all());
```

このような競合ポジショニング分析ロジックを実装することで、各競合企業の市場内での相対的なポジションを多次元的に評価し、競争環境の全体像を把握することができます。また、各企業の相対的な強みと弱みを特定することで、差別化戦略の策定にも役立てることができます。

**競合製品比較分析**:
競合企業の製品・サービスの特徴、価格、性能などを詳細に比較し、競争優位性や差別化ポイントを特定します。

```javascript
// 競合製品比較分析の実装例
function analyzeCompetitorProducts(items) {
  // 製品カテゴリと特徴の定義
  const productCategories = [
    { id: 'entry', name: 'エントリーモデル', description: '初心者向け・低価格帯製品' },
    { id: 'mid', name: 'ミッドレンジモデル', description: '一般ユーザー向け・中価格帯製品' },
    { id: 'high', name: 'ハイエンドモデル', description: '上級ユーザー向け・高価格帯製品' },
    { id: 'business', name: 'ビジネスモデル', description: '法人向け製品・サービス' },
    { id: 'specialized', name: '特化型モデル', description: '特定用途に特化した製品' }
  ];
  
  const featureGroups = [
    { id: 'core', name: '基本機能', weight: 0.3 },
    { id: 'performance', name: '性能', weight: 0.25 },
    { id: 'usability', name: '使いやすさ', weight: 0.2 },
    { id: 'ecosystem', name: 'エコシステム', weight: 0.15 },
    { id: 'support', name: 'サポート', weight: 0.1 }
  ];
  
  // 製品データの整理
  const products = {};
  const companies = new Set();
  const features = new Set();
  
  for (const item of items) {
    const product = item.json;
    const productId = product.product_id;
    
    if (!products[productId]) {
      products[productId] = {
        product_id: productId,
        product_name: product.product_name,
        company_id: product.company_id,
        company_name: product.company_name,
        category: product.category,
        price: product.price,
        currency: product.currency || 'JPY',
        release_date: product.release_date,
        features: {},
        unique_selling_points: product.unique_selling_points || [],
        target_segments: product.target_segments || [],
        market_share: product.market_share
      };
      
      companies.add(product.company_id);
    }
    
    // 特徴データを記録
    if (product.feature_id && product.feature_score !== undefined) {
      products[productId].features[product.feature_id] = {
        score: product.feature_score,
        group: product.feature_group,
        notes: product.feature_notes || '',
        data_source: product.data_source || 'manual',
        confidence: product.confidence || 0.7
      };
      
      features.add(product.feature_id);
    }
  }
  
  // 特徴グループごとの製品スコアを計算
  const productAnalysis = Object.values(products).map(product => {
    // 特徴グループごとのスコアを集計
    const groupScores = {};
    let totalWeightedScore = 0;
    
    for (const group of featureGroups) {
      const groupFeatures = Object.entries(product.features)
        .filter(([, feature]) => feature.group === group.id);
      
      if (groupFeatures.length > 0) {
        const avgScore = groupFeatures.reduce((sum, [, feature]) => sum + feature.score, 0) / groupFeatures.length;
        groupScores[group.id] = {
          group_name: group.name,
          score: avgScore,
          feature_count: groupFeatures.length
        };
        
        totalWeightedScore += avgScore * group.weight;
      }
    }
    
    // 価格パフォーマンス比の計算
    const overallScore = totalWeightedScore;
    const pricePerformanceRatio = product.price > 0 ? overallScore / product.price * 1000 : null;
    
    // 製品の相対的な強みと弱みを特定
    const strengths = [];
    const weaknesses = [];
    
    for (const [featureId, feature] of Object.entries(product.features)) {
      // 同カテゴリの他製品の平均スコアを計算
      const otherProducts = Object.values(products).filter(p => 
        p.product_id !== product.product_id && 
        p.category === product.category &&
        p.features[featureId]
      );
      
      if (otherProducts.length > 0) {
        const avgScore = otherProducts.reduce((sum, p) => sum + p.features[featureId].score, 0) / otherProducts.length;
        const difference = feature.score - avgScore;
        
        if (difference > 1.5) {
          strengths.push({
            feature_id: featureId,
            score: feature.score,
            avg_score: avgScore,
            difference: difference
          });
        } else if (difference < -1.5) {
          weaknesses.push({
            feature_id: featureId,
            score: feature.score,
            avg_score: avgScore,
            difference: difference
          });
        }
      }
    }
    
    return {
      product_id: product.product_id,
      product_name: product.product_name,
      company_id: product.company_id,
      company_name: product.company_name,
      category: product.category,
      price: product.price,
      currency: product.currency,
      release_date: product.release_date,
      overall_score: overallScore,
      price_performance_ratio: pricePerformanceRatio,
      group_scores: groupScores,
      relative_strengths: strengths.sort((a, b) => b.difference - a.difference),
      relative_weaknesses: weaknesses.sort((a, b) => a.difference - b.difference),
      unique_selling_points: product.unique_selling_points,
      target_segments: product.target_segments,
      market_share: product.market_share
    };
  });
  
  // カテゴリごとに製品をグループ化
  const categorizedProducts = {};
  for (const product of productAnalysis) {
    if (!categorizedProducts[product.category]) {
      categorizedProducts[product.category] = [];
    }
    
    categorizedProducts[product.category].push(product);
  }
  
  // カテゴリごとに製品をスコアでソート
  for (const category of Object.keys(categorizedProducts)) {
    categorizedProducts[category].sort((a, b) => b.overall_score - a.overall_score);
  }
  
  // 企業ごとの製品ポートフォリオを分析
  const companyPortfolios = {};
  for (const companyId of companies) {
    const companyProducts = productAnalysis.filter(p => p.company_id === companyId);
    
    if (companyProducts.length > 0) {
      const categoryCount = new Set(companyProducts.map(p => p.category)).size;
      const avgScore = companyProducts.reduce((sum, p) => sum + p.overall_score, 0) / companyProducts.length;
      const priceRange = {
        min: Math.min(...companyProducts.map(p => p.price)),
        max: Math.max(...companyProducts.map(p => p.price)),
        avg: companyProducts.reduce((sum, p) => sum + p.price, 0) / companyProducts.length
      };
      
      companyPortfolios[companyId] = {
        company_id: companyId,
        company_name: companyProducts[0].company_name,
        product_count: companyProducts.length,
        category_coverage: categoryCount / productCategories.length,
        avg_product_score: avgScore,
        price_range: priceRange,
        products: companyProducts.map(p => ({
          product_id: p.product_id,
          product_name: p.product_name,
          category: p.category,
          overall_score: p.overall_score,
          price: p.price
        }))
      };
    }
  }
  
  // 結果を整形
  const result = {
    products: productAnalysis,
    categorized_products: categorizedProducts,
    company_portfolios: Object.values(companyPortfolios),
    product_categories: productCategories,
    feature_groups: featureGroups,
    metadata: {
      product_count: productAnalysis.length,
      company_count: companies.size,
      feature_count: features.size,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeCompetitorProducts($input.all());
```

このような競合製品比較分析ロジックを実装することで、各製品の特徴や性能を多角的に評価し、製品間の相対的な強みと弱みを特定することができます。また、企業ごとの製品ポートフォリオ分析により、各企業の市場戦略や製品展開の特徴も把握できます。

**顧客ニーズ分析の実装方法**

顧客ニーズ分析は、顧客の要求、期待、行動パターンなどを体系的に分析し、市場機会や製品・サービス改善のポイントを特定するプロセスです。この分析により、企業は顧客中心の戦略策定や、製品開発の優先順位付けに役立つ洞察を得ることができます。

n8nでの顧客ニーズ分析の実装方法としては、主にFunctionノードとHTTP Requestノードが活用されます。以下に、具体的な実装例を示します：

**顧客セグメント分析**:
顧客データを基に、類似した特性や行動パターンを持つグループ（セグメント）を特定し、各セグメントの特徴や規模を分析します。

```javascript
// 顧客セグメント分析の実装例
function analyzeCustomerSegments(items) {
  // セグメンテーション基準の定義
  const segmentationCriteria = [
    { id: 'demographics', name: '人口統計学的特性', fields: ['age_group', 'gender', 'income_level', 'education'] },
    { id: 'behavior', name: '行動特性', fields: ['purchase_frequency', 'avg_order_value', 'preferred_channel', 'loyalty_level'] },
    { id: 'psychographics', name: '心理的特性', fields: ['lifestyle', 'values', 'interests', 'attitudes'] },
    { id: 'needs', name: 'ニーズ', fields: ['primary_need', 'secondary_need', 'pain_points', 'goals'] }
  ];
  
  // 顧客データの整理
  const customers = items.map(item => item.json);
  
  // 行動特性に基づくセグメンテーション（簡易的なクラスタリング）
  const behaviorSegments = segmentCustomersByBehavior(customers);
  
  // ニーズに基づくセグメンテーション
  const needsSegments = segmentCustomersByNeeds(customers);
  
  // 人口統計学的特性の分布を分析
  const demographicsDistribution = analyzeDemographicsDistribution(customers);
  
  // セグメント間の相関関係を分析
  const segmentCorrelations = analyzeSegmentCorrelations(behaviorSegments, needsSegments);
  
  // 結果を整形
  const result = {
    behavior_segments: behaviorSegments,
    needs_segments: needsSegments,
    demographics_distribution: demographicsDistribution,
    segment_correlations: segmentCorrelations,
    metadata: {
      customer_count: customers.length,
      segmentation_criteria: segmentationCriteria,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// 行動特性に基づくセグメンテーション
function segmentCustomersByBehavior(customers) {
  // 行動特性の指標
  const behaviorMetrics = [
    'purchase_frequency',
    'avg_order_value',
    'product_category_diversity',
    'loyalty_level'
  ];
  
  // 各指標の最小値と最大値を計算（正規化用）
  const metricRanges = {};
  for (const metric of behaviorMetrics) {
    const values = customers
      .filter(c => c[metric] !== undefined && c[metric] !== null)
      .map(c => c[metric]);
    
    if (values.length > 0) {
      metricRanges[metric] = {
        min: Math.min(...values),
        max: Math.max(...values)
      };
    }
  }
  
  // 顧客の行動特性を正規化
  const normalizedCustomers = customers.map(customer => {
    const normalized = {
      customer_id: customer.customer_id,
      normalized_metrics: {}
    };
    
    for (const metric of behaviorMetrics) {
      if (customer[metric] !== undefined && customer[metric] !== null && metricRanges[metric]) {
        const { min, max } = metricRanges[metric];
        normalized.normalized_metrics[metric] = max > min 
          ? (customer[metric] - min) / (max - min)
          : 0.5;
      }
    }
    
    return normalized;
  });
  
  // 簡易的なクラスタリング（K-means の簡易実装）
  const k = 4; // クラスタ数
  const clusters = simplifiedKMeans(normalizedCustomers, behaviorMetrics, k);
  
  // 各クラスタの特徴を分析
  const segments = [];
  for (let i = 0; i < clusters.length; i++) {
    const cluster = clusters[i];
    const clusterCustomers = cluster.customers.map(c => 
      customers.find(customer => customer.customer_id === c.customer_id)
    );
    
    // クラスタの中心的な特徴を計算
    const centerFeatures = {};
    for (const metric of behaviorMetrics) {
      const values = clusterCustomers
        .filter(c => c[metric] !== undefined && c[metric] !== null)
        .map(c => c[metric]);
      
      if (values.length > 0) {
        centerFeatures[metric] = values.reduce((sum, v) => sum + v, 0) / values.length;
      }
    }
    
    // セグメント名の生成（特徴に基づく）
    let segmentName = 'セグメント ' + (i + 1);
    if (centerFeatures.purchase_frequency > 0.7 && centerFeatures.loyalty_level > 0.7) {
      segmentName = '高頻度・高ロイヤルティ顧客';
    } else if (centerFeatures.purchase_frequency < 0.3 && centerFeatures.avg_order_value > 0.7) {
      segmentName = '低頻度・高単価顧客';
    } else if (centerFeatures.purchase_frequency > 0.7 && centerFeatures.avg_order_value < 0.3) {
      segmentName = '高頻度・低単価顧客';
    } else if (centerFeatures.purchase_frequency < 0.3 && centerFeatures.loyalty_level < 0.3) {
      segmentName = '低関与顧客';
    }
    
    segments.push({
      segment_id: 'behavior_' + (i + 1),
      segment_name: segmentName,
      customer_count: cluster.customers.length,
      percentage: cluster.customers.length / customers.length,
      center_features: centerFeatures,
      key_characteristics: identifyKeyCharacteristics(clusterCustomers, behaviorMetrics),
      customer_sample: cluster.customers.slice(0, 5).map(c => c.customer_id)
    });
  }
  
  return segments;
}

// ニーズに基づくセグメンテーション
function segmentCustomersByNeeds(customers) {
  // 主要ニーズの抽出
  const primaryNeeds = {};
  for (const customer of customers) {
    if (customer.primary_need) {
      if (!primaryNeeds[customer.primary_need]) {
        primaryNeeds[customer.primary_need] = {
          need: customer.primary_need,
          count: 0,
          customers: []
        };
      }
      
      primaryNeeds[customer.primary_need].count++;
      primaryNeeds[customer.primary_need].customers.push(customer.customer_id);
    }
  }
  
  // ニーズセグメントの整形
  const segments = Object.values(primaryNeeds)
    .filter(need => need.count >= 5) // 最低5人以上のセグメントのみ
    .map(need => {
      const needCustomers = customers.filter(c => c.primary_need === need.need);
      
      // セグメントの特徴を分析
      const painPoints = {};
      const goals = {};
      
      for (const customer of needCustomers) {
        if (customer.pain_points && Array.isArray(customer.pain_points)) {
          for (const pain of customer.pain_points) {
            painPoints[pain] = (painPoints[pain] || 0) + 1;
          }
        }
        
        if (customer.goals && Array.isArray(customer.goals)) {
          for (const goal of customer.goals) {
            goals[goal] = (goals[goal] || 0) + 1;
          }
        }
      }
      
      // 上位の課題と目標を抽出
      const topPainPoints = Object.entries(painPoints)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([pain, count]) => ({
          pain_point: pain,
          count: count,
          percentage: count / needCustomers.length
        }));
      
      const topGoals = Object.entries(goals)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([goal, count]) => ({
          goal: goal,
          count: count,
          percentage: count / needCustomers.length
        }));
      
      return {
        segment_id: 'need_' + need.need.toLowerCase().replace(/\s+/g, '_'),
        segment_name: need.need + ' 重視顧客',
        customer_count: need.count,
        percentage: need.count / customers.length,
        primary_need: need.need,
        top_pain_points: topPainPoints,
        top_goals: topGoals,
        customer_sample: need.customers.slice(0, 5)
      };
    })
    .sort((a, b) => b.customer_count - a.customer_count);
  
  return segments;
}

// 人口統計学的特性の分布を分析
function analyzeDemographicsDistribution(customers) {
  const demographicFields = ['age_group', 'gender', 'income_level', 'education', 'location'];
  const distribution = {};
  
  for (const field of demographicFields) {
    const fieldValues = {};
    
    for (const customer of customers) {
      if (customer[field]) {
        fieldValues[customer[field]] = (fieldValues[customer[field]] || 0) + 1;
      }
    }
    
    distribution[field] = Object.entries(fieldValues)
      .map(([value, count]) => ({
        value: value,
        count: count,
        percentage: count / customers.length
      }))
      .sort((a, b) => b.count - a.count);
  }
  
  return distribution;
}

// セグメント間の相関関係を分析
function analyzeSegmentCorrelations(behaviorSegments, needsSegments) {
  // 実際の実装では、顧客IDを基にセグメント間の重複を分析
  // 簡易的な実装として、ランダムな相関係数を生成
  const correlations = [];
  
  for (const behaviorSegment of behaviorSegments) {
    for (const needsSegment of needsSegments) {
      correlations.push({
        segment_1: {
          id: behaviorSegment.segment_id,
          name: behaviorSegment.segment_name,
          type: 'behavior'
        },
        segment_2: {
          id: needsSegment.segment_id,
          name: needsSegment.segment_name,
          type: 'needs'
        },
        correlation_coefficient: Math.random(), // 実際には顧客の重複から計算
        significance: Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low'
      });
    }
  }
  
  // 相関係数でソート（降順）
  correlations.sort((a, b) => b.correlation_coefficient - a.correlation_coefficient);
  
  return correlations;
}

// 簡易的なK-meansクラスタリング
function simplifiedKMeans(normalizedCustomers, metrics, k) {
  // 初期クラスタ中心をランダムに選択
  const centers = [];
  const customersCopy = [...normalizedCustomers];
  
  for (let i = 0; i < k; i++) {
    if (customersCopy.length > 0) {
      const randomIndex = Math.floor(Math.random() * customersCopy.length);
      centers.push({
        metrics: { ...customersCopy[randomIndex].normalized_metrics }
      });
      customersCopy.splice(randomIndex, 1);
    }
  }
  
  // 最大イテレーション数
  const maxIterations = 10;
  let iterations = 0;
  let changed = true;
  
  // クラスタ割り当て
  const clusters = Array(k).fill().map(() => ({ center: null, customers: [] }));
  
  while (changed && iterations < maxIterations) {
    changed = false;
    iterations++;
    
    // クラスタをリセット
    for (let i = 0; i < k; i++) {
      clusters[i].center = centers[i];
      clusters[i].customers = [];
    }
    
    // 各顧客を最も近いクラスタに割り当て
    for (const customer of normalizedCustomers) {
      let minDistance = Infinity;
      let closestCluster = 0;
      
      for (let i = 0; i < k; i++) {
        const distance = calculateDistance(customer.normalized_metrics, centers[i].metrics, metrics);
        
        if (distance < minDistance) {
          minDistance = distance;
          closestCluster = i;
        }
      }
      
      clusters[closestCluster].customers.push(customer);
    }
    
    // クラスタ中心を更新
    for (let i = 0; i < k; i++) {
      if (clusters[i].customers.length > 0) {
        const newCenter = { metrics: {} };
        
        for (const metric of metrics) {
          const values = clusters[i].customers
            .filter(c => c.normalized_metrics[metric] !== undefined)
            .map(c => c.normalized_metrics[metric]);
          
          if (values.length > 0) {
            newCenter.metrics[metric] = values.reduce((sum, v) => sum + v, 0) / values.length;
          }
        }
        
        // 中心が変化したかチェック
        const centerChanged = !isEqualCenter(centers[i].metrics, newCenter.metrics, metrics);
        if (centerChanged) {
          centers[i] = newCenter;
          changed = true;
        }
      }
    }
  }
  
  return clusters;
}

// 2点間の距離を計算（ユークリッド距離）
function calculateDistance(point1, point2, metrics) {
  let sumSquared = 0;
  let validMetrics = 0;
  
  for (const metric of metrics) {
    if (point1[metric] !== undefined && point2[metric] !== undefined) {
      sumSquared += Math.pow(point1[metric] - point2[metric], 2);
      validMetrics++;
    }
  }
  
  return validMetrics > 0 ? Math.sqrt(sumSquared / validMetrics) : Infinity;
}

// 2つのクラスタ中心が等しいかチェック
function isEqualCenter(center1, center2, metrics) {
  const threshold = 0.01; // 許容誤差
  
  for (const metric of metrics) {
    if (center1[metric] !== undefined && center2[metric] !== undefined) {
      if (Math.abs(center1[metric] - center2[metric]) > threshold) {
        return false;
      }
    }
  }
  
  return true;
}

// セグメントの主要特性を特定
function identifyKeyCharacteristics(customers, metrics) {
  const characteristics = [];
  
  // 各指標の分布を分析
  for (const metric of metrics) {
    const values = customers
      .filter(c => c[metric] !== undefined && c[metric] !== null)
      .map(c => c[metric]);
    
    if (values.length > 0) {
      const avg = values.reduce((sum, v) => sum + v, 0) / values.length;
      
      // 特徴的な値かどうかを判定
      let characteristic = null;
      if (avg > 0.7) {
        characteristic = `高い${metric}`;
      } else if (avg < 0.3) {
        characteristic = `低い${metric}`;
      }
      
      if (characteristic) {
        characteristics.push({
          metric: metric,
          value: avg,
          description: characteristic
        });
      }
    }
  }
  
  return characteristics.sort((a, b) => Math.abs(b.value - 0.5) - Math.abs(a.value - 0.5));
}

// メイン処理
return analyzeCustomerSegments($input.all());
```

このような顧客セグメント分析ロジックを実装することで、顧客を行動特性やニーズに基づいて意味のあるグループに分類し、各セグメントの特徴や規模を把握することができます。また、セグメント間の相関関係や人口統計学的特性の分布も分析することで、より包括的な顧客理解が可能になります。

**顧客満足度・不満点分析**:
顧客フィードバック、レビュー、問い合わせデータなどを分析し、顧客満足度の要因や不満点を特定します。

```javascript
// 顧客満足度・不満点分析の実装例
function analyzeCustomerFeedback(items) {
  // 感情分析のための単語辞書（簡易版）
  const sentimentDictionary = {
    positive: ['good', 'great', 'excellent', 'love', 'best', 'amazing', 'helpful', 'satisfied', 'easy', 'recommend'],
    negative: ['bad', 'poor', 'terrible', 'worst', 'difficult', 'disappointed', 'frustrating', 'confusing', 'expensive', 'slow']
  };
  
  // トピック分類のためのキーワード辞書
  const topicKeywords = {
    'product_quality': ['quality', 'durable', 'reliable', 'broke', 'defect', 'material'],
    'usability': ['easy', 'intuitive', 'user-friendly', 'difficult', 'confusing', 'complicated'],
    'performance': ['fast', 'slow', 'responsive', 'speed', 'efficient', 'lag'],
    'features': ['feature', 'functionality', 'capability', 'option', 'missing', 'lacks'],
    'price': ['price', 'expensive', 'cheap', 'cost', 'worth', 'value'],
    'customer_service': ['service', 'support', 'staff', 'representative', 'response', 'helpful'],
    'delivery': ['delivery', 'shipping', 'arrived', 'package', 'late', 'damaged']
  };
  
  // フィードバックデータの整理
  const feedbacks = items.map(item => ({
    id: item.json.feedback_id,
    customer_id: item.json.customer_id,
    product_id: item.json.product_id,
    rating: item.json.rating,
    text: item.json.feedback_text,
    date: new Date(item.json.feedback_date),
    source: item.json.source || 'review'
  }));
  
  // 各フィードバックの感情分析とトピック分類
  const analyzedFeedbacks = feedbacks.map(feedback => {
    // テキストの前処理
    const text = feedback.text.toLowerCase();
    const words = text.split(/\W+/).filter(word => word.length > 0);
    
    // 感情分析
    let positiveCount = 0;
    let negativeCount = 0;
    
    for (const word of words) {
      if (sentimentDictionary.positive.includes(word)) {
        positiveCount++;
      } else if (sentimentDictionary.negative.includes(word)) {
        negativeCount++;
      }
    }
    
    const sentimentScore = words.length > 0 
      ? (positiveCount - negativeCount) / words.length 
      : 0;
    
    const sentiment = sentimentScore > 0.05 ? 'positive' : 
                     sentimentScore < -0.05 ? 'negative' : 'neutral';
    
    // トピック分類
    const topicScores = {};
    for (const [topic, keywords] of Object.entries(topicKeywords)) {
      let matchCount = 0;
      for (const keyword of keywords) {
        if (text.includes(keyword)) {
          matchCount++;
        }
      }
      
      topicScores[topic] = matchCount / keywords.length;
    }
    
    // 主要トピックの特定（スコアが0.1以上のトピック）
    const mainTopics = Object.entries(topicScores)
      .filter(([, score]) => score >= 0.1)
      .sort((a, b) => b[1] - a[1])
      .map(([topic, score]) => ({
        topic: topic,
        score: score
      }));
    
    return {
      ...feedback,
      sentiment: {
        score: sentimentScore,
        label: sentiment,
        positive_words: positiveCount,
        negative_words: negativeCount
      },
      topics: mainTopics
    };
  });
  
  // 全体的な満足度の集計
  const overallSatisfaction = {
    average_rating: feedbacks.reduce((sum, f) => sum + (f.rating || 0), 0) / feedbacks.length,
    rating_distribution: {},
    sentiment_distribution: {
      positive: 0,
      neutral: 0,
      negative: 0
    }
  };
  
  // 評価の分布を集計
  for (const feedback of feedbacks) {
    if (feedback.rating) {
      overallSatisfaction.rating_distribution[feedback.rating] = 
        (overallSatisfaction.rating_distribution[feedback.rating] || 0) + 1;
    }
  }
  
  // 感情の分布を集計
  for (const feedback of analyzedFeedbacks) {
    overallSatisfaction.sentiment_distribution[feedback.sentiment.label]++;
  }
  
  // トピック別の満足度分析
  const topicSatisfaction = {};
  for (const topic of Object.keys(topicKeywords)) {
    const topicFeedbacks = analyzedFeedbacks.filter(f => 
      f.topics.some(t => t.topic === topic)
    );
    
    if (topicFeedbacks.length > 0) {
      const avgRating = topicFeedbacks.reduce((sum, f) => sum + (f.rating || 0), 0) / topicFeedbacks.length;
      const sentimentCounts = {
        positive: topicFeedbacks.filter(f => f.sentiment.label === 'positive').length,
        neutral: topicFeedbacks.filter(f => f.sentiment.label === 'neutral').length,
        negative: topicFeedbacks.filter(f => f.sentiment.label === 'negative').length
      };
      
      topicSatisfaction[topic] = {
        topic: topic,
        feedback_count: topicFeedbacks.length,
        average_rating: avgRating,
        sentiment_distribution: {
          positive: sentimentCounts.positive / topicFeedbacks.length,
          neutral: sentimentCounts.neutral / topicFeedbacks.length,
          negative: sentimentCounts.negative / topicFeedbacks.length
        },
        satisfaction_score: avgRating / 5, // 0～1のスコアに正規化
        sample_feedbacks: topicFeedbacks
          .sort((a, b) => Math.abs(b.sentiment.score) - Math.abs(a.sentiment.score))
          .slice(0, 3)
          .map(f => ({
            id: f.id,
            text: f.text,
            rating: f.rating,
            sentiment: f.sentiment.label
          }))
      };
    }
  }
  
  // 主要な不満点の特定
  const painPoints = Object.entries(topicSatisfaction)
    .filter(([, data]) => data.satisfaction_score < 0.6)
    .sort((a, b) => a[1].satisfaction_score - b[1].satisfaction_score)
    .map(([topic, data]) => ({
      topic: topic,
      satisfaction_score: data.satisfaction_score,
      feedback_count: data.feedback_count,
      negative_percentage: data.sentiment_distribution.negative,
      sample_feedbacks: analyzedFeedbacks
        .filter(f => f.topics.some(t => t.topic === topic) && f.sentiment.label === 'negative')
        .sort((a, b) => a.sentiment.score - b.sentiment.score)
        .slice(0, 3)
        .map(f => ({
          id: f.id,
          text: f.text,
          rating: f.rating,
          sentiment_score: f.sentiment.score
        }))
    }));
  
  // 時系列での満足度推移
  const timeSeriesSatisfaction = analyzeSatisfactionTrend(analyzedFeedbacks);
  
  // 結果を整形
  const result = {
    overall_satisfaction: overallSatisfaction,
    topic_satisfaction: Object.values(topicSatisfaction)
      .sort((a, b) => b.feedback_count - a.feedback_count),
    pain_points: painPoints,
    time_series_satisfaction: timeSeriesSatisfaction,
    metadata: {
      feedback_count: feedbacks.length,
      date_range: {
        start: new Date(Math.min(...feedbacks.map(f => f.date))).toISOString(),
        end: new Date(Math.max(...feedbacks.map(f => f.date))).toISOString()
      },
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// 時系列での満足度推移を分析
function analyzeSatisfactionTrend(feedbacks) {
  // 月ごとにフィードバックをグループ化
  const monthlyFeedbacks = {};
  
  for (const feedback of feedbacks) {
    const year = feedback.date.getFullYear();
    const month = feedback.date.getMonth() + 1;
    const yearMonth = `${year}-${month.toString().padStart(2, '0')}`;
    
    if (!monthlyFeedbacks[yearMonth]) {
      monthlyFeedbacks[yearMonth] = [];
    }
    
    monthlyFeedbacks[yearMonth].push(feedback);
  }
  
  // 月ごとの満足度を計算
  const timeSeriesData = Object.entries(monthlyFeedbacks)
    .map(([yearMonth, monthFeedbacks]) => {
      const avgRating = monthFeedbacks.reduce((sum, f) => sum + (f.rating || 0), 0) / monthFeedbacks.length;
      
      const sentimentCounts = {
        positive: monthFeedbacks.filter(f => f.sentiment.label === 'positive').length,
        neutral: monthFeedbacks.filter(f => f.sentiment.label === 'neutral').length,
        negative: monthFeedbacks.filter(f => f.sentiment.label === 'negative').length
      };
      
      // トピック別の言及数
      const topicMentions = {};
      for (const feedback of monthFeedbacks) {
        for (const topicData of feedback.topics) {
          const topic = topicData.topic;
          topicMentions[topic] = (topicMentions[topic] || 0) + 1;
        }
      }
      
      return {
        year_month: yearMonth,
        feedback_count: monthFeedbacks.length,
        average_rating: avgRating,
        sentiment_distribution: {
          positive: sentimentCounts.positive / monthFeedbacks.length,
          neutral: sentimentCounts.neutral / monthFeedbacks.length,
          negative: sentimentCounts.negative / monthFeedbacks.length
        },
        satisfaction_score: avgRating / 5, // 0～1のスコアに正規化
        topic_mentions: Object.entries(topicMentions)
          .sort((a, b) => b[1] - a[1])
          .map(([topic, count]) => ({
            topic: topic,
            count: count,
            percentage: count / monthFeedbacks.length
          }))
      };
    })
    .sort((a, b) => a.year_month.localeCompare(b.year_month));
  
  return timeSeriesData;
}

// メイン処理
return analyzeCustomerFeedback($input.all());
```

このような顧客満足度・不満点分析ロジックを実装することで、顧客フィードバックから感情やトピックを自動的に抽出し、満足度の要因や不満点を特定することができます。また、トピック別の満足度分析や時系列での満足度推移も把握することで、改善すべき領域や成功している取り組みを明確にすることができます。

これらのマーケット視点の分析実装により、コンセンサスモデルは市場動向、競合状況、顧客ニーズなどを多角的に評価し、市場機会の特定や差別化戦略の策定を支援することができます。また、これらの分析結果は、テクノロジー視点やビジネス視点の分析と統合することで、より包括的な意思決定基盤を構築することが可能になります。
