# 改良版RichtmannCognitiveProcessorの実装
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class CognitiveProfile:
    """認知プロファイル - Richtmann et al. (2024) 理論に基づく改良版"""
    age: int
    experience_years: float
    domain_expertise: float  # 0.0-1.0
    stress_level: float      # 0.0-1.0
    attention_span: float    # 0.0-1.0
    processing_speed: float  # 0.0-1.0

@dataclass
class IntegrationResult:
    """統合結果"""
    integration_score: float
    recommended_complexity: str
    optimal_modality: str
    cognitive_load: float
    confidence: float
    recommendations: List[str]

class ImprovedRichtmannProcessor:
    """
    改良版Richtmann認知プロセッサ
    実装実現性と理論的妥当性を両立
    """
    
    def __init__(self):
        # Richtmann et al. (2024) 実証パラメータ
        self.age_params = {
            'decline_start': 25,
            'decline_rate': 0.003,
            'experience_bonus': 0.15,
            'min_capacity': 0.3
        }
        
        # 複雑性閾値
        self.complexity_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
        
        # モダリティ選択パラメータ
        self.modality_params = {
            'visual_age_threshold': 45,
            'text_complexity_limit': 0.7,
            'mixed_threshold': 0.6
        }
    
    def calculate_age_factor(self, age: int, expertise: float = 0.5) -> float:
        """年齢適応係数の計算（Richtmann理論実装）"""
        # 基本的な年齢による認知能力低下
        decline = self.age_params['decline_rate'] * max(0, age - self.age_params['decline_start'])
        
        # 経験による補正（年齢と専門性の相互作用）
        experience_compensation = self.age_params['experience_bonus'] * min(age/50, 1.0) * expertise
        
        # 最小能力保証付きの適応係数
        return max(self.age_params['min_capacity'], 1.0 - decline + experience_compensation)
    
    def calculate_experience_factor(self, experience_years: float, domain_relevance: float = 0.8) -> float:
        """経験補正係数の計算"""
        # 経験年数の正規化（10年で最大効果）
        normalized_exp = min(experience_years / 10.0, 1.0)
        
        # ドメイン関連性による重み付け
        return 1.0 + (self.age_params['experience_bonus'] * normalized_exp * domain_relevance)
    
    def calculate_expertise_factor(self, domain_expertise: float, task_complexity: float) -> float:
        """専門性適応係数の計算"""
        # 専門性と課題複雑性の相互作用
        expertise_boost = 0.2 * np.tanh(domain_expertise * 5)
        complexity_adjustment = 1.0 - (task_complexity * 0.3)
        
        return 1.0 + (expertise_boost * complexity_adjustment)
    
    def assess_cognitive_load(self, content_complexity: float, profile: CognitiveProfile) -> float:
        """認知負荷の評価"""
        # 内在的負荷（コンテンツ固有）
        intrinsic_load = content_complexity * (1.0 - profile.domain_expertise)
        
        # 外在的負荷（個人要因）
        age_factor = self.calculate_age_factor(profile.age, profile.domain_expertise)
        processing_mismatch = abs(content_complexity - profile.processing_speed)
        stress_amplification = profile.stress_level * 0.5
        
        extraneous_load = (processing_mismatch + stress_amplification) * (2.0 - age_factor)
        
        # 有効負荷（学習促進）
        germane_load = content_complexity * profile.attention_span * age_factor
        
        # 重み付け統合
        total_load = 0.4 * intrinsic_load + 0.3 * extraneous_load + 0.3 * germane_load
        return min(total_load, 1.0)
    
    def select_optimal_complexity(self, profile: CognitiveProfile) -> str:
        """最適複雑性レベルの選択"""
        # 総合認知能力の評価
        age_factor = self.calculate_age_factor(profile.age, profile.domain_expertise)
        experience_factor = self.calculate_experience_factor(profile.experience_years)
        
        cognitive_capacity = (
            age_factor * 0.4 +
            profile.processing_speed * 0.3 +
            profile.attention_span * 0.2 +
            profile.domain_expertise * 0.1
        ) * (1.0 - profile.stress_level * 0.3)
        
        # 複雑性レベルの決定
        if cognitive_capacity > self.complexity_thresholds['high']:
            return 'high'
        elif cognitive_capacity > self.complexity_thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def select_optimal_modality(self, profile: CognitiveProfile) -> str:
        """最適出力モダリティの選択"""
        # 年齢による視覚処理能力の考慮
        if profile.age > self.modality_params['visual_age_threshold']:
            if profile.processing_speed > 0.6:
                return 'mixed'  # 聴覚+視覚
            else:
                return 'auditory'  # 聴覚中心
        
        # 専門性と注意力による判断
        if profile.domain_expertise > 0.7:
            return 'visual'  # 高専門性：詳細視覚情報
        elif profile.attention_span < 0.5:
            return 'mixed'   # 注意力低下：マルチモーダル
        else:
            return 'text'    # 標準：テキストベース
    
    def generate_recommendations(self, profile: CognitiveProfile, cognitive_load: float) -> List[str]:
        """処理改善推奨事項の生成"""
        recommendations = []
        
        # 年齢に基づく推奨
        if profile.age > 50:
            recommendations.extend([
                "フォントサイズを14pt以上に設定",
                "情報提示速度を20%減速"
            ])
        
        # 認知負荷に基づく推奨
        if cognitive_load > 0.7:
            recommendations.extend([
                "情報を段階的に提示",
                "不要な視覚要素を除去"
            ])
        
        # ストレスレベルに基づく推奨
        if profile.stress_level > 0.6:
            recommendations.extend([
                "進捗表示を追加",
                "適切な休憩時間を設定"
            ])
        
        # 専門性に基づく推奨
        if profile.domain_expertise < 0.3:
            recommendations.extend([
                "専門用語の解説を追加",
                "具体例を多用"
            ])
        
        return recommendations
    
    def process_integration(self, tech_score: float, market_score: float, 
                          business_score: float, profile: CognitiveProfile) -> IntegrationResult:
        """3視点統合処理の実行"""
        # 認知適応係数の計算
        age_factor = self.calculate_age_factor(profile.age, profile.domain_expertise)
        experience_factor = self.calculate_experience_factor(profile.experience_years)
        expertise_factor = self.calculate_expertise_factor(profile.domain_expertise, 0.6)
        
        # 統合重み付けの動的調整
        base_weights = [0.33, 0.33, 0.34]  # Tech, Market, Business
        
        # 専門性による重み調整
        if profile.domain_expertise > 0.7:
            base_weights[0] *= 1.2  # 技術重視
        
        # 経験による重み調整
        if profile.experience_years > 10:
            base_weights[2] *= 1.1  # ビジネス重視
        
        # 重みの正規化
        total_weight = sum(base_weights)
        weights = [w/total_weight for w in base_weights]
        
        # 統合スコアの計算
        raw_integration = sum(score * weight for score, weight in 
                             zip([tech_score, market_score, business_score], weights))
        
        # 認知適応による最終調整
        integration_score = raw_integration * age_factor * experience_factor * expertise_factor
        
        # 認知負荷の評価
        cognitive_load = self.assess_cognitive_load(integration_score, profile)
        
        # 最適化推奨の生成
        recommended_complexity = self.select_optimal_complexity(profile)
        optimal_modality = self.select_optimal_modality(profile)
        recommendations = self.generate_recommendations(profile, cognitive_load)
        
        # 信頼度の計算
        confidence = min(0.95, 
                        0.7 + 0.2 * profile.domain_expertise + 
                        0.1 * (1.0 - profile.stress_level))
        
        return IntegrationResult(
            integration_score=integration_score,
            recommended_complexity=recommended_complexity,
            optimal_modality=optimal_modality,
            cognitive_load=cognitive_load,
            confidence=confidence,
            recommendations=recommendations
        )

