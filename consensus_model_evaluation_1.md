# 評価計算フロー図

## 1. 重要度評価計算フロー図 (Mermaid)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f0f0', 'primaryTextColor': '#323232', 'primaryBorderColor': '#888888', 'lineColor': '#555555', 'secondaryColor': '#e0e0e0', 'tertiaryColor': '#f9f9f9'}}}%%

flowchart TD
    classDef input fill:#DAE8FC,stroke:#6C8EBF,color:#0D5AA7,stroke-width:2px
    classDef process fill:#D5E8D4,stroke:#82B366,color:#006400,stroke-width:1px
    classDef parameter fill:#FFE6CC,stroke:#D79B00,color:#D79B00,stroke-width:1px
    classDef output fill:#F8CECC,stroke:#B85450,color:#B85450,stroke-width:1px
    classDef formula fill:#E1D5E7,stroke:#9673A6,color:#9673A6,stroke-width:1px
    classDef subheader fill:none,stroke:#555555,color:#333333,stroke-width:1px,stroke-dasharray: 5 5
    
    %% タイトルと説明
    title["<b>重要度評価計算フロー</b><br/>影響範囲・変化の大きさ・戦略的関連性・時間的緊急性の統合評価"]
    title:::subheader
    
    %% 入力データ
    RawData["入力データ<br/>(変化点情報, 分析結果)"]:::input
    
    %% パラメータ
    subgraph Parameters["パラメータ設定"]
        direction LR
        WeightImpact["影響範囲の重み<br/>w_impact = 0.3"]:::parameter
        WeightChange["変化の大きさの重み<br/>w_change = 0.25"]:::parameter
        WeightStrategy["戦略的関連性の重み<br/>w_strategy = 0.25"]:::parameter
        WeightUrgency["時間的緊急性の重み<br/>w_urgency = 0.2"]:::parameter
        Thresholds["重要度レベル閾値<br/>高: ≥0.7, 中: ≥0.4, 低: <0.4"]:::parameter
    end
    
    %% 前処理
    Preprocess["データ前処理<br/>(正規化, 欠損値処理)"]:::process
    
    %% 各要素の評価
    subgraph ElementEval["要素別評価 (n8n Function Node)"]
        direction TB
        ImpactEval["影響範囲評価<br/>impactScore = evaluateImpact(data)"]:::process
        ChangeEval["変化の大きさ評価<br/>changeScore = evaluateChange(data)"]:::process
        StrategyEval["戦略的関連性評価<br/>strategyScore = evaluateStrategy(data)"]:::process
        UrgencyEval["時間的緊急性評価<br/>urgencyScore = evaluateUrgency(data)"]:::process
    end
    
    %% 重み付け計算
    WeightedCalc["重み付け計算 (n8n Function Node)"]:::process
    
    %% 計算式
    Formula["<b>重要度スコア計算式</b><br/>importanceScore = <br/>w_impact * impactScore + <br/>w_change * changeScore + <br/>w_strategy * strategyScore + <br/>w_urgency * urgencyScore"]:::formula
    
    %% レベル判定
    LevelDetermination["重要度レベル判定<br/>(n8n If Node)"]:::process
    
    %% 出力
    ImportanceOutput["出力: 重要度評価結果<br/>{score: 0.0-1.0, level: '高'|'中'|'低'}"]:::output
    
    %% 接続
    RawData --> Preprocess
    Preprocess --> ElementEval
    ElementEval --> WeightedCalc
    Parameters --> WeightedCalc
    WeightedCalc --> Formula
    Formula --> LevelDetermination
    Parameters --> LevelDetermination
    LevelDetermination --> ImportanceOutput
    
    %% 注釈
    Note["<b>実装上の注意点</b><br/>・各要素評価は0.0-1.0の範囲に正規化<br/>・重み係数の合計は1.0に設定<br/>・閾値はコンテキストに応じて調整可能<br/>・n8n Function Nodeで実装"]:::subheader
    Note -.-> ElementEval
