# 予測モデルの実装と統合（パート2-1：時系列予測モデルの基本実装）

## 時系列予測モデルの概要

トリプルパースペクティブ型戦略AIレーダーにおける予測エンジンの中核となるのが時系列予測モデルです。時系列予測モデルは、過去の時間的パターンを分析し、将来の値を予測するために使用されます。本セクションでは、主要な時系列予測モデルの基本実装について解説します。

### 時系列予測の基本概念

時系列データとは、時間の経過とともに収集されたデータポイントの集合です。トリプルパースペクティブ型戦略AIレーダーでは、以下のような時系列データを扱います：

- テクノロジー採用率の推移
- 市場シェアの変動
- 売上高や利益率の推移
- 特許出願数の変化
- 消費者センチメントの変動

時系列予測の主な課題は以下の通りです：

1. **トレンド**: データの長期的な上昇または下降傾向
2. **季節性**: 一定の周期で繰り返されるパターン
3. **循環性**: 不規則な周期で発生する変動
4. **ノイズ**: ランダムな変動
5. **構造的変化**: データの基本的な性質の変化

## ARIMA（自己回帰和分移動平均）モデルの実装

ARIMA（AutoRegressive Integrated Moving Average）モデルは、時系列予測の基本的かつ強力なアプローチです。ARIMAモデルは以下の3つのコンポーネントで構成されます：

- **AR(p)**: 自己回帰成分 - 過去の値に基づく予測
- **I(d)**: 和分（差分）成分 - 非定常性の除去
- **MA(q)**: 移動平均成分 - 過去の予測誤差に基づく調整

### n8nによるARIMAモデル実装

