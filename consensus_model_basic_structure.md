# コンセンサスモデルの基本構造概念図

## 基本構造概念図 (Mermaid)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f0f0', 'primaryTextColor': '#323232', 'primaryBorderColor': '#888888', 'lineColor': '#555555', 'secondaryColor': '#e0e0e0', 'tertiaryColor': '#f9f9f9'}}}%%

flowchart TB
    classDef inputLayer fill:#D4F1F9,stroke:#05445E,color:#05445E,stroke-width:2px
    classDef evaluationLayer fill:#FFE6CC,stroke:#D79B00,color:#D79B00,stroke-width:2px
    classDef integrationLayer fill:#D5E8D4,stroke:#82B366,color:#82B366,stroke-width:2px
    classDef outputLayer fill:#E1D5E7,stroke:#9673A6,color:#9673A6,stroke-width:2px
    classDef perspective fill:#F5F5F5,stroke:#666666,color:#333333,stroke-width:1px
    classDef dataFlow fill:none,stroke:#555555,color:#333333,stroke-width:1px
    
    %% タイトルと説明
    title["<b>コンセンサスモデル基本構造</b><br/>多視点データ統合と意思決定支援エンジン"]
    title:::dataFlow
    
    %% 入力レイヤー
    subgraph InputLayer["入力レイヤー (Input Layer)"]
        direction LR
        Tech["テクノロジー視点<br/>技術トレンド・成熟度・特許"]
        Market["マーケット視点<br/>市場動向・競合・顧客ニーズ"]
        Business["ビジネス視点<br/>収益性・戦略適合性・リソース"]
    end
    InputLayer:::inputLayer
    
    %% 評価レイヤー
    subgraph EvalLayer["評価レイヤー (Evaluation Layer)"]
        direction LR
        Importance["重要度評価<br/>影響範囲・変化の大きさ"]
        Confidence["確信度評価<br/>情報源信頼性・データ量"]
        Coherence["整合性評価<br/>視点間一致度・論理整合性"]
    end
    EvalLayer:::evaluationLayer
    
    %% 統合レイヤー
    subgraph IntegLayer["統合レイヤー (Integration Layer)"]
        direction LR
        Integration["視点統合<br/>重み付け・優先順位付け"]
        Equilibrium["静止点検出<br/>最適解・安定性分析"]
        Alternative["代替解生成<br/>シナリオ分析"]
    end
    IntegLayer:::integrationLayer
    
    %% 出力レイヤー
    subgraph OutputLayer["出力レイヤー (Output Layer)"]
        direction LR
        Insight["インサイト生成<br/>解釈・意味付け"]
        Action["アクション推奨<br/>戦略オプション"]
        Visual["可視化<br/>ダッシュボード・レポート"]
    end
    OutputLayer:::outputLayer
    
    %% レイヤー間の接続
    InputLayer --> EvalLayer
    EvalLayer --> IntegLayer
    IntegLayer --> OutputLayer
    
    %% 視点間の相互作用（入力レイヤー内）
    Tech <--> Market
    Market <--> Business
    Tech <--> Business
    
    %% フィードバックループ
    OutputLayer -.-> InputLayer
    
    %% 外部連携
    OutputLayer --> External["外部システム<br/>意思決定支援・通知"]
    External:::dataFlow
```

## 図の説明

この概念図は、コンセンサスモデルの基本構造を視覚的に表現したものです。モデルは4つの主要レイヤーで構成されています：

1. **入力レイヤー（青色）**: テクノロジー、マーケット、ビジネスの3つの視点からのデータを収集・処理します。各視点は相互に影響し合い、情報を交換します。

2. **評価レイヤー（オレンジ色）**: 収集したデータの重要度、確信度、整合性を評価します。これにより、情報の価値と信頼性を定量化します。

3. **統合レイヤー（緑色）**: 評価された情報を統合し、最適な解釈（静止点）を検出します。また、代替的な解釈も生成します。

4. **出力レイヤー（紫色）**: 分析結果をインサイト、アクション推奨、可視化の形で提供します。

図中の実線矢印はデータの主な流れを、点線矢印はフィードバックループを表しています。各レイヤー内のコンポーネントは、それぞれ特定の機能を担当し、全体として一貫した分析・意思決定支援プロセスを形成しています。

この構造により、コンセンサスモデルは複数の視点からの情報を効果的に統合し、より包括的で信頼性の高い意思決定支援を実現します。
