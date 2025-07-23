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
        ${isExpense ? `<td>${row.payment}</td>` : `<td>${row.memo || "-"}</td>`}
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
  const res2 = await fetch("/summary/income_vs_expense");
  const summaryData = await res2.json();
  drawSummaryChart(summaryData);
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
