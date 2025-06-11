# 第3章 応用実践演習拡充プラン

## 概要

第3章「n8nと生成AIの連携：ChatGPT・DALL-E・StableDiffusionの活用法」の実践演習セクションを拡充し、より高度で実践的な演習を追加します。これにより、読者が実際のビジネスシーンで応用できるスキルを習得できるようにします。

## 現状の演習内容

現在の第3章には以下の基本的な演習が含まれています：

1. **演習1：ChatGPTによるメール件名自動生成**
   - 基本的なテキスト生成ワークフロー
   - 単一のOpenAIノードの使用

2. **演習2：DALL-Eによる製品紹介用画像生成**
   - 基本的な画像生成ワークフロー
   - 単一のOpenAIノード（Image）の使用

## 拡充する応用演習

### 応用演習1：多段階AIレビュー付き顧客対応システム

**目標**：顧客からの問い合わせメールに対して、ChatGPTが回答案を生成し、その回答案を別のAIプロンプトで品質チェックした上で、承認または修正プロセスを経て送信するワークフローを構築する。

**難易度**：★★★☆☆（中級）

**ビジネス価値**：カスタマーサポート業務の効率化と品質向上。初期対応時間の短縮と一貫した回答品質の確保。

**使用ノード**：
- Gmail / IMAP（トリガー）
- Function（メール内容分析）
- OpenAI（回答案生成）
- OpenAI（回答品質チェック）
- Switch（品質スコアによる分岐）
- Slack（承認リクエスト）
- Wait（承認待ち）
- Gmail / SMTP（返信送信）

**実装手順**：
1. メール受信トリガーの設定
2. メール本文と件名の抽出・分析
3. 第1のOpenAIノードで回答案生成
4. 第2のOpenAIノードで回答品質チェック（敬語、正確性、トーンなど）
5. 品質スコアによる分岐処理
   - 高スコア：自動送信
   - 中スコア：Slackで承認リクエスト
   - 低スコア：要修正としてSlackに通知
6. 承認/修正プロセスの実装
7. 最終回答のメール送信

**発展課題**：
- 顧客タイプ（VIP、一般など）による対応の差別化
- 過去の対応履歴を参照した回答生成
- 特定の製品やサービスに関する専門知識ベースとの連携

### 応用演習2：マルチモーダルAI連携によるコンテンツ自動生成システム

**目標**：ブログ記事のタイトルと概要から、ChatGPTによる記事本文生成、DALL-Eによるアイキャッチ画像生成、そしてStable Diffusionによる補足画像生成を行い、最終的にWordPressに投稿するワークフローを構築する。

**難易度**：★★★★☆（上級）

**ビジネス価値**：コンテンツマーケティング業務の効率化。記事作成時間の大幅短縮と視覚的に魅力的なコンテンツの一貫した生成。

**使用ノード**：
- Manual（トリガー）
- Set（記事タイトルと概要入力）
- OpenAI（記事本文生成）
- OpenAI（アイキャッチ画像生成）
- HTTP Request（Stability AI API連携）
- Write Binary File（画像保存）
- WordPress（記事投稿）
- Slack（完了通知）

**実装手順**：
1. 記事タイトルと概要の入力フォーム設定
2. ChatGPTによる記事本文生成
   - 見出し構造の自動作成
   - SEO最適化指示の組み込み
   - 日本語ライティングスタイルの指定
3. DALL-Eによるアイキャッチ画像生成
   - 記事内容に基づく動的プロンプト生成
   - 画像スタイルの一貫性確保
4. Stability AI APIによる補足画像生成
   - 各セクションに対応する画像生成
   - 画像スタイルの統一
5. 画像の保存と最適化
6. WordPressへの記事投稿設定
   - 本文、画像、メタデータの設定
   - カテゴリとタグの自動割り当て
7. 完了通知の設定

