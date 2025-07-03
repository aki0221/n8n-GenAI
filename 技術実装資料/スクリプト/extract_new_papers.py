#!/usr/bin/env python3
"""
新しい4つの論文からテキストを抽出するスクリプト
"""

import pdfplumber
import PyPDF2
import os

def extract_text_from_pdf(pdf_path, output_path):
    """PDFからテキストを抽出してファイルに保存"""
    try:
        # pdfplumberを使用してテキスト抽出
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # テキストをファイルに保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✓ 抽出完了: {os.path.basename(pdf_path)}")
        print(f"  文字数: {len(text):,}")
        print(f"  語数: {len(text.split()):,}")
        print(f"  保存先: {output_path}")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ エラー: {pdf_path} - {str(e)}")
        return False

def main():
    """メイン処理"""
    base_dir = "/home/ubuntu/triple_perspective_radar_research"
    citing_papers_dir = f"{base_dir}/citing_papers"
    
    # 抽出対象のPDFファイル
    pdf_files = [
        ("Value-Based_Decision-Making_and_Its_Relation_to_Co.pdf", "richtmann_2024_text.txt"),
        ("Human-AIcoordinationforlarge-scalegroupdecisionmakingwithheterogeneousfeedbackstrategies.pdf", "zhang_2025_text.txt"),
        ("ArtificialIntelligenceandStrategicDecision-Making_EvidencefromEntrepreneursandInvestors.pdf", "csaszar_2024_text.txt"),
        ("Granularcomputing-driventwo-stageconsensusmodelforlarge-scalegroupdecision-making.pdf", "wang_2025_text.txt")
    ]
    
    print("=== 新しい4つの論文からのテキスト抽出開始 ===\n")
    
    success_count = 0
    for pdf_file, output_file in pdf_files:
        pdf_path = f"{citing_papers_dir}/{pdf_file}"
        output_path = f"{citing_papers_dir}/{output_file}"
        
        if extract_text_from_pdf(pdf_path, output_path):
            success_count += 1
    
    print(f"=== 抽出完了: {success_count}/{len(pdf_files)} ファイル成功 ===")

if __name__ == "__main__":
    main()

