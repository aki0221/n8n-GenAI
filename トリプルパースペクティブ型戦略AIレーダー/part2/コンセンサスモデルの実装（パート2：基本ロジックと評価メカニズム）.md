# コンセンサスモデルの実装（パート2：基本ロジックと評価メカニズム）

## コンセンサスモデルの基本ロジック

コンセンサスモデルの基本ロジックは、3つの視点（テクノロジー、マーケット、ビジネス）からの情報を評価・統合し、最適な解釈と判断を導き出すプロセスです。このセクションでは、n8nを活用したコンセンサスモデルの基本ロジックの実装方法について解説します。

### 視点別評価プロセス

各視点（テクノロジー、マーケット、ビジネス）からの情報は、まず個別に評価されます。この評価プロセスをn8nで実装する方法を示します。

```javascript
// n8n workflow: Perspective Evaluation Process
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "evaluate-perspective",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getPerspectiveData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get perspective data from webhook payload
        const perspectiveData = $input.item.json;
        
        // Validate required fields
        const requiredFields = ['perspective_id', 'topic_id', 'date', 'change_points', 'analysis_results'];
        for (const field of requiredFields) {
          if (!perspectiveData[field]) {
            throw new Error(\`Missing required field: \${field}\`);
          }
        }
        
        return {json: perspectiveData};
      `
    }
  },
  {
    "id": "getConsensusParameters",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get active consensus parameters
        SELECT parameters
        FROM consensus_parameters
        WHERE is_active = TRUE
        ORDER BY created_at DESC
        LIMIT 1
      `
    }
  },
  {
    "id": "evaluatePerspective",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const perspectiveData = $input.item.json;
        const consensusParameters = $input.item.json.parameters;
        
        // Extract perspective information
        const perspectiveId = perspectiveData.perspective_id;
        const topicId = perspectiveData.topic_id;
        const date = perspectiveData.date;
        const changePoints = perspectiveData.change_points;
        const analysisResults = perspectiveData.analysis_results;
        
        // Get evaluation parameters based on perspective
        const importanceParams = consensusParameters.importanceParameters;
        const confidenceParams = consensusParameters.confidenceParameters;
        
        // Evaluate importance
        const importanceEvaluation = evaluateImportance(changePoints, analysisResults, importanceParams);
        
        // Evaluate confidence
        const confidenceEvaluation = evaluateConfidence(changePoints, analysisResults, confidenceParams);
        
        // Combine evaluations
        const perspectiveEvaluation = {
          perspective_id: perspectiveId,
          topic_id: topicId,
          date: date,
          importance: importanceEvaluation,
          confidence: confidenceEvaluation,
          overall_score: calculateOverallScore(importanceEvaluation, confidenceEvaluation)
        };
        
        return {json: {
          perspective_data: perspectiveData,
          perspective_evaluation: perspectiveEvaluation,
          consensus_parameters: consensusParameters
        }};
        
        // Helper function: Evaluate importance
        function evaluateImportance(changePoints, analysisResults, params) {
          // Calculate impact scope score
          const impactScopeScore = calculateImpactScope(changePoints, analysisResults);
          
          // Calculate change magnitude score
          const changeMagnitudeScore = calculateChangeMagnitude(changePoints);
          
          // Calculate strategic relevance score
          const strategicRelevanceScore = calculateStrategicRelevance(analysisResults);
          
          // Calculate time urgency score
          const timeUrgencyScore = calculateTimeUrgency(changePoints, analysisResults);
          
          // Calculate weighted importance score
          const importanceScore = 
            params.impactScope.weight * impactScopeScore +
            params.changeMagnitude.weight * changeMagnitudeScore +
            params.strategicRelevance.weight * strategicRelevanceScore +
            params.timeUrgency.weight * timeUrgencyScore;
          
          // Determine importance level
          let importanceLevel;
          if (importanceScore >= params.strategicRelevance.thresholds.high) {
            importanceLevel = 'high';
          } else if (importanceScore >= params.strategicRelevance.thresholds.medium) {
            importanceLevel = 'medium';
          } else {
            importanceLevel = 'low';
          }
          
          return {
            score: importanceScore,
            level: importanceLevel,
            components: {
              impact_scope: impactScopeScore,
              change_magnitude: changeMagnitudeScore,
              strategic_relevance: strategicRelevanceScore,
              time_urgency: timeUrgencyScore
            }
          };
        }
        
        // Helper function: Calculate impact scope
        function calculateImpactScope(changePoints, analysisResults) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          let impactScore = 0;
          
          // Consider the number of affected entities
          const affectedEntities = new Set();
          for (const cp of changePoints) {
            if (cp.entities) {
              for (const entity of cp.entities) {
                affectedEntities.add(entity);
              }
            }
          }
          
          // Normalize score based on number of affected entities
          const entityCount = affectedEntities.size;
          if (entityCount > 10) {
            impactScore = 1.0;
          } else if (entityCount > 5) {
            impactScore = 0.7;
          } else if (entityCount > 2) {
            impactScore = 0.4;
          } else {
            impactScore = 0.2;
          }
          
          return impactScore;
        }
        
        // Helper function: Calculate change magnitude
        function calculateChangeMagnitude(changePoints) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          let totalMagnitude = 0;
          let count = 0;
          
          for (const cp of changePoints) {
            if (cp.change_magnitude !== undefined) {
              totalMagnitude += cp.change_magnitude;
              count++;
            }
          }
          
          return count > 0 ? totalMagnitude / count : 0;
        }
        
        // Helper function: Calculate strategic relevance
        function calculateStrategicRelevance(analysisResults) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          if (analysisResults.strategic_relevance !== undefined) {
            return analysisResults.strategic_relevance;
          }
          
          // Default calculation based on keywords
          let relevanceScore = 0;
          const strategicKeywords = ['戦略', '重要', '優先', '必須', '競争', '差別化', '成長', '革新'];
          
          if (analysisResults.summary) {
            let matchCount = 0;
            for (const keyword of strategicKeywords) {
              if (analysisResults.summary.includes(keyword)) {
                matchCount++;
              }
            }
            relevanceScore = Math.min(1.0, matchCount / 4);
          }
          
          return relevanceScore;
        }
        
        // Helper function: Calculate time urgency
        function calculateTimeUrgency(changePoints, analysisResults) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          if (analysisResults.time_urgency !== undefined) {
            return analysisResults.time_urgency;
          }
          
          // Default calculation based on change point timing
          let urgencyScore = 0;
          const now = new Date();
          
          for (const cp of changePoints) {
            if (cp.date) {
              const changeDate = new Date(cp.date);
              const daysDiff = Math.abs((now - changeDate) / (1000 * 60 * 60 * 24));
              
              // More recent changes have higher urgency
              if (daysDiff < 7) {
                urgencyScore = Math.max(urgencyScore, 1.0);
              } else if (daysDiff < 30) {
                urgencyScore = Math.max(urgencyScore, 0.7);
              } else if (daysDiff < 90) {
                urgencyScore = Math.max(urgencyScore, 0.4);
              } else {
                urgencyScore = Math.max(urgencyScore, 0.2);
              }
            }
          }
          
          return urgencyScore;
        }
        
        // Helper function: Evaluate confidence
        function evaluateConfidence(changePoints, analysisResults, params) {
          // Calculate source reliability score
          const sourceReliabilityScore = calculateSourceReliability(analysisResults);
          
          // Calculate data volume score
          const dataVolumeScore = calculateDataVolume(changePoints, analysisResults);
          
          // Calculate consistency score
          const consistencyScore = calculateConsistency(changePoints);
          
          // Calculate verifiability score
          const verifiabilityScore = calculateVerifiability(analysisResults);
          
          // Calculate weighted confidence score
          const confidenceScore = 
            params.sourceReliability.weight * sourceReliabilityScore +
            params.dataVolume.weight * dataVolumeScore +
            params.consistency.weight * consistencyScore +
            params.verifiability.weight * verifiabilityScore;
          
          // Determine confidence level
          let confidenceLevel;
          if (confidenceScore >= params.sourceReliability.thresholds.high) {
            confidenceLevel = 'high';
          } else if (confidenceScore >= params.sourceReliability.thresholds.medium) {
            confidenceLevel = 'medium';
          } else {
            confidenceLevel = 'low';
          }
          
          return {
            score: confidenceScore,
            level: confidenceLevel,
            components: {
              source_reliability: sourceReliabilityScore,
              data_volume: dataVolumeScore,
              consistency: consistencyScore,
              verifiability: verifiabilityScore
            }
          };
        }
        
        // Helper function: Calculate source reliability
        function calculateSourceReliability(analysisResults) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          if (analysisResults.source_reliability !== undefined) {
            return analysisResults.source_reliability;
          }
          
          // Default calculation based on source types
          let reliabilityScore = 0;
          
          if (analysisResults.sources) {
            const sourceTypes = {
              academic: 1.0,
              government: 0.9,
              industry_report: 0.8,
              news_major: 0.7,
              news_tech: 0.6,
              blog_expert: 0.5,
              social_media: 0.3,
              forum: 0.2,
              unknown: 0.1
            };
            
            let totalWeight = 0;
            let weightedSum = 0;
            
            for (const source of analysisResults.sources) {
              const type = source.type || 'unknown';
              const weight = source.weight || 1;
              
              weightedSum += (sourceTypes[type] || 0.1) * weight;
              totalWeight += weight;
            }
            
            reliabilityScore = totalWeight > 0 ? weightedSum / totalWeight : 0;
          }
          
          return reliabilityScore;
        }
        
        // Helper function: Calculate data volume
        function calculateDataVolume(changePoints, analysisResults) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          const dataPoints = (analysisResults.data_points || 0);
          const sourceCount = (analysisResults.sources || []).length;
          
          // Normalize based on data points and sources
          let volumeScore = 0;
          
          if (dataPoints > 100 || sourceCount > 20) {
            volumeScore = 1.0;
          } else if (dataPoints > 50 || sourceCount > 10) {
            volumeScore = 0.8;
          } else if (dataPoints > 20 || sourceCount > 5) {
            volumeScore = 0.6;
          } else if (dataPoints > 10 || sourceCount > 2) {
            volumeScore = 0.4;
          } else {
            volumeScore = 0.2;
          }
          
          return volumeScore;
        }
        
        // Helper function: Calculate consistency
        function calculateConsistency(changePoints) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          if (changePoints.length <= 1) {
            return 0.5; // Neutral score for single data point
          }
          
          // Check consistency across change points
          let consistencyScore = 0;
          let consistentCount = 0;
          let totalComparisons = 0;
          
          for (let i = 0; i < changePoints.length; i++) {
            for (let j = i + 1; j < changePoints.length; j++) {
              // Compare direction of change
              if (changePoints[i].direction && changePoints[j].direction) {
                if (changePoints[i].direction === changePoints[j].direction) {
                  consistentCount++;
                }
                totalComparisons++;
              }
            }
          }
          
          consistencyScore = totalComparisons > 0 ? consistentCount / totalComparisons : 0.5;
          return consistencyScore;
        }
        
        // Helper function: Calculate verifiability
        function calculateVerifiability(analysisResults) {
          // Implementation depends on the specific data structure
          // This is a simplified example
          if (analysisResults.verifiability !== undefined) {
            return analysisResults.verifiability;
          }
          
          // Default calculation based on evidence types
          let verifiabilityScore = 0;
          
          const evidenceTypes = {
            quantitative_data: 1.0,
            official_statement: 0.9,
            direct_observation: 0.8,
            expert_opinion: 0.7,
            multiple_sources: 0.6,
            single_source: 0.4,
            anecdotal: 0.2,
            speculation: 0.1
          };
          
          if (analysisResults.evidence_types) {
            let totalWeight = 0;
            let weightedSum = 0;
            
            for (const evidence of analysisResults.evidence_types) {
              const type = evidence.type || 'speculation';
              const weight = evidence.weight || 1;
              
              weightedSum += (evidenceTypes[type] || 0.1) * weight;
              totalWeight += weight;
            }
            
            verifiabilityScore = totalWeight > 0 ? weightedSum / totalWeight : 0;
          } else {
            // Default moderate score if no evidence types specified
            verifiabilityScore = 0.5;
          }
          
          return verifiabilityScore;
        }
        
        // Helper function: Calculate overall score
        function calculateOverallScore(importance, confidence) {
          // Combine importance and confidence scores
          // This is a simplified approach - can be customized based on requirements
          return (importance.score * 0.6) + (confidence.score * 0.4);
        }
      `
    }
  },
  {
    "id": "savePerspectiveEvaluation",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create perspective_evaluations table if not exists
        CREATE TABLE IF NOT EXISTS perspective_evaluations (
          id SERIAL PRIMARY KEY,
          perspective_id VARCHAR(50) NOT NULL,
          topic_id VARCHAR(50) NOT NULL,
          date DATE NOT NULL,
          importance JSONB NOT NULL,
          confidence JSONB NOT NULL,
          overall_score FLOAT NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          
          CONSTRAINT unique_perspective_topic_date UNIQUE (perspective_id, topic_id, date)
        );
        
        -- Insert or update perspective evaluation
        INSERT INTO perspective_evaluations (
          perspective_id,
          topic_id,
          date,
          importance,
          confidence,
          overall_score
        )
        VALUES (
          '{{ $json.perspective_evaluation.perspective_id }}',
          '{{ $json.perspective_evaluation.topic_id }}',
          '{{ $json.perspective_evaluation.date }}',
          '{{ $json.perspective_evaluation.importance | json | replace("'", "''") }}'::jsonb,
          '{{ $json.perspective_evaluation.confidence | json | replace("'", "''") }}'::jsonb,
          {{ $json.perspective_evaluation.overall_score }}
        )
        ON CONFLICT (perspective_id, topic_id, date)
        DO UPDATE SET
          importance = '{{ $json.perspective_evaluation.importance | json | replace("'", "''") }}'::jsonb,
          confidence = '{{ $json.perspective_evaluation.confidence | json | replace("'", "''") }}'::jsonb,
          overall_score = {{ $json.perspective_evaluation.overall_score }},
          created_at = CURRENT_TIMESTAMP;
      `
    }
  },
  {
    "id": "triggerCoherenceEvaluation",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/check-coherence",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.perspective_evaluation.topic_id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.perspective_evaluation.date }}"
          }
        ]
      }
    }
  }
]
```

このワークフローでは、各視点からの情報を評価し、重要度と確信度のスコアを算出しています。評価結果はデータベースに保存され、次のステップである整合性評価のトリガーとなります。

### 整合性評価プロセス

異なる視点からの評価結果の整合性を評価するプロセスをn8nで実装します。

```javascript
// n8n workflow: Coherence Evaluation Process
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "check-coherence",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getPerspectiveEvaluations",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get perspective evaluations for the topic and date
        SELECT
          perspective_id,
          topic_id,
          date,
          importance,
          confidence,
          overall_score
        FROM
          perspective_evaluations
        WHERE
          topic_id = '{{ $json.topic_id }}'
          AND date = '{{ $json.date }}'
      `
    }
  },
  {
    "id": "getConsensusParameters",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Get active consensus parameters
        SELECT parameters
        FROM consensus_parameters
        WHERE is_active = TRUE
        ORDER BY created_at DESC
        LIMIT 1
      `
    }
  },
  {
    "id": "evaluateCoherence",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const perspectiveEvaluations = $input.item.json;
        const consensusParameters = $input.item.json.parameters;
        
        // Check if we have evaluations from all three perspectives
        const perspectives = ['technology', 'market', 'business'];
        const evaluations = {};
        let missingPerspectives = [];
        
        for (const perspective of perspectives) {
          const evaluation = perspectiveEvaluations.find(e => e.perspective_id === perspective);
          if (evaluation) {
            evaluations[perspective] = evaluation;
          } else {
            missingPerspectives.push(perspective);
          }
        }
        
        // If any perspective is missing, we can't evaluate coherence yet
        if (missingPerspectives.length > 0) {
          return {
            json: {
              status: 'incomplete',
              topic_id: $json.topic_id,
              date: $json.date,
              missing_perspectives: missingPerspectives
            }
          };
        }
        
        // Get coherence parameters
        const coherenceParams = consensusParameters.coherenceParameters;
        
        // Evaluate coherence
        const coherenceEvaluation = evaluateCoherence(evaluations, coherenceParams);
        
        return {
          json: {
            status: 'complete',
            topic_id: $json.topic_id,
            date: $json.date,
            perspective_evaluations: evaluations,
            coherence_evaluation: coherenceEvaluation,
            consensus_parameters: consensusParameters
          }
        };
        
        // Helper function: Evaluate coherence
        function evaluateCoherence(evaluations, params) {
          // Calculate perspective agreement score
          const perspectiveAgreementScore = calculatePerspectiveAgreement(evaluations);
          
          // Calculate logical coherence score
          const logicalCoherenceScore = calculateLogicalCoherence(evaluations);
          
          // Calculate temporal coherence score
          const temporalCoherenceScore = calculateTemporalCoherence(evaluations);
          
          // Calculate contextual coherence score
          const contextualCoherenceScore = calculateContextualCoherence(evaluations);
          
          // Calculate weighted coherence score
          const coherenceScore = 
            params.perspectiveAgreement.weight * perspectiveAgreementScore +
            params.logicalCoherence.weight * logicalCoherenceScore +
            params.temporalCoherence.weight * temporalCoherenceScore +
            params.contextualCoherence.weight * contextualCoherenceScore;
          
          // Determine coherence level
          let coherenceLevel;
          if (coherenceScore >= params.perspectiveAgreement.thresholds.high) {
            coherenceLevel = 'high';
          } else if (coherenceScore >= params.perspectiveAgreement.thresholds.medium) {
            coherenceLevel = 'medium';
          } else {
            coherenceLevel = 'low';
          }
          
          return {
            score: coherenceScore,
            level: coherenceLevel,
            components: {
              perspective_agreement: perspectiveAgreementScore,
              logical_coherence: logicalCoherenceScore,
              temporal_coherence: temporalCoherenceScore,
              contextual_coherence: contextualCoherenceScore
            }
          };
        }
        
        // Helper function: Calculate perspective agreement
        function calculatePerspectiveAgreement(evaluations) {
          // Calculate agreement between perspectives based on overall scores
          const tech = evaluations.technology.overall_score;
          const market = evaluations.market.overall_score;
          const business = evaluations.business.overall_score;
          
          // Calculate pairwise differences
          const techMarketDiff = Math.abs(tech - market);
          const techBusinessDiff = Math.abs(tech - business);
          const marketBusinessDiff = Math.abs(market - business);
          
          // Average difference (normalized to 0-1 scale)
          const avgDiff = (techMarketDiff + techBusinessDiff + marketBusinessDiff) / 3;
          
          // Convert to agreement score (1 - difference)
          return Math.max(0, 1 - avgDiff);
        }
        
        // Helper function: Calculate logical coherence
        function calculateLogicalCoherence(evaluations) {
          // Check for logical contradictions in importance and confidence
          const tech = evaluations.technology;
          const market = evaluations.market;
          const business = evaluations.business;
          
          // Check for high importance but low confidence scenarios
          let contradictions = 0;
          
          if (tech.importance.level === 'high' && tech.confidence.level === 'low') contradictions++;
          if (market.importance.level === 'high' && market.confidence.level === 'low') contradictions++;
          if (business.importance.level === 'high' && business.confidence.level === 'low') contradictions++;
          
          // Check for major disagreements in importance
          if (tech.importance.level === 'high' && market.importance.level === 'low') contradictions++;
          if (tech.importance.level === 'high' && business.importance.level === 'low') contradictions++;
          if (market.importance.level === 'high' && tech.importance.level === 'low') contradictions++;
          if (market.importance.level === 'high' && business.importance.level === 'low') contradictions++;
          if (business.importance.level === 'high' && tech.importance.level === 'low') contradictions++;
          if (business.importance.level === 'high' && market.importance.level === 'low') contradictions++;
          
          // Normalize to 0-1 scale (0 contradictions = 1.0 score, 9 contradictions = 0.0 score)
          return Math.max(0, 1 - (contradictions / 9));
        }
        
        // Helper function: Calculate temporal coherence
        function calculateTemporalCoherence(evaluations) {
          // This would typically involve comparing with historical evaluations
          // For simplicity, we'll return a default value
          return 0.8;
        }
        
        // Helper function: Calculate contextual coherence
        function calculateContextualCoherence(evaluations) {
          // This would typically involve comparing with broader context
          // For simplicity, we'll return a default value
          return 0.7;
        }
      `
    }
  },
  {
    "id": "saveCoherenceEvaluation",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": [
        {
          "value1": "={{ $json.status }}",
          "operation": "equal",
          "value2": "complete"
        }
      ]
    }
  },
  {
    "id": "saveCoherenceEvaluationTrue",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        -- Create coherence_evaluations table if not exists
        CREATE TABLE IF NOT EXISTS coherence_evaluations (
          id SERIAL PRIMARY KEY,
          topic_id VARCHAR(50) NOT NULL,
          date DATE NOT NULL,
          coherence JSONB NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          
          CONSTRAINT unique_topic_date UNIQUE (topic_id, date)
        );
        
        -- Insert or update coherence evaluation
        INSERT INTO coherence_evaluations (
          topic_id,
          date,
          coherence
        )
        VALUES (
          '{{ $json.topic_id }}',
          '{{ $json.date }}',
          '{{ $json.coherence_evaluation | json | replace("'", "''") }}'::jsonb
        )
        ON CONFLICT (topic_id, date)
        DO UPDATE SET
          coherence = '{{ $json.coherence_evaluation | json | replace("'", "''") }}'::jsonb,
          created_at = CURRENT_TIMESTAMP;
      `
    }
  },
  {
    "id": "triggerConsensusIntegration",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/integrate-consensus",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "topic_id",
            "value": "={{ $json.topic_id }}"
          },
          {
            "name": "date",
            "value": "={{ $json.date }}"
          }
        ]
      }
    }
  }
]
```

このワークフローでは、3つの視点からの評価結果の整合性を評価し、整合性スコアを算出しています。評価結果はデータベースに保存され、次のステップであるコンセンサス統合のトリガーとなります。

## 評価メカニズムの詳細

コンセンサスモデルの評価メカニズムは、重要度評価、確信度評価、整合性評価の3つの主要コンポーネントから構成されます。各コンポーネントの詳細について解説します。

### 重要度評価

重要度評価は、検出された変化や情報の重要性を評価するメカニズムです。重要度は以下の4つの要素から算出されます：

1. **影響範囲（Impact Scope）**
   - 変化が影響を与える範囲の広さを評価
   - 影響を受けるエンティティ（企業、技術、市場セグメントなど）の数と重要性を考慮
   - 広範囲に影響を与える変化ほど高スコア

2. **変化の大きさ（Change Magnitude）**
   - 変化の量的・質的な大きさを評価
   - 変化前後の状態の差異の程度を測定
   - 大きな変化ほど高スコア

3. **戦略的関連性（Strategic Relevance）**
   - 組織の戦略目標との関連性を評価
   - 戦略的キーワードや重要トピックとの関連性を分析
   - 戦略的に重要な変化ほど高スコア

4. **時間的緊急性（Time Urgency）**
   - 対応の緊急性を評価
   - 変化の発生時期と対応必要時期を考慮
   - 緊急性の高い変化ほど高スコア

これらの要素は、設定された重みに基づいて統合され、総合的な重要度スコアが算出されます。

### 確信度評価

確信度評価は、情報や分析結果の信頼性を評価するメカニズムです。確信度は以下の4つの要素から算出されます：

1. **情報源の信頼性（Source Reliability）**
   - 情報源の権威性や過去の正確性を評価
   - 学術機関、政府機関、業界レポートなどの信頼性の高い情報源ほど高スコア
   - 情報源のタイプと評判を考慮

2. **データ量（Data Volume）**
   - 分析に使用されたデータの量を評価
   - データポイント数、情報源数、時間範囲などを考慮
   - データ量が多いほど高スコア

3. **一貫性（Consistency）**
   - 複数の情報源や時点での一貫性を評価
   - 情報間の矛盾や不一致を検出
   - 一貫性が高いほど高スコア

4. **検証可能性（Verifiability）**
   - 情報が独立に検証可能かどうかを評価
   - 定量的データ、公式声明、直接観察などの検証可能な情報ほど高スコア
   - 証拠のタイプと質を考慮

これらの要素は、設定された重みに基づいて統合され、総合的な確信度スコアが算出されます。

### 整合性評価

整合性評価は、異なる視点からの情報の整合性を評価するメカニズムです。整合性は以下の4つの要素から算出されます：

1. **視点間の一致度（Perspective Agreement）**
   - 異なる視点からの評価の一致度を評価
   - テクノロジー、マーケット、ビジネスの3視点間の評価の差異を測定
   - 一致度が高いほど高スコア

2. **論理的整合性（Logical Coherence）**
   - 情報間の論理的な矛盾の有無を評価
   - 重要度と確信度の関係、視点間の論理的整合性を分析
   - 論理的矛盾が少ないほど高スコア

3. **時間的整合性（Temporal Coherence）**
   - 時系列での整合性を評価
   - 過去の評価との一貫性、時間経過に伴う変化の合理性を分析
   - 時間的に一貫した変化ほど高スコア

4. **コンテキスト整合性（Contextual Coherence）**
   - より広いコンテキストとの整合性を評価
   - 業界動向、マクロ環境、関連トピックとの整合性を分析
   - コンテキストと整合した情報ほど高スコア

これらの要素は、設定された重みに基づいて統合され、総合的な整合性スコアが算出されます。

## 評価結果の統合

重要度評価、確信度評価、整合性評価の結果は、コンセンサスモデルの次のステップである視点統合と静止点検出のための入力となります。次のセクションでは、これらの評価結果を統合し、最適な解釈と判断を導き出すプロセスについて解説します。