**発展課題**：
- 複数の記事テーマを一括処理するバッチ処理の実装
- SNS投稿用のショート版コンテンツの自動生成
- 競合記事分析と差別化ポイントの自動抽出

### 応用演習3：AIを活用した市場動向分析ダッシュボード

**目標**：特定のキーワードに関するニュース記事、SNS投稿、競合情報などをAPIから収集し、ChatGPTで要約・分析した結果をダッシュボードに自動更新するワークフローを構築する。

**難易度**：★★★★★（エキスパート）

**ビジネス価値**：市場調査・競合分析業務の効率化と高度化。データドリブンな意思決定の促進と市場変化への迅速な対応。

**使用ノード**：
- Schedule（定期実行トリガー）
- HTTP Request（ニュースAPI）
- HTTP Request（Twitter/X API）
- HTTP Request（競合Webサイトスクレイピング）
- Function（データ前処理）
- OpenAI（テキスト分析・要約）
- OpenAI（トレンド可視化用データ生成）
- Function（データ構造化）
- Postgres/MySQL（データ保存）
- HTTP Request（Grafanaダッシュボード更新）
- Slack（重要アラート通知）

**実装手順**：
1. データ収集ソースの設定
   - ニュースAPI（NewsAPI, GNEWS等）の連携
   - SNS API（Twitter/X API等）の連携
   - Webスクレイピング設定（競合サイト、業界ポータル等）
2. データ前処理ロジックの実装
   - 重複排除
   - ノイズフィルタリング
   - 言語検出と翻訳（必要に応じて）
3. ChatGPTによるテキスト分析
   - キーポイント抽出
   - センチメント分析
   - トレンドキーワード抽出
   - 競合動向の要約
4. データ構造化と保存
   - 分析結果のJSON形式への変換
   - データベースへの保存
5. ダッシュボード更新処理
   - Grafana API連携
   - ダッシュボードパネル更新
6. アラート条件設定
   - 重要キーワード検出時のSlack通知
   - 急激なセンチメント変化時のアラート

**発展課題**：
- 複数の競合・製品カテゴリの並行分析
- 予測モデルとの連携による将来トレンド予測
- 自然言語によるダッシュボード操作機能の実装

## 実装詳細：応用演習1

### 多段階AIレビュー付き顧客対応システムの詳細実装

#### ステップ1：メール受信トリガーの設定
```javascript
// IMAPノード設定例
{
  "authentication": "OAuth2",
  "mailbox": "INBOX",
  "action": "get",
  "options": {
    "limit": 10,
    "markSeen": false,
    "filter": {
      "criteria": ["UNSEEN"],
      "operator": "AND"
    }
  }
}
```

#### ステップ2：メール内容分析（Functionノード）
```javascript
// メール内容から問い合わせカテゴリを判定
const subject = items[0].json.subject || '';
const body = items[0].json.text || '';
const combinedText = subject + ' ' + body;

// カテゴリ判定ロジック
let category = 'general';
const keywords = {
  'product': ['製品', '使い方', 'マニュアル', '操作', '機能'],
  'billing': ['請求', '支払い', '料金', '価格', '領収書', '返金'],
  'technical': ['エラー', 'バグ', '動作しない', '接続できない', '問題'],
  'complaint': ['クレーム', '不満', '失望', '残念', '対応が悪い']
};

// キーワードマッチングでカテゴリ判定
for (const [cat, words] of Object.entries(keywords)) {
  if (words.some(word => combinedText.includes(word))) {
    category = cat;
    break;
  }
}

// 緊急度判定
const urgencyKeywords = ['至急', '緊急', 'すぐに', '今すぐ', '重要'];
const isUrgent = urgencyKeywords.some(word => combinedText.includes(word));

// 結果を返す
return [{
  json: {
    ...items[0].json,
    category,
    isUrgent,
    analysisTimestamp: new Date().toISOString()
  }
}];
```

