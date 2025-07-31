document.addEventListener("DOMContentLoaded", () => {
  loadAllData();

  // 支出フォームの登録イベント
  document
    .getElementById("expense-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      await submitForm("/expense", e.target);
      loadAllData(); // 登録後に一覧＆グラフ更新
    });

  // 収入フォームの登録イベント
  document
    .getElementById("income-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      await submitForm("/income", e.target);
      loadAllData(); // 登録後に一覧＆グラフ更新
    });
});

async function submitForm(url, form) {
  const data = Object.fromEntries(new FormData(form).entries());
  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  form.reset();
}

async function loadAllData() {
  await loadExpenseList();
  await loadIncomeList();
  await loadCharts();
}

function renderTable(data, isExpense = true) {
  return data
    .map(
      (row) => `
      <tr>
        <td>${row.date}</td>
        <td>${row.category}</td>
        ${isExpense ? `<td>${row.shop || "-"}</td>` : ""}
        <td>${row.amount.toLocaleString()}円</td>
        ${isExpense ? `<td>${row.payment}</td>` : ""}
      </tr>
    `
    )
    .join("");
}

async function loadExpenseList() {
  const res = await fetch("/expense");
  const data = await res.json();
  document.querySelector("#expense-list tbody").innerHTML = renderTable(
    data,
    true
  );
}

async function loadIncomeList() {
  const res = await fetch("/income");
  const data = await res.json();
  document.querySelector("#income-list tbody").innerHTML = renderTable(
    data,
    false
  );
}

async function loadCharts() {
  // カテゴリ別支出
  const res = await fetch("/expense/summary/category");
  const expenseSummary = await res.json();
  drawExpenseChart(expenseSummary);

  // 収支比較
  drawMonthlyComparisonChart();
  drawAssetTrendChart();
}

let expenseChartInstance;
function drawExpenseChart(summary) {
  const ctx = document.getElementById("expense-chart");
  if (expenseChartInstance) expenseChartInstance.destroy();
  expenseChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: summary.map((s) => s.category),
      datasets: [
        {
          data: summary.map((s) => s.total),
          backgroundColor: ["#f87171", "#60a5fa", "#34d399", "#fbbf24"],
        },
      ],
    },
  });
}

let summaryChartInstance;
function drawSummaryChart(data) {
  const ctx = document.getElementById("summary-chart");
  if (summaryChartInstance) summaryChartInstance.destroy();
  summaryChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["収入", "支出"],
      datasets: [
        {
          data: [data.total_income, data.total_expense],
          backgroundColor: ["#4ade80", "#f87171"],
        },
      ],
    },
  });
}

document.getElementById("filter-btn").addEventListener("click", async () => {
  const start = document.getElementById("start-date").value;
  const end = document.getElementById("end-date").value;

  updateExpenseList(start, end);
  updateIncomeList(start, end);
  updateexpenseChartInstance(start, end);
});

async function updateIncomeList(start, end) {
  let url = "/income";
  const params = [];
  if (start) params.push(`start=${start}`);
  if (end) params.push(`end=${end}`);
  if (params.length > 0) url += "?" + params.join("&");

  const res = await fetch(url);
  const data = await res.json();
  document.querySelector("#income-list tbody").innerHTML = renderTable(
    data,
    false
  );
}

async function updateExpenseList(start, end) {
  let url = "/expense";
  const params = [];
  if (start) params.push(`start=${start}`);
  if (end) params.push(`end=${end}`);
  if (params.length > 0) url += "?" + params.join("&");

  const res = await fetch(url);
  const data = await res.json();
  document.querySelector("#expense-list tbody").innerHTML = renderTable(
    data,
    true
  );
}

async function fetchExpenseSummaryByCategory(start, end) {
  const params = new URLSearchParams();
  if (start) params.append("start", start);
  if (end) params.append("end", end);

  const res = await fetch(`/expense/summary/category?${params.toString()}`);
  return await res.json();
}

async function updateexpenseChartInstance(start, end) {
  const data = await fetchExpenseSummaryByCategory(start, end);

  const labels = data.map((item) => item.category);
  const amounts = data.map((item) => item.total);

  if (expenseChartInstance) {
    expenseChartInstance.destroy();
  }

  const ctx = document.getElementById("expense-chart").getContext("2d");
  expenseChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "カテゴリ別支出",
          data: amounts,
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F49",
          ],
        },
      ],
    },
  });
}

// sankeyデータを取得して描画
function drawSankeyChart() {
  fetch("/sankey-data")
    .then((response) => response.json())
    .then((data) => {
      const nodes = data.nodes;
      const links = data.links;

      // Google Charts 用のデータを整形
      const chartData = new google.visualization.DataTable();
      chartData.addColumn("string", "From");
      chartData.addColumn("string", "To");
      chartData.addColumn("number", "Amount");

      const rows = links.map((link) => [
        nodes[link.source],
        nodes[link.target],
        link.value,
      ]);

      chartData.addRows(rows);

      const chart = new google.visualization.Sankey(
        document.getElementById("sankey-chart")
      );
      chart.draw(chartData, {});
    })
    .catch((error) => {
      console.error("Error loading sankey data:", error);
    });
}

async function drawMonthlyComparisonChart() {
  const response = await fetch("/monthly-summary");
  const data = await response.json();

  const labels = Object.keys(data);
  const incomeData = labels.map((month) => data[month].income || 0);
  const expenseData = labels.map((month) => data[month].expense || 0);

  const ctx = document
    .getElementById("monthly-comparison-chart")
    .getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "収入",
          data: incomeData,
          backgroundColor: "rgba(75, 192, 192, 0.7)",
        },
        {
          label: "支出",
          data: expenseData,
          backgroundColor: "rgba(255, 99, 132, 0.7)",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "月別 収支比較" },
      },
    },
  });
}

async function drawAssetTrendChart() {
  const response = await fetch("/asset-trend");
  const data = await response.json();

  const labels = data.map((item) => item.month);
  const values = data.map((item) => item.total);

  const ctx = document.getElementById("asset-trend-chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "資産推移",
          data: values,
          borderColor: "rgba(54, 162, 235,1)",
          backgroundColor: "rgba(64, 162, 235, 0.1)",
          fill: true,
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "資産の推移" },
      },
      scales: {
        y: { beginAtZero: true },
      },
    },
  });
}
