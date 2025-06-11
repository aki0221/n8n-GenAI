### 4.3 ビジネス視点の分析

ビジネス視点の分析は、コンセンサスモデルにおいて、技術や市場の動向が自社の事業戦略や財務状況にどのような影響を与えるかを評価するための重要なコンポーネントです。この分析では、事業ポートフォリオ、財務状況、組織能力、リスク管理などを体系的に分析し、持続的な成長と競争優位性の確立を目指します。n8nを活用することで、ビジネス視点の分析プロセスを効率的かつ再現性高く実装することができます。

**事業ポートフォリオ分析の実装方法**

事業ポートフォリオ分析は、企業が展開する複数の事業を評価し、リソース配分の最適化や、将来の成長戦略を策定するプロセスです。この分析により、企業は成長性の高い事業への投資集中や、不採算事業からの撤退など、戦略的な意思決定を行うことができます。

n8nでの事業ポートフォリオ分析の実装方法としては、主にFunctionノードと外部データソース（例：財務データベース、CRMシステム）との連携が活用されます。以下に、具体的な実装例を示します：

**BCGマトリックス分析**:
各事業の市場成長率と相対的市場シェアを評価し、「花形（Star）」、「金のなる木（Cash Cow）」、「問題児（Question Mark）」、「負け犬（Dog）」の4つのカテゴリに分類します。

```javascript
// BCGマトリックス分析の実装例
function analyzeBusinessPortfolioBCG(items) {
  // 各事業のデータを整理
  const businesses = items.map(item => item.json);
  
  // 市場成長率と相対的市場シェアの閾値を設定
  const growthRateThreshold = 0.1; // 例: 10%以上を高成長と定義
  const marketShareThreshold = 1.0; // 例: 相対的市場シェア1.0以上を高シェアと定義
  
  // 各事業をBCGマトリックスに分類
  const categorizedBusinesses = businesses.map(business => {
    let category = 
      business.market_growth_rate >= growthRateThreshold && business.relative_market_share >= marketShareThreshold ? 'Star' :
      business.market_growth_rate < growthRateThreshold && business.relative_market_share >= marketShareThreshold ? 'Cash Cow' :
      business.market_growth_rate >= growthRateThreshold && business.relative_market_share < marketShareThreshold ? 'Question Mark' :
      'Dog';
      
    // 戦略的推奨事項の生成（簡易版）
    let strategicRecommendation = '';
    switch (category) {
      case 'Star':
        strategicRecommendation = '積極的な投資を継続し、市場リーダーシップを維持・強化する。';
        break;
      case 'Cash Cow':
        strategicRecommendation = '収益性を最大化し、得られたキャッシュフローを他の成長事業へ再投資する。';
        break;
      case 'Question Mark':
        strategicRecommendation = '市場シェア拡大のための戦略的投資を検討するか、将来性が見込めなければ撤退を検討する。';
        break;
      case 'Dog':
        strategicRecommendation = '事業の再構築、売却、または撤退を検討する。リソースの再配分を優先する。';
        break;
    }
    
    return {
      business_id: business.business_id,
      business_name: business.business_name,
      market_growth_rate: business.market_growth_rate,
      relative_market_share: business.relative_market_share,
      revenue: business.revenue,
      profit: business.profit,
      bcg_category: category,
      strategic_recommendation: strategicRecommendation,
      data_source: business.data_source,
      analysis_date: new Date().toISOString()
    };
  });
  
  // カテゴリ別の集計
  const categorySummary = {};
  for (const business of categorizedBusinesses) {
    if (!categorySummary[business.bcg_category]) {
      categorySummary[business.bcg_category] = {
        count: 0,
        total_revenue: 0,
        total_profit: 0,
        businesses: []
      };
    }
    categorySummary[business.bcg_category].count++;
    categorySummary[business.bcg_category].total_revenue += business.revenue || 0;
    categorySummary[business.bcg_category].total_profit += business.profit || 0;
    categorySummary[business.bcg_category].businesses.push({
      id: business.business_id,
      name: business.business_name,
      revenue: business.revenue,
      profit: business.profit
    });
  }
  
  // 結果を整形
  const result = {
    businesses: categorizedBusinesses.sort((a,b) => (b.revenue || 0) - (a.revenue || 0) ),
    summary: Object.entries(categorySummary).map(([category, data]) => ({
      category: category,
      count: data.count,
      total_revenue: data.total_revenue,
      total_profit: data.total_profit,
      avg_revenue_per_business: data.count > 0 ? data.total_revenue / data.count : 0,
      businesses: data.businesses
    })),
    metadata: {
      growth_rate_threshold: growthRateThreshold,
      market_share_threshold: marketShareThreshold,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeBusinessPortfolioBCG($input.all());
```

