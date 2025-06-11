# 小売業向け適用例：段階的実装ガイド

コンセンサスモデルを小売業に適用する際の段階的な実装アプローチを以下に示します。このガイドは、需要予測、在庫最適化、価格設定、顧客セグメンテーションなどの領域で、初期プロトタイプから本格的なシステム展開までをカバーします。

## フェーズ1：限定的スコープでの概念実証（PoC）（1-3ヶ月）

最初のフェーズでは、特定の製品カテゴリまたは小規模な店舗群に焦点を当て、コンセンサスモデルの基本的な有効性を検証します。

### ステップ1：データ収集と準備（特定製品カテゴリ・店舗）

```javascript
// n8nでの小売データ収集ワークフロー（例：特定カテゴリのPOSデータと在庫データ）
{
  "nodes": [
    {
      "name": "Fetch POS Data (Category X)",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://internal-pos-system/api/sales?category_code=CAT-X&store_ids=S001,S002,S003&date_range=last_30_days",
        "method": "GET",
        "authentication": "apiKey",
        "options": {
          "timeout": 15000 // 15秒タイムアウト
        }
      }
    },
    {
      "name": "Fetch Inventory Data (Category X)",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://internal-inventory-system/api/stock?category_code=CAT-X&store_ids=S001,S002,S003",
        "method": "GET",
        "authentication": "apiKey",
        "options": {
          "timeout": 10000
        }
      }
    },
    {
      "name": "Basic Data Cleansing & Transformation",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "// POSデータと在庫データの基本的なクレンジングと結合\nconst salesData = $node[\"Fetch POS Data (Category X)\"].json;\nconst inventoryData = $node[\"Fetch Inventory Data (Category X)\"].json;\n\nconst cleanedSales = salesData.map(s => ({ \n  productId: s.product_id, \n  storeId: s.store_id, \n  timestamp: new Date(s.sale_time).toISOString(), \n  quantity: parseInt(s.quantity_sold),\n  price: parseFloat(s.unit_price)\n}));\n\nconst cleanedInventory = inventoryData.map(i => ({ \n  productId: i.product_id, \n  storeId: i.store_id, \n  currentStock: parseInt(i.stock_level),\n  lastUpdated: new Date(i.last_update_time).toISOString()\n}));\n\n// 簡単な結合（PoC用）\nconst combinedData = cleanedSales.map(sale => {\n  const stockInfo = cleanedInventory.find(inv => inv.productId === sale.productId && inv.storeId === sale.storeId);\n  return { ...sale, currentStockBeforeSale: stockInfo ? stockInfo.currentStock + sale.quantity : null };\n});\n\nreturn combinedData;"
      }
    },
    {
      "name": "Store for PoC Analysis",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "insert",
        "table": "poc_retail_data_cat_x",
        "columns": "product_id,store_id,timestamp,quantity,price,current_stock_before_sale",
        "values": "={{$node[\"Basic Data Cleansing & Transformation\"].json.map(item => `\\\"${item.productId}\\\",\\\"${item.storeId}\\\",\\\"${item.timestamp}\\\",${item.quantity},${item.price},${item.currentStockBeforeSale || \"NULL\"}`).join(\",\")}}"
      }
    }
  ]
}
```

このステップでは：
- 特定の製品カテゴリ（例：飲料、スナック菓子）または数店舗のPOSデータ、在庫データを収集。
- 関連するプロモーション情報、天候データ（該当地域）を限定的に収集。
- PoC分析用の一時的なデータストアに保存。
- データ収集は日次バッチで実行。

### ステップ2：基本的な分析モデルのプロトタイピング（需要予測）

```javascript
// 基本的な需要予測モデルのプロトタイプワークフロー
{
  "nodes": [
    {
      "name": "Fetch PoC Retail Data",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "select",
        "table": "poc_retail_data_cat_x",
        "query": "SELECT product_id, store_id, DATE(timestamp) as sale_date, SUM(quantity) as daily_sales FROM poc_retail_data_cat_x GROUP BY 1,2,3 ORDER BY 1,2,3"
      }
    },
    {
      "name": "Simple Moving Average Forecast",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "// 単純移動平均による需要予測（例：過去7日間）\nconst salesHistory = $input.item.json;\nconst forecasts = [];\nconst uniqueProductStores = [...new Set(salesHistory.map(s => `${s.product_id}-${s.store_id}`))];\n\nfor (const ps of uniqueProductStores) {\n  const [productId, storeId] = ps.split(\'-\\' );\n  const productStoreSales = salesHistory.filter(s => s.product_id === productId && s.store_id === storeId).sort((a,b) => new Date(a.sale_date) - new Date(b.sale_date));\n  if (productStoreSales.length >= 7) {\n    const last7DaysSales = productStoreSales.slice(-7).reduce((sum, s) => sum + parseFloat(s.daily_sales), 0);\n    forecasts.push({ productId, storeId, forecastDate: new Date(new Date(productStoreSales.slice(-1)[0].sale_date).getTime() + 24*60*60*1000).toISOString().split(\'T\')[0], smaForecast: last7DaysSales / 7 });\n  }\n}\nreturn forecasts;"
      }
    },
    {
      "name": "Basic Exponential Smoothing (Mock)",
      "type": "n8n-nodes-base.function", // 実際には統計ライブラリや外部サービスコール
      "parameters": {
        "functionCode": "// 基本的な指数平滑化予測（モック）\nconst salesHistory = $node[\"Fetch PoC Retail Data\"].json;\nconst forecasts = [];\nconst uniqueProductStores = [...new Set(salesHistory.map(s => `${s.product_id}-${s.store_id}`))];\n\nfor (const ps of uniqueProductStores) {\n  const [productId, storeId] = ps.split(\'-\\' );\n  const productStoreSales = salesHistory.filter(s => s.product_id === productId && s.store_id === storeId).sort((a,b) => new Date(a.sale_date) - new Date(b.sale_date));\n  if (productStoreSales.length > 0) {\n    // 実際には指数平滑化アルゴリズムを適用\n    const mockEsForecast = parseFloat(productStoreSales.slice(-1)[0].daily_sales) * (0.8 + Math.random() * 0.4); // 前日実績の0.8～1.2倍\n    forecasts.push({ productId, storeId, forecastDate: new Date(new Date(productStoreSales.slice(-1)[0].sale_date).getTime() + 24*60*60*1000).toISOString().split(\'T\')[0], esForecast: mockEsForecast });\n  }\n}\nreturn forecasts;"
      }
    },
    {
      "name": "Store PoC Forecasts",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "insert",
        "table": "poc_retail_forecasts_cat_x",
        "columns": "product_id,store_id,forecast_date,sma_forecast,es_forecast",
        "values": "={{$input.item.json.map(item => `\\\"${item.productId}\\\",\\\"${item.storeId}\\\",\\\"${item.forecastDate}\\\",${item.smaForecast || \"NULL\"},${item.esForecast || \"NULL\"}`).join(\",\")}}" // Assuming one forecast per product-store-date from each model
      }
    }
  ]
}
```

このステップでは：
- 収集データに対して、単純移動平均（SMA）法による需要予測モデルを実装。
- 基本的な指数平滑法（ES）による予測（またはそのモック）を並行して実施。
- 2つのモデルの予測結果を比較し、基本的なコンセンサスの必要性を検討。
- 週次バッチで実行。

### ステップ3：PoCコンセンサスモデルの構築と評価（需要予測）

```javascript
// PoCコンセンサス需要予測モデルワークフロー
{
  "nodes": [
    {
      "name": "Fetch PoC Forecasts",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "select",
        "table": "poc_retail_forecasts_cat_x",
        "query": "SELECT pf.*, prd.daily_sales as actual_sales FROM poc_retail_forecasts_cat_x pf LEFT JOIN (SELECT product_id, store_id, DATE(timestamp) as sale_date, SUM(quantity) as daily_sales FROM poc_retail_data_cat_x GROUP BY 1,2,3) prd ON pf.product_id = prd.product_id AND pf.store_id = prd.store_id AND pf.forecast_date = prd.sale_date WHERE pf.sma_forecast IS NOT NULL AND pf.es_forecast IS NOT NULL"
      }
    },
    {
      "name": "PoC Consensus Forecast Formation",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "// PoCコンセンサス予測形成（単純平均）と精度評価\nconst forecasts = $input.item.json;\nconst consensusForecasts = forecasts.map(f => {\n  const consensusForecast = (f.sma_forecast + f.es_forecast) / 2;\n  const smaError = f.actual_sales !== null ? Math.abs(f.sma_forecast - f.actual_sales) : null;\n  const esError = f.actual_sales !== null ? Math.abs(f.es_forecast - f.actual_sales) : null;\n  const consensusError = f.actual_sales !== null ? Math.abs(consensusForecast - f.actual_sales) : null;\n  return { ...f, consensusForecast, smaError, esError, consensusError };\n});\nreturn consensusForecasts;"
      }
    },
    {
      "name": "Generate PoC Forecast Report",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "// PoC予測結果レポート生成 (MAPEなど)\nconst results = $input.item.json;\nconst validResults = results.filter(r => r.actual_sales !== null && r.actual_sales > 0);\nconst smaMape = validResults.reduce((sum, r) => sum + (r.smaError / r.actual_sales), 0) / validResults.length * 100;\nconst esMape = validResults.reduce((sum, r) => sum + (r.esError / r.actual_sales), 0) / validResults.length * 100;\nconst consensusMape = validResults.reduce((sum, r) => sum + (r.consensusError / r.actual_sales), 0) / validResults.length * 100;\n\nconst summary = {\n  totalForecasts: results.length,\n  evaluatedForecasts: validResults.length,\n  smaMape: smaMape.toFixed(2) + \"%\",\n  esMape: esMape.toFixed(2) + \"%\",\n  consensusMape: consensusMape.toFixed(2) + \"%\"\n};\nconsole.log(\'PoC Forecast Report:																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																	100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:00:00.000 --> 00:00:04.000Z
