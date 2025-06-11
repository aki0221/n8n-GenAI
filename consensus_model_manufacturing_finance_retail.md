# 成果物結合プロトコルとインデックス管理

## 1. ファイル命名規則

### 1.1 業種別適用例ファイル

- 製造業適用例: `01_manufacturing_use_case.md`
- 金融業適用例: `02_finance_use_case.md`
- 小売業適用例: `03_retail_use_case.md`

### 1.2 実装ガイダンスファイル

- 初心者向けガイド: `04_beginner_implementation_guide.md`
- 中級者向けガイド: `05_intermediate_implementation_guide.md`
- 上級者向けガイド: `06_advanced_implementation_guide.md`

### 1.3 エラーハンドリングとスケーラビリティファイル

- エラーハンドリング: `07_error_handling_examples.md`
- スケーラビリティ: `08_scalability_strategies.md`

### 1.4 用語集と補足説明ファイル

- 用語集: `09_glossary.md`
- 初心者向け補足説明: `10_beginner_supplement.md`

## 2. インデックス管理

### 2.1 ファイル間の依存関係

```
メインドキュメント
├── 01_manufacturing_use_case.md
├── 02_finance_use_case.md
├── 03_retail_use_case.md
├── 04_beginner_implementation_guide.md
├── 05_intermediate_implementation_guide.md
├── 06_advanced_implementation_guide.md
├── 07_error_handling_examples.md
├── 08_scalability_strategies.md
├── 09_glossary.md
└── 10_beginner_supplement.md
```

### 2.2 ファイル内構造テンプレート

各ファイルの冒頭に以下のメタデータを含めます：

```
---
file_id: "01_manufacturing_use_case"
title: "製造業向けコンセンサスモデル適用例"
version: "1.0"
created_at: "2025-06-06"
position: 1
previous_file: "none"
next_file: "02_finance_use_case"
main_document_section: "業種別適用例"
---
```

## 3. 結合手順

1. 各ファイルを個別に作成・編集
2. ファイル単位で保存と検証
3. メインドキュメントへの挿入位置を特定
4. メインドキュメントへの統合
5. 相互参照の更新
6. 最終検証

## 4. 進捗管理

| ファイルID | 状態 | 作成日時 | 最終更新 | 検証状態 |
|----------|------|---------|---------|---------|
| 01_manufacturing_use_case | 未着手 | - | - | - |
| 02_finance_use_case | 未着手 | - | - | - |
| 03_retail_use_case | 未着手 | - | - | - |
| 04_beginner_implementation_guide | 未着手 | - | - | - |
| 05_intermediate_implementation_guide | 未着手 | - | - | - |
| 06_advanced_implementation_guide | 未着手 | - | - | - |
| 07_error_handling_examples | 未着手 | - | - | - |
| 08_scalability_strategies | 未着手 | - | - | - |
| 09_glossary | 未着手 | - | - | - |
| 10_beginner_supplement | 未着手 | - | - | - |

## 5. エラー発生時の対応

1. 作業中のファイルを保存
2. エラーログを記録
3. 最後の安定状態から再開
4. 必要に応じてファイルを分割
5. 進捗管理表を更新
