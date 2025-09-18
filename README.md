# 🧾 Receipt Parser

Convert receipt images (JPG/PNG) into structured **JSON** and **CSV** using OCR + Google Document AI.

## 🚀 Features
- Upload receipts as images
- Extract key fields (store, date, items, total, GST, etc.)
- Export results as JSON or CSV
- Sample receipts & parsed outputs included

## 📂 Repo Structure
```
receipt-parser/
 ┣ 📜 GoogleReceiptScannerBatch.ipynb   # Jupyter Notebook pipeline
 ┣ 📜 requirements.txt                   # Dependencies
 ┣ 📜 README.md                          # Project documentation
 ┣ 📂 sample_receipts/                   # Example receipt images
 ┣ 📂 output/                            # Parsed JSON + CSV outputs
```

## 🔧 Setup
```bash
pip install -r requirements.txt
```

## ▶️ Usage
Run the Jupyter notebook:
```bash
jupyter notebook GoogleReceiptScannerBatch.ipynb
```

## 📊 Examples
Input (sample receipt) → Output (JSON/CSV in `output/`)
