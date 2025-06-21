### 4.1 テクノロジー視点の分析

テクノロジー視点の分析は、コンセンサスモデルの中核を成す重要なコンポーネントの一つです。この分析では、技術トレンド、研究開発動向、特許情報、技術的実現可能性など、テクノロジーの進化や新興技術に関する情報を体系的に分析します。n8nを活用することで、テクノロジー視点の分析プロセスを効率的かつ再現性高く実装することができます。

**技術トレンド分析の実装方法**

技術トレンド分析は、新興技術や既存技術の進化を定量的・定性的に評価し、将来の技術動向を予測するプロセスです。この分析により、企業は技術投資の優先順位付けや、製品開発の方向性決定に役立つ洞察を得ることができます。

n8nでの技術トレンド分析の実装方法としては、主にFunctionノードとHTTP Requestノードが活用されます。以下に、具体的な実装例を示します：

**時系列データ分析による技術トレンド検出**:
GitHub、Stack Overflow、特許データベースなどから収集した時系列データを分析し、技術の普及率や成長率を計算します。

```javascript
// 技術トレンドの時系列分析実装例
function analyzeTechnologyTrends(items) {
  // 技術キーワードごとにデータをグループ化
  const techGroups = {};
  
  for (const item of items) {
    const tech = item.json.technology;
    const date = new Date(item.json.date);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const yearMonth = `${year}-${month.toString().padStart(2, '0')}`;
    
    if (!techGroups[tech]) {
      techGroups[tech] = {};
    }
    
    if (!techGroups[tech][yearMonth]) {
      techGroups[tech][yearMonth] = {
        count: 0,
        mentions: 0,
        stars: 0
      };
    }
    
    techGroups[tech][yearMonth].count++;
    techGroups[tech][yearMonth].mentions += item.json.mentions || 0;
    techGroups[tech][yearMonth].stars += item.json.stars || 0;
  }
  
  // 各技術の時系列トレンドを計算
  const results = [];
  
  for (const [tech, monthlyData] of Object.entries(techGroups)) {
    // 月次データを時系列順にソート
    const sortedMonths = Object.keys(monthlyData).sort();
    
    // 成長率と移動平均を計算
    const timeSeriesData = sortedMonths.map((month, index) => {
      const current = monthlyData[month];
      
      // 成長率の計算（前月比）
      let growthRate = null;
      if (index > 0) {
        const prevMonth = sortedMonths[index - 1];
        const previous = monthlyData[prevMonth];
        growthRate = previous.count > 0 
          ? (current.count - previous.count) / previous.count 
          : null;
      }
      
      // 3ヶ月移動平均の計算
      let movingAvg = current.count;
      let maCount = 1;
      
      for (let i = 1; i <= 2; i++) {
        if (index - i >= 0) {
          const prevMonth = sortedMonths[index - i];
          movingAvg += monthlyData[prevMonth].count;
          maCount++;
        }
      }
      
      movingAvg = movingAvg / maCount;
      
      return {
        month,
        count: current.count,
        mentions: current.mentions,
        stars: current.stars,
        growth_rate: growthRate,
        moving_avg_3m: movingAvg
      };
    });
    
    // トレンドスコアの計算
    // 最新3ヶ月の平均成長率と直近の絶対数を考慮
    const recentMonths = timeSeriesData.slice(-3);
    const avgRecentGrowth = recentMonths
      .filter(m => m.growth_rate !== null)
      .reduce((sum, m) => sum + m.growth_rate, 0) / 
      recentMonths.filter(m => m.growth_rate !== null).length || 0;
    
    const latestCount = timeSeriesData[timeSeriesData.length - 1]?.count || 0;
    const maxCount = Math.max(...timeSeriesData.map(m => m.count));
    
    // トレンドスコアの計算（成長率と絶対数のバランスを考慮）
    const trendScore = (avgRecentGrowth * 0.7) + ((latestCount / maxCount) * 0.3);
    
    results.push({
      technology: tech,
      trend_score: trendScore,
      latest_count: latestCount,
      avg_growth_rate: avgRecentGrowth,
      time_series: timeSeriesData,
      analysis_date: new Date().toISOString()
    });
  }
  
  // トレンドスコアでソート（降順）
  results.sort((a, b) => b.trend_score - a.trend_score);
  
  return results.map(result => ({ json: result }));
}

// メイン処理
return analyzeTechnologyTrends($input.all());
```

