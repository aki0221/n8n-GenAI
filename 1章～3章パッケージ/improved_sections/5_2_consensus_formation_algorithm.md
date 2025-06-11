### 5.2 コンセンサス形成アルゴリズム

コンセンサス形成アルゴリズムは、コンセンサスモデルの中核となる要素であり、異なる視点からの評価結果の間に生じる矛盾や対立を解消し、合意形成を促進するための仕組みです。このアルゴリズムにより、単なる数値的な統合を超えて、各視点の本質的な意図を尊重した意思決定が可能になります。n8nを活用することで、このコンセンサス形成プロセスを効率的かつ再現性高く実装することができます。

**矛盾検出の実装方法**

コンセンサス形成の第一歩は、異なる視点間の矛盾や対立を検出することです。これにより、単純な統合では見落とされがちな重要な判断ポイントを特定し、より深い分析や議論を促すことができます。

n8nでの矛盾検出の実装方法としては、主にFunctionノードが活用されます。以下に、具体的な実装例を示します：

**評価スコアの乖離検出**:
各視点の評価スコアの間に大きな乖離がある場合を検出し、潜在的な矛盾として特定します。

```javascript
// 評価スコアの乖離検出の実装例
function detectScoreDivergence(items) {
  // 統合データを取得
  const integratedData = items[0].json.integrated_results;
  
  // 乖離検出のパラメータ設定
  const divergenceParams = {
    threshold: 0.3, // 乖離と判断する閾値（例：0.3 = 30%の差）
    perspectives: ['technology', 'market', 'business'] // 分析対象の視点
  };
  
  // 各評価対象の視点間スコア乖離を分析
  const divergenceResults = [];
  
  for (const target of integratedData) {
    const perspectiveScores = target.perspective_scores;
    const divergences = [];
    
    // 視点ペアごとに乖離を計算
    for (let i = 0; i < divergenceParams.perspectives.length; i++) {
      const perspective1 = divergenceParams.perspectives[i];
      
      for (let j = i + 1; j < divergenceParams.perspectives.length; j++) {
        const perspective2 = divergenceParams.perspectives[j];
        
        // 両方の視点のデータが存在する場合のみ比較
        if (perspectiveScores[perspective1] && perspectiveScores[perspective2]) {
          const score1 = perspectiveScores[perspective1].score;
          const score2 = perspectiveScores[perspective2].score;
          
          // 絶対差と相対差を計算
          const absoluteDifference = Math.abs(score1 - score2);
          const relativeDifference = Math.max(score1, score2) > 0 ? 
            absoluteDifference / Math.max(score1, score2) : 0;
          
          // 閾値を超える場合は乖離として記録
          if (absoluteDifference >= divergenceParams.threshold) {
            divergences.push({
              perspective_pair: [perspective1, perspective2],
              scores: [score1, score2],
              absolute_difference: absoluteDifference,
              relative_difference: relativeDifference,
              higher_perspective: score1 > score2 ? perspective1 : perspective2,
              lower_perspective: score1 > score2 ? perspective2 : perspective1
            });
          }
        }
      }
    }
    
    // 乖離の総合評価
    const hasDivergence = divergences.length > 0;
    const maxDivergence = divergences.length > 0 ? 
      Math.max(...divergences.map(d => d.absolute_difference)) : 0;
    
    divergenceResults.push({
      target_id: target.target_id,
      target_name: target.target_name,
      overall_score: target.overall_score,
      has_divergence: hasDivergence,
      divergence_count: divergences.length,
      max_divergence: maxDivergence,
      divergence_details: divergences.sort((a, b) => b.absolute_difference - a.absolute_difference)
    });
  }
  
  // 乖離の大きい順にソート
  divergenceResults.sort((a, b) => b.max_divergence - a.max_divergence);
  
  // 結果を整形
  const result = {
    divergence_analysis: divergenceResults,
    parameters: divergenceParams,
    summary: {
      total_targets: divergenceResults.length,
      targets_with_divergence: divergenceResults.filter(r => r.has_divergence).length,
      average_divergence_count: divergenceResults.reduce((sum, r) => sum + r.divergence_count, 0) / divergenceResults.length,
      max_divergence_found: Math.max(...divergenceResults.map(r => r.max_divergence))
    },
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// メイン処理
return detectScoreDivergence($input.all());
```

このような評価スコアの乖離検出ロジックを実装することで、各視点の評価スコアの間に大きな差異がある評価対象を特定し、より詳細な分析や議論を促すことができます。これにより、単純な数値的統合では見落とされがちな重要な判断ポイントを明確にすることができます。

**評価根拠の矛盾検出**:
各視点の評価根拠（定性的なコメントや判断理由）を分析し、論理的な矛盾や対立を検出します。

