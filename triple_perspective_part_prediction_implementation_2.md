# 予測モデルの実装と統合（パート2-3：深層学習モデルの実装）

## 深層学習モデルによる予測の概要

トリプルパースペクティブ型戦略AIレーダーにおける予測エンジンでは、時系列予測モデルや機械学習モデルに加えて、より複雑なパターンを捉えるために深層学習モデルを活用します。深層学習モデルは、大量のデータから自動的に特徴を抽出し、非線形関係を学習する能力に優れています。本セクションでは、主要な深層学習予測モデルのn8nによる実装について解説します。

### 深層学習予測の基本概念

深層学習による予測は、以下のステップで行われます：

1. **データ前処理**: 生データの正規化、シーケンス変換など
2. **モデル設計**: ネットワークアーキテクチャの選択と構築
3. **モデルトレーニング**: 大量のデータを用いた学習
4. **モデル評価**: 学習したモデルの性能を検証
5. **予測生成**: 学習したモデルを使用して将来の値を予測

トリプルパースペクティブ型戦略AIレーダーでは、以下のような深層学習モデルを活用します：

- LSTM（Long Short-Term Memory）ネットワーク
- GRU（Gated Recurrent Unit）ネットワーク
- 1次元CNN（Convolutional Neural Network）
- Transformer
- ハイブリッドモデル

## LSTM（Long Short-Term Memory）ネットワークの実装

LSTM（Long Short-Term Memory）は、長期的な依存関係を学習できる再帰型ニューラルネットワーク（RNN）の一種です。LSTMは、勾配消失問題を解決し、長いシーケンスデータから効果的にパターンを学習できます。

### n8nからPythonを使用したLSTM実装

