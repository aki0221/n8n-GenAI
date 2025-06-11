# 情報収集システムの実装（パート2：データ収集と前処理）

## データ収集の基本アーキテクチャ

トリプルパースペクティブ型戦略AIレーダーのデータ収集システムは、多様な情報源から効率的にデータを収集し、分析可能な形式に変換する役割を担います。このセクションでは、n8nを活用したデータ収集システムの実装方法について解説します。

データ収集システムの基本アーキテクチャは以下の通りです：

1. **収集スケジューラ**
   - 情報源ごとの収集タイミングを管理
   - 優先度に基づくリソース割り当て
   - エラー処理とリトライメカニズム

2. **コネクタモジュール**
   - 各情報源タイプに対応したデータ取得方法
   - 認証と接続管理
   - レート制限の遵守

3. **コンテンツ抽出エンジン**
   - HTML/XML/JSONからの構造化データ抽出
   - テキスト、画像、メタデータの分離
   - マルチメディアコンテンツの処理

4. **前処理パイプライン**
   - テキスト正規化と前処理
   - 言語検出と翻訳
   - エンティティ抽出と関係性分析
   - 重複検出と排除

5. **データ保存システム**
   - 構造化データの永続化
   - メタデータとインデックス管理
   - バージョン管理とアーカイブ

## n8nによる収集スケジューラの実装

n8nを活用して、情報源ごとに最適なスケジュールでデータを収集するシステムを実装します。

### マスタースケジューラワークフロー

情報源の収集スケジュールを管理するマスターワークフローです。

