#!/usr/bin/env python3
"""
PDF論文解析スクリプト
3つの論文PDFからテキストを抽出し、構造化された分析を実行
"""

import pdfplumber
import PyPDF2
import os
import re
from typing import Dict, List, Tuple

def extract_text_with_pdfplumber(pdf_path: str) -> str:
    """pdfplumberを使用してPDFからテキストを抽出"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"pdfplumber抽出エラー: {e}")
    return text

def extract_text_with_pypdf2(pdf_path: str) -> str:
    """PyPDF2を使用してPDFからテキストを抽出"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"PyPDF2抽出エラー: {e}")
    return text

def extract_pdf_text(pdf_path: str) -> str:
    """複数の方法でPDFテキスト抽出を試行"""
    print(f"PDFテキスト抽出開始: {pdf_path}")
    
    # まずpdfplumberを試行
    text = extract_text_with_pdfplumber(pdf_path)
    
    # pdfplumberで十分なテキストが取得できない場合はPyPDF2を試行
    if len(text.strip()) < 1000:
        print("pdfplumberで十分なテキストが取得できませんでした。PyPDF2を試行します。")
        text = extract_text_with_pypdf2(pdf_path)
    
    return text

def analyze_paper_structure(text: str, paper_title: str) -> Dict:
    """論文の構造を分析"""
    analysis = {
        "title": paper_title,
        "total_length": len(text),
        "word_count": len(text.split()),
        "sections": [],
        "key_concepts": [],
        "mathematical_content": [],
        "references_section": ""
    }
    
    # セクション見出しを検出
    section_patterns = [
        r'^(\d+\.?\s+[A-Z][^.\n]*)',
        r'^([A-Z][A-Z\s]+)$',
        r'^(Abstract|Introduction|Conclusion|References|Methodology|Results|Discussion)',
    ]
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if len(line) > 3 and len(line) < 100:
            for pattern in section_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    analysis["sections"].append(line)
                    break
    
    # 数学的内容を検出
    math_patterns = [
        r'[A-Za-z]\s*=\s*[^=\n]+',  # 数式
        r'\b(?:equation|formula|theorem|lemma|proof)\b',  # 数学用語
        r'[∑∏∫∂∇αβγδεζηθικλμνξοπρστυφχψω]',  # 数学記号
        r'\b\d+\.\d+\b',  # 数値
    ]
    
    for pattern in math_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            analysis["mathematical_content"].extend(matches[:10])  # 最初の10個まで
    
    # キーコンセプトを検出
    key_terms = [
        'decision making', 'multi-perspective', 'consensus', 'strategic',
        'value-based', 'confidence', 'group decision', 'perspective',
        'framework', 'model', 'algorithm', 'methodology'
    ]
    
    for term in key_terms:
        count = len(re.findall(term, text, re.IGNORECASE))
        if count > 0:
            analysis["key_concepts"].append(f"{term}: {count}回")
    
    return analysis

def main():
    """メイン処理"""
    pdf_files = [
        ("/home/ubuntu/upload/Multi-perspectiveStrategicDecisionMaking.pdf", "Wainfan (2010) - Multi-perspective Strategic Decision Making"),
        ("/home/ubuntu/upload/Engagingmultipleperspectives_Avalue-baseddecision-makingmodel.pdf", "Hall & Davis (2007) - Value-based Decision-making Model"),
        ("/home/ubuntu/upload/Confidenceconsensus-basedmodelforlarge-scalegroupdecisionmaking_Anovelapproachtomanagingnon-cooperativebehaviors.pdf", "Xu et al. (2019) - Confidence Consensus-based Model")
    ]
    
    results = {}
    
    for pdf_path, title in pdf_files:
        if os.path.exists(pdf_path):
            print(f"\n{'='*60}")
            print(f"論文分析開始: {title}")
            print(f"{'='*60}")
            
            # テキスト抽出
            text = extract_pdf_text(pdf_path)
            
            if text.strip():
                # 構造分析
                analysis = analyze_paper_structure(text, title)
                results[title] = {
                    "text": text,
                    "analysis": analysis
                }
                
                print(f"抽出完了: {len(text)}文字, {len(text.split())}語")
                print(f"検出されたセクション数: {len(analysis['sections'])}")
                print(f"キーコンセプト数: {len(analysis['key_concepts'])}")
                
                # テキストファイルに保存
                output_filename = f"/home/ubuntu/extracted_{title.split()[0].lower()}_text.txt"
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(f"論文タイトル: {title}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(text)
                
                print(f"テキストファイル保存: {output_filename}")
                
            else:
                print(f"テキスト抽出に失敗しました: {pdf_path}")
        else:
            print(f"ファイルが見つかりません: {pdf_path}")
    
    return results

if __name__ == "__main__":
    results = main()
    print(f"\n{'='*60}")
    print("PDF解析完了")
    print(f"{'='*60}")