```javascript
// n8n workflow: LSTM Network Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; import tensorflow as tf; from tensorflow.keras.models import Sequential; from tensorflow.keras.layers import LSTM, Dense, Dropout; from tensorflow.keras.optimizers import Adam; from sklearn.preprocessing import MinMaxScaler; # Extract data X = np.array([item['sequence'] for item in data['training_data']]); y = np.array([item['target'] for item in data['training_data']]); # Reshape input to be [samples, time steps, features] X = X.reshape(X.shape[0], X.shape[1], 1); # Create and compile the model params = data['parameters']; model = Sequential(); model.add(LSTM(units=params.get('units', 50), return_sequences=True, input_shape=(X.shape[1], 1))); model.add(Dropout(params.get('dropout', 0.2))); model.add(LSTM(units=params.get('units', 50))); model.add(Dropout(params.get('dropout', 0.2))); model.add(Dense(units=1)); model.compile(optimizer=Adam(learning_rate=params.get('learning_rate', 0.001)), loss='mean_squared_error'); # Train the model history = model.fit(X, y, epochs=params.get('epochs', 50), batch_size=params.get('batch_size', 32), verbose=0); # Make predictions X_test = np.array([item['sequence'] for item in data['test_data']]); X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1); predictions = model.predict(X_test).flatten().tolist(); # Prepare output result = {'predictions': [{'sequence': data['test_data'][i]['sequence'], 'prediction': predictions[i]} for i in range(len(predictions))], 'model_info': {'loss_history': history.history['loss'], 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setLSTMInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for LSTM model
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for LSTM
        const lstmInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            units: parameters.units || 50,
            dropout: parameters.dropout || 0.2,
            learning_rate: parameters.learning_rate || 0.001,
            epochs: parameters.epochs || 50,
            batch_size: parameters.batch_size || 32
          }
        };
        
        return {
          json: lstmInput
        };
      `
    }
  },
  {
    "id": "processLSTMResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process LSTM model results
        const lstmResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = lstmResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'LSTM Network',
          parameters: lstmResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            sequence: p.sequence,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          model_info: {
            final_loss: lstmResults.model_info.loss_history[lstmResults.model_info.loss_history.length - 1]
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

### LSTMモデルの使用例

```javascript
// n8n workflow: LSTM Model Usage Example
// HTTP Request node to call LSTM model
[
  {
    "id": "httpRequest",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/lstm-model",
      "method": "POST",
      "bodyContent": "{\n  \"training_data\": [\n    {\"sequence\": [1, 2, 3, 4, 5], \"target\": 6},\n    {\"sequence\": [2, 3, 4, 5, 6], \"target\": 7},\n    {\"sequence\": [3, 4, 5, 6, 7], \"target\": 8},\n    {\"sequence\": [4, 5, 6, 7, 8], \"target\": 9},\n    {\"sequence\": [5, 6, 7, 8, 9], \"target\": 10},\n    {\"sequence\": [6, 7, 8, 9, 10], \"target\": 11},\n    {\"sequence\": [7, 8, 9, 10, 11], \"target\": 12},\n    {\"sequence\": [8, 9, 10, 11, 12], \"target\": 13},\n    {\"sequence\": [9, 10, 11, 12, 13], \"target\": 14},\n    {\"sequence\": [10, 11, 12, 13, 14], \"target\": 15}\n  ],\n  \"test_data\": [\n    {\"sequence\": [11, 12, 13, 14, 15]},\n    {\"sequence\": [12, 13, 14, 15, 16]},\n    {\"sequence\": [13, 14, 15, 16, 17]}\n  ],\n  \"parameters\": {\n    \"units\": 64,\n    \"dropout\": 0.2,\n    \"learning_rate\": 0.001,\n    \"epochs\": 100,\n    \"batch_size\": 8\n  }\n}",
      "bodyContentType": "json"
    }
  }
]
```

## GRU（Gated Recurrent Unit）ネットワークの実装

GRU（Gated Recurrent Unit）は、LSTMの簡略化バージョンで、より少ないパラメータで同様の性能を発揮することができます。GRUは、リセットゲートとアップデートゲートを使用して、情報の流れを制御します。

### n8nからPythonを使用したGRU実装

```javascript
// n8n workflow: GRU Network Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; import tensorflow as tf; from tensorflow.keras.models import Sequential; from tensorflow.keras.layers import GRU, Dense, Dropout; from tensorflow.keras.optimizers import Adam; # Extract data X = np.array([item['sequence'] for item in data['training_data']]); y = np.array([item['target'] for item in data['training_data']]); # Reshape input to be [samples, time steps, features] X = X.reshape(X.shape[0], X.shape[1], 1); # Create and compile the model params = data['parameters']; model = Sequential(); model.add(GRU(units=params.get('units', 50), return_sequences=True, input_shape=(X.shape[1], 1))); model.add(Dropout(params.get('dropout', 0.2))); model.add(GRU(units=params.get('units', 50))); model.add(Dropout(params.get('dropout', 0.2))); model.add(Dense(units=1)); model.compile(optimizer=Adam(learning_rate=params.get('learning_rate', 0.001)), loss='mean_squared_error'); # Train the model history = model.fit(X, y, epochs=params.get('epochs', 50), batch_size=params.get('batch_size', 32), verbose=0); # Make predictions X_test = np.array([item['sequence'] for item in data['test_data']]); X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1); predictions = model.predict(X_test).flatten().tolist(); # Prepare output result = {'predictions': [{'sequence': data['test_data'][i]['sequence'], 'prediction': predictions[i]} for i in range(len(predictions))], 'model_info': {'loss_history': history.history['loss'], 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setGRUInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for GRU model
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for GRU
        const gruInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            units: parameters.units || 50,
            dropout: parameters.dropout || 0.2,
            learning_rate: parameters.learning_rate || 0.001,
            epochs: parameters.epochs || 50,
            batch_size: parameters.batch_size || 32
          }
        };
        
        return {
          json: gruInput
        };
      `
    }
  },
  {
    "id": "processGRUResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process GRU model results
        const gruResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = gruResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'GRU Network',
          parameters: gruResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            sequence: p.sequence,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          model_info: {
            final_loss: gruResults.model_info.loss_history[gruResults.model_info.loss_history.length - 1]
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

## 1次元CNN（Convolutional Neural Network）の実装

1次元CNN（Convolutional Neural Network）は、時系列データのパターン抽出に効果的です。1次元の畳み込み層を使用して、時間的な特徴を自動的に抽出します。

### n8nからPythonを使用した1次元CNN実装

```javascript
// n8n workflow: 1D CNN Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; import tensorflow as tf; from tensorflow.keras.models import Sequential; from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout; from tensorflow.keras.optimizers import Adam; # Extract data X = np.array([item['sequence'] for item in data['training_data']]); y = np.array([item['target'] for item in data['training_data']]); # Reshape input to be [samples, time steps, features] X = X.reshape(X.shape[0], X.shape[1], 1); # Create and compile the model params = data['parameters']; model = Sequential(); model.add(Conv1D(filters=params.get('filters', 64), kernel_size=params.get('kernel_size', 3), activation='relu', input_shape=(X.shape[1], 1))); model.add(MaxPooling1D(pool_size=2)); model.add(Dropout(params.get('dropout', 0.2))); model.add(Flatten()); model.add(Dense(units=params.get('dense_units', 50), activation='relu')); model.add(Dropout(params.get('dropout', 0.2))); model.add(Dense(units=1)); model.compile(optimizer=Adam(learning_rate=params.get('learning_rate', 0.001)), loss='mean_squared_error'); # Train the model history = model.fit(X, y, epochs=params.get('epochs', 50), batch_size=params.get('batch_size', 32), verbose=0); # Make predictions X_test = np.array([item['sequence'] for item in data['test_data']]); X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1); predictions = model.predict(X_test).flatten().tolist(); # Prepare output result = {'predictions': [{'sequence': data['test_data'][i]['sequence'], 'prediction': predictions[i]} for i in range(len(predictions))], 'model_info': {'loss_history': history.history['loss'], 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setCNNInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for 1D CNN model
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for 1D CNN
        const cnnInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            filters: parameters.filters || 64,
            kernel_size: parameters.kernel_size || 3,
            dense_units: parameters.dense_units || 50,
            dropout: parameters.dropout || 0.2,
            learning_rate: parameters.learning_rate || 0.001,
            epochs: parameters.epochs || 50,
            batch_size: parameters.batch_size || 32
          }
        };
        
        return {
          json: cnnInput
        };
      `
    }
  },
  {
    "id": "processCNNResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process 1D CNN model results
        const cnnResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = cnnResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: '1D CNN',
          parameters: cnnResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            sequence: p.sequence,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          model_info: {
            final_loss: cnnResults.model_info.loss_history[cnnResults.model_info.loss_history.length - 1]
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

## Transformerモデルの実装

Transformerは、自己注意機構（Self-Attention）を使用して、シーケンスデータ内の長距離依存関係を効果的に捉えることができるモデルです。時系列予測においても高い性能を発揮します。

### n8nからPythonを使用したTransformer実装

```javascript
// n8n workflow: Transformer Model Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; import tensorflow as tf; from tensorflow.keras.models import Model; from tensorflow.keras.layers import Input, Dense, Dropout, LayerNormalization, MultiHeadAttention, GlobalAveragePooling1D; from tensorflow.keras.optimizers import Adam; # Extract data X = np.array([item['sequence'] for item in data['training_data']]); y = np.array([item['target'] for item in data['training_data']]); # Reshape input to be [samples, time steps, features] X = X.reshape(X.shape[0], X.shape[1], 1); # Create Transformer model params = data['parameters']; def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0): # Multi-head attention x = LayerNormalization(epsilon=1e-6)(inputs); x = MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(x, x); x = Dropout(dropout)(x); res = x + inputs; # Feed-forward network x = LayerNormalization(epsilon=1e-6)(res); x = Dense(ff_dim, activation='relu')(x); x = Dropout(dropout)(x); x = Dense(inputs.shape[-1])(x); return x + res; # Build the model inputs = Input(shape=(X.shape[1], 1)); x = inputs; for _ in range(params.get('num_transformer_blocks', 2)): x = transformer_encoder(x, params.get('head_size', 64), params.get('num_heads', 2), params.get('ff_dim', 128), params.get('dropout', 0.2)); x = GlobalAveragePooling1D()(x); x = Dropout(params.get('dropout', 0.2))(x); x = Dense(params.get('dense_units', 50), activation='relu')(x); x = Dropout(params.get('dropout', 0.2))(x); outputs = Dense(1)(x); model = Model(inputs=inputs, outputs=outputs); model.compile(optimizer=Adam(learning_rate=params.get('learning_rate', 0.001)), loss='mean_squared_error'); # Train the model history = model.fit(X, y, epochs=params.get('epochs', 50), batch_size=params.get('batch_size', 32), verbose=0); # Make predictions X_test = np.array([item['sequence'] for item in data['test_data']]); X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1); predictions = model.predict(X_test).flatten().tolist(); # Prepare output result = {'predictions': [{'sequence': data['test_data'][i]['sequence'], 'prediction': predictions[i]} for i in range(len(predictions))], 'model_info': {'loss_history': history.history['loss'], 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setTransformerInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for Transformer model
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for Transformer
        const transformerInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            num_transformer_blocks: parameters.num_transformer_blocks || 2,
            head_size: parameters.head_size || 64,
            num_heads: parameters.num_heads || 2,
            ff_dim: parameters.ff_dim || 128,
            dense_units: parameters.dense_units || 50,
            dropout: parameters.dropout || 0.2,
            learning_rate: parameters.learning_rate || 0.001,
            epochs: parameters.epochs || 50,
            batch_size: parameters.batch_size || 32
          }
        };
        
        return {
          json: transformerInput
        };
      `
    }
  },
  {
    "id": "processTransformerResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process Transformer model results
        const transformerResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = transformerResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'Transformer',
          parameters: transformerResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            sequence: p.sequence,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          model_info: {
            final_loss: transformerResults.model_info.loss_history[transformerResults.model_info.loss_history.length - 1]
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

## ハイブリッドモデルの実装

ハイブリッドモデルは、異なるタイプのニューラルネットワークを組み合わせることで、各モデルの長所を活かした予測を行います。例えば、CNNとLSTMを組み合わせたCNN-LSTMモデルは、CNNで局所的な特徴を抽出し、LSTMで時間的な依存関係を捉えることができます。

### n8nからPythonを使用したCNN-LSTMハイブリッドモデル実装

```javascript
// n8n workflow: CNN-LSTM Hybrid Model Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); import numpy as np; import tensorflow as tf; from tensorflow.keras.models import Sequential; from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout; from tensorflow.keras.optimizers import Adam; # Extract data X = np.array([item['sequence'] for item in data['training_data']]); y = np.array([item['target'] for item in data['training_data']]); # Reshape input to be [samples, time steps, features] X = X.reshape(X.shape[0], X.shape[1], 1); # Create and compile the model params = data['parameters']; model = Sequential(); # CNN layers model.add(Conv1D(filters=params.get('cnn_filters', 64), kernel_size=params.get('kernel_size', 3), activation='relu', input_shape=(X.shape[1], 1))); model.add(MaxPooling1D(pool_size=2)); model.add(Dropout(params.get('dropout', 0.2))); # LSTM layers model.add(LSTM(units=params.get('lstm_units', 50), return_sequences=False)); model.add(Dropout(params.get('dropout', 0.2))); # Output layer model.add(Dense(units=1)); model.compile(optimizer=Adam(learning_rate=params.get('learning_rate', 0.001)), loss='mean_squared_error'); # Train the model history = model.fit(X, y, epochs=params.get('epochs', 50), batch_size=params.get('batch_size', 32), verbose=0); # Make predictions X_test = np.array([item['sequence'] for item in data['test_data']]); X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1); predictions = model.predict(X_test).flatten().tolist(); # Prepare output result = {'predictions': [{'sequence': data['test_data'][i]['sequence'], 'prediction': predictions[i]} for i in range(len(predictions))], 'model_info': {'loss_history': history.history['loss'], 'parameters': params}}; print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setCNNLSTMInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for CNN-LSTM hybrid model
        const trainingData = $input.item.json.training_data || [];
        const testData = $input.item.json.test_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for CNN-LSTM
        const cnnLstmInput = {
          training_data: trainingData,
          test_data: testData,
          parameters: {
            cnn_filters: parameters.cnn_filters || 64,
            kernel_size: parameters.kernel_size || 3,
            lstm_units: parameters.lstm_units || 50,
            dropout: parameters.dropout || 0.2,
            learning_rate: parameters.learning_rate || 0.001,
            epochs: parameters.epochs || 50,
            batch_size: parameters.batch_size || 32
          }
        };
        
        return {
          json: cnnLstmInput
        };
      `
    }
  },
  {
    "id": "processCNNLSTMResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process CNN-LSTM hybrid model results
        const cnnLstmResults = JSON.parse($input.item.json);
        
        // Extract predictions
        const predictions = cnnLstmResults.predictions || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'CNN-LSTM Hybrid',
          parameters: cnnLstmResults.model_info.parameters,
          predictions: predictions.map((p, index) => ({
            test_case: index + 1,
            sequence: p.sequence,
            prediction: Math.round(p.prediction * 100) / 100
          })),
          model_info: {
            final_loss: cnnLstmResults.model_info.loss_history[cnnLstmResults.model_info.loss_history.length - 1]
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

## 深層学習モデルのハイパーパラメータ最適化

深層学習モデルの性能は、適切なハイパーパラメータの選択に大きく依存します。n8nを使用してハイパーパラメータ最適化を行う例を示します。

```javascript
// n8n workflow: Deep Learning Hyperparameter Optimization
// Function node for hyperparameter optimization
[
  {
    "id": "hyperparameterOptimization",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Training data and optimization parameters
        const trainingData = $input.item.json.training_data || [];
        const validationData = $input.item.json.validation_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract optimization parameters
        const modelType = parameters.model_type || 'lstm';
        const numTrials = parameters.num_trials || 10;
        const maxEpochs = parameters.max_epochs || 100;
        const earlyStoppingPatience = parameters.early_stopping_patience || 10;
        
        // Define hyperparameter search space
        const searchSpace = {
          lstm: {
            units: [32, 64, 128, 256],
            num_layers: [1, 2, 3],
            dropout: [0.1, 0.2, 0.3, 0.4, 0.5],
            learning_rate: [0.0001, 0.0005, 0.001, 0.005, 0.01],
            batch_size: [16, 32, 64, 128]
          },
          gru: {
            units: [32, 64, 128, 256],
            num_layers: [1, 2, 3],
            dropout: [0.1, 0.2, 0.3, 0.4, 0.5],
            learning_rate: [0.0001, 0.0005, 0.001, 0.005, 0.01],
            batch_size: [16, 32, 64, 128]
          },
          cnn: {
            filters: [32, 64, 128, 256],
            kernel_size: [2, 3, 5, 7],
            num_layers: [1, 2, 3],
            dropout: [0.1, 0.2, 0.3, 0.4, 0.5],
            learning_rate: [0.0001, 0.0005, 0.001, 0.005, 0.01],
            batch_size: [16, 32, 64, 128]
          },
          transformer: {
            num_heads: [1, 2, 4, 8],
            head_size: [32, 64, 128],
            ff_dim: [64, 128, 256, 512],
            num_transformer_blocks: [1, 2, 3, 4],
            dropout: [0.1, 0.2, 0.3, 0.4, 0.5],
            learning_rate: [0.0001, 0.0005, 0.001, 0.005],
            batch_size: [16, 32, 64, 128]
          }
        };
        
        // In a real implementation, this would perform actual hyperparameter optimization
        // For demonstration, we'll simulate the optimization process
        
        // Generate random trials
        const trials = [];
        const space = searchSpace[modelType] || searchSpace.lstm;
        
        for (let i = 0; i < numTrials; i++) {
          // Generate random hyperparameters
          const hyperparams = {};
          
          Object.entries(space).forEach(([param, values]) => {
            hyperparams[param] = values[Math.floor(Math.random() * values.length)];
          });
          
          // Simulate training and validation
          const validationLoss = simulateTraining(hyperparams, maxEpochs, earlyStoppingPatience);
          
          trials.push({
            trial_id: i + 1,
            hyperparameters: hyperparams,
            validation_loss: validationLoss,
            epochs_trained: Math.floor(Math.random() * maxEpochs) + 1
          });
        }
        
        // Sort trials by validation loss
        trials.sort((a, b) => a.validation_loss - b.validation_loss);
        
        // Get best hyperparameters
        const bestTrial = trials[0];
        
        return {
          json: {
            model_type: modelType,
            num_trials: numTrials,
            best_hyperparameters: bestTrial.hyperparameters,
            best_validation_loss: bestTrial.validation_loss,
            all_trials: trials
          }
        };
        
        // Helper function: Simulate training
        function simulateTraining(hyperparams, maxEpochs, patience) {
          // In a real implementation, this would train the model and return validation loss
          // For demonstration, we'll simulate the validation loss
          
          // Base loss depends on hyperparameters
          let baseLoss = 0;
          
          // Units/filters: more is generally better, but with diminishing returns
          const units = hyperparams.units || hyperparams.filters || 64;
          baseLoss += 1 / Math.sqrt(units) * 0.5;
          
          // Dropout: moderate dropout is usually better
          const dropout = hyperparams.dropout || 0.2;
          baseLoss += Math.abs(dropout - 0.3) * 0.5;
          
          // Learning rate: moderate learning rate is usually better
          const learningRate = hyperparams.learning_rate || 0.001;
          baseLoss += Math.abs(Math.log10(learningRate) + 3) * 0.3;
          
          // Add some randomness
          baseLoss += Math.random() * 0.2;
          
          return Math.max(0.1, baseLoss);
        }
      `
    }
  }
]
```

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおける深層学習モデルの実装について詳細に解説しました。LSTM、GRU、1次元CNN、Transformer、ハイブリッドモデルなど、主要な深層学習予測手法のn8nによる実装例を提供しました。また、深層学習モデルの性能向上に不可欠なハイパーパラメータ最適化の実装例も紹介しました。

次のセクションでは、アンサンブル手法の実装について詳細に解説します。
