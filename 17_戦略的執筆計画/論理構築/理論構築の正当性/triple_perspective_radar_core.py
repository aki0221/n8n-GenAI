"""
トリプルパースペクティブ型戦略AIレーダー：核心アルゴリズム実装

このモジュールは、3視点統合×3軸評価×コンセンサスモデルによる
戦略的意思決定支援システムの核心アルゴリズムを実装する。

数学的基盤：
- AHP (Analytic Hierarchy Process) による重要度算出
- TOPSIS による代替案評価
- 動的システム理論によるコンセンサス形成
- セマンティック推論による洞察生成
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging
from scipy.linalg import eig
from scipy.spatial.distance import euclidean
import networkx as nx

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerspectiveType(Enum):
    """視点タイプの定義"""
    TECHNOLOGY = "technology"
    MARKET = "market"
    BUSINESS = "business"

class EvaluationAxis(Enum):
    """評価軸の定義"""
    IMPORTANCE = "importance"
    CONFIDENCE = "confidence"
    CONSISTENCY = "consistency"

@dataclass
class StrategicCriterion:
    """戦略的基準の定義"""
    id: str
    name: str
    description: str
    perspective: PerspectiveType
    weight: float = 0.0

@dataclass
class EvaluationResult:
    """評価結果の定義"""
    criterion_id: str
    importance: float
    confidence: float
    consistency: float
    overall_score: float

class AHPProcessor:
    """AHP（階層分析法）による重要度算出"""
    
    def __init__(self, tolerance: float = 1e-6, max_iterations: int = 100):
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def create_pairwise_matrix(self, criteria: List[StrategicCriterion], 
                              comparisons: Dict[Tuple[str, str], float]) -> np.ndarray:
        """ペアワイズ比較行列の作成"""
        n = len(criteria)
        matrix = np.ones((n, n))
        
        criterion_indices = {criterion.id: i for i, criterion in enumerate(criteria)}
        
        for (id1, id2), value in comparisons.items():
            i, j = criterion_indices[id1], criterion_indices[id2]
            matrix[i, j] = value
            matrix[j, i] = 1.0 / value
        
        return matrix
    
    def calculate_weights(self, pairwise_matrix: np.ndarray) -> Tuple[np.ndarray, float]:
        """固有ベクトル法による重み算出"""
        eigenvalues, eigenvectors = eig(pairwise_matrix)
        
        # 最大固有値とその固有ベクトルを取得
        max_eigenvalue_index = np.argmax(eigenvalues.real)
        max_eigenvalue = eigenvalues[max_eigenvalue_index].real
        principal_eigenvector = eigenvectors[:, max_eigenvalue_index].real
        
        # 正規化
        weights = principal_eigenvector / np.sum(principal_eigenvector)
        
        return weights, max_eigenvalue
    
    def calculate_consistency_ratio(self, pairwise_matrix: np.ndarray, 
                                  max_eigenvalue: float) -> float:
        """整合性比率の算出"""
        n = pairwise_matrix.shape[0]
        
        # 整合性指標（CI）
        ci = (max_eigenvalue - n) / (n - 1)
        
        # ランダム整合性指標（RI）
        ri_values = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 
                    7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        ri = ri_values.get(n, 1.49)
        
        # 整合性比率（CR）
        cr = ci / ri if ri > 0 else 0
        
        return cr

class TOPSISProcessor:
    """TOPSIS法による代替案評価"""
    
    def __init__(self):
        self.decision_matrix = None
        self.weights = None
        self.normalized_matrix = None
        self.weighted_matrix = None
    
    def normalize_matrix(self, decision_matrix: np.ndarray) -> np.ndarray:
        """決定行列の正規化"""
        normalized = np.zeros_like(decision_matrix)
        
        for j in range(decision_matrix.shape[1]):
            column_norm = np.sqrt(np.sum(decision_matrix[:, j] ** 2))
            if column_norm > 0:
                normalized[:, j] = decision_matrix[:, j] / column_norm
        
        return normalized
    
    def apply_weights(self, normalized_matrix: np.ndarray, 
                     weights: np.ndarray) -> np.ndarray:
        """重み付き正規化行列の作成"""
        return normalized_matrix * weights
    
    def find_ideal_solutions(self, weighted_matrix: np.ndarray, 
                           benefit_criteria: List[bool]) -> Tuple[np.ndarray, np.ndarray]:
        """理想解と負理想解の算出"""
        positive_ideal = np.zeros(weighted_matrix.shape[1])
        negative_ideal = np.zeros(weighted_matrix.shape[1])
        
        for j in range(weighted_matrix.shape[1]):
            if benefit_criteria[j]:  # 利益基準
                positive_ideal[j] = np.max(weighted_matrix[:, j])
                negative_ideal[j] = np.min(weighted_matrix[:, j])
            else:  # コスト基準
                positive_ideal[j] = np.min(weighted_matrix[:, j])
                negative_ideal[j] = np.max(weighted_matrix[:, j])
        
        return positive_ideal, negative_ideal
    
    def calculate_distances(self, weighted_matrix: np.ndarray, 
                          positive_ideal: np.ndarray, 
                          negative_ideal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """理想解からの距離計算"""
        distances_positive = np.array([
            euclidean(row, positive_ideal) for row in weighted_matrix
        ])
        
        distances_negative = np.array([
            euclidean(row, negative_ideal) for row in weighted_matrix
        ])
        
        return distances_positive, distances_negative
    
    def calculate_relative_closeness(self, distances_positive: np.ndarray, 
                                   distances_negative: np.ndarray) -> np.ndarray:
        """相対的近接度の算出"""
        return distances_negative / (distances_positive + distances_negative)

class ConsensusEngine:
    """コンセンサス形成エンジン"""
    
    def __init__(self, learning_rate: float = 0.1, convergence_threshold: float = 1e-3):
        self.learning_rate = learning_rate
        self.convergence_threshold = convergence_threshold
        self.opinion_history = []
    
    def detect_non_cooperative_behavior(self, opinions: np.ndarray, 
                                      previous_opinions: np.ndarray, 
                                      threshold: float = 0.05) -> np.ndarray:
        """非協力的行動の検出"""
        if previous_opinions is None:
            return np.zeros(len(opinions), dtype=bool)
        
        changes = np.abs(opinions - previous_opinions)
        return changes < threshold
    
    def calculate_cooperation_level(self, opinions: np.ndarray, 
                                  group_opinion: np.ndarray, 
                                  variance_threshold: float = 1.0) -> np.ndarray:
        """協力度レベルの算出"""
        distances = np.array([
            euclidean(opinion, group_opinion) for opinion in opinions
        ])
        
        cooperation_levels = np.exp(-distances ** 2 / variance_threshold)
        return cooperation_levels
    
    def update_weights(self, current_weights: np.ndarray, 
                      cooperation_levels: np.ndarray, 
                      adjustment_strength: float = 0.5) -> np.ndarray:
        """重み調整メカニズム"""
        new_weights = current_weights * (cooperation_levels ** adjustment_strength)
        return new_weights / np.sum(new_weights)  # 正規化
    
    def consensus_iteration(self, opinions: np.ndarray, 
                          weights: np.ndarray) -> Tuple[np.ndarray, float]:
        """コンセンサス反復プロセス"""
        # 重み付き群意見の計算
        group_opinion = np.average(opinions, weights=weights, axis=0)
        
        # 協力度レベルの算出
        cooperation_levels = self.calculate_cooperation_level(opinions, group_opinion)
        
        # 重みの更新
        updated_weights = self.update_weights(weights, cooperation_levels)
        
        # 意見の調整
        adjusted_opinions = np.zeros_like(opinions)
        for i in range(len(opinions)):
            adjustment = self.learning_rate * (group_opinion - opinions[i])
            adjusted_opinions[i] = opinions[i] + adjustment
        
        # 収束度の計算
        convergence_measure = np.mean([
            euclidean(opinion, group_opinion) for opinion in adjusted_opinions
        ])
        
        return adjusted_opinions, convergence_measure

class SemanticReasoningEngine:
    """セマンティック推論エンジン"""
    
    def __init__(self):
        self.knowledge_graph = nx.DiGraph()
        self.concept_embeddings = {}
    
    def add_concept(self, concept_id: str, properties: Dict[str, any]):
        """概念の追加"""
        self.knowledge_graph.add_node(concept_id, **properties)
    
    def add_relation(self, source: str, target: str, relation_type: str, 
                    strength: float = 1.0):
        """関係の追加"""
        self.knowledge_graph.add_edge(source, target, 
                                    relation_type=relation_type, 
                                    strength=strength)
    
    def calculate_semantic_distance(self, concept1: str, concept2: str) -> float:
        """セマンティック距離の計算"""
        try:
            path_length = nx.shortest_path_length(self.knowledge_graph, 
                                                concept1, concept2)
            max_distance = len(self.knowledge_graph.nodes())
            return path_length / max_distance
        except nx.NetworkXNoPath:
            return 1.0  # 接続なしの場合は最大距離
    
    def find_emergent_insights(self, concepts: List[str], 
                             threshold: float = 0.3) -> List[Dict[str, any]]:
        """創発的洞察の発見"""
        insights = []
        
        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts[i+1:], i+1):
                distance = self.calculate_semantic_distance(concept1, concept2)
                
                if distance < threshold:
                    # 近い概念間の関係を洞察として抽出
                    insight = {
                        'concept1': concept1,
                        'concept2': concept2,
                        'semantic_distance': distance,
                        'insight_strength': 1.0 - distance,
                        'type': 'semantic_proximity'
                    }
                    insights.append(insight)
        
        return sorted(insights, key=lambda x: x['insight_strength'], reverse=True)

class TriplePerspectiveRadar:
    """トリプルパースペクティブ型戦略AIレーダー メインクラス"""
    
    def __init__(self):
        self.ahp_processor = AHPProcessor()
        self.topsis_processor = TOPSISProcessor()
        self.consensus_engine = ConsensusEngine()
        self.semantic_engine = SemanticReasoningEngine()
        
        self.criteria = []
        self.evaluation_results = []
        self.consensus_history = []
    
    def add_criterion(self, criterion: StrategicCriterion):
        """戦略的基準の追加"""
        self.criteria.append(criterion)
        logger.info(f"基準追加: {criterion.name} ({criterion.perspective.value})")
    
    def evaluate_3axis(self, criterion_id: str, 
                      importance_data: Dict[str, float],
                      confidence_data: Dict[str, float],
                      consistency_data: Dict[str, float]) -> EvaluationResult:
        """3軸評価の実行"""
        
        # 重要度の算出（AHP）
        importance_score = self._calculate_importance(importance_data)
        
        # 確信度の算出（統計的手法）
        confidence_score = self._calculate_confidence(confidence_data)
        
        # 整合性の算出（論理的整合性）
        consistency_score = self._calculate_consistency(consistency_data)
        
        # 総合スコアの算出
        overall_score = (importance_score * 0.4 + 
                        confidence_score * 0.3 + 
                        consistency_score * 0.3)
        
        result = EvaluationResult(
            criterion_id=criterion_id,
            importance=importance_score,
            confidence=confidence_score,
            consistency=consistency_score,
            overall_score=overall_score
        )
        
        self.evaluation_results.append(result)
        return result
    
    def _calculate_importance(self, data: Dict[str, float]) -> float:
        """重要度の算出"""
        # 簡略化された重要度計算（実際はAHPを使用）
        values = list(data.values())
        return np.mean(values) if values else 0.0
    
    def _calculate_confidence(self, data: Dict[str, float]) -> float:
        """確信度の算出"""
        values = list(data.values())
        if len(values) < 2:
            return 0.5
        
        mean_val = np.mean(values)
        std_val = np.std(values)
        
        # 標準偏差の逆数として確信度を定義
        confidence = 1.0 / (1.0 + std_val) if std_val > 0 else 1.0
        return min(confidence, 1.0)
    
    def _calculate_consistency(self, data: Dict[str, float]) -> float:
        """整合性の算出"""
        values = list(data.values())
        if len(values) < 2:
            return 1.0
        
        # 値の分散の逆数として整合性を定義
        variance = np.var(values)
        consistency = 1.0 / (1.0 + variance) if variance > 0 else 1.0
        return consistency
    
    def integrate_perspectives(self, 
                             tech_evaluations: List[EvaluationResult],
                             market_evaluations: List[EvaluationResult],
                             business_evaluations: List[EvaluationResult]) -> Dict[str, float]:
        """3視点統合の実行"""
        
        # 各視点の重み（調整可能）
        perspective_weights = {
            PerspectiveType.TECHNOLOGY: 0.35,
            PerspectiveType.MARKET: 0.35,
            PerspectiveType.BUSINESS: 0.30
        }
        
        integrated_scores = {}
        
        # 各基準について視点統合を実行
        all_evaluations = tech_evaluations + market_evaluations + business_evaluations
        
        for criterion in self.criteria:
            criterion_evaluations = [
                eval_result for eval_result in all_evaluations 
                if eval_result.criterion_id == criterion.id
            ]
            
            if criterion_evaluations:
                # 視点別スコアの重み付き平均
                weighted_score = sum(
                    eval_result.overall_score * perspective_weights[criterion.perspective]
                    for eval_result in criterion_evaluations
                )
                integrated_scores[criterion.id] = weighted_score
        
        return integrated_scores
    
    def generate_strategic_insights(self, integrated_scores: Dict[str, float]) -> List[Dict[str, any]]:
        """戦略的洞察の生成"""
        insights = []
        
        # 高スコア基準の特定
        sorted_scores = sorted(integrated_scores.items(), key=lambda x: x[1], reverse=True)
        top_criteria = sorted_scores[:3]  # 上位3基準
        
        for criterion_id, score in top_criteria:
            criterion = next((c for c in self.criteria if c.id == criterion_id), None)
            if criterion:
                insight = {
                    'type': 'high_priority',
                    'criterion': criterion.name,
                    'perspective': criterion.perspective.value,
                    'score': score,
                    'recommendation': f"{criterion.name}は戦略的優先度が高く、重点的な投資を推奨"
                }
                insights.append(insight)
        
        # セマンティック推論による創発的洞察
        concept_ids = [criterion.id for criterion in self.criteria]
        emergent_insights = self.semantic_engine.find_emergent_insights(concept_ids)
        
        for emergent in emergent_insights[:2]:  # 上位2つの創発的洞察
            insight = {
                'type': 'emergent',
                'concept1': emergent['concept1'],
                'concept2': emergent['concept2'],
                'strength': emergent['insight_strength'],
                'recommendation': f"{emergent['concept1']}と{emergent['concept2']}の相乗効果を活用した統合戦略を検討"
            }
            insights.append(insight)
        
        return insights
    
    def run_consensus_process(self, stakeholder_opinions: np.ndarray, 
                            max_iterations: int = 50) -> Dict[str, any]:
        """コンセンサス形成プロセスの実行"""
        
        # 初期重み（均等）
        weights = np.ones(len(stakeholder_opinions)) / len(stakeholder_opinions)
        
        current_opinions = stakeholder_opinions.copy()
        convergence_history = []
        
        for iteration in range(max_iterations):
            # コンセンサス反復
            current_opinions, convergence_measure = self.consensus_engine.consensus_iteration(
                current_opinions, weights
            )
            
            convergence_history.append(convergence_measure)
            
            # 収束判定
            if convergence_measure < self.consensus_engine.convergence_threshold:
                logger.info(f"コンセンサス収束: {iteration+1}回目の反復で収束")
                break
        
        # 最終群意見の算出
        final_group_opinion = np.average(current_opinions, weights=weights, axis=0)
        
        result = {
            'final_group_opinion': final_group_opinion,
            'convergence_iterations': len(convergence_history),
            'final_convergence_measure': convergence_history[-1] if convergence_history else float('inf'),
            'convergence_history': convergence_history,
            'consensus_achieved': convergence_measure < self.consensus_engine.convergence_threshold
        }
        
        self.consensus_history.append(result)
        return result

# 使用例とテストコード
if __name__ == "__main__":
    # システムの初期化
    radar = TriplePerspectiveRadar()
    
    # 戦略的基準の定義
    criteria = [
        StrategicCriterion("tech_ai", "AI技術革新", "AI技術の革新性と競争優位性", PerspectiveType.TECHNOLOGY),
        StrategicCriterion("market_demand", "市場需要", "市場における需要の強さと成長性", PerspectiveType.MARKET),
        StrategicCriterion("business_roi", "投資収益性", "ビジネス投資の収益性と持続性", PerspectiveType.BUSINESS)
    ]
    
    for criterion in criteria:
        radar.add_criterion(criterion)
    
    # 3軸評価の実行例
    tech_evaluation = radar.evaluate_3axis(
        "tech_ai",
        importance_data={"expert1": 0.8, "expert2": 0.9, "expert3": 0.7},
        confidence_data={"expert1": 0.7, "expert2": 0.8, "expert3": 0.6},
        consistency_data={"expert1": 0.9, "expert2": 0.8, "expert3": 0.9}
    )
    
    print(f"技術評価結果: {tech_evaluation}")
    
    # コンセンサス形成の実行例
    stakeholder_opinions = np.array([
        [0.8, 0.6, 0.7],  # ステークホルダー1の意見
        [0.7, 0.8, 0.6],  # ステークホルダー2の意見
        [0.9, 0.5, 0.8],  # ステークホルダー3の意見
    ])
    
    consensus_result = radar.run_consensus_process(stakeholder_opinions)
    print(f"コンセンサス結果: {consensus_result}")

