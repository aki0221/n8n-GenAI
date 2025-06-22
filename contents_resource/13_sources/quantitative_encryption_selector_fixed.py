# 修正版：完全実装可能な暗号化選択アルゴリズム

import hashlib
import time
import psutil
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305, AESGCM
from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum

class EncryptionMethod(Enum):
    AES_256_GCM = "aes_256_gcm"
    CHACHA20_POLY1305 = "chacha20_poly1305"
    AES_128_GCM = "aes_128_gcm"

@dataclass
class DataCharacteristics:
    """データ特性の定量的定義"""
    size_bytes: int
    access_frequency_per_hour: int
    structure_complexity: float  # 0.0-1.0
    sensitivity_level: int  # 1-5
    real_time_requirement: bool
    mobile_access_required: bool
    iot_device_access: bool

@dataclass
class PerformanceRequirements:
    """パフォーマンス要件の定量的定義"""
    max_latency_ms: int
    min_throughput_mbps: float
    max_cpu_usage_percent: int
    max_memory_usage_mb: int
    battery_constraint: bool
    network_bandwidth_limited: bool

@dataclass
class EncryptionBenchmark:
    """暗号化方式のベンチマーク結果"""
    method: EncryptionMethod
    encryption_speed_mbps: float
    decryption_speed_mbps: float
    cpu_usage_percent: float
    memory_usage_mb: float
    key_size_bits: int
    security_strength_bits: int

class EncryptionPerformanceBenchmark:
    """実際の暗号化性能測定システム"""
    
    def __init__(self):
        self.benchmark_data_sizes = [1024, 10240, 102400]  # 1KB, 10KB, 100KB
        self.benchmark_results = {}
        self._initialize_benchmarks()
    
    def _initialize_benchmarks(self):
        """各暗号化方式のベンチマークを実行"""
        print("暗号化性能ベンチマーク実行中...")
        
        for method in EncryptionMethod:
            print(f"  {method.value} ベンチマーク実行中...")
            self.benchmark_results[method] = self._benchmark_encryption_method(method)
            print(f"  {method.value} 完了")
    
    def _benchmark_encryption_method(self, method: EncryptionMethod) -> EncryptionBenchmark:
        """特定の暗号化方式のベンチマーク実行"""
        total_encryption_time = 0
        total_decryption_time = 0
        iterations = len(self.benchmark_data_sizes)
        
        # CPU使用率の基準値取得
        cpu_baseline = psutil.cpu_percent(interval=0.1)
        memory_baseline = psutil.virtual_memory().used
        
        for data_size in self.benchmark_data_sizes:
            test_data = os.urandom(data_size)
            
            # 暗号化時間測定
            start_time = time.perf_counter()
            encrypted_data = self._encrypt_with_method(test_data, method)
            encryption_time = time.perf_counter() - start_time
            
            # 復号化時間測定
            start_time = time.perf_counter()
            decrypted_data = self._decrypt_with_method(encrypted_data, method)
            decryption_time = time.perf_counter() - start_time
            
            # 結果の蓄積
            total_encryption_time += encryption_time
            total_decryption_time += decryption_time
            
            # データ整合性確認
            assert test_data == decrypted_data, f"データ整合性エラー: {method}"
        
        # CPU・メモリ使用量測定
        cpu_after = psutil.cpu_percent(interval=0.1)
        memory_after = psutil.virtual_memory().used
        
        # 平均値計算
        avg_data_size = sum(self.benchmark_data_sizes) / len(self.benchmark_data_sizes)
        encryption_speed = (avg_data_size / (total_encryption_time / iterations)) / (1024 * 1024)  # MB/s
        decryption_speed = (avg_data_size / (total_decryption_time / iterations)) / (1024 * 1024)  # MB/s
        cpu_usage = max(0, cpu_after - cpu_baseline)
        memory_usage = max(0, (memory_after - memory_baseline) / (1024 * 1024))  # MB
        
        return EncryptionBenchmark(
            method=method,
            encryption_speed_mbps=encryption_speed,
            decryption_speed_mbps=decryption_speed,
            cpu_usage_percent=cpu_usage,
            memory_usage_mb=memory_usage,
            key_size_bits=self._get_key_size(method),
            security_strength_bits=self._get_security_strength(method)
        )
    
    def _encrypt_with_method(self, data: bytes, method: EncryptionMethod) -> dict:
        """指定された方式でデータを暗号化"""
        if method == EncryptionMethod.AES_256_GCM:
            key = os.urandom(32)  # 256 bits
            cipher = AESGCM(key)
            nonce = os.urandom(12)  # 96 bits for GCM
            ciphertext = cipher.encrypt(nonce, data, None)
            return {'ciphertext': ciphertext, 'key': key, 'nonce': nonce}
        
        elif method == EncryptionMethod.CHACHA20_POLY1305:
            key = os.urandom(32)  # 256 bits
            cipher = ChaCha20Poly1305(key)
            nonce = os.urandom(12)  # 96 bits
            ciphertext = cipher.encrypt(nonce, data, None)
            return {'ciphertext': ciphertext, 'key': key, 'nonce': nonce}
        
        elif method == EncryptionMethod.AES_128_GCM:
            key = os.urandom(16)  # 128 bits
            cipher = AESGCM(key)
            nonce = os.urandom(12)  # 96 bits
            ciphertext = cipher.encrypt(nonce, data, None)
            return {'ciphertext': ciphertext, 'key': key, 'nonce': nonce}
    
    def _decrypt_with_method(self, encrypted_data: dict, method: EncryptionMethod) -> bytes:
        """指定された方式でデータを復号化"""
        if method in [EncryptionMethod.AES_256_GCM, EncryptionMethod.AES_128_GCM]:
            cipher = AESGCM(encrypted_data['key'])
            return cipher.decrypt(encrypted_data['nonce'], encrypted_data['ciphertext'], None)
        
        elif method == EncryptionMethod.CHACHA20_POLY1305:
            cipher = ChaCha20Poly1305(encrypted_data['key'])
            return cipher.decrypt(encrypted_data['nonce'], encrypted_data['ciphertext'], None)
    
    def _get_key_size(self, method: EncryptionMethod) -> int:
        """暗号化方式の鍵サイズを取得"""
        key_sizes = {
            EncryptionMethod.AES_256_GCM: 256,
            EncryptionMethod.CHACHA20_POLY1305: 256,
            EncryptionMethod.AES_128_GCM: 128
        }
        return key_sizes[method]
    
    def _get_security_strength(self, method: EncryptionMethod) -> int:
        """暗号化方式のセキュリティ強度を取得"""
        security_strengths = {
            EncryptionMethod.AES_256_GCM: 256,
            EncryptionMethod.CHACHA20_POLY1305: 256,
            EncryptionMethod.AES_128_GCM: 128
        }
        return security_strengths[method]