#### ステップ3：回答案生成（OpenAIノード）
```javascript
// OpenAIノード設定例
{
  "authentication": "predefinedCredentialType",
  "resource": "chat",
  "operation": "completion",
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "あなたは日本の企業のカスタマーサポート担当者です。顧客からの問い合わせに対して、丁寧で正確、かつ簡潔な回答を作成してください。以下のガイドラインに従ってください：\n1. 常に敬語を使用する\n2. 具体的な情報を提供する\n3. 必要に応じて追加の質問をする\n4. 会社の評判を守る表現を使う\n5. 長すぎる回答は避ける（300字程度に収める）"
    },
    {
      "role": "user",
      "content": "以下は顧客からの問い合わせメールです。適切な返信を作成してください。\n\nカテゴリ: {{$node[\"Function\"].json[\"category\"]}}\n緊急度: {{$node[\"Function\"].json[\"isUrgent\"] ? \"高\" : \"通常\"}}\n\n件名: {{$node[\"IMAP\"].json[\"subject\"]}}\n\n本文:\n{{$node[\"IMAP\"].json[\"text\"]}}"
    }
  ],
  "options": {
    "temperature": 0.3
  }
}
```

#### ステップ4：回答品質チェック（OpenAIノード）
```javascript
// OpenAIノード設定例（品質チェック用）
{
  "authentication": "predefinedCredentialType",
  "resource": "chat",
  "operation": "completion",
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "あなたは日本企業のカスタマーサポート品質管理者です。AIが生成した顧客への返信案を評価し、1〜10のスコアと改善点を提供してください。以下の基準で評価します：\n- 敬語の適切さ（敬語が正しく使われているか）\n- 回答の正確性（質問に正確に答えているか）\n- トーンの適切さ（丁寧すぎず、カジュアルすぎないか）\n- 簡潔さ（必要な情報を簡潔に伝えているか）\n- 追加情報の提供（役立つ追加情報があるか）"
    },
    {
      "role": "user",
      "content": "以下の顧客問い合わせとAIが生成した返信案を評価してください。\n\n【顧客問い合わせ】\n件名: {{$node[\"IMAP\"].json[\"subject\"]}}\n本文: {{$node[\"IMAP\"].json[\"text\"]}}\n\n【AI生成返信案】\n{{$node[\"OpenAI\"].json[\"response\"]}}}"
    }
  ],
  "options": {
    "temperature": 0.3
  }
}
```

#### ステップ5：品質スコアによる分岐処理（Functionノード）
```javascript
// 品質評価結果からスコアを抽出
const evaluationText = items[0].json.response || '';
const scoreMatch = evaluationText.match(/(\d+)\/10|スコア[：:]\s*(\d+)/);
let score = 0;

if (scoreMatch) {
  // マッチした数字を取得
  score = parseInt(scoreMatch[1] || scoreMatch[2] || 0);
}

// 改善点の抽出
const improvementMatch = evaluationText.match(/改善点[：:]([\s\S]+?)(?=\n\n|\n$|$)/);
const improvements = improvementMatch ? improvementMatch[1].trim() : '特になし';

// 処理分岐の決定
let route = 'manual_review';
if (score >= 8) {
  route = 'auto_send';
} else if (score >= 6) {
  route = 'approval_required';
} else {
  route = 'manual_review';
}

// 結果を返す
return [{
  json: {
    ...items[0].json,
    qualityScore: score,
    improvements,
    route,
    evaluationTimestamp: new Date().toISOString()
  }
}];
```

