# 7つの論文における数学的用語の体系的洗い出し

## 第2段階：論文ごとの数学的用語抽出

### 論文1：Multi-perspective Strategic Decision Making (Wainfan, 2010)

#### 1.1 線形代数・ベクトル解析

**ベクトル空間論**
- Vector: ベクトル
- Vector space: ベクトル空間
- Multidimensional vector: 多次元ベクトル
- Vector norm: ベクトルノルム
- Inner product: 内積
- Orthogonality: 直交性
- Linear independence: 線形独立
- Basis vector: 基底ベクトル
- Dimension: 次元

**行列理論**
- Matrix: 行列
- Transformation matrix: 変換行列
- Eigenvalue: 固有値
- Eigenvector: 固有ベクトル
- Matrix decomposition: 行列分解
- Singular value decomposition: 特異値分解
- Rank: 階数
- Determinant: 行列式
- Inverse matrix: 逆行列

#### 1.2 最適化理論

**数理最適化**
- Optimization: 最適化
- Objective function: 目的関数
- Constraint: 制約
- Feasible region: 実行可能領域
- Global optimum: 大域最適解
- Local optimum: 局所最適解
- Pareto optimality: パレート最適性
- Multi-objective optimization: 多目的最適化
- Linear programming: 線形計画法
- Nonlinear programming: 非線形計画法

**制約最適化**
- Lagrange multiplier: ラグランジュ乗数
- KKT conditions: KKT条件
- Penalty method: ペナルティ法
- Barrier method: バリア法
- Augmented Lagrangian: 拡張ラグランジアン

#### 1.3 意思決定理論の数学

**効用理論**
- Utility function: 効用関数
- Expected utility: 期待効用
- Von Neumann-Morgenstern utility: フォン・ノイマン-モルゲンシュテルン効用
- Risk aversion: リスク回避
- Certainty equivalent: 確実性等価

**ゲーム理論**
- Game theory: ゲーム理論
- Nash equilibrium: ナッシュ均衡
- Dominant strategy: 支配戦略
- Zero-sum game: ゼロサムゲーム
- Cooperative game: 協力ゲーム
- Coalition: 提携
- Shapley value: シャプレー値

#### 1.4 確率・統計理論

**確率論**
- Probability: 確率
- Random variable: 確率変数
- Probability distribution: 確率分布
- Conditional probability: 条件付き確率
- Bayes' theorem: ベイズの定理
- Independence: 独立性
- Correlation: 相関

**統計的推論**
- Statistical inference: 統計的推論
- Hypothesis testing: 仮説検定
- Confidence interval: 信頼区間
- Significance level: 有意水準
- p-value: p値
- Type I error: 第1種の誤り
- Type II error: 第2種の誤り

### 論文2：Confidence consensus-based model (Xu et al., 2019)

#### 2.1 ファジィ理論

**ファジィ集合論**
- Fuzzy set: ファジィ集合
- Membership function: 所属関数
- Fuzzy number: ファジィ数
- Triangular fuzzy number: 三角ファジィ数
- Trapezoidal fuzzy number: 台形ファジィ数
- α-cut: α-カット
- Support: 台
- Core: コア

**ファジィ演算**
- Fuzzy arithmetic: ファジィ演算
- Fuzzy addition: ファジィ加法
- Fuzzy multiplication: ファジィ乗法
- Fuzzy aggregation: ファジィ集約
- Weighted average: 重み付き平均
- OWA operator: OWA演算子

#### 2.2 コンセンサス測定

**距離測度**
- Distance measure: 距離測度
- Euclidean distance: ユークリッド距離
- Manhattan distance: マンハッタン距離
- Hamming distance: ハミング距離
- Cosine similarity: コサイン類似度
- Jaccard coefficient: ジャッカード係数

**合意度指標**
- Consensus degree: 合意度
- Consensus index: 合意指標
- Proximity measure: 近接度測度
- Similarity measure: 類似度測度
- Consistency ratio: 一貫性比
- Agreement level: 合意レベル

#### 2.3 信頼度理論

**信頼度計算**
- Confidence level: 信頼度レベル
- Confidence interval: 信頼区間
- Reliability: 信頼性
- Credibility: 信用度
- Trust degree: 信頼度
- Uncertainty measure: 不確実性測度

**重み計算**
- Weight calculation: 重み計算
- Normalized weight: 正規化重み
- Relative importance: 相対重要度
- Priority vector: 優先度ベクトル
- Consistency check: 一貫性チェック

#### 2.4 集約理論

**集約演算子**
- Aggregation operator: 集約演算子
- Weighted aggregation: 重み付き集約
- Ordered weighted averaging: 順序重み付き平均
- Choquet integral: ショケ積分
- Sugeno integral: 菅野積分

**数式表現**
```
信頼度ベースコンセンサス測度:
CC(x) = 1 - (1/n) Σᵢ₌₁ⁿ |xᵢ - x̄| × wᵢ

重み正規化:
wᵢ = cᵢ / Σⱼ₌₁ⁿ cⱼ

調整コスト最小化:
min Σᵢ₌₁ⁿ λᵢ(xᵢ^new - xᵢ^old)²
```

