# 予測モデルの実装と統合（パート2-4：アンサンブル手法の実装）

## アンサンブル手法による予測の概要

トリプルパースペクティブ型戦略AIレーダーにおける予測エンジンでは、単一のモデルに依存するのではなく、複数のモデルを組み合わせるアンサンブル手法を活用することで、より堅牢で精度の高い予測を実現します。アンサンブル手法は、異なるモデルの長所を活かし、短所を補完することで、予測の安定性と精度を向上させます。本セクションでは、主要なアンサンブル手法のn8nによる実装について解説します。

### アンサンブル予測の基本概念

アンサンブル予測は、以下のステップで行われます：

1. **複数モデルの構築**: 異なるアルゴリズム、パラメータ、トレーニングデータを使用して複数のモデルを構築
2. **個別予測の生成**: 各モデルで独立に予測を生成
3. **予測の統合**: 何らかの方法（平均、加重平均、投票など）で個別予測を統合
4. **最終予測の生成**: 統合された予測を最終結果として出力

トリプルパースペクティブ型戦略AIレーダーでは、以下のようなアンサンブル手法を活用します：

- 平均化アンサンブル（単純平均、加重平均）
- スタッキングアンサンブル
- ブースティングアンサンブル
- バギングアンサンブル
- 多様性を考慮したアンサンブル

## 平均化アンサンブルの実装

平均化アンサンブルは、最も基本的なアンサンブル手法で、複数のモデルの予測結果を平均化することで最終予測を生成します。単純平均と加重平均の2種類があります。

### n8nによる平均化アンサンブル実装

