# 予測モデルの実装と統合（パート2-5：n8nによるモデル統合ワークフロー）

## モデル統合ワークフローの概要

トリプルパースペクティブ型戦略AIレーダーにおける予測エンジンでは、時系列予測モデル、機械学習モデル、深層学習モデル、アンサンブル手法など、様々な予測モデルを統合して運用する必要があります。n8nは、これらの異なるモデルを効率的に統合し、オーケストレーションするための強力なプラットフォームを提供します。本セクションでは、n8nを使用したモデル統合ワークフローの実装について詳細に解説します。

### モデル統合の基本概念

モデル統合ワークフローは、以下の主要コンポーネントで構成されます：

1. **データ収集と前処理**: 様々なソースからデータを収集し、予測モデルに適した形式に変換
2. **モデル選択と実行**: 適切なモデルを選択し、予測を実行
3. **予測結果の統合**: 複数のモデルからの予測結果を統合
4. **結果の評価と保存**: 予測結果の評価、履歴の保存、フィードバックの収集
5. **モデル更新と再トレーニング**: 新しいデータに基づくモデルの更新

n8nを使用することで、これらのコンポーネントを柔軟に組み合わせ、自動化されたエンドツーエンドのワークフローを構築できます。

## データ収集と前処理ワークフロー

予測モデルの統合において、最初のステップはデータの収集と前処理です。n8nを使用して、様々なソースからデータを収集し、前処理するワークフローの例を示します。

