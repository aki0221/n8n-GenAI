```mermaid
graph TD
    %% メインコンポーネント定義
    subgraph N8N["n8nオーケストレーション層"]
        NT["ワークフロートリガー"] --> ND["データ連携管理"]
        ND --> NE["エラーハンドリング"]
        NE --> NR["結果統合・配信"]
        NS["スケジュール管理"] --> NT
    end
    
    subgraph DC["データ収集コンポーネント"]
        DS["データソース接続"] --> PP["前処理と構造化"]
        DV["データ検証"] --> DS
        DC_S["データストレージ"] --> PP
    end
    
    subgraph AC["分析コンポーネント"]
        subgraph TP["テクノロジー視点"]
            TP_A["技術トレンド分析"] --> TP_D["変化点検出"]
            TP_F["特徴抽出"] --> TP_A
        end
        subgraph MP["マーケット視点"]
            MP_A["市場データ分析"] --> MP_D["変化点検出"]
            MP_F["特徴抽出"] --> MP_A
        end
        subgraph BP["ビジネス視点"]
            BP_A["ビジネスデータ分析"] --> BP_D["変化点検出"]
            BP_F["特徴抽出"] --> BP_A
        end
    end
    
    subgraph EC["評価コンポーネント"]
        subgraph TP_E["テクノロジー評価"]
            TP_IC["重要度・確信度評価"]
            TP_TH["閾値判定"]
        end
        subgraph MP_E["マーケット評価"]
            MP_IC["重要度・確信度評価"]
            MP_TH["閾値判定"]
        end
        subgraph BP_E["ビジネス評価"]
            BP_IC["重要度・確信度評価"]
            BP_TH["閾値判定"]
        end
        CC["整合性評価"]
        CR["評価結果キャッシュ"]
    end
    
    subgraph IC["統合コンポーネント"]
        PI["視点統合"] --> FP["静止点検出"]
        FP --> AS["代替解生成"]
        WA["重み付けアルゴリズム"] --> PI
        CS["コンセンサススコア計算"] --> FP
    end
    
    subgraph OC["出力コンポーネント"]
        IG["インサイト生成"] --> AR["アクション推奨"]
        AR --> VZ["可視化"]
        NT_M["通知管理"] --> IG
        API["API出力"] --> AR
    end
    
    subgraph MC["管理コンポーネント"]
        PM["パラメータ管理"] --> RM["ルール管理"]
        RM --> ME["モデル評価と最適化"]
        LG["ログ管理"] --> PM
        ER["エラー復旧"] --> ME
        PF["パフォーマンスモニタリング"] --> ME
    end
    
    %% コンポーネント間の連携フロー（データフロー）
    PP ==> TP_F
    PP ==> MP_F
    PP ==> BP_F
    
    TP_D ==> TP_IC
    MP_D ==> MP_IC
    BP_D ==> BP_IC
    
    TP_IC ==> TP_TH
    MP_IC ==> MP_TH
    BP_IC ==> BP_TH
    
    TP_TH ==> CC
    MP_TH ==> CC
    BP_TH ==> CC
    
    CC ==> CR
    CR ==> PI
    
    AS ==> IG
    
    %% n8nオーケストレーション層との連携
    ND ==> DS
    ND ==> TP_A
    ND ==> MP_A
    ND ==> BP_A
    ND ==> CC
    ND ==> PI
    ND ==> IG
    
    NE ==> ER
    NR ==> VZ
    NR ==> API
    NR ==> NT_M
    
    %% 管理コンポーネントからの制御フロー
    PM -.-> DS
    PM -.-> TP_A
    PM -.-> MP_A
    PM -.-> BP_A
    PM -.-> TP_IC
    PM -.-> MP_IC
    PM -.-> BP_IC
    PM -.-> WA
    PM -.-> IG
    
    ME -.-> CC
    ME -.-> FP
    ME -.-> VZ
    ME -.-> CS
    
    LG -.-> DS
    LG -.-> CC
    LG -.-> AS
    LG -.-> VZ
    
    %% スタイル設定
    classDef n8n fill:#f9f9f9,stroke:#666666,stroke-width:2px,rx:10px,ry:10px
    classDef component fill:#e6f2ff,stroke:#3385ff,stroke-width:2px,rx:10px,ry:10px
    classDef perspective fill:#f2ffe6,stroke:#85ff33,stroke-width:2px,rx:5px,ry:5px
    classDef management fill:#ffe6cc,stroke:#ff9933,stroke-width:2px,rx:10px,ry:10px
    classDef submodule fill:#f9f9f9,stroke:#999999,stroke-width:1px
    
    class N8N n8n
    class DC,AC,EC,IC,OC component
    class TP,MP,BP,TP_E,MP_E,BP_E perspective
    class MC management
    class NT,ND,NE,NR,NS,DS,PP,DV,DC_S,TP_F,MP_F,BP_F,TP_TH,MP_TH,BP_TH,CR,WA,CS,NT_M,API,LG,ER,PF submodule
    
    %% 凡例
    subgraph Legend["凡例"]
        L1["n8nオーケストレーション層"]
        L2["処理コンポーネント"]
        L3["視点サブグループ"]
        L4["管理コンポーネント"]
        L5["サブモジュール"]
        L6["データフロー"] ==> L7[""]
        L8["制御フロー"] -.-> L9[""]
    end
    
    class L1 n8n
    class L2 component
    class L3 perspective
    class L4 management
    class L5 submodule
```

**図1: コンセンサスモデルの全体アーキテクチャ**

この図は、n8nによるオーケストレーション層を含むコンセンサスモデルの全体アーキテクチャを示しています。主要なコンポーネント（データ収集、分析、評価、統合、出力、管理）とそれらの相互関係、データフローと制御フローを視覚的に表現しています。

特に、3つの視点（テクノロジー、マーケット、ビジネス）がどのように分析され、評価され、最終的に統合されるかを示しています。また、n8nオーケストレーション層がどのようにこれらのコンポーネントを連携させ、全体のワークフローを管理するかも表現しています。

実線はデータフローを、点線は制御フローを表しています。色分けにより、n8n層、処理コンポーネント、視点サブグループ、管理コンポーネント、サブモジュールを区別しています。
