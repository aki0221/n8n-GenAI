### 5.1 視点間の統合プロセス

コンセンサスモデルの核心部分である視点間の統合プロセスは、テクノロジー視点、マーケット視点、ビジネス視点から得られた分析結果を統合し、包括的かつバランスの取れた意思決定基盤を構築するための重要なコンポーネントです。この統合プロセスにより、技術的な実現可能性、市場の受容性、事業的な持続可能性のすべてを考慮した戦略的判断が可能になります。n8nを活用することで、この複雑な統合プロセスを効率的かつ再現性高く実装することができます。

**データ正規化と重み付けの実装方法**

視点間の統合を行う前に、各視点から得られたデータを正規化し、適切な重み付けを行うことが重要です。これにより、異なるスケールや単位で表現されたデータを比較可能な形式に変換し、各視点の重要度に応じた評価を行うことができます。

n8nでのデータ正規化と重み付けの実装方法としては、主にFunctionノードが活用されます。以下に、具体的な実装例を示します：

**スコア正規化の実装**:
各視点から得られた評価スコアを0～1の範囲に正規化し、比較可能な形式に変換します。

```javascript
// スコア正規化の実装例
function normalizeScores(items) {
  // 各視点のデータを整理
  const perspectiveData = {
    technology: items.filter(item => item.json.perspective === 'technology').map(item => item.json),
    market: items.filter(item => item.json.perspective === 'market').map(item => item.json),
    business: items.filter(item => item.json.perspective === 'business').map(item => item.json)
  };
  
  // 正規化関数（Min-Max正規化）
  function minMaxNormalize(value, min, max) {
    if (max === min) return 0.5; // 全て同じ値の場合
    return (value - min) / (max - min);
  }
  
  // 各視点のスコアを正規化
  const normalizedData = {};
  
  for (const [perspective, data] of Object.entries(perspectiveData)) {
    normalizedData[perspective] = [];
    
    // 評価対象（例：製品、プロジェクト、技術など）ごとにグループ化
    const targetGroups = {};
    for (const item of data) {
      if (!targetGroups[item.target_id]) {
        targetGroups[item.target_id] = [];
      }
      targetGroups[item.target_id].push(item);
    }
    
    // 各評価対象のスコアを正規化
    for (const [targetId, items] of Object.entries(targetGroups)) {
      // 評価指標ごとにグループ化
      const metricGroups = {};
      for (const item of items) {
        if (!metricGroups[item.metric_id]) {
          metricGroups[item.metric_id] = [];
        }
        metricGroups[item.metric_id].push(item);
      }
      
      // 各評価指標のスコアを正規化
      const normalizedItems = [];
      for (const [metricId, metricItems] of Object.entries(metricGroups)) {
        // 最小値と最大値を取得
        const values = metricItems.map(item => item.score);
        const min = Math.min(...values);
        const max = Math.max(...values);
        
        // 各アイテムのスコアを正規化
        for (const item of metricItems) {
          const normalizedItem = {
            ...item,
            original_score: item.score,
            normalized_score: minMaxNormalize(item.score, min, max)
          };
          normalizedItems.push(normalizedItem);
        }
      }
      
      normalizedData[perspective].push({
        target_id: targetId,
        target_name: items[0].target_name,
        items: normalizedItems
      });
    }
  }
  
  return [{ json: normalizedData }];
}

// メイン処理
return normalizeScores($input.all());
```

このようなスコア正規化ロジックを実装することで、各視点から得られた評価スコアを0～1の範囲に変換し、異なる指標間での比較を可能にします。これにより、視点間の統合時に公平な評価が行えるようになります。

**重み付け設定の実装**:
各視点や評価指標に対して、その重要度に応じた重みを設定し、総合評価に反映させます。