このような時系列分析ロジックを実装することで、各技術キーワードの普及率や成長率を定量的に評価し、注目すべき技術トレンドを特定することができます。また、トレンドスコアを計算することで、多数の技術を客観的な基準で比較・ランク付けすることが可能になります。

**テキストマイニングによる技術キーワード抽出**:
技術ブログ、研究論文、ニュース記事などのテキストデータから、重要な技術キーワードや概念を抽出し、その関連性を分析します。

```javascript
// テキストマイニングによる技術キーワード抽出の実装例
function extractTechnologyKeywords(items) {
  // 技術用語の辞書（簡易版）
  const techTerms = [
    { term: 'artificial intelligence', aliases: ['ai', 'machine intelligence'], category: 'AI' },
    { term: 'machine learning', aliases: ['ml', 'statistical learning'], category: 'AI' },
    { term: 'deep learning', aliases: ['neural networks', 'dnn', 'cnn', 'rnn'], category: 'AI' },
    { term: 'natural language processing', aliases: ['nlp', 'text analytics'], category: 'AI' },
    { term: 'computer vision', aliases: ['image recognition', 'object detection'], category: 'AI' },
    { term: 'blockchain', aliases: ['distributed ledger', 'crypto'], category: 'Blockchain' },
    { term: 'smart contracts', aliases: ['self-executing contracts'], category: 'Blockchain' },
    { term: 'internet of things', aliases: ['iot', 'connected devices'], category: 'IoT' },
    { term: 'edge computing', aliases: ['fog computing'], category: 'Infrastructure' },
    { term: 'quantum computing', aliases: ['quantum information', 'qubits'], category: 'Quantum' },
    { term: 'augmented reality', aliases: ['ar', 'mixed reality'], category: 'XR' },
    { term: 'virtual reality', aliases: ['vr'], category: 'XR' },
    { term: '5g', aliases: ['fifth generation'], category: 'Telecom' },
    { term: 'robotics', aliases: ['robots', 'robotic process'], category: 'Robotics' },
    { term: 'autonomous vehicles', aliases: ['self-driving cars', 'driverless'], category: 'Automotive' }
  ];
  
  // 各アイテムからキーワードを抽出
  const results = [];
  
  for (const item of items) {
    // テキストフィールドを結合
    const text = [
      item.json.title || '',
      item.json.description || '',
      item.json.content || '',
      item.json.abstract || ''
    ].join(' ').toLowerCase();
    
    // キーワードの出現回数をカウント
    const keywordCounts = {};
    const keywordCategories = {};
    
    for (const techTerm of techTerms) {
      // メインの用語をチェック
      const mainRegex = new RegExp(`\\b${techTerm.term}\\b`, 'gi');
      const mainMatches = text.match(mainRegex);
      const mainCount = mainMatches ? mainMatches.length : 0;
      
      // 別名をチェック
      let aliasCount = 0;
      for (const alias of techTerm.aliases) {
        const aliasRegex = new RegExp(`\\b${alias}\\b`, 'gi');
        const aliasMatches = text.match(aliasRegex);
        aliasCount += aliasMatches ? aliasMatches.length : 0;
      }
      
      // 合計カウントを記録
      const totalCount = mainCount + aliasCount;
      if (totalCount > 0) {
        keywordCounts[techTerm.term] = totalCount;
        keywordCategories[techTerm.term] = techTerm.category;
      }
    }
    
    // キーワードの共起関係を分析
    const cooccurrences = [];
    const keywords = Object.keys(keywordCounts);
    
    for (let i = 0; i < keywords.length; i++) {
      for (let j = i + 1; j < keywords.length; j++) {
        cooccurrences.push({
          source: keywords[i],
          target: keywords[j],
          source_category: keywordCategories[keywords[i]],
          target_category: keywordCategories[keywords[j]],
          weight: Math.min(keywordCounts[keywords[i]], keywordCounts[keywords[j]])
        });
      }
    }
    
    // 結果を整形
    results.push({
      source_id: item.json.id,
      source_title: item.json.title,
      source_date: item.json.date,
      keywords: Object.entries(keywordCounts).map(([term, count]) => ({
        term,
        count,
        category: keywordCategories[term]
      })).sort((a, b) => b.count - a.count),
      cooccurrences: cooccurrences,
      analysis_date: new Date().toISOString()
    });
  }
  
  return results.map(result => ({ json: result }));
}

// メイン処理
return extractTechnologyKeywords($input.all());
```

