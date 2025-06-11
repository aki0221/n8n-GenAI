# 静止点検出プロセスの全体フローチャート

静止点検出プロセスは、3つの視点からの評価データを入力とし、一連の計算と評価ステップを経て最終的な静止点を特定する複雑なプロセスです。以下のフローチャートは、このプロセスの全体像を詳細に示しています。

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

## 静止点検出プロセスの主要コンポーネント

### 1. データ取得と前処理
プロセスは3つの視点（テクノロジー、マーケット、ビジネス）からの評価データ、各視点の確信度、および重要度（重み）の取得から始まります。入力データは検証され、欠損値や異常値がある場合は適切に処理されます。

### 2. 統合スコア計算
各視点の評価スコアに確信度と重要度を掛け合わせ、それらを合計して統合スコアを算出します。

```
統合スコア = Σ (視点iの評価スコア * 視点iの確信度 * 視点iの重要度)
```

同時に、3つの視点からの評価がどの程度一致しているかを示す「整合性スコア」も計算されます。

### 3. 整合性による調整
整合性スコアが閾値を下回る場合（評価がばらついている場合）、警告フラグが設定されるか、代替パラメータが使用されます。整合性スコアに基づいて統合スコアが調整され、視点間の一致度が高いほど調整後のスコアも高くなります。

### 4. 静止点候補のチェック
調整後統合スコアと各視点の評価スコアが、それぞれ設定された閾値を満たしているかチェックされます。全ての閾値をクリアした評価対象が「静止点候補」として特定されます。候補がない場合は、閾値の緩和、重み付けの再検討、または準静止点としての処理などの代替処理が実行されます。

### 5. 安定性評価
静止点候補に対して安定性評価が行われます。入力パラメータにランダムなノイズを加えたモンテカルロシミュレーションを複数回実行し、候補が安定して検出される確率（安定性スコア）を計算します。安定性スコアが閾値を超えた候補が、より信頼性の高い静止点と見なされます。

### 6. 最終的な静止点決定
安定性評価をクリアした候補の中から、調整後統合スコアや安定性スコアに基づいてランク付けし、最終的な静止点が選定されます。

### 7. 結果出力と活用
静止点情報はデータベースに記録され、ダッシュボードやレポートで可視化されます。また、関連システムに通知が送られ、意思決定プロセスに活用されます。

## n8nでの実装

このフローチャートは、n8nワークフローとして実装できます。主要なノードタイプは以下の通りです：

- **データ取得**: Google Sheets Read、Postgres、HTTP Requestなどのノード
- **計算処理**: Function（JavaScript）ノード
- **条件分岐**: If、Switchノード
- **ループ処理**: Loop（安定性評価用）ノード
- **エラーハンドリング**: Error Triggerノード
- **結果出力**: Database、Webhookノード

n8nの視覚的インターフェースを使用することで、このフローチャートを実際の実行可能なワークフローとして実装し、静止点検出プロセスを自動化することができます。
