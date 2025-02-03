# Adjusted extraction function for Sheet 2 to correctly extract transactions and maintain the five standard columns

import pdfplumber
import pandas as pd
import re

# Updated PDF path for Sheet 2
pdf_path = "sheet2.pdf"

# Regular expression to identify transaction dates (Format: DD MMM YY)
date_pattern = re.compile(r"\d{2} \w{3}\d{2}")  # e.g., 04 Sep19

# Function to extract transactions from Sheet 2 while keeping only the five standard columns
def extract_transactions_sheet2(pdf_path):
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split("\n")
            for line in lines:
                match = date_pattern.match(line)
                if match:
                    parts = line.split()
                    if len(parts) >= 5:
                        transaction_date = parts[0] + " " + parts[1]  # Date format: DD MMM YY
                        description = " ".join(parts[2:-3])  # Extracting the description properly
                        money_in = float(parts[-3].replace(",", "")) if parts[-3].replace(",", "").replace(".", "").isdigit() else 0
                        money_out = float(parts[-2].replace(",", "")) if parts[-2].replace(",", "").replace(".", "").isdigit() else 0
                        balance = float(parts[-1].replace(",", "")) if parts[-1].replace(",", "").replace(".", "").isdigit() else None

                        transactions.append([transaction_date, description, money_in, money_out, balance])

    return transactions

# Extract transactions from Sheet 2
transactions_sheet2 = extract_transactions_sheet2(pdf_path)

# Convert extracted transactions into a DataFrame with standardized columns
df_transactions = pd.DataFrame(transactions_sheet2, columns=["Date", "Description", "In (£)", "Out (£)", "Balance (£)"])

# Updated CSV filename
csv_filename = "extracted_transactions_sheet2.csv"
df_transactions.to_csv(csv_filename, index=False)


# Print confirmation message
print(f"✅ Successfully extracted {len(df_transactions)} transactions from Sheet 2 and saved to {csv_filename}")
