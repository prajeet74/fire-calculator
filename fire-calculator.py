import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(page_title="FIRE Calculator", layout="wide")

# App title and description
st.title("FIRE Calculator")
st.markdown("Calculate your path to Financial Independence and Early Retirement")

# Sidebar for inputs
st.sidebar.header("Your Details")

# Personal details
current_age = st.sidebar.number_input("Current Age", min_value=18, max_value=80, value=28)
retirement_age = st.sidebar.number_input("Target Retirement Age", min_value=current_age, max_value=100, value=45)
years_until_retirement = retirement_age - current_age

# Current financial status
st.sidebar.header("Current Financial Status")
current_savings = st.sidebar.number_input("Current Savings (Rs)", min_value=0, value=1000000)
monthly_income = st.sidebar.number_input("Monthly Income (Rs)", min_value=0, value=100000)
savings_rate = st.sidebar.slider("Savings Rate (%)", min_value=5, max_value=80, value=40)
annual_investment_return = st.sidebar.slider("Expected Investment Return (%)", min_value=1, max_value=15, value=7)

# Expense details
st.sidebar.header("Expense Details")
monthly_expense = st.sidebar.number_input("Current Monthly Expenses (Rs)", min_value=0, value=50000)
expense_inflation = st.sidebar.slider("Expense Inflation Rate (%)", min_value=1, max_value=10, value=4)

# Trips
trips_per_year = st.sidebar.number_input("Trips Per Year", min_value=0, max_value=10, value=1)
trip_budget = st.sidebar.number_input("Trip Budget (Rs)", min_value=0, value=250000)
trip_inflation = st.sidebar.slider("Trip Cost Inflation Rate (%)", min_value=1, max_value=10, value=6)

# Car Upgrade
car_upgrade_years = st.sidebar.number_input("Car Upgrade Frequency (years)", min_value=1, max_value=20, value=7)
car_cost = st.sidebar.number_input("Car Upgrade Cost (Rs)", min_value=0, value=1500000)
car_inflation = st.sidebar.slider("Car Cost Inflation Rate (%)", min_value=1, max_value=10, value=5)

# Phone/Gadget Upgrade
gadget_upgrade_years = st.sidebar.number_input("Gadget Upgrade Frequency (years)", min_value=1, max_value=10, value=7)
gadget_cost = st.sidebar.number_input("Gadget Upgrade Cost (Rs)", min_value=0, value=500000)
gadget_inflation = st.sidebar.slider("Gadget Cost Inflation Rate (%)", min_value=1, max_value=10, value=3)

# Dependents
num_dependents = st.sidebar.number_input("Number of Dependents", min_value=0, max_value=10, value=1)
dependent_cost = st.sidebar.number_input("Annual Cost per Dependent (Rs)", min_value=0, value=600000)
dependent_inflation = st.sidebar.slider("Dependent Cost Inflation Rate (%)", min_value=1, max_value=10, value=6)

# Misc Costs
misc_monthly = st.sidebar.number_input("Miscellaneous Monthly Costs (Rs)", min_value=0, value=10000)
misc_inflation = st.sidebar.slider("Misc Cost Inflation Rate (%)", min_value=1, max_value=10, value=6)

# Safe Withdrawal Rate
swr = st.sidebar.slider("Safe Withdrawal Rate (%)", min_value=2.0, max_value=5.0, value=4.0, step=0.1)

# Calculate annualized values
annual_expense = monthly_expense * 12
annual_trips = trips_per_year * trip_budget
car_annual = car_cost / car_upgrade_years
gadget_annual = gadget_cost / gadget_upgrade_years
dependent_annual = num_dependents * dependent_cost
misc_annual = misc_monthly * 12

# Calculate weighted average inflation
total_annual_cost = annual_expense + annual_trips + car_annual + gadget_annual + dependent_annual + misc_annual

if total_annual_cost > 0:
    weighted_inflation = (
        (annual_expense * expense_inflation) + 
        (annual_trips * trip_inflation) + 
        (car_annual * car_inflation) + 
        (gadget_annual * gadget_inflation) + 
        (dependent_annual * dependent_inflation) + 
        (misc_annual * misc_inflation)
    ) / total_annual_cost
else:
    weighted_inflation = 4  # Default if total cost is zero

# Main calculations for FIRE
def calculate_fire_number(annual_expenses, swr):
    return annual_expenses * (100 / swr)