```javascript
// 重み付け設定の実装例
function applyWeights(items) {
  // 入力データを取得
  const normalizedData = items[0].json;
  
  // 視点ごとの重み設定（例）
  const perspectiveWeights = {
    technology: 0.35, // テクノロジー視点の重み
    market: 0.35,     // マーケット視点の重み
    business: 0.3     // ビジネス視点の重み
  };
  
  // 各視点内の評価指標の重み設定（例）
  const metricWeights = {
    technology: {
      technical_feasibility: 0.3,
      innovation_level: 0.2,
      technology_maturity: 0.2,
      implementation_complexity: 0.15,
      scalability: 0.15
    },
    market: {
      market_size: 0.25,
      growth_potential: 0.25,
      competition_intensity: 0.2,
      customer_needs_alignment: 0.3
    },
    business: {
      revenue_potential: 0.3,
      profitability: 0.25,
      strategic_alignment: 0.25,
      resource_requirements: 0.2
    }
  };
  
  // 重み付けを適用
  const weightedData = {};
  
  for (const [perspective, targets] of Object.entries(normalizedData)) {
    weightedData[perspective] = [];
    
    for (const target of targets) {
      const weightedItems = [];
      let perspectiveScore = 0;
      let totalMetricWeight = 0;
      
      // 各評価指標に重みを適用
      for (const item of target.items) {
        const metricId = item.metric_id;
        const metricWeight = metricWeights[perspective][metricId] || 0.1; // デフォルト重み
        
        const weightedItem = {
          ...item,
          metric_weight: metricWeight,
          weighted_score: item.normalized_score * metricWeight
        };
        
        weightedItems.push(weightedItem);
        perspectiveScore += weightedItem.weighted_score;
        totalMetricWeight += metricWeight;
      }
      
      // 視点全体のスコアを計算（正規化）
      const normalizedPerspectiveScore = totalMetricWeight > 0 ? perspectiveScore / totalMetricWeight : 0;
      
      weightedData[perspective].push({
        target_id: target.target_id,
        target_name: target.target_name,
        items: weightedItems,
        perspective_score: normalizedPerspectiveScore,
        perspective_weight: perspectiveWeights[perspective]
      });
    }
  }
  
  return [{ json: weightedData }];
}

// メイン処理
return applyWeights($input.all());
```

このような重み付け設定ロジックを実装することで、各視点や評価指標の重要度に応じた重みを設定し、より現実的かつ戦略的な評価を行うことができます。また、状況や目的に応じて重みを調整することで、柔軟な意思決定支援が可能になります。

**統合アルゴリズムの実装方法**

視点間の統合アルゴリズムは、正規化・重み付けされた各視点のデータを統合し、総合的な評価結果を生成するプロセスです。この統合により、技術的、市場的、事業的な観点をバランスよく考慮した意思決定が可能になります。

n8nでの統合アルゴリズムの実装方法としては、主にFunctionノードが活用されます。以下に、具体的な実装例を示します：

**加重平均法による統合**:
各視点のスコアに重みを掛けて合計し、総合評価スコアを算出します。

```javascript
// 加重平均法による統合の実装例
function integrateByWeightedAverage(items) {
  // 重み付けされたデータを取得
  const weightedData = items[0].json;
  
  // 評価対象ごとに視点間の統合を行う
  const integratedResults = [];
  
  // 評価対象のIDリストを取得
  const targetIds = new Set();
  for (const perspective of Object.values(weightedData)) {
    for (const target of perspective) {
      targetIds.add(target.target_id);
    }
  }
  
  // 各評価対象について統合処理
  for (const targetId of targetIds) {
    // 各視点のデータを取得
    const targetData = {};
    let targetName = '';
    
    for (const [perspective, targets] of Object.entries(weightedData)) {
      const target = targets.find(t => t.target_id === targetId);
      if (target) {
        targetData[perspective] = target;
        targetName = target.target_name; // 名前を記録
      }
    }
    
    // 総合スコアの計算（加重平均）
    let totalWeightedScore = 0;
    let totalWeight = 0;
    
    for (const [perspective, target] of Object.entries(targetData)) {
      totalWeightedScore += target.perspective_score * target.perspective_weight;
      totalWeight += target.perspective_weight;
    }
    
    const overallScore = totalWeight > 0 ? totalWeightedScore / totalWeight : 0;
    
    // 視点別の詳細スコアを整理
    const perspectiveScores = {};
    for (const [perspective, target] of Object.entries(targetData)) {
      perspectiveScores[perspective] = {
        score: target.perspective_score,
        weight: target.perspective_weight,
        weighted_score: target.perspective_score * target.perspective_weight,
        metrics: target.items.map(item => ({
          metric_id: item.metric_id,
          metric_name: item.metric_name,
          original_score: item.original_score,
          normalized_score: item.normalized_score,
          weight: item.metric_weight,
          weighted_score: item.weighted_score
        }))
      };
    }
    
    // 結果を整形
    integratedResults.push({
      target_id: targetId,
      target_name: targetName,
      overall_score: overallScore,
      perspective_scores: perspectiveScores,
      integration_method: 'weighted_average',
      integration_date: new Date().toISOString()
    });
  }
  
  // 総合スコアでソート（降順）
  integratedResults.sort((a, b) => b.overall_score - a.overall_score);
  
  return [{ json: { integrated_results: integratedResults } }];
}

// メイン処理
return integrateByWeightedAverage($input.all());
```

