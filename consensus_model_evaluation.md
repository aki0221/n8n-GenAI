# 評価プロセス全体のフロー図

## 評価プロセス全体のフロー図 (Mermaid)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f0f0', 'primaryTextColor': '#323232', 'primaryBorderColor': '#888888', 'lineColor': '#555555', 'secondaryColor': '#e0e0e0', 'tertiaryColor': '#f9f9f9'}}}%%

flowchart TD
    classDef input fill:#DAE8FC,stroke:#6C8EBF,color:#0D5AA7,stroke-width:2px
    classDef process fill:#D5E8D4,stroke:#82B366,color:#006400,stroke-width:1px
    classDef database fill:#FFE6CC,stroke:#D79B00,color:#D79B00,stroke-width:1px
    classDef output fill:#F8CECC,stroke:#B85450,color:#B85450,stroke-width:1px
    classDef subheader fill:none,stroke:#555555,color:#333333,stroke-width:1px,stroke-dasharray: 5 5
    
    %% タイトルと説明
    title["<b>コンセンサスモデル評価プロセス全体フロー</b><br/>視点別評価と整合性評価の連携による多層的評価システム"]
    title:::subheader
    
    %% 入力データ
    Input["入力: 視点別情報<br/>(変化点, 分析結果)"]:::input
    
    %% 視点別評価プロセス
    subgraph PerspectiveEval["視点別評価プロセス (n8n Workflow 1)"]
        direction TB
        WebhookTrigger["Webhook Trigger<br/>/evaluate-perspective"]:::process
        GetData["Function Node<br/>getPerspectiveData()"]:::process
        
        subgraph ImportanceEval["重要度評価コンポーネント"]
            direction TB
            ImpactScope["影響範囲評価<br/>(Impact Scope)"]:::process
            ChangeMagnitude["変化の大きさ評価<br/>(Change Magnitude)"]:::process
            StrategicRelevance["戦略的関連性評価<br/>(Strategic Relevance)"]:::process
            TimeUrgency["時間的緊急性評価<br/>(Time Urgency)"]:::process
            ImportanceCalc["重要度統合計算<br/>(Weighted Score)"]:::process
            
            ImpactScope --> ImportanceCalc
            ChangeMagnitude --> ImportanceCalc
            StrategicRelevance --> ImportanceCalc
            TimeUrgency --> ImportanceCalc
        end
        
        subgraph ConfidenceEval["確信度評価コンポーネント"]
            direction TB
            SourceReliability["情報源信頼性評価<br/>(Source Reliability)"]:::process
            DataQuality["データ量・質評価<br/>(Data Volume/Quality)"]:::process
            Consistency["一貫性評価<br/>(Consistency)"]:::process
            Verifiability["検証可能性評価<br/>(Verifiability)"]:::process
            ConfidenceCalc["確信度統合計算<br/>(Weighted Score)"]:::process
            
            SourceReliability --> ConfidenceCalc
            DataQuality --> ConfidenceCalc
            Consistency --> ConfidenceCalc
            Verifiability --> ConfidenceCalc
        end
        
        EvaluatePerspective["Function Node<br/>evaluatePerspective()"]:::process
        SaveDB["Postgres Node<br/>savePerspectiveEvaluation()"]:::process
        TriggerCoherence["HTTP Request Node<br/>triggerCoherenceEvaluation()"]:::process
        
        WebhookTrigger --> GetData
        GetData --> EvaluatePerspective
        EvaluatePerspective --> ImportanceEval
        EvaluatePerspective --> ConfidenceEval
        ImportanceEval --> SaveDB
        ConfidenceEval --> SaveDB
        SaveDB --> TriggerCoherence
    end
    
    %% データベース
    DB[(評価結果DB<br/>perspective_evaluations)]:::database
    
    %% 整合性評価プロセス
    subgraph CoherenceEval["整合性評価プロセス (n8n Workflow 2)"]
        direction TB
        CoherenceWebhook["Webhook Trigger<br/>/check-coherence"]:::process
        GetEvaluations["Function Node<br/>getPerspectiveEvaluations()"]:::process
        
        subgraph CoherenceComponents["整合性評価コンポーネント"]
            direction TB
            PerspectiveAgreement["視点間一致度評価<br/>(Perspective Agreement)"]:::process
            LogicalCoherence["論理的整合性評価<br/>(Logical Coherence)"]:::process
            TemporalCoherence["時間的整合性評価<br/>(Temporal Coherence)"]:::process
            ContextualCoherence["コンテキスト整合性評価<br/>(Contextual Coherence)"]:::process
            CoherenceCalc["整合性統合計算<br/>(Weighted Score)"]:::process
            
            PerspectiveAgreement --> CoherenceCalc
            LogicalCoherence --> CoherenceCalc
            TemporalCoherence --> CoherenceCalc
            ContextualCoherence --> CoherenceCalc
        end
        
        EvaluateCoherence["Function Node<br/>evaluateCoherence()"]:::process
        SaveCoherence["Postgres Node<br/>saveCoherenceEvaluation()"]:::process
        
        CoherenceWebhook --> GetEvaluations
        GetEvaluations --> EvaluateCoherence
        EvaluateCoherence --> CoherenceComponents
        CoherenceComponents --> SaveCoherence
    end
    
    %% 出力
    Output["出力: 統合評価結果<br/>(重要度, 確信度, 整合性)"]:::output
    
    %% 接続
    Input --> WebhookTrigger
    SaveDB --> DB
    DB --> GetEvaluations
    SaveCoherence --> DB
    DB --> Output
    
    %% フィードバックループ
    Output -.-> |"フィードバック<br/>(パラメータ調整)"| WebhookTrigger
    
    %% 注釈
    Note["<b>評価プロセスの特徴</b><br/>・多層的評価: 重要度、確信度、整合性の3軸<br/>・データ永続化: 評価結果の履歴管理<br/>・フィードバックループ: 継続的な精度向上<br/>・n8n実装: 2つの連携ワークフロー"]:::subheader
    Note -.-> PerspectiveEval