def calculate_future_expenses(years):
    future_expense = annual_expense * ((1 + expense_inflation/100) ** years)
    future_trips = annual_trips * ((1 + trip_inflation/100) ** years)
    future_car = car_annual * ((1 + car_inflation/100) ** years)
    future_gadget = gadget_annual * ((1 + gadget_inflation/100) ** years)
    future_dependent = dependent_annual * ((1 + dependent_inflation/100) ** years)
    future_misc = misc_annual * ((1 + misc_inflation/100) ** years)
    
    return future_expense + future_trips + future_car + future_gadget + future_dependent + future_misc

# Calculate retirement number
retirement_annual_expenses = calculate_future_expenses(years_until_retirement)
fire_number = calculate_fire_number(retirement_annual_expenses, swr)

# Display calculations
st.header("Current Expenses Breakdown")

# Create expenses table
expense_data = {
    "Category": ["Monthly Expenses", "Annual Trips", "Car Upgrade", "Gadget Upgrade", "Dependents", "Misc Costs", "Total"],
    "Current Amount (Rs)": [
        f"{monthly_expense:,.2f} (monthly)", 
        f"{trip_budget:,.2f} × {trips_per_year} trip(s)", 
        f"{car_cost:,.2f} (every {car_upgrade_years} years)", 
        f"{gadget_cost:,.2f} (every {gadget_upgrade_years} years)",
        f"{dependent_cost:,.2f} × {num_dependents} dependent(s)",
        f"{misc_monthly:,.2f} (monthly)",
        ""
    ],
    "Annualized (Rs)": [
        f"{annual_expense:,.2f}",
        f"{annual_trips:,.2f}",
        f"{car_annual:,.2f}",
        f"{gadget_annual:,.2f}",
        f"{dependent_annual:,.2f}",
        f"{misc_annual:,.2f}",
        f"{total_annual_cost:,.2f}"
    ],
    "Inflation Rate (%)": [
        f"{expense_inflation:.2f}%",
        f"{trip_inflation:.2f}%",
        f"{car_inflation:.2f}%",
        f"{gadget_inflation:.2f}%",
        f"{dependent_inflation:.2f}%",
        f"{misc_inflation:.2f}%",
        f"{weighted_inflation:.2f}% (weighted avg)"
    ]
}

expense_df = pd.DataFrame(expense_data)
st.dataframe(expense_df, use_container_width=True, hide_index=True)

# Display FIRE details
st.header("FIRE Calculation Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Current Annual Expenses", f"₹{total_annual_cost:,.2f}")
    st.metric("Projected Annual Expenses at Retirement", f"₹{retirement_annual_expenses:,.2f}")
    st.metric("Years Until Retirement", f"{years_until_retirement} years")

with col2:
    st.metric("Weighted Average Inflation", f"{weighted_inflation:.2f}%")
    st.metric("Safe Withdrawal Rate", f"{swr:.1f}%")
    st.metric("FIRE Number", f"₹{fire_number:,.2f}", help="The amount you need to save to retire")

# Projection calculation
def calculate_fire_projection():
    monthly_saving = monthly_income * (savings_rate / 100)
    annual_saving = monthly_saving * 12
    
    # Projection data
    years = list(range(0, years_until_retirement + 1))
    age = [current_age + y for y in years]
    savings = [current_savings]
    annual_expenses = [total_annual_cost]
    fire_numbers = [calculate_fire_number(total_annual_cost, swr)]
    fire_achieved = [False]
    
    for year in range(1, years_until_retirement + 1):
        # Calculate next year's values
        new_savings = savings[-1] * (1 + annual_investment_return/100) + annual_saving
        new_expense = calculate_future_expenses(year)
        new_fire_number = calculate_fire_number(new_expense, swr)
        achieved = new_savings >= new_fire_number
        
        # Append to lists
        savings.append(new_savings)
        annual_expenses.append(new_expense)
        fire_numbers.append(new_fire_number)
        fire_achieved.append(achieved)
    
    # Find when FIRE is achieved
    fire_year = None
    if True in fire_achieved:
        fire_year = fire_achieved.index(True)
    
    return {
        'age': age,
        'year': years,
        'savings': savings,
        'annual_expenses': annual_expenses,
        'fire_numbers': fire_numbers,
        'fire_achieved': fire_achieved,
        'fire_year': fire_year
    }

# Calculate projection
projection = calculate_fire_projection()

# Display projection chart
st.header("FIRE Projection")

