# Function to extract transactions from Sheet 4 and correctly categorize In/Out based on amount

import pdfplumber
import pandas as pd
import re

# Updated PDF path for Sheet 4
pdf_path = "sheet3.pdf"

# Regular expression to identify transaction dates (Format: MMM DD)
date_pattern = re.compile(r"[A-Za-z]{3} \d{1,2}")

# Function to extract transactions from Sheet 4 with correct In/Out categorization
def extract_transactions_sheet4(pdf_path):
    transactions = []
    starting_balance = 10487.68  # Extracted from the Account Summary
    current_balance = starting_balance

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split("\n")
            for line in lines:
                match = date_pattern.match(line)
                if match:
                    parts = line.split()
                    if len(parts) >= 4:
                        transaction_date = parts[0] + " " + parts[1]  # Format: MMM DD
                        description = " ".join(parts[2:-2])
                        amount = float(parts[-1].replace(",", "").replace("$", "")) if parts[-1].replace(",", "").replace("$", "").replace(".", "").isdigit() else 0
                        
                        # Categorize In (£) or Out (£)
                        money_in = amount if amount > 0 else 0
                        money_out = abs(amount) if amount < 0 else 0

                        # Adjust balance based on transaction
                        current_balance += money_in - money_out

                        transactions.append([transaction_date, description, money_in, money_out, current_balance])
    
    return transactions

# Extract transactions from Sheet 4
transactions_sheet4 = extract_transactions_sheet4(pdf_path)

# Convert extracted transactions into a DataFrame with correct column names
df_transactions = pd.DataFrame(transactions_sheet4, columns=["Date", "Description", "In (£)", "Out (£)", "Balance (£)"])

# Updated CSV filename
csv_filename = "extracted_transactions_sheet3.csv"
df_transactions.to_csv(csv_filename, index=False)


# Print confirmation message
print(f"✅ Successfully extracted {len(df_transactions)} transactions from Sheet 3 and saved to {csv_filename}")