このようなテキストマイニングロジックを実装することで、大量のテキストデータから技術キーワードを自動的に抽出し、その出現頻度や共起関係を分析することができます。これにより、新興技術の早期発見や、技術間の関連性の把握が可能になります。

**特許分析の実装方法**

特許分析は、特許データベースから収集した情報を分析し、技術の革新性、市場性、競合状況などを評価するプロセスです。この分析により、企業は技術的な差別化ポイントや、将来の研究開発の方向性を特定することができます。

n8nでの特許分析の実装方法としては、主にFunctionノードとHTTP Requestノードが活用されます。以下に、具体的な実装例を示します：

**特許出願トレンド分析**:
特定の技術分野における特許出願数の時系列変化を分析し、技術の成熟度や注目度を評価します。

```javascript
// 特許出願トレンド分析の実装例
function analyzePatentTrends(items) {
  // 技術分野ごとに特許データをグループ化
  const fieldGroups = {};
  
  for (const item of items) {
    const field = item.json.technology_field;
    const filingDate = new Date(item.json.filing_date);
    const year = filingDate.getFullYear();
    
    if (!fieldGroups[field]) {
      fieldGroups[field] = {};
    }
    
    if (!fieldGroups[field][year]) {
      fieldGroups[field][year] = {
        count: 0,
        companies: new Set(),
        countries: new Set(),
        citations: 0
      };
    }
    
    fieldGroups[field][year].count++;
    fieldGroups[field][year].companies.add(item.json.applicant_name);
    fieldGroups[field][year].countries.add(item.json.country_code);
    fieldGroups[field][year].citations += item.json.citation_count || 0;
  }
  
  // 各技術分野のトレンドを計算
  const results = [];
  
  for (const [field, yearlyData] of Object.entries(fieldGroups)) {
    // 年次データを時系列順にソート
    const sortedYears = Object.keys(yearlyData).sort();
    
    // 成長率と集中度を計算
    const timeSeriesData = sortedYears.map((year, index) => {
      const current = yearlyData[year];
      
      // 成長率の計算（前年比）
      let growthRate = null;
      if (index > 0) {
        const prevYear = sortedYears[index - 1];
        const previous = yearlyData[prevYear];
        growthRate = previous.count > 0 
          ? (current.count - previous.count) / previous.count 
          : null;
      }
      
      // 企業集中度（ハーフィンダール指数の簡易版）
      const companyCount = current.companies.size;
      const concentration = companyCount > 0 ? 1 / companyCount : 0;
      
      // 平均引用数
      const avgCitations = current.count > 0 ? current.citations / current.count : 0;
      
      return {
        year: parseInt(year),
        patent_count: current.count,
        company_count: companyCount,
        country_count: current.countries.size,
        growth_rate: growthRate,
        concentration: concentration,
        avg_citations: avgCitations,
        companies: Array.from(current.companies),
        countries: Array.from(current.countries)
      };
    });
    
    // 技術成熟度の評価
    // 特許出願数の変化パターンから技術のライフサイクルステージを推定
    let maturityStage = 'unknown';
    const recentYears = timeSeriesData.slice(-5);
    
    if (recentYears.length >= 3) {
      const recentGrowthRates = recentYears
        .filter(y => y.growth_rate !== null)
        .map(y => y.growth_rate);
      
      const avgRecentGrowth = recentGrowthRates.reduce((sum, rate) => sum + rate, 0) / recentGrowthRates.length;
      const latestCount = recentYears[recentYears.length - 1].patent_count;
      const maxCount = Math.max(...recentYears.map(y => y.patent_count));
      
      if (avgRecentGrowth > 0.5) {
        maturityStage = 'emerging';
      } else if (avgRecentGrowth > 0.1) {
        maturityStage = 'growth';
      } else if (avgRecentGrowth > -0.1) {
        maturityStage = 'maturity';
      } else if (latestCount < maxCount * 0.7) {
        maturityStage = 'decline';
      } else {
        maturityStage = 'stability';
      }
    }
    
    results.push({
      technology_field: field,
      maturity_stage: maturityStage,
      total_patents: timeSeriesData.reduce((sum, y) => sum + y.patent_count, 0),
      unique_companies: new Set(timeSeriesData.flatMap(y => y.companies)).size,
      unique_countries: new Set(timeSeriesData.flatMap(y => y.countries)).size,
      time_series: timeSeriesData,
      analysis_date: new Date().toISOString()
    });
  }
  
  // 特許総数でソート（降順）
  results.sort((a, b) => b.total_patents - a.total_patents);
  
  return results.map(result => ({ json: result }));
}

// メイン処理
return analyzePatentTrends($input.all());
```

