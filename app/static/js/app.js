const API_URL = "/api/expenses/";

const expenseForm = document.getElementById("expense-form");
const expenseList = document.getElementById("expense-list");
const filterCategory = document.getElementById("filter-category");
const message = document.getElementById("message");

// Set today's date by default
document.getElementById("date").value =
    new Date().toISOString().split("T")[0];


// Fetch expenses from backend
async function loadExpenses() {
    const category = filterCategory.value;

    const url = category
        ? `${API_URL}?category=${encodeURIComponent(category)}`
        : API_URL;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Unable to load expenses");
        }

        const expenses = await response.json();

        displayExpenses(expenses);
        await loadSummary();

    } catch (error) {
        expenseList.textContent = error.message;
    }
}


// Display expenses on the page
function displayExpenses(expenses) {
    expenseList.innerHTML = "";

    if (expenses.length === 0) {
        expenseList.textContent = "No expenses found.";
        return;
    }

    expenses.forEach(expense => {
        const item = document.createElement("div");
        item.className = "expense-item";

        const info = document.createElement("div");
        info.className = "expense-info";

        const title = document.createElement("strong");
        title.textContent = expense.title;

        const details = document.createElement("p");
        details.textContent =
            `${expense.category} | ${expense.date}`;

        const amount = document.createElement("strong");
        amount.textContent = `Rs. ${Number(expense.amount).toFixed(2)}`;

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-button";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
            deleteExpense(expense.id);
        });

        info.append(title, details);
        item.append(info, amount, deleteButton);

        expenseList.appendChild(item);
    });
}


// Add a new expense
expenseForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const expense = {
        title: document.getElementById("title").value.trim(),
        amount: Number(document.getElementById("amount").value),
        category: document.getElementById("category").value,
        date: document.getElementById("date").value
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(expense)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to add expense");
        }

        message.textContent = "Expense added successfully!";
        expenseForm.reset();

        document.getElementById("date").value =
            new Date().toISOString().split("T")[0];

        await loadExpenses();

    } catch (error) {
        message.textContent = error.message;
    }
});


// Delete an expense
async function deleteExpense(id) {
    try {
        const response = await fetch(`${API_URL}${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Unable to delete expense");
        }

        await loadExpenses();

    } catch (error) {
        message.textContent = error.message;
    }
}


// Fetch summary information
async function loadSummary() {
    try {
        const response = await fetch(`${API_URL}summary`);

        if (!response.ok) {
            throw new Error("Unable to load summary");
        }

        const summary = await response.json();

        document.getElementById("total-expenses").textContent =
            `Rs. ${Number(summary.total_expenses).toFixed(2)}`;

        document.getElementById("transaction-count").textContent =
            summary.transaction_count;

        document.getElementById("average-expense").textContent =
            `Rs. ${Number(summary.average_expense).toFixed(2)}`;

    } catch (error) {
        message.textContent = error.message;
    }
}


// Filter expenses
filterCategory.addEventListener("change", loadExpenses);


// Initial page load
loadExpenses();
