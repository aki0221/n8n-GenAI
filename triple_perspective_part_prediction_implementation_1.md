# 予測モデルの実装と統合（パート2-2：機械学習モデルの実装）

## 機械学習モデルによる予測の概要

トリプルパースペクティブ型戦略AIレーダーにおける予測エンジンでは、時系列予測モデルに加えて、より複雑なパターンを捉えるために機械学習モデルを活用します。機械学習モデルは、多変量データから非線形関係を学習し、将来の状態を予測する能力に優れています。本セクションでは、主要な機械学習予測モデルのn8nによる実装について解説します。

### 機械学習予測の基本概念

機械学習による予測は、以下のステップで行われます：

1. **特徴量エンジニアリング**: 生データから予測に有用な特徴を抽出・変換
2. **モデルトレーニング**: 過去のデータからパターンを学習
3. **モデル評価**: 学習したモデルの性能を検証
4. **予測生成**: 学習したモデルを使用して将来の値を予測

トリプルパースペクティブ型戦略AIレーダーでは、以下のような機械学習モデルを活用します：

- ランダムフォレスト回帰
- 勾配ブースティング回帰
- サポートベクター回帰
- k近傍回帰

## ランダムフォレスト回帰モデルの実装

ランダムフォレストは、複数の決定木を組み合わせたアンサンブル学習手法です。個々の決定木の予測を平均化することで、過学習を抑制し、堅牢な予測を実現します。

### n8nによるランダムフォレスト回帰モデル実装