このような特許出願トレンド分析ロジックを実装することで、各技術分野の特許出願動向を時系列で把握し、技術の成熟度や将来性を評価することができます。また、企業集中度や国際的な広がりなどの指標も算出することで、技術の競争環境や地理的な展開状況も分析できます。

**特許引用ネットワーク分析**:
特許間の引用関係を分析し、影響力の高い基本特許や、技術の発展経路を特定します。

```javascript
// 特許引用ネットワーク分析の実装例
function analyzePatentCitationNetwork(items) {
  // 特許データの整理
  const patents = {};
  const citations = [];
  
  // 特許データの基本情報を整理
  for (const item of items) {
    const patentId = item.json.patent_id;
    
    patents[patentId] = {
      id: patentId,
      title: item.json.title,
      applicant: item.json.applicant_name,
      filing_date: item.json.filing_date,
      technology_field: item.json.technology_field,
      country: item.json.country_code,
      in_citations: 0,
      out_citations: 0
    };
    
    // 引用関係を記録
    if (item.json.cited_patents && Array.isArray(item.json.cited_patents)) {
      for (const citedPatent of item.json.cited_patents) {
        citations.push({
          source: patentId,
          target: citedPatent,
          date: item.json.filing_date
        });
      }
      
      patents[patentId].out_citations = item.json.cited_patents.length;
    }
  }
  
  // 被引用数をカウント
  for (const citation of citations) {
    if (patents[citation.target]) {
      patents[citation.target].in_citations++;
    }
  }
  
  // 中心性指標の計算
  const patentIds = Object.keys(patents);
  
  // 次数中心性（被引用数を正規化）
  const maxInCitations = Math.max(...patentIds.map(id => patents[id].in_citations));
  for (const id of patentIds) {
    patents[id].degree_centrality = maxInCitations > 0 
      ? patents[id].in_citations / maxInCitations 
      : 0;
  }
  
  // ページランクの簡易実装（反復計算）
  const damping = 0.85;
  const iterations = 20;
  const initialScore = 1 / patentIds.length;
  
  // 初期スコアを設定
  for (const id of patentIds) {
    patents[id].pagerank = initialScore;
  }
  
  // 反復計算
  for (let i = 0; i < iterations; i++) {
    const newScores = {};
    
    for (const id of patentIds) {
      newScores[id] = (1 - damping) / patentIds.length;
    }
    
    for (const citation of citations) {
      const source = citation.source;
      const target = citation.target;
      
      if (patents[source] && patents[target]) {
        const outLinks = patents[source].out_citations;
        if (outLinks > 0) {
          newScores[target] += damping * patents[source].pagerank / outLinks;
        }
      }
    }
    
    // スコアを更新
    for (const id of patentIds) {
      patents[id].pagerank = newScores[id];
    }
  }
  
  // 結果を整形
  const results = {
    patents: Object.values(patents)
      .sort((a, b) => b.pagerank - a.pagerank)
      .map(patent => ({
        ...patent,
        influence_score: patent.pagerank * 100 // スケーリングして読みやすく
      })),
    citations: citations,
    network_stats: {
      patent_count: patentIds.length,
      citation_count: citations.length,
      density: patentIds.length > 1 
        ? citations.length / (patentIds.length * (patentIds.length - 1)) 
        : 0,
      analysis_date: new Date().toISOString()
    }
  };
  
  return [{ json: results }];
}

// メイン処理
return analyzePatentCitationNetwork($input.all());
```