```

## 2. 確信度評価計算フロー図 (Mermaid)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f0f0', 'primaryTextColor': '#323232', 'primaryBorderColor': '#888888', 'lineColor': '#555555', 'secondaryColor': '#e0e0e0', 'tertiaryColor': '#f9f9f9'}}}%%

flowchart TD
    classDef input fill:#DAE8FC,stroke:#6C8EBF,color:#0D5AA7,stroke-width:2px
    classDef process fill:#D5E8D4,stroke:#82B366,color:#006400,stroke-width:1px
    classDef parameter fill:#FFE6CC,stroke:#D79B00,color:#D79B00,stroke-width:1px
    classDef output fill:#F8CECC,stroke:#B85450,color:#B85450,stroke-width:1px
    classDef formula fill:#E1D5E7,stroke:#9673A6,color:#9673A6,stroke-width:1px
    classDef subheader fill:none,stroke:#555555,color:#333333,stroke-width:1px,stroke-dasharray: 5 5
    
    %% タイトルと説明
    title["<b>確信度評価計算フロー</b><br/>情報源信頼性・データ量質・一貫性・検証可能性の統合評価"]
    title:::subheader
    
    %% 入力データ
    RawData["入力データ<br/>(情報源メタデータ, データ特性)"]:::input
    
    %% パラメータ
    subgraph Parameters["パラメータ設定"]
        direction LR
        WeightSource["情報源信頼性の重み<br/>w_source = 0.35"]:::parameter
        WeightData["データ量・質の重み<br/>w_data = 0.25"]:::parameter
        WeightConsistency["一貫性の重み<br/>w_consistency = 0.2"]:::parameter
        WeightVerify["検証可能性の重み<br/>w_verify = 0.2"]:::parameter
        Thresholds["確信度レベル閾値<br/>高: ≥0.75, 中: ≥0.5, 低: <0.5"]:::parameter
    end
    
    %% 前処理
    Preprocess["メタデータ前処理<br/>(情報源分類, データ特性抽出)"]:::process
    
    %% 各要素の評価
    subgraph ElementEval["要素別評価 (n8n Function Node)"]
        direction TB
        SourceEval["情報源信頼性評価<br/>sourceScore = evaluateSource(metadata)"]:::process
        DataEval["データ量・質評価<br/>dataScore = evaluateData(metadata)"]:::process
        ConsistencyEval["一貫性評価<br/>consistencyScore = evaluateConsistency(data)"]:::process
        VerifyEval["検証可能性評価<br/>verifyScore = evaluateVerifiability(data)"]:::process
    end
    
    %% 重み付け計算
    WeightedCalc["重み付け計算 (n8n Function Node)"]:::process
    
    %% 計算式
    Formula["<b>確信度スコア計算式</b><br/>confidenceScore = <br/>w_source * sourceScore + <br/>w_data * dataScore + <br/>w_consistency * consistencyScore + <br/>w_verify * verifyScore"]:::formula
    
    %% レベル判定
    LevelDetermination["確信度レベル判定<br/>(n8n If Node)"]:::process
    
    %% 出力
    ConfidenceOutput["出力: 確信度評価結果<br/>{score: 0.0-1.0, level: '高'|'中'|'低'}"]:::output
    
    %% 接続
    RawData --> Preprocess
    Preprocess --> ElementEval
    ElementEval --> WeightedCalc
    Parameters --> WeightedCalc
    WeightedCalc --> Formula
    Formula --> LevelDetermination
    Parameters --> LevelDetermination
    LevelDetermination --> ConfidenceOutput
    
    %% 注釈
    Note["<b>実装上の注意点</b><br/>・情報源の種類に応じた信頼性基準を設定<br/>・データ量と質のバランスを考慮<br/>・一貫性は時系列データの変動係数で評価<br/>・検証可能性は外部参照の有無で判定"]:::subheader
    Note -.-> ElementEval
```

## 3. 整合性評価計算フロー図 (Mermaid)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f0f0', 'primaryTextColor': '#323232', 'primaryBorderColor': '#888888', 'lineColor': '#555555', 'secondaryColor': '#e0e0e0', 'tertiaryColor': '#f9f9f9'}}}%%