#### ステップ6：承認/修正プロセス（Slackノード）
```javascript
// Slackノード設定例（承認リクエスト用）
{
  "authentication": "predefinedCredentialType",
  "channel": "customer-support-approvals",
  "text": "🔄 *顧客返信の承認リクエスト*\n\n*カテゴリ:* {{$node[\"Function\"].json[\"category\"]}}\n*緊急度:* {{$node[\"Function\"].json[\"isUrgent\"] ? \"⚠️ 高\" : \"通常\"}}\n*品質スコア:* {{$node[\"Function1\"].json[\"qualityScore\"]}}/10\n\n*顧客問い合わせ:*\n```\n件名: {{$node[\"IMAP\"].json[\"subject\"]}}\n\n{{$node[\"IMAP\"].json[\"text\"]}}\n```\n\n*提案された返信:*\n```\n{{$node[\"OpenAI\"].json[\"response\"]}}\n```\n\n*品質評価コメント:*\n```\n{{$node[\"Function1\"].json[\"improvements\"]}}\n```",
  "attachments": [
    {
      "actions": [
        {
          "name": "approve",
          "text": "承認して送信",
          "type": "button",
          "value": "approve"
        },
        {
          "name": "edit",
          "text": "編集が必要",
          "type": "button",
          "value": "edit"
        }
      ]
    }
  ],
  "otherOptions": {
    "thread_ts": "{{$node[\"IMAP\"].json[\"messageId\"]}}"
  }
}
```

#### ステップ7：最終回答のメール送信（Gmailノード）
```javascript
// Gmailノード設定例
{
  "authentication": "predefinedCredentialType",
  "resource": "message",
  "operation": "send",
  "subject": "Re: {{$node[\"IMAP\"].json[\"subject\"]}}",
  "text": "{{$node[\"OpenAI\"].json[\"response\"]}}{{$node[\"Function2\"] ? $node[\"Function2\"].json[\"editedResponse\"] : ''}}",
  "to": "{{$node[\"IMAP\"].json[\"from\"]}}",
  "options": {
    "inReplyTo": "{{$node[\"IMAP\"].json[\"messageId\"]}}",
    "references": "{{$node[\"IMAP\"].json[\"messageId\"]}}"
  }
}
```

## 実装詳細：応用演習2

### マルチモーダルAI連携によるコンテンツ自動生成システムの詳細実装

#### ステップ1：記事タイトルと概要入力（Setノード）
```javascript
// Setノード設定例
{
  "articleTitle": "n8nとChatGPTを活用した業務効率化の最新トレンド",
  "articleSummary": "本記事では、ノーコード自動化ツールn8nと生成AI（ChatGPT）を組み合わせた業務効率化の最新事例と導入方法について解説します。特に日本企業における活用シナリオと、ROI向上のポイントに焦点を当てます。",
  "targetAudience": "IT管理者、業務改善担当者、DX推進担当者",
  "keywordsToInclude": ["業務自動化", "ノーコード開発", "生成AI活用", "DX推進", "ROI最大化"],
  "desiredLength": "2000字程度",
  "articleStyle": "解説型、具体例を含む、専門的だが初心者にも理解しやすい"
}
```

#### ステップ2：記事本文生成（OpenAIノード）
```javascript
// OpenAIノード設定例（記事本文生成用）
{
  "authentication": "predefinedCredentialType",
  "resource": "chat",
  "operation": "completion",
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "あなたは経験豊富なテクノロジーライターです。読者に価値のある、SEO最適化された記事を作成してください。以下のガイドラインに従ってください：\n1. 見出し（H2, H3）を適切に使用する\n2. 導入、本文、まとめの構成を守る\n3. 専門用語は初出時に簡潔に説明する\n4. 具体的な例や事例を含める\n5. 読者の行動を促す結論で締めくくる"
    },
    {
      "role": "user",
      "content": "以下の情報に基づいて記事を作成してください。\n\n【タイトル】\n{{$node[\"Set\"].json[\"articleTitle\"]}}\n\n【概要】\n{{$node[\"Set\"].json[\"articleSummary\"]}}\n\n【ターゲット読者】\n{{$node[\"Set\"].json[\"targetAudience\"]}}\n\n【含めるべきキーワード】\n{{$node[\"Set\"].json[\"keywordsToInclude\"].join(\", \")}}\n\n【記事の長さ】\n{{$node[\"Set\"].json[\"desiredLength\"]}}\n\n【スタイル】\n{{$node[\"Set\"].json[\"articleStyle\"]}}\n\n記事はMarkdown形式で作成し、見出しには # (H1), ## (H2), ### (H3) を使用してください。"
    }
  ],
  "options": {
    "temperature": 0.7
  }
}
```

#### ステップ3：アイキャッチ画像生成（OpenAIノード）
```javascript
// OpenAIノード設定例（DALL-E画像生成用）
{
  "authentication": "predefinedCredentialType",
  "resource": "image",
  "operation": "create",
  "prompt": "以下の記事タイトルと概要に基づいたアイキャッチ画像を生成してください。モダンでプロフェッショナルなデザイン、ブルーとグレーのカラースキーム、テクノロジーをテーマにした抽象的なイメージ。テキストは含めないでください。\n\nタイトル: {{$node[\"Set\"].json[\"articleTitle\"]}}\n概要: {{$node[\"Set\"].json[\"articleSummary\"]}}",
  "n": 1,
  "size": "1024x1024",
  "responseFormat": "url"
}
```

#### ステップ4：補足画像生成（HTTP Requestノード - Stability AI API）
```javascript
// HTTP Requestノード設定例（Stability AI API用）
{
  "url": "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
  "method": "POST",
  "authentication": "predefinedCredentialType",
  "headers": {
    "Content-Type": "application/json",
    "Accept": "application/json"
  },
  "body": {
    "text_prompts": [
      {
        "text": "n8nとChatGPTの連携を示す図。ワークフローの自動化とAIの統合を視覚的に表現。ブルーとグレーのカラースキーム、ミニマルでクリーンなデザイン、テキストなし。",
        "weight": 1
      }
    ],
    "cfg_scale": 7,
    "height": 1024,
    "width": 1024,
    "samples": 1,
    "steps": 50
  }
}
```

#### ステップ5：画像保存（Write Binary Fileノード）
```javascript
// Write Binary Fileノード設定例（DALL-E画像保存用）
{
  "fileName": "/tmp/featured-image-{{$timestamp}}.png",
  "binaryPropertyName": "data",
  "binaryData": "{{$node[\"HTTP Request\"].json[\"binary\"][\"data\"][\"data\"]}}",
  "fileFormat": "binary"
}
```

#### ステップ6：WordPress投稿（WordPressノード）
```javascript
// WordPressノード設定例
{
  "authentication": "predefinedCredentialType",
  "resource": "post",
  "operation": "create",
  "title": "{{$node[\"Set\"].json[\"articleTitle\"]}}",
  "content": "{{$node[\"OpenAI\"].json[\"response\"]}}",
  "status": "draft",
  "featuredMedia": "{{$node[\"Write Binary File\"].json[\"fileUrl\"]}}",
  "additionalFields": {
    "categories": [3, 5],  // カテゴリID
    "tags": [7, 12, 15],   // タグID
    "excerpt": "{{$node[\"Set\"].json[\"articleSummary\"]}}",
    "slug": "{{$node[\"Set\"].json[\"articleTitle\"].toLowerCase().replace(/[^a-z0-9]+/g, '-')}}"
  }
}
```

#### ステップ7：完了通知（Slackノード）
```javascript
// Slackノード設定例（完了通知用）
{
  "authentication": "predefinedCredentialType",
  "channel": "content-marketing",
  "text": "✅ *新しい記事が自動生成されました*\n\n*タイトル:* {{$node[\"Set\"].json[\"articleTitle\"]}}\n\n*概要:* {{$node[\"Set\"].json[\"articleSummary\"]}}\n\n*WordPressステータス:* ドラフト\n*投稿ID:* {{$node[\"WordPress\"].json[\"id\"]}}\n\n編集画面: {{$node[\"WordPress\"].json[\"link\"]}}/wp-admin/post.php?post={{$node[\"WordPress\"].json[\"id\"]}}&action=edit",
  "attachments": [
    {
      "title": "アイキャッチ画像プレビュー",
      "image_url": "{{$node[\"Write Binary File\"].json[\"fileUrl\"]}}"
    }
  ]
}
```

## 実装詳細：応用演習3

### AIを活用した市場動向分析ダッシュボードの詳細実装

#### ステップ1：データ収集（HTTP Requestノード - ニュースAPI）
```javascript
// HTTP Requestノード設定例（NewsAPI用）
{
  "url": "https://newsapi.org/v2/everything",
  "method": "GET",
  "authentication": "predefinedCredentialType",
  "qs": {
    "q": "n8n OR \"workflow automation\" OR \"no-code automation\" OR \"business process automation\"",
    "language": "ja",
    "sortBy": "publishedAt",
    "pageSize": 100,
    "from": "{{$today.minus({ days: 7 }).format(\"YYYY-MM-DD\")}}",
    "to": "{{$today.format(\"YYYY-MM-DD\")}}"
  }
}
```

#### ステップ2：データ前処理（Functionノード）
```javascript
// Functionノード設定例（ニュースデータ前処理用）
const articles = items[0].json.articles || [];
const processedArticles = [];

