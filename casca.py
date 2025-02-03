# Correcting the column format to match all other sheets with "In (£)" and "Out (£)"

import pdfplumber
import pandas as pd
import re

# Define PDF path
pdf_path = "sheet1.pdf"

# Regular expression to identify transaction dates
date_pattern_sheet1 = re.compile(r"\d{2}-[A-Za-z]{3,}-\d{4}")

# Function to extract transactions from Sheet1 with standardized columns
def extract_sheet1(pdf_path):
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    if len(row) >= 6 and date_pattern_sheet1.match(str(row[0])):  
                        try:
                            transaction_date = row[0]
                            description = row[2]
                            debit = row[4] if row[4] else "0"
                            credit = row[5] if row[5] else "0"
                            balance = row[6] if len(row) > 6 else None
                            
                            # Convert to float where applicable
                            debit = float(debit.replace(",", "")) if debit.replace(",", "").replace(".", "").isdigit() else 0
                            credit = float(credit.replace(",", "")) if credit.replace(",", "").replace(".", "").isdigit() else 0
                            balance = float(balance.replace(",", "")) if balance and balance.replace(",", "").replace(".", "").isdigit() else None
                            
                            # Standardize column format (Debit -> "Out (£)", Credit -> "In (£)")
                            transactions.append([transaction_date, description, credit, debit, balance])
                        except:
                            continue
    return transactions

# Extract transactions from Sheet 1
transactions_sheet1 = extract_sheet1(pdf_path)

# Convert extracted transactions into a DataFrame
df_sheet1 = pd.DataFrame(transactions_sheet1, columns=["Date", "Description", "In (£)", "Out (£)", "Balance (£)"])

# Save DataFrame to CSV
csv_path = "extracted_transactions_sheet1.csv"
df_sheet1.to_csv(csv_path, index=False)



# Print confirmation message
print(f"✅ Successfully extracted {len(df_sheet1)} transactions from sheet1 and saved to {csv_path}.")