# テスト実行
def test_improved_processor():
    """改良版プロセッサのテスト"""
    processor = ImprovedRichtmannProcessor()
    
    # テストプロファイル
    test_profile = CognitiveProfile(
        age=45,
        experience_years=15,
        domain_expertise=0.8,
        stress_level=0.3,
        attention_span=0.7,
        processing_speed=0.6
    )
    
    # 3視点スコア（例）
    tech_score = 0.8
    market_score = 0.6
    business_score = 0.7
    
    # 統合処理の実行
    result = processor.process_integration(tech_score, market_score, business_score, test_profile)
    
    print("=== 改良版Richtmann認知プロセッサ テスト結果 ===")
    print(f"統合スコア: {result.integration_score:.3f}")
    print(f"推奨複雑性: {result.recommended_complexity}")
    print(f"最適モダリティ: {result.optimal_modality}")
    print(f"認知負荷: {result.cognitive_load:.3f}")
    print(f"信頼度: {result.confidence:.3f}")
    print(f"推奨事項: {', '.join(result.recommendations)}")
    
    # 年齢適応係数の詳細テスト
    print("\n=== 年齢適応係数テスト ===")
    ages = [25, 35, 45, 55, 65]
    for age in ages:
        factor = processor.calculate_age_factor(age, 0.8)
        print(f"年齢{age}歳: 適応係数 {factor:.3f}")
    
    return result

if __name__ == "__main__":
    test_improved_processor()