このような加重平均法による統合ロジックを実装することで、各視点のスコアを重み付けして合計し、総合的な評価結果を得ることができます。これにより、複数の視点をバランスよく考慮した意思決定が可能になります。

**多基準意思決定法（MCDM）による統合**:
AHP（階層分析法）やTOPSIS（理想解からの類似性による優先順位付け技法）などの多基準意思決定法を用いて、より洗練された統合を行います。

```javascript
// TOPSISによる統合の実装例
function integrateByTOPSIS(items) {
  // 重み付けされたデータを取得
  const weightedData = items[0].json;
  
  // 評価対象のIDリストを取得
  const targetIds = new Set();
  for (const perspective of Object.values(weightedData)) {
    for (const target of perspective) {
      targetIds.add(target.target_id);
    }
  }
  
  // 各視点をTOPSISの基準として扱う
  const criteria = Object.keys(weightedData);
  const criteriaWeights = {};
  for (const perspective of criteria) {
    criteriaWeights[perspective] = weightedData[perspective][0]?.perspective_weight || 0.33;
  }
  
  // 決定行列の構築
  const decisionMatrix = [];
  const targetNames = {};
  
  for (const targetId of targetIds) {
    const row = { target_id: targetId };
    
    for (const perspective of criteria) {
      const target = weightedData[perspective].find(t => t.target_id === targetId);
      if (target) {
        row[perspective] = target.perspective_score;
        targetNames[targetId] = target.target_name;
      } else {
        row[perspective] = 0; // データがない場合は0とする
      }
    }
    
    decisionMatrix.push(row);
  }
  
  // TOPSIS法による計算
  const topsisResults = calculateTOPSIS(decisionMatrix, criteriaWeights);
  
  // 結果を整形
  const integratedResults = topsisResults.map(result => {
    // 各視点の詳細スコアを取得
    const perspectiveScores = {};
    for (const perspective of criteria) {
      const target = weightedData[perspective].find(t => t.target_id === result.target_id);
      if (target) {
        perspectiveScores[perspective] = {
          score: target.perspective_score,
          weight: target.perspective_weight,
          metrics: target.items.map(item => ({
            metric_id: item.metric_id,
            metric_name: item.metric_name,
            original_score: item.original_score,
            normalized_score: item.normalized_score,
            weight: item.metric_weight,
            weighted_score: item.weighted_score
          }))
        };
      }
    }
    
    return {
      target_id: result.target_id,
      target_name: targetNames[result.target_id],
      overall_score: result.topsis_score,
      rank: result.rank,
      perspective_scores: perspectiveScores,
      positive_ideal_distance: result.positive_ideal_distance,
      negative_ideal_distance: result.negative_ideal_distance,
      integration_method: 'topsis',
      integration_date: new Date().toISOString()
    };
  });
  
  return [{ json: { integrated_results: integratedResults } }];
}

// TOPSIS法の計算
function calculateTOPSIS(decisionMatrix, criteriaWeights) {
  const criteria = Object.keys(criteriaWeights);
  
  // ステップ1: 決定行列の正規化
  const normalizedMatrix = [];
  
  for (const row of decisionMatrix) {
    const normalizedRow = { target_id: row.target_id };
    
    for (const criterion of criteria) {
      // 各基準の二乗和の平方根を計算
      const sumOfSquares = decisionMatrix.reduce((sum, r) => sum + Math.pow(r[criterion], 2), 0);
      const normalizingFactor = Math.sqrt(sumOfSquares);
      
      normalizedRow[criterion] = normalizingFactor > 0 ? row[criterion] / normalizingFactor : 0;
    }
    
    normalizedMatrix.push(normalizedRow);
  }
  
  // ステップ2: 重み付け正規化行列の作成
  const weightedNormalizedMatrix = [];
  
  for (const row of normalizedMatrix) {
    const weightedRow = { target_id: row.target_id };
    
    for (const criterion of criteria) {
      weightedRow[criterion] = row[criterion] * criteriaWeights[criterion];
    }
    
    weightedNormalizedMatrix.push(weightedRow);
  }
  
  // ステップ3: 理想解と負の理想解の特定
  const idealSolution = {};
  const negativeIdealSolution = {};
  
  for (const criterion of criteria) {
    const values = weightedNormalizedMatrix.map(row => row[criterion]);
    idealSolution[criterion] = Math.max(...values);
    negativeIdealSolution[criterion] = Math.min(...values);
  }
  
  // ステップ4: 理想解と負の理想解からの距離を計算
  const distances = [];
  
  for (const row of weightedNormalizedMatrix) {
    let positiveIdealDistance = 0;
    let negativeIdealDistance = 0;
    
    for (const criterion of criteria) {
      positiveIdealDistance += Math.pow(row[criterion] - idealSolution[criterion], 2);
      negativeIdealDistance += Math.pow(row[criterion] - negativeIdealSolution[criterion], 2);
    }
    
    positiveIdealDistance = Math.sqrt(positiveIdealDistance);
    negativeIdealDistance = Math.sqrt(negativeIdealDistance);
    
    distances.push({
      target_id: row.target_id,
      positive_ideal_distance: positiveIdealDistance,
      negative_ideal_distance: negativeIdealDistance
    });
  }
  
  // ステップ5: 理想解への相対的近さ（TOPSISスコア）の計算
  const topsisScores = distances.map(distance => {
    const denominator = distance.positive_ideal_distance + distance.negative_ideal_distance;
    const topsisScore = denominator > 0 ? distance.negative_ideal_distance / denominator : 0;
    
    return {
      target_id: distance.target_id,
      positive_ideal_distance: distance.positive_ideal_distance,
      negative_ideal_distance: distance.negative_ideal_distance,
      topsis_score: topsisScore
    };
  });
  
  // スコアでソートしてランク付け
  topsisScores.sort((a, b) => b.topsis_score - a.topsis_score);
  
  for (let i = 0; i < topsisScores.length; i++) {
    topsisScores[i].rank = i + 1;
  }
  
  return topsisScores;
}

// メイン処理
return integrateByTOPSIS($input.all());
```

