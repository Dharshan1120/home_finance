document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('expense-form');
    const tbody = document.getElementById('expenses-tbody');
    const idField = document.getElementById('expense-id');
    const submitBtn = document.getElementById('exp-submit');
    const cancelBtn = document.getElementById('exp-cancel');
    const noDataRow = document.getElementById('no-expenses');

    loadExpenses();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const expenseData = {
            amount: document.getElementById('exp-amount').value,
            category: document.getElementById('exp-category').value,
            date: document.getElementById('exp-date').value,
            description: document.getElementById('exp-desc').value
        };

        const existingId = idField.value;

        try {
            if (existingId) {
                // Update
                const res = await apiFetch(`/expenses/${existingId}`, {
                    method: 'PUT',
                    body: JSON.stringify(expenseData)
                });
                if (res) showToast('Expense updated successfully');
            } else {
                // Create
                const res = await apiFetch(`/expenses/`, {
                    method: 'POST',
                    body: JSON.stringify(expenseData)
                });
                if (res) showToast('Expense added successfully');
            }
            
            resetForm();
            loadExpenses();
        } catch (e) {
            console.error("Failed to save expense", e);
        }
    });

    cancelBtn.addEventListener('click', () => {
        resetForm();
    });

    async function loadExpenses() {
        try {
            const data = await apiFetch('/expenses/');
            renderTable(data);
        } catch (e) {
            console.error("Failed to load expenses", e);
        }
    }

    function renderTable(expenses) {
        tbody.innerHTML = '';
        if (!expenses || expenses.length === 0) {
            noDataRow.classList.remove('hidden');
            return;
        }
        
        noDataRow.classList.add('hidden');
        expenses.forEach(exp => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${exp.date}</td>
                <td><span class="badge" style="color:var(--accent-primary); background:rgba(88,166,255,0.1); padding:4px 8px; border-radius:4px; font-size:0.8rem;">${exp.category}</span></td>
                <td>${exp.description || '-'}</td>
                <td style="font-weight:600;">$${parseFloat(exp.amount).toFixed(2)}</td>
                <td>
                    <button class="action-btn edit" data-id="${exp.id}" onclick="editExpense(${exp.id}, ${exp.amount}, '${exp.category}', '${exp.date}', '${exp.description || ''}')">
                        <i data-feather="edit-2"></i>
                    </button>
                    <button class="action-btn delete" data-id="${exp.id}" onclick="deleteExpense(${exp.id})">
                        <i data-feather="trash-2"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        feather.replace();
    }

    window.editExpense = function(id, amount, category, date, desc) {
        idField.value = id;
        document.getElementById('exp-amount').value = amount;
        document.getElementById('exp-category').value = category;
        document.getElementById('exp-date').value = date;
        document.getElementById('exp-desc').value = desc;
        
        submitBtn.innerText = 'Update Expense';
        cancelBtn.classList.remove('hidden');
    }

    window.deleteExpense = async function(id) {
        if (!confirm("Are you sure you want to delete this expense?")) return;
        
        try {
            await apiFetch(`/expenses/${id}`, { method: 'DELETE' });
            showToast('Expense deleted');
            loadExpenses();
        } catch (e) {
            console.error("Failed to delete", e);
        }
    }

    function resetForm() {
        form.reset();
        idField.value = '';
        submitBtn.innerText = 'Save Expense';
        cancelBtn.classList.add('hidden');
    }
});
