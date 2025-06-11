```mermaid
graph TB
    %% 静止点検出プロセスの全体フローチャート
    %% 色分け: 青=データ取得・前処理, 緑=計算処理, 黄=条件分岐, オレンジ=検証・評価, 紫=結果出力, 赤=エラー・代替処理

    %% スタイル定義
    classDef data fill:#d0e0ff,stroke:#3050b0,stroke-width:2px
    classDef process fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef decision fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef validation fill:#ffccbc,stroke:#e64a19,stroke-width:2px
    classDef output fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    classDef error fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    classDef subgraph fill:#f5f5f5,stroke:#616161,stroke-width:1px

    %% 開始点
    Start([静止点検出プロセス開始]) --> DataValidation{データ検証}
    class Start data

    %% データ検証と前処理
    DataValidation -->|OK| GetPerspectiveData
    DataValidation -->|NG| HandleDataError
    class DataValidation decision
    
    HandleDataError[データエラー処理<br>欠損値補完/デフォルト値設定] --> GetPerspectiveData
    class HandleDataError error

    %% データ取得
    subgraph DataAcquisition [データ取得・前処理]
        GetPerspectiveData[3視点の評価データ取得<br>テクノロジー/マーケット/ビジネス] --> GetConfidenceData
        GetConfidenceData[各視点の確信度取得] --> GetWeightData
        GetWeightData[各視点の重要度(重み)取得] --> PreprocessData
        PreprocessData[データ正規化・前処理] 
    end
    class GetPerspectiveData,GetConfidenceData,GetWeightData,PreprocessData data

    %% 統合スコア計算
    PreprocessData --> CalculateIntegratedScore
    
    subgraph ScoreCalculation [統合スコア計算]
        CalculateIntegratedScore[統合スコア計算<br>Σ(評価×確信度×重要度)] --> CalculateCoherenceScore
        CalculateCoherenceScore[整合性スコア計算<br>視点間の一致度評価]
    end
    class CalculateIntegratedScore,CalculateCoherenceScore process

    %% 整合性チェックと調整
    CalculateCoherenceScore --> CoherenceCheck{整合性チェック}
    CoherenceCheck -->|閾値以上| AdjustScore
    CoherenceCheck -->|閾値未満| HandleLowCoherence
    class CoherenceCheck decision
    
    HandleLowCoherence[低整合性処理<br>警告フラグ設定/代替パラメータ] --> AdjustScore
    class HandleLowCoherence error
    
    AdjustScore[整合性に基づくスコア調整<br>調整後統合スコア計算] --> CandidateCheck
    class AdjustScore process

    %% 静止点候補チェック
    CandidateCheck{静止点候補チェック}
    CandidateCheck -->|全閾値クリア| StabilityEvaluation
    CandidateCheck -->|閾値未達| HandleNoCandidates
    class CandidateCheck decision
    
    HandleNoCandidates{代替処理選択}
    HandleNoCandidates -->|閾値緩和| RelaxThresholds
    HandleNoCandidates -->|重み再検討| ReconsiderWeights
    HandleNoCandidates -->|準静止点提示| PresentQuasiPoints
    class HandleNoCandidates decision
    
    RelaxThresholds[閾値の段階的緩和] --> CandidateCheck
    ReconsiderWeights[重み付けの再検討] --> CalculateIntegratedScore
    PresentQuasiPoints[準静止点として処理] --> OutputResults
    class RelaxThresholds,ReconsiderWeights,PresentQuasiPoints error

    %% 安定性評価
    subgraph StabilityAssessment [安定性評価]
        StabilityEvaluation[安定性評価準備<br>パラメータ設定] --> MonteCarloSimulation
        MonteCarloSimulation[モンテカルロシミュレーション<br>ノイズ付加と再評価] --> CalculateStabilityScore
        CalculateStabilityScore[安定性スコア計算<br>安定検出率の算出]
    end
    class StabilityEvaluation,MonteCarloSimulation,CalculateStabilityScore validation

    %% 安定性チェック
    CalculateStabilityScore --> StabilityCheck{安定性チェック}
    StabilityCheck -->|閾値以上| RankCandidates
    StabilityCheck -->|閾値未満| HandleLowStability
    class StabilityCheck decision
    
    HandleLowStability[低安定性処理<br>パラメータ調整/再評価] --> StabilityEvaluation
    class HandleLowStability error

    %% 最終的な静止点決定
    RankCandidates[候補のランク付け<br>スコア・安定性による順位付け] --> SelectFinalPoint
    SelectFinalPoint[最終的な静止点選定] --> RecordResults
    class RankCandidates,SelectFinalPoint process

    %% 結果出力と活用
    subgraph ResultsOutput [結果出力と活用]
        RecordResults[静止点情報の記録<br>データベース保存] --> VisualizeResults
        VisualizeResults[結果の可視化<br>ダッシュボード/レポート] --> NotifySystem
        NotifySystem[関連システムへの通知]
    end
    class RecordResults,VisualizeResults,NotifySystem output

    %% 終了点
    NotifySystem --> OutputResults
    OutputResults([静止点検出プロセス完了])
    class OutputResults output

    %% n8n実装注釈
    subgraph n8nImplementation [n8n実装ノード]
        n1[データ取得: Google Sheets/Postgres/HTTP]
        n2[計算処理: Function(JavaScript)]
        n3[条件分岐: If/Switch]
        n4[ループ処理: Loop(安定性評価)]
        n5[エラー処理: Error Trigger]
        n6[結果出力: Database/Webhook]
    end
```
