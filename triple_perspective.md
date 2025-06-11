# インタラクティブダッシュボードの設計：確信度の視覚的表現

## 確信度の視覚的表現の重要性

トリプルパースペクティブ型戦略AIレーダーにおいて、確信度の厳密な評価と視覚的表現は、意思決定の質を大きく左右する重要な要素です。特に情報不均衡が存在する状況では、確信度を適切に表現することで、ユーザーは結果の信頼性を正確に理解し、より適切な判断を下すことができます。

本セクションでは、確信度の視覚的表現に焦点を当て、インタラクティブダッシュボードにおける実装方法を詳細に解説します。

### 確信度表現の目的

確信度の視覚的表現には、以下の目的があります：

1. **不確実性の明示化**
   - 分析結果に含まれる不確実性の程度を明示的に示す
   - 情報不足や情報の質の問題を透明に伝える

2. **判断の支援**
   - 確信度の低い結果に対する過度の依存を防ぐ
   - 確信度に応じた意思決定の調整を促す

3. **追加情報収集の動機付け**
   - 確信度の低い領域を特定し、追加情報収集の優先順位付けを支援
   - 情報不均衡の改善に向けた具体的なアクションを促す

4. **時間的変化の把握**
   - 確信度の時間的変化を追跡し、情報の蓄積による確信度向上を可視化
   - 突発的な確信度低下を検出し、早期警告として活用

## 確信度の多次元評価

確信度を厳密に評価するためには、単一の指標ではなく、複数の次元から評価することが重要です。以下に、確信度の多次元評価の枠組みを示します。

### 評価次元

1. **情報量の次元**
   - データポイント数
   - 情報源の数
   - 時間的カバレッジ

2. **情報質の次元**
   - 情報源の信頼性
   - データの鮮度
   - 検証可能性

3. **整合性の次元**
   - 内部整合性（同一視点内）
   - 外部整合性（視点間）
   - 時間的整合性

4. **専門性の次元**
   - 専門家の関与度
   - 専門知識の適用度
   - 方法論の堅牢性

### 次元間の関係

これらの次元は互いに独立ではなく、相互に影響し合います。例えば、情報量が多くても情報質が低ければ、全体の確信度は低下します。また、整合性が高くても専門性が不足していれば、誤った方向に高い確信度を持つリスクがあります。

このような次元間の関係を考慮し、総合的な確信度評価を行うことが重要です。

## 確信度の視覚的表現手法

確信度を視覚的に表現するための手法として、以下のアプローチを提案します。

### 1. 信頼区間と確率分布

信頼区間と確率分布は、不確実性を定量的に表現するための強力なツールです。

#### 実装方法

