document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('budget-form');
    const budgetList = document.getElementById('budget-list');

    loadBudgets();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const category = document.getElementById('bud-category').value;
        const limit = document.getElementById('bud-limit').value;

        try {
            await apiFetch('/budgets/', {
                method: 'POST',
                body: JSON.stringify({ category, limit })
            });
            showToast('Budget saved successfully');
            loadBudgets();
            form.reset();
        } catch (err) {
            console.error(err);
        }
    });

    async function loadBudgets() {
        try {
            const data = await apiFetch('/budgets/');
            renderBudgets(data);
        } catch (err) {
            console.error('Failed to load budgets', err);
        }
    }

    function renderBudgets(budgets) {
        // Clear all except the no-data paragraph
        Array.from(budgetList.children).forEach(child => {
            if (!child.classList.contains('no-data')) {
                budgetList.removeChild(child);
            }
        });

        const noDataMsg = budgetList.querySelector('.no-data');

        if (!budgets || budgets.length === 0) {
            noDataMsg.classList.remove('hidden');
            return;
        }

        noDataMsg.classList.add('hidden');

        budgets.forEach(b => {
            const div = document.createElement('div');
            div.className = 'card mt-2';
            div.style.background = 'rgba(255,255,255,0.03)';
            div.style.padding = '16px';
            div.style.borderRadius = '8px';

            div.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; font-size:1rem; color:var(--text-primary);"><i data-feather="tag" style="width:14px; height:14px; margin-right:6px; color:var(--accent-primary);"></i>${b.category}</h4>
                    <span style="font-weight:700; color:#fff;">$${parseFloat(b.limit).toFixed(2)}</span>
                </div>
                <div style="margin-top:12px; height:6px; background:rgba(255,255,255,0.1); border-radius:3px; overflow:hidden;">
                    <!-- Visual representation could go here by fetching spent amount per category -->
                    <div style="height:100%; width:100%; background:var(--accent-primary); opacity:0.5;"></div>
                </div>
            `;
            budgetList.appendChild(div);
        });
        feather.replace();
    }
});