```javascript
// n8n workflow: Master Scheduler
// Trigger: Schedule (Every 5 minutes)
[
  {
    "id": "schedule",
    "type": "n8n-nodes-base.scheduleTrigger",
    "parameters": {
      "rule": "*/5 * * * *" // Every 5 minutes
    }
  },
  {
    "id": "getCurrentTime",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Get current time
        const now = new Date();
        
        // Format as cron-compatible time components
        const minute = now.getMinutes();
        const hour = now.getHours();
        const dayOfMonth = now.getDate();
        const month = now.getMonth() + 1;
        const dayOfWeek = now.getDay();
        
        return {
          json: {
            current_time: now.toISOString(),
            cron_components: {
              minute,
              hour,
              dayOfMonth,
              month,
              dayOfWeek
            }
          }
        };
      `
    }
  },
  {
    "id": "findSourcesToCrawl",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        SELECT * FROM sources
        WHERE active = true
        ORDER BY 
          reliability_score * 0.3 + relevance_score * 0.7 DESC
        LIMIT 10
      `
    }
  },
  {
    "id": "filterDueSources",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const sources = $input.item.json;
        const cronComponents = $input.item.json.cron_components;
        
        // Helper function to check if a source is due for crawling
        function isSourceDue(crawlFrequency, cronComponents) {
          // Parse cron expression
          const parts = crawlFrequency.split(' ');
          if (parts.length !== 5) return false;
          
          const [minute, hour, dayOfMonth, month, dayOfWeek] = parts;
          
          // Check minute
          if (minute !== '*' && minute !== '*/5' && !minute.split(',').includes(cronComponents.minute.toString())) {
            if (minute.includes('/')) {
              const divisor = parseInt(minute.split('/')[1]);
              if (cronComponents.minute % divisor !== 0) return false;
            } else {
              return false;
            }
          }
          
          // Check hour
          if (hour !== '*' && !hour.split(',').includes(cronComponents.hour.toString())) {
            if (hour.includes('/')) {
              const divisor = parseInt(hour.split('/')[1]);
              if (cronComponents.hour % divisor !== 0) return false;
            } else {
              return false;
            }
          }
          
          // Check day of month
          if (dayOfMonth !== '*' && !dayOfMonth.split(',').includes(cronComponents.dayOfMonth.toString())) {
            if (dayOfMonth.includes('/')) {
              const divisor = parseInt(dayOfMonth.split('/')[1]);
              if (cronComponents.dayOfMonth % divisor !== 0) return false;
            } else {
              return false;
            }
          }
          
          // Check month
          if (month !== '*' && !month.split(',').includes(cronComponents.month.toString())) {
            if (month.includes('/')) {
              const divisor = parseInt(month.split('/')[1]);
              if (cronComponents.month % divisor !== 0) return false;
            } else {
              return false;
            }
          }
          
          // Check day of week
          if (dayOfWeek !== '*' && !dayOfWeek.split(',').includes(cronComponents.dayOfWeek.toString())) {
            return false;
          }
          
          return true;
        }
        
        // Filter sources that are due for crawling
        const dueSources = sources.filter(source => {
          // Check if the source is due based on its crawl frequency
          return isSourceDue(source.crawl_frequency, cronComponents);
        });
        
        return {json: {dueSources}};
      `
    }
  },
  {
    "id": "triggerCrawlJobs",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {dueSources} = $input.item.json;
        const crawlJobs = [];
        
        // Create a crawl job for each due source
        for (const source of dueSources) {
          crawlJobs.push({
            source_id: source.id,
            source_type: source.source_type,
            url: source.url,
            priority: source.reliability_score * 0.3 + source.relevance_score * 0.7
          });
        }
        
        return {json: {crawlJobs}};
      `
    }
  },
  {
    "id": "dispatchCrawlJobs",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/crawl-dispatcher",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "jobs",
            "value": "={{ $json.crawlJobs }}"
          }
        ]
      }
    }
  },
  {
    "id": "updateLastCrawledTime",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        UPDATE sources
        SET 
          last_crawled_at = CURRENT_TIMESTAMP
        WHERE id IN ({% for job in $json.crawlJobs %}'{{ job.source_id }}'{% if not loop.last %},{% endif %}{% endfor %})
      `
    }
  }
]
```

### クロールディスパッチャーワークフロー

収集ジョブを適切なコネクタに振り分けるワークフローです。

```javascript
// n8n workflow: Crawl Dispatcher
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "crawl-dispatcher",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "processCrawlJobs",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {jobs} = $input.item.json;
        
        // Group jobs by source type
        const jobsByType = {
          WEB: [],
          RSS: [],
          API: [],
          DATABASE: [],
          DOCUMENT: []
        };
        
        for (const job of jobs) {
          if (jobsByType[job.source_type]) {
            jobsByType[job.source_type].push(job);
          }
        }
        
        return {json: {jobsByType}};
      `
    }
  },
  {
    "id": "dispatchWebCrawlJobs",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "condition": {
        "conditions": [
          {
            "value1": "={{ $json.jobsByType.WEB.length }}",
            "operation": "notEqual",
            "value2": 0
          }
        ]
      }
    }
  },
  {
    "id": "triggerWebCrawler",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/web-crawler",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "jobs",
            "value": "={{ $json.jobsByType.WEB }}"
          }
        ]
      }
    }
  },
  {
    "id": "dispatchRssCrawlJobs",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "condition": {
        "conditions": [
          {
            "value1": "={{ $json.jobsByType.RSS.length }}",
            "operation": "notEqual",
            "value2": 0
          }
        ]
      }
    }
  },
  {
    "id": "triggerRssCrawler",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/rss-crawler",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "jobs",
            "value": "={{ $json.jobsByType.RSS }}"
          }
        ]
      }
    }
  },
  {
    "id": "dispatchApiCrawlJobs",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "condition": {
        "conditions": [
          {
            "value1": "={{ $json.jobsByType.API.length }}",
            "operation": "notEqual",
            "value2": 0
          }
        ]
      }
    }
  },
  {
    "id": "triggerApiCrawler",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/api-crawler",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "jobs",
            "value": "={{ $json.jobsByType.API }}"
          }
        ]
      }
    }
  },
  {
    "id": "dispatchDatabaseCrawlJobs",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "condition": {
        "conditions": [
          {
            "value1": "={{ $json.jobsByType.DATABASE.length }}",
            "operation": "notEqual",
            "value2": 0
          }
        ]
      }
    }
  },
  {
    "id": "triggerDatabaseCrawler",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/database-crawler",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "jobs",
            "value": "={{ $json.jobsByType.DATABASE }}"
          }
        ]
      }
    }
  },
  {
    "id": "dispatchDocumentCrawlJobs",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "condition": {
        "conditions": [
          {
            "value1": "={{ $json.jobsByType.DOCUMENT.length }}",
            "operation": "notEqual",
            "value2": 0
          }
        ]
      }
    }
  },
  {
    "id": "triggerDocumentCrawler",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/document-crawler",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "jobs",
            "value": "={{ $json.jobsByType.DOCUMENT }}"
          }
        ]
      }
    }
  }
]
```