このような特許引用ネットワーク分析ロジックを実装することで、特許間の引用関係を基にした影響力評価や、技術の発展経路の可視化が可能になります。特に、ページランクなどのネットワーク中心性指標を計算することで、技術分野における基本特許や重要特許を客観的に特定することができます。

**技術的実現可能性評価の実装方法**

技術的実現可能性評価は、新技術や革新的なアイデアが技術的に実現可能かどうかを、複数の観点から体系的に評価するプロセスです。この評価により、企業は技術投資や製品開発の意思決定をより確かな根拠に基づいて行うことができます。

n8nでの技術的実現可能性評価の実装方法としては、主にFunctionノードとHTTP Requestノードが活用されます。以下に、具体的な実装例を示します：

**技術成熟度評価（TRL: Technology Readiness Level）**:
NASAやEUで使用されている技術成熟度レベル（TRL）の枠組みを用いて、技術の成熟度を1（基本原理の観察）から9（実証済みシステム）までの段階で評価します。

```javascript
// 技術成熟度評価（TRL）の実装例
function assessTechnologyReadinessLevel(items) {
  // TRLの定義
  const trlDefinitions = [
    { level: 1, name: "基本原理の観察と報告", description: "科学研究から応用研究への移行。基本的な性質の観察。" },
    { level: 2, name: "技術コンセプトの形成", description: "発明の開始。コンセプトと応用が定式化される。" },
    { level: 3, name: "コンセプトの実験的証明", description: "研究開発の開始。分析的研究と実験室での研究。" },
    { level: 4, name: "研究室環境での技術実証", description: "基本的な技術要素の統合。低い信頼性での実証。" },
    { level: 5, name: "関連環境での技術実証", description: "技術要素の統合と現実的な環境での実証。" },
    { level: 6, name: "関連環境でのシステム実証", description: "システム/サブシステムモデルまたはプロトタイプの実証。" },
    { level: 7, name: "実環境でのシステム実証", description: "実際のシステムプロトタイプの実証。" },
    { level: 8, name: "実システムの完成と認定", description: "実際のシステムの完成と認定テスト。" },
    { level: 9, name: "実環境での実システムの証明", description: "実際のシステムが実環境での任務で実証される。" }
  ];
  
  // TRL評価基準（簡易版）
  const trlCriteria = {
    scientific_publications: {
      weight: 0.15,
      levels: {
        1: "基本原理に関する理論的な論文が存在する",
        2: "応用可能性に関する論文が存在する",
        3: "実験的な検証に関する論文が存在する",
        4: "プロトタイプに関する論文が存在する",
        5: "実環境に近い条件での検証に関する論文が存在する"
      }
    },
    patents: {
      weight: 0.15,
      levels: {
        2: "基本的な特許出願がある",
        3: "複数の特許出願がある",
        4: "特許が登録されている",
        5: "複数の特許ファミリーがある"
      }
    },
    prototypes: {
      weight: 0.25,
      levels: {
        3: "実験室レベルのプロトタイプがある",
        4: "機能するプロトタイプがある",
        5: "実環境に近い条件でテストされたプロトタイプがある",
        6: "完全なシステムプロトタイプがある",
        7: "実環境でテストされたプロトタイプがある"
      }
    },
    industry_adoption: {
      weight: 0.25,
      levels: {
        6: "業界パートナーによるテストが行われている",
        7: "限定的な商業利用が始まっている",
        8: "複数の商業製品に採用されている",
        9: "広範な商業利用がある"
      }
    },
    standards: {
      weight: 0.20,
      levels: {
        5: "標準化の議論が始まっている",
        6: "標準化団体での検討が進んでいる",
        7: "標準化のドラフトが公開されている",
        8: "標準規格として採用されている",
        9: "複数の標準規格に採用されている"
      }
    }
  };
  
  // 各技術のTRL評価を実施
  const results = [];
  
  for (const item of items) {
    const technology = item.json;
    const trlScores = {};
    
    // 各評価基準でスコアを計算
    for (const [criterion, config] of Object.entries(trlCriteria)) {
      let criterionLevel = 0;
      
      // 技術データから該当する最高レベルを特定
      for (const [level, description] of Object.entries(config.levels)) {
        const intLevel = parseInt(level);
        
        // 評価基準に応じた条件チェック
        let meetsCondition = false;
        
        switch (criterion) {
          case 'scientific_publications':
            meetsCondition = (technology.publication_count || 0) >= intLevel * 5;
            break;
          case 'patents':
            meetsCondition = (technology.patent_count || 0) >= intLevel * 3;
            break;
          case 'prototypes':
            meetsCondition = technology.prototype_stage && technology.prototype_stage >= intLevel;
            break;
          case 'industry_adoption':
            meetsCondition = (technology.commercial_products || 0) >= (intLevel - 5) * 2;
            break;
          case 'standards':
            meetsCondition = technology.standardization_stage && technology.standardization_stage >= intLevel - 4;
            break;
        }
        
        if (meetsCondition && intLevel > criterionLevel) {
          criterionLevel = intLevel;
        }
      }
      
      trlScores[criterion] = {
        level: criterionLevel,
        weight: config.weight,
        weighted_score: criterionLevel * config.weight
      };
    }
    
    // 総合TRLスコアの計算
    const totalWeightedScore = Object.values(trlScores).reduce((sum, score) => sum + score.weighted_score, 0);
    const totalWeight = Object.values(trlScores).reduce((sum, score) => sum + score.weight, 0);
    const weightedAvgTrl = totalWeight > 0 ? totalWeightedScore / totalWeight : 0;
    
    // 最終TRLレベルの決定（小数点以下を切り捨て）
    const finalTrl = Math.floor(weightedAvgTrl);
    const trlInfo = trlDefinitions.find(def => def.level === finalTrl) || 
                   { level: 0, name: "評価不能", description: "十分なデータがありません" };
    
    results.push({
      technology_id: technology.id,
      technology_name: technology.name,
      trl: {
        level: finalTrl,
        name: trlInfo.name,
        description: trlInfo.description,
        raw_score: weightedAvgTrl
      },
      criterion_scores: trlScores,
      assessment_date: new Date().toISOString(),
      data_confidence: calculateDataConfidence(technology)
    });
  }
  
  return results.map(result => ({ json: result }));
}

// データ信頼性の計算（補助関数）
function calculateDataConfidence(technology) {
  // データの完全性と鮮度に基づく信頼性評価
  const completeness = Object.keys(technology).length / 10; // 仮の基準
  const freshness = technology.last_updated_date 
    ? Math.max(0, 1 - (Date.now() - new Date(technology.last_updated_date).getTime()) / (365 * 24 * 60 * 60 * 1000)) 
    : 0.5;
  
  return (completeness * 0.6) + (freshness * 0.4);
}

// メイン処理
return assessTechnologyReadinessLevel($input.all());
```

