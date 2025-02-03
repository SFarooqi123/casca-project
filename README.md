# Loan Approval System

This repository contains a Flask-based web application that analyzes bank statements (PDFs) to determine loan eligibility using a machine learning model. The system extracts financial transactions, processes key financial features, and provides a loan decision along with SHAP-based explanations.

---

## **🚀 How to Run the Application**

### **1️⃣ Install Dependencies**
Ensure you have Python installed. Then, install the required dependencies using:
```bash
pip install flask pdfplumber shap scikit-learn pandas fpdf numpy matplotlib
```

### **2️⃣ Run the Flask Server**
```bash
python app.py
```

### **3️⃣ Open in Browser**
Once the server is running, open the application in your web browser:
```
http://127.0.0.1:5000/
```

---

## **📁 Project Structure**
```
CASCA/
│── csv_files/               # Stores extracted and training CSV data
│── scripts/                 # Python scripts for feature extraction
│   ├── feature_extraction.py  # Extracts features from transactions
│   ├── sheet2.py              # Additional transaction processing
│   ├── sheet3.py              # Additional transaction processing
│── static/                  # Static assets (CSS, images)
│   ├── styles.css             # Custom CSS styles
│── templates/               # HTML templates for Flask
│   ├── upload.html            # Upload page
│   ├── result.html            # Results page
│── uploads/                 # Uploaded PDF bank statements
│── app.py                   # Main Flask backend
│── casca.py                 # Additional processing script
```

---

## **📌 What Each File Does**

### **📂 csv_files/**
- `ml_training_features.csv` → Stores training data used for the ML model.
- `extracted_transactions_*.csv` → Extracted transaction data from uploaded PDFs.
- `combined_transactions.csv` → Combined financial data from different sources.

### **📂 scripts/**
- `feature_extraction.py` → Extracts financial features from transaction data.
- `sheet2.py` / `sheet3.py` → Process and analyze different sets of transactions.

### **📂 static/**
- `styles.css` → Styling for the web application.

### **📂 templates/**
- `upload.html` → User uploads a PDF.
- `result.html` → Displays loan decision and key influencing factors.

### **📂 uploads/**
- Stores all uploaded PDF bank statements.

### **app.py**
- Main Flask application.
- Handles file uploads, extracts transactions, applies ML model, and returns results.

### **casca.py**
- Additional script (if needed for processing extra tasks).

---

## **🛠️ Next Steps**
- Deploy on **Render, AWS, or Heroku**.
- Improve **UI design** with **Bootstrap or Tailwind CSS**.
- Add **graphical SHAP visualizations** for better explanations.

---

## **👨‍💻 Author**
Developed for **loan evaluation and financial analysis**.