```javascript
// 評価根拠の矛盾検出の実装例
function detectReasoningContradictions(items) {
  // 評価データを取得
  const evaluationData = items.map(item => item.json);
  
  // 矛盾検出のパラメータ設定
  const contradictionParams = {
    perspectives: ['technology', 'market', 'business'], // 分析対象の視点
    contradiction_keywords: {
      positive_negative: [
        { positive: ['feasible', 'viable', 'achievable', 'realistic', 'practical'], 
          negative: ['infeasible', 'unviable', 'unachievable', 'unrealistic', 'impractical'] },
        { positive: ['profitable', 'lucrative', 'cost-effective', 'economical'], 
          negative: ['unprofitable', 'costly', 'expensive', 'uneconomical'] },
        { positive: ['growing', 'expanding', 'increasing', 'rising'], 
          negative: ['shrinking', 'contracting', 'decreasing', 'declining'] },
        { positive: ['innovative', 'novel', 'unique', 'original'], 
          negative: ['conventional', 'standard', 'common', 'ordinary'] },
        { positive: ['simple', 'easy', 'straightforward'], 
          negative: ['complex', 'difficult', 'complicated'] }
      ]
    }
  };
  
  // 評価対象ごとにグループ化
  const targetGroups = {};
  for (const evaluation of evaluationData) {
    if (!targetGroups[evaluation.target_id]) {
      targetGroups[evaluation.target_id] = {
        target_id: evaluation.target_id,
        target_name: evaluation.target_name,
        perspectives: {}
      };
    }
    
    // 視点ごとの評価データを記録
    if (contradictionParams.perspectives.includes(evaluation.perspective)) {
      targetGroups[evaluation.target_id].perspectives[evaluation.perspective] = {
        score: evaluation.score,
        reasoning: evaluation.reasoning || '',
        key_points: evaluation.key_points || []
      };
    }
  }
  
  // 各評価対象の矛盾を検出
  const contradictionResults = [];
  
  for (const [targetId, targetData] of Object.entries(targetGroups)) {
    const contradictions = [];
    
    // 視点ペアごとに矛盾を検出
    for (let i = 0; i < contradictionParams.perspectives.length; i++) {
      const perspective1 = contradictionParams.perspectives[i];
      
      for (let j = i + 1; j < contradictionParams.perspectives.length; j++) {
        const perspective2 = contradictionParams.perspectives[j];
        
        // 両方の視点のデータが存在する場合のみ比較
        if (targetData.perspectives[perspective1] && targetData.perspectives[perspective2]) {
          const reasoning1 = targetData.perspectives[perspective1].reasoning.toLowerCase();
          const reasoning2 = targetData.perspectives[perspective2].reasoning.toLowerCase();
          
          // キーワードベースの矛盾検出
          const keywordContradictions = detectKeywordContradictions(
            reasoning1, reasoning2, 
            contradictionParams.contradiction_keywords.positive_negative
          );
          
          // 矛盾が検出された場合は記録
          if (keywordContradictions.length > 0) {
            contradictions.push({
              perspective_pair: [perspective1, perspective2],
              contradiction_type: 'keyword_based',
              contradiction_details: keywordContradictions,
              reasoning_1: reasoning1,
              reasoning_2: reasoning2
            });
          }
          
          // キーポイントベースの矛盾検出（同じトピックに対する異なる評価）
          const keyPoints1 = targetData.perspectives[perspective1].key_points;
          const keyPoints2 = targetData.perspectives[perspective2].key_points;
          
          if (keyPoints1 && keyPoints2 && keyPoints1.length > 0 && keyPoints2.length > 0) {
            const keyPointContradictions = detectKeyPointContradictions(keyPoints1, keyPoints2);
            
            if (keyPointContradictions.length > 0) {
              contradictions.push({
                perspective_pair: [perspective1, perspective2],
                contradiction_type: 'key_point_based',
                contradiction_details: keyPointContradictions
              });
            }
          }
        }
      }
    }
    
    // 矛盾の総合評価
    const hasContradiction = contradictions.length > 0;
    
    contradictionResults.push({
      target_id: targetId,
      target_name: targetData.target_name,
      has_contradiction: hasContradiction,
      contradiction_count: contradictions.length,
      contradiction_details: contradictions
    });
  }
  
  // 矛盾の多い順にソート
  contradictionResults.sort((a, b) => b.contradiction_count - a.contradiction_count);
  
  // 結果を整形
  const result = {
    contradiction_analysis: contradictionResults,
    parameters: contradictionParams,
    summary: {
      total_targets: contradictionResults.length,
      targets_with_contradiction: contradictionResults.filter(r => r.has_contradiction).length,
      average_contradiction_count: contradictionResults.reduce((sum, r) => sum + r.contradiction_count, 0) / contradictionResults.length
    },
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// キーワードベースの矛盾検出
function detectKeywordContradictions(text1, text2, keywordPairs) {
  const contradictions = [];
  
  for (const pair of keywordPairs) {
    const positiveKeywords = pair.positive;
    const negativeKeywords = pair.negative;
    
    // テキスト1のポジティブキーワードとテキスト2のネガティブキーワードの矛盾
    for (const positive of positiveKeywords) {
      if (text1.includes(positive)) {
        for (const negative of negativeKeywords) {
          if (text2.includes(negative)) {
            contradictions.push({
              keyword_pair: [positive, negative],
              context_1: extractContext(text1, positive),
              context_2: extractContext(text2, negative)
            });
          }
        }
      }
    }
    
    // テキスト2のポジティブキーワードとテキスト1のネガティブキーワードの矛盾
    for (const positive of positiveKeywords) {
      if (text2.includes(positive)) {
        for (const negative of negativeKeywords) {
          if (text1.includes(negative)) {
            contradictions.push({
              keyword_pair: [negative, positive],
              context_1: extractContext(text1, negative),
              context_2: extractContext(text2, positive)
            });
          }
        }
      }
    }
  }
  
  return contradictions;
}

// キーポイントベースの矛盾検出
function detectKeyPointContradictions(keyPoints1, keyPoints2) {
  const contradictions = [];
  
  for (const point1 of keyPoints1) {
    for (const point2 of keyPoints2) {
      // 同じトピックに関するキーポイントを検出
      if (point1.topic && point2.topic && point1.topic === point2.topic) {
        // 評価の方向性が異なる場合は矛盾として検出
        if ((point1.sentiment === 'positive' && point2.sentiment === 'negative') ||
            (point1.sentiment === 'negative' && point2.sentiment === 'positive')) {
          contradictions.push({
            topic: point1.topic,
            point_1: point1.point,
            sentiment_1: point1.sentiment,
            point_2: point2.point,
            sentiment_2: point2.sentiment
          });
        }
      }
    }
  }
  
  return contradictions;
}

// テキストからキーワードの前後の文脈を抽出
function extractContext(text, keyword, contextLength = 50) {
  const keywordIndex = text.indexOf(keyword);
  if (keywordIndex === -1) return '';
  
  const startIndex = Math.max(0, keywordIndex - contextLength);
  const endIndex = Math.min(text.length, keywordIndex + keyword.length + contextLength);
  
  return text.substring(startIndex, endIndex);
}

// メイン処理
return detectReasoningContradictions($input.all());
```

