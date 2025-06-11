# 情報収集システムの実装（パート1：基本設計と情報源管理）

## 情報収集システムの概要

トリプルパースペクティブ型戦略AIレーダーの核となる機能の一つが、多様な情報源から関連データを自動的に収集するシステムです。このセクションでは、n8nを活用した情報収集システムの実装方法について解説します。

情報収集システムの主な目的は以下の通りです：

1. キートピックに関連する情報を多様な情報源から効率的に収集する
2. 収集した情報を適切に前処理し、構造化された形式で保存する
3. 情報の信頼性と関連性を評価し、高品質なデータセットを構築する
4. 収集プロセスを自動化し、継続的な情報更新を実現する

## 情報源の種類と特性

戦略AIレーダーでは、以下の5種類の情報源からデータを収集します：

### 1. Webサイト

ニュースサイト、企業サイト、ブログなどのWebコンテンツは、最新情報の重要な源泉です。

**特性：**
- 更新頻度：高（ニュースサイト）～低（企業サイト）
- 構造化度：低（HTMLから構造を抽出する必要がある）
- 信頼性：情報源により大きく異なる
- アクセス方法：Webスクレイピング

**収集対象例：**
- 業界ニュースサイト（TechCrunch, The Verge, 日経ビジネスなど）
- 企業の公式ブログやプレスリリース
- 専門家のブログや技術記事

### 2. RSS/Atomフィード

多くのニュースサイトやブログはRSSフィードを提供しており、効率的な情報収集が可能です。

**特性：**
- 更新頻度：中～高
- 構造化度：高（XMLフォーマット）
- 信頼性：情報源に依存
- アクセス方法：RSSリーダー、フィードパーサー

**収集対象例：**
- ニュースサイトのRSSフィード
- 企業ブログのフィード
- 学術ジャーナルの最新論文フィード

### 3. API

多くのサービスはAPIを通じてデータにアクセスする方法を提供しています。

**特性：**
- 更新頻度：リアルタイム～定期的（APIによる）
- 構造化度：非常に高い（JSON/XMLフォーマット）
- 信頼性：高（公式APIの場合）
- アクセス方法：HTTP/RESTリクエスト

**収集対象例：**
- ニュースAPI（NewsAPI, GDELT, Aylien）
- ソーシャルメディアAPI（Twitter, LinkedIn, Reddit）
- 市場データAPI（Alpha Vantage, Yahoo Finance）

### 4. データベースとデータセット

既存のデータベースやオープンデータセットも重要な情報源です。

**特性：**
- 更新頻度：低～中
- 構造化度：高
- 信頼性：データソースに依存
- アクセス方法：データベース接続、ファイルダウンロード

**収集対象例：**
- 政府のオープンデータ
- 業界レポートとデータセット
- 学術研究データベース

### 5. ドキュメントリポジトリ

PDFや文書ファイルなどのドキュメントも重要な情報源です。

**特性：**
- 更新頻度：低
- 構造化度：低（テキスト抽出が必要）
- 信頼性：ソースに依存
- アクセス方法：ファイルダウンロード、テキスト抽出

**収集対象例：**
- 企業の年次報告書
- 業界白書
- 技術仕様書や標準文書

## 情報源管理システムの実装

効率的な情報収集のためには、情報源を適切に管理するシステムが必要です。n8nを活用した情報源管理システムの実装方法を解説します。

### 情報源データベースの設計

情報源を管理するためのデータベーススキーマは以下の通りです：

```sql
CREATE TABLE sources (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    source_type VARCHAR(50) NOT NULL,  -- WEB, RSS, API, DATABASE, DOCUMENT
    crawl_frequency VARCHAR(100),  -- cron形式
    last_crawled_at TIMESTAMP,
    reliability_score FLOAT,
    relevance_score FLOAT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE source_metadata (
    source_id UUID REFERENCES sources(id),
    key VARCHAR(100) NOT NULL,
    value TEXT,
    PRIMARY KEY (source_id, key)
);

CREATE TABLE source_topics (
    source_id UUID REFERENCES sources(id),
    topic_id UUID,
    relevance_score FLOAT,
    PRIMARY KEY (source_id, topic_id)
);
```