```

## 図の説明

この図は、コンセンサスモデルの評価プロセス全体を視覚的に表現したものです。評価プロセスは大きく「視点別評価プロセス」と「整合性評価プロセス」の2つの主要コンポーネントで構成され、それぞれがn8nの独立したワークフローとして実装されます。

### 主要コンポーネント

1. **視点別評価プロセス (n8n Workflow 1)**:
   - Webhookトリガーで起動し、評価対象の視点（テクノロジー、マーケット、ビジネス）の情報を取得
   - 重要度評価コンポーネントで影響範囲、変化の大きさ、戦略的関連性、時間的緊急性を評価
   - 確信度評価コンポーネントで情報源信頼性、データ量・質、一貫性、検証可能性を評価
   - 評価結果をデータベースに保存し、整合性評価プロセスをトリガー

2. **整合性評価プロセス (n8n Workflow 2)**:
   - Webhookトリガーで起動し、データベースから各視点の評価結果を取得
   - 視点間一致度、論理的整合性、時間的整合性、コンテキスト整合性を評価
   - 整合性評価結果をデータベースに保存

3. **データベース**:
   - 視点別評価結果と整合性評価結果を永続化
   - 履歴データとして保存し、時系列分析や傾向把握に活用

### データフロー

1. **入力**: 各視点（テクノロジー、マーケット、ビジネス）からの情報（変化点、分析結果など）
2. **処理**: 視点別評価プロセスで重要度と確信度を評価し、整合性評価プロセスで視点間の整合性を評価
3. **出力**: 重要度、確信度、整合性の3軸に基づく統合評価結果
4. **フィードバック**: 評価結果に基づくパラメータ調整や評価ロジックの改善

### 実装上の特徴

- **n8nワークフロー**: 2つの独立したワークフローとして実装し、Webhook、Function、Databaseノードを活用
- **モジュール性**: 各評価コンポーネントを独立したサブグラフとして設計し、拡張性と保守性を確保
- **データ永続化**: PostgreSQLデータベースを使用して評価結果を永続化し、履歴管理を実現
- **フィードバックループ**: 評価結果に基づくパラメータ調整や評価ロジックの改善を可能にする設計

この評価プロセス全体のフロー図により、コンセンサスモデルの中核をなす評価メカニズムの構造と動作を理解することができます。各コンポーネントの詳細な実装については、コード例やパラメータ設定などの追加情報が必要です。