このような評価根拠の矛盾検出ロジックを実装することで、各視点の評価根拠（定性的なコメントや判断理由）の間にある論理的な矛盾や対立を特定し、より深い分析や議論を促すことができます。キーワードベースの矛盾検出やキーポイントベースの矛盾検出により、表面的なスコアの比較だけでは見えない本質的な対立点を明らかにすることができます。

**合意形成アルゴリズムの実装方法**

矛盾や対立を検出した後は、それらを解消し、合意形成を促進するためのアルゴリズムが必要です。このアルゴリズムにより、各視点の本質的な意図を尊重しながら、バランスの取れた意思決定を行うことができます。

n8nでの合意形成アルゴリズムの実装方法としては、主にFunctionノードが活用されます。以下に、具体的な実装例を示します：

**デルファイ法による合意形成**:
各視点の評価者に対して、他の視点からのフィードバックを提供し、評価の再考を促すことで、徐々に合意形成を図ります。

```javascript
// デルファイ法による合意形成の実装例
function delphiConsensusFormation(items) {
  // 初期評価データと矛盾検出結果を取得
  const initialEvaluations = items[0].json;
  const contradictions = items[1].json.contradiction_analysis;
  
  // デルファイ法のパラメータ設定
  const delphiParams = {
    max_rounds: 3, // 最大ラウンド数
    convergence_threshold: 0.1, // 収束と判断する閾値
    perspectives: ['technology', 'market', 'business'] // 分析対象の視点
  };
  
  // デルファイ法のシミュレーション結果
  const delphiResults = {
    rounds: [],
    final_evaluations: {},
    convergence_analysis: {}
  };
  
  // 初期ラウンドのデータを準備
  let currentRoundEvaluations = JSON.parse(JSON.stringify(initialEvaluations));
  delphiResults.rounds.push({
    round: 1,
    evaluations: currentRoundEvaluations,
    feedback: generateFeedback(currentRoundEvaluations, contradictions)
  });
  
  // デルファイ法の各ラウンドをシミュレーション
  for (let round = 2; round <= delphiParams.max_rounds; round++) {
    // 前ラウンドの評価とフィードバックに基づいて新たな評価を生成
    const newEvaluations = simulateReevaluation(
      currentRoundEvaluations, 
      delphiResults.rounds[round - 2].feedback,
      delphiParams.perspectives
    );
    
    // 新たなフィードバックを生成
    const newFeedback = generateFeedback(newEvaluations, contradictions);
    
    // ラウンド結果を記録
    delphiResults.rounds.push({
      round: round,
      evaluations: newEvaluations,
      feedback: newFeedback
    });
    
    // 収束分析
    const convergenceAnalysis = analyzeConvergence(
      delphiResults.rounds[round - 2].evaluations,
      newEvaluations,
      delphiParams.perspectives
    );
    
    // 収束したかどうかをチェック
    if (convergenceAnalysis.max_change < delphiParams.convergence_threshold) {
      delphiResults.convergence_analysis = {
        converged: true,
        converged_at_round: round,
        convergence_details: convergenceAnalysis
      };
      break;
    }
    
    // 次のラウンドの準備
    currentRoundEvaluations = newEvaluations;
    
    // 最終ラウンドの場合
    if (round === delphiParams.max_rounds) {
      delphiResults.convergence_analysis = {
        converged: false,
        max_rounds_reached: true,
        convergence_details: convergenceAnalysis
      };
    }
  }
  
  // 最終評価を設定
  delphiResults.final_evaluations = delphiResults.rounds[delphiResults.rounds.length - 1].evaluations;
  
  // 結果を整形
  const result = {
    delphi_process: delphiResults,
    parameters: delphiParams,
    summary: {
      initial_evaluations: initialEvaluations,
      final_evaluations: delphiResults.final_evaluations,
      total_rounds: delphiResults.rounds.length,
      converged: delphiResults.convergence_analysis.converged || false
    },
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// フィードバック生成
function generateFeedback(evaluations, contradictions) {
  const feedback = {};
  
  // 矛盾がある評価対象に対してフィードバックを生成
  for (const contradiction of contradictions) {
    if (contradiction.has_contradiction) {
      const targetId = contradiction.target_id;
      feedback[targetId] = {
        target_id: targetId,
        target_name: contradiction.target_name,
        perspective_feedback: {}
      };
      
      // 各矛盾に対するフィードバックを生成
      for (const detail of contradiction.contradiction_details) {
        const perspectives = detail.perspective_pair;
        
        // 各視点に対するフィードバックを生成
        for (let i = 0; i < perspectives.length; i++) {
          const currentPerspective = perspectives[i];
          const otherPerspective = perspectives[1 - i]; // ペアの他方の視点
          
          if (!feedback[targetId].perspective_feedback[currentPerspective]) {
            feedback[targetId].perspective_feedback[currentPerspective] = [];
          }
          
          // 矛盾の種類に応じたフィードバック生成
          if (detail.contradiction_type === 'keyword_based') {
            for (const keywordContradiction of detail.contradiction_details) {
              feedback[targetId].perspective_feedback[currentPerspective].push({
                from_perspective: otherPerspective,
                type: 'keyword_contradiction',
                message: `${otherPerspective} perspective uses "${keywordContradiction.keyword_pair[1 - i]}" which contradicts your "${keywordContradiction.keyword_pair[i]}"`,
                context: i === 0 ? keywordContradiction.context_2 : keywordContradiction.context_1,
                suggestion: `Consider if this contradiction affects your evaluation.`
              });
            }
          } else if (detail.contradiction_type === 'key_point_based') {
            for (const pointContradiction of detail.contradiction_details) {
              feedback[targetId].perspective_feedback[currentPerspective].push({
                from_perspective: otherPerspective,
                type: 'key_point_contradiction',
                message: `${otherPerspective} perspective has a different view on "${pointContradiction.topic}"`,
                context: i === 0 ? pointContradiction.point_2 : pointContradiction.point_1,
                suggestion: `Reconsider your evaluation of this topic in light of this different perspective.`
              });
            }
          }
        }
      }
    }
  }
  
  return feedback;
}

// 再評価のシミュレーション
function simulateReevaluation(previousEvaluations, feedback, perspectives) {
  // 深いコピーを作成
  const newEvaluations = JSON.parse(JSON.stringify(previousEvaluations));
  
  // フィードバックに基づいて評価を調整
  for (const [targetId, targetFeedback] of Object.entries(feedback)) {
    // 各視点の評価を調整
    for (const perspective of perspectives) {
      if (targetFeedback.perspective_feedback[perspective]) {
        const perspectiveFeedback = targetFeedback.perspective_feedback[perspective];
        
        // フィードバックの量と内容に基づいて調整係数を計算
        const adjustmentFactor = calculateAdjustmentFactor(perspectiveFeedback);
        
        // 評価を調整（シミュレーション）
        if (newEvaluations[targetId] && newEvaluations[targetId][perspective]) {
          const currentScore = newEvaluations[targetId][perspective].score;
          
          // スコアを調整（他の視点の平均に向けて少し移動）
          const otherPerspectivesScores = [];
          for (const otherPerspective of perspectives) {
            if (otherPerspective !== perspective && 
                newEvaluations[targetId] && 
                newEvaluations[targetId][otherPerspective]) {
              otherPerspectivesScores.push(newEvaluations[targetId][otherPerspective].score);
            }
          }
          
          if (otherPerspectivesScores.length > 0) {
            const averageOtherScore = otherPerspectivesScores.reduce((sum, score) => sum + score, 0) / otherPerspectivesScores.length;
            const scoreDifference = averageOtherScore - currentScore;
            
            // 調整係数に基づいてスコアを調整
            const adjustedScore = currentScore + (scoreDifference * adjustmentFactor);
            
            // 調整後のスコアを設定
            newEvaluations[targetId][perspective].score = adjustedScore;
            newEvaluations[targetId][perspective].adjusted = true;
            newEvaluations[targetId][perspective].adjustment_factor = adjustmentFactor;
            newEvaluations[targetId][perspective].original_score = currentScore;
          }
        }
      }
    }
  }
  
  return newEvaluations;
}

// 調整係数の計算
function calculateAdjustmentFactor(feedback) {
  // フィードバックの量と重要度に基づいて調整係数を計算
  // 実際の実装では、フィードバックの内容や説得力に基づいてより複雑な計算を行う
  
  // 簡易的な実装：フィードバックの数に基づく調整係数（0～0.5の範囲）
  const baseAdjustment = Math.min(0.5, feedback.length * 0.1);
  
  return baseAdjustment;
}

// 収束分析
function analyzeConvergence(previousEvaluations, currentEvaluations, perspectives) {
  const changes = [];
  
  // 各評価対象と視点の変化を分析
  for (const [targetId, targetData] of Object.entries(currentEvaluations)) {
    if (previousEvaluations[targetId]) {
      for (const perspective of perspectives) {
        if (targetData[perspective] && previousEvaluations[targetId][perspective]) {
          const currentScore = targetData[perspective].score;
          const previousScore = previousEvaluations[targetId][perspective].score;
          
          const absoluteChange = Math.abs(currentScore - previousScore);
          const relativeChange = previousScore !== 0 ? absoluteChange / previousScore : absoluteChange;
          
          changes.push({
            target_id: targetId,
            perspective: perspective,
            previous_score: previousScore,
            current_score: currentScore,
            absolute_change: absoluteChange,
            relative_change: relativeChange
          });
        }
      }
    }
  }
  
  // 変化の統計を計算
  const maxChange = changes.length > 0 ? Math.max(...changes.map(c => c.absolute_change)) : 0;
  const avgChange = changes.length > 0 ? changes.reduce((sum, c) => sum + c.absolute_change, 0) / changes.length : 0;
  
  return {
    changes: changes.sort((a, b) => b.absolute_change - a.absolute_change),
    max_change: maxChange,
    avg_change: avgChange,
    change_count: changes.length
  };
}

// メイン処理
return delphiConsensusFormation($input.all());
```