# Create chart
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add projection lines
fig.add_trace(
    go.Scatter(
        x=projection['age'], 
        y=projection['savings'],
        mode='lines',
        name='Projected Savings',
        line=dict(color='green', width=3)
    )
)

fig.add_trace(
    go.Scatter(
        x=projection['age'], 
        y=projection['fire_numbers'],
        mode='lines',
        name='FIRE Number',
        line=dict(color='red', width=3)
    )
)

# If FIRE is achieved, mark the point
if projection['fire_year'] is not None:
    fire_age = projection['age'][projection['fire_year']]
    fire_amount = projection['savings'][projection['fire_year']]
    
    fig.add_trace(
        go.Scatter(
            x=[fire_age],
            y=[fire_amount],
            mode='markers',
            marker=dict(size=15, color='gold', symbol='star'),
            name=f'FIRE Achieved at Age {fire_age}'
        )
    )

# Update layout
fig.update_layout(
    title='Savings vs. FIRE Number Projection',
    xaxis_title='Age',
    yaxis_title='Amount (Rs)',
    legend=dict(x=0.01, y=0.99),
    hovermode='x unified',
    height=600
)

# Format y-axis to display large numbers better
fig.update_yaxes(
    tickprefix='₹',
    tickformat='.2s'
)

st.plotly_chart(fig, use_container_width=True)

# Show detailed projection data
if st.checkbox("Show Detailed Projection Data"):
    projection_data = {
        "Age": projection['age'],
        "Year": [f"Year {y}" for y in projection['year']],
        "Projected Savings (Rs)": [f"₹{s:,.2f}" for s in projection['savings']],
        "Annual Expenses (Rs)": [f"₹{e:,.2f}" for e in projection['annual_expenses']],
        "FIRE Number (Rs)": [f"₹{fn:,.2f}" for fn in projection['fire_numbers']],
        "FIRE Achieved": projection['fire_achieved']
    }
    
    projection_df = pd.DataFrame(projection_data)
    st.dataframe(projection_df, use_container_width=True, hide_index=True)

# Add insights section
st.header("FIRE Insights")

# Calculate FIRE achievement
if projection['fire_year'] is not None:
    fire_age = projection['age'][projection['fire_year']]
    years_to_fire = projection['year'][projection['fire_year']]
    
    st.success(f"🎉 Based on your inputs, you can achieve FIRE at age {fire_age}, which is {years_to_fire} years from now!")
    
    # If achieved before retirement age
    if fire_age < retirement_age:
        st.info(f"You're on track to reach FIRE {retirement_age - fire_age} years earlier than your target retirement age of {retirement_age}!")
else:
    if years_until_retirement > 0:
        st.warning(f"Based on current projections, you may not reach your FIRE number by your target retirement age of {retirement_age}.")
        
        # Suggestions
        st.subheader("Suggestions to Improve Your FIRE Journey")
        st.markdown("""
        Consider these options to accelerate your FIRE timeline:
        - Increase your savings rate
        - Look for ways to boost your income
        - Optimize your investment returns
        - Reduce expenses in any category
        - Adjust your retirement expectations
        """)

# Key financial metrics
st.subheader("Key Financial Metrics")
col1, col2, col3 = st.columns(3)

annual_saving = monthly_income * 12 * (savings_rate / 100)
years_to_save = 0 if annual_saving <= 0 else (fire_number - current_savings) / (annual_saving * (1 + annual_investment_return/100))

with col1:
    st.metric("Annual Savings", f"₹{annual_saving:,.2f}")
    
with col2:
    if annual_saving > 0:
        st.metric("Savings Rate", f"{savings_rate}%")
    else:
        st.metric("Savings Rate", f"{savings_rate}%", delta="-", delta_color="inverse")
        
with col3:
    if years_to_save > 0 and years_to_save < float('inf'):
        st.metric("Years to Save (without returns)", f"{years_to_save:.1f} years")
    else:
        st.metric("Years to Save (without returns)", "N/A")

# Notes and disclaimers
st.header("Notes & Disclaimers")
st.info("""
- This calculator provides estimates based on the inputs you provide and assumes constant growth rates.
- Actual results may vary due to market fluctuations, changes in income, expenses, and other life events.
- It's recommended to revisit your FIRE plan periodically and adjust as needed.
- The Safe Withdrawal Rate is based on historical data and may not guarantee future results.
- This is a planning tool and not financial advice. Consider consulting with a financial advisor for personalized guidance.
""")