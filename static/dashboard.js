// static/dashboard.js

// ダッシュボードのグラフ描画
// 担当C: このファイルを実装

// Chart.jsを使って3つのグラフを描画する予定
// 1. 利用年齢層 - 棒グラフ（★今はこれだけ実装）
// 2. 人気の旅行先 - 円グラフ
// 3. 利用が多かった日 - 棒グラフ

let ageChartInstance = null; // 再描画用に保持

// 年齢分布データを API から取得
async function fetchAgeDistribution() {
  try {
    const res = await fetch('/api/age_distribution');

    if (!res.ok) {
      console.error('年齢分布の取得に失敗しました:', res.status, res.statusText);
      return null;
    }

    // 例: { "20": 2, "30": 1 }
    const json = await res.json();
    return json;
  } catch (err) {
    console.error('年齢分布の取得中にエラーが発生しました:', err);
    return null;
  }
}

// 「利用年齢層」グラフを描画
function renderAgeChart(ageDist) {
  const canvas = document.getElementById('ageChart');
  if (!canvas) {
    console.error('ageChart 用の <canvas id="ageChart"> が見つかりません。');
    return;
  }

  // ageDist = { "20": 2, "30": 1, ... }
  // キーを数値としてソートしてからラベル・値を作る
  const sortedDecades = Object.keys(ageDist)
    .map((k) => parseInt(k, 10))
    .sort((a, b) => a - b);

  const labels = sortedDecades.map((d) => `${d}代`);
  const values = sortedDecades.map((d) => ageDist[d]);

  // 既存チャートがあれば破棄
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
          backgroundColor: 'rgba(54, 162, 235, 0.8)', // 色はお好みで
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // 親コンテナに合わせたいとき便利
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0, // 1, 2, 3…みたいに整数で表示
          },
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
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.parsed.y}人`,
          },
        },
      },
    },
  });
}

// ページ読み込み時に初期化
async function initDashboard() {
  const ageDist = await fetchAgeDistribution();
  if (ageDist) {
    renderAgeChart(ageDist);
  }
  // TODO: popular_places / busy_dates もここから呼び出す
}

document.addEventListener('DOMContentLoaded', initDashboard);