このような技術成熟度評価ロジックを実装することで、各技術の成熟度を体系的かつ客観的に評価し、技術投資や製品開発の優先順位付けに役立てることができます。また、評価基準ごとのスコアを算出することで、技術の強みや弱みを特定し、重点的に強化すべき領域を明確にすることも可能です。

**技術リスク評価**:
技術の実現に関連するリスク要因（技術的課題、リソース要件、依存関係など）を特定し、その影響度と発生確率を評価します。

```javascript
// 技術リスク評価の実装例
function assessTechnologyRisks(items) {
  // リスクカテゴリの定義
  const riskCategories = [
    { id: 'technical', name: '技術的リスク', description: '技術そのものに関連するリスク' },
    { id: 'resource', name: 'リソースリスク', description: '人材、設備、資金などのリソースに関連するリスク' },
    { id: 'dependency', name: '依存関係リスク', description: '他の技術や外部要因への依存に関連するリスク' },
    { id: 'market', name: '市場リスク', description: '市場の受容性や競合に関連するリスク' },
    { id: 'regulatory', name: '規制リスク', description: '法規制や標準化に関連するリスク' }
  ];
  
  // リスク要因の定義（簡易版）
  const riskFactors = [
    { id: 'complexity', name: '技術的複雑性', category: 'technical', weight: 0.8 },
    { id: 'scalability', name: 'スケーラビリティ', category: 'technical', weight: 0.7 },
    { id: 'reliability', name: '信頼性・安定性', category: 'technical', weight: 0.9 },
    { id: 'expertise', name: '専門知識の要求度', category: 'resource', weight: 0.7 },
    { id: 'cost', name: '開発・実装コスト', category: 'resource', weight: 0.8 },
    { id: 'time', name: '開発期間', category: 'resource', weight: 0.6 },
    { id: 'external_tech', name: '外部技術への依存', category: 'dependency', weight: 0.7 },
    { id: 'supply_chain', name: 'サプライチェーンリスク', category: 'dependency', weight: 0.6 },
    { id: 'adoption', name: '市場採用障壁', category: 'market', weight: 0.7 },
    { id: 'competition', name: '競合技術の存在', category: 'market', weight: 0.6 },
    { id: 'legal', name: '法的規制', category: 'regulatory', weight: 0.8 },
    { id: 'standards', name: '標準化の不確実性', category: 'regulatory', weight: 0.7 }
  ];
  
  // 各技術のリスク評価を実施
  const results = [];
  
  for (const item of items) {
    const technology = item.json;
    const riskAssessments = {};
    
    // 各リスク要因を評価
    for (const factor of riskFactors) {
      // リスクスコアの計算（仮の計算ロジック）
      let probability = 0.5; // デフォルト値
      let impact = 0.5; // デフォルト値
      
      // 技術データに基づいてリスク確率と影響度を評価
      switch (factor.id) {
        case 'complexity':
          probability = technology.complexity_score ? technology.complexity_score / 10 : 0.5;
          impact = 0.8; // 複雑性が高いと実装が困難になる
          break;
        case 'scalability':
          probability = technology.scalability_issues ? 0.7 : 0.3;
          impact = 0.7; // スケーラビリティ問題は大規模展開時に重大
          break;
        case 'reliability':
          probability = 1 - (technology.reliability_score || 0.5);
          impact = 0.9; // 信頼性問題は製品品質に直結
          break;
        case 'expertise':
          probability = technology.expertise_level ? technology.expertise_level / 10 : 0.5;
          impact = 0.7; // 専門知識要求は人材確保の障壁に
          break;
        case 'cost':
          probability = technology.estimated_cost ? Math.min(technology.estimated_cost / 1000000, 1) : 0.5;
          impact = 0.8; // コストは予算制約に直結
          break;
        case 'time':
          probability = technology.estimated_months ? Math.min(technology.estimated_months / 36, 1) : 0.5;
          impact = 0.6; // 開発期間は市場投入タイミングに影響
          break;
        case 'external_tech':
          probability = technology.external_dependencies ? technology.external_dependencies.length / 5 : 0.3;
          impact = 0.7; // 外部依存は制御不能リスクを増加
          break;
        case 'supply_chain':
          probability = technology.rare_materials ? 0.8 : 0.2;
          impact = 0.6; // サプライチェーンリスクは調達の安定性に影響
          break;
        case 'adoption':
          probability = 1 - (technology.market_readiness || 0.5);
          impact = 0.7; // 採用障壁は市場浸透に直結
          break;
        case 'competition':
          probability = technology.competitor_count ? Math.min(technology.competitor_count / 10, 1) : 0.4;
          impact = 0.6; // 競合は差別化の難しさに影響
          break;
        case 'legal':
          probability = technology.regulatory_issues ? 0.8 : 0.3;
          impact = 0.8; // 法的問題は事業継続に重大な影響
          break;
        case 'standards':
          probability = technology.standardization_stage ? 1 - (technology.standardization_stage / 5) : 0.5;
          impact = 0.7; // 標準化の不確実性は市場受容に影響
          break;
      }
      
      // リスクスコアの計算
      const riskScore = probability * impact * factor.weight;
      
      // リスクレベルの判定
      let riskLevel;
      if (riskScore < 0.3) riskLevel = 'low';
      else if (riskScore < 0.6) riskLevel = 'medium';
      else riskLevel = 'high';
      
      riskAssessments[factor.id] = {
        factor_name: factor.name,
        category: factor.category,
        probability: probability,
        impact: impact,
        weight: factor.weight,
        risk_score: riskScore,
        risk_level: riskLevel
      };
    }
    
    // カテゴリ別のリスクスコアを集計
    const categoryScores = {};
    for (const category of riskCategories) {
      const categoryFactors = Object.values(riskAssessments).filter(a => a.category === category.id);
      const avgScore = categoryFactors.length > 0
        ? categoryFactors.reduce((sum, a) => sum + a.risk_score, 0) / categoryFactors.length
        : 0;
      
      categoryScores[category.id] = {
        category_name: category.name,
        risk_score: avgScore,
        risk_level: avgScore < 0.3 ? 'low' : avgScore < 0.6 ? 'medium' : 'high',
        factor_count: categoryFactors.length
      };
    }
    
    // 総合リスクスコアの計算
    const overallRiskScore = Object.values(riskAssessments).reduce((sum, a) => sum + a.risk_score, 0) / 
                            Object.values(riskAssessments).length;
    
    // 主要リスク要因の特定（スコアの高い上位3つ）
    const topRiskFactors = Object.entries(riskAssessments)
      .sort(([, a], [, b]) => b.risk_score - a.risk_score)
      .slice(0, 3)
      .map(([id, assessment]) => ({
        id,
        name: assessment.factor_name,
        score: assessment.risk_score,
        level: assessment.risk_level
      }));
    
    results.push({
      technology_id: technology.id,
      technology_name: technology.name,
      overall_risk: {
        score: overallRiskScore,
        level: overallRiskScore < 0.3 ? 'low' : overallRiskScore < 0.6 ? 'medium' : 'high'
      },
      category_risks: categoryScores,
      factor_assessments: riskAssessments,
      top_risk_factors: topRiskFactors,
      assessment_date: new Date().toISOString(),
      data_confidence: calculateDataConfidence(technology)
    });
  }
  
  return results.map(result => ({ json: result }));
}

// メイン処理
return assessTechnologyRisks($input.all());
```

このような技術リスク評価ロジックを実装することで、各技術の実現に関連するリスク要因を体系的に評価し、リスク管理戦略の策定に役立てることができます。また、カテゴリ別のリスク評価や主要リスク要因の特定により、重点的に対応すべきリスク領域を明確にすることも可能です。

これらのテクノロジー視点の分析実装により、コンセンサスモデルは技術トレンド、特許動向、技術的実現可能性などを多角的に評価し、技術戦略の策定や製品開発の意思決定を支援することができます。また、これらの分析結果は、マーケット視点やビジネス視点の分析と統合することで、より包括的な意思決定基盤を構築することが可能になります。