このようなBCGマトリックス分析ロジックを実装することで、各事業の市場ポジションを客観的に評価し、リソース配分の最適化や戦略的な意思決定に役立てることができます。また、カテゴリ別の集計により、ポートフォリオ全体のバランスや課題も把握できます。

**GE/マッキンゼー・マトリックス分析**:
各事業の業界魅力度と事業強度を評価し、9つのセルに分類して、投資優先度を決定します。

```javascript
// GE/マッキンゼー・マトリックス分析の実装例
function analyzeBusinessPortfolioGE(items) {
  // 各事業のデータを整理
  const businesses = items.map(item => item.json);
  
  // 業界魅力度と事業強度の評価基準（例）
  const industryAttractivenessFactors = [
    { id: 'market_size', name: '市場規模', weight: 0.2 },
    { id: 'market_growth', name: '市場成長率', weight: 0.3 },
    { id: 'profitability', name: '収益性', weight: 0.25 },
    { id: 'competition_intensity', name: '競争激度', weight: -0.15 }, // マイナスウェイト
    { id: 'entry_barriers', name: '参入障壁', weight: 0.1 }
  ];
  
  const businessStrengthFactors = [
    { id: 'market_share', name: '市場シェア', weight: 0.25 },
    { id: 'brand_equity', name: 'ブランド力', weight: 0.2 },
    { id: 'product_differentiation', name: '製品差別化', weight: 0.2 },
    { id: 'cost_efficiency', name: 'コスト効率', weight: 0.15 },
    { id: 'distribution_channels', name: '販売チャネル', weight: 0.1 },
    { id: 'management_capability', name: '経営能力', weight: 0.1 }
  ];
  
  // 各事業のスコアを計算
  const scoredBusinesses = businesses.map(business => {
    // 業界魅力度の計算
    let industryAttractivenessScore = 0;
    for (const factor of industryAttractivenessFactors) {
      if (business.industry_factors && business.industry_factors[factor.id] !== undefined) {
        // スコアは1～5の範囲と仮定
        const score = Math.max(1, Math.min(5, business.industry_factors[factor.id]));
        industryAttractivenessScore += score * factor.weight;
      }
    }
    
    // 事業強度の計算
    let businessStrengthScore = 0;
    for (const factor of businessStrengthFactors) {
      if (business.strength_factors && business.strength_factors[factor.id] !== undefined) {
        // スコアは1～5の範囲と仮定
        const score = Math.max(1, Math.min(5, business.strength_factors[factor.id]));
        businessStrengthScore += score * factor.weight;
      }
    }
    
    // スコアを正規化（0～1の範囲に）
    const normalizedIA = (industryAttractivenessScore - 1) / 4; // (score - min) / (max - min)
    const normalizedBS = (businessStrengthScore - 1) / 4;
    
    // GEマトリックスのカテゴリ分類
    let geCategory = '';
    let strategicAction = '';
    
    if (normalizedIA >= 0.66 && normalizedBS >= 0.66) {
      geCategory = '成長/投資'; strategicAction = 'リーダーシップ維持のための積極投資、成長機会の追求。';
    } else if (normalizedIA >= 0.66 && normalizedBS >= 0.33 && normalizedBS < 0.66) {
      geCategory = '成長/選択的投資'; strategicAction = '市場セグメントへの集中投資、弱点の克服。';
    } else if (normalizedIA >= 0.33 && normalizedIA < 0.66 && normalizedBS >= 0.66) {
      geCategory = '選択的投資/収益維持'; strategicAction = '収益性重視の投資、市場シェアの維持。';
    } else if (normalizedIA >= 0.33 && normalizedIA < 0.66 && normalizedBS >= 0.33 && normalizedBS < 0.66) {
      geCategory = '選択的投資/注意深い管理'; strategicAction = 'リスク管理と収益性維持、ニッチ市場での機会探索。';
    } else if (normalizedIA < 0.33 && normalizedBS >= 0.66) {
      geCategory = '収穫/撤退準備'; strategicAction = 'キャッシュフロー最大化、段階的な撤退準備。';
    } else if (normalizedIA >= 0.66 && normalizedBS < 0.33) {
      geCategory = '選択的投資/再構築'; strategicAction = '事業再構築による競争力強化、または撤退検討。';
    } else if (normalizedIA < 0.33 && normalizedBS >= 0.33 && normalizedBS < 0.66) {
      geCategory = '収穫/撤退'; strategicAction = '収益確保と早期の撤退検討。';
    } else if (normalizedIA >= 0.33 && normalizedIA < 0.66 && normalizedBS < 0.33) {
      geCategory = '撤退/再構築'; strategicAction = '事業売却または再構築によるニッチ市場での生存模索。';
    } else { // normalizedIA < 0.33 && normalizedBS < 0.33
      geCategory = '撤退'; strategicAction = '速やかな事業売却または撤退。';
    }
    
    return {
      business_id: business.business_id,
      business_name: business.business_name,
      industry_attractiveness: normalizedIA,
      business_strength: normalizedBS,
      revenue: business.revenue,
      profit: business.profit,
      ge_category: geCategory,
      strategic_action: strategicAction,
      industry_factors_raw: business.industry_factors,
      strength_factors_raw: business.strength_factors,
      analysis_date: new Date().toISOString()
    };
  });
  
  // カテゴリ別の集計
  const categorySummary = {};
  for (const business of scoredBusinesses) {
    if (!categorySummary[business.ge_category]) {
      categorySummary[business.ge_category] = {
        count: 0,
        total_revenue: 0,
        total_profit: 0,
        businesses: []
      };
    }
    categorySummary[business.ge_category].count++;
    categorySummary[business.ge_category].total_revenue += business.revenue || 0;
    categorySummary[business.ge_category].total_profit += business.profit || 0;
    categorySummary[business.ge_category].businesses.push({
      id: business.business_id,
      name: business.business_name,
      revenue: business.revenue,
      profit: business.profit
    });
  }
  
  // 結果を整形
  const result = {
    businesses: scoredBusinesses.sort((a,b) => (b.revenue || 0) - (a.revenue || 0) ),
    summary: Object.entries(categorySummary).map(([category, data]) => ({
      category: category,
      count: data.count,
      total_revenue: data.total_revenue,
      total_profit: data.total_profit,
      businesses: data.businesses
    })),
    evaluation_criteria: {
      industry_attractiveness_factors: industryAttractivenessFactors,
      business_strength_factors: businessStrengthFactors
    },
    metadata: {
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeBusinessPortfolioGE($input.all());
```