class QuantitativeEncryptionSelector:
    """定量的暗号化選択アルゴリズム"""
    
    def __init__(self):
        self.benchmark = EncryptionPerformanceBenchmark()
        self.selection_weights = {
            'security': 0.4,
            'performance': 0.3,
            'resource_efficiency': 0.2,
            'compatibility': 0.1
        }
    
    def select_optimal_encryption(
        self,
        data_characteristics: DataCharacteristics,
        performance_requirements: PerformanceRequirements
    ) -> Tuple[EncryptionMethod, float, Dict]:
        """
        データ特性とパフォーマンス要件に基づく最適暗号化方式の選択
        
        Returns:
            Tuple[EncryptionMethod, confidence_score, selection_rationale]
        """
        scores = {}
        detailed_analysis = {}
        
        for method in EncryptionMethod:
            benchmark = self.benchmark.benchmark_results[method]
            
            # セキュリティスコア計算
            security_score = self._calculate_security_score(
                benchmark, data_characteristics
            )
            
            # パフォーマンススコア計算
            performance_score = self._calculate_performance_score(
                benchmark, performance_requirements
            )
            
            # リソース効率スコア計算
            resource_score = self._calculate_resource_efficiency_score(
                benchmark, performance_requirements
            )
            
            # 互換性スコア計算
            compatibility_score = self._calculate_compatibility_score(
                method, data_characteristics
            )
            
            # 総合スコア計算
            total_score = (
                security_score * self.selection_weights['security'] +
                performance_score * self.selection_weights['performance'] +
                resource_score * self.selection_weights['resource_efficiency'] +
                compatibility_score * self.selection_weights['compatibility']
            )
            
            scores[method] = total_score
            detailed_analysis[method] = {
                'security_score': security_score,
                'performance_score': performance_score,
                'resource_score': resource_score,
                'compatibility_score': compatibility_score,
                'total_score': total_score,
                'benchmark_data': benchmark
            }
        
        # 最高スコアの方式を選択
        optimal_method = max(scores, key=scores.get)
        confidence_score = scores[optimal_method]
        
        return optimal_method, confidence_score, detailed_analysis
    
    def _calculate_security_score(
        self,
        benchmark: EncryptionBenchmark,
        data_characteristics: DataCharacteristics
    ) -> float:
        """セキュリティスコアの計算"""
        # セキュリティ強度の正規化 (0-1)
        max_security_bits = 256
        security_strength_score = min(benchmark.security_strength_bits / max_security_bits, 1.0)
        
        # データ機密性要件との適合性
        required_security_level = data_characteristics.sensitivity_level / 5.0
        security_adequacy = min(security_strength_score / max(required_security_level, 0.1), 1.0)
        
        # 最終セキュリティスコア
        return (security_strength_score * 0.6 + security_adequacy * 0.4)
    
    def _calculate_performance_score(
        self,
        benchmark: EncryptionBenchmark,
        performance_requirements: PerformanceRequirements
    ) -> float:
        """パフォーマンススコアの計算"""
        # レイテンシ要件の評価（推定）
        estimated_latency = max(1, 1000 / max(benchmark.encryption_speed_mbps, 0.1))  # ms per MB
        latency_score = max(0, 1 - (estimated_latency / max(performance_requirements.max_latency_ms, 1)))
        
        # スループット要件の評価
        throughput_score = min(benchmark.encryption_speed_mbps / max(performance_requirements.min_throughput_mbps, 0.1), 1.0)
        
        # 最終パフォーマンススコア
        return (latency_score * 0.5 + throughput_score * 0.5)
    
    def _calculate_resource_efficiency_score(
        self,
        benchmark: EncryptionBenchmark,
        performance_requirements: PerformanceRequirements
    ) -> float:
        """リソース効率スコアの計算"""
        # CPU使用率の評価
        cpu_score = max(0, 1 - (benchmark.cpu_usage_percent / max(performance_requirements.max_cpu_usage_percent, 1)))
        
        # メモリ使用量の評価
        memory_score = max(0, 1 - (benchmark.memory_usage_mb / max(performance_requirements.max_memory_usage_mb, 1)))
        
        # バッテリー制約の考慮
        battery_penalty = 0.2 if performance_requirements.battery_constraint and benchmark.cpu_usage_percent > 50 else 0
        
        # 最終リソース効率スコア
        base_score = (cpu_score * 0.6 + memory_score * 0.4)
        return max(0, base_score - battery_penalty)
    
    def _calculate_compatibility_score(
        self,
        method: EncryptionMethod,
        data_characteristics: DataCharacteristics
    ) -> float:
        """互換性スコアの計算"""
        score = 1.0
        
        # モバイルアクセス要件
        if data_characteristics.mobile_access_required:
            if method == EncryptionMethod.CHACHA20_POLY1305:
                score += 0.2  # ChaCha20はモバイルに最適化
        
        # IoTデバイスアクセス要件
        if data_characteristics.iot_device_access:
            if method == EncryptionMethod.AES_128_GCM:
                score += 0.2  # 軽量暗号化
        
        # リアルタイム要件
        if data_characteristics.real_time_requirement:
            if method == EncryptionMethod.CHACHA20_POLY1305:
                score += 0.3  # 高速処理
        
        return max(0, min(score, 1.0))

