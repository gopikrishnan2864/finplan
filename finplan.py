import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if 'income' not in st.session_state:
    st.session_state.income = 0
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'savings_goal' not in st.session_state:
    st.session_state.savings_goal = 0

# Function to calculate budget
def calculate_budget(income, expenses):
    total_expenses = sum(expenses)
    budget = income - total_expenses
    return budget

# Function to track savings
def track_savings(savings_goal, budget):
    progress = (budget / savings_goal) * 100 if savings_goal > 0 else 0
    return progress

# Function to generate report
def generate_report(income, expenses, savings_goal, budget):
    expense_categories = ["Housing", "Food", "Transportation", "Entertainment", "Other"]
    report = ""
    
    # Determine spender type
    if sum(expenses) / income > 0.8:
        spender_type = "High Spender"
    elif sum(expenses) / income > 0.5:
        spender_type = "Moderate Spender"
    else:
        spender_type = "Frugal Spender"
    
    report += f"Spender Type: {spender_type}\n"
    
    # Identify areas for improvement
    sorted_expenses = sorted(zip(expense_categories, expenses), key=lambda x: x[1], reverse=True)
    report += "Areas for Improvement:\n"
    for category, amount in sorted_expenses[:2]:
        report += f"- {category}: ₹{amount} (Consider reducing expenses in this category)\n"
    
    # Savings goal achievement
    if budget >= savings_goal:
        report += f"\nYou are on track to achieve your savings goal of ₹{savings_goal}."
    else:
        report += f"\nYou need to save an additional ₹{savings_goal - budget} to achieve your savings goal."
    
    return report

# Streamlit app
st.title("Personal Financial Planner")

# Income input
st.subheader("Income")
income = st.number_input("Enter your monthly income", min_value=0)
st.session_state.income = income

# Expense tracking
st.subheader("Expenses")
expenses = []
expense_categories = ["Housing", "Food", "Transportation", "Entertainment", "Other"]
for category in expense_categories:
    expense = st.number_input(f"Enter your monthly {category} expenses", min_value=0)
    expenses.append(expense)
st.session_state.expenses = expenses

# Savings goal
st.subheader("Savings Goal")
savings_goal = st.number_input("Enter your monthly savings goal", min_value=0)
st.session_state.savings_goal = savings_goal

# Calculate budget and track savings
budget = calculate_budget(st.session_state.income, st.session_state.expenses)
savings_progress = track_savings(st.session_state.savings_goal, budget)

# Display results
st.subheader("Results")
st.write(f"Budget: {budget}")
st.write(f"Savings Progress: {savings_progress}%")

# Visualize expenses
st.subheader("Expense Breakdown")
expense_df = pd.DataFrame({"Category": expense_categories, "Amount": st.session_state.expenses})
fig, ax = plt.subplots()
ax.pie(expense_df["Amount"], labels=expense_df["Category"], autopct='%1.1f%%')
st.pyplot(fig)

# Visualize savings progress
st.subheader("Savings Progress")
fig, ax = plt.subplots()
ax.bar(["Savings Goal", "Current Savings"], [st.session_state.savings_goal, budget])
ax.set_xlabel("Category")
ax.set_ylabel("Amount")
st.pyplot(fig)

# Generate report
st.subheader("Personalized Report")
report = generate_report(income, expenses, savings_goal, budget)
st.code(report, language="text")