このようなGE/マッキンゼー・マトリックス分析ロジックを実装することで、各事業の業界魅力度と事業強度を多角的に評価し、より詳細な投資優先度の判断や戦略策定に役立てることができます。また、評価基準を明確にすることで、分析の客観性と透明性を高めることができます。

**財務分析の実装方法**

財務分析は、企業の財務諸表（貸借対照表、損益計算書、キャッシュフロー計算書）を分析し、収益性、安全性、成長性、効率性などを評価するプロセスです。この分析により、企業は財務状況の健全性を把握し、経営課題の特定や改善策の策定に役立つ洞察を得ることができます。

n8nでの財務分析の実装方法としては、主にFunctionノードと会計システムやERPシステムとの連携が活用されます。以下に、具体的な実装例を示します：

**主要財務指標の計算とトレンド分析**:
収益性指標（売上高総利益率、営業利益率、ROEなど）、安全性指標（流動比率、自己資本比率など）、成長性指標（売上高成長率、利益成長率など）、効率性指標（総資産回転率、棚卸資産回転率など）を計算し、時系列での変化を分析します。

```javascript
// 主要財務指標の計算とトレンド分析の実装例
function analyzeFinancialPerformance(items) {
  // 財務データを整理（各アイテムが特定の期間の財務諸表データと仮定）
  const financialData = items.map(item => item.json).sort((a, b) => new Date(a.period_end_date) - new Date(b.period_end_date));
  
  // 各期間の財務指標を計算
  const financialMetrics = financialData.map((data, index) => {
    const metrics = {
      period_end_date: data.period_end_date,
      company_id: data.company_id,
      // 収益性指標
      gross_profit_margin: data.revenue && data.cost_of_goods_sold !== undefined ? (data.revenue - data.cost_of_goods_sold) / data.revenue : null,
      operating_profit_margin: data.revenue && data.operating_income !== undefined ? data.operating_income / data.revenue : null,
      net_profit_margin: data.revenue && data.net_income !== undefined ? data.net_income / data.revenue : null,
      roe: data.net_income && data.total_equity ? data.net_income / data.total_equity : null, // Return on Equity
      roa: data.net_income && data.total_assets ? data.net_income / data.total_assets : null, // Return on Assets
      
      // 安全性指標
      current_ratio: data.current_assets && data.current_liabilities ? data.current_assets / data.current_liabilities : null,
      quick_ratio: data.current_assets && data.inventory && data.current_liabilities ? (data.current_assets - data.inventory) / data.current_liabilities : null,
      debt_to_equity_ratio: data.total_debt && data.total_equity ? data.total_debt / data.total_equity : null,
      equity_ratio: data.total_equity && data.total_assets ? data.total_equity / data.total_assets : null,
      
      // 成長性指標 (前年同期比)
      revenue_growth_rate: null,
      net_income_growth_rate: null,
      total_assets_growth_rate: null,
      
      // 効率性指標
      total_asset_turnover: data.revenue && data.total_assets ? data.revenue / data.total_assets : null,
      inventory_turnover: data.cost_of_goods_sold && data.inventory ? data.cost_of_goods_sold / data.inventory : null,
      days_sales_outstanding: data.accounts_receivable && data.revenue ? (data.accounts_receivable / data.revenue) * 365 : null, // 売上債権回転日数
      
      // キャッシュフロー指標
      operating_cash_flow_margin: data.operating_cash_flow && data.revenue ? data.operating_cash_flow / data.revenue : null,
      free_cash_flow: data.operating_cash_flow && data.capital_expenditures !== undefined ? data.operating_cash_flow - data.capital_expenditures : null
    };
    
    // 成長率の計算 (前年同期データが存在する場合)
    if (index > 0) {
      const prevData = financialData[index - 1];
      if (prevData.revenue) metrics.revenue_growth_rate = (data.revenue - prevData.revenue) / prevData.revenue;
      if (prevData.net_income) metrics.net_income_growth_rate = (data.net_income - prevData.net_income) / prevData.net_income;
      if (prevData.total_assets) metrics.total_assets_growth_rate = (data.total_assets - prevData.total_assets) / prevData.total_assets;
    }
    
    return metrics;
  });
  
  // 主要指標のトレンド分析（簡易的な傾向評価）
  const keyMetricsForTrend = [
    'gross_profit_margin', 'operating_profit_margin', 'net_profit_margin', 'roe',
    'current_ratio', 'debt_to_equity_ratio',
    'revenue_growth_rate', 'net_income_growth_rate',
    'total_asset_turnover', 'operating_cash_flow_margin'
  ];
  
  const trendAnalysis = {};
  for (const metricName of keyMetricsForTrend) {
    const values = financialMetrics.map(m => m[metricName]).filter(v => v !== null && !isNaN(v));
    
    if (values.length >= 3) {
      const firstHalfAvg = values.slice(0, Math.floor(values.length / 2)).reduce((sum, v) => sum + v, 0) / Math.floor(values.length / 2);
      const secondHalfAvg = values.slice(Math.ceil(values.length / 2)).reduce((sum, v) => sum + v, 0) / Math.ceil(values.length / 2);
      
      let trend = 'stable';
      if (secondHalfAvg > firstHalfAvg * 1.05) trend = 'improving'; // 5%以上改善
      else if (secondHalfAvg < firstHalfAvg * 0.95) trend = 'deteriorating'; // 5%以上悪化
      
      trendAnalysis[metricName] = {
        trend: trend,
        latest_value: values[values.length - 1],
        average_value: values.reduce((sum, v) => sum + v, 0) / values.length,
        values: values
      };
    }
  }
  
  // 財務健全性スコアの計算（簡易版）
  let financialHealthScore = 0;
  let scoreComponents = 0;
  
  const healthChecks = [
    { metric: 'operating_profit_margin', threshold: 0.05, weight: 0.2 }, // 営業利益率5%以上
    { metric: 'current_ratio', threshold: 1.5, weight: 0.15 }, // 流動比率1.5以上
    { metric: 'debt_to_equity_ratio', threshold: 1.0, weight: 0.15, lower_is_better: true }, // 負債資本倍率1.0以下
    { metric: 'revenue_growth_rate', threshold: 0.05, weight: 0.2 }, // 売上成長率5%以上
    { metric: 'operating_cash_flow_margin', threshold: 0.1, weight: 0.15 }, //営業CFマージン10%以上
    { metric: 'roe', threshold: 0.1, weight: 0.15 } // ROE 10%以上
  ];
  
  for (const check of healthChecks) {
    const latestValue = trendAnalysis[check.metric]?.latest_value;
    if (latestValue !== undefined) {
      let pass = false;
      if (check.lower_is_better) {
        pass = latestValue <= check.threshold;
      } else {
        pass = latestValue >= check.threshold;
      }
      financialHealthScore += (pass ? 1 : 0) * check.weight;
      scoreComponents += check.weight;
    }
  }
  
  const normalizedHealthScore = scoreComponents > 0 ? financialHealthScore / scoreComponents : null;
  let healthRating = 'N/A';
  if (normalizedHealthScore !== null) {
    if (normalizedHealthScore >= 0.8) healthRating = 'Excellent';
    else if (normalizedHealthScore >= 0.6) healthRating = 'Good';
    else if (normalizedHealthScore >= 0.4) healthRating = 'Fair';
    else healthRating = 'Poor';
  }
  
  // 結果を整形
  const result = {
    financial_metrics_time_series: financialMetrics,
    trend_analysis: trendAnalysis,
    financial_health: {
      score: normalizedHealthScore,
      rating: healthRating,
      details: healthChecks.map(check => ({
        metric: check.metric,
        latest_value: trendAnalysis[check.metric]?.latest_value,
        threshold: check.threshold,
        pass: trendAnalysis[check.metric]?.latest_value !== undefined ? 
              (check.lower_is_better ? trendAnalysis[check.metric].latest_value <= check.threshold : trendAnalysis[check.metric].latest_value >= check.threshold) : null
      }))
    },
    metadata: {
      company_id: financialData.length > 0 ? financialData[0].company_id : null,
      period_count: financialData.length,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeFinancialPerformance($input.all());
```