## 情報源タイプ別のコネクタ実装

各情報源タイプに対応したコネクタを実装します。ここでは、代表的な情報源タイプのコネクタ実装を解説します。

### Webクローラーの実装

Webサイトからコンテンツを収集するクローラーの実装です。

```javascript
// n8n workflow: Web Crawler
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "web-crawler",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "splitInBatches",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1,
      "options": {
        "field": "jobs"
      }
    }
  },
  {
    "id": "fetchWebpage",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "={{ $json.url }}",
      "method": "GET",
      "timeout": 10000,
      "options": {
        "redirect": {
          "redirect": {
            "followRedirects": true,
            "maxRedirects": 5
          }
        },
        "proxy": {
          "enabled": false
        },
        "timeout": 10000
      }
    }
  },
  {
    "id": "extractContent",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const cheerio = require('cheerio');
        
        const job = $input.item.json;
        const html = $input.item.json.data;
        
        // Parse HTML
        const $ = cheerio.load(html);
        
        // Remove script and style elements
        $('script, style').remove();
        
        // Extract title
        const title = $('title').text().trim() || $('h1').first().text().trim();
        
        // Extract main content
        // This is a simplified approach - in a real system, you would use
        // more sophisticated content extraction algorithms
        let mainContent = '';
        
        // Try to find main content container
        const possibleContentSelectors = [
          'article',
          '.content',
          '.post',
          '.entry',
          '#content',
          '.main',
          'main'
        ];
        
        let contentElement = null;
        for (const selector of possibleContentSelectors) {
          if ($(selector).length > 0) {
            contentElement = $(selector).first();
            break;
          }
        }
        
        // If no specific content container found, use body
        if (!contentElement) {
          contentElement = $('body');
        }
        
        // Extract text from content element
        mainContent = contentElement.text().trim()
          .replace(/\\s+/g, ' ')
          .replace(/\\n+/g, '\\n');
        
        // Extract metadata
        const metadata = {
          url: job.url,
          language: $('html').attr('lang') || 'en',
          description: $('meta[name="description"]').attr('content') || '',
          keywords: $('meta[name="keywords"]').attr('content') || '',
          author: $('meta[name="author"]').attr('content') || '',
          publishedDate: $('meta[property="article:published_time"]').attr('content') || null
        };
        
        // Extract images
        const images = [];
        $('img').each((i, element) => {
          const src = $(element).attr('src');
          const alt = $(element).attr('alt') || '';
          if (src) {
            try {
              // Resolve relative URLs
              const absoluteUrl = new URL(src, job.url).href;
              images.push({
                url: absoluteUrl,
                alt: alt
              });
            } catch (e) {
              // Invalid URL, skip
            }
          }
        });
        
        return {
          json: {
            source_id: job.source_id,
            url: job.url,
            title: title,
            content: mainContent,
            metadata: metadata,
            images: images,
            crawled_at: new Date().toISOString()
          }
        };
      `
    }
  },
  {
    "id": "saveContent",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/save-content",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "content",
            "value": "={{ $json }}"
          }
        ]
      }
    }
  }
]
```

### RSSフィードコネクタの実装

RSSフィードからコンテンツを収集するコネクタの実装です。

```javascript
// n8n workflow: RSS Crawler
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "rss-crawler",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "splitInBatches",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1,
      "options": {
        "field": "jobs"
      }
    }
  },
  {
    "id": "fetchRssFeed",
    "type": "n8n-nodes-base.rssFeedRead",
    "parameters": {
      "url": "={{ $json.url }}",
      "options": {
        "returnAll": true,
        "limit": 20
      }
    }
  },
  {
    "id": "processRssItems",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const job = $input.item.json;
        const rssItems = $input.item.json;
        
        // Process each RSS item
        const processedItems = rssItems.map(item => {
          // Extract content
          let content = item.content || item.description || '';
          
          // Clean up content (remove HTML tags if needed)
          if (content.includes('<')) {
            // Simple HTML tag removal - in a real system, you would use a proper HTML parser
            content = content.replace(/<[^>]*>/g, ' ').replace(/\\s+/g, ' ').trim();
          }
          
          // Parse published date
          let publishedDate = null;
          if (item.pubDate) {
            publishedDate = new Date(item.pubDate).toISOString();
          } else if (item.isoDate) {
            publishedDate = item.isoDate;
          }
          
          return {
            source_id: job.source_id,
            url: item.link,
            title: item.title,
            content: content,
            metadata: {
              url: item.link,
              language: item.language || 'en',
              author: item.creator || item.author || '',
              publishedDate: publishedDate,
              categories: item.categories || []
            },
            images: [],  // RSS feeds typically don't include images directly
            crawled_at: new Date().toISOString()
          };
        });
        
        return {json: {processedItems}};
      `
    }
  },
  {
    "id": "saveRssContent",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/save-content-batch",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "content_items",
            "value": "={{ $json.processedItems }}"
          }
        ]
      }
    }
  }
]
```

### APIコネクタの実装

外部APIからデータを収集するコネクタの実装例です。ここでは、ニュースAPIを例に解説します。

```javascript
// n8n workflow: API Crawler (News API Example)
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "api-crawler",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "splitInBatches",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1,
      "options": {
        "field": "jobs"
      }
    }
  },
  {
    "id": "getSourceMetadata",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "select",
      "schema": "public",
      "table": "source_metadata",
      "where": "source_id = '{{ $json.source_id }}'"
    }
  },
  {
    "id": "prepareApiRequest",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const job = $input.item.json;
        const metadata = $input.item.json;
        
        // Create a map of metadata
        const metadataMap = {};
        metadata.forEach(item => {
          metadataMap[item.key] = item.value;
        });
        
        // Prepare API request based on source type
        // This example assumes a News API source
        const apiKey = metadataMap.api_key || process.env.NEWS_API_KEY;
        const endpoint = metadataMap.endpoint || 'everything';
        const query = metadataMap.query || '';
        const language = metadataMap.language || 'en';
        const sortBy = metadataMap.sort_by || 'publishedAt';
        
        // Construct API URL
        let apiUrl = `https://newsapi.org/v2/${endpoint}?`;
        
        if (query) {
          apiUrl += `q=${encodeURIComponent(query)}&`;
        }
        
        apiUrl += `language=${language}&sortBy=${sortBy}&apiKey=${apiKey}`;
        
        return {
          json: {
            source_id: job.source_id,
            api_url: apiUrl,
            metadata: metadataMap
          }
        };
      `
    }
  },
  {
    "id": "fetchApiData",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "={{ $json.api_url }}",
      "method": "GET",
      "timeout": 10000
    }
  },
  {
    "id": "processApiResponse",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const job = $input.item.json;
        const apiResponse = $input.item.json.data;
        
        // Process News API response
        if (!apiResponse.articles || !Array.isArray(apiResponse.articles)) {
          throw new Error('Invalid API response format');
        }
        
        // Process each article
        const processedItems = apiResponse.articles.map(article => {
          return {
            source_id: job.source_id,
            url: article.url,
            title: article.title,
            content: article.content || article.description || '',
            metadata: {
              url: article.url,
              language: job.metadata.language || 'en',
              author: article.author || '',
              publishedDate: article.publishedAt ? new Date(article.publishedAt).toISOString() : null,
              source_name: article.source?.name || ''
            },
            images: article.urlToImage ? [{
              url: article.urlToImage,
              alt: article.title
            }] : [],
            crawled_at: new Date().toISOString()
          };
        });
        
        return {json: {processedItems}};
      `
    }
  },
  {
    "id": "saveApiContent",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/save-content-batch",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "content_items",
            "value": "={{ $json.processedItems }}"
          }
        ]
      }
    }
  }
]
```

## コンテンツ保存と前処理パイプライン

収集したコンテンツを保存し、前処理を行うパイプラインを実装します。

### コンテンツ保存ワークフロー

収集したコンテンツをデータベースに保存するワークフローです。

```javascript
// n8n workflow: Save Content
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "save-content",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "checkDuplicate",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": "SELECT id FROM content WHERE url = '{{ $json.content.url }}' LIMIT 1"
    }
  },
  {
    "id": "processDuplicateCheck",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const content = $input.item.json.content;
        const duplicateCheck = $input.item.json[0].json;
        
        // Check if content already exists
        const isDuplicate = duplicateCheck && duplicateCheck.length > 0;
        
        if (isDuplicate) {
          // Content already exists, update it
          return {
            json: {
              operation: "update",
              content: content,
              existing_id: duplicateCheck[0].id
            }
          };
        } else {
          // New content, insert it
          return {
            json: {
              operation: "insert",
              content: content
            }
          };
        }
      `
    }
  },
  {
    "id": "routeOperation",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "condition": {
        "conditions": [
          {
            "value1": "={{ $json.operation }}",
            "operation": "equal",
            "value2": "insert"
          }
        ]
      }
    }
  },
  {
    "id": "insertContent",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        INSERT INTO content (
          id, source_id, url, title, body, published_at, collected_at, metadata
        ) VALUES (
          gen_random_uuid(),
          '{{ $json.content.source_id }}',
          '{{ $json.content.url }}',
          '{{ $json.content.title }}',
          '{{ $json.content.content }}',
          {{ $json.content.metadata.publishedDate ? "'" + $json.content.metadata.publishedDate + "'" : 'NULL' }},
          '{{ $json.content.crawled_at }}',
          '{{ $json.content.metadata | json | replace("'", "''") }}'::jsonb
        )
        RETURNING id
      `
    }
  },
  {
    "id": "updateContent",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        UPDATE content
        SET
          title = '{{ $json.content.title }}',
          body = '{{ $json.content.content }}',
          published_at = {{ $json.content.metadata.publishedDate ? "'" + $json.content.metadata.publishedDate + "'" : 'NULL' }},
          collected_at = '{{ $json.content.crawled_at }}',
          metadata = '{{ $json.content.metadata | json | replace("'", "''") }}'::jsonb,
          updated_at = CURRENT_TIMESTAMP
        WHERE id = '{{ $json.existing_id }}'
        RETURNING id
      `
    }
  },
  {
    "id": "getContentId",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const operation = $input.item.json.operation;
        let contentId;
        
        if (operation === 'insert') {
          contentId = $input.item.json[0].id;
        } else {
          contentId = $input.item.json.existing_id;
        }
        
        return {
          json: {
            content_id: contentId,
            content: $input.item.json.content
          }
        };
      `
    }
  },
  {
    "id": "saveImages",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {content_id, content} = $input.item.json;
        const images = content.images || [];
        
        if (images.length === 0) {
          return {json: {content_id, image_count: 0}};
        }
        
        // Prepare image data for insertion
        const imageData = images.map((image, index) => ({
          content_id,
          url: image.url,
          alt_text: image.alt || '',
          position: index,
          metadata: {}
        }));
        
        return {json: {content_id, images: imageData, image_count: images.length}};
      `
    }
  },
  {
    "id": "insertImages",
    "type": "n8n-nodes-base.if",
    "parameters": {
      "condition": {
        "conditions": [
          {
            "value1": "={{ $json.image_count }}",
            "operation": "notEqual",
            "value2": 0
          }
        ]
      }
    }
  },
  {
    "id": "saveImagesToDb",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        {% for image in $json.images %}
        INSERT INTO content_images (
          content_id, url, alt_text, position, metadata
        ) VALUES (
          '{{ $json.content_id }}',
          '{{ image.url }}',
          '{{ image.alt_text }}',
          {{ image.position }},
          '{}'::jsonb
        );
        {% endfor %}
      `
    }
  },
  {
    "id": "triggerContentProcessing",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/process-content",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "content_id",
            "value": "={{ $json.content_id }}"
          }
        ]
      }
    }
  }
]
```

### バッチコンテンツ保存ワークフロー

複数のコンテンツアイテムを一括で保存するワークフローです。

```javascript
// n8n workflow: Save Content Batch
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "save-content-batch",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "splitInBatches",
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 1,
      "options": {
        "field": "content_items"
      }
    }
  },
  {
    "id": "saveIndividualContent",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/save-content",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "content",
            "value": "={{ $json }}"
          }
        ]
      }
    }
  }
]
```

### コンテンツ前処理ワークフロー

保存したコンテンツに対して前処理を行うワークフローです。

```javascript
// n8n workflow: Process Content
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "process-content",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getContent",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": "SELECT * FROM content WHERE id = '{{ $json.content_id }}'"
    }
  },
  {
    "id": "normalizeText",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const content = $input.item.json[0];
        
        if (!content) {
          throw new Error('Content not found');
        }
        
        // Normalize text
        let normalizedBody = content.body;
        
        // Remove extra whitespace
        normalizedBody = normalizedBody.replace(/\\s+/g, ' ').trim();
        
        // Remove common boilerplate text (simplified example)
        const boilerplatePatterns = [
          'Please enable JavaScript to view this site.',
          'This site uses cookies.',
          'Accept cookies to continue.',
          'Subscribe to our newsletter',
          'Sign up for our newsletter'
        ];
        
        for (const pattern of boilerplatePatterns) {
          normalizedBody = normalizedBody.replace(new RegExp(pattern, 'gi'), '');
        }
        
        return {
          json: {
            content_id: content.id,
            original_body: content.body,
            normalized_body: normalizedBody,
            metadata: content.metadata
          }
        };
      `
    }
  },
  {
    "id": "detectLanguage",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {content_id, normalized_body, metadata} = $input.item.json;
        
        // Simple language detection based on metadata
        // In a real system, you would use a proper language detection library
        let language = metadata.language || 'en';
        
        // If language is not specified in metadata, try to detect from content
        if (!language || language === 'en') {
          // Very simplified language detection
          // In a real system, you would use a proper language detection library
          const japaneseChars = normalized_body.match(/[\\u3000-\\u303f\\u3040-\\u309f\\u30a0-\\u30ff\\uff00-\\uff9f\\u4e00-\\u9faf]/g);
          const koreanChars = normalized_body.match(/[\\uac00-\\ud7af\\u1100-\\u11ff\\u3130-\\u318f\\uffa0-\\uffdc]/g);
          const chineseChars = normalized_body.match(/[\\u4e00-\\u9fff\\u3400-\\u4dbf]/g);
          
          if (japaneseChars && japaneseChars.length > 10) {
            language = 'ja';
          } else if (koreanChars && koreanChars.length > 10) {
            language = 'ko';
          } else if (chineseChars && chineseChars.length > 10) {
            language = 'zh';
          }
        }
        
        return {
          json: {
            content_id,
            normalized_body,
            language,
            metadata
          }
        };
      `
    }
  },
  {
    "id": "extractEntities",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5000/extract-entities",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "text",
            "value": "={{ $json.normalized_body }}"
          },
          {
            "name": "language",
            "value": "={{ $json.language }}"
          }
        ]
      }
    }
  },
  {
    "id": "processExtractedEntities",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {content_id, normalized_body, language, metadata} = $input.item.json;
        const extractedEntities = $input.item.json.data || {
          entities: [],
          keywords: [],
          summary: ''
        };
        
        // Process entities
        const entities = extractedEntities.entities.map(entity => ({
          type: entity.type,
          text: entity.text,
          relevance: entity.relevance || 0.5
        }));
        
        // Process keywords
        const keywords = extractedEntities.keywords.map(keyword => ({
          text: keyword.text,
          relevance: keyword.relevance || 0.5
        }));
        
        // Get summary
        const summary = extractedEntities.summary || '';
        
        return {
          json: {
            content_id,
            normalized_body,
            language,
            entities,
            keywords,
            summary,
            metadata
          }
        };
      `
    }
  },
  {
    "id": "updateContentWithProcessedData",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        UPDATE content
        SET
          normalized_body = '{{ $json.normalized_body }}',
          language = '{{ $json.language }}',
          entities = '{{ $json.entities | json | replace("'", "''") }}'::jsonb,
          keywords = '{{ $json.keywords | json | replace("'", "''") }}'::jsonb,
          summary = '{{ $json.summary }}',
          processed_at = CURRENT_TIMESTAMP
        WHERE id = '{{ $json.content_id }}'
      `
    }
  },
  {
    "id": "linkContentToTopics",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/link-content-to-topics",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "content_id",
            "value": "={{ $json.content_id }}"
          },
          {
            "name": "keywords",
            "value": "={{ $json.keywords }}"
          },
          {
            "name": "entities",
            "value": "={{ $json.entities }}"
          }
        ]
      }
    }
  }
]
```

### コンテンツとトピックのリンク付けワークフロー

収集したコンテンツを関連するトピックにリンク付けするワークフローです。

```javascript
// n8n workflow: Link Content to Topics
// Trigger: Webhook
[
  {
    "id": "webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "link-content-to-topics",
      "responseMode": "onReceived",
      "options": {}
    }
  },
  {
    "id": "getTopics",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "select",
      "schema": "public",
      "table": "topics",
      "returnAll": true
    }
  },
  {
    "id": "calculateTopicRelevance",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        const {content_id, keywords, entities} = $input.item.json;
        const topics = $input.item.json;
        
        // Calculate relevance score for each topic
        const topicRelevance = [];
        
        for (const topic of topics) {
          // Get topic keywords
          const topicKeywords = topic.keywords || [];
          
          // Calculate keyword match score
          let keywordMatchScore = 0;
          let keywordMatchCount = 0;
          
          for (const topicKeyword of topicKeywords) {
            for (const contentKeyword of keywords) {
              // Check if keywords match (simplified)
              if (contentKeyword.text.toLowerCase().includes(topicKeyword.toLowerCase()) ||
                  topicKeyword.toLowerCase().includes(contentKeyword.text.toLowerCase())) {
                keywordMatchScore += contentKeyword.relevance;
                keywordMatchCount++;
              }
            }
          }
          
          // Calculate entity match score
          let entityMatchScore = 0;
          let entityMatchCount = 0;
          
          for (const entity of entities) {
            // Check if entity is relevant to topic (simplified)
            if (topic.name.toLowerCase().includes(entity.text.toLowerCase()) ||
                entity.text.toLowerCase().includes(topic.name.toLowerCase())) {
              entityMatchScore += entity.relevance;
              entityMatchCount++;
            }
          }
          
          // Calculate overall relevance score
          let relevanceScore = 0;
          
          if (keywordMatchCount > 0) {
            relevanceScore += (keywordMatchScore / keywordMatchCount) * 0.7;
          }
          
          if (entityMatchCount > 0) {
            relevanceScore += (entityMatchScore / entityMatchCount) * 0.3;
          }
          
          // Only include topics with non-zero relevance
          if (relevanceScore > 0) {
            topicRelevance.push({
              content_id,
              topic_id: topic.id,
              relevance_score: relevanceScore
            });
          }
        }
        
        return {json: {topicRelevance}};
      `
    }
  },
  {
    "id": "insertContentTopics",
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "operation": "executeQuery",
      "query": `
        {% for item in $json.topicRelevance %}
        INSERT INTO content_topics (
          content_id, topic_id, relevance_score
        ) VALUES (
          '{{ item.content_id }}',
          '{{ item.topic_id }}',
          {{ item.relevance_score }}
        )
        ON CONFLICT (content_id, topic_id) DO UPDATE
        SET relevance_score = {{ item.relevance_score }};
        {% endfor %}
      `
    }
  },
  {
    "id": "triggerChangeDetection",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "http://localhost:5678/webhook/detect-changes",
      "method": "POST",
      "jsonParameters": true,
      "bodyParameters": {
        "parameters": [
          {
            "name": "content_id",
            "value": "={{ $json.topicRelevance[0].content_id }}"
          }
        ]
      }
    }
  }
]
```

## まとめ

このセクションでは、トリプルパースペクティブ型戦略AIレーダーのデータ収集システムの実装方法について解説しました。n8nを活用することで、多様な情報源からデータを効率的に収集し、前処理を行うシステムを構築することができます。

収集スケジューラ、各種コネクタ、コンテンツ保存と前処理パイプラインを組み合わせることで、高品質なデータセットを自動的に構築し、分析に活用することができます。

次のセクションでは、収集したデータの分析と変化点検出の実装方法について解説します。