### n8nによる情報源管理ワークフロー

情報源を管理するためのn8nワークフローを実装します。

#### 1. 情報源追加ワークフロー

新しい情報源を追加するためのワークフローです。

```javascript
// n8n workflow: Add New Source
// Trigger: Webhook or Manual
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "add-source",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "validateSource",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const source = $input.item.json;
        // Validate required fields
        if (!source.name || !source.url || !source.source_type) {
          throw new Error('Missing required fields: name, url, or source_type');
        }
        
        // Generate UUID
        source.id = crypto.randomUUID();
        
        // Set default values
        source.crawl_frequency = source.crawl_frequency || '0 0 * * *'; // Default: daily
        source.reliability_score = source.reliability_score || 0.5;
        source.relevance_score = source.relevance_score || 0.5;
        source.active = true;
        
        return {json: source};
      `
    }
  },
  {
    "id": "testSourceConnection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "={{ $json.url }}",
      "method": "GET",
      "timeout": 5000
    }
  },
  {
    "id": "insertSourceToDB",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "insert",
      "schema": "public",
      "table": "sources",
      "columns": "id,name,url,source_type,crawl_frequency,reliability_score,relevance_score,active",
      "values": "={{ $json.id }},={{ $json.name }},={{ $json.url }},={{ $json.source_type }},={{ $json.crawl_frequency }},={{ $json.reliability_score }},={{ $json.relevance_score }},={{ $json.active }}"
    }
  },
  {
    "id": "linkSourceToTopics",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const source = $input.item.json;
        const topics = source.topics || [];
        
        const sourceTopics = topics.map(topic => ({
          source_id: source.id,
          topic_id: topic.id,
          relevance_score: topic.relevance_score || 0.5
        }));
        
        return {json: {source, sourceTopics}};
      `
    }
  },
  {
    "id": "insertSourceTopics",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "insert",
      "schema": "public",
      "table": "source_topics",
      "columns": "source_id,topic_id,relevance_score",
      "additionalFields": {
        "mode": "multiple",
        "data": "={{ $json.sourceTopics }}"
      }
    }
  },
  {
    "id": "scheduleInitialCrawl",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/trigger-crawl",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "source_id",
            "value": "={{ $json.source.id }}"
          }
        ]
      }
    }
  }
]
```

#### 2. 情報源更新ワークフロー

既存の情報源を更新するためのワークフローです。

```javascript
// n8n workflow: Update Source
// Trigger: Webhook or Manual
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "update-source",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "validateSourceUpdate",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const source = $input.item.json;
        // Validate source ID
        if (!source.id) {
          throw new Error('Missing source ID');
        }
        
        return {json: source};
      `
    }
  },
  {
    "id": "updateSourceInDB",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "update",
      "schema": "public",
      "table": "sources",
      "updateKey": "id",
      "columns": "name,url,source_type,crawl_frequency,reliability_score,relevance_score,active,updated_at",
      "values": "={{ $json.name }},={{ $json.url }},={{ $json.source_type }},={{ $json.crawl_frequency }},={{ $json.reliability_score }},={{ $json.relevance_score }},={{ $json.active }},CURRENT_TIMESTAMP"
    }
  },
  {
    "id": "updateSourceTopics",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const source = $input.item.json;
        const topics = source.topics || [];
        
        // First, delete existing topic associations
        const deleteOperation = {
          operation: "delete",
          source_id: source.id
        };
        
        // Then, create new topic associations
        const sourceTopics = topics.map(topic => ({
          source_id: source.id,
          topic_id: topic.id,
          relevance_score: topic.relevance_score || 0.5
        }));
        
        return {json: {source, deleteOperation, sourceTopics}};
      `
    }
  },
  {
    "id": "deleteExistingTopics",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": "DELETE FROM source_topics WHERE source_id = '{{ $json.deleteOperation.source_id }}'"
    }
  },
  {
    "id": "insertUpdatedTopics",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "insert",
      "schema": "public",
      "table": "source_topics",
      "columns": "source_id,topic_id,relevance_score",
      "additionalFields": {
        "mode": "multiple",
        "data": "={{ $json.sourceTopics }}"
      }
    }
  }
]
```

#### 3. 情報源評価ワークフロー

情報源の信頼性と関連性を定期的に評価するワークフローです。

```javascript
// n8n workflow: Evaluate Sources
// Trigger: Schedule (Weekly)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "0 0 * * 0" // Every Sunday at midnight
    }
  },
  {
    "id": "getSources",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "select",
      "schema": "public",
      "table": "sources",
      "returnAll": true
    }
  },
  {
    "id": "evaluateSources",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get all sources
        const sources = $input.item.json;
        const updatedSources = [];
        
        // Process each source
        for (const source of sources) {
          // Get content quality metrics from content table
          // This is a simplified example - in a real system, you would
          // calculate these metrics based on actual content analysis
          
          // Simulate reliability score calculation
          // In a real system, this would be based on:
          // - Content accuracy (compared to other sources)
          // - Historical reliability
          // - Source authority
          // - Content freshness
          let reliabilityScore = source.reliability_score;
          
          // Adjust based on simulated metrics
          const randomFactor = Math.random() * 0.1 - 0.05; // -0.05 to +0.05
          reliabilityScore = Math.max(0, Math.min(1, reliabilityScore + randomFactor));
          
          // Simulate relevance score calculation
          // In a real system, this would be based on:
          // - Content relevance to topics
          // - User engagement with content from this source
          // - Citation frequency
          let relevanceScore = source.relevance_score;
          
          // Adjust based on simulated metrics
          const randomRelevanceFactor = Math.random() * 0.1 - 0.05; // -0.05 to +0.05
          relevanceScore = Math.max(0, Math.min(1, relevanceScore + randomRelevanceFactor));
          
          // Update source with new scores
          updatedSources.push({
            id: source.id,
            reliability_score: reliabilityScore,
            relevance_score: relevanceScore
          });
        }
        
        return {json: {updatedSources}};
      `
    }
  },
  {
    "id": "updateSourceScores",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {updatedSources} = $input.item.json;
        const updatePromises = [];
        
        // For each source, update the scores in the database
        for (const source of updatedSources) {
          updatePromises.push({
            operation: "update",
            source_id: source.id,
            reliability_score: source.reliability_score,
            relevance_score: source.relevance_score
          });
        }
        
        return {json: {updatePromises}};
      `
    }
  },
  {
    "id": "executeBatchUpdate",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        UPDATE sources
        SET 
          reliability_score = CASE id 
            {% for source in $json.updatePromises %}
              WHEN '{{ source.source_id }}' THEN {{ source.reliability_score }}
            {% endfor %}
            ELSE reliability_score
          END,
          relevance_score = CASE id
            {% for source in $json.updatePromises %}
              WHEN '{{ source.source_id }}' THEN {{ source.relevance_score }}
            {% endfor %}
            ELSE relevance_score
          END,
          updated_at = CURRENT_TIMESTAMP
        WHERE id IN ({% for source in $json.updatePromises %}'{{ source.source_id }}'{% if not loop.last %},{% endif %}{% endfor %})
      `
    }
  }
]
```

### 情報源の自動発見

新たな情報源を自動的に発見するための機能も実装します。

#### 関連情報源発見ワークフロー

既存の情報源から関連する新たな情報源を発見するワークフローです。

```javascript
// n8n workflow: Discover Related Sources
// Trigger: Schedule (Monthly)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "0 0 1 * *" // First day of each month
    }
  },
  {
    "id": "getActiveSources",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "select",
      "schema": "public",
      "table": "sources",
      "where": "active = true",
      "returnAll": true
    }
  },
  {
    "id": "extractLinksFromSources",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const sources = $input.item.json;
        const discoveryTasks = [];
        
        // Process each source
        for (const source of sources) {
          // Only process web sources
          if (source.source_type === 'WEB') {
            discoveryTasks.push({
              source_id: source.id,
              url: source.url
            });
          }
        }
        
        return {json: {discoveryTasks}};
      `
    }
  },
  {
    "id": "splitInBatches",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1,
      "options": {
        "field": "discoveryTasks"
      }
    }
  },
  {
    "id": "fetchWebpage",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "={{ $json.url }}",
      "method": "GET",
      "timeout": 10000
    }
  },
  {
    "id": "extractLinks",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const cheerio = require('cheerio');
        const url = require('url');
        
        const task = $input.item.json;
        const html = $input.item.json.data;
        const baseUrl = task.url;
        
        // Parse HTML
        const $ = cheerio.load(html);
        const links = new Set();
        
        // Extract all links
        $('a').each((i, element) => {
          const href = $(element).attr('href');
          if (href) {
            try {
              // Resolve relative URLs
              const absoluteUrl = new URL(href, baseUrl).href;
              links.add(absoluteUrl);
            } catch (e) {
              // Invalid URL, skip
            }
          }
        });
        
        // Extract RSS/Atom feed links
        $('link[type="application/rss+xml"], link[type="application/atom+xml"]').each((i, element) => {
          const href = $(element).attr('href');
          if (href) {
            try {
              const absoluteUrl = new URL(href, baseUrl).href;
              links.add(absoluteUrl);
            } catch (e) {
              // Invalid URL, skip
            }
          }
        });
        
        return {json: {
          source_id: task.source_id,
          base_url: baseUrl,
          discovered_links: Array.from(links)
        }};
      `
    }
  },
  {
    "id": "filterLinks",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const data = $input.item.json;
        const links = data.discovered_links;
        
        // Filter out links to the same domain
        const baseUrlObj = new URL(data.base_url);
        const baseDomain = baseUrlObj.hostname;
        
        const externalLinks = links.filter(link => {
          try {
            const linkUrl = new URL(link);
            return linkUrl.hostname !== baseDomain;
          } catch (e) {
            return false;
          }
        });
        
        // Filter out common non-content sites
        const filteredLinks = externalLinks.filter(link => {
          const url = new URL(link);
          const hostname = url.hostname.toLowerCase();
          
          // Exclude social media, advertising, etc.
          const excludeDomains = [
            'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com',
            'youtube.com', 'pinterest.com', 'reddit.com',
            'google.com', 'bing.com', 'yahoo.com',
            'doubleclick.net', 'googlesyndication.com', 'adservice.google.com'
          ];
          
          return !excludeDomains.some(domain => hostname.includes(domain));
        });
        
        return {json: {
          source_id: data.source_id,
          potential_sources: filteredLinks.map(link => ({
            url: link,
            source_type: link.includes('/feed') || link.includes('rss') || link.includes('atom') ? 'RSS' : 'WEB'
          }))
        }};
      `
    }
  },
  {
    "id": "checkExistingSources",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "select",
      "schema": "public",
      "table": "sources",
      "returnAll": true
    }
  },
  {
    "id": "filterNewSources",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const data = $input.item.json;
        const existingSources = $input.item.json[0].json;
        
        // Get all existing URLs
        const existingUrls = new Set(existingSources.map(source => source.url));
        
        // Filter out already existing sources
        const newSources = data.potential_sources.filter(source => !existingUrls.has(source.url));
        
        return {json: {
          source_id: data.source_id,
          new_sources: newSources
        }};
      `
    }
  },
  {
    "id": "evaluateNewSources",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/evaluate-sources",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "sources",
            "value": "={{ $json.new_sources }}"
          }
        ]
      }
    }
  }
]
```

## 情報源の優先順位付けと最適化

効率的な情報収集のためには、情報源の優先順位付けと収集頻度の最適化が重要です。

### 優先順位付けのアルゴリズム

情報源の優先順位は以下の要素に基づいて決定されます：

1. **関連性スコア**: トピックとの関連度
2. **信頼性スコア**: 情報の正確性と信頼性
3. **更新頻度**: 情報源の更新頻度
4. **過去の有用性**: 過去に有用な情報を提供した実績

これらの要素を組み合わせた優先度スコアの計算式は以下の通りです：

```
優先度スコア = (関連性スコア * 0.4) + (信頼性スコア * 0.3) + (更新頻度スコア * 0.2) + (過去の有用性スコア * 0.1)
```

### クローリング頻度の最適化

情報源ごとに最適なクローリング頻度を決定するn8nワークフローを実装します。

```javascript
// n8n workflow: Optimize Crawling Frequency
// Trigger: Schedule (Weekly)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "0 0 * * 0" // Every Sunday at midnight
    }
  },
  {
    "id": "getSources",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "select",
      "schema": "public",
      "table": "sources",
      "returnAll": true
    }
  },
  {
    "id": "getContentUpdateStats",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        SELECT 
          source_id,
          COUNT(*) as content_count,
          MIN(published_at) as first_content,
          MAX(published_at) as last_content,
          AVG(EXTRACT(EPOCH FROM (lead(published_at) OVER (PARTITION BY source_id ORDER BY published_at) - published_at))/3600) as avg_hours_between_updates
        FROM content
        WHERE published_at IS NOT NULL
        GROUP BY source_id
      `
    }
  },
  {
    "id": "optimizeCrawlFrequency",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const sources = $input.item.json;
        const updateStats = $input.item.json[0].json;
        
        // Create a map of source_id to update stats
        const statsMap = {};
        updateStats.forEach(stat => {
          statsMap[stat.source_id] = stat;
        });
        
        const updatedSources = [];
        
        // Process each source
        for (const source of sources) {
          const stats = statsMap[source.id];
          let newFrequency = source.crawl_frequency;
          
          if (stats) {
            // Calculate optimal crawl frequency based on update patterns
            const avgHoursBetweenUpdates = stats.avg_hours_between_updates;
            
            if (avgHoursBetweenUpdates) {
              // Set crawl frequency to slightly more frequent than average update time
              // but not more frequent than hourly and not less frequent than weekly
              let optimalHours = Math.max(1, Math.min(168, Math.floor(avgHoursBetweenUpdates * 0.8)));
              
              if (optimalHours <= 1) {
                // Hourly
                newFrequency = '0 * * * *';
              } else if (optimalHours <= 6) {
                // Every 6 hours
                newFrequency = '0 */6 * * *';
              } else if (optimalHours <= 12) {
                // Twice daily
                newFrequency = '0 */12 * * *';
              } else if (optimalHours <= 24) {
                // Daily
                newFrequency = '0 0 * * *';
              } else if (optimalHours <= 72) {
                // Every 3 days
                newFrequency = '0 0 */3 * *';
              } else {
                // Weekly
                newFrequency = '0 0 * * 0';
              }
            }
          }
          
          // Add source with potentially updated frequency
          updatedSources.push({
            id: source.id,
            crawl_frequency: newFrequency
          });
        }
        
        return {json: {updatedSources}};
      `
    }
  },
  {
    "id": "updateCrawlFrequencies",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {updatedSources} = $input.item.json;
        const updatePromises = [];
        
        // For each source, update the crawl frequency in the database
        for (const source of updatedSources) {
          updatePromises.push({
            operation: "update",
            source_id: source.id,
            crawl_frequency: source.crawl_frequency
          });
        }
        
        return {json: {updatePromises}};
      `
    }
  },
  {
    "id": "executeBatchUpdate",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        UPDATE sources
        SET 
          crawl_frequency = CASE id 
            {% for source in $json.updatePromises %}
              WHEN '{{ source.source_id }}' THEN '{{ source.crawl_frequency }}'
            {% endfor %}
            ELSE crawl_frequency
          END,
          updated_at = CURRENT_TIMESTAMP
        WHERE id IN ({% for source in $json.updatePromises %}'{{ source.source_id }}'{% if not loop.last %},{% endif %}{% endfor %})
      `
    }
  },
  {
    "id": "updateCrawlSchedules",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/update-crawl-schedules",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "updated_sources",
            "value": "={{ $json.updatedSources }}"
          }
        ]
      }
    }
  }
]
```

## まとめ

このセクションでは、トリプルパースペクティブ型戦略AIレーダーの情報収集システムの基本設計と情報源管理について解説しました。n8nを活用することで、多様な情報源からのデータ収集を効率的に管理し、自動化することが可能です。

情報源の種類と特性を理解し、適切な管理システムを構築することで、高品質な情報収集の基盤を整えることができます。また、情報源の優先順位付けとクローリング頻度の最適化により、効率的なリソース利用と最新情報の収集を両立させることができます。

次のパートでは、各種情報源からのデータ収集の具体的な実装方法について解説します。