### 論文3：Value-based decision-making model (Hall & Davis, 2007)

#### 3.1 多基準意思決定

**MCDM理論**
- Multi-criteria decision making: 多基準意思決定
- Analytic hierarchy process: 階層分析法
- TOPSIS: TOPSIS法
- ELECTRE: ELECTRE法
- PROMETHEE: PROMETHEE法
- Weighted sum model: 重み付き和モデル

**価値関数**
- Value function: 価値関数
- Additive value function: 加法的価値関数
- Multiplicative value function: 乗法的価値関数
- Utility function: 効用関数
- Preference function: 選好関数

#### 3.2 Sprangerの価値測定

**価値次元計算**
- Value dimension: 価値次元
- Theoretical value score: 理論的価値スコア
- Economic value score: 経済的価値スコア
- Aesthetic value score: 美的価値スコア
- Social value score: 社会的価値スコア
- Political value score: 政治的価値スコア
- Religious value score: 宗教的価値スコア

**価値統合計算**
- Value integration: 価値統合
- Weighted value sum: 重み付き価値和
- Value conflict index: 価値対立指数
- Value harmony measure: 価値調和測度
- Composite value score: 複合価値スコア

#### 3.3 統計分析

**記述統計**
- Mean: 平均
- Standard deviation: 標準偏差
- Variance: 分散
- Median: 中央値
- Mode: 最頻値
- Range: 範囲
- Quartile: 四分位数

**推測統計**
- t-test: t検定
- ANOVA: 分散分析
- Chi-square test: カイ二乗検定
- Correlation analysis: 相関分析
- Regression analysis: 回帰分析

### 論文4：Value-Based Decision-Making and Cognition (Richtmann et al., 2024)

#### 4.1 認知モデリング

**認知アーキテクチャ**
- Cognitive model: 認知モデル
- Information processing model: 情報処理モデル
- Dual-process model: 二重過程モデル
- Working memory capacity: ワーキングメモリ容量
- Processing speed: 処理速度
- Cognitive load: 認知負荷

**計算認知科学**
- Computational cognitive science: 計算認知科学
- Bayesian brain: ベイズ脳
- Neural network: ニューラルネットワーク
- Connectionist model: コネクショニストモデル
- Symbolic computation: 記号計算

#### 4.2 実験統計

**実験設計**
- Experimental design: 実験設計
- Randomized controlled trial: ランダム化比較試験
- Between-subjects design: 被験者間計画
- Within-subjects design: 被験者内計画
- Factorial design: 要因計画
- Counterbalancing: カウンターバランス

**統計的検定**
- Statistical test: 統計的検定
- Effect size: 効果量
- Cohen's d: コーエンのd
- Eta squared: イータ二乗
- Power analysis: 検定力分析
- Multiple comparison: 多重比較

#### 4.3 年齢効果の数学的モデリング

**発達曲線**
- Growth curve: 成長曲線
- Developmental trajectory: 発達軌跡
- Linear model: 線形モデル
- Quadratic model: 二次モデル
- Exponential decay: 指数減衰
- Logistic function: ロジスティック関数

**数式表現**
```
年齢効果モデル:
Y = β₀ + β₁(Age) + β₂(Age²) + ε

認知処理速度:
RT = a + b × exp(-c × Age)

価値重み付け:
w(age) = w₀ × (1 + α × age)^(-β)
```

### 論文5：Human-AI coordination (Zhang et al., 2025)

#### 5.1 協調最適化

**多エージェント最適化**
- Multi-agent optimization: 多エージェント最適化
- Distributed optimization: 分散最適化
- Consensus optimization: コンセンサス最適化
- Cooperative optimization: 協力最適化
- Nash optimization: ナッシュ最適化

**協調アルゴリズム**
- Coordination algorithm: 協調アルゴリズム
- Consensus algorithm: コンセンサスアルゴリズム
- Distributed consensus: 分散コンセンサス
- Synchronization: 同期化
- Convergence: 収束

#### 5.2 機械学習理論

**学習アルゴリズム**
- Machine learning: 機械学習
- Supervised learning: 教師あり学習
- Unsupervised learning: 教師なし学習
- Reinforcement learning: 強化学習
- Deep learning: 深層学習
- Transfer learning: 転移学習

**最適化手法**
- Gradient descent: 勾配降下法
- Stochastic gradient descent: 確率的勾配降下法
- Adam optimizer: Adam最適化
- Backpropagation: 誤差逆伝播法
- Cross-validation: 交差検証

#### 5.3 情報理論

**情報測度**
- Information theory: 情報理論
- Entropy: エントロピー
- Mutual information: 相互情報量
- Kullback-Leibler divergence: KLダイバージェンス
- Cross-entropy: 交差エントロピー
- Information gain: 情報利得

**数式表現**
```
協調効率性:
CE = (P_human + P_AI - P_overlap) / (P_human + P_AI)

情報統合:
I_integrated = α × I_human + β × I_AI + γ × I_interaction

学習収束:
θ(t+1) = θ(t) - η∇L(θ(t))
```