```javascript
// n8n workflow: ARIMA Model Implementation
// Function node for ARIMA model
[
  {
    "id": "arimaModelImplementation",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Time series data and model parameters
        const timeSeriesData = $input.item.json.time_series_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract ARIMA parameters
        const p = parameters.p || 1; // AR order
        const d = parameters.d || 1; // Differencing order
        const q = parameters.q || 1; // MA order
        
        // Validate input
        if (timeSeriesData.length < p + d + q + 10) {
          throw new Error('Insufficient data points for ARIMA model');
        }
        
        // In a real implementation, this would use a proper ARIMA algorithm
        // For demonstration, we'll implement a simplified version
        
        // Step 1: Apply differencing to make the series stationary
        let diffData = timeSeriesData;
        for (let i = 0; i < d; i++) {
          diffData = differenceTimeSeries(diffData);
        }
        
        // Step 2: Estimate AR and MA parameters
        // In a real implementation, this would use proper parameter estimation
        // For demonstration, we'll use simplified parameter estimation
        const arParams = estimateARParameters(diffData, p);
        const maParams = estimateMAParameters(diffData, q);
        
        // Step 3: Generate forecasts
        const forecastHorizon = parameters.forecast_horizon || 5;
        const forecasts = generateForecasts(
          timeSeriesData, 
          diffData, 
          arParams, 
          maParams, 
          d, 
          forecastHorizon
        );
        
        return {
          json: {
            model_type: 'ARIMA',
            parameters: {
              p,
              d,
              q
            },
            ar_parameters: arParams,
            ma_parameters: maParams,
            forecasts: forecasts,
            model_info: {
              data_points_used: timeSeriesData.length,
              stationarity_achieved: isStationary(diffData)
            }
          }
        };
        
        // Helper function: Difference time series
        function differenceTimeSeries(data) {
          const result = [];
          for (let i = 1; i < data.length; i++) {
            result.push(data[i] - data[i-1]);
          }
          return result;
        }
        
        // Helper function: Estimate AR parameters
        function estimateARParameters(data, p) {
          // In a real implementation, this would use proper parameter estimation
          // For demonstration, we'll use a simplified approach
          
          const params = [];
          
          // Simple autocorrelation-based estimation
          for (let i = 1; i <= p; i++) {
            let numerator = 0;
            let denominator = 0;
            
            for (let t = i; t < data.length; t++) {
              numerator += data[t] * data[t-i];
              denominator += data[t-i] * data[t-i];
            }
            
            params.push(denominator !== 0 ? numerator / denominator : 0);
          }
          
          return params;
        }
        
        // Helper function: Estimate MA parameters
        function estimateMAParameters(data, q) {
          // In a real implementation, this would use proper parameter estimation
          // For demonstration, we'll return placeholder values
          
          const params = [];
          for (let i = 0; i < q; i++) {
            params.push(0.1 * (i + 1));
          }
          
          return params;
        }
        
        // Helper function: Generate forecasts
        function generateForecasts(originalData, diffData, arParams, maParams, d, horizon) {
          const forecasts = [];
          const errors = [];
          
          // Initialize with the last values from the original data
          const lastValues = originalData.slice(-Math.max(arParams.length, maParams.length));
          
          // Generate forecasts
          for (let h = 0; h < horizon; h++) {
            // AR component
            let arComponent = 0;
            for (let i = 0; i < arParams.length; i++) {
              const idx = lastValues.length - 1 - i;
              if (idx >= 0) {
                arComponent += arParams[i] * lastValues[idx];
              }
            }
            
            // MA component
            let maComponent = 0;
            for (let i = 0; i < maParams.length; i++) {
              const idx = errors.length - 1 - i;
              if (idx >= 0) {
                maComponent += maParams[i] * errors[idx];
              }
            }
            
            // Combine components
            let forecast = arComponent + maComponent;
            
            // Integrate (reverse differencing) if needed
            for (let i = 0; i < d; i++) {
              forecast += lastValues[lastValues.length - 1];
            }
            
            // Add forecast to results
            forecasts.push(forecast);
            
            // Update lastValues for next iteration
            lastValues.push(forecast);
            lastValues.shift();
            
            // Add a placeholder error (in a real implementation, this would be based on actual vs. predicted)
            errors.push(0);
          }
          
          return forecasts;
        }
        
        // Helper function: Check if time series is stationary
        function isStationary(data) {
          // In a real implementation, this would use proper stationarity tests
          // For demonstration, we'll use a simplified approach
          
          // Calculate mean and standard deviation
          const mean = data.reduce((sum, val) => sum + val, 0) / data.length;
          const stdDev = Math.sqrt(
            data.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / data.length
          );
          
          // Check if the coefficient of variation is small
          return stdDev / Math.abs(mean) < 0.1;
        }
      `
    }
  }
]
```

### ARIMAモデルの使用例

```javascript
// n8n workflow: ARIMA Model Usage Example
// HTTP Request node to call ARIMA model
[
  {
    "id": "httpRequest",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/arima-model",
      "method": "POST",
      "bodyContent": "{\n  \"time_series_data\": [100, 105, 110, 112, 115, 120, 125, 130, 135, 140, 142, 145, 150, 155, 160, 165, 170, 172, 175, 180],\n  \"parameters\": {\n    \"p\": 2,\n    \"d\": 1,\n    \"q\": 1,\n    \"forecast_horizon\": 5\n  }\n}",
      "bodyContentType": "json"
    }
  },
  {
    "id": "processARIMAResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process ARIMA model results
        const arimaResults = $input.item.json;
        
        // Extract forecasts
        const forecasts = arimaResults.forecasts || [];
        
        // Format results for display
        const formattedResults = {
          model_type: arimaResults.model_type,
          parameters: arimaResults.parameters,
          forecasts: forecasts.map((value, index) => ({
            period: index + 1,
            forecast_value: Math.round(value * 100) / 100
          })),
          model_info: arimaResults.model_info
        };
        
        return {
          json: formattedResults
        };
      `
    }
  }
]
```

## 指数平滑法モデルの実装

指数平滑法は、より最近のデータポイントに大きな重みを与える時系列予測手法です。ここでは、単純指数平滑法とホルト・ウィンタース法の実装を紹介します。

### 単純指数平滑法

```javascript
// n8n workflow: Simple Exponential Smoothing Implementation
// Function node for Simple Exponential Smoothing
[
  {
    "id": "simpleExponentialSmoothing",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Time series data and model parameters
        const timeSeriesData = $input.item.json.time_series_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const alpha = parameters.alpha || 0.3; // Smoothing factor (0 < alpha < 1)
        
        // Validate input
        if (timeSeriesData.length < 3) {
          throw new Error('Insufficient data points for exponential smoothing');
        }
        
        if (alpha <= 0 || alpha >= 1) {
          throw new Error('Alpha must be between 0 and 1');
        }
        
        // Apply simple exponential smoothing
        const smoothedData = [];
        let level = timeSeriesData[0];
        
        // Calculate smoothed values
        smoothedData.push(level);
        
        for (let i = 1; i < timeSeriesData.length; i++) {
          level = alpha * timeSeriesData[i] + (1 - alpha) * level;
          smoothedData.push(level);
        }
        
        // Generate forecasts
        const forecastHorizon = parameters.forecast_horizon || 5;
        const forecasts = [];
        
        for (let i = 0; i < forecastHorizon; i++) {
          forecasts.push(level); // In SES, all forecasts are the same
        }
        
        return {
          json: {
            model_type: 'Simple Exponential Smoothing',
            parameters: {
              alpha
            },
            smoothed_data: smoothedData,
            forecasts: forecasts,
            model_info: {
              data_points_used: timeSeriesData.length,
              final_level: level
            }
          }
        };
      `
    }
  }
]
```

### ホルト・ウィンタース法（三重指数平滑法）

```javascript
// n8n workflow: Holt-Winters Method Implementation
// Function node for Holt-Winters Method
[
  {
    "id": "holtWintersMethod",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Time series data and model parameters
        const timeSeriesData = $input.item.json.time_series_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Extract parameters
        const alpha = parameters.alpha || 0.3; // Level smoothing factor
        const beta = parameters.beta || 0.1; // Trend smoothing factor
        const gamma = parameters.gamma || 0.1; // Seasonal smoothing factor
        const seasonalPeriod = parameters.seasonal_period || 4; // e.g., 4 for quarterly data
        const multiplicative = parameters.multiplicative || false; // Multiplicative or additive
        
        // Validate input
        if (timeSeriesData.length < 2 * seasonalPeriod) {
          throw new Error('Insufficient data points for Holt-Winters method');
        }
        
        if (alpha <= 0 || alpha >= 1 || beta < 0 || beta > 1 || gamma < 0 || gamma > 1) {
          throw new Error('Smoothing factors must be between 0 and 1');
        }
        
        // Initialize level, trend, and seasonal components
        let level, trend;
        const seasonal = [];
        
        // Initialize seasonal components
        for (let i = 0; i < seasonalPeriod; i++) {
          let seasonalSum = 0;
          let seasonalCount = 0;
          
          for (let j = i; j < timeSeriesData.length; j += seasonalPeriod) {
            seasonalSum += timeSeriesData[j];
            seasonalCount++;
          }
          
          const seasonalAvg = seasonalSum / seasonalCount;
          seasonal.push(seasonalAvg);
        }
        
        // Normalize seasonal components
        const seasonalAvg = seasonal.reduce((sum, val) => sum + val, 0) / seasonalPeriod;
        for (let i = 0; i < seasonalPeriod; i++) {
          if (multiplicative) {
            seasonal[i] = seasonal[i] / seasonalAvg;
          } else {
            seasonal[i] = seasonal[i] - seasonalAvg;
          }
        }
        
        // Initialize level and trend
        level = timeSeriesData[0];
        trend = timeSeriesData[1] - timeSeriesData[0];
        
        // Apply Holt-Winters method
        const fittedValues = [];
        
        for (let i = 0; i < timeSeriesData.length; i++) {
          const s = i % seasonalPeriod;
          let value;
          
          if (i === 0) {
            value = level;
          } else {
            if (multiplicative) {
              value = (level + trend) * seasonal[s];
            } else {
              value = level + trend + seasonal[s];
            }
          }
          
          fittedValues.push(value);
          
          // Update components
          if (i < timeSeriesData.length) {
            const observed = timeSeriesData[i];
            const oldLevel = level;
            
            if (multiplicative) {
              level = alpha * (observed / seasonal[s]) + (1 - alpha) * (level + trend);
              trend = beta * (level - oldLevel) + (1 - beta) * trend;
              seasonal[s] = gamma * (observed / level) + (1 - gamma) * seasonal[s];
            } else {
              level = alpha * (observed - seasonal[s]) + (1 - alpha) * (level + trend);
              trend = beta * (level - oldLevel) + (1 - beta) * trend;
              seasonal[s] = gamma * (observed - level) + (1 - gamma) * seasonal[s];
            }
          }
        }
        
        // Generate forecasts
        const forecastHorizon = parameters.forecast_horizon || seasonalPeriod * 2;
        const forecasts = [];
        
        for (let i = 0; i < forecastHorizon; i++) {
          const s = (timeSeriesData.length + i) % seasonalPeriod;
          let forecast;
          
          if (multiplicative) {
            forecast = (level + (i + 1) * trend) * seasonal[s];
          } else {
            forecast = level + (i + 1) * trend + seasonal[s];
          }
          
          forecasts.push(forecast);
        }
        
        return {
          json: {
            model_type: 'Holt-Winters Method',
            parameters: {
              alpha,
              beta,
              gamma,
              seasonal_period: seasonalPeriod,
              multiplicative
            },
            fitted_values: fittedValues,
            forecasts: forecasts,
            model_info: {
              data_points_used: timeSeriesData.length,
              final_level: level,
              final_trend: trend,
              seasonal_components: seasonal
            }
          }
        };
      `
    }
  }
]
```

## Prophet モデルの実装

Facebook（Meta）が開発したProphetは、季節性、休日効果、トレンド変化点を自動的に検出する強力な時系列予測ツールです。n8nでProphetを使用するには、Pythonコードを実行するノードを活用します。

### n8nからPythonスクリプトを実行する例

```javascript
// n8n workflow: Prophet Model Implementation
// Execute Command node to run Python script
[
  {
    "id": "executePythonScript",
    "type": "n8n-nodes-base.executeCommand",
    "parameters": {
      "command": "python3",
      "arguments": "-c \"import sys, json; data = json.loads(sys.stdin.read()); from prophet import Prophet; import pandas as pd; import numpy as np; # Convert input data to DataFrame df = pd.DataFrame({'ds': pd.date_range(start=data['start_date'], periods=len(data['y']), freq=data['freq']), 'y': data['y']}); # Create and fit model m = Prophet(seasonality_mode=data['parameters'].get('seasonality_mode', 'additive'), changepoint_prior_scale=data['parameters'].get('changepoint_prior_scale', 0.05)); m.fit(df); # Make future dataframe future = m.make_future_dataframe(periods=data['forecast_horizon'], freq=data['freq']); # Forecast forecast = m.predict(future); # Prepare output result = {'forecast': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(data['forecast_horizon']).to_dict('records'), 'components': {'trend': forecast['trend'].tail(data['forecast_horizon']).tolist(), 'seasonal': [forecast['yearly'].tail(data['forecast_horizon']).tolist() if 'yearly' in forecast else [], forecast['weekly'].tail(data['forecast_horizon']).tolist() if 'weekly' in forecast else [], forecast['daily'].tail(data['forecast_horizon']).tolist() if 'daily' in forecast else []]}};print(json.dumps(result))\"",
      "executeInShell": true
    }
  },
  {
    "id": "setProphetInput",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Prepare input for Prophet model
        const timeSeriesData = $input.item.json.time_series_data || [];
        const parameters = $input.item.json.parameters || {};
        
        // Format data for Prophet
        const prophetInput = {
          y: timeSeriesData,
          start_date: parameters.start_date || '2020-01-01',
          freq: parameters.freq || 'D', // D for daily, W for weekly, M for monthly
          forecast_horizon: parameters.forecast_horizon || 30,
          parameters: {
            seasonality_mode: parameters.seasonality_mode || 'additive',
            changepoint_prior_scale: parameters.changepoint_prior_scale || 0.05
          }
        };
        
        return {
          json: prophetInput
        };
      `
    }
  },
  {
    "id": "processProphetResults",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Process Prophet model results
        const prophetResults = JSON.parse($input.item.json);
        
        // Extract forecasts
        const forecasts = prophetResults.forecast || [];
        
        // Format results for display
        const formattedResults = {
          model_type: 'Prophet',
          forecasts: forecasts.map(f => ({
            date: f.ds,
            forecast: f.yhat,
            lower_bound: f.yhat_lower,
            upper_bound: f.yhat_upper
          })),
          components: prophetResults.components
        };
        
        return {
          json: formattedResults
        };
      `
    }
  }
]
```

## 時系列予測モデルの評価と選択

時系列予測モデルの性能を評価し、最適なモデルを選択するためのワークフローを実装します。

```javascript
// n8n workflow: Time Series Model Evaluation
// Function node for model evaluation
[
  {
    "id": "evaluateTimeSeriesModels",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Time series data and model predictions
        const timeSeriesData = $input.item.json.time_series_data || [];
        const modelPredictions = $input.item.json.model_predictions || {};
        
        // Validate input
        if (timeSeriesData.length === 0) {
          throw new Error('No time series data provided');
        }
        
        if (Object.keys(modelPredictions).length === 0) {
          throw new Error('No model predictions provided');
        }
        
        // Split data into training and test sets
        const testSize = Math.floor(timeSeriesData.length * 0.2); // 20% for testing
        const trainingData = timeSeriesData.slice(0, -testSize);
        const testData = timeSeriesData.slice(-testSize);
        
        // Calculate evaluation metrics for each model
        const evaluationResults = {};
        
        Object.entries(modelPredictions).forEach(([modelName, predictions]) => {
          // Ensure predictions match test data length
          if (predictions.length < testData.length) {
            throw new Error(\`Insufficient predictions for model \${modelName}\`);
          }
          
          // Calculate metrics
          const metrics = calculateMetrics(testData, predictions.slice(0, testData.length));
          
          evaluationResults[modelName] = {
            metrics,
            predictions: predictions.slice(0, testData.length)
          };
        });
        
        // Rank models based on RMSE
        const rankedModels = Object.entries(evaluationResults)
          .sort((a, b) => a[1].metrics.rmse - b[1].metrics.rmse)
          .map(([modelName, results]) => ({
            model_name: modelName,
            rmse: results.metrics.rmse,
            mae: results.metrics.mae,
            mape: results.metrics.mape
          }));
        
        return {
          json: {
            evaluation_results: evaluationResults,
            ranked_models: rankedModels,
            best_model: rankedModels[0].model_name,
            test_data_size: testData.length
          }
        };
        
        // Helper function: Calculate metrics
        function calculateMetrics(actual, predicted) {
          // Calculate Root Mean Square Error (RMSE)
          const squaredErrors = actual.map((val, i) => Math.pow(val - predicted[i], 2));
          const mse = squaredErrors.reduce((sum, val) => sum + val, 0) / actual.length;
          const rmse = Math.sqrt(mse);
          
          // Calculate Mean Absolute Error (MAE)
          const absoluteErrors = actual.map((val, i) => Math.abs(val - predicted[i]));
          const mae = absoluteErrors.reduce((sum, val) => sum + val, 0) / actual.length;
          
          // Calculate Mean Absolute Percentage Error (MAPE)
          const percentageErrors = actual.map((val, i) => 
            val !== 0 ? Math.abs((val - predicted[i]) / val) * 100 : 0
          );
          const mape = percentageErrors.reduce((sum, val) => sum + val, 0) / actual.length;
          
          return {
            rmse,
            mae,
            mape
          };
        }
      `
    }
  }
]
```

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおける時系列予測モデルの基本実装について解説しました。ARIMAモデル、指数平滑法、Prophetモデルなど、主要な時系列予測手法のn8nによる実装例を提供しました。また、モデル評価と選択のためのワークフローも紹介しました。

次のセクションでは、機械学習モデルの実装について詳細に解説します。
