# 🧠 LLMs in Business Intelligence

This project demonstrates how **Large Language Models (LLMs)** can enhance **Business Intelligence (BI)** by enabling **natural language queries** on structured datasets.  
Using the **Superstore dataset** (from Kaggle), we built a **NL→SQL assistant** that lets users ask questions like:  

- *"Show total sales and profit by region"*  
- *"List the top 10 customers by sales"*  
- *"Show yearly sales totals from 2014 to 2017"*  

…and instantly get results with SQL queries, tables, and visualizations.

---

## 🚀 Features
- Natural language to SQL query conversion (via Hugging Face T5 model).
- Safe fallback SQL for common queries (no model needed).
- SQLite in-memory database for fast querying.
- Streamlit web UI with interactive charts & results.
- Exports results (CSV + charts) for reproducibility.

---

## 📂 Dataset
We use the **Sample Superstore dataset** from Kaggle:  
👉 [Superstore Dataset (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

The app first checks if `Sample - Superstore.csv` exists locally.  
If not found, it automatically downloads from KaggleHub.

---

## 🛠️ Installation (Local Setup)

Clone the repo:

```bash
git clone https://github.com/SagarTechTrends/LLM-s-in-Business-Intelligence.git
cd LLM-s-in-Business-Intelligence
```

Create a virtual environment & install dependencies:

```bash
python3 -m venv myenv
source myenv/bin/activate   # (Linux/Mac)
myenv\Scripts\activate      # (Windows)

pip install -r requirements.txt
```

Run the Streamlit app locally:

```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501).

---

## ☁️ Deploy to Streamlit Cloud

1. Push your repo (with `app.py`, `requirements.txt`, and optionally the dataset CSV) to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Connect your GitHub repo.
4. Select `app.py` as the entry point.
5. Deploy 🚀.

If you don’t upload the dataset, don’t worry — the app will auto-download it via KaggleHub.

---

## 📊 Example Queries

- **Sales & Profit by Region**
- **Top 10 Customers by Sales**
- **Profitability by Category**
- **Yearly Sales (2014–2017)**
- **Discount Impact on Profit**

The app generates SQL, executes it, and shows both **tables + charts**.

---

## 📦 Requirements
See [`requirements.txt`](requirements.txt) for dependencies:
```
streamlit
pandas
numpy
matplotlib
sqlite3-bro
transformers
sentencepiece
kagglehub
```

---

## 📄 License
MIT License – feel free to use, modify, and share.  
