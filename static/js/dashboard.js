// Global refs for chart instances to destroy them before re-render if needed
let monthlyChartInstance = null;
let categoryChartInstance = null;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const stats = await apiFetch('/dashboard/stats');
        
        if (stats) {
            renderKPIs(stats);
            renderMonthlyChart(stats.monthly_chart);
            renderCategoryChart(stats.category_chart);
            renderAlerts(stats.budget_warnings);
        }
    } catch (e) {
        console.error('Failed to load dashboard stats', e);
    }
});

function formatCurrency(num) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);
}

function renderKPIs(data) {
    document.getElementById('kpi-income').innerText = formatCurrency(data.total_income);
    document.getElementById('kpi-expenses').innerText = formatCurrency(data.total_expenses);
    document.getElementById('kpi-savings').innerText = formatCurrency(data.savings);
    document.getElementById('ai-prediction').innerText = formatCurrency(data.predicted_expenses);
    
    // Change color of savings depending on positive/negative
    if (data.savings < 0) {
        document.getElementById('kpi-savings').style.color = 'var(--danger)';
    }
}

function renderMonthlyChart(chartData) {
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    
    if (monthlyChartInstance) monthlyChartInstance.destroy();

    monthlyChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Monthly Expenses',
                data: chartData.data,
                borderColor: '#58a6ff',
                backgroundColor: 'rgba(88, 166, 255, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { grid: { color: 'rgba(255,255,255,0.05)' } }
            }
        }
    });
}

function renderCategoryChart(chartData) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    if (categoryChartInstance) categoryChartInstance.destroy();

    // Curated dark theme colors
    const premiumColors = [
        '#58a6ff', '#2ea043', '#8957e5', '#f85149', '#cca700', '#d2a8ff'
    ];

    categoryChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.data,
                backgroundColor: premiumColors.slice(0, chartData.labels.length),
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#c9d1d9', font: {family: 'Inter'} } }
            },
            cutout: '70%'
        }
    });
}

function renderAlerts(warnings) {
    const container = document.getElementById('alerts-container');
    container.innerHTML = '';
    
    if (!warnings || warnings.length === 0) {
        container.innerHTML = '<p class="no-data" style="color:var(--success);">No alerts. You are within your budget!</p>';
        return;
    }
    
    warnings.forEach(w => {
        const div = document.createElement('div');
        div.className = 'error-msg'; // reusing auth error styles for generic warning layout
        div.style.marginBottom = '10px';
        div.innerHTML = `<strong>Warning for ${w.category}:</strong> Limits set: ${formatCurrency(w.limit)}. Currently spent: <strong>${formatCurrency(w.spent)}</strong>! You are overbudget.`;
        container.appendChild(div);
    });
}