// 重複除去用のURLセット
const urlSet = new Set();

for (const article of articles) {
  // 既に処理済みのURLはスキップ
  if (urlSet.has(article.url)) continue;
  urlSet.add(article.url);
  
  // 必要なフィールドを抽出
  const processedArticle = {
    title: article.title,
    description: article.description,
    content: article.content,
    url: article.url,
    source: article.source.name,
    publishedAt: article.publishedAt,
    // データソースを追加
    dataSource: 'news',
    // 言語を検出（簡易版）
    language: detectLanguage(article.title + ' ' + article.description),
    // 収集タイムスタンプ
    collectedAt: new Date().toISOString()
  };
  
  processedArticles.push(processedArticle);
}

// 簡易言語検出関数
function detectLanguage(text) {
  const jaRegex = /[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf]/g;
  const jaChars = text.match(jaRegex);
  
  if (jaChars && jaChars.length > 5) {
    return 'ja';
  }
  return 'en';
}

return processedArticles.map(article => ({ json: article }));
```

#### ステップ3：テキスト分析（OpenAIノード）
```javascript
// OpenAIノード設定例（テキスト分析用）
{
  "authentication": "predefinedCredentialType",
  "resource": "chat",
  "operation": "completion",
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "あなたは市場動向分析の専門家です。提供されるニュース記事やSNS投稿を分析し、以下の情報を抽出してJSON形式で返してください：\n1. 主要トピック（3つまで）\n2. センチメント（positive, neutral, negative）とその理由\n3. 業界への影響度（1-10のスケール）\n4. 重要キーワード（5つまで）\n5. 競合企業への言及（あれば）\n6. 市場トレンドの示唆（あれば）"
    },
    {
      "role": "user",
      "content": "以下の記事を分析してください：\n\nタイトル: {{$node[\"Function\"].json[\"title\"]}}\n\n概要: {{$node[\"Function\"].json[\"description\"]}}\n\n本文: {{$node[\"Function\"].json[\"content\"]}}\n\n出典: {{$node[\"Function\"].json[\"source\"]}}\n\n公開日: {{$node[\"Function\"].json[\"publishedAt\"]}}"
    }
  ],
  "options": {
    "temperature": 0.3
  }
}
```

#### ステップ4：データ構造化（Functionノード）
```javascript
// Functionノード設定例（分析結果構造化用）
const analysisText = items[0].json.response || '';
let structuredData = {};