このようなデルファイ法による合意形成ロジックを実装することで、各視点の評価者に対して他の視点からのフィードバックを提供し、評価の再考を促すことで、徐々に合意形成を図ることができます。このプロセスを通じて、各視点の本質的な意図を尊重しながら、より包括的かつバランスの取れた評価に収束させることが可能になります。

**加重調整法による合意形成**:
矛盾や対立の度合いに応じて各視点の重みを動的に調整し、より公平でバランスの取れた統合結果を生成します。

```javascript
// 加重調整法による合意形成の実装例
function weightedAdjustmentConsensus(items) {
  // 初期評価データと矛盾検出結果を取得
  const initialEvaluations = items[0].json.integrated_results;
  const divergenceAnalysis = items[1].json.divergence_analysis;
  
  // 加重調整法のパラメータ設定
  const adjustmentParams = {
    base_weights: {
      technology: 0.33,
      market: 0.33,
      business: 0.33
    },
    max_weight_adjustment: 0.15, // 最大重み調整量
    divergence_threshold: 0.2, // 乖離と判断する閾値
    perspectives: ['technology', 'market', 'business'] // 分析対象の視点
  };
  
  // 各評価対象の重みを調整
  const adjustedResults = [];
  
  for (const target of initialEvaluations) {
    // 対応する乖離分析結果を取得
    const divergence = divergenceAnalysis.find(d => d.target_id === target.target_id);
    
    // 調整後の重みを初期化
    const adjustedWeights = { ...adjustmentParams.base_weights };
    
    // 乖離がある場合は重みを調整
    if (divergence && divergence.has_divergence) {
      // 各乖離に対して重みを調整
      for (const detail of divergence.divergence_details) {
        const perspectives = detail.perspective_pair;
        const scores = detail.scores;
        const absoluteDifference = detail.absolute_difference;
        
        // 乖離が閾値を超える場合のみ調整
        if (absoluteDifference >= adjustmentParams.divergence_threshold) {
          // 乖離の度合いに応じた調整量を計算
          const adjustmentFactor = Math.min(
            adjustmentParams.max_weight_adjustment,
            (absoluteDifference - adjustmentParams.divergence_threshold) / (1 - adjustmentParams.divergence_threshold) * adjustmentParams.max_weight_adjustment
          );
          
          // スコアの高い視点の重みを増やし、低い視点の重みを減らす
          const higherPerspective = scores[0] > scores[1] ? perspectives[0] : perspectives[1];
          const lowerPerspective = scores[0] > scores[1] ? perspectives[1] : perspectives[0];
          
          adjustedWeights[higherPerspective] += adjustmentFactor / 2;
          adjustedWeights[lowerPerspective] -= adjustmentFactor / 2;
        }
      }
      
      // 重みの合計が1になるように正規化
      const weightSum = Object.values(adjustedWeights).reduce((sum, weight) => sum + weight, 0);
      for (const perspective of adjustmentParams.perspectives) {
        adjustedWeights[perspective] = adjustedWeights[perspective] / weightSum;
      }
    }
    
    // 調整後の重みで総合スコアを再計算
    let adjustedOverallScore = 0;
    for (const perspective of adjustmentParams.perspectives) {
      if (target.perspective_scores[perspective]) {
        adjustedOverallScore += target.perspective_scores[perspective].score * adjustedWeights[perspective];
      }
    }
    
    // 結果を整形
    adjustedResults.push({
      target_id: target.target_id,
      target_name: target.target_name,
      original_overall_score: target.overall_score,
      adjusted_overall_score: adjustedOverallScore,
      original_weights: adjustmentParams.base_weights,
      adjusted_weights: adjustedWeights,
      perspective_scores: target.perspective_scores,
      has_weight_adjustment: JSON.stringify(adjustedWeights) !== JSON.stringify(adjustmentParams.base_weights)
    });
  }
  
  // 調整後のスコアでソート（降順）
  adjustedResults.sort((a, b) => b.adjusted_overall_score - a.adjusted_overall_score);
  
  // ランクを追加
  for (let i = 0; i < adjustedResults.length; i++) {
    adjustedResults[i].adjusted_rank = i + 1;
  }
  
  // 元のランクとの比較
  for (let i = 0; i < adjustedResults.length; i++) {
    const originalResult = initialEvaluations.find(r => r.target_id === adjustedResults[i].target_id);
    if (originalResult && originalResult.rank) {
      adjustedResults[i].original_rank = originalResult.rank;
      adjustedResults[i].rank_change = originalResult.rank - adjustedResults[i].adjusted_rank;
    }
  }
  
  // 結果を整形
  const result = {
    adjusted_results: adjustedResults,
    parameters: adjustmentParams,
    summary: {
      total_targets: adjustedResults.length,
      targets_with_adjustment: adjustedResults.filter(r => r.has_weight_adjustment).length,
      max_rank_change: Math.max(...adjustedResults.map(r => Math.abs(r.rank_change || 0)))
    },
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// メイン処理
return weightedAdjustmentConsensus($input.all());
```

