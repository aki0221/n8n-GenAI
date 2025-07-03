# 第17章 数学的記法統一ルール

## 統一記法の基本原則

### 1. 変数命名規則
- **認知能力関連**: `cognitive_*` (例: cognitive_profile, cognitive_load)
- **適応係数**: `α_*` (例: α_age, α_experience)
- **補正係数**: `β_*` (例: β_exp, β_domain)
- **最適化係数**: `γ_*` (例: γ_expertise, γ_complexity)
- **ノイズ係数**: `δ_*` (例: δ_noise, δ_stress)

### 2. 関数記法統一
- **計算関数**: `calculate_*()` (例: calculate_age_factor())
- **評価関数**: `assess_*()` (例: assess_cognitive_load())
- **最適化関数**: `optimize_*()` (例: optimize_complexity())
- **選択関数**: `select_*()` (例: select_modality())

### 3. 数式表現の統一
- **範囲表記**: [min, max] 形式
- **確率・係数**: 0.0-1.0 正規化
- **年齢**: 整数値（歳）
- **経験**: 年数または正規化値

### 4. 実装可能性の確保
- 複雑な行列演算 → 単純な関数計算
- 6次元ベクトル → 3次元プロファイル
- 抽象的数式 → 具体的計算式

## 統一後の標準数式

### 年齢適応係数
```
α_age(age) = max(0.3, 1.0 - 0.003 × max(0, age - 25) + 0.15 × min(age/50, 1.0))
```

### 経験補正係数
```
β_exp(experience, relevance) = 0.15 × min(experience/10, 1.0) × relevance
```

### 専門性係数
```
γ_expertise(domain_exp, complexity) = 1.0 + 0.2 × tanh(domain_exp/5) × (1 - complexity)
```

### 統合効率関数
```
E_integration = α_age × (1 + β_exp) × (1 + γ_expertise) × (1 - complexity_penalty)
```

## 実装対応表

| 理論概念 | 数学的表現 | 実装関数 |
|---------|-----------|---------|
| 認知能力変化 | α_age(age) | calculate_age_factor() |
| 経験補正 | β_exp(exp) | calculate_experience_bonus() |
| 専門性適応 | γ_expertise | calculate_expertise_factor() |
| 統合最適化 | E_integration | calculate_integration_efficiency() |

この統一ルールにより、第17章全体の数学的記法が一貫性を持ち、実装可能性が確保されます。