try {
  // JSONレスポンスを抽出（OpenAIが常にJSONを返すとは限らないため）
  const jsonMatch = analysisText.match(/```json\n([\s\S]*?)\n```/) || 
                   analysisText.match(/\{[\s\S]*\}/);
  
  if (jsonMatch) {
    structuredData = JSON.parse(jsonMatch[1] || jsonMatch[0]);
  } else {
    // JSONでない場合は手動でパース
    structuredData = {
      topics: extractList(analysisText, /主要トピック[：:]([\s\S]*?)(?=\n\n|\nセンチメント)/),
      sentiment: extractSentiment(analysisText),
      impact: extractNumber(analysisText, /影響度[：:]\s*(\d+)/),
      keywords: extractList(analysisText, /重要キーワード[：:]([\s\S]*?)(?=\n\n|\n競合)/),
      competitors: extractList(analysisText, /競合企業[：:]([\s\S]*?)(?=\n\n|\n市場)/),
      trends: extractText(analysisText, /市場トレンド[：:]([\s\S]*?)(?=\n\n|$)/)
    };
  }
  
  // 元の記事データを追加
  structuredData.sourceData = {
    title: items[0].json.title,
    url: items[0].json.url,
    source: items[0].json.source,
    publishedAt: items[0].json.publishedAt,
    dataSource: items[0].json.dataSource,
    language: items[0].json.language
  };
  
  // 分析タイムスタンプを追加
  structuredData.analysisTimestamp = new Date().toISOString();
  
} catch (error) {
  // エラー時のフォールバック
  structuredData = {
    error: true,
    errorMessage: error.message,
    rawResponse: analysisText,
    sourceData: {
      title: items[0].json.title,
      url: items[0].json.url
    }
  };
}