このような加重調整法による合意形成ロジックを実装することで、矛盾や対立の度合いに応じて各視点の重みを動的に調整し、より公平でバランスの取れた統合結果を生成することができます。特に、特定の視点間で大きな乖離がある場合に、その乖離の度合いに応じて重みを調整することで、より現実的かつ合理的な意思決定を支援することができます。

**コンセンサス品質評価の実装方法**

コンセンサス形成プロセスの最終段階として、形成されたコンセンサスの品質を評価することが重要です。この評価により、コンセンサスの安定性、包括性、説得力などを客観的に判断し、必要に応じて追加の分析や議論を促すことができます。

n8nでのコンセンサス品質評価の実装方法としては、主にFunctionノードが活用されます。以下に、具体的な実装例を示します：

**コンセンサス安定性評価**:
形成されたコンセンサスの安定性を評価し、外部要因や条件の変化に対する頑健性を分析します。

```javascript
// コンセンサス安定性評価の実装例
function evaluateConsensusStability(items) {
  // コンセンサス結果を取得
  const consensusResults = items[0].json.adjusted_results;
  
  // 安定性評価のパラメータ設定
  const stabilityParams = {
    weight_variation: 0.1, // 重みの変動幅（±10%）
    score_variation: 0.05, // スコアの変動幅（±5%）
    simulation_iterations: 50, // シミュレーション回数
    perspectives: ['technology', 'market', 'business'] // 分析対象の視点
  };
  
  // 各評価対象の安定性を分析
  const stabilityResults = [];
  
  for (const target of consensusResults) {
    // モンテカルロシミュレーションによる安定性分析
    const simulationResults = simulateVariations(
      target, 
      stabilityParams.weight_variation,
      stabilityParams.score_variation,
      stabilityParams.simulation_iterations,
      stabilityParams.perspectives
    );
    
    // スコアの変動範囲を計算
    const scores = simulationResults.map(r => r.overall_score);
    const minScore = Math.min(...scores);
    const maxScore = Math.max(...scores);
    const avgScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    const stdDev = Math.sqrt(scores.reduce((sum, score) => sum + Math.pow(score - avgScore, 2), 0) / scores.length);
    
    // ランクの変動範囲を計算
    const ranks = simulationResults.map(r => r.rank);
    const minRank = Math.min(...ranks);
    const maxRank = Math.max(...ranks);
    const rankRange = maxRank - minRank;
    
    // 安定性スコアの計算（標準偏差とランク範囲に基づく）
    const scoreStability = 1 - (stdDev / avgScore);
    const rankStability = 1 - (rankRange / consensusResults.length);
    const overallStability = (scoreStability + rankStability) / 2;
    
    // 安定性の評価
    let stabilityRating;
    if (overallStability >= 0.9) stabilityRating = 'Very High';
    else if (overallStability >= 0.8) stabilityRating = 'High';
    else if (overallStability >= 0.6) stabilityRating = 'Moderate';
    else if (overallStability >= 0.4) stabilityRating = 'Low';
    else stabilityRating = 'Very Low';
    
    stabilityResults.push({
      target_id: target.target_id,
      target_name: target.target_name,
      consensus_score: target.adjusted_overall_score,
      consensus_rank: target.adjusted_rank,
      score_stability: {
        min_score: minScore,
        max_score: maxScore,
        avg_score: avgScore,
        std_dev: stdDev,
        stability_score: scoreStability
      },
      rank_stability: {
        min_rank: minRank,
        max_rank: maxRank,
        rank_range: rankRange,
        stability_score: rankStability
      },
      overall_stability: overallStability,
      stability_rating: stabilityRating,
      simulation_count: simulationResults.length
    });
  }
  
  // 安定性の低い順にソート
  stabilityResults.sort((a, b) => a.overall_stability - b.overall_stability);
  
  // 結果を整形
  const result = {
    stability_analysis: stabilityResults,
    parameters: stabilityParams,
    summary: {
      total_targets: stabilityResults.length,
      avg_stability: stabilityResults.reduce((sum, r) => sum + r.overall_stability, 0) / stabilityResults.length,
      targets_by_stability: {
        very_high: stabilityResults.filter(r => r.stability_rating === 'Very High').length,
        high: stabilityResults.filter(r => r.stability_rating === 'High').length,
        moderate: stabilityResults.filter(r => r.stability_rating === 'Moderate').length,
        low: stabilityResults.filter(r => r.stability_rating === 'Low').length,
        very_low: stabilityResults.filter(r => r.stability_rating === 'Very Low').length
      }
    },
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// バリエーションのシミュレーション
function simulateVariations(target, weightVariation, scoreVariation, iterations, perspectives) {
  const simulationResults = [];
  
  for (let i = 0; i < iterations; i++) {
    // 深いコピーを作成
    const simulation = JSON.parse(JSON.stringify(target));
    
    // 重みとスコアをランダムに変動
    const adjustedWeights = {};
    let totalWeight = 0;
    
    for (const perspective of perspectives) {
      if (simulation.adjusted_weights[perspective]) {
        // 重みをランダムに変動
        const weightDelta = (Math.random() * 2 - 1) * weightVariation;
        adjustedWeights[perspective] = Math.max(0, simulation.adjusted_weights[perspective] + weightDelta);
        totalWeight += adjustedWeights[perspective];
      }
    }
    
    // 重みの合計が1になるように正規化
    for (const perspective of perspectives) {
      if (adjustedWeights[perspective]) {
        adjustedWeights[perspective] = adjustedWeights[perspective] / totalWeight;
      }
    }
    
    // 各視点のスコアをランダムに変動
    const adjustedScores = {};
    for (const perspective of perspectives) {
      if (simulation.perspective_scores[perspective]) {
        // スコアをランダムに変動
        const scoreDelta = (Math.random() * 2 - 1) * scoreVariation;
        adjustedScores[perspective] = Math.max(0, Math.min(1, simulation.perspective_scores[perspective].score + scoreDelta));
      }
    }
    
    // 総合スコアを再計算
    let overallScore = 0;
    for (const perspective of perspectives) {
      if (adjustedWeights[perspective] && adjustedScores[perspective]) {
        overallScore += adjustedScores[perspective] * adjustedWeights[perspective];
      }
    }
    
    simulationResults.push({
      iteration: i + 1,
      overall_score: overallScore,
      adjusted_weights: adjustedWeights,
      adjusted_scores: adjustedScores
    });
  }
  
  // 全シミュレーション結果をスコアでソート
  simulationResults.sort((a, b) => b.overall_score - a.overall_score);
  
  // ランクを追加
  for (let i = 0; i < simulationResults.length; i++) {
    simulationResults[i].rank = i + 1;
  }
  
  return simulationResults;
}

// メイン処理
return evaluateConsensusStability($input.all());
```