def demonstrate_quantitative_encryption_selection():
    """定量的暗号化選択のデモンストレーション"""
    print("定量的暗号化選択システム初期化中...")
    selector = QuantitativeEncryptionSelector()
    
    # テストシナリオ1: 高機密データ、標準パフォーマンス
    scenario1_data = DataCharacteristics(
        size_bytes=1048576,  # 1MB
        access_frequency_per_hour=100,
        structure_complexity=0.7,
        sensitivity_level=5,  # 最高機密
        real_time_requirement=False,
        mobile_access_required=False,
        iot_device_access=False
    )
    
    scenario1_perf = PerformanceRequirements(
        max_latency_ms=1000,
        min_throughput_mbps=10.0,
        max_cpu_usage_percent=80,
        max_memory_usage_mb=512,
        battery_constraint=False,
        network_bandwidth_limited=False
    )
    
    # テストシナリオ2: 中機密データ、リアルタイム処理
    scenario2_data = DataCharacteristics(
        size_bytes=10240,  # 10KB
        access_frequency_per_hour=1000,
        structure_complexity=0.3,
        sensitivity_level=3,
        real_time_requirement=True,
        mobile_access_required=True,
        iot_device_access=False
    )
    
    scenario2_perf = PerformanceRequirements(
        max_latency_ms=50,
        min_throughput_mbps=100.0,
        max_cpu_usage_percent=30,
        max_memory_usage_mb=128,
        battery_constraint=True,
        network_bandwidth_limited=True
    )
    
    # テストシナリオ3: IoTデバイス向け軽量データ
    scenario3_data = DataCharacteristics(
        size_bytes=1024,  # 1KB
        access_frequency_per_hour=10000,
        structure_complexity=0.1,
        sensitivity_level=2,
        real_time_requirement=True,
        mobile_access_required=True,
        iot_device_access=True
    )
    
    scenario3_perf = PerformanceRequirements(
        max_latency_ms=10,
        min_throughput_mbps=1.0,
        max_cpu_usage_percent=10,
        max_memory_usage_mb=32,
        battery_constraint=True,
        network_bandwidth_limited=True
    )
    
    scenarios = [
        ("高機密データ・標準パフォーマンス", scenario1_data, scenario1_perf),
        ("中機密データ・リアルタイム処理", scenario2_data, scenario2_perf),
        ("IoTデバイス向け軽量データ", scenario3_data, scenario3_perf)
    ]
    
    results = []
    print("\n暗号化方式選択分析実行中...")
    
    for name, data_char, perf_req in scenarios:
        print(f"  {name} 分析中...")
        optimal_method, confidence, analysis = selector.select_optimal_encryption(
            data_char, perf_req
        )
        
        results.append({
            'scenario': name,
            'optimal_method': optimal_method.value,
            'confidence_score': confidence,
            'security_score': analysis[optimal_method]['security_score'],
            'performance_score': analysis[optimal_method]['performance_score'],
            'resource_score': analysis[optimal_method]['resource_score'],
            'compatibility_score': analysis[optimal_method]['compatibility_score'],
            'benchmark_data': analysis[optimal_method]['benchmark_data']
        })
    
    return results