flowchart TD
    classDef input fill:#DAE8FC,stroke:#6C8EBF,color:#0D5AA7,stroke-width:2px
    classDef process fill:#D5E8D4,stroke:#82B366,color:#006400,stroke-width:1px
    classDef parameter fill:#FFE6CC,stroke:#D79B00,color:#D79B00,stroke-width:1px
    classDef output fill:#F8CECC,stroke:#B85450,color:#B85450,stroke-width:1px
    classDef formula fill:#E1D5E7,stroke:#9673A6,color:#9673A6,stroke-width:1px
    classDef subheader fill:none,stroke:#555555,color:#333333,stroke-width:1px,stroke-dasharray: 5 5
    
    %% タイトルと説明
    title["<b>整合性評価計算フロー</b><br/>視点間一致度・論理的整合性・時間的整合性・コンテキスト整合性の統合評価"]
    title:::subheader
    
    %% 入力データ
    PerspectiveData["入力: 視点別評価結果<br/>(テクノロジー, マーケット, ビジネス)"]:::input
    
    %% パラメータ
    subgraph Parameters["パラメータ設定"]
        direction LR
        WeightAgreement["視点間一致度の重み<br/>w_agreement = 0.3"]:::parameter
        WeightLogical["論理的整合性の重み<br/>w_logical = 0.3"]:::parameter
        WeightTemporal["時間的整合性の重み<br/>w_temporal = 0.2"]:::parameter
        WeightContextual["コンテキスト整合性の重み<br/>w_contextual = 0.2"]:::parameter
        Thresholds["整合性レベル閾値<br/>高: ≥0.8, 中: ≥0.6, 低: <0.6"]:::parameter
    end
    
    %% データ統合
    DataIntegration["視点データ統合<br/>(共通フォーマット変換)"]:::process
    
    %% 各要素の評価
    subgraph ElementEval["要素別評価 (n8n Function Node)"]
        direction TB
        AgreementEval["視点間一致度評価<br/>agreementScore = evaluateAgreement(perspectives)"]:::process
        LogicalEval["論理的整合性評価<br/>logicalScore = evaluateLogical(perspectives)"]:::process
        TemporalEval["時間的整合性評価<br/>temporalScore = evaluateTemporal(perspectives)"]:::process
        ContextualEval["コンテキスト整合性評価<br/>contextualScore = evaluateContextual(perspectives)"]:::process
    end
    
    %% 重み付け計算
    WeightedCalc["重み付け計算 (n8n Function Node)"]:::process
    
    %% 計算式
    Formula["<b>整合性スコア計算式</b><br/>coherenceScore = <br/>w_agreement * agreementScore + <br/>w_logical * logicalScore + <br/>w_temporal * temporalScore + <br/>w_contextual * contextualScore"]:::formula
    
    %% レベル判定
    LevelDetermination["整合性レベル判定<br/>(n8n If Node)"]:::process
    
    %% 出力
    CoherenceOutput["出力: 整合性評価結果<br/>{score: 0.0-1.0, level: '高'|'中'|'低'}"]:::output
    
    %% 接続
    PerspectiveData --> DataIntegration
    DataIntegration --> ElementEval
    ElementEval --> WeightedCalc
    Parameters --> WeightedCalc
    WeightedCalc --> Formula
    Formula --> LevelDetermination
    Parameters --> LevelDetermination
    LevelDetermination --> CoherenceOutput
    
    %% 注釈
    Note["<b>実装上の注意点</b><br/>・視点間一致度はベクトル類似度で計算<br/>・論理的整合性は因果関係の矛盾検出<br/>・時間的整合性は時系列の一貫性評価<br/>・コンテキスト整合性は外部環境との整合性評価"]:::subheader
    Note -.-> ElementEval
```

## 図の説明

この資料では、コンセンサスモデルの3つの主要評価計算（重要度評価、確信度評価、整合性評価）のフロー図を示しています。各図は、入力データから評価スコア・レベルの算出までの計算プロセスを視覚的に表現しています。

### 1. 重要度評価計算フロー

重要度評価は、変化点や分析結果の重要性を4つの要素（影響範囲、変化の大きさ、戦略的関連性、時間的緊急性）から多角的に評価します。

**計算プロセス**:
1. 入力データの前処理（正規化、欠損値処理）
2. 各要素の個別評価（0.0-1.0のスコア化）
3. 重み付け係数を適用した統合計算
4. 閾値に基づく重要度レベル（高・中・低）の判定

**実装上のポイント**:
- 各要素評価は専用の評価関数で実装
- 重み係数はコンテキストに応じて調整可能
- n8nのFunctionノードで計算ロジックを実装

### 2. 確信度評価計算フロー

確信度評価は、情報やデータの信頼性を4つの要素（情報源信頼性、データ量・質、一貫性、検証可能性）から評価します。

**計算プロセス**:
1. メタデータの前処理（情報源分類、データ特性抽出）
2. 各要素の個別評価（0.0-1.0のスコア化）
3. 重み付け係数を適用した統合計算
4. 閾値に基づく確信度レベル（高・中・低）の判定

**実装上のポイント**:
- 情報源の種類に応じた信頼性基準の設定
- データ量と質のバランスを考慮した評価
- 一貫性は時系列データの変動係数で評価
- 検証可能性は外部参照の有無などで判定

### 3. 整合性評価計算フロー

整合性評価は、複数の視点（テクノロジー、マーケット、ビジネス）間の一貫性を4つの要素（視点間一致度、論理的整合性、時間的整合性、コンテキスト整合性）から評価します。

**計算プロセス**:
1. 視点別データの統合（共通フォーマット変換）
2. 各要素の個別評価（0.0-1.0のスコア化）
3. 重み付け係数を適用した統合計算
4. 閾値に基づく整合性レベル（高・中・低）の判定

**実装上のポイント**:
- 視点間一致度はベクトル類似度で計算
- 論理的整合性は因果関係の矛盾検出
- 時間的整合性は時系列の一貫性評価
- コンテキスト整合性は外部環境との整合性評価

### 共通実装要素

3つの評価計算に共通する実装要素:
- n8nのFunctionノードでJavaScriptによる計算ロジックを実装
- Ifノードで閾値に基づくレベル判定を実装
- パラメータ（重み係数、閾値）は外部から調整可能に設計
- 評価結果はJSON形式で出力し、後続処理で利用可能