このようなコンセンサス安定性評価ロジックを実装することで、形成されたコンセンサスの安定性を評価し、外部要因や条件の変化に対する頑健性を分析することができます。モンテカルロシミュレーションを用いることで、重みやスコアの小さな変動がコンセンサス結果にどの程度影響を与えるかを定量的に評価し、安定性の高い意思決定と不安定な意思決定を区別することができます。

**コンセンサス包括性評価**:
形成されたコンセンサスが各視点の本質的な意図をどの程度反映しているかを評価し、包括性や公平性を分析します。

```javascript
// コンセンサス包括性評価の実装例
function evaluateConsensusInclusiveness(items) {
  // コンセンサス結果と初期評価を取得
  const consensusResults = items[0].json.adjusted_results;
  const initialEvaluations = items[1].json.integrated_results;
  
  // 包括性評価のパラメータ設定
  const inclusivenessParams = {
    perspectives: ['technology', 'market', 'business'], // 分析対象の視点
    min_representation_threshold: 0.7, // 最小表現閾値（70%）
    perspective_importance: {
      technology: 1.0,
      market: 1.0,
      business: 1.0
    }
  };
  
  // 各評価対象の包括性を分析
  const inclusivenessResults = [];
  
  for (const consensus of consensusResults) {
    // 対応する初期評価を取得
    const initial = initialEvaluations.find(e => e.target_id === consensus.target_id);
    
    if (initial) {
      // 各視点の表現度を計算
      const representationScores = {};
      let totalRepresentation = 0;
      let weightedTotalRepresentation = 0;
      let totalWeight = 0;
      
      for (const perspective of inclusivenessParams.perspectives) {
        if (initial.perspective_scores[perspective] && consensus.perspective_scores[perspective]) {
          // 初期評価と最終コンセンサスのスコア
          const initialScore = initial.perspective_scores[perspective].score;
          const consensusScore = consensus.perspective_scores[perspective].score;
          
          // 視点の重要度
          const importance = inclusivenessParams.perspective_importance[perspective] || 1.0;
          
          // 表現度の計算（コンセンサススコアが初期スコアをどれだけ反映しているか）
          // 1に近いほど完全に反映、0に近いほど全く反映していない
          const representation = 1 - Math.abs(consensusScore - initialScore);
          
          representationScores[perspective] = {
            initial_score: initialScore,
            consensus_score: consensusScore,
            representation: representation,
            importance: importance,
            weighted_representation: representation * importance
          };
          
          totalRepresentation += representation;
          weightedTotalRepresentation += representation * importance;
          totalWeight += importance;
        }
      }
      
      // 平均表現度の計算
      const avgRepresentation = Object.keys(representationScores).length > 0 ? 
        totalRepresentation / Object.keys(representationScores).length : 0;
      
      // 重み付き平均表現度の計算
      const weightedAvgRepresentation = totalWeight > 0 ? 
        weightedTotalRepresentation / totalWeight : 0;
      
      // 最小表現度の計算
      const minRepresentation = Object.values(representationScores).length > 0 ? 
        Math.min(...Object.values(representationScores).map(s => s.representation)) : 0;
      
      // 包括性スコアの計算（重み付き平均表現度と最小表現度の組み合わせ）
      const inclusivenessScore = (weightedAvgRepresentation * 0.7) + (minRepresentation * 0.3);
      
      // 包括性の評価
      let inclusivenessRating;
      if (inclusivenessScore >= 0.9) inclusivenessRating = 'Excellent';
      else if (inclusivenessScore >= 0.8) inclusivenessRating = 'Good';
      else if (inclusivenessScore >= 0.7) inclusivenessRating = 'Satisfactory';
      else if (inclusivenessScore >= 0.5) inclusivenessRating = 'Marginal';
      else inclusivenessRating = 'Poor';
      
      // 十分に表現されていない視点の特定
      const underrepresentedPerspectives = Object.entries(representationScores)
        .filter(([, score]) => score.representation < inclusivenessParams.min_representation_threshold)
        .map(([perspective, score]) => ({
          perspective: perspective,
          representation: score.representation,
          initial_score: score.initial_score,
          consensus_score: score.consensus_score
        }));
      
      inclusivenessResults.push({
        target_id: consensus.target_id,
        target_name: consensus.target_name,
        consensus_score: consensus.adjusted_overall_score,
        consensus_rank: consensus.adjusted_rank,
        perspective_representation: representationScores,
        avg_representation: avgRepresentation,
        weighted_avg_representation: weightedAvgRepresentation,
        min_representation: minRepresentation,
        inclusiveness_score: inclusivenessScore,
        inclusiveness_rating: inclusivenessRating,
        underrepresented_perspectives: underrepresentedPerspectives,
        has_underrepresented_perspectives: underrepresentedPerspectives.length > 0
      });
    }
  }
  
  // 包括性の低い順にソート
  inclusivenessResults.sort((a, b) => a.inclusiveness_score - b.inclusiveness_score);
  
  // 結果を整形
  const result = {
    inclusiveness_analysis: inclusivenessResults,
    parameters: inclusivenessParams,
    summary: {
      total_targets: inclusivenessResults.length,
      avg_inclusiveness: inclusivenessResults.reduce((sum, r) => sum + r.inclusiveness_score, 0) / inclusivenessResults.length,
      targets_by_inclusiveness: {
        excellent: inclusivenessResults.filter(r => r.inclusiveness_rating === 'Excellent').length,
        good: inclusivenessResults.filter(r => r.inclusiveness_rating === 'Good').length,
        satisfactory: inclusivenessResults.filter(r => r.inclusiveness_rating === 'Satisfactory').length,
        marginal: inclusivenessResults.filter(r => r.inclusiveness_rating === 'Marginal').length,
        poor: inclusivenessResults.filter(r => r.inclusiveness_rating === 'Poor').length
      },
      targets_with_underrepresented_perspectives: inclusivenessResults.filter(r => r.has_underrepresented_perspectives).length
    },
    analysis_date: new Date().toISOString()
  };
  
  return [{ json: result }];
}

// メイン処理
return evaluateConsensusInclusiveness($input.all());
```

このようなコンセンサス包括性評価ロジックを実装することで、形成されたコンセンサスが各視点の本質的な意図をどの程度反映しているかを評価し、包括性や公平性を分析することができます。特に、十分に表現されていない視点を特定することで、追加の分析や議論が必要な領域を明確にし、より包括的なコンセンサス形成を促すことができます。

これらのコンセンサス形成アルゴリズムの実装により、コンセンサスモデルは異なる視点からの評価結果の間に生じる矛盾や対立を効果的に解消し、各視点の本質的な意図を尊重したバランスの取れた意思決定を支援することができます。また、形成されたコンセンサスの品質評価により、意思決定の安定性や包括性を客観的に判断し、より信頼性の高い意思決定プロセスを実現することが可能になります。