if __name__ == "__main__":
    print("=== 定量的暗号化選択アルゴリズム実証システム ===")
    results = demonstrate_quantitative_encryption_selection()
    
    print("\n=== 分析結果 ===")
    for result in results:
        print(f"\n【{result['scenario']}】")
        print(f"最適暗号化方式: {result['optimal_method']}")
        print(f"信頼度スコア: {result['confidence_score']:.3f}")
        print(f"  ├ セキュリティスコア: {result['security_score']:.3f}")
        print(f"  ├ パフォーマンススコア: {result['performance_score']:.3f}")
        print(f"  ├ リソース効率スコア: {result['resource_score']:.3f}")
        print(f"  └ 互換性スコア: {result['compatibility_score']:.3f}")
        
        benchmark = result['benchmark_data']
        print(f"実測性能:")
        print(f"  ├ 暗号化速度: {benchmark.encryption_speed_mbps:.2f} MB/s")
        print(f"  ├ 復号化速度: {benchmark.decryption_speed_mbps:.2f} MB/s")
        print(f"  ├ CPU使用率: {benchmark.cpu_usage_percent:.1f}%")
        print(f"  ├ メモリ使用量: {benchmark.memory_usage_mb:.1f} MB")
        print(f"  └ セキュリティ強度: {benchmark.security_strength_bits} bits")
    
    print("\n=== システム実証完了 ===")
    print("このシステムは実際のデータ特性とパフォーマンス要件に基づいて")
    print("定量的に最適な暗号化方式を選択し、実測ベンチマークにより")
    print("その選択の妥当性を検証可能です。")

