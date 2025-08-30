# LLMs in Business Intelligence: NL → SQL Assistant

This project demonstrates how **Large Language Models (LLMs)** can be applied to **Business Intelligence (BI)** workflows by translating **natural language (NL)** questions into **SQL queries** for the popular *Superstore* dataset.  

Users can ask questions like:
- *"Show total sales and profit by region."*
- *"List the top 10 customers by total sales."*
- *"Show yearly sales totals from 2014 to 2017."*

The system automatically:
1. Generates valid **SQLite SQL** from natural language.  
2. Executes queries on the Superstore dataset.  
3. Returns **tables and visualizations**.  
4. Exports results to **CSV + charts** for reproducibility.  

---

## 🚀 Features
- NL → SQL query translation using **Hugging Face T5 (WikiSQL fine-tuned model)**.  
- Fallback SQL templates for robustness.  
- Automatic exports:
  - Individual CSVs per query
  - Batch summary CSV
  - Charts (`Sales by Region`, `Yearly Sales`)  
- Organized `results/` folder with timestamps.  
- Ready-to-deploy on **Binder** and **Streamlit**.  

---

## 📊 Example Outputs
### Sales & Profit by Region
*(Add chart image here — e.g., `Sales & Profit by Region.png`)*

### Yearly Sales (2014–2017)
*(Add chart image here — e.g., `Yearly Sales.png`)*

---

## ⚙️ Setup

### 1. Clone Repo
```bash
git clone https://github.com/SagarTechTrends/LLM-s-in-Business-Intelligence.git
cd LLM-s-in-Business-Intelligence
```

### 2. Create Virtual Environment
```bash
python3 -m venv myenv
source myenv/bin/activate   # on Mac/Linux
myenv\Scripts\activate      # on Windows
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Usage (Jupyter Notebook)

1. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
2. Open `LLM_SQL_BI.ipynb`.  
3. Run all cells — ask NL questions and see generated SQL, execution results, and charts.  
4. Results & exports will be saved under the `results/` folder.  

---

## 🌐 Try Online (Binder)

Click below to launch in Binder without installation:  

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SagarTechTrends/LLM-s-in-Business-Intelligence/HEAD)

---

## 🌐 Streamlit Demo (Optional)

Run a simple web app with Streamlit:  

```bash
streamlit run app.py
```

Deploy free at [Streamlit Cloud](https://streamlit.io/cloud).  

---

## 📂 Project Structure
```
LLM-s-in-Business-Intelligence/
│── requirements.txt
│── README.md
│── LLM_SQL_BI.ipynb          # Main Jupyter Notebook
│── app.py                    # (Optional) Streamlit App
│── results/                  # Auto-generated CSVs + charts
│   ├── query_*.csv
│   ├── batch_results_summary_*.csv
│   ├── sales_profit_by_region_*.png
│   └── yearly_sales_*.png
```

---

## 📄 Requirements
All dependencies are listed in `requirements.txt`. Main libraries:
- `pandas`
- `numpy`
- `matplotlib`
- `transformers`
- `datasets`
- `sentencepiece`
- `kagglehub`
- `torch`

---

## 📌 Executive Summary
**What we built:** A grounded NL→SQL assistant for ad-hoc BI questions on the Superstore dataset.  
**Why it matters:** Reduces analyst dependency, speeds up exploratory analysis, and communicates insights with narratives and charts.  
**Proof:** Valid SQL generated for five canonical questions; charts and CSVs exported.  
**Risks:** Hallucinations and cost; mitigated with schema whitelists, fallback SQL, logging, and caches.  
**Next:** Add a semantic layer, CI test pack, and usage analytics; evaluate smaller domain-tuned models for cost/latency.  

---

👨‍💻 Author: **Sagar Murugesh Babu**  
📌 Repo: [LLM-s-in-Business-Intelligence](https://github.com/SagarTechTrends/LLM-s-in-Business-Intelligence)
