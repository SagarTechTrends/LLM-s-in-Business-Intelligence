# app.py
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import re, time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# =========================
# Load dataset into SQLite
# =========================
@st.cache_resource
def load_db():
    csv_file = "data/superstore.csv"  # ensure file is in data/ folder
    superstore = pd.read_csv(csv_file, encoding="latin1")

    # Fix dates
    superstore["Order Date"] = pd.to_datetime(superstore["Order Date"], errors="coerce")
    superstore["Ship Date"] = pd.to_datetime(superstore["Ship Date"], errors="coerce")

    # SQLite in-memory DB
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    superstore.to_sql("superstore", conn, if_exists="replace", index=False)
    return conn

conn = load_db()

# =========================
# Hugging Face model
# =========================
@st.cache_resource
def load_model():
    model_id = "mrm8488/t5-base-finetuned-wikiSQL"
    tokenizer = AutoTokenizer.from_pretrained(model_id, legacy=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)

hf_generator = load_model()

# =========================
# Example Questions
# =========================
example_questions = [
    "Show total sales and profit by region.",
    "List the top 10 customers by total sales.",
    "Show profitability (profit margin) by product category.",
    "Show yearly sales totals from 2014 to 2017.",
    "Analyze how discount levels impact average profit.",
    "Which sub-category has the highest sales?",
    "Show total sales by shipping mode.",
    "List top 5 states by total profit.",
    "Show monthly sales trend for 2017.",
    "Compare average discount by region."
]

# =========================
# Helpers
# =========================
def safe_fallback(nl_query: str):
    q = nl_query.lower()
    if "sales and profit by region" in q:
        return "SELECT Region, SUM(Sales) AS Total_Sales, SUM(Profit) AS Total_Profit FROM superstore GROUP BY Region;"
    if "top 10 customers" in q:
        return "SELECT [Customer Name], SUM(Sales) AS Total_Sales FROM superstore GROUP BY [Customer Name] ORDER BY Total_Sales DESC LIMIT 10;"
    if "profitability" in q and "category" in q:
        return "SELECT Category, SUM(Profit)/SUM(Sales) AS Profit_Margin FROM superstore GROUP BY Category;"
    if "yearly sales" in q:
        return "SELECT strftime('%Y', [Order Date]) AS Year, SUM(Sales) AS Total_Sales FROM superstore GROUP BY Year ORDER BY Year;"
    if "discount" in q and "profit" in q:
        return "SELECT Discount, AVG(Profit) AS Avg_Profit FROM superstore GROUP BY Discount ORDER BY Discount;"
    if "sub-category" in q:
        return "SELECT [Sub-Category], SUM(Sales) AS Total_Sales FROM superstore GROUP BY [Sub-Category] ORDER BY Total_Sales DESC LIMIT 1;"
    if "shipping mode" in q:
        return "SELECT [Ship Mode], SUM(Sales) AS Total_Sales FROM superstore GROUP BY [Ship Mode];"
    if "top 5 states" in q:
        return "SELECT State, SUM(Profit) AS Total_Profit FROM superstore GROUP BY State ORDER BY Total_Profit DESC LIMIT 5;"
    if "monthly sales trend" in q:
        return "SELECT strftime('%Y-%m', [Order Date]) AS Month, SUM(Sales) AS Total_Sales FROM superstore WHERE strftime('%Y',[Order Date])='2017' GROUP BY Month ORDER BY Month;"
    if "average discount by region" in q:
        return "SELECT Region, AVG(Discount) AS Avg_Discount FROM superstore GROUP BY Region;"
    return None

def hf_nl_to_sql(nl_query):
    prompt = f"""
    You are an expert SQLite SQL assistant.
    Convert the following natural language query into valid SQL.
    Table: superstore
    Columns: "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
             "Customer ID", "Customer Name", "Segment", "Country", "City",
             "State", "Postal Code", "Region", "Product ID", "Category",
             "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit"
    NL Query: {nl_query}
    SQL:
    """
    start = time.time()
    response = hf_generator(prompt, max_new_tokens=200, do_sample=False)
    latency = time.time() - start
    raw_sql = response[0]["generated_text"].strip()

    match = re.search(r"(SELECT[\s\S]*?)(;|$)", raw_sql, re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
        if not sql.endswith(";"):
            sql += ";"
    else:
        sql = safe_fallback(nl_query)
    return sql, latency

def run_sql(query):
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        return f"SQL Error: {e}"

# =========================
# Streamlit UI
# =========================
st.title("🧠 LLMs in Business Intelligence")
st.write("Ask natural language queries on the **Superstore dataset** and see results with SQL + charts.")

choice = st.selectbox("Choose an example question:", ["(Custom)"] + example_questions)
if choice == "(Custom)":
    user_query = st.text_input("Or type your own question:")
else:
    user_query = choice

if st.button("Run Query") and user_query:
    sql, latency = hf_nl_to_sql(user_query)
    st.markdown(f"**Generated SQL:** `{sql}`")
    st.markdown(f"⏱️ Latency: {round(latency, 2)} seconds")

    result = run_sql(sql)

    if isinstance(result, pd.DataFrame) and not result.empty:
        st.dataframe(result)

        # Simple chart logic
        if "Region" in result.columns and "Total_Sales" in result.columns:
            st.bar_chart(result.set_index("Region")[["Total_Sales", "Total_Profit"]] if "Total_Profit" in result.columns else result.set_index("Region")[["Total_Sales"]])
        elif "Year" in result.columns and "Total_Sales" in result.columns:
            st.line_chart(result.set_index("Year")["Total_Sales"])
        elif "Month" in result.columns and "Total_Sales" in result.columns:
            st.line_chart(result.set_index("Month")["Total_Sales"])
        elif "State" in result.columns and "Total_Profit" in result.columns:
            st.bar_chart(result.set_index("State")["Total_Profit"])
        elif "Ship Mode" in result.columns and "Total_Sales" in result.columns:
            st.bar_chart(result.set_index("Ship Mode")["Total_Sales"])
    else:
        st.error(result)