```javascript
// n8n workflow: Confidence Interval Visualization
// Function node for generating confidence interval data
[
  {
    "id": "generateConfidenceIntervalData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Score and uncertainty level
        const score = $input.item.json.score || 0.7;
        const uncertainty = $input.item.json.uncertainty || 0.3;
        
        // Calculate interval width based on uncertainty
        const intervalWidth = score * uncertainty;
        
        // Calculate lower and upper bounds
        const lowerBound = Math.max(0, score - intervalWidth / 2);
        const upperBound = Math.min(1, score + intervalWidth / 2);
        
        // Generate distribution points for visualization
        const distributionPoints = [];
        const pointCount = 100;
        const stdDev = intervalWidth / 4; // Approximate for normal distribution
        
        for (let i = 0; i < pointCount; i++) {
          const x = lowerBound + (upperBound - lowerBound) * i / (pointCount - 1);
          
          // Generate normal distribution around score
          const y = Math.exp(-0.5 * Math.pow((x - score) / stdDev, 2)) / (stdDev * Math.sqrt(2 * Math.PI));
          
          distributionPoints.push({ x, y });
        }
        
        // Normalize y values to max of 1
        const maxY = Math.max(...distributionPoints.map(p => p.y));
        const normalizedPoints = distributionPoints.map(p => ({ x: p.x, y: p.y / maxY }));
        
        return {
          json: {
            score,
            uncertainty,
            confidence_interval: {
              lower_bound: lowerBound,
              central_value: score,
              upper_bound: upperBound,
              interval_width: upperBound - lowerBound
            },
            distribution_points: normalizedPoints
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（D3.js）

```javascript
// D3.js implementation for confidence interval visualization
function renderConfidenceInterval(data, containerId) {
  // Clear previous content
  d3.select(`#${containerId}`).html("");
  
  // Set dimensions
  const width = 600;
  const height = 200;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Create SVG
  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  
  // Create group for the visualization
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // Create scales
  const xScale = d3.scaleLinear()
    .domain([0, 1])
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, 1])
    .range([innerHeight, 0]);
  
  // Create area generator
  const area = d3.area()
    .x(d => xScale(d.x))
    .y0(innerHeight)
    .y1(d => yScale(d.y))
    .curve(d3.curveBasis);
  
  // Draw confidence interval area
  g.append("path")
    .datum(data.distribution_points)
    .attr("fill", "rgba(70, 130, 180, 0.5)")
    .attr("d", area);
  
  // Draw central value line
  g.append("line")
    .attr("x1", xScale(data.confidence_interval.central_value))
    .attr("x2", xScale(data.confidence_interval.central_value))
    .attr("y1", 0)
    .attr("y2", innerHeight)
    .attr("stroke", "rgba(70, 130, 180, 1)")
    .attr("stroke-width", 2)
    .attr("stroke-dasharray", "5,5");
  
  // Draw lower and upper bound lines
  g.append("line")
    .attr("x1", xScale(data.confidence_interval.lower_bound))
    .attr("x2", xScale(data.confidence_interval.lower_bound))
    .attr("y1", 0)
    .attr("y2", innerHeight)
    .attr("stroke", "rgba(70, 130, 180, 0.7)")
    .attr("stroke-width", 1)
    .attr("stroke-dasharray", "3,3");
  
  g.append("line")
    .attr("x1", xScale(data.confidence_interval.upper_bound))
    .attr("x2", xScale(data.confidence_interval.upper_bound))
    .attr("y1", 0)
    .attr("y2", innerHeight)
    .attr("stroke", "rgba(70, 130, 180, 0.7)")
    .attr("stroke-width", 1)
    .attr("stroke-dasharray", "3,3");
  
  // Add labels
  g.append("text")
    .attr("x", xScale(data.confidence_interval.central_value))
    .attr("y", innerHeight + 20)
    .attr("text-anchor", "middle")
    .text(`${Math.round(data.confidence_interval.central_value * 100)}%`);
  
  g.append("text")
    .attr("x", xScale(data.confidence_interval.lower_bound))
    .attr("y", innerHeight + 20)
    .attr("text-anchor", "middle")
    .text(`${Math.round(data.confidence_interval.lower_bound * 100)}%`);
  
  g.append("text")
    .attr("x", xScale(data.confidence_interval.upper_bound))
    .attr("y", innerHeight + 20)
    .attr("text-anchor", "middle")
    .text(`${Math.round(data.confidence_interval.upper_bound * 100)}%`);
  
  // Add axes
  const xAxis = d3.axisBottom(xScale)
    .tickFormat(d => `${d * 100}%`);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(xAxis);
  
  g.append("text")
    .attr("x", innerWidth / 2)
    .attr("y", innerHeight + margin.bottom - 5)
    .attr("text-anchor", "middle")
    .text("スコア");
  
  // Add uncertainty indicator
  g.append("text")
    .attr("x", innerWidth)
    .attr("y", 0)
    .attr("text-anchor", "end")
    .attr("font-weight", "bold")
    .text(`不確実性: ${Math.round(data.uncertainty * 100)}%`);
}
```

### 2. 多次元レーダーチャート

多次元レーダーチャートは、確信度の複数の次元を同時に可視化するための効果的な手法です。

#### 実装方法

```javascript
// n8n workflow: Multidimensional Confidence Radar Chart
// Function node for generating radar chart data
[
  {
    "id": "generateRadarChartData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Confidence metrics for each perspective
        const confidenceMetrics = $input.item.json.confidence_metrics || {
          technology: {
            information_quantity: 0.8,
            information_quality: 0.7,
            coherence: 0.9,
            expertise: 0.6
          },
          market: {
            information_quantity: 0.6,
            information_quality: 0.8,
            coherence: 0.7,
            expertise: 0.9
          },
          business: {
            information_quantity: 0.7,
            information_quality: 0.6,
            coherence: 0.8,
            expertise: 0.7
          }
        };
        
        // Prepare radar chart data
        const radarData = {
          labels: ['情報量', '情報質', '整合性', '専門性'],
          datasets: [
            {
              label: 'テクノロジー視点',
              data: [
                confidenceMetrics.technology.information_quantity,
                confidenceMetrics.technology.information_quality,
                confidenceMetrics.technology.coherence,
                confidenceMetrics.technology.expertise
              ]
            },
            {
              label: 'マーケット視点',
              data: [
                confidenceMetrics.market.information_quantity,
                confidenceMetrics.market.information_quality,
                confidenceMetrics.market.coherence,
                confidenceMetrics.market.expertise
              ]
            },
            {
              label: 'ビジネス視点',
              data: [
                confidenceMetrics.business.information_quantity,
                confidenceMetrics.business.information_quality,
                confidenceMetrics.business.coherence,
                confidenceMetrics.business.expertise
              ]
            }
          ]
        };
        
        return {
          json: {
            radar_data: radarData,
            overall_confidence: {
              technology: calculateOverallConfidence(confidenceMetrics.technology),
              market: calculateOverallConfidence(confidenceMetrics.market),
              business: calculateOverallConfidence(confidenceMetrics.business)
            }
          }
        };
        
        // Helper function: Calculate overall confidence
        function calculateOverallConfidence(metrics) {
          // Weights for each dimension
          const weights = {
            information_quantity: 0.25,
            information_quality: 0.3,
            coherence: 0.25,
            expertise: 0.2
          };
          
          // Calculate weighted average
          return Object.keys(weights).reduce((sum, key) => {
            return sum + metrics[key] * weights[key];
          }, 0);
        }
      `
    }
  }
]
```

#### フロントエンド実装（Chart.js）

```javascript
// Chart.js implementation for radar chart visualization
function renderConfidenceRadarChart(data, containerId) {
  // Create canvas element
  const canvas = document.createElement('canvas');
  document.getElementById(containerId).appendChild(canvas);
  
  // Define colors
  const colors = {
    technology: {
      background: 'rgba(54, 162, 235, 0.2)',
      border: 'rgba(54, 162, 235, 1)'
    },
    market: {
      background: 'rgba(255, 99, 132, 0.2)',
      border: 'rgba(255, 99, 132, 1)'
    },
    business: {
      background: 'rgba(75, 192, 192, 0.2)',
      border: 'rgba(75, 192, 192, 1)'
    }
  };
  
  // Apply colors to datasets
  data.radar_data.datasets.forEach((dataset, index) => {
    const perspective = ['technology', 'market', 'business'][index];
    dataset.backgroundColor = colors[perspective].background;
    dataset.borderColor = colors[perspective].border;
    dataset.pointBackgroundColor = colors[perspective].border;
    dataset.pointBorderColor = '#fff';
    dataset.pointHoverBackgroundColor = '#fff';
    dataset.pointHoverBorderColor = colors[perspective].border;
  });
  
  // Create chart
  new Chart(canvas, {
    type: 'radar',
    data: data.radar_data,
    options: {
      scales: {
        r: {
          angleLines: {
            display: true
          },
          suggestedMin: 0,
          suggestedMax: 1
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.dataset.label || '';
              const value = context.raw;
              return `${label}: ${Math.round(value * 100)}%`;
            }
          }
        },
        legend: {
          position: 'bottom'
        }
      }
    }
  });
  
  // Add overall confidence indicators
  const overallContainer = document.createElement('div');
  overallContainer.className = 'overall-confidence-container';
  overallContainer.style.display = 'flex';
  overallContainer.style.justifyContent = 'space-around';
  overallContainer.style.marginTop = '20px';
  
  Object.entries(data.overall_confidence).forEach(([perspective, value]) => {
    const perspectiveNames = {
      technology: 'テクノロジー',
      market: 'マーケット',
      business: 'ビジネス'
    };
    
    const indicator = document.createElement('div');
    indicator.className = 'confidence-indicator';
    indicator.style.textAlign = 'center';
    
    const label = document.createElement('div');
    label.textContent = `${perspectiveNames[perspective]}視点の総合確信度`;
    
    const valueElement = document.createElement('div');
    valueElement.textContent = `${Math.round(value * 100)}%`;
    valueElement.style.fontSize = '24px';
    valueElement.style.fontWeight = 'bold';
    valueElement.style.color = colors[perspective].border;
    
    indicator.appendChild(label);
    indicator.appendChild(valueElement);
    overallContainer.appendChild(indicator);
  });
  
  document.getElementById(containerId).appendChild(overallContainer);
}
```

### 3. 確信度ヒートマップ

確信度ヒートマップは、複数の要素や時間的変化における確信度の分布を可視化するための効果的な手法です。

#### 実装方法

```javascript
// n8n workflow: Confidence Heatmap
// Function node for generating heatmap data
[
  {
    "id": "generateHeatmapData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Topic data with confidence values over time
        const topicData = $input.item.json.topic_data || {
          id: 'topic-001',
          name: 'AI自動運転技術',
          perspectives: ['technology', 'market', 'business'],
          dates: ['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01'],
          confidence_values: {
            technology: [0.7, 0.75, 0.8, 0.85, 0.9, 0.85],
            market: [0.5, 0.55, 0.6, 0.7, 0.75, 0.8],
            business: [0.4, 0.45, 0.5, 0.6, 0.7, 0.75]
          }
        };
        
        // Prepare heatmap data
        const heatmapData = [];
        
        topicData.perspectives.forEach(perspective => {
          topicData.dates.forEach((date, index) => {
            heatmapData.push({
              perspective,
              date,
              confidence: topicData.confidence_values[perspective][index]
            });
          });
        });
        
        return {
          json: {
            topic_id: topicData.id,
            topic_name: topicData.name,
            perspectives: topicData.perspectives,
            dates: topicData.dates,
            heatmap_data: heatmapData
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（D3.js）

```javascript
// D3.js implementation for confidence heatmap visualization
function renderConfidenceHeatmap(data, containerId) {
  // Clear previous content
  d3.select(`#${containerId}`).html("");
  
  // Set dimensions
  const width = 800;
  const height = 200;
  const margin = { top: 30, right: 30, bottom: 50, left: 120 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Create SVG
  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  
  // Create group for the visualization
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // Define perspective names
  const perspectiveNames = {
    technology: 'テクノロジー視点',
    market: 'マーケット視点',
    business: 'ビジネス視点'
  };
  
  // Create scales
  const xScale = d3.scaleBand()
    .domain(data.dates)
    .range([0, innerWidth])
    .padding(0.05);
  
  const yScale = d3.scaleBand()
    .domain(data.perspectives)
    .range([0, innerHeight])
    .padding(0.05);
  
  const colorScale = d3.scaleSequential()
    .domain([0, 1])
    .interpolator(d3.interpolateViridis);
  
  // Draw heatmap cells
  g.selectAll("rect")
    .data(data.heatmap_data)
    .enter()
    .append("rect")
    .attr("x", d => xScale(d.date))
    .attr("y", d => yScale(d.perspective))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colorScale(d.confidence))
    .attr("stroke", "white")
    .attr("stroke-width", 1)
    .append("title")
    .text(d => `${perspectiveNames[d.perspective]}\n日付: ${d.date}\n確信度: ${Math.round(d.confidence * 100)}%`);
  
  // Add confidence values
  g.selectAll("text")
    .data(data.heatmap_data)
    .enter()
    .append("text")
    .attr("x", d => xScale(d.date) + xScale.bandwidth() / 2)
    .attr("y", d => yScale(d.perspective) + yScale.bandwidth() / 2)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .attr("fill", d => d.confidence > 0.5 ? "white" : "black")
    .text(d => `${Math.round(d.confidence * 100)}%`);
  
  // Add axes
  const xAxis = d3.axisBottom(xScale);
  const yAxis = d3.axisLeft(yScale)
    .tickFormat(d => perspectiveNames[d]);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(xAxis)
    .selectAll("text")
    .attr("transform", "rotate(-45)")
    .attr("text-anchor", "end");
  
  g.append("g")
    .call(yAxis);
  
  // Add title
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", margin.top / 2)
    .attr("text-anchor", "middle")
    .attr("font-weight", "bold")
    .text(`「${data.topic_name}」の確信度推移`);
  
  // Add color legend
  const legendWidth = 200;
  const legendHeight = 20;
  
  const legendX = width - margin.right - legendWidth;
  const legendY = height - margin.bottom + 30;
  
  const legendScale = d3.scaleLinear()
    .domain([0, 1])
    .range([0, legendWidth]);
  
  const legendAxis = d3.axisBottom(legendScale)
    .tickFormat(d => `${d * 100}%`);
  
  const defs = svg.append("defs");
  
  const linearGradient = defs.append("linearGradient")
    .attr("id", "confidence-gradient")
    .attr("x1", "0%")
    .attr("y1", "0%")
    .attr("x2", "100%")
    .attr("y2", "0%");
  
  linearGradient.selectAll("stop")
    .data(d3.range(0, 1.1, 0.1))
    .enter()
    .append("stop")
    .attr("offset", d => `${d * 100}%`)
    .attr("stop-color", d => colorScale(d));
  
  svg.append("rect")
    .attr("x", legendX)
    .attr("y", legendY)
    .attr("width", legendWidth)
    .attr("height", legendHeight)
    .style("fill", "url(#confidence-gradient)");
  
  svg.append("g")
    .attr("transform", `translate(${legendX},${legendY + legendHeight})`)
    .call(legendAxis);
  
  svg.append("text")
    .attr("x", legendX)
    .attr("y", legendY - 5)
    .attr("text-anchor", "start")
    .text("確信度");
}
```

### 4. 確信度バッジとインジケーター

確信度バッジとインジケーターは、ダッシュボード全体で一貫した確信度表現を提供するための簡潔な視覚要素です。

#### 実装方法

```javascript
// n8n workflow: Confidence Badge Generator
// Function node for generating badge data
[
  {
    "id": "generateBadgeData",
    "type": "n8n-nodes-base.function",
    "parameters": {
      "functionCode": `
        // Input: Confidence value
        const confidence = $input.item.json.confidence || 0.7;
        
        // Determine badge level and color
        let level, color, textColor;
        
        if (confidence >= 0.8) {
          level = '高';
          color = '#4caf50'; // Green
          textColor = 'white';
        } else if (confidence >= 0.6) {
          level = '中';
          color = '#ff9800'; // Orange
          textColor = 'black';
        } else {
          level = '低';
          color = '#f44336'; // Red
          textColor = 'white';
        }
        
        return {
          json: {
            confidence,
            badge: {
              level,
              color,
              textColor,
              percentage: Math.round(confidence * 100)
            }
          }
        };
      `
    }
  }
]
```

#### フロントエンド実装（HTML/CSS/JavaScript）

```javascript
// HTML/CSS/JavaScript implementation for confidence badges
function renderConfidenceBadge(data, containerId) {
  // Create badge element
  const badge = document.createElement('div');
  badge.className = 'confidence-badge';
  badge.style.display = 'inline-block';
  badge.style.padding = '4px 8px';
  badge.style.borderRadius = '12px';
  badge.style.backgroundColor = data.badge.color;
  badge.style.color = data.badge.textColor;
  badge.style.fontWeight = 'bold';
  badge.style.fontSize = '14px';
  
  badge.textContent = `確信度: ${data.badge.level} (${data.badge.percentage}%)`;
  
  // Add tooltip
  badge.title = `確信度スコア: ${data.badge.percentage}%`;
  
  // Add to container
  document.getElementById(containerId).appendChild(badge);
  
  // Add interactive features
  badge.addEventListener('mouseover', () => {
    badge.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
  });
  
  badge.addEventListener('mouseout', () => {
    badge.style.boxShadow = 'none';
  });
  
  badge.addEventListener('click', () => {
    // Show detailed confidence information
    showConfidenceDetails(data, containerId);
  });
}

// Function to show detailed confidence information
function showConfidenceDetails(data, containerId) {
  // Create modal or expand details
  const detailsContainer = document.createElement('div');
  detailsContainer.className = 'confidence-details';
  detailsContainer.style.marginTop = '10px';
  detailsContainer.style.padding = '10px';
  detailsContainer.style.border = `1px solid ${data.badge.color}`;
  detailsContainer.style.borderRadius = '5px';
  detailsContainer.style.backgroundColor = '#f9f9f9';
  
  // Add confidence meter
  const meter = document.createElement('div');
  meter.className = 'confidence-meter';
  meter.style.height = '10px';
  meter.style.width = '100%';
  meter.style.backgroundColor = '#e0e0e0';
  meter.style.borderRadius = '5px';
  meter.style.overflow = 'hidden';
  meter.style.marginBottom = '10px';
  
  const fill = document.createElement('div');
  fill.style.height = '100%';
  fill.style.width = `${data.badge.percentage}%`;
  fill.style.backgroundColor = data.badge.color;
  
  meter.appendChild(fill);
  detailsContainer.appendChild(meter);
  
  // Add confidence description
  const description = document.createElement('p');
  description.style.margin = '5px 0';
  description.style.fontSize = '14px';
  
  let descriptionText;
  if (data.badge.level === '高') {
    descriptionText = '高い確信度: 十分な情報に基づく信頼性の高い結果です。';
  } else if (data.badge.level === '中') {
    descriptionText = '中程度の確信度: ある程度の情報に基づく結果ですが、追加情報があるとより確実になります。';
  } else {
    descriptionText = '低い確信度: 限られた情報に基づく暫定的な結果です。追加情報の収集が強く推奨されます。';
  }
  
  description.textContent = descriptionText;
  detailsContainer.appendChild(description);
  
  // Add close button
  const closeButton = document.createElement('button');
  closeButton.textContent = '閉じる';
  closeButton.style.marginTop = '10px';
  closeButton.style.padding = '5px 10px';
  closeButton.style.border = 'none';
  closeButton.style.borderRadius = '3px';
  closeButton.style.backgroundColor = '#e0e0e0';
  closeButton.style.cursor = 'pointer';
  
  closeButton.addEventListener('click', () => {
    detailsContainer.remove();
  });
  
  detailsContainer.appendChild(closeButton);
  
  // Add to container
  const container = document.getElementById(containerId);
  
  // Remove existing details if any
  const existingDetails = container.querySelector('.confidence-details');
  if (existingDetails) {
    existingDetails.remove();
  }
  
  container.appendChild(detailsContainer);
}
```

## 確信度表現の統合

上記の視覚的表現手法を組み合わせることで、確信度の厳密な評価と効果的な表現が可能になります。以下に、これらの手法を統合したダッシュボードの例を示します。

### 統合ダッシュボードの構成

1. **トップレベル表示**
   - 確信度バッジ（簡潔な概要）
   - 総合確信度スコア

2. **詳細表示**
   - 信頼区間と確率分布（定量的な不確実性）
   - 多次元レーダーチャート（次元別の確信度）
   - 確信度ヒートマップ（時間的変化と視点別の確信度）

3. **インタラクティブ要素**
   - 確信度の詳細情報の展開/折りたたみ
   - 時間範囲の選択
   - 視点のフィルタリング

### 実装例（React）

```jsx
// React component for integrated confidence visualization
function ConfidenceVisualization({ topicId, date }) {
  const [confidenceData, setConfidenceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showDetails, setShowDetails] = useState(false);
  
  useEffect(() => {
    // Fetch confidence data
    async function fetchData() {
      try {
        setLoading(true);
        
        // In a real implementation, this would be an API call
        const response = await fetch(`/api/confidence?topic_id=${topicId}&date=${date}`);
        const data = await response.json();
        
        setConfidenceData(data);
      } catch (error) {
        console.error('Error fetching confidence data:', error);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, [topicId, date]);
  
  if (loading) {
    return <div>Loading confidence data...</div>;
  }
  
  if (!confidenceData) {
    return <div>No confidence data available</div>;
  }
  
  return (
    <div className="confidence-visualization">
      <div className="confidence-summary">
        <h3>確信度サマリー</h3>
        <div className="confidence-badge-container">
          {Object.entries(confidenceData.overall_confidence).map(([perspective, value]) => (
            <div key={perspective} className="perspective-badge">
              <span className="perspective-name">
                {perspective === 'technology' ? 'テクノロジー' : 
                 perspective === 'market' ? 'マーケット' : 'ビジネス'}:
              </span>
              <ConfidenceBadge confidence={value} />
            </div>
          ))}
        </div>
        
        <button 
          className="details-toggle"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? '詳細を隠す' : '詳細を表示'}
        </button>
      </div>
      
      {showDetails && (
        <div className="confidence-details">
          <div className="visualization-row">
            <div className="visualization-card">
              <h4>確信度分布</h4>
              <ConfidenceDistribution 
                data={confidenceData.confidence_distribution} 
              />
            </div>
            
            <div className="visualization-card">
              <h4>次元別確信度</h4>
              <ConfidenceRadarChart 
                data={confidenceData.radar_data} 
              />
            </div>
          </div>
          
          <div className="visualization-card full-width">
            <h4>確信度の時間的推移</h4>
            <ConfidenceHeatmap 
              data={confidenceData.heatmap_data} 
            />
          </div>
          
          <div className="information-imbalance">
            <h4>情報不均衡の検出</h4>
            {confidenceData.detected_imbalances.length > 0 ? (
              <div className="imbalance-warnings">
                <p>以下の情報不均衡が検出されました：</p>
                <ul>
                  {confidenceData.detected_imbalances.map((imbalance, index) => (
                    <li key={index} className={`severity-${imbalance.severity}`}>
                      {imbalance.description}
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p>重大な情報不均衡は検出されていません。</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// Confidence Badge component
function ConfidenceBadge({ confidence }) {
  let level, color, textColor;
  
  if (confidence >= 0.8) {
    level = '高';
    color = '#4caf50';
    textColor = 'white';
  } else if (confidence >= 0.6) {
    level = '中';
    color = '#ff9800';
    textColor = 'black';
  } else {
    level = '低';
    color = '#f44336';
    textColor = 'white';
  }
  
  return (
    <span 
      className="confidence-badge"
      style={{ 
        backgroundColor: color, 
        color: textColor,
        padding: '3px 8px',
        borderRadius: '12px',
        fontWeight: 'bold',
        fontSize: '14px',
        marginLeft: '5px'
      }}
    >
      {level} ({Math.round(confidence * 100)}%)
    </span>
  );
}
```

## 確信度表現のベストプラクティス

確信度の視覚的表現を効果的に実装するためのベストプラクティスを以下に示します：

### 1. 一貫性の確保

- ダッシュボード全体で一貫した色とスタイルを使用
- 確信度レベルの定義と表現を統一
- 同じ種類の情報には同じ視覚化手法を適用

### 2. 直感的な理解の促進

- 色による直感的な確信度レベルの表現（例：赤=低、黄=中、緑=高）
- 数値と視覚要素の組み合わせによる多層的な理解の促進
- ツールチップや補足説明による詳細情報の提供

### 3. コンテキストの提供

- 確信度の評価基準を明示
- 情報不均衡との関連性を示す
- 過去の確信度との比較を可能にする

### 4. インタラクティブ性の活用

- 詳細情報の展開/折りたたみ機能
- 時間範囲や視点のフィルタリング
- ドリルダウンによる詳細分析の提供

### 5. アクセシビリティの確保

- 色だけに依存しない情報伝達
- スクリーンリーダー対応
- キーボードナビゲーションのサポート

## まとめ

本セクションでは、トリプルパースペクティブ型戦略AIレーダーにおける確信度の視覚的表現について詳細に解説しました。信頼区間と確率分布、多次元レーダーチャート、確信度ヒートマップ、確信度バッジとインジケーターなど、様々な視覚化手法を紹介し、それらの実装方法を示しました。

これらの手法を組み合わせることで、確信度の厳密な評価と効果的な表現が可能になり、ユーザーは結果の信頼性を正確に理解し、より適切な判断を下すことができます。特に情報不均衡が存在する状況では、確信度の適切な表現が意思決定の質を大きく左右します。

次のセクションでは、代替シナリオの可視化について詳細に解説します。
