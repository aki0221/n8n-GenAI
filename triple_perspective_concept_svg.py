import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon, FancyArrowPatch, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.font_manager as fm

# 日本語フォントの設定
plt.rcParams['font.family'] = ['IPAGothic', 'IPAexGothic', 'IPAPGothic', 'sans-serif']

# 図のサイズ設定
plt.figure(figsize=(12, 10))
ax = plt.subplot(111)

# 背景色設定
ax.set_facecolor('#f8f8f8')

# 3つの視点を表す円の中心座標
centers = {
    'tech': (0.3, 0.7),
    'market': (0.7, 0.7),
    'business': (0.5, 0.3)
}

# 円の半径
radius = 0.25

# 色の定義
colors = {
    'tech': '#3498db',      # 青色
    'market': '#e74c3c',    # 赤色
    'business': '#2ecc71',  # 緑色
    'overlap': '#f39c12',   # オレンジ色（重なり部分）
    'center': '#9b59b6'     # 紫色（中央部分）
}

# 透明度
alpha = 0.6

# 円の描画
tech_circle = Circle(centers['tech'], radius, color=colors['tech'], alpha=alpha, zorder=1)
market_circle = Circle(centers['market'], radius, color=colors['market'], alpha=alpha, zorder=1)
business_circle = Circle(centers['business'], radius, color=colors['business'], alpha=alpha, zorder=1)

ax.add_patch(tech_circle)
ax.add_patch(market_circle)
ax.add_patch(business_circle)

# 視点の名前を追加（日英併記）
ax.text(centers['tech'][0], centers['tech'][1], 'テクノロジー視点\n(Technology)', 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#000')
ax.text(centers['market'][0], centers['market'][1], 'マーケット視点\n(Market)', 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#000')
ax.text(centers['business'][0], centers['business'][1], 'ビジネス視点\n(Business)', 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#000')

# 中央の重なり部分に「コンセンサスモデル」を表示
ax.text(0.5, 0.55, 'コンセンサスモデル\n(Consensus Model)', 
        ha='center', va='center', fontsize=12, fontweight='bold', color='#000', 
        bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))

# 各視点の特徴を示すテキスト
features = {
    'tech': ['技術成熟度\n(Tech Maturity)', '技術革新指標\n(Innovation Index)', '技術競争力\n(Tech Competitiveness)'],
    'market': ['市場成長率\n(Market Growth)', '顧客ニーズ変化\n(Customer Needs)', '競合動向\n(Competition)'],
    'business': ['収益性指標\n(Profitability)', '事業拡張性\n(Scalability)', '組織能力\n(Capabilities)']
}

# テキスト位置の調整
text_positions = {
    'tech': [(0.15, 0.85), (0.15, 0.75), (0.15, 0.65)],
    'market': [(0.85, 0.85), (0.85, 0.75), (0.85, 0.65)],
    'business': [(0.35, 0.15), (0.5, 0.15), (0.65, 0.15)]
}

# 特徴テキストの追加
for perspective, texts in features.items():
    for i, text in enumerate(texts):
        ax.text(text_positions[perspective][i][0], text_positions[perspective][i][1], 
                text, ha='center', va='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor=colors[perspective], boxstyle='round,pad=0.3'))

# 矢印の追加（視点間の相互作用を示す）
arrow_style = "fancy,head_width=8,head_length=12"
arrow1 = FancyArrowPatch(centers['tech'], centers['market'], connectionstyle="arc3,rad=0.2", 
                        arrowstyle=arrow_style, color='gray', lw=1.5, alpha=0.7)
arrow2 = FancyArrowPatch(centers['market'], centers['business'], connectionstyle="arc3,rad=0.2", 
                        arrowstyle=arrow_style, color='gray', lw=1.5, alpha=0.7)
arrow3 = FancyArrowPatch(centers['business'], centers['tech'], connectionstyle="arc3,rad=0.2", 
                        arrowstyle=arrow_style, color='gray', lw=1.5, alpha=0.7)

ax.add_patch(arrow1)
ax.add_patch(arrow2)
ax.add_patch(arrow3)

# タイトルの追加
plt.title('トリプルパースペクティブ型戦略AIレーダー概念図\n(Triple Perspective Strategic AI Radar Concept)', fontsize=18, fontweight='bold', pad=20)

# 凡例の追加
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['tech'], markersize=15, alpha=alpha, label='テクノロジー視点 (Technology)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['market'], markersize=15, alpha=alpha, label='マーケット視点 (Market)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['business'], markersize=15, alpha=alpha, label='ビジネス視点 (Business)')
]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.05), ncol=3)

# 軸の設定
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')

# SVG形式で保存
plt.savefig('/home/ubuntu/note_research/diagrams/triple_perspective_concept_fig1-1.svg', format='svg', bbox_inches='tight')
plt.savefig('/home/ubuntu/note_research/diagrams/triple_perspective_concept_fig1-1.png', dpi=300, bbox_inches='tight')

# 図の表示
plt.close()

print("トリプルパースペクティブ概念図（図1-1）をSVG形式で作成しました。")