```javascript
// n8n workflow: Random Forest Regression Implementation
// Function node for Random Forest model
[
  {
    "id": "randomForestImplementation",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Training data and model parameters
        const trainingData = $input.item.json.training_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const nEstimators = parameters.n_estimators || 100;
        const maxDepth = parameters.max_depth || 10;
        const minSamplesSplit = parameters.min_samples_split || 2;
        const maxFeatures = parameters.max_features || 'auto';
        
        // Validate input
        if (trainingData.length === 0) {
          throw new Error('No training data provided');
        }
        
        // In a real implementation, this would use a proper Random Forest algorithm
        // For demonstration, we'll implement a simplified version
        
        // Step 1: Prepare data
        const features = trainingData.map(item => item.features || []);
        const targets = trainingData.map(item => item.target || 0);
        
        // Step 2: Create and train multiple decision trees
        const trees = [];
        for (let i = 0; i < nEstimators; i++) {
          // Create a bootstrap sample
          const bootstrapSample = createBootstrapSample(features, targets);
          
          // Train a decision tree
          const tree = trainDecisionTree(
            bootstrapSample.features, 
            bootstrapSample.targets, 
            maxDepth, 
            minSamplesSplit, 
            maxFeatures
          );
          
          trees.push(tree);
        }
        
        // Step 3: Generate predictions for test data
        const testData = $input.item.json.test_data || [];
        const predictions = [];
        
        for (const dataPoint of testData) {
          const features = dataPoint.features || [];
          
          // Get predictions from all trees
          const treePredictions = trees.map(tree => predictWithTree(tree, features));
          
          // Average the predictions
          const avgPrediction = treePredictions.reduce((sum, val) => sum + val, 0) / treePredictions.length;
          
          predictions.push({
            features: features,
            prediction: avgPrediction,
            tree_predictions: treePredictions
          });
        }
        
        return {
          json: {
            model_type: 'Random Forest Regression',
            parameters: {
              n_estimators: nEstimators,
              max_depth: maxDepth,
              min_samples_split: minSamplesSplit,
              max_features: maxFeatures
            },
            num_trees: trees.length,
            predictions: predictions,
            model_info: {
              training_samples: trainingData.length,
              test_samples: testData.length
            }
          }
        };
        
        // Helper function: Create bootstrap sample
        function createBootstrapSample(features, targets) {
          const sampleFeatures = [];
          const sampleTargets = [];
          const n = features.length;
          
          for (let i = 0; i < n; i++) {
            const idx = Math.floor(Math.random() * n);
            sampleFeatures.push(features[idx]);
            sampleTargets.push(targets[idx]);
          }
          
          return {
            features: sampleFeatures,
            targets: sampleTargets
          };
        }
        
        // Helper function: Train decision tree
        function trainDecisionTree(features, targets, maxDepth, minSamplesSplit, maxFeatures) {
          // In a real implementation, this would use a proper decision tree algorithm
          // For demonstration, we'll create a simplified tree structure
          
          // Create a simple tree structure
          const tree = {
            depth: 0,
            split_feature: null,
            split_value: null,
            left: null,
            right: null,
            is_leaf: false,
            prediction: null
          };
          
          // Recursive function to build the tree
          function buildTree(nodeFeatures, nodeTargets, depth) {
            // Create a node
            const node = {
              depth: depth,
              split_feature: null,
              split_value: null,
              left: null,
              right: null,
              is_leaf: false,
              prediction: null
            };
            
            // Check stopping criteria
            if (depth >= maxDepth || nodeFeatures.length < minSamplesSplit) {
              node.is_leaf = true;
              node.prediction = calculateMean(nodeTargets);
              return node;
            }
            
            // Find the best split
            const bestSplit = findBestSplit(nodeFeatures, nodeTargets, maxFeatures);
            
            // If no good split found, make it a leaf
            if (!bestSplit) {
              node.is_leaf = true;
              node.prediction = calculateMean(nodeTargets);
              return node;
            }
            
            // Apply the split
            node.split_feature = bestSplit.feature;
            node.split_value = bestSplit.value;
            
            const splitResult = applySplit(
              nodeFeatures, 
              nodeTargets, 
              bestSplit.feature, 
              bestSplit.value
            );
            
            // Build left and right subtrees
            node.left = buildTree(splitResult.leftFeatures, splitResult.leftTargets, depth + 1);
            node.right = buildTree(splitResult.rightFeatures, splitResult.rightTargets, depth + 1);
            
            return node;
          }
          
          // Build the tree
          return buildTree(features, targets, 0);
        }
        
        // Helper function: Find best split
        function findBestSplit(features, targets, maxFeatures) {
          // In a real implementation, this would use proper criteria like Gini or entropy
          // For demonstration, we'll use a simplified approach
          
          // If no features, return null
          if (features.length === 0 || features[0].length === 0) {
            return null;
          }
          
          // Determine number of features to consider
          const numFeatures = features[0].length;
          let featuresToConsider = numFeatures;
          
          if (maxFeatures === 'sqrt') {
            featuresToConsider = Math.floor(Math.sqrt(numFeatures));
          } else if (maxFeatures === 'log2') {
            featuresToConsider = Math.floor(Math.log2(numFeatures));
          } else if (typeof maxFeatures === 'number') {
            featuresToConsider = Math.min(maxFeatures, numFeatures);
          }
          
          // Randomly select features to consider
          const featureIndices = [];
          for (let i = 0; i < numFeatures; i++) {
            featureIndices.push(i);
          }
          shuffleArray(featureIndices);
          const selectedFeatures = featureIndices.slice(0, featuresToConsider);
          
          // Find the best split among selected features
          let bestSplit = null;
          let bestScore = Infinity;
          
          for (const featureIdx of selectedFeatures) {
            // Get unique values for this feature
            const values = features.map(f => f[featureIdx]);
            const uniqueValues = [...new Set(values)];
            
            // Try each value as a split point
            for (const value of uniqueValues) {
              const splitResult = applySplit(features, targets, featureIdx, value);
              
              // Skip if split is too unbalanced
              if (splitResult.leftTargets.length < 1 || splitResult.rightTargets.length < 1) {
                continue;
              }
              
              // Calculate score (MSE)
              const leftMean = calculateMean(splitResult.leftTargets);
              const rightMean = calculateMean(splitResult.rightTargets);
              
              const leftMSE = calculateMSE(splitResult.leftTargets, leftMean);
              const rightMSE = calculateMSE(splitResult.rightTargets, rightMean);
              
              const leftWeight = splitResult.leftTargets.length / targets.length;
              const rightWeight = splitResult.rightTargets.length / targets.length;
              
              const score = leftWeight * leftMSE + rightWeight * rightMSE;
              
              // Update best split if this is better
              if (score < bestScore) {
                bestScore = score;
                bestSplit = {
                  feature: featureIdx,
                  value: value,
                  score: score
                };
              }
            }
          }
          
          return bestSplit;
        }
        
        // Helper function: Apply split
        function applySplit(features, targets, featureIdx, value) {
          const leftFeatures = [];
          const leftTargets = [];
          const rightFeatures = [];
          const rightTargets = [];
          
          for (let i = 0; i < features.length; i++) {
            if (features[i][featureIdx] <= value) {
              leftFeatures.push(features[i]);
              leftTargets.push(targets[i]);
            } else {
              rightFeatures.push(features[i]);
              rightTargets.push(targets[i]);
            }
          }
          
          return {
            leftFeatures,
            leftTargets,
            rightFeatures,
            rightTargets
          };
        }
        
        // Helper function: Predict with tree
        function predictWithTree(tree, features) {
          let node = tree;
          
          while (!node.is_leaf) {
            if (features[node.split_feature] <= node.split_value) {
              node = node.left;
            } else {
              node = node.right;
            }
          }
          
          return node.prediction;
        }
        
        // Helper function: Calculate mean
        function calculateMean(values) {
          return values.reduce((sum, val) => sum + val, 0) / values.length;
        }
        
        // Helper function: Calculate MSE
        function calculateMSE(values, mean) {
          return values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
        }
        
        // Helper function: Shuffle array
        function shuffleArray(array) {
          for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
          }
        }
      `
    }
  }
]
```

### ランダムフォレストモデルの使用例

```javascript
// n8n workflow: Random Forest Model Usage Example
// HTTP Request node to call Random Forest model
[
  {
    "id": "httpRequest",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/random-forest-model",
      "method": "POST",
      "bodyContent": "{\n  \"training_data\": [\n    {\"features\": [1, 2, 3], \"target\": 10},\n    {\"features\": [2, 3, 4], \"target\": 15},\n    {\"features\": [3, 4, 5], \"target\": 20},\n    {\"features\": [4, 5, 6], \"target\": 25},\n    {\"features\": [5, 6, 7], \"target\": 30}\n  ],\n  \"test_data\": [\n    {\"features\": [2, 3, 4]},\n    {\"features\": [4, 5, 6]},\n    {\"features\": [6, 7, 8]}\n  ],\n  \"parameters\": {\n    \"n_estimators\": 50,\n    \"max_depth\": 5,\n    \"min_samples_split\": 2,\n    \"max_features\": \"sqrt\"\n  }\n}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "processRandomForestResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process Random Forest model results
        const rfResults = $input.item.json;
        
        // Extract predictions
        const predictions = rfResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: rfResults.model_type,
          parameters: rfResults.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            features: p.features,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          model_info: rfResults.model_info
        };
        
        return {
          json: formattedResults
        };
      `
    }
  }
]
```

## 勾配ブースティング回帰モデルの実装

勾配ブースティングは、弱学習器（通常は決定木）を逐次的に追加し、各ステップで前のモデルの誤差を修正していくアンサンブル手法です。XGBoost、LightGBM、CatBoostなどの実装が広く使われています。

### n8nによる勾配ブースティング回帰モデル実装

```javascript
// n8n workflow: Gradient Boosting Regression Implementation
// Function node for Gradient Boosting model
[
  {
    "id": "gradientBoostingImplementation",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Training data and model parameters
        const trainingData = $input.item.json.training_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const nEstimators = parameters.n_estimators || 100;
        const learningRate = parameters.learning_rate || 0.1;
        const maxDepth = parameters.max_depth || 3;
        const subsample = parameters.subsample || 1.0;
        
        // Validate input
        if (trainingData.length === 0) {
          throw new Error('No training data provided');
        }
        
        // In a real implementation, this would use a proper Gradient Boosting algorithm
        // For demonstration, we'll implement a simplified version
        
        // Step 1: Prepare data
        const features = trainingData.map(item => item.features || []);
        const targets = trainingData.map(item => item.target || 0);
        
        // Step 2: Initialize predictions with the mean of targets
        const initialPrediction = calculateMean(targets);
        let currentPredictions = Array(targets.length).fill(initialPrediction);
        
        // Step 3: Train boosting rounds
        const trees = [];
        
        for (let i = 0; i < nEstimators; i++) {
          // Calculate residuals (negative gradients)
          const residuals = targets.map((target, idx) => target - currentPredictions[idx]);
          
          // Create a subsample if specified
          let sampleFeatures = features;
          let sampleResiduals = residuals;
          
          if (subsample < 1.0) {
            const sampleIndices = createSubsample(features.length, subsample);
            sampleFeatures = sampleIndices.map(idx => features[idx]);
            sampleResiduals = sampleIndices.map(idx => residuals[idx]);
          }
          
          // Train a decision tree on residuals
          const tree = trainDecisionTree(
            sampleFeatures, 
            sampleResiduals, 
            maxDepth
          );
          
          trees.push(tree);
          
          // Update predictions
          for (let j = 0; j < features.length; j++) {
            const treePrediction = predictWithTree(tree, features[j]);
            currentPredictions[j] += learningRate * treePrediction;
          }
        }
        
        // Step 4: Generate predictions for test data
        const testData = $input.item.json.test_data || [];
        const predictions = [];
        
        for (const dataPoint of testData) {
          const features = dataPoint.features || [];
          
          // Start with initial prediction
          let prediction = initialPrediction;
          
          // Add contributions from each tree
          for (const tree of trees) {
            prediction += learningRate * predictWithTree(tree, features);
          }
          
          predictions.push({
            features: features,
            prediction: prediction
          });
        }
        
        return {
          json: {
            model_type: 'Gradient Boosting Regression',
            parameters: {
              n_estimators: nEstimators,
              learning_rate: learningRate,
              max_depth: maxDepth,
              subsample: subsample
            },
            initial_prediction: initialPrediction,
            num_trees: trees.length,
            predictions: predictions,
            model_info: {
              training_samples: trainingData.length,
              test_samples: testData.length
            }
          }
        };
        
        // Helper function: Create subsample
        function createSubsample(size, ratio) {
          const indices = [];
          const sampleSize = Math.floor(size * ratio);
          
          // Create array of indices
          const allIndices = Array.from({ length: size }, (_, i) => i);
          
          // Shuffle and take first sampleSize elements
          shuffleArray(allIndices);
          return allIndices.slice(0, sampleSize);
        }
        
        // Helper function: Train decision tree
        function trainDecisionTree(features, targets, maxDepth) {
          // In a real implementation, this would use a proper decision tree algorithm
          // For demonstration, we'll create a simplified tree structure
          
          // Create a simple tree structure
          const tree = {
            depth: 0,
            split_feature: null,
            split_value: null,
            left: null,
            right: null,
            is_leaf: false,
            prediction: null
          };
          
          // Recursive function to build the tree
          function buildTree(nodeFeatures, nodeTargets, depth) {
            // Create a node
            const node = {
              depth: depth,
              split_feature: null,
              split_value: null,
              left: null,
              right: null,
              is_leaf: false,
              prediction: null
            };
            
            // Check stopping criteria
            if (depth >= maxDepth || nodeFeatures.length <= 1) {
              node.is_leaf = true;
              node.prediction = calculateMean(nodeTargets);
              return node;
            }
            
            // Find the best split
            const bestSplit = findBestSplit(nodeFeatures, nodeTargets);
            
            // If no good split found, make it a leaf
            if (!bestSplit) {
              node.is_leaf = true;
              node.prediction = calculateMean(nodeTargets);
              return node;
            }
            
            // Apply the split
            node.split_feature = bestSplit.feature;
            node.split_value = bestSplit.value;
            
            const splitResult = applySplit(
              nodeFeatures, 
              nodeTargets, 
              bestSplit.feature, 
              bestSplit.value
            );
            
            // Build left and right subtrees
            node.left = buildTree(splitResult.leftFeatures, splitResult.leftTargets, depth + 1);
            node.right = buildTree(splitResult.rightFeatures, splitResult.rightTargets, depth + 1);
            
            return node;
          }
          
          // Build the tree
          return buildTree(features, targets, 0);
        }
        
        // Helper function: Find best split
        function findBestSplit(features, targets) {
          // In a real implementation, this would use proper criteria like MSE
          // For demonstration, we'll use a simplified approach
          
          // If no features, return null
          if (features.length === 0 || features[0].length === 0) {
            return null;
          }
          
          // Find the best split
          let bestSplit = null;
          let bestScore = Infinity;
          
          for (let featureIdx = 0; featureIdx < features[0].length; featureIdx++) {
            // Get unique values for this feature
            const values = features.map(f => f[featureIdx]);
            const uniqueValues = [...new Set(values)];
            
            // Try each value as a split point
            for (const value of uniqueValues) {
              const splitResult = applySplit(features, targets, featureIdx, value);
              
              // Skip if split is too unbalanced
              if (splitResult.leftTargets.length < 1 || splitResult.rightTargets.length < 1) {
                continue;
              }
              
              // Calculate score (MSE)
              const leftMean = calculateMean(splitResult.leftTargets);
              const rightMean = calculateMean(splitResult.rightTargets);
              
              const leftMSE = calculateMSE(splitResult.leftTargets, leftMean);
              const rightMSE = calculateMSE(splitResult.rightTargets, rightMean);
              
              const leftWeight = splitResult.leftTargets.length / targets.length;
              const rightWeight = splitResult.rightTargets.length / targets.length;
              
              const score = leftWeight * leftMSE + rightWeight * rightMSE;
              
              // Update best split if this is better
              if (score < bestScore) {
                bestScore = score;
                bestSplit = {
                  feature: featureIdx,
                  value: value,
                  score: score
                };
              }
            }
          }
          
          return bestSplit;
        }
        
        // Helper function: Apply split
        function applySplit(features, targets, featureIdx, value) {
          const leftFeatures = [];
          const leftTargets = [];
          const rightFeatures = [];
          const rightTargets = [];
          
          for (let i = 0; i < features.length; i++) {
            if (features[i][featureIdx] <= value) {
              leftFeatures.push(features[i]);
              leftTargets.push(targets[i]);
            } else {
              rightFeatures.push(features[i]);
              rightTargets.push(targets[i]);
            }
          }
          
          return {
            leftFeatures,
            leftTargets,
            rightFeatures,
            rightTargets
          };
        }
        
        // Helper function: Predict with tree
        function predictWithTree(tree, features) {
          let node = tree;
          
          while (!node.is_leaf) {
            if (features[node.split_feature] <= node.split_value) {
              node = node.left;
            } else {
              node = node.right;
            }
          }
          
          return node.prediction;
        }
        
        // Helper function: Calculate mean
        function calculateMean(values) {
          if (values.length === 0) return 0;
          return values.reduce((sum, val) => sum + val, 0) / values.length;
        }
        
        // Helper function: Calculate MSE
        function calculateMSE(values, mean) {
          if (values.length === 0) return 0;
          return values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
        }
        
        // Helper function: Shuffle array
        function shuffleArray(array) {
          for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
          }
        }
      `
    }
  }
]
```

## サポートベクター回帰（SVR）モデルの実装

サポートベクター回帰（SVR）は、サポートベクターマシン（SVM）の回帰問題への応用です。SVRは、許容誤差の範囲内で可能な限り多くのデータポイントを含む「チューブ」を見つけることを目指します。

### n8nからPythonを使用したSVR実装

```javascript
// n8n workflow: Support Vector Regression Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); from sklearn.svm import SVR; import numpy as np; # Extract data X_train = np.array([item['features'] for item in data['training_data']]); y_train = np.array([item['target'] for item in data['training_data']]); # Create and fit model params = data['parameters']; model = SVR(kernel=params.get('kernel', 'rbf'), C=params.get('C', 1.0), epsilon=params.get('epsilon', 0.1), gamma=params.get('gamma', 'scale')); model.fit(X_train, y_train); # Make predictions X_test = np.array([item['features'] for item in data['test_data']]); predictions = model.predict(X_test).tolist(); # Prepare output result = {'predictions': [{'features': data['test_data'][i]['features'], 'prediction': predictions[i]} for i in range(len(predictions))], 'model_info': {'support_vectors_count': len(model.support_vectors_), 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setSVRInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for SVR model
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for SVR
        const svrInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            kernel: parameters.kernel || 'rbf',
            C: parameters.C || 1.0,
            epsilon: parameters.epsilon || 0.1,
            gamma: parameters.gamma || 'scale'
          }
        };
        
        return {
          json: svrInput
        };
      `
    }
  },
  {
    "id": "processSVRResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process SVR model results
        const svrResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = svrResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'Support Vector Regression',
          parameters: svrResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            features: p.features,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          model_info: {
            support_vectors_count: svrResults.model_info.support_vectors_count
          }
        };
        
        return {
          json: formattedResults
        };
      `
    }
  }
]
```

## k近傍回帰（KNN）モデルの実装

k近傍回帰（KNN）は、新しいデータポイントの予測値を、トレーニングデータセット内のk個の最も近いデータポイントの平均として計算するシンプルな非パラメトリックモデルです。

### n8nによるk近傍回帰モデル実装

```javascript
// n8n workflow: k-Nearest Neighbors Regression Implementation
// Function node for KNN model
[
  {
    "id": "knnImplementation",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Training data and model parameters
        const trainingData = $input.item.json.training_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const k = parameters.k || 5;
        const weightType = parameters.weight_type || 'uniform';
        const distanceMetric = parameters.distance_metric || 'euclidean';
        
        // Validate input
        if (trainingData.length === 0) {
          throw new Error('No training data provided');
        }
        
        if (k <= 0 || k > trainingData.length) {
          throw new Error(\`Invalid k value: \${k}. Must be between 1 and \${trainingData.length}\`);
        }
        
        // Step 1: Prepare data
        const features = trainingData.map(item => item.features || []);
        const targets = trainingData.map(item => item.target || 0);
        
        // Step 2: Generate predictions for test data
        const testData = $input.item.json.test_data || [];
        const predictions = [];
        
        for (const dataPoint of testData) {
          const testFeatures = dataPoint.features || [];
          
          // Calculate distances to all training points
          const distances = features.map((trainFeatures, idx) => ({
            distance: calculateDistance(testFeatures, trainFeatures, distanceMetric),
            target: targets[idx]
          }));
          
          // Sort by distance
          distances.sort((a, b) => a.distance - b.distance);
          
          // Take k nearest neighbors
          const neighbors = distances.slice(0, k);
          
          // Calculate prediction based on weight type
          let prediction;
          
          if (weightType === 'uniform') {
            // Simple average
            prediction = neighbors.reduce((sum, n) => sum + n.target, 0) / k;
          } else if (weightType === 'distance') {
            // Distance-weighted average
            let weightedSum = 0;
            let weightSum = 0;
            
            for (const neighbor of neighbors) {
              const weight = 1 / (neighbor.distance + 0.00001); // Avoid division by zero
              weightedSum += neighbor.target * weight;
              weightSum += weight;
            }
            
            prediction = weightSum > 0 ? weightedSum / weightSum : 0;
          }
          
          predictions.push({
            features: testFeatures,
            prediction: prediction,
            neighbors: neighbors.map(n => ({
              distance: n.distance,
              target: n.target
            }))
          });
        }
        
        return {
          json: {
            model_type: 'k-Nearest Neighbors Regression',
            parameters: {
              k,
              weight_type: weightType,
              distance_metric: distanceMetric
            },
            predictions: predictions,
            model_info: {
              training_samples: trainingData.length,
              test_samples: testData.length
            }
          }
        };
        
        // Helper function: Calculate distance
        function calculateDistance(features1, features2, metric) {
          if (features1.length !== features2.length) {
            throw new Error('Feature vectors must have the same length');
          }
          
          switch (metric) {
            case 'euclidean':
              return Math.sqrt(
                features1.reduce((sum, val, idx) => sum + Math.pow(val - features2[idx], 2), 0)
              );
            
            case 'manhattan':
              return features1.reduce((sum, val, idx) => sum + Math.abs(val - features2[idx]), 0);
            
            case 'cosine':
              let dotProduct = 0;
              let norm1 = 0;
              let norm2 = 0;
              
              for (let i = 0; i < features1.length; i++) {
                dotProduct += features1[i] * features2[i];
                norm1 += Math.pow(features1[i], 2);
                norm2 += Math.pow(features2[i], 2);
              }
              
              norm1 = Math.sqrt(norm1);
              norm2 = Math.sqrt(norm2);
              
              if (norm1 === 0 || norm2 === 0) return 1; // Maximum distance
              
              return 1 - (dotProduct / (norm1 * norm2));
            
            default:
              return Math.sqrt(
                features1.reduce((sum, val, idx) => sum + Math.pow(val - features2[idx], 2), 0)
              );
          }
        }
      `
    }
  }
]
```

## 機械学習モデルの特徴量エンジニアリング

機械学習モデルの性能は、適切な特徴量エンジニアリングに大きく依存します。n8nを使用して特徴量エンジニアリングを行う例を示します。

```javascript
// n8n workflow: Feature Engineering for ML Models
// Function node for feature engineering
[
  {
    "id": "featureEngineering",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Raw data and feature engineering parameters
        const rawData = $input.item.json.raw_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Validate input
        if (rawData.length === 0) {
          throw new Error('No raw data provided');
        }
        
        // Step 1: Handle missing values
        const dataWithoutMissing = handleMissingValues(rawData, parameters.missing_strategy || 'mean');
        
        // Step 2: Scale numerical features
        const scaledData = scaleFeatures(dataWithoutMissing, parameters.scaling_method || 'standard');
        
        // Step 3: Create polynomial features if specified
        let processedData = scaledData;
        if (parameters.create_polynomial && parameters.polynomial_degree) {
          processedData = createPolynomialFeatures(scaledData, parameters.polynomial_degree);
        }
        
        // Step 4: Perform feature selection if specified
        if (parameters.feature_selection && parameters.num_features) {
          processedData = selectFeatures(processedData, parameters.num_features);
        }
        
        return {
          json: {
            original_data_size: rawData.length,
            processed_data_size: processedData.length,
            feature_count: processedData.length > 0 ? processedData[0].features.length : 0,
            processed_data: processedData
          }
        };
        
        // Helper function: Handle missing values
        function handleMissingValues(data, strategy) {
          // Find columns with missing values
          const featureCount = data[0].features.length;
          const missingValueCounts = Array(featureCount).fill(0);
          
          for (const item of data) {
            for (let i = 0; i < featureCount; i++) {
              if (item.features[i] === null || item.features[i] === undefined || isNaN(item.features[i])) {
                missingValueCounts[i]++;
              }
            }
          }
          
          // Calculate replacement values based on strategy
          const replacementValues = Array(featureCount);
          
          for (let i = 0; i < featureCount; i++) {
            if (missingValueCounts[i] > 0) {
              switch (strategy) {
                case 'mean':
                  let sum = 0;
                  let count = 0;
                  for (const item of data) {
                    if (item.features[i] !== null && item.features[i] !== undefined && !isNaN(item.features[i])) {
                      sum += item.features[i];
                      count++;
                    }
                  }
                  replacementValues[i] = count > 0 ? sum / count : 0;
                  break;
                
                case 'median':
                  const validValues = data
                    .map(item => item.features[i])
                    .filter(val => val !== null && val !== undefined && !isNaN(val))
                    .sort((a, b) => a - b);
                  
                  const mid = Math.floor(validValues.length / 2);
                  replacementValues[i] = validValues.length > 0 ?
                    (validValues.length % 2 === 0 ? (validValues[mid - 1] + validValues[mid]) / 2 : validValues[mid]) : 0;
                  break;
                
                case 'zero':
                  replacementValues[i] = 0;
                  break;
                
                default:
                  replacementValues[i] = 0;
              }
            }
          }
          
          // Replace missing values
          return data.map(item => {
            const newFeatures = [...item.features];
            
            for (let i = 0; i < featureCount; i++) {
              if (newFeatures[i] === null || newFeatures[i] === undefined || isNaN(newFeatures[i])) {
                newFeatures[i] = replacementValues[i];
              }
            }
            
            return {
              ...item,
              features: newFeatures
            };
          });
        }
        
        // Helper function: Scale features
        function scaleFeatures(data, method) {
          const featureCount = data[0].features.length;
          
          // Calculate statistics for scaling
          const stats = Array(featureCount).fill().map(() => ({
            min: Infinity,
            max: -Infinity,
            sum: 0,
            sumSquared: 0,
            count: 0
          }));
          
          for (const item of data) {
            for (let i = 0; i < featureCount; i++) {
              const val = item.features[i];
              stats[i].min = Math.min(stats[i].min, val);
              stats[i].max = Math.max(stats[i].max, val);
              stats[i].sum += val;
              stats[i].sumSquared += val * val;
              stats[i].count++;
            }
          }
          
          // Calculate mean and standard deviation
          for (let i = 0; i < featureCount; i++) {
            stats[i].mean = stats[i].sum / stats[i].count;
            stats[i].stdDev = Math.sqrt(
              (stats[i].sumSquared / stats[i].count) - (stats[i].mean * stats[i].mean)
            );
            
            // Prevent division by zero
            if (stats[i].stdDev === 0) stats[i].stdDev = 1;
            if (stats[i].max === stats[i].min) stats[i].max = stats[i].min + 1;
          }
          
          // Scale features
          return data.map(item => {
            const newFeatures = [...item.features];
            
            for (let i = 0; i < featureCount; i++) {
              switch (method) {
                case 'standard':
                  // Z-score normalization
                  newFeatures[i] = (newFeatures[i] - stats[i].mean) / stats[i].stdDev;
                  break;
                
                case 'minmax':
                  // Min-max scaling to [0, 1]
                  newFeatures[i] = (newFeatures[i] - stats[i].min) / (stats[i].max - stats[i].min);
                  break;
                
                case 'robust':
                  // Robust scaling using median and IQR
                  // For simplicity, we'll use mean and stdDev as approximation
                  newFeatures[i] = (newFeatures[i] - stats[i].mean) / stats[i].stdDev;
                  break;
                
                default:
                  // No scaling
                  break;
              }
            }
            
            return {
              ...item,
              features: newFeatures
            };
          });
        }
        
        // Helper function: Create polynomial features
        function createPolynomialFeatures(data, degree) {
          if (degree < 2) return data;
          
          return data.map(item => {
            const originalFeatures = item.features;
            const newFeatures = [...originalFeatures];
            
            // Add polynomial features (x^2, x^3, ..., x^degree)
            for (let d = 2; d <= degree; d++) {
              for (let i = 0; i < originalFeatures.length; i++) {
                newFeatures.push(Math.pow(originalFeatures[i], d));
              }
            }
            
            // Add interaction terms (x_i * x_j)
            if (degree >= 2) {
              for (let i = 0; i < originalFeatures.length; i++) {
                for (let j = i + 1; j < originalFeatures.length; j++) {
                  newFeatures.push(originalFeatures[i] * originalFeatures[j]);
                }
              }
            }
            
            return {
              ...item,
              features: newFeatures
            };
          });
        }
        
        // Helper function: Select features
        function selectFeatures(data, numFeatures) {
          const featureCount = data[0].features.length;
          
          if (numFeatures >= featureCount) return data;
          
          // For demonstration, we'll use a simple variance-based feature selection
          // In a real implementation, more sophisticated methods would be used
          
          // Calculate variance for each feature
          const variances = Array(featureCount).fill(0);
          const means = Array(featureCount).fill(0);
          
          // Calculate means
          for (const item of data) {
            for (let i = 0; i < featureCount; i++) {
              means[i] += item.features[i];
            }
          }
          
          for (let i = 0; i < featureCount; i++) {
            means[i] /= data.length;
          }
          
          // Calculate variances
          for (const item of data) {
            for (let i = 0; i < featureCount; i++) {
              variances[i] += Math.pow(item.features[i] - means[i], 2);
            }
          }
          
          for (let i = 0; i < featureCount; i++) {
            variances[i] /= data.length;
          }
          
          // Sort features by variance
          const featureIndices = Array.from({ length: featureCount }, (_, i) => i)
            .sort((a, b) => variances[b] - variances[a]);
          
          // Select top features
          const selectedIndices = featureIndices.slice(0, numFeatures);
          
          // Create new dataset with selected features
          return data.map(item => {
            const newFeatures = selectedIndices.map(idx => item.features[idx]);
            
            return {
              ...item,
              features: newFeatures
            };
          });
        }
      `
    }
  }
]
```

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおける機械学習モデルの実装について詳細に解説しました。ランダムフォレスト回帰、勾配ブースティング回帰、サポートベクター回帰、k近傍回帰など、主要な機械学習予測手法のn8nによる実装例を提供しました。また、機械学習モデルの性能向上に不可欠な特徴量エンジニアリングの実装例も紹介しました。

次のセクションでは、深層学習モデルの実装について詳細に解説します。
