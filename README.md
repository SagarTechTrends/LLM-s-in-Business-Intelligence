# LLMs in Business Intelligence 🚀

This project demonstrates how **Large Language Models (LLMs)** can be applied in **Business Intelligence (BI)** workflows by translating **natural language (NL) queries** into **SQL queries**, running them on the popular **Superstore dataset**, and visualizing the results with Python + SQLite.

---

## 📌 Features
- ✅ NL → SQL generation using Hugging Face (`t5-base-finetuned-wikiSQL`).
- ✅ Fallback SQL templates for reliability.
- ✅ Executable SQL queries on the Superstore dataset (via SQLite).
- ✅ Export results to CSV for further analysis.
- ✅ Visualization of insights with Matplotlib (e.g., sales by region, yearly sales).
- ✅ Organized results folder with timestamped charts & logs.

---

## 📊 Example Queries
- **"Show total sales and profit by region."**
- **"List the top 10 customers by total sales."**
- **"Show profitability (profit margin) by product category."**
- **"Show yearly sales totals from 2014 to 2017."**
- **"Analyze how discount levels impact average profit."**

---

## 📂 Repository Structure
```
LLM-s-in-Business-Intelligence/
│
├── notebooks/                # Jupyter notebooks
├── results/                  # CSV exports + charts (auto-generated)
│   ├── nl_sql_results_*.csv
│   ├── sales_profit_by_region_*.png
│   └── yearly_sales_*.png
├── Sales & Profit by Region.png   # Sample chart
├── Yearly Sales.png               # Sample chart
├── nl_sql_results.csv             # Example results log
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview (this file)
```

---

## 🛠️ Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/SagarTechTrends/LLM-s-in-Business-Intelligence.git
   cd LLM-s-in-Business-Intelligence
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # on Linux/Mac
   myenv\Scripts\activate     # on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📈 Sample Outputs

### Sales & Profit by Region
![Sales & Profit by Region](Sales%20&%20Profit%20by%20Region.png)

### Yearly Sales (2014–2017)
![Yearly Sales](Yearly%20Sales.png)

---

## 📄 Dataset
- **Sample - Superstore** (public dataset, available on [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final))  
- Contains ~10k rows with attributes like `Order Date`, `Ship Date`, `Region`, `Category`, `Sales`, `Profit`, etc.

---

## 🚀 Future Enhancements
- Add semantic layer for schema understanding.
- Evaluate smaller domain-tuned models for faster/cheaper inference.
- Integrate with BI dashboards (Power BI, Tableau, Streamlit).
- CI test pack for generated SQL queries.

---

## 👨‍💻 Author
**Sagar Murugesh Babu**  
🎓 M.S. Information Technology Management, University of Wisconsin–Milwaukee  
🔗 [LinkedIn](https://www.linkedin.com/in/sagar-murugesh-babu-1a3454123/) | [GitHub](https://github.com/SagarTechTrends)