// ヘルパー関数
function extractList(text, regex) {
  const match = text.match(regex);
  if (!match) return [];
  
  return match[1].split(/[,、\n]/)
    .map(item => item.trim().replace(/^[-・]/, ''))
    .filter(item => item.length > 0);
}

function extractSentiment(text) {
  const match = text.match(/センチメント[：:]\s*(\w+)/);
  return match ? match[1].toLowerCase() : 'neutral';
}

function extractNumber(text, regex) {
  const match = text.match(regex);
  return match ? parseInt(match[1]) : 5;
}

function extractText(text, regex) {
  const match = text.match(regex);
  return match ? match[1].trim() : '';
}

return [{ json: structuredData }];
```

#### ステップ5：データベース保存（PostgreSQLノード）
```javascript
// PostgreSQLノード設定例
{
  "operation": "insert",
  "schema": "public",
  "table": "market_analysis",
  "columns": "title, url, source, published_at, topics, sentiment, impact_score, keywords, competitors, trends, analysis_timestamp",
  "values": "{{$node[\"Function1\"].json[\"sourceData\"][\"title\"]}}, {{$node[\"Function1\"].json[\"sourceData\"][\"url\"]}}, {{$node[\"Function1\"].json[\"sourceData\"][\"source\"]}}, {{$node[\"Function1\"].json[\"sourceData\"][\"publishedAt\"]}}, {{JSON.stringify($node[\"Function1\"].json[\"topics\"])}}, {{$node[\"Function1\"].json[\"sentiment\"]}}, {{$node[\"Function1\"].json[\"impact\"]}}, {{JSON.stringify($node[\"Function1\"].json[\"keywords\"])}}, {{JSON.stringify($node[\"Function1\"].json[\"competitors\"])}}, {{$node[\"Function1\"].json[\"trends\"]}}, {{$node[\"Function1\"].json[\"analysisTimestamp\"]}}"
}
```

#### ステップ6：ダッシュボード更新（HTTP Requestノード - Grafana API）
```javascript
// HTTP Requestノード設定例（Grafana API用）
{
  "url": "http://grafana-server:3000/api/dashboards/db",
  "method": "POST",
  "authentication": "predefinedCredentialType",
  "headers": {
    "Content-Type": "application/json",
    "Accept": "application/json"
  },
  "body": {
    "dashboard": {
      "id": null,
      "uid": "market-trends-dashboard",
      "title": "市場動向分析ダッシュボード",
      "tags": ["market-analysis", "ai-generated"],
      "timezone": "browser",
      "schemaVersion": 16,
      "version": 1,
      "refresh": "5m",
      "panels": [
        {
          "id": 1,
          "title": "トピック分布",
          "type": "piechart",
          "datasource": "PostgreSQL",
          "targets": [
            {
              "rawSql": "SELECT unnest(topics) as topic, count(*) FROM market_analysis WHERE analysis_timestamp > now() - interval '7 days' GROUP BY topic ORDER BY count(*) DESC LIMIT 10",
              "refId": "A"
            }
          ]
        },
        {
          "id": 2,
          "title": "センチメント推移",
          "type": "timeseries",
          "datasource": "PostgreSQL",
          "targets": [
            {
              "rawSql": "SELECT date_trunc('day', analysis_timestamp) as time, sentiment, count(*) FROM market_analysis WHERE analysis_timestamp > now() - interval '30 days' GROUP BY time, sentiment ORDER BY time",
              "refId": "A"
            }
          ]
        }
        // 他のパネル定義は省略
      ]
    },
    "overwrite": true
  }
}
```

#### ステップ7：重要アラート通知（Slackノード）
```javascript
// Slackノード設定例（条件付き実行）
{
  "authentication": "predefinedCredentialType",
  "channel": "market-alerts",
  "text": "🚨 *重要な市場動向アラート*\n\n*タイトル:* {{$node[\"Function\"].json[\"sourceData\"][\"title\"]}}\n\n*影響度:* {{$node[\"Function1\"].json[\"impact\"]}}/10\n\n*センチメント:* {{$node[\"Function1\"].json[\"sentiment\"]}}\n\n*主要トピック:*\n{{$node[\"Function1\"].json[\"topics\"].map(topic => `• ${topic}`).join(\"\\n\")}}\n\n*市場トレンドの示唆:*\n{{$node[\"Function1\"].json[\"trends\"]}}\n\n*ソース:* {{$node[\"Function\"].json[\"sourceData\"][\"source\"]}}\n*URL:* {{$node[\"Function\"].json[\"sourceData\"][\"url\"]}}",
  "attachments": [
    {
      "color": "{{$node[\"Function1\"].json[\"sentiment\"] === 'positive' ? '#36a64f' : $node[\"Function1\"].json[\"sentiment\"] === 'negative' ? '#d72b3f' : '#2196f3'}}",
      "title": "詳細分析を見る",
      "title_link": "http://grafana-server:3000/d/market-trends-dashboard"
    }
  ]
}
```

## 演習の進め方

各応用演習は、以下のステップで進めることを推奨します：

1. **基本構成の理解**：まず各演習の目標と全体的なワークフローの流れを理解します。
2. **段階的な実装**：一度にすべてを実装するのではなく、各ステップを順番に実装し、動作確認しながら進めます。
3. **エラーハンドリングの追加**：基本機能が動作したら、エラーハンドリングやフォールバック処理を追加します。
4. **最適化とカスタマイズ**：自社の環境や要件に合わせて、プロンプトやパラメータを調整します。
5. **発展課題への挑戦**：基本機能が完成したら、発展課題に取り組み、より高度な機能を実装します。

## 評価基準

演習の完成度は以下の基準で評価できます：

- **機能性**：設計通りの機能が実装されているか
- **エラー耐性**：例外的な状況やエラーに適切に対応できるか
- **拡張性**：新しい要件や変更に対応しやすい設計になっているか
- **実用性**：実際のビジネスシーンで活用できる実用的な実装になっているか
- **創造性**：独自の工夫や改善点が盛り込まれているか

## まとめ

これらの応用演習を通じて、n8nと生成AIの連携による高度な自動化の可能性を体験できます。単なる技術的な実装にとどまらず、実際のビジネス課題解決や価値創出につながる実践的なスキルを習得することが目標です。各演習は、基本から応用へと段階的に難易度が上がるよう設計されていますので、順を追って取り組むことで、着実にスキルを向上させることができます。