```javascript
// n8n workflow: Averaging Ensemble Implementation
// Function node for averaging ensemble
[
  {
    "id": "averagingEnsemble",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Predictions from multiple models and ensemble parameters
        const modelPredictions = $input.item.json.model_predictions || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const ensembleType = parameters.ensemble_type || 'simple_average';
        const weights = parameters.weights || [];
        
        // Validate input
        if (modelPredictions.length === 0) {
          throw new Error('No model predictions provided');
        }
        
        // Extract test data and predictions
        const testData = [];
        const allPredictions = [];
        
        // Organize predictions by test case
        modelPredictions.forEach(modelResult => {
          const modelName = modelResult.model_name;
          const predictions = modelResult.predictions || [];
          
          predictions.forEach((pred, idx) => {
            // Initialize test case if not exists
            if (!testData[idx]) {
              testData[idx] = pred.features || pred.sequence || \`Test case \${idx + 1}\`;
            }
            
            // Initialize predictions array if not exists
            if (!allPredictions[idx]) {
              allPredictions[idx] = [];
            }
            
            // Add prediction
            allPredictions[idx].push({
              model: modelName,
              prediction: pred.prediction
            });
          });
        });
        
        // Generate ensemble predictions
        const ensemblePredictions = [];
        
        for (let i = 0; i < testData.length; i++) {
          const testCase = testData[i];
          const predictions = allPredictions[i] || [];
          
          // Skip if no predictions
          if (predictions.length === 0) continue;
          
          let ensemblePrediction;
          
          if (ensembleType === 'simple_average') {
            // Simple average
            const sum = predictions.reduce((acc, p) => acc + p.prediction, 0);
            ensemblePrediction = sum / predictions.length;
          } else if (ensembleType === 'weighted_average') {
            // Weighted average
            let weightedSum = 0;
            let weightSum = 0;
            
            predictions.forEach((p, idx) => {
              const weight = idx < weights.length ? weights[idx] : 1;
              weightedSum += p.prediction * weight;
              weightSum += weight;
            });
            
            ensemblePrediction = weightSum > 0 ? weightedSum / weightSum : 0;
          } else {
            // Default to simple average
            const sum = predictions.reduce((acc, p) => acc + p.prediction, 0);
            ensemblePrediction = sum / predictions.length;
          }
          
          ensemblePredictions.push({
            test_case: i + 1,
            features: testCase,
            individual_predictions: predictions,
            ensemble_prediction: ensemblePrediction
          });
        }
        
        return {
          json: {
            ensemble_type: ensembleType,
            num_models: modelPredictions.length,
            model_names: modelPredictions.map(m => m.model_name),
            weights: ensembleType === 'weighted_average' ? weights : null,
            predictions: ensemblePredictions
          }
        };
      `
    }
  }
]
```

### 平均化アンサンブルの使用例

```javascript
// n8n workflow: Averaging Ensemble Usage Example
// HTTP Request node to call averaging ensemble
[
  {
    "id": "httpRequest",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/averaging-ensemble",
      "method": "POST",
      "bodyContent": "{\n  \"model_predictions\": [\n    {\n      \"model_name\": \"ARIMA\",\n      \"predictions\": [\n        {\"features\": [1, 2, 3, 4, 5], \"prediction\": 6.2},\n        {\"features\": [2, 3, 4, 5, 6], \"prediction\": 7.1},\n        {\"features\": [3, 4, 5, 6, 7], \"prediction\": 8.3}\n      ]\n    },\n    {\n      \"model_name\": \"RandomForest\",\n      \"predictions\": [\n        {\"features\": [1, 2, 3, 4, 5], \"prediction\": 6.5},\n        {\"features\": [2, 3, 4, 5, 6], \"prediction\": 7.4},\n        {\"features\": [3, 4, 5, 6, 7], \"prediction\": 8.0}\n      ]\n    },\n    {\n      \"model_name\": \"LSTM\",\n      \"predictions\": [\n        {\"features\": [1, 2, 3, 4, 5], \"prediction\": 6.0},\n        {\"features\": [2, 3, 4, 5, 6], \"prediction\": 7.2},\n        {\"features\": [3, 4, 5, 6, 7], \"prediction\": 8.1}\n      ]\n    }\n  ],\n  \"parameters\": {\n    \"ensemble_type\": \"weighted_average\",\n    \"weights\": [1, 2, 3]\n  }\n}",
      "bodyContentType": "json"
    }
  }
]
```

## スタッキングアンサンブルの実装

スタッキングアンサンブルは、複数のベースモデル（レベル0）の予測結果を入力として、メタモデル（レベル1）を訓練し、最終予測を生成する手法です。メタモデルは、ベースモデルの予測結果の組み合わせ方を学習します。

### n8nからPythonを使用したスタッキングアンサンブル実装

```javascript
// n8n workflow: Stacking Ensemble Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor; from sklearn.linear_model import LinearRegression; from sklearn.svm import SVR; # Extract data base_models_train = data['base_models_train']; base_models_test = data['base_models_test']; y_train = np.array(data['y_train']); # Prepare meta-features X_meta_train = np.array([[pred for pred in model['predictions']] for model in base_models_train]).T; X_meta_test = np.array([[pred for pred in model['predictions']] for model in base_models_test]).T; # Create and train meta-model params = data['parameters']; meta_model_type = params.get('meta_model_type', 'linear'); if meta_model_type == 'linear': meta_model = LinearRegression(); elif meta_model_type == 'random_forest': meta_model = RandomForestRegressor(n_estimators=params.get('n_estimators', 100), max_depth=params.get('max_depth', 10)); elif meta_model_type == 'gradient_boosting': meta_model = GradientBoostingRegressor(n_estimators=params.get('n_estimators', 100), learning_rate=params.get('learning_rate', 0.1)); elif meta_model_type == 'svr': meta_model = SVR(kernel=params.get('kernel', 'rbf'), C=params.get('C', 1.0)); else: meta_model = LinearRegression(); # Train meta-model meta_model.fit(X_meta_train, y_train); # Make predictions meta_predictions = meta_model.predict(X_meta_test).tolist(); # Prepare output result = {'predictions': [{'test_case': i + 1, 'base_model_predictions': [model['predictions'][i] for model in base_models_test], 'meta_prediction': meta_predictions[i]} for i in range(len(meta_predictions))], 'model_info': {'meta_model_type': meta_model_type, 'base_models': [model['model_name'] for model in base_models_train], 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setStackingInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for stacking ensemble
        const baseModelsTrain = $input.item.json.base_models_train || [];
        const baseModelsTest = $input.item.json.base_models_test || [];
        const yTrain = $input.item.json.y_train || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for stacking ensemble
        const stackingInput = {
          base_models_train: baseModelsTrain,
          base_models_test: baseModelsTest,
          y_train: yTrain,
          parameters: {
            meta_model_type: parameters.meta_model_type || 'linear',
            n_estimators: parameters.n_estimators || 100,
            max_depth: parameters.max_depth || 10,
            learning_rate: parameters.learning_rate || 0.1,
            kernel: parameters.kernel || 'rbf',
            C: parameters.C || 1.0
          }
        };
        
        return {
          json: stackingInput
        };
      `
    }
  },
  {
    "id": "processStackingResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process stacking ensemble results
        const stackingResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = stackingResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'Stacking Ensemble',
          meta_model_type: stackingResults.model_info.meta_model_type,
          base_models: stackingResults.model_info.base_models,
          parameters: stackingResults.model_info.parameters,
          predictions: predictions.map(p => ({
            test_case: p.test_case,
            base_model_predictions: p.base_model_predictions.map((pred, idx) => ({
              model: stackingResults.model_info.base_models[idx],
              prediction: Math.round(pred * 100) / 100
            })),
            meta_prediction: Math.round(p.meta_prediction * 100) / 100
          }))
        };
        
        return {
          json: formattedResults
        };
      `
    }
  }
]
```

## ブースティングアンサンブルの実装

ブースティングアンサンブルは、モデルを逐次的に構築し、各モデルが前のモデルの誤差を修正するように訓練する手法です。AdaBoost、Gradient Boosting、XGBoostなどの実装があります。

### n8nからPythonを使用したブースティングアンサンブル実装

```javascript
// n8n workflow: Boosting Ensemble Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor; from sklearn.tree import DecisionTreeRegressor; # Extract data X_train = np.array([item['features'] for item in data['training_data']]); y_train = np.array([item['target'] for item in data['training_data']]); X_test = np.array([item['features'] for item in data['test_data']]); # Create and train boosting model params = data['parameters']; boosting_type = params.get('boosting_type', 'adaboost'); if boosting_type == 'adaboost': base_estimator = DecisionTreeRegressor(max_depth=params.get('base_max_depth', 3)); model = AdaBoostRegressor(base_estimator=base_estimator, n_estimators=params.get('n_estimators', 50), learning_rate=params.get('learning_rate', 1.0)); elif boosting_type == 'gradient_boosting': model = GradientBoostingRegressor(n_estimators=params.get('n_estimators', 100), learning_rate=params.get('learning_rate', 0.1), max_depth=params.get('max_depth', 3), subsample=params.get('subsample', 1.0)); else: base_estimator = DecisionTreeRegressor(max_depth=params.get('base_max_depth', 3)); model = AdaBoostRegressor(base_estimator=base_estimator, n_estimators=params.get('n_estimators', 50), learning_rate=params.get('learning_rate', 1.0)); # Train model model.fit(X_train, y_train); # Make predictions predictions = model.predict(X_test).tolist(); # Get feature importances if hasattr(model, 'feature_importances_'): feature_importances = model.feature_importances_.tolist(); else: feature_importances = None; # Prepare output result = {'predictions': [{'features': data['test_data'][i]['features'], 'prediction': predictions[i]} for i in range(len(predictions))], 'model_info': {'boosting_type': boosting_type, 'feature_importances': feature_importances, 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setBoostingInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for boosting ensemble
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for boosting ensemble
        const boostingInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            boosting_type: parameters.boosting_type || 'adaboost',
            n_estimators: parameters.n_estimators || 50,
            learning_rate: parameters.learning_rate || 1.0,
            base_max_depth: parameters.base_max_depth || 3,
            max_depth: parameters.max_depth || 3,
            subsample: parameters.subsample || 1.0
          }
        };
        
        return {
          json: boostingInput
        };
      `
    }
  },
  {
    "id": "processBoostingResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process boosting ensemble results
        const boostingResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = boostingResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'Boosting Ensemble',
          boosting_type: boostingResults.model_info.boosting_type,
          parameters: boostingResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            features: p.features,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          feature_importances: boostingResults.model_info.feature_importances ? 
            boostingResults.model_info.feature_importances.map((imp, idx) => ({
              feature: idx + 1,
              importance: Math.round(imp * 1000) / 1000
            })) : null
        };
        
        return {
          json: formattedResults
        };
      `
    }
  }
]
```

## バギングアンサンブルの実装

バギングアンサンブルは、元のデータセットからブートストラップサンプル（重複を許したランダムサンプリング）を複数作成し、各サンプルで独立にモデルを訓練する手法です。ランダムフォレストはバギングの一種です。

### n8nからPythonを使用したバギングアンサンブル実装

```javascript
// n8n workflow: Bagging Ensemble Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; from sklearn.ensemble import BaggingRegressor; from sklearn.tree import DecisionTreeRegressor; from sklearn.linear_model import LinearRegression; from sklearn.svm import SVR; # Extract data X_train = np.array([item['features'] for item in data['training_data']]); y_train = np.array([item['target'] for item in data['training_data']]); X_test = np.array([item['features'] for item in data['test_data']]); # Create base estimator params = data['parameters']; base_estimator_type = params.get('base_estimator_type', 'decision_tree'); if base_estimator_type == 'decision_tree': base_estimator = DecisionTreeRegressor(max_depth=params.get('max_depth', 10)); elif base_estimator_type == 'linear': base_estimator = LinearRegression(); elif base_estimator_type == 'svr': base_estimator = SVR(kernel=params.get('kernel', 'rbf'), C=params.get('C', 1.0)); else: base_estimator = DecisionTreeRegressor(max_depth=params.get('max_depth', 10)); # Create and train bagging model model = BaggingRegressor(base_estimator=base_estimator, n_estimators=params.get('n_estimators', 10), max_samples=params.get('max_samples', 1.0), max_features=params.get('max_features', 1.0), bootstrap=params.get('bootstrap', True), bootstrap_features=params.get('bootstrap_features', False), random_state=42); model.fit(X_train, y_train); # Make predictions predictions = model.predict(X_test).tolist(); # Make individual estimator predictions if params.get('return_individual_predictions', False): individual_predictions = np.array([estimator.predict(X_test) for estimator in model.estimators_]).T.tolist(); else: individual_predictions = None; # Prepare output result = {'predictions': [{'features': data['test_data'][i]['features'], 'prediction': predictions[i], 'individual_predictions': individual_predictions[i] if individual_predictions else None} for i in range(len(predictions))], 'model_info': {'base_estimator_type': base_estimator_type, 'n_estimators': params.get('n_estimators', 10), 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setBaggingInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for bagging ensemble
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for bagging ensemble
        const baggingInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            base_estimator_type: parameters.base_estimator_type || 'decision_tree',
            n_estimators: parameters.n_estimators || 10,
            max_depth: parameters.max_depth || 10,
            kernel: parameters.kernel || 'rbf',
            C: parameters.C || 1.0,
            max_samples: parameters.max_samples || 1.0,
            max_features: parameters.max_features || 1.0,
            bootstrap: parameters.bootstrap !== undefined ? parameters.bootstrap : true,
            bootstrap_features: parameters.bootstrap_features !== undefined ? parameters.bootstrap_features : false,
            return_individual_predictions: parameters.return_individual_predictions !== undefined ? parameters.return_individual_predictions : false
          }
        };
        
        return {
          json: baggingInput
        };
      `
    }
  },
  {
    "id": "processBaggingResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process bagging ensemble results
        const baggingResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = baggingResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'Bagging Ensemble',
          base_estimator_type: baggingResults.model_info.base_estimator_type,
          n_estimators: baggingResults.model_info.n_estimators,
          parameters: baggingResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            features: p.features,
            prediction: Math.round(p.prediction * 100) / 100,
            individual_predictions: p.individual_predictions ? 
              p.individual_predictions.map(pred => Math.round(pred * 100) / 100) : null
          }))
        };
        
        return {
          json: formattedResults
        };
      `
    }
  }
]
```

## 多様性を考慮したアンサンブルの実装

多様性を考慮したアンサンブルは、予測の多様性を明示的に促進することで、より堅牢な予測を実現する手法です。異なるアルゴリズム、異なるデータサブセット、異なる特徴量サブセットなどを組み合わせます。

### n8nによる多様性を考慮したアンサンブル実装

```javascript
// n8n workflow: Diversity-Aware Ensemble Implementation
// Function node for diversity-aware ensemble
[
  {
    "id": "diversityAwareEnsemble",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Predictions from multiple models and ensemble parameters
        const modelPredictions = $input.item.json.model_predictions || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const diversityWeight = parameters.diversity_weight || 0.5;
        const accuracyMetric = parameters.accuracy_metric || 'rmse';
        const modelAccuracies = parameters.model_accuracies || [];
        
        // Validate input
        if (modelPredictions.length === 0) {
          throw new Error('No model predictions provided');
        }
        
        // Extract test data and predictions
        const testData = [];
        const allPredictions = [];
        
        // Organize predictions by test case
        modelPredictions.forEach(modelResult => {
          const modelName = modelResult.model_name;
          const predictions = modelResult.predictions || [];
          
          predictions.forEach((pred, idx) => {
            // Initialize test case if not exists
            if (!testData[idx]) {
              testData[idx] = pred.features || pred.sequence || \`Test case \${idx + 1}\`;
            }
            
            // Initialize predictions array if not exists
            if (!allPredictions[idx]) {
              allPredictions[idx] = [];
            }
            
            // Add prediction
            allPredictions[idx].push({
              model: modelName,
              prediction: pred.prediction
            });
          });
        });
        
        // Calculate diversity matrix for each test case
        const diversityMatrices = [];
        
        for (const predictions of allPredictions) {
          const n = predictions.length;
          const diversityMatrix = Array(n).fill().map(() => Array(n).fill(0));
          
          for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
              if (i === j) {
                diversityMatrix[i][j] = 0;
              } else {
                // Calculate diversity as absolute difference between predictions
                diversityMatrix[i][j] = Math.abs(predictions[i].prediction - predictions[j].prediction);
              }
            }
          }
          
          diversityMatrices.push(diversityMatrix);
        }
        
        // Calculate model weights based on accuracy and diversity
        const calculateModelWeights = (predictions, diversityMatrix) => {
          const n = predictions.length;
          const weights = Array(n).fill(0);
          
          // Calculate accuracy weights
          for (let i = 0; i < n; i++) {
            const modelName = predictions[i].model;
            const accuracyIndex = modelAccuracies.findIndex(acc => acc.model === modelName);
            
            if (accuracyIndex >= 0) {
              const accuracy = modelAccuracies[accuracyIndex].accuracy;
              
              // For RMSE and MAE, lower is better, so invert
              if (accuracyMetric === 'rmse' || accuracyMetric === 'mae') {
                weights[i] = 1 / (accuracy + 0.0001); // Avoid division by zero
              } else {
                weights[i] = accuracy;
              }
            } else {
              weights[i] = 1; // Default weight if accuracy not provided
            }
          }
          
          // Normalize accuracy weights
          const sumAccuracyWeights = weights.reduce((sum, w) => sum + w, 0);
          for (let i = 0; i < n; i++) {
            weights[i] /= sumAccuracyWeights;
          }
          
          // Calculate diversity weights
          const diversityWeights = Array(n).fill(0);
          
          for (let i = 0; i < n; i++) {
            // Sum of diversities with other models
            diversityWeights[i] = diversityMatrix[i].reduce((sum, d) => sum + d, 0);
          }
          
          // Normalize diversity weights
          const sumDiversityWeights = diversityWeights.reduce((sum, w) => sum + w, 0);
          for (let i = 0; i < n; i++) {
            diversityWeights[i] = sumDiversityWeights > 0 ? diversityWeights[i] / sumDiversityWeights : 1 / n;
          }
          
          // Combine accuracy and diversity weights
          const combinedWeights = Array(n).fill(0);
          
          for (let i = 0; i < n; i++) {
            combinedWeights[i] = (1 - diversityWeight) * weights[i] + diversityWeight * diversityWeights[i];
          }
          
          // Normalize combined weights
          const sumCombinedWeights = combinedWeights.reduce((sum, w) => sum + w, 0);
          for (let i = 0; i < n; i++) {
            combinedWeights[i] = sumCombinedWeights > 0 ? combinedWeights[i] / sumCombinedWeights : 1 / n;
          }
          
          return combinedWeights;
        };
        
        // Generate ensemble predictions
        const ensemblePredictions = [];
        
        for (let i = 0; i < testData.length; i++) {
          const testCase = testData[i];
          const predictions = allPredictions[i] || [];
          const diversityMatrix = diversityMatrices[i] || [];
          
          // Skip if no predictions
          if (predictions.length === 0) continue;
          
          // Calculate weights
          const weights = calculateModelWeights(predictions, diversityMatrix);
          
          // Calculate weighted average
          let weightedSum = 0;
          
          for (let j = 0; j < predictions.length; j++) {
            weightedSum += predictions[j].prediction * weights[j];
          }
          
          ensemblePredictions.push({
            test_case: i + 1,
            features: testCase,
            individual_predictions: predictions.map((p, idx) => ({
              model: p.model,
              prediction: p.prediction,
              weight: weights[idx]
            })),
            ensemble_prediction: weightedSum
          });
        }
        
        return {
          json: {
            ensemble_type: 'Diversity-Aware Ensemble',
            diversity_weight: diversityWeight,
            accuracy_metric: accuracyMetric,
            num_models: modelPredictions.length,
            model_names: modelPredictions.map(m => m.model_name),
            predictions: ensemblePredictions
          }
        };
      `
    }
  }
]
```

### 多様性を考慮したアンサンブルの使用例

```javascript
// n8n workflow: Diversity-Aware Ensemble Usage Example
// HTTP Request node to call diversity-aware ensemble
[
  {
    "id": "httpRequest",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/diversity-aware-ensemble",
      "method": "POST",
      "bodyContent": "{\n  \"model_predictions\": [\n    {\n      \"model_name\": \"ARIMA\",\n      \"predictions\": [\n        {\"features\": [1, 2, 3, 4, 5], \"prediction\": 6.2},\n        {\"features\": [2, 3, 4, 5, 6], \"prediction\": 7.1},\n        {\"features\": [3, 4, 5, 6, 7], \"prediction\": 8.3}\n      ]\n    },\n    {\n      \"model_name\": \"RandomForest\",\n      \"predictions\": [\n        {\"features\": [1, 2, 3, 4, 5], \"prediction\": 6.5},\n        {\"features\": [2, 3, 4, 5, 6], \"prediction\": 7.4},\n        {\"features\": [3, 4, 5, 6, 7], \"prediction\": 8.0}\n      ]\n    },\n    {\n      \"model_name\": \"LSTM\",\n      \"predictions\": [\n        {\"features\": [1, 2, 3, 4, 5], \"prediction\": 6.0},\n        {\"features\": [2, 3, 4, 5, 6], \"prediction\": 7.2},\n        {\"features\": [3, 4, 5, 6, 7], \"prediction\": 8.1}\n      ]\n    }\n  ],\n  \"parameters\": {\n    \"diversity_weight\": 0.3,\n    \"accuracy_metric\": \"rmse\",\n    \"model_accuracies\": [\n      {\"model\": \"ARIMA\", \"accuracy\": 0.8},\n      {\"model\": \"RandomForest\", \"accuracy\": 0.5},\n      {\"model\": \"LSTM\", \"accuracy\": 0.6}\n    ]\n  }\n}",
      "bodyContentType": "json"
    }
  }
]
```

## アンサンブル手法の評価と選択

アンサンブル手法の選択は、予測タスクの性質、データの特性、計算リソースなどに依存します。n8nを使用してアンサンブル手法を評価し、最適な手法を選択する例を示します。

```javascript
// n8n workflow: Ensemble Method Evaluation and Selection
// Function node for ensemble evaluation
[
  {
    "id": "ensembleEvaluation",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Predictions from multiple ensemble methods and evaluation parameters
        const ensemblePredictions = $input.item.json.ensemble_predictions || [];
        const actualValues = $input.item.json.actual_values || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const evaluationMetrics = parameters.evaluation_metrics || ['rmse', 'mae', 'mape'];
        
        // Validate input
        if (ensemblePredictions.length === 0) {
          throw new Error('No ensemble predictions provided');
        }
        
        if (actualValues.length === 0) {
          throw new Error('No actual values provided');
        }
        
        // Calculate evaluation metrics for each ensemble method
        const evaluationResults = [];
        
        for (const ensemble of ensemblePredictions) {
          const ensembleName = ensemble.ensemble_name;
          const predictions = ensemble.predictions || [];
          
          // Skip if no predictions
          if (predictions.length === 0) continue;
          
          // Calculate metrics
          const metrics = {};
          
          if (evaluationMetrics.includes('rmse')) {
            let sumSquaredError = 0;
            let count = 0;
            
            for (let i = 0; i < predictions.length; i++) {
              if (i < actualValues.length) {
                const error = predictions[i] - actualValues[i];
                sumSquaredError += error * error;
                count++;
              }
            }
            
            metrics.rmse = count > 0 ? Math.sqrt(sumSquaredError / count) : null;
          }
          
          if (evaluationMetrics.includes('mae')) {
            let sumAbsError = 0;
            let count = 0;
            
            for (let i = 0; i < predictions.length; i++) {
              if (i < actualValues.length) {
                const error = Math.abs(predictions[i] - actualValues[i]);
                sumAbsError += error;
                count++;
              }
            }
            
            metrics.mae = count > 0 ? sumAbsError / count : null;
          }
          
          if (evaluationMetrics.includes('mape')) {
            let sumAbsPercentError = 0;
            let count = 0;
            
            for (let i = 0; i < predictions.length; i++) {
              if (i < actualValues.length && actualValues[i] !== 0) {
                const percentError = Math.abs((predictions[i] - actualValues[i]) / actualValues[i]) * 100;
                sumAbsPercentError += percentError;
                count++;
              }
            }
            
            metrics.mape = count > 0 ? sumAbsPercentError / count : null;
          }
          
          evaluationResults.push({
            ensemble_name: ensembleName,
            metrics: metrics
          });
        }
        
        // Rank ensemble methods based on metrics
        const rankEnsembles = () => {
          const ranks = {};
          
          // Initialize ranks
          for (const ensemble of evaluationResults) {
            ranks[ensemble.ensemble_name] = 0;
          }
          
          // Rank by each metric
          for (const metric of evaluationMetrics) {
            // Sort ensembles by metric (lower is better)
            const sorted = [...evaluationResults]
              .filter(e => e.metrics[metric] !== null)
              .sort((a, b) => a.metrics[metric] - b.metrics[metric]);
            
            // Assign ranks
            for (let i = 0; i < sorted.length; i++) {
              ranks[sorted[i].ensemble_name] += i + 1;
            }
          }
          
          // Calculate final ranks
          return Object.entries(ranks)
            .map(([name, rank]) => ({ ensemble_name: name, rank }))
            .sort((a, b) => a.rank - b.rank);
        };
        
        const rankedEnsembles = rankEnsembles();
        const bestEnsemble = rankedEnsembles.length > 0 ? rankedEnsembles[0].ensemble_name : null;
        
        return {
          json: {
            evaluation_metrics: evaluationMetrics,
            evaluation_results: evaluationResults,
            ranked_ensembles: rankedEnsembles,
            best_ensemble: bestEnsemble
          }
        };
      `
    }
  }
]
```

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおけるアンサンブル手法の実装について詳細に解説しました。平均化アンサンブル、スタッキングアンサンブル、ブースティングアンサンブル、バギングアンサンブル、多様性を考慮したアンサンブルなど、主要なアンサンブル手法のn8nによる実装例を提供しました。また、アンサンブル手法の評価と選択の実装例も紹介しました。

次のセクションでは、n8nによるモデル統合ワークフローについて詳細に解説します。