このようなTOPSISによる統合ロジックを実装することで、各評価対象の理想解からの距離に基づいた総合評価を行うことができます。TOPSISは複数の基準（この場合は視点）間のトレードオフを考慮した意思決定を支援する手法であり、より洗練された統合結果を得ることができます。

**感度分析の実装方法**

感度分析は、重みや評価値の変動が最終的な統合結果にどの程度影響を与えるかを分析するプロセスです。この分析により、統合結果の安定性や信頼性を評価し、重要なパラメータを特定することができます。

n8nでの感度分析の実装方法としては、主にFunctionノードが活用されます。以下に、具体的な実装例を示します：

**重み変動の感度分析**:
各視点や評価指標の重みを変動させ、統合結果への影響を分析します。

```javascript
// 重み変動の感度分析の実装例
function analyzeSensitivityToWeights(items) {
  // 基本データを取得
  const baseData = items[0].json;
  const baseResults = baseData.integrated_results;
  
  // 感度分析のパラメータ設定
  const sensitivityParams = {
    weight_variation: 0.1, // 重みの変動幅（±10%）
    perspectives: ['technology', 'market', 'business'] // 分析対象の視点
  };
  
  // 各視点の重みを変動させた場合の結果を計算
  const sensitivityResults = {};
  
  for (const perspective of sensitivityParams.perspectives) {
    // 重みを増加させた場合
    const increasedWeightResults = recalculateWithModifiedWeight(baseData, perspective, sensitivityParams.weight_variation);
    
    // 重みを減少させた場合
    const decreasedWeightResults = recalculateWithModifiedWeight(baseData, perspective, -sensitivityParams.weight_variation);
    
    // 結果の変化を分析
    const increasedChanges = analyzeResultChanges(baseResults, increasedWeightResults);
    const decreasedChanges = analyzeResultChanges(baseResults, decreasedWeightResults);
    
    sensitivityResults[perspective] = {
      weight_increase: {
        variation: `+${sensitivityParams.weight_variation * 100}%`,
        results: increasedWeightResults,
        changes: increasedChanges
      },
      weight_decrease: {
        variation: `-${sensitivityParams.weight_variation * 100}%`,
        results: decreasedWeightResults,
        changes: decreasedChanges
      }
    };
  }
  
  // 感度スコアの計算（各視点の重要度を評価）
  const sensitivityScores = calculateSensitivityScores(sensitivityResults);
  
  // 結果を整形
  const result = {
    base_results: baseResults,
    sensitivity_analysis: sensitivityResults,
    sensitivity_scores: sensitivityScores,
    parameters: sensitivityParams,
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// 重みを変更して再計算
function recalculateWithModifiedWeight(baseData, targetPerspective, weightVariation) {
  // 深いコピーを作成
  const modifiedData = JSON.parse(JSON.stringify(baseData));
  const results = modifiedData.integrated_results;
  
  // 各評価対象の重みを変更
  for (const result of results) {
    if (result.perspective_scores[targetPerspective]) {
      const originalWeight = result.perspective_scores[targetPerspective].weight;
      const newWeight = Math.max(0, Math.min(1, originalWeight + weightVariation));
      
      // 重みを更新
      result.perspective_scores[targetPerspective].weight = newWeight;
      
      // 総合スコアを再計算
      let totalWeightedScore = 0;
      let totalWeight = 0;
      
      for (const [perspective, data] of Object.entries(result.perspective_scores)) {
        totalWeightedScore += data.score * data.weight;
        totalWeight += data.weight;
      }
      
      result.overall_score = totalWeight > 0 ? totalWeightedScore / totalWeight : 0;
    }
  }
  
  // スコアでソート
  results.sort((a, b) => b.overall_score - a.overall_score);
  
  // ランクを更新
  for (let i = 0; i < results.length; i++) {
    results[i].rank = i + 1;
  }
  
  return results;
}

// 結果の変化を分析
function analyzeResultChanges(baseResults, modifiedResults) {
  const changes = {
    score_changes: [],
    rank_changes: [],
    average_absolute_score_change: 0,
    max_absolute_score_change: 0,
    average_absolute_rank_change: 0,
    max_absolute_rank_change: 0
  };
  
  // 各評価対象の変化を計算
  for (const baseResult of baseResults) {
    const modifiedResult = modifiedResults.find(r => r.target_id === baseResult.target_id);
    
    if (modifiedResult) {
      const scoreChange = modifiedResult.overall_score - baseResult.overall_score;
      const rankChange = (baseResult.rank || 0) - (modifiedResult.rank || 0);
      
      changes.score_changes.push({
        target_id: baseResult.target_id,
        target_name: baseResult.target_name,
        base_score: baseResult.overall_score,
        modified_score: modifiedResult.overall_score,
        absolute_change: Math.abs(scoreChange),
        relative_change: scoreChange
      });
      
      changes.rank_changes.push({
        target_id: baseResult.target_id,
        target_name: baseResult.target_name,
        base_rank: baseResult.rank || 0,
        modified_rank: modifiedResult.rank || 0,
        absolute_change: Math.abs(rankChange),
        relative_change: rankChange
      });
    }
  }
  
  // 変化の統計を計算
  if (changes.score_changes.length > 0) {
    changes.average_absolute_score_change = changes.score_changes.reduce((sum, change) => sum + change.absolute_change, 0) / changes.score_changes.length;
    changes.max_absolute_score_change = Math.max(...changes.score_changes.map(change => change.absolute_change));
  }
  
  if (changes.rank_changes.length > 0) {
    changes.average_absolute_rank_change = changes.rank_changes.reduce((sum, change) => sum + change.absolute_change, 0) / changes.rank_changes.length;
    changes.max_absolute_rank_change = Math.max(...changes.rank_changes.map(change => change.absolute_change));
  }
  
  // 変化の大きい順にソート
  changes.score_changes.sort((a, b) => b.absolute_change - a.absolute_change);
  changes.rank_changes.sort((a, b) => b.absolute_change - a.absolute_change);
  
  return changes;
}

// 感度スコアの計算
function calculateSensitivityScores(sensitivityResults) {
  const scores = {};
  
  for (const [perspective, results] of Object.entries(sensitivityResults)) {
    const increaseImpact = results.weight_increase.changes.average_absolute_score_change;
    const decreaseImpact = results.weight_decrease.changes.average_absolute_score_change;
    
    // 平均影響度を計算
    const averageImpact = (increaseImpact + decreaseImpact) / 2;
    
    scores[perspective] = {
      sensitivity_score: averageImpact,
      increase_impact: increaseImpact,
      decrease_impact: decreaseImpact
    };
  }
  
  // 感度スコアでソート（降順）
  const sortedScores = Object.entries(scores)
    .sort(([, a], [, b]) => b.sensitivity_score - a.sensitivity_score)
    .reduce((obj, [key, value]) => {
      obj[key] = value;
      return obj;
    }, {});
  
  return sortedScores;
}

// メイン処理
return analyzeSensitivityToWeights($input.all());
```

