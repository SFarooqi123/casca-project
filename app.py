import os
import pdfplumber
import pandas as pd
import numpy as np
import shap
import re
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load ML Model
df = pd.read_csv("csv_files/ml_training_features.csv", index_col=0)
labels = {"Business1": 1, "Business2": 1, "Business3": 0}
df["Loan Approved"] = df.index.map(labels)
df = df.apply(pd.to_numeric, errors="coerce")
X = df.drop(columns=["Loan Approved"])
y = df["Loan Approved"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
explainer = shap.Explainer(lambda x: model.predict_proba(x), X, algorithm="permutation")

# Extract transactions from PDF
def extract_transactions(pdf_path):
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    match = re.match(r"(\d{2} \w{3}) (.+?) (\d{1,3}(?:,\d{3})*\.\d{2})? (\d{1,3}(?:,\d{3})*\.\d{2})? (\d{1,3}(?:,\d{3})*\.\d{2}) CR?", line)
                    if match:
                        date, transaction, debit, credit, balance = match.groups()
                        transactions.append([date, transaction, 
                                             float(debit.replace(',', '')) if debit else 0.0,
                                             float(credit.replace(',', '')) if credit else 0.0,
                                             float(balance.replace(',', '')) if balance else 0.0])
    return pd.DataFrame(transactions, columns=["Date", "Transaction", "Out (Debit)", "In (Credit)", "Balance"])

# Extract financial features
def extract_features(transactions_df):
    features = {
        "Total Credits": transactions_df["In (Credit)"].sum(),
        "Total Debits": transactions_df["Out (Debit)"].sum(),
        "Final Balance": transactions_df["Balance"].iloc[-1] if not transactions_df.empty else 0,
        "Net Cash Flow": transactions_df["In (Credit)"].sum() - transactions_df["Out (Debit)"].sum(),
    }
    return pd.DataFrame([features])

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".pdf"):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            transactions_df = extract_transactions(file_path)
            user_features = extract_features(transactions_df)

            for feature in set(X.columns) - set(user_features.columns):
                user_features[feature] = 0
            user_features = user_features[X.columns]

            prediction = model.predict(user_features)[0]
            decision = "Approved ✅" if prediction == 1 else "Denied ❌"

            shap_values = explainer(user_features)
            top_features = np.argsort(-np.abs(shap_values.values[0]))[:3]
            explanations = [f"{X.columns[i]} had a significant impact" for i in top_features]

            return render_template("result.html", decision=decision, explanations=explanations)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