```javascript
// n8n workflow: Data Collection and Preprocessing
// HTTP Request nodes to collect data from various sources
[
  {
    "id": "httpRequestMarketData",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "https://api.example.com/market-data",
      "method": "GET",
      "authentication": "genericCredentialType",
      "genericAuthType": "httpHeaderAuth",
      "nodeCredentialName": "marketDataApiKey"
    }
  },
  {
    "id": "httpRequestTechData",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "https://api.example.com/tech-trends",
      "method": "GET",
      "authentication": "genericCredentialType",
      "genericAuthType": "httpHeaderAuth",
      "nodeCredentialName": "techDataApiKey"
    }
  },
  {
    "id": "httpRequestBusinessData",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "https://api.example.com/business-metrics",
      "method": "GET",
      "authentication": "genericCredentialType",
      "genericAuthType": "httpHeaderAuth",
      "nodeCredentialName": "businessDataApiKey"
    }
  },
  {
    "id": "mergeData",
    "type": "n8n-nodes-base.merge",
    "parameters": {
      "mode": "mergeByPosition"
    }
  },
  {
    "id": "dataPreprocessing",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Merge data from different sources
        const marketData = $input.item(0).json;
        const techData = $input.item(1).json;
        const businessData = $input.item(2).json;
        
        // Extract relevant features
        const extractFeatures = (data, prefix) => {
          const features = {};
          
          // Extract numerical features
          Object.entries(data).forEach(([key, value]) => {
            if (typeof value === 'number') {
              features[\`\${prefix}_\${key}\`] = value;
            }
          });
          
          return features;
        };
        
        const marketFeatures = extractFeatures(marketData, 'market');
        const techFeatures = extractFeatures(techData, 'tech');
        const businessFeatures = extractFeatures(businessData, 'business');
        
        // Combine features
        const combinedFeatures = {
          ...marketFeatures,
          ...techFeatures,
          ...businessFeatures,
          timestamp: new Date().toISOString()
        };
        
        // Handle missing values
        const handleMissingValues = (features) => {
          const result = { ...features };
          
          Object.entries(result).forEach(([key, value]) => {
            if (value === null || value === undefined || Number.isNaN(value)) {
              // Replace with mean or default value (0 in this case)
              result[key] = 0;
            }
          });
          
          return result;
        };
        
        const cleanedFeatures = handleMissingValues(combinedFeatures);
        
        // Normalize numerical features
        const normalizeFeatures = (features) => {
          const result = { ...features };
          const numericalKeys = Object.keys(result).filter(key => 
            typeof result[key] === 'number' && key !== 'timestamp'
          );
          
          // Simple min-max normalization (assuming values between -100 and 100)
          numericalKeys.forEach(key => {
            result[key] = (result[key] + 100) / 200;
          });
          
          return result;
        };
        
        const normalizedFeatures = normalizeFeatures(cleanedFeatures);
        
        // Prepare feature vector for prediction models
        const featureVector = Object.entries(normalizedFeatures)
          .filter(([key, _]) => key !== 'timestamp')
          .map(([_, value]) => value);
        
        return {
          json: {
            raw_data: {
              market: marketData,
              tech: techData,
              business: businessData
            },
            features: normalizedFeatures,
            feature_vector: featureVector,
            timestamp: normalizedFeatures.timestamp
          }
        };
      `
    }
  },
  {
    "id": "savePreprocessedData",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insert",
      "collection": "preprocessed_data",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## モデル選択と実行ワークフロー

データの前処理が完了したら、次のステップは適切なモデルを選択し、予測を実行することです。n8nを使用して、モデル選択と実行を行うワークフローの例を示します。

```javascript
// n8n workflow: Model Selection and Execution
// Function node for model selection
[
  {
    "id": "loadPreprocessedData",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "find",
      "collection": "preprocessed_data",
      "options": {
        "sort": {
          "timestamp": -1
        },
        "limit": 1
      }
    }
  },
  {
    "id": "modelSelection",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get preprocessed data
        const preprocessedData = $input.item.json;
        const featureVector = preprocessedData.feature_vector;
        
        // Define model selection criteria
        const selectModels = (features, rawData) => {
          const selectedModels = [];
          
          // Check data characteristics to select appropriate models
          
          // 1. Check for time series patterns
          const hasTimeSeriesPatterns = true; // In real implementation, analyze data for patterns
          
          if (hasTimeSeriesPatterns) {
            selectedModels.push({
              type: 'time_series',
              models: ['arima', 'prophet', 'exponential_smoothing']
            });
          }
          
          // 2. Check for complex non-linear relationships
          const hasNonLinearRelationships = true; // In real implementation, analyze data
          
          if (hasNonLinearRelationships) {
            selectedModels.push({
              type: 'machine_learning',
              models: ['random_forest', 'gradient_boosting']
            });
          }
          
          // 3. Check for sequential patterns
          const hasSequentialPatterns = true; // In real implementation, analyze data
          
          if (hasSequentialPatterns) {
            selectedModels.push({
              type: 'deep_learning',
              models: ['lstm', 'gru']
            });
          }
          
          // 4. Always include ensemble methods
          selectedModels.push({
            type: 'ensemble',
            models: ['averaging', 'stacking']
          });
          
          return selectedModels;
        };
        
        const selectedModels = selectModels(featureVector, preprocessedData.raw_data);
        
        return {
          json: {
            preprocessed_data: preprocessedData,
            selected_models: selectedModels,
            execution_id: \`exec_\${Date.now()}\`,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "executeModels",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get selected models and data
        const data = $input.item.json;
        const selectedModels = data.selected_models;
        const preprocessedData = data.preprocessed_data;
        const executionId = data.execution_id;
        
        // Prepare model execution tasks
        const modelTasks = [];
        
        selectedModels.forEach(modelGroup => {
          modelGroup.models.forEach(model => {
            modelTasks.push({
              execution_id: executionId,
              model_type: modelGroup.type,
              model_name: model,
              data: preprocessedData,
              status: 'pending',
              created_at: new Date().toISOString()
            });
          });
        });
        
        return {
          json: {
            execution_id: executionId,
            model_tasks: modelTasks,
            total_tasks: modelTasks.length,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveModelTasks",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertMany",
      "collection": "model_tasks",
      "documents": "={{ $json.model_tasks }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "splitInBatches",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1,
      "options": {
        "batch": "={{ $json.model_tasks }}"
      }
    }
  },
  {
    "id": "executeTimeSeriesModels",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_type }}",
            "operation": "equal",
            "value2": "time_series"
          }
        ]
      }
    }
  },
  {
    "id": "executeMachineLearningModels",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_type }}",
            "operation": "equal",
            "value2": "machine_learning"
          }
        ]
      }
    }
  },
  {
    "id": "executeDeepLearningModels",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_type }}",
            "operation": "equal",
            "value2": "deep_learning"
          }
        ]
      }
    }
  },
  {
    "id": "executeEnsembleModels",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_type }}",
            "operation": "equal",
            "value2": "ensemble"
          }
        ]
      }
    }
  },
  {
    "id": "executeARIMA",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_name }}",
            "operation": "equal",
            "value2": "arima"
          }
        ]
      }
    }
  },
  {
    "id": "arimaExecution",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5000/api/models/arima",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "executeRandomForest",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_name }}",
            "operation": "equal",
            "value2": "random_forest"
          }
        ]
      }
    }
  },
  {
    "id": "randomForestExecution",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5000/api/models/random-forest",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "executeLSTM",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_name }}",
            "operation": "equal",
            "value2": "lstm"
          }
        ]
      }
    }
  },
  {
    "id": "lstmExecution",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5000/api/models/lstm",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "updateModelTaskStatus",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "updateOne",
      "collection": "model_tasks",
      "filter": {
        "execution_id": "={{ $json.execution_id }}",
        "model_type": "={{ $json.model_type }}",
        "model_name": "={{ $json.model_name }}"
      },
      "update": {
        "$set": {
          "status": "completed",
          "result": "={{ $json.result }}",
          "completed_at": "={{ new Date().toISOString() }}"
        }
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## 予測結果の統合ワークフロー

各モデルの予測が完了したら、次のステップは予測結果を統合することです。n8nを使用して、予測結果を統合するワークフローの例を示します。

```javascript
// n8n workflow: Prediction Results Integration
// Function node for results integration
[
  {
    "id": "checkModelTasksCompletion",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "find",
      "collection": "model_tasks",
      "filter": {
        "execution_id": "={{ $node[\"loadExecutionId\"].json.execution_id }}"
      }
    }
  },
  {
    "id": "verifyAllTasksCompleted",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get model tasks
        const modelTasks = $input.item.json;
        
        // Check if all tasks are completed
        const allCompleted = modelTasks.every(task => task.status === 'completed');
        const totalTasks = modelTasks.length;
        const completedTasks = modelTasks.filter(task => task.status === 'completed').length;
        
        if (!allCompleted) {
          return {
            json: {
              all_completed: false,
              total_tasks: totalTasks,
              completed_tasks: completedTasks,
              execution_id: modelTasks[0].execution_id,
              message: \`Waiting for all tasks to complete. \${completedTasks} of \${totalTasks} completed.\`
            }
          };
        }
        
        // Group results by model type
        const resultsByType = {};
        
        modelTasks.forEach(task => {
          if (!resultsByType[task.model_type]) {
            resultsByType[task.model_type] = [];
          }
          
          resultsByType[task.model_type].push({
            model_name: task.model_name,
            result: task.result
          });
        });
        
        return {
          json: {
            all_completed: true,
            total_tasks: totalTasks,
            completed_tasks: completedTasks,
            execution_id: modelTasks[0].execution_id,
            results_by_type: resultsByType
          }
        };
      `
    }
  },
  {
    "id": "waitIfNotCompleted",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "boolean": [
          {
            "value1": "={{ $json.all_completed }}",
            "value2": true
          }
        ]
      }
    }
  },
  {
    "id": "integrateResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get results by type
        const resultsByType = $input.item.json.results_by_type;
        const executionId = $input.item.json.execution_id;
        
        // Integrate time series model results
        const integrateTimeSeriesResults = (results) => {
          if (!results || results.length === 0) return null;
          
          // Extract predictions
          const predictions = results.map(r => ({
            model: r.model_name,
            prediction: r.result.prediction,
            confidence: r.result.confidence || 0.5
          }));
          
          // Calculate weighted average based on confidence
          let weightedSum = 0;
          let weightSum = 0;
          
          predictions.forEach(p => {
            weightedSum += p.prediction * p.confidence;
            weightSum += p.confidence;
          });
          
          const integratedPrediction = weightSum > 0 ? weightedSum / weightSum : null;
          
          return {
            individual_predictions: predictions,
            integrated_prediction: integratedPrediction,
            confidence: Math.min(1, weightSum / predictions.length)
          };
        };
        
        // Integrate machine learning model results
        const integrateMachineLearningResults = (results) => {
          if (!results || results.length === 0) return null;
          
          // Extract predictions
          const predictions = results.map(r => ({
            model: r.model_name,
            prediction: r.result.prediction,
            confidence: r.result.confidence || 0.5
          }));
          
          // Calculate weighted average based on confidence
          let weightedSum = 0;
          let weightSum = 0;
          
          predictions.forEach(p => {
            weightedSum += p.prediction * p.confidence;
            weightSum += p.confidence;
          });
          
          const integratedPrediction = weightSum > 0 ? weightedSum / weightSum : null;
          
          return {
            individual_predictions: predictions,
            integrated_prediction: integratedPrediction,
            confidence: Math.min(1, weightSum / predictions.length)
          };
        };
        
        // Integrate deep learning model results
        const integrateDeepLearningResults = (results) => {
          if (!results || results.length === 0) return null;
          
          // Extract predictions
          const predictions = results.map(r => ({
            model: r.model_name,
            prediction: r.result.prediction,
            confidence: r.result.confidence || 0.5
          }));
          
          // Calculate weighted average based on confidence
          let weightedSum = 0;
          let weightSum = 0;
          
          predictions.forEach(p => {
            weightedSum += p.prediction * p.confidence;
            weightSum += p.confidence;
          });
          
          const integratedPrediction = weightSum > 0 ? weightedSum / weightSum : null;
          
          return {
            individual_predictions: predictions,
            integrated_prediction: integratedPrediction,
            confidence: Math.min(1, weightSum / predictions.length)
          };
        };
        
        // Integrate ensemble model results
        const integrateEnsembleResults = (results) => {
          if (!results || results.length === 0) return null;
          
          // Extract predictions
          const predictions = results.map(r => ({
            model: r.model_name,
            prediction: r.result.prediction,
            confidence: r.result.confidence || 0.5
          }));
          
          // Calculate weighted average based on confidence
          let weightedSum = 0;
          let weightSum = 0;
          
          predictions.forEach(p => {
            weightedSum += p.prediction * p.confidence;
            weightSum += p.confidence;
          });
          
          const integratedPrediction = weightSum > 0 ? weightedSum / weightSum : null;
          
          return {
            individual_predictions: predictions,
            integrated_prediction: integratedPrediction,
            confidence: Math.min(1, weightSum / predictions.length)
          };
        };
        
        // Integrate all results
        const timeSeriesResults = integrateTimeSeriesResults(resultsByType.time_series);
        const machineLearningResults = integrateMachineLearningResults(resultsByType.machine_learning);
        const deepLearningResults = integrateDeepLearningResults(resultsByType.deep_learning);
        const ensembleResults = integrateEnsembleResults(resultsByType.ensemble);
        
        // Calculate final integrated prediction
        const calculateFinalPrediction = () => {
          const predictions = [];
          
          if (timeSeriesResults) {
            predictions.push({
              type: 'time_series',
              prediction: timeSeriesResults.integrated_prediction,
              confidence: timeSeriesResults.confidence
            });
          }
          
          if (machineLearningResults) {
            predictions.push({
              type: 'machine_learning',
              prediction: machineLearningResults.integrated_prediction,
              confidence: machineLearningResults.confidence
            });
          }
          
          if (deepLearningResults) {
            predictions.push({
              type: 'deep_learning',
              prediction: deepLearningResults.integrated_prediction,
              confidence: deepLearningResults.confidence
            });
          }
          
          if (ensembleResults) {
            predictions.push({
              type: 'ensemble',
              prediction: ensembleResults.integrated_prediction,
              confidence: ensembleResults.confidence
            });
          }
          
          // Calculate weighted average based on confidence
          let weightedSum = 0;
          let weightSum = 0;
          
          predictions.forEach(p => {
            if (p.prediction !== null) {
              weightedSum += p.prediction * p.confidence;
              weightSum += p.confidence;
            }
          });
          
          const finalPrediction = weightSum > 0 ? weightedSum / weightSum : null;
          const finalConfidence = Math.min(1, weightSum / predictions.length);
          
          return {
            predictions_by_type: predictions,
            final_prediction: finalPrediction,
            confidence: finalConfidence
          };
        };
        
        const finalResult = calculateFinalPrediction();
        
        return {
          json: {
            execution_id: executionId,
            time_series_results: timeSeriesResults,
            machine_learning_results: machineLearningResults,
            deep_learning_results: deepLearningResults,
            ensemble_results: ensembleResults,
            final_result: finalResult,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveIntegratedResults",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "integrated_results",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## 結果の評価と保存ワークフロー

予測結果の統合が完了したら、次のステップは結果の評価と保存です。n8nを使用して、結果の評価と保存を行うワークフローの例を示します。

```javascript
// n8n workflow: Results Evaluation and Storage
// Function node for results evaluation
[
  {
    "id": "loadIntegratedResults",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "findOne",
      "collection": "integrated_results",
      "filter": {
        "execution_id": "={{ $node[\"loadExecutionId\"].json.execution_id }}"
      },
      "options": {
        "sort": {
          "timestamp": -1
        }
      }
    }
  },
  {
    "id": "evaluateResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get integrated results
        const integratedResults = $input.item.json;
        const finalResult = integratedResults.final_result;
        
        // Evaluate prediction quality
        const evaluatePredictionQuality = () => {
          // In a real implementation, this would compare with actual values when available
          // For demonstration, we'll use confidence as a proxy for quality
          
          const confidence = finalResult.confidence;
          
          let qualityScore;
          let qualityLabel;
          
          if (confidence >= 0.8) {
            qualityScore = 5;
            qualityLabel = 'Excellent';
          } else if (confidence >= 0.6) {
            qualityScore = 4;
            qualityLabel = 'Good';
          } else if (confidence >= 0.4) {
            qualityScore = 3;
            qualityLabel = 'Moderate';
          } else if (confidence >= 0.2) {
            qualityScore = 2;
            qualityLabel = 'Poor';
          } else {
            qualityScore = 1;
            qualityLabel = 'Very Poor';
          }
          
          return {
            quality_score: qualityScore,
            quality_label: qualityLabel,
            confidence: confidence
          };
        };
        
        // Evaluate prediction consistency
        const evaluatePredictionConsistency = () => {
          // Calculate consistency across different model types
          const predictions = finalResult.predictions_by_type;
          
          if (predictions.length <= 1) {
            return {
              consistency_score: null,
              consistency_label: 'Not Applicable',
              std_deviation: null
            };
          }
          
          // Calculate standard deviation
          const values = predictions.map(p => p.prediction).filter(p => p !== null);
          const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
          const squaredDiffs = values.map(val => Math.pow(val - mean, 2));
          const variance = squaredDiffs.reduce((sum, val) => sum + val, 0) / values.length;
          const stdDeviation = Math.sqrt(variance);
          
          // Normalize by mean to get coefficient of variation
          const cv = mean !== 0 ? stdDeviation / Math.abs(mean) : null;
          
          let consistencyScore;
          let consistencyLabel;
          
          if (cv !== null) {
            if (cv < 0.1) {
              consistencyScore = 5;
              consistencyLabel = 'Excellent';
            } else if (cv < 0.2) {
              consistencyScore = 4;
              consistencyLabel = 'Good';
            } else if (cv < 0.3) {
              consistencyScore = 3;
              consistencyLabel = 'Moderate';
            } else if (cv < 0.4) {
              consistencyScore = 2;
              consistencyLabel = 'Poor';
            } else {
              consistencyScore = 1;
              consistencyLabel = 'Very Poor';
            }
          } else {
            consistencyScore = null;
            consistencyLabel = 'Not Applicable';
          }
          
          return {
            consistency_score: consistencyScore,
            consistency_label: consistencyLabel,
            std_deviation: stdDeviation,
            coefficient_of_variation: cv
          };
        };
        
        // Generate insights
        const generateInsights = () => {
          const insights = [];
          
          // Check for high confidence
          if (finalResult.confidence >= 0.8) {
            insights.push('High confidence prediction suggests reliable forecast.');
          }
          
          // Check for low confidence
          if (finalResult.confidence < 0.4) {
            insights.push('Low confidence prediction suggests caution in interpretation.');
          }
          
          // Check for consistency
          const consistency = evaluatePredictionConsistency();
          
          if (consistency.consistency_score === 5) {
            insights.push('Excellent consistency across different model types suggests robust prediction.');
          }
          
          if (consistency.consistency_score === 1) {
            insights.push('Poor consistency across different model types suggests high uncertainty.');
          }
          
          // Check for model type performance
          const modelTypes = ['time_series', 'machine_learning', 'deep_learning', 'ensemble'];
          
          modelTypes.forEach(type => {
            const results = integratedResults[\`\${type}_results\`];
            
            if (results && results.confidence >= 0.8) {
              insights.push(\`\${type.replace('_', ' ')} models show high confidence.\`);
            }
          });
          
          return insights;
        };
        
        const qualityEvaluation = evaluatePredictionQuality();
        const consistencyEvaluation = evaluatePredictionConsistency();
        const insights = generateInsights();
        
        return {
          json: {
            execution_id: integratedResults.execution_id,
            final_prediction: finalResult.final_prediction,
            confidence: finalResult.confidence,
            quality_evaluation: qualityEvaluation,
            consistency_evaluation: consistencyEvaluation,
            insights: insights,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveEvaluationResults",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "evaluation_results",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "generateReport",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get evaluation results
        const evaluationResults = $input.item.json;
        
        // Generate HTML report
        const generateHtmlReport = () => {
          return \`
            <!DOCTYPE html>
            <html>
            <head>
              <title>Prediction Results Report</title>
              <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .section { margin-bottom: 20px; }
                .metric { margin-bottom: 10px; }
                .label { font-weight: bold; }
                .value { margin-left: 10px; }
                .excellent { color: #2e7d32; }
                .good { color: #388e3c; }
                .moderate { color: #f9a825; }
                .poor { color: #e65100; }
                .very-poor { color: #c62828; }
                .insights { background-color: #f5f5f5; padding: 10px; border-radius: 5px; }
                .insight-item { margin-bottom: 5px; }
              </style>
            </head>
            <body>
              <h1>Prediction Results Report</h1>
              
              <div class="section">
                <h2>Summary</h2>
                <div class="metric">
                  <span class="label">Final Prediction:</span>
                  <span class="value">\${evaluationResults.final_prediction.toFixed(2)}</span>
                </div>
                <div class="metric">
                  <span class="label">Confidence:</span>
                  <span class="value">\${(evaluationResults.confidence * 100).toFixed(1)}%</span>
                </div>
                <div class="metric">
                  <span class="label">Quality:</span>
                  <span class="value \${evaluationResults.quality_evaluation.quality_label.toLowerCase()}">\${evaluationResults.quality_evaluation.quality_label} (\${evaluationResults.quality_evaluation.quality_score}/5)</span>
                </div>
                <div class="metric">
                  <span class="label">Consistency:</span>
                  <span class="value \${evaluationResults.consistency_evaluation.consistency_label.toLowerCase()}">\${evaluationResults.consistency_evaluation.consistency_label} (\${evaluationResults.consistency_evaluation.consistency_score}/5)</span>
                </div>
              </div>
              
              <div class="section">
                <h2>Insights</h2>
                <div class="insights">
                  \${evaluationResults.insights.map(insight => \`<div class="insight-item">\${insight}</div>\`).join('')}
                </div>
              </div>
              
              <div class="section">
                <h2>Timestamp</h2>
                <div class="metric">
                  <span class="value">\${new Date(evaluationResults.timestamp).toLocaleString()}</span>
                </div>
              </div>
            </body>
            </html>
          \`;
        };
        
        // Generate JSON report
        const generateJsonReport = () => {
          return {
            summary: {
              final_prediction: evaluationResults.final_prediction,
              confidence: evaluationResults.confidence,
              quality: {
                score: evaluationResults.quality_evaluation.quality_score,
                label: evaluationResults.quality_evaluation.quality_label
              },
              consistency: {
                score: evaluationResults.consistency_evaluation.consistency_score,
                label: evaluationResults.consistency_evaluation.consistency_label
              }
            },
            insights: evaluationResults.insights,
            timestamp: evaluationResults.timestamp
          };
        };
        
        const htmlReport = generateHtmlReport();
        const jsonReport = generateJsonReport();
        
        return {
          json: {
            execution_id: evaluationResults.execution_id,
            html_report: htmlReport,
            json_report: jsonReport,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveReport",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "reports",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## モデル更新と再トレーニングワークフロー

予測結果の評価が完了したら、最後のステップはモデルの更新と再トレーニングです。n8nを使用して、モデルの更新と再トレーニングを行うワークフローの例を示します。

```javascript
// n8n workflow: Model Update and Retraining
// Function node for model update and retraining
[
  {
    "id": "checkModelPerformance",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "find",
      "collection": "evaluation_results",
      "options": {
        "sort": {
          "timestamp": -1
        },
        "limit": 10
      }
    }
  },
  {
    "id": "analyzeModelPerformance",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get evaluation results
        const evaluationResults = $input.items;
        
        // Analyze model performance
        const analyzePerformance = () => {
          // Calculate average quality score
          const qualityScores = evaluationResults.map(result => result.json.quality_evaluation.quality_score);
          const avgQualityScore = qualityScores.reduce((sum, score) => sum + score, 0) / qualityScores.length;
          
          // Calculate average consistency score
          const consistencyScores = evaluationResults
            .map(result => result.json.consistency_evaluation.consistency_score)
            .filter(score => score !== null);
          
          const avgConsistencyScore = consistencyScores.length > 0 ?
            consistencyScores.reduce((sum, score) => sum + score, 0) / consistencyScores.length : null;
          
          // Identify models that need retraining
          const modelsToRetrain = [];
          
          // Check if quality is declining
          const isQualityDeclining = qualityScores.length >= 3 &&
            qualityScores[0] < qualityScores[1] &&
            qualityScores[1] < qualityScores[2];
          
          if (isQualityDeclining) {
            modelsToRetrain.push('all'); // Retrain all models if quality is consistently declining
          } else if (avgQualityScore < 3) {
            // If average quality is poor, identify specific model types to retrain
            
            // Check time series models
            const timeSeriesConfidence = evaluationResults
              .filter(result => result.json.time_series_results)
              .map(result => result.json.time_series_results.confidence);
            
            const avgTimeSeriesConfidence = timeSeriesConfidence.length > 0 ?
              timeSeriesConfidence.reduce((sum, conf) => sum + conf, 0) / timeSeriesConfidence.length : null;
            
            if (avgTimeSeriesConfidence !== null && avgTimeSeriesConfidence < 0.4) {
              modelsToRetrain.push('time_series');
            }
            
            // Check machine learning models
            const mlConfidence = evaluationResults
              .filter(result => result.json.machine_learning_results)
              .map(result => result.json.machine_learning_results.confidence);
            
            const avgMlConfidence = mlConfidence.length > 0 ?
              mlConfidence.reduce((sum, conf) => sum + conf, 0) / mlConfidence.length : null;
            
            if (avgMlConfidence !== null && avgMlConfidence < 0.4) {
              modelsToRetrain.push('machine_learning');
            }
            
            // Check deep learning models
            const dlConfidence = evaluationResults
              .filter(result => result.json.deep_learning_results)
              .map(result => result.json.deep_learning_results.confidence);
            
            const avgDlConfidence = dlConfidence.length > 0 ?
              dlConfidence.reduce((sum, conf) => sum + conf, 0) / dlConfidence.length : null;
            
            if (avgDlConfidence !== null && avgDlConfidence < 0.4) {
              modelsToRetrain.push('deep_learning');
            }
          }
          
          return {
            avg_quality_score: avgQualityScore,
            avg_consistency_score: avgConsistencyScore,
            quality_trend: isQualityDeclining ? 'declining' : 'stable',
            models_to_retrain: modelsToRetrain
          };
        };
        
        const performanceAnalysis = analyzePerformance();
        
        return {
          json: {
            performance_analysis: performanceAnalysis,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "decideRetraining",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "number": [
          {
            "value1": "={{ $json.performance_analysis.models_to_retrain.length }}",
            "operation": "larger",
            "value2": 0
          }
        ]
      }
    }
  },
  {
    "id": "prepareRetrainingData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get performance analysis
        const performanceAnalysis = $input.item.json.performance_analysis;
        const modelsToRetrain = performanceAnalysis.models_to_retrain;
        
        // Prepare retraining tasks
        const retrainingTasks = [];
        
        if (modelsToRetrain.includes('all')) {
          // Retrain all model types
          retrainingTasks.push(
            { model_type: 'time_series', models: ['arima', 'prophet', 'exponential_smoothing'] },
            { model_type: 'machine_learning', models: ['random_forest', 'gradient_boosting'] },
            { model_type: 'deep_learning', models: ['lstm', 'gru'] }
          );
        } else {
          // Retrain specific model types
          if (modelsToRetrain.includes('time_series')) {
            retrainingTasks.push(
              { model_type: 'time_series', models: ['arima', 'prophet', 'exponential_smoothing'] }
            );
          }
          
          if (modelsToRetrain.includes('machine_learning')) {
            retrainingTasks.push(
              { model_type: 'machine_learning', models: ['random_forest', 'gradient_boosting'] }
            );
          }
          
          if (modelsToRetrain.includes('deep_learning')) {
            retrainingTasks.push(
              { model_type: 'deep_learning', models: ['lstm', 'gru'] }
            );
          }
        }
        
        return {
          json: {
            retraining_tasks: retrainingTasks,
            retraining_id: \`retrain_\${Date.now()}\`,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveRetrainingTasks",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "retraining_tasks",
      "document": "={{ $json }}",
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "splitRetrainingTasks",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1,
      "options": {
        "batch": "={{ $json.retraining_tasks }}"
      }
    }
  },
  {
    "id": "retrainTimeSeriesModels",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_type }}",
            "operation": "equal",
            "value2": "time_series"
          }
        ]
      }
    }
  },
  {
    "id": "timeSeriesRetraining",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5000/api/retrain/time-series",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "retrainMachineLearningModels",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_type }}",
            "operation": "equal",
            "value2": "machine_learning"
          }
        ]
      }
    }
  },
  {
    "id": "machineLearningRetraining",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5000/api/retrain/machine-learning",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "retrainDeepLearningModels",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "conditions": {
        "string": [
          {
            "value1": "={{ $json.model_type }}",
            "operation": "equal",
            "value2": "deep_learning"
          }
        ]
      }
    }
  },
  {
    "id": "deepLearningRetraining",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5000/api/retrain/deep-learning",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "updateRetrainingStatus",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "updateOne",
      "collection": "retraining_tasks",
      "filter": {
        "retraining_id": "={{ $node[\"prepareRetrainingData\"].json.retraining_id }}"
      },
      "update": {
        "$set": {
          "status": "completed",
          "completed_at": "={{ new Date().toISOString() }}"
        }
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## マスターオーケストレーションワークフロー

最後に、上記のすべてのワークフローを統合するマスターオーケストレーションワークフローを示します。このワークフローは、データ収集から予測結果の評価、モデルの更新まで、エンドツーエンドのプロセスを自動化します。

```javascript
// n8n workflow: Master Orchestration Workflow
// Cron node to trigger the workflow periodically
[
  {
    "id": "cronTrigger",
    "type": "n8n-nodes-base.cron",
    "parameters": {
      "triggerTimes": {
        "item": [
          {
            "mode": "everyX",
            "value": 1,
            "unit": "hours"
          }
        ]
      }
    }
  },
  {
    "id": "generateExecutionId",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Generate a unique execution ID
        const executionId = \`exec_\${Date.now()}\`;
        
        return {
          json: {
            execution_id: executionId,
            timestamp: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveExecutionStart",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "insertOne",
      "collection": "execution_log",
      "document": {
        "execution_id": "={{ $json.execution_id }}",
        "status": "started",
        "start_time": "={{ $json.timestamp }}",
        "steps_completed": []
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "executeDataCollection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/data-collection",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "updateExecutionLog1",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "updateOne",
      "collection": "execution_log",
      "filter": {
        "execution_id": "={{ $json.execution_id }}"
      },
      "update": {
        "$push": {
          "steps_completed": "data_collection"
        }
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "executeModelSelection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/model-selection",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "updateExecutionLog2",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "updateOne",
      "collection": "execution_log",
      "filter": {
        "execution_id": "={{ $json.execution_id }}"
      },
      "update": {
        "$push": {
          "steps_completed": "model_selection"
        }
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "waitForModelExecution",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // This function simulates waiting for model execution to complete
        // In a real implementation, this would poll the database to check if all model tasks are completed
        
        // For demonstration, we'll just wait for a few seconds
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              json: $input.item.json
            });
          }, 5000);
        });
      `
    }
  },
  {
    "id": "executeResultsIntegration",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/results-integration",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "updateExecutionLog3",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "updateOne",
      "collection": "execution_log",
      "filter": {
        "execution_id": "={{ $json.execution_id }}"
      },
      "update": {
        "$push": {
          "steps_completed": "results_integration"
        }
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "executeResultsEvaluation",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/results-evaluation",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "updateExecutionLog4",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "updateOne",
      "collection": "execution_log",
      "filter": {
        "execution_id": "={{ $json.execution_id }}"
      },
      "update": {
        "$push": {
          "steps_completed": "results_evaluation"
        }
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  },
  {
    "id": "executeModelUpdate",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/model-update",
      "method": "POST",
      "bodyContent": "={{ JSON.stringify($json) }}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "updateExecutionLog5",
    "type": "n8n-nodes-base.mongoDb",
    "parameters": {
      "operation": "updateOne",
      "collection": "execution_log",
      "filter": {
        "execution_id": "={{ $json.execution_id }}"
      },
      "update": {
        "$set": {
          "status": "completed",
          "end_time": "={{ new Date().toISOString() }}"
        },
        "$push": {
          "steps_completed": "model_update"
        }
      },
      "options": {
        "writeConcern": {
          "w": "majority",
          "j": true
        }
      }
    }
  }
]
```

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおけるn8nによるモデル統合ワークフローの実装について詳細に解説しました。データ収集と前処理、モデル選択と実行、予測結果の統合、結果の評価と保存、モデル更新と再トレーニング、そしてマスターオーケストレーションワークフローなど、主要なワークフローのn8nによる実装例を提供しました。

これらのワークフローを組み合わせることで、時系列予測モデル、機械学習モデル、深層学習モデル、アンサンブル手法など、様々な予測モデルを効率的に統合し、自動化されたエンドツーエンドの予測システムを構築することができます。

次のセクションでは、シナリオ生成と予測の活用について詳細に解説します。
