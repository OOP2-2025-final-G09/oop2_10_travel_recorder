// static/dashboard.js

// ダッシュボードのグラフ描画
// 1. 利用年齢層       /api/age_distribution   → ageChart（棒グラフ）
// 2. 人気の旅行先     /api/popular_places     → placeChart（円グラフ）
// 3. 利用が多かった日 /api/busy_dates         → dateChart（棒グラフ）

let ageChartInstance = null;
let placeChartInstance = null;
let dateChartInstance = null;

// ---------- API 呼び出し ----------

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
    // 例: { "沖縄": 3, "北海道": 2 }
    return await res.json();
  } catch (err) {
    console.error('人気の旅行先の取得中にエラーが発生しました:', err);
    return null;
  }
}

async function fetchBusyDates() {
  try {
    const res = await fetch('/api/busy_dates');
    if (!res.ok) {
      console.error('利用が多い日の取得に失敗しました:', res.status, res.statusText);
      return null;
    }
    // dashboard.py の実装より:
    // 例: { "2025/01/04": 2, "2025/01/15": 1, ... } （件数の多い順 上位10件）
    return await res.json();
  } catch (err) {
    console.error('利用が多い日の取得中にエラーが発生しました:', err);
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
      labels,
      datasets: [
        {
          label: 'ユーザー数',
          data: values,
          backgroundColor: 'rgba(54, 162, 235, 0.8)',
          borderWidth: 0,
        },
      ],
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
            text: '人数',
          },
        },
        x: {
          title: {
            display: true,
            text: '年齢層',
          },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.parsed.y}人`,
          },
        },
      },
    },
  });
}

// ---------- 人気の旅行先（円グラフ） ----------

function renderPopularPlacesChart(placeDist) {
  const canvas = document.getElementById('placeChart');
  if (!canvas) {
    console.error('placeChart 用の <canvas id="placeChart"> が見つかりません。');
    return;
  }

  const labels = Object.keys(placeDist);
  const values = Object.values(placeDist);
  const total = values.reduce((sum, v) => sum + v, 0);

  const baseColors = [
    'rgba(54, 162, 235, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(255, 99, 132, 0.8)',
  ];
  const bgColors = labels.map((_, idx) => baseColors[idx % baseColors.length]);

  if (placeChartInstance) {
    placeChartInstance.destroy();
  }

  placeChartInstance = new Chart(canvas, {
    type: 'pie',
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: bgColors,
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
        },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const label = ctx.label || '';
              const value = ctx.parsed;
              const percent = total ? Math.round((value / total) * 100) : 0;
              return `${label} ${percent}% (${value}件)`;
            },
          },
        },
      },
    },
  });
}

// ---------- 利用が多かった日（棒グラフ） ----------

function renderBusyDatesChart(dateDist) {
  const canvas = document.getElementById('dateChart');
  if (!canvas) {
    console.error('dateChart 用の <canvas id="dateChart"> が見つかりません。');
    return;
  }

  // dateDist = { "2025/01/04": 2, "2025/01/15": 1, ... }
  // dashboard.py 側ですでに「件数の多い順 上位10件」にソート済み
  const labels = Object.keys(dateDist);
  const values = Object.values(dateDist);

  if (dateChartInstance) {
    dateChartInstance.destroy();
  }

  dateChartInstance = new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: '予約件数',
          data: values,
          backgroundColor: 'rgba(255, 159, 64, 0.8)', // 目立つ色
          borderWidth: 0,
        },
      ],
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
            text: '件数',
          },
        },
        x: {
          title: {
            display: true,
            text: '日付',
          },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.parsed.y}件`,
          },
        },
      },
    },
  });
}

// ---------- 初期化 ----------

async function initDashboard() {
  const [ageDist, placeDist, dateDist] = await Promise.all([
    fetchAgeDistribution(),
    fetchPopularPlaces(),
    fetchBusyDates(),
  ]);

  if (ageDist) {
    renderAgeChart(ageDist);
  }
  if (placeDist) {
    renderPopularPlacesChart(placeDist);
  }
  if (dateDist) {
    renderBusyDatesChart(dateDist);
  }
}

document.addEventListener('DOMContentLoaded', initDashboard);
