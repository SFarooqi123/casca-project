# Adjusted feature extraction script to include multiple businesses (Sheet1, Sheet2, Sheet3)
# Each business is represented as a row in the dataset for ML training

import pandas as pd

# List of extracted transaction CSV files for multiple businesses
csv_files = {
    "Business1": "extracted_transactions_sheet1.csv",
    "Business2": "extracted_transactions_sheet2.csv",
    "Business3": "extracted_transactions_sheet3.csv"
}

# Function to compute financial metrics for each business
def compute_financial_metrics(df):
    # Ensure Date is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Fill missing values
    df.fillna({"In (£)": 0, "Out (£)": 0, "Balance (£)": 0}, inplace=True)

    # Extract Month and Year for Monthly Aggregations
    df["Year-Month"] = df["Date"].dt.to_period("M")

    # Compute Monthly Aggregates
    monthly_summary = df.groupby("Year-Month").agg(
        Total_Deposits=("In (£)", "sum"),
        Total_Withdrawals=("Out (£)", "sum"),
        Closing_Balance=("Balance (£)", "last")
    ).reset_index()

    # Compute Net Cash Flow
    monthly_summary["Net_Cash_Flow"] = monthly_summary["Total_Deposits"] - monthly_summary["Total_Withdrawals"]

    # Compute Cash Flow Volatility (Standard Deviation of Net Cash Flow)
    cash_flow_volatility = monthly_summary["Net_Cash_Flow"].std()

    # Compute Average Monthly Balance
    avg_monthly_balance = monthly_summary["Closing_Balance"].mean()

    # Compute Number of Months with Negative Balance
    num_negative_balance_months = (monthly_summary["Closing_Balance"] < 0).sum()

    # Compute Loan-to-Income Ratio
    loan_payments = df[df["Description"].str.contains("loan|mortgage|credit card|emi|finance", case=False, na=False)]["Out (£)"].sum()
    total_income = df["In (£)"].sum()
    loan_to_income_ratio = loan_payments / total_income if total_income > 0 else 0

    # Compute Missed Payments (Late Fees)
    missed_payment_keywords = ["late fee", "penalty", "overdraft", "bounced"]
    missed_payments = df[df["Description"].str.contains('|'.join(missed_payment_keywords), case=False, na=False)]
    num_missed_payments = len(missed_payments)

    # Compute Revenue Growth
    df["Year"] = df["Date"].dt.year
    yearly_revenue = df.groupby("Year").agg(Total_Revenue=("In (£)", "sum")).reset_index()
    yearly_revenue["Growth_Rate"] = yearly_revenue["Total_Revenue"].pct_change() * 100

    # Identify High-Value Transactions (Deposits > 90th Percentile)
    high_value_threshold = df["In (£)"].quantile(0.90)
    num_high_value_transactions = (df["In (£)"] >= high_value_threshold).sum()

    # Identify Customer Diversity (Does one customer contribute >50% of revenue?)
    customer_revenue = df.groupby("Description").agg(Total_Revenue=("In (£)", "sum")).reset_index()
    customer_revenue["Revenue_Share"] = customer_revenue["Total_Revenue"] / total_income
    max_customer_share = customer_revenue["Revenue_Share"].max()

    # Return computed features as a dictionary
    return {
        "Average Monthly Deposits": monthly_summary["Total_Deposits"].mean(),
        "Average Monthly Withdrawals": monthly_summary["Total_Withdrawals"].mean(),
        "Average Monthly Net Cash Flow": monthly_summary["Net_Cash_Flow"].mean(),
        "Cash Flow Volatility": cash_flow_volatility,
        "Average Monthly Balance": avg_monthly_balance,
        "Months with Negative Balance": num_negative_balance_months,
        "Total Loan Payments": loan_payments,
        "Loan-to-Income Ratio": loan_to_income_ratio,
        "Missed Payments Count": num_missed_payments,
        "Revenue Growth Rate (Last Year)": yearly_revenue["Growth_Rate"].iloc[-1] if len(yearly_revenue) > 1 else None,
        "Number of High-Value Transactions": num_high_value_transactions,
        "Highest Customer Revenue Share": max_customer_share
    }

# Compute financial metrics for each business
business_data = {}
for business, file in csv_files.items():
    df = pd.read_csv(file)
    business_data[business] = compute_financial_metrics(df)

# Convert to DataFrame
df_features = pd.DataFrame.from_dict(business_data, orient="index")

# Save Features to CSV for ML Model Training
csv_filename = "ml_training_features.csv"
df_features.to_csv(csv_filename, index=True)



# Print Confirmation
print(f"✅ Successfully extracted financial features for multiple businesses and saved to '{csv_filename}'")