このような重み変動の感度分析ロジックを実装することで、各視点の重みを変動させた場合の統合結果への影響を分析し、重要な視点や不安定な評価対象を特定することができます。これにより、より堅牢な意思決定や、重点的に検討すべき領域の特定が可能になります。

**モンテカルロシミュレーションによる感度分析**:
評価値や重みをランダムに変動させる多数のシミュレーションを実行し、統合結果の確率分布や信頼区間を分析します。

```javascript
// モンテカルロシミュレーションによる感度分析の実装例
function monteCarloSensitivityAnalysis(items) {
  // 基本データを取得
  const baseData = items[0].json;
  const baseResults = baseData.integrated_results;
  
  // シミュレーションのパラメータ設定
  const simulationParams = {
    iterations: 100, // シミュレーション回数
    weight_variation_range: 0.1, // 重みの変動範囲（±10%）
    score_variation_range: 0.05 // スコアの変動範囲（±5%）
  };
  
  // シミュレーション結果を格納する配列
  const simulationResults = [];
  
  // モンテカルロシミュレーションの実行
  for (let i = 0; i < simulationParams.iterations; i++) {
    // 重みとスコアをランダムに変動させたデータを生成
    const simulatedData = generateSimulatedData(baseData, simulationParams);
    
    // 統合結果を再計算
    const simulatedResults = recalculateIntegratedResults(simulatedData);
    
    simulationResults.push(simulatedResults);
  }
  
  // シミュレーション結果の統計分析
  const statisticalAnalysis = analyzeSimulationResults(baseResults, simulationResults);
  
  // 結果を整形
  const result = {
    base_results: baseResults,
    simulation_parameters: simulationParams,
    statistical_analysis: statisticalAnalysis,
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// シミュレーションデータの生成
function generateSimulatedData(baseData, params) {
  // 深いコピーを作成
  const simulatedData = JSON.parse(JSON.stringify(baseData));
  
  // 各評価対象のデータを変動させる
  for (const result of simulatedData.integrated_results) {
    // 各視点のデータを変動
    for (const [perspective, data] of Object.entries(result.perspective_scores)) {
      // 重みを変動
      const weightVariation = (Math.random() * 2 - 1) * params.weight_variation_range;
      data.weight = Math.max(0, Math.min(1, data.weight + weightVariation));
      
      // スコアを変動
      const scoreVariation = (Math.random() * 2 - 1) * params.score_variation_range;
      data.score = Math.max(0, Math.min(1, data.score + scoreVariation));
      
      // 各メトリクスのスコアも変動
      if (data.metrics) {
        for (const metric of data.metrics) {
          const metricScoreVariation = (Math.random() * 2 - 1) * params.score_variation_range;
          metric.normalized_score = Math.max(0, Math.min(1, metric.normalized_score + metricScoreVariation));
          metric.weighted_score = metric.normalized_score * metric.weight;
        }
      }
    }
  }
  
  return simulatedData;
}

// 統合結果の再計算
function recalculateIntegratedResults(simulatedData) {
  const results = [];
  
  for (const baseResult of simulatedData.integrated_results) {
    // 総合スコアを再計算
    let totalWeightedScore = 0;
    let totalWeight = 0;
    
    for (const [perspective, data] of Object.entries(baseResult.perspective_scores)) {
      totalWeightedScore += data.score * data.weight;
      totalWeight += data.weight;
    }
    
    const overallScore = totalWeight > 0 ? totalWeightedScore / totalWeight : 0;
    
    results.push({
      target_id: baseResult.target_id,
      target_name: baseResult.target_name,
      overall_score: overallScore
    });
  }
  
  // スコアでソート
  results.sort((a, b) => b.overall_score - a.overall_score);
  
  // ランクを追加
  for (let i = 0; i < results.length; i++) {
    results[i].rank = i + 1;
  }
  
  return results;
}

// シミュレーション結果の統計分析
function analyzeSimulationResults(baseResults, simulationResults) {
  const analysis = {
    target_statistics: {},
    rank_probability: {},
    top_rank_probability: {}
  };
  
  // 各評価対象の統計を計算
  for (const baseResult of baseResults) {
    const targetId = baseResult.target_id;
    const scores = [];
    const ranks = [];
    
    // 全シミュレーションから当該評価対象のデータを収集
    for (const simulation of simulationResults) {
      const result = simulation.find(r => r.target_id === targetId);
      if (result) {
        scores.push(result.overall_score);
        ranks.push(result.rank);
      }
    }
    
    // スコアの統計
    const scoreStats = calculateStatistics(scores);
    
    // ランクの統計
    const rankStats = calculateStatistics(ranks);
    
    // ランク分布の計算
    const rankDistribution = {};
    for (const rank of ranks) {
      rankDistribution[rank] = (rankDistribution[rank] || 0) + 1;
    }
    
    // 各ランクの確率を計算
    const rankProbability = {};
    for (const [rank, count] of Object.entries(rankDistribution)) {
      rankProbability[rank] = count / ranks.length;
    }
    
    // 結果を格納
    analysis.target_statistics[targetId] = {
      target_name: baseResult.target_name,
      base_score: baseResult.overall_score,
      base_rank: baseResult.rank,
      score_statistics: scoreStats,
      rank_statistics: rankStats,
      rank_probability: rankProbability
    };
    
    // 全体のランク確率マトリックスを更新
    for (const [rank, probability] of Object.entries(rankProbability)) {
      if (!analysis.rank_probability[rank]) {
        analysis.rank_probability[rank] = {};
      }
      analysis.rank_probability[rank][targetId] = probability;
    }
  }
  
  // トップランク（1位）になる確率を計算
  for (const targetId of Object.keys(analysis.target_statistics)) {
    analysis.top_rank_probability[targetId] = analysis.target_statistics[targetId].rank_probability['1'] || 0;
  }
  
  // トップランク確率でソート（降順）
  analysis.top_rank_probability = Object.entries(analysis.top_rank_probability)
    .sort(([, a], [, b]) => b - a)
    .reduce((obj, [key, value]) => {
      obj[key] = value;
      return obj;
    }, {});
  
  return analysis;
}

// 統計値の計算
function calculateStatistics(values) {
  if (values.length === 0) return null;
  
  // 平均
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  
  // 分散と標準偏差
  const variance = values.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / values.length;
  const stdDev = Math.sqrt(variance);
  
  // 最小値と最大値
  const min = Math.min(...values);
  const max = Math.max(...values);
  
  // 中央値
  const sortedValues = [...values].sort((a, b) => a - b);
  const median = sortedValues.length % 2 === 0
    ? (sortedValues[sortedValues.length / 2 - 1] + sortedValues[sortedValues.length / 2]) / 2
    : sortedValues[Math.floor(sortedValues.length / 2)];
  
  // 95%信頼区間（正規分布を仮定）
  const confidenceInterval95 = {
    lower: mean - 1.96 * stdDev / Math.sqrt(values.length),
    upper: mean + 1.96 * stdDev / Math.sqrt(values.length)
  };
  
  return {
    count: values.length,
    mean: mean,
    median: median,
    min: min,
    max: max,
    std_dev: stdDev,
    variance: variance,
    confidence_interval_95: confidenceInterval95
  };
}

// メイン処理
return monteCarloSensitivityAnalysis($input.all());
```

このようなモンテカルロシミュレーションによる感度分析ロジックを実装することで、評価値や重みの不確実性を考慮した統合結果の確率分布や信頼区間を分析し、より堅牢な意思決定を支援することができます。特に、各評価対象がトップランクになる確率や、ランクの変動範囲などの情報は、リスクを考慮した意思決定に役立ちます。

これらの視点間の統合プロセスの実装により、コンセンサスモデルはテクノロジー視点、マーケット視点、ビジネス視点から得られた分析結果を効果的に統合し、包括的かつバランスの取れた意思決定基盤を提供することができます。また、感度分析により、統合結果の安定性や信頼性を評価し、より堅牢な意思決定を支援することも可能になります。