### 論文6：AI and Strategic Decision-Making (Csaszar et al., 2024)

#### 6.1 統計的実証分析

**実証研究設計**
- Empirical research design: 実証研究設計
- Randomized experiment: ランダム化実験
- Treatment effect: 処置効果
- Control group: 統制群
- Treatment group: 処置群
- Causal inference: 因果推論

**統計的検定**
- Independent t-test: 独立標本t検定
- Paired t-test: 対応標本t検定
- Mann-Whitney U test: マン・ホイットニーのU検定
- Wilcoxon signed-rank test: ウィルコクソン符号順位検定
- Effect size calculation: 効果量計算

#### 6.2 性能評価指標

**評価メトリクス**
- Performance metric: 性能指標
- Accuracy: 精度
- Precision: 適合率
- Recall: 再現率
- F1-score: F1スコア
- ROC curve: ROC曲線
- AUC: AUC値

**相関分析**
- Correlation coefficient: 相関係数
- Pearson correlation: ピアソン相関
- Spearman correlation: スピアマン相関
- Kendall's tau: ケンドールのタウ
- Partial correlation: 偏相関

#### 6.3 実験統計

**重要な数値結果**
```
ビジネスプラン評価比較:
- 起業家平均スコア: 5.12 ± 0.89
- LLM平均スコア: 5.08 ± 0.76
- 統計的差異: p = 0.691 (n.s.)
- 効果量: Cohen's d = 0.05

投資判断相関:
- 人間-AI相関: r = 0.734, p < 0.001
- 一致率: 73.4%
- 信頼区間: 95% CI [0.689, 0.774]

実験規模:
- 参加者数: n = 127 (起業家)
- 評価者数: n = 38 (投資家)
- 評価対象: 342件のビジネスプラン
```

### 論文7：Granular computing consensus model (Wang et al., 2025)

#### 7.1 粒度計算理論

**情報粒子**
- Information granule: 情報粒子
- Granular structure: 粒度構造
- Granularity level: 粒度レベル
- Granular hierarchy: 粒度階層
- Granular decomposition: 粒度分解

**粒度測度**
- Coverage: カバレッジ
- Specificity: 特異性
- Granular quality: 粒度品質
- Justifiable granularity: 正当化可能粒度
- Granular optimization: 粒度最適化

#### 7.2 クラスタリング理論

**クラスタリングアルゴリズム**
- Clustering algorithm: クラスタリングアルゴリズム
- Hierarchical clustering: 階層クラスタリング
- K-means clustering: K-means法
- Fuzzy clustering: ファジィクラスタリング
- Density-based clustering: 密度ベースクラスタリング

**クラスタ評価**
- Cluster validity: クラスタ妥当性
- Silhouette coefficient: シルエット係数
- Davies-Bouldin index: デイビス・ボールディン指標
- Calinski-Harabasz index: カリンスキー・ハラバス指標
- Dunn index: ダン指標

#### 7.3 コンセンサス数学

**コンセンサス測度**
- Consensus measure: コンセンサス測度
- Agreement index: 合意指標
- Harmony degree: 調和度
- Consistency level: 一貫性レベル
- Convergence rate: 収束率

**最適化問題**
- Consensus optimization: コンセンサス最適化
- Cost minimization: コスト最小化
- Multi-objective optimization: 多目的最適化
- Constraint satisfaction: 制約充足
- Pareto frontier: パレートフロンティア

#### 7.4 重要な数式群

**粒度品質指標**
```
Q(G) = Cov(G) × Sp(G)
Cov(G) = |G| / n
Sp(G) = 1 / (1 + σ²(G))
```

**分割指数**
```
DI(k) = α × LCI(k) + β × GCI(k) + γ × Comp(k)
LCI(k) = (1/k) Σᵢ₌₁ᵏ (1/|Cᵢ|) Σⱼ,ₗ∈Cᵢ S(pⱼ, pₗ)
GCI(k) = (1/k) Σᵢ₌₁ᵏ S(p̄ᵢ, p̄)
```

**2段階最適化**
```
段階1: max Σᵢ₌₁ⁿ CD(Gᵢ)
段階2: min Σᵢ₌₁ⁿ cᵢ × ||pᵢ^new - pᵢ^old||²
制約: CD(G) ≥ θ, ||pᵢ^new - pᵢ^old|| ≤ δᵢ
```

**区間ファジィ数演算**
```
優先度: Pr(p₁, p₂) = min{I(p₁) + I(p₂), max{p₂⁺ - p₁⁻, 0}} / (I(p₁) + I(p₂))
類似度: S(p₁, p₂) = 1 - (|p₁⁻ - p₂⁻| + |p₁⁺ - p₂⁺|) / (p₁⁺ + p₁⁻ + p₂⁺ + p₂⁻)
```

この第2段階では、7つの論文から数学的用語を体系的に抽出しました。各論文で使用されている数学的概念、数式、統計手法、計算アルゴリズムを詳細に整理し、具体的な数値結果も含めて包括的に記録しています。