このような財務指標分析ロジックを実装することで、企業の収益性、安全性、成長性、効率性を多角的に評価し、財務状況の健全性や経営課題を客観的に把握することができます。また、時系列でのトレンド分析や財務健全性スコアの算出により、将来の業績予測や改善策の検討にも役立てることができます。

**組織能力評価の実装方法**

組織能力評価は、企業の戦略実行に必要な人材、プロセス、技術、文化などの組織的な能力を評価し、強みと弱みを特定するプロセスです。この分析により、企業は組織能力の向上や、戦略実行力の強化に役立つ洞察を得ることができます。

n8nでの組織能力評価の実装方法としては、主にFunctionノードと人事システムやアンケートツールとの連携が活用されます。以下に、具体的な実装例を示します：

**コアコンピタンス分析**:
企業の競争優位性の源泉となる独自の技術、ノウハウ、プロセスなどを特定し、その持続可能性や強化策を評価します。

```javascript
// コアコンピタンス分析の実装例
function analyzeCoreCompetencies(items) {
  // 評価対象のコンピタンスデータを整理
  const competencies = items.map(item => item.json);
  
  // VRIOフレームワークの評価基準
  const vrioCriteria = [
    { id: 'value', name: '経済価値 (Value)', question: 'その能力は市場機会を活用したり、脅威を無力化したりするのに役立つか？' },
    { id: 'rarity', name: '希少性 (Rarity)', question: 'その能力を保有している競合他社は少ないか？' },
    { id: 'inimitability', name: '模倣困難性 (Inimitability)', question: '競合他社がその能力を模倣するのは困難か、コストがかかるか？' },
    { id: 'organization', name: '組織 (Organization)', question: '企業はその能力を十分に活用するための組織体制（方針、手順、システム）を持っているか？' }
  ];
  
  // 各コンピタンスをVRIOフレームワークで評価
  const analyzedCompetencies = competencies.map(competency => {
    const vrioScores = {};
    let competitiveAdvantage = 'Competitive Disadvantage';
    
    // 各基準で評価（1: No, 2: Partially, 3: Yes と仮定）
    for (const criterion of vrioCriteria) {
      const score = competency.vrio_assessment && competency.vrio_assessment[criterion.id] !== undefined 
                  ? competency.vrio_assessment[criterion.id] 
                  : 1; // デフォルトはNo
      vrioScores[criterion.id] = score;
    }
    
    // 競争優位性の判定
    if (vrioScores.value >= 2) {
      competitiveAdvantage = 'Competitive Parity';
      if (vrioScores.rarity >= 2) {
        competitiveAdvantage = 'Temporary Competitive Advantage';
        if (vrioScores.inimitability >= 2) {
          competitiveAdvantage = 'Sustainable Competitive Advantage (Unused)';
          if (vrioScores.organization >= 2) {
            competitiveAdvantage = 'Sustainable Competitive Advantage (Used)';
          }
        }
      }
    }
    
    // 強化策の提案（簡易版）
    let improvementSuggestions = [];
    if (vrioScores.value < 2) improvementSuggestions.push('市場価値を高めるための応用分野を探索する。');
    if (vrioScores.rarity < 2 && vrioScores.value >=2) improvementSuggestions.push('独自性を高めるための改良や特許化を検討する。');
    if (vrioScores.inimitability < 2 && vrioScores.rarity >=2) improvementSuggestions.push('模倣障壁を構築する（例：複雑なプロセス、企業文化との連携）。');
    if (vrioScores.organization < 2 && vrioScores.inimitability >=2) improvementSuggestions.push('能力を最大限に活用するための組織体制やインセンティブを見直す。');
    
    return {
      competency_id: competency.competency_id,
      competency_name: competency.competency_name,
      description: competency.description,
      category: competency.category,
      vrio_assessment: vrioScores,
      vrio_criteria_questions: vrioCriteria.reduce((obj, item) => { obj[item.id] = item.question; return obj; }, {}),
      competitive_advantage: competitiveAdvantage,
      strength_level: (vrioScores.value + vrioScores.rarity + vrioScores.inimitability + vrioScores.organization) / 4, // 簡易的な強みレベル
      improvement_suggestions: improvementSuggestions,
      related_products_services: competency.related_products_services || [],
      assessment_date: new Date().toISOString()
    };
  });
  
  // 競争優位性別の集計
  const advantageSummary = {};
  for (const competency of analyzedCompetencies) {
    if (!advantageSummary[competency.competitive_advantage]) {
      advantageSummary[competency.competitive_advantage] = {
        count: 0,
        competencies: []
      };
    }
    advantageSummary[competency.competitive_advantage].count++;
    advantageSummary[competency.competitive_advantage].competencies.push({
      id: competency.competency_id,
      name: competency.competency_name,
      strength_level: competency.strength_level
    });
  }
  
  // 結果を整形
  const result = {
    competencies: analyzedCompetencies.sort((a,b) => b.strength_level - a.strength_level),
    summary_by_advantage: Object.entries(advantageSummary).map(([advantage, data]) => ({
      competitive_advantage: advantage,
      count: data.count,
      competencies: data.competencies.sort((a,b) => b.strength_level - a.strength_level)
    })),
    vrio_framework_description: vrioCriteria,
    metadata: {
      competency_count: competencies.length,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeCoreCompetencies($input.all());
```

