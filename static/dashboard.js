// ダッシュボードのグラフ描画
// 担当C: このファイルを実装

// Chart.jsを使って3つのグラフを描画する
// 1. 利用年齢層 - 棒グラフ
// 2. 人気の旅行先 - 円グラフ
// 3. 利用が多かった日 - 棒グラフ

// TODO: Chart.jsのCDNをindex.htmlに追加
// TODO: 各グラフの描画関数を実装
// TODO: APIからデータを取得してグラフに反映

// 例:
// fetch('/api/age_distribution')
//   .then(response => response.json())
//   .then(data => {
//     // Chart.jsで棒グラフを描画
//   });

document.addEventListener("DOMContentLoaded", () => {

    /* ===== 利用年齢層（棒グラフ） ===== */
    const ageCtx = document.getElementById("ageChart");
    if (ageCtx) {
        new Chart(ageCtx, {
            type: "bar",
            data: {
                labels: ["10代", "20代", "30代", "40代", "50代以上"],
                datasets: [{
                    label: "利用者数",
                    data: [5, 18, 25, 14, 8],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "人数"
                        }
                    }
                }
            }
        });
    }

    /* ===== 人気の旅行先（円グラフ） ===== */
    const placeCtx = document.getElementById("placeChart");
    if (placeCtx) {
        new Chart(placeCtx, {
            type: "pie",
            data: {
                labels: ["北海道", "東京", "沖縄", "大阪"],
                datasets: [{
                    data: [12, 20, 9, 7],
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    /* ===== 利用が多かった日（棒グラフ） ===== */
    const dateCtx = document.getElementById("dateChart");
    if (dateCtx) {
        new Chart(dateCtx, {
            type: "bar",
            data: {
                labels: ["月", "火", "水", "木", "金", "土", "日"],
                datasets: [{
                    label: "予約数",
                    data: [3, 6, 4, 5, 8, 12, 10],
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "件数"
                        }
                    }
                }
            }
        });
    }

});
