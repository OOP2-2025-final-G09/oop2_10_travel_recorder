// static/dashboard.js

// ダッシュボードのグラフ描画
// 担当C: このファイルを実装

// 1. 利用年齢層 - 棒グラフ（/api/age_distribution）
// 2. 人気の旅行先 - 円グラフ（/api/popular_places）
// 3. 利用が多かった日 - 棒グラフ（TODO）

let ageChartInstance = null;
let placeChartInstance = null;

// ---------- 共通：API 呼び出し ----------

async function fetchAgeDistribution() {
  try {
    const res = await fetch('/api/age_distribution');
    if (!res.ok) {
      console.error('年齢分布の取得に失敗しました:', res.status, res.statusText);
      return null;
    }
    // 例: { "20": 2, "30": 1 }
    return await res.json();
  } catch (err) {
    console.error('年齢分布の取得中にエラーが発生しました:', err);
    return null;
  }
}

async function fetchPopularPlaces() {
  try {
    const res = await fetch('/api/popular_places');
    if (!res.ok) {
      console.error('人気の旅行先の取得に失敗しました:', res.status, res.statusText);
      return null;
    }
    // 例: { "沖縄": 2, "北海道": 1 }
    return await res.json();
  } catch (err) {
    console.error('人気の旅行先の取得中にエラーが発生しました:', err);
    return null;
  }
}

// ---------- 利用年齢層（棒グラフ） ----------

function renderAgeChart(ageDist) {
  const canvas = document.getElementById('ageChart');
  if (!canvas) {
    console.error('ageChart 用の <canvas id="ageChart"> が見つかりません。');
    return;
  }

  // ageDist = { "20": 2, "30": 1, ... }
  const sortedDecades = Object.keys(ageDist)
    .map((k) => parseInt(k, 10))
    .sort((a, b) => a - b);

  const labels = sortedDecades.map((d) => `${d}代`);
  const values = sortedDecades.map((d) => ageDist[d]);

  if (ageChartInstance) {
    ageChartInstance.destroy();
  }

  ageChartInstance = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'ユーザー数',
          data: values,
          backgroundColor: 'rgba(54, 162, 235, 0.8)',
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 },
          title: {
            display: true,
            text: '人数'
          }
        },
        x: {
          title: {
            display: true,
            text: '年齢層'
          }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.parsed.y}人`
          }
        }
      }
    }
  });
}

// ---------- 人気の旅行先（円グラフ） ----------

function renderPopularPlacesChart(placeDist) {
  const canvas = document.getElementById('placeChart');
  if (!canvas) {
    console.error('placeChart 用の <canvas id="placeChart"> が見つかりません。');
    return;
  }

  // placeDist = { "沖縄": 2, "北海道": 1, ... }
  const labels = Object.keys(placeDist);
  const values = Object.values(placeDist);
  const total = values.reduce((sum, v) => sum + v, 0);

  // 色はとりあえず数パターン用意してローテーション
  const baseColors = [
    'rgba(54, 162, 235, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(255, 99, 132, 0.8)'
  ];
  const bgColors = labels.map((_, idx) => baseColors[idx % baseColors.length]);

  if (placeChartInstance) {
    placeChartInstance.destroy();
  }

  placeChartInstance = new Chart(canvas, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [
        {
          data: values,
          backgroundColor: bgColors,
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right'
        },
        tooltip: {
          callbacks: {
            // ツールチップに「沖縄 67% (2件)」みたいに表示
            label: (ctx) => {
              const label = ctx.label || '';
              const value = ctx.parsed;
              const percent = total ? Math.round((value / total) * 100) : 0;
              return `${label} ${percent}% (${value}件)`;
            }
          }
        }
      }
    }
  });
}

// ---------- 初期化 ----------

async function initDashboard() {
  const [ageDist, placeDist] = await Promise.all([
    fetchAgeDistribution(),
    fetchPopularPlaces()
  ]);

  if (ageDist) {
    renderAgeChart(ageDist);
  }
  if (placeDist) {
    renderPopularPlacesChart(placeDist);
  }

  // TODO: /api/busy_dates を使った棒グラフもここで呼ぶ
}

document.addEventListener('DOMContentLoaded', initDashboard);