このようなコアコンピタンス分析ロジックを実装することで、企業の競争優位性の源泉となる能力をVRIOフレームワークなどの体系的な手法で評価し、持続的な競争優位性の構築や強化策の検討に役立てることができます。

**人材ポートフォリオ分析**:
従業員のスキル、経験、役職、部門などの情報を分析し、人材の過不足や育成ニーズを特定します。

```javascript
// 人材ポートフォリオ分析の実装例
function analyzeHumanResources(items) {
  // 従業員データを整理
  const employees = items.map(item => item.json);
  
  // スキルセットの定義（例）
  const skillCategories = [
    { id: 'technical', name: '専門技術スキル', keywords: ['python', 'java', 'c++', 'data analysis', 'machine learning', 'cad', 'engineering'] },
    { id: 'business', name: 'ビジネススキル', keywords: ['project management', 'marketing', 'sales', 'finance', 'strategy', 'negotiation'] },
    { id: 'soft', name: 'ソフトスキル', keywords: ['communication', 'leadership', 'problem solving', 'teamwork', 'creativity'] },
    { id: 'language', name: '語学スキル', keywords: ['english', 'chinese', 'spanish', 'german', 'french'] }
  ];
  
  // 各従業員のスキルプロファイルを生成
  const employeeProfiles = employees.map(employee => {
    const skills = {};
    for (const category of skillCategories) {
      skills[category.id] = {
        name: category.name,
        count: 0,
        matched_skills: []
      };
      
      if (employee.skills && Array.isArray(employee.skills)) {
        for (const skill of employee.skills) {
          if (category.keywords.some(keyword => skill.toLowerCase().includes(keyword))) {
            skills[category.id].count++;
            skills[category.id].matched_skills.push(skill);
          }
        }
      }
    }
    
    // 経験年数に基づくキャリアステージの判定
    let careerStage = 'Early Career';
    if (employee.years_of_experience >= 15) careerStage = 'Senior/Expert';
    else if (employee.years_of_experience >= 7) careerStage = 'Mid Career';
    
    return {
      employee_id: employee.employee_id,
      name: employee.name,
      department: employee.department,
      role: employee.role,
      years_of_experience: employee.years_of_experience,
      career_stage: careerStage,
      performance_rating: employee.performance_rating, // 1-5段階評価と仮定
      potential_rating: employee.potential_rating, // 1-5段階評価と仮定
      skills_profile: skills,
      education_level: employee.education_level,
      certifications: employee.certifications || []
    };
  });
  
  // 9ボックスグリッド分析（パフォーマンスとポテンシャル）
  const nineBoxGrid = {
    'High Potentials': [], // 高パフォーマンス・高ポテンシャル
    'Core Players': [],    // 高パフォーマンス・中ポテンシャル
    'Solid Performers': [],// 高パフォーマンス・低ポテンシャル
    'Emerging Potentials': [],// 中パフォーマンス・高ポテンシャル
    'Key Contributors': [], // 中パフォーマンス・中ポテンシャル
    'Reliable Performers': [],// 中パフォーマンス・低ポテンシャル
    'Inconsistent Performers': [],// 低パフォーマンス・高ポテンシャル
    'Needs Development': [], // 低パフォーマンス・中ポテンシャル
    'Underperformers': [] // 低パフォーマンス・低ポテンシャル
  };
  
  for (const profile of employeeProfiles) {
    const perf = profile.performance_rating;
    const pot = profile.potential_rating;
    let box = 'Needs Development';
    
    if (perf >= 4 && pot >= 4) box = 'High Potentials';
    else if (perf >= 4 && pot === 3) box = 'Core Players';
    else if (perf >= 4 && pot <= 2) box = 'Solid Performers';
    else if (perf === 3 && pot >= 4) box = 'Emerging Potentials';
    else if (perf === 3 && pot === 3) box = 'Key Contributors';
    else if (perf === 3 && pot <= 2) box = 'Reliable Performers';
    else if (perf <= 2 && pot >= 4) box = 'Inconsistent Performers';
    else if (perf <= 2 && pot <= 2) box = 'Underperformers';
    
    nineBoxGrid[box].push({
      employee_id: profile.employee_id,
      name: profile.name,
      department: profile.department,
      role: profile.role
    });
  }
  
  // 部門別のスキル分布
  const departmentSkillDistribution = {};
  for (const profile of employeeProfiles) {
    if (!departmentSkillDistribution[profile.department]) {
      departmentSkillDistribution[profile.department] = {};
      for (const category of skillCategories) {
        departmentSkillDistribution[profile.department][category.id] = { total_skills: 0, employee_count: 0 };
      }
    }
    
    departmentSkillDistribution[profile.department].employee_count = 
      (departmentSkillDistribution[profile.department].employee_count || 0) + 1;
      
    for (const category of skillCategories) {
      departmentSkillDistribution[profile.department][category.id].total_skills += profile.skills_profile[category.id].count;
    }
  }
  
  // 部門別平均スキル数の計算
  for (const dept of Object.keys(departmentSkillDistribution)) {
    for (const category of skillCategories) {
      const data = departmentSkillDistribution[dept][category.id];
      departmentSkillDistribution[dept][category.id].average_skills_per_employee = 
        data.employee_count > 0 ? data.total_skills / data.employee_count : 0;
    }
  }
  
  // 結果を整形
  const result = {
    employee_profiles: employeeProfiles,
    nine_box_grid_analysis: Object.entries(nineBoxGrid).map(([box, employees]) => ({
      box_name: box,
      employee_count: employees.length,
      employees: employees
    })),
    department_skill_distribution: Object.entries(departmentSkillDistribution).map(([department, skills]) => ({
      department: department,
      employee_count: skills.employee_count,
      skill_summary: Object.entries(skills)
        .filter(([key]) => key !== 'employee_count')
        .map(([skill_category_id, data]) => ({
          category_id: skill_category_id,
          category_name: skillCategories.find(c => c.id === skill_category_id)?.name,
          total_skills: data.total_skills,
          average_skills_per_employee: data.average_skills_per_employee
        }))
    })),
    overall_skill_summary: skillCategories.map(category => ({
      category_id: category.id,
      category_name: category.name,
      total_skills_in_organization: employeeProfiles.reduce((sum, p) => sum + p.skills_profile[category.id].count, 0),
      average_skills_per_employee: employeeProfiles.length > 0 ? 
        employeeProfiles.reduce((sum, p) => sum + p.skills_profile[category.id].count, 0) / employeeProfiles.length : 0
    })),
    metadata: {
      employee_count: employees.length,
      skill_categories_defined: skillCategories.length,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}

// メイン処理
return analyzeHumanResources($input.all());
```

このような人材ポートフォリオ分析ロジックを実装することで、従業員のスキル、経験、パフォーマンス、ポテンシャルなどを多角的に評価し、人材の過不足や育成ニーズを特定することができます。9ボックスグリッド分析や部門別のスキル分布分析により、戦略的な人材配置や育成計画の策定にも役立てることができます。

これらのビジネス視点の分析実装により、コンセンサスモデルは事業ポートフォリオ、財務状況、組織能力などを多角的に評価し、持続的な成長と競争優位性の確立を支援することができます。また、これらの分析結果は、テクノロジー視点やマーケット視点の分析と統合することで、より包括的かつ戦略的な意思決定基盤を構築することが可能になります。
