import numpy as np
import pandas as pd

try:
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def predict_next_month_expenses(expenses):
    """
    Predict next month's total expenses using simple Linear Regression
    based on historical monthly expense totals.
    
    expenses: list of Expense objects
    return: predicted total amount as float, or 0 if insufficient data
    """
    if not expenses:
        return 0.0
        
    # Prepare data
    data = []
    for exp in expenses:
        data.append({
            'date': pd.to_datetime(exp.date),
            'amount': exp.amount
        })
        
    df = pd.DataFrame(data)
    
    # Set month index for aggregation Let's say we group by year & month
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Aggregate data by month
    monthly_totals = df.groupby('year_month')['amount'].sum().reset_index()
    monthly_totals['month_index'] = np.arange(len(monthly_totals))
    
    # Ensure there's at least 2 points for a meaningful, albeit simple, regression
    if len(monthly_totals) < 2:
        # If only 1 month of data, just return that month's total or average
        return float(monthly_totals['amount'].iloc[0])

    if not SKLEARN_AVAILABLE:
        # Simple fallback: return average of available months
        return float(monthly_totals['amount'].mean())

    X = monthly_totals[['month_index']].values
    y = monthly_totals['amount'].values

    # Fit the linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict for next month (index = len(monthly_totals))
    next_month_index = np.array([[len(monthly_totals)]])
    prediction = model.predict(next_month_index)[0]
    
    # If the model predicts a negative amount due to a steep downward trend, floor it to 0
    return max(0.0, float(prediction))
