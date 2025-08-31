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
    csv_file = "data/superstore.csv"
    superstore = pd.read_csv(csv_file, encoding="latin1")

    # Fix dates
    superstore["Order Date"] = pd.to_datetime(superstore["Order Date"], errors="coerce")
    superstore["Ship Date"] = pd.to_datetime(superstore["Ship Date"], errors="coerce")

    # SQLite with thread-safe mode
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
    if "yearly profit" in q and "region" in q:
        return "SELECT strftime('%Y', [Order Date]) AS Year, Region, SUM(Profit) AS Total_Profit FROM superstore GROUP BY Year, Region ORDER BY Year;"
    if "discount" in q and "profit" in q:
        return "SELECT Discount, AVG(Profit) AS Avg_Profit FROM superstore GROUP BY Discount ORDER BY Discount;"
    if "ship mode" in q:
        return "SELECT [Ship Mode], SUM(Sales) AS Total_Sales, SUM(Profit) AS Total_Profit FROM superstore GROUP BY [Ship Mode];"
    if "segment performance" in q:
        return "SELECT Segment, SUM(Sales) AS Total_Sales, SUM(Profit) AS Total_Profit FROM superstore GROUP BY Segment;"
    if "most profitable sub-category" in q:
        return "SELECT [Sub-Category], SUM(Profit) AS Total_Profit FROM superstore GROUP BY [Sub-Category] ORDER BY Total_Profit DESC LIMIT 10;"
    if "state with highest sales" in q:
        return "SELECT State, SUM(Sales) AS Total_Sales FROM superstore GROUP BY State ORDER BY Total_Sales DESC LIMIT 10;"
    if "monthly sales" in q:
        return "SELECT strftime('%Y-%m', [Order Date]) AS Month, SUM(Sales) AS Total_Sales FROM superstore GROUP BY Month ORDER BY Month;"
    if "loss" in q:
        return "SELECT [Sub-Category], SUM(Profit) AS Total_Profit FROM superstore GROUP BY [Sub-Category] ORDER BY Total_Profit ASC LIMIT 10;"
    if "average shipping time" in q:
        return "SELECT AVG(julianday([Ship Date]) - julianday([Order Date])) AS Avg_Shipping_Time FROM superstore;"
    if "top 5 products" in q:
        return "SELECT [Product Name], SUM(Sales) AS Total_Sales FROM superstore GROUP BY [Product Name] ORDER BY Total_Sales DESC LIMIT 5;"
    if "total profit by customer segment" in q:
        return "SELECT Segment, SUM(Profit) AS Total_Profit FROM superstore GROUP BY Segment;"
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
st.write("Ask questions on the **Superstore dataset** using natural language.")

# Predefined questions
questions = [
    "Show total sales and profit by region.",
    "List the top 10 customers by total sales.",
    "Show profitability (profit margin) by product category.",
    "Show yearly sales totals from 2014 to 2017.",
    "Show yearly profit trend by region.",
    "Analyze how discount levels impact average profit.",
    "Show sales and profit by ship mode.",
    "Show segment performance in terms of sales and profit.",
    "List the top 10 most profitable sub-categories.",
    "Which states have the highest sales?",
    "Show monthly sales trends over time.",
    "List sub-categories with the highest losses.",
    "Calculate average shipping time.",
    "List top 5 products by total sales.",
    "Show total profit by customer segment."
]

user_query = st.selectbox("Pick a predefined question:", questions)

if st.button("Run Query"):
    sql, latency = hf_nl_to_sql(user_query)
    st.markdown(f"**Generated SQL:** `{sql}`")
    st.markdown(f"⏱️ Latency: {round(latency, 2)} seconds")

    result = run_sql(sql)

    if isinstance(result, pd.DataFrame):
        st.dataframe(result)

        # === Chart logic ===
        if "Region" in result.columns and "Total_Sales" in result.columns:
            fig, ax = plt.subplots()
            result.set_index("Region")[["Total_Sales", "Total_Profit"]].plot(kind="bar", ax=ax)
            ax.set_title("Sales & Profit by Region")
            ax.set_ylabel("Amount")
            st.pyplot(fig)

        elif "Customer Name" in result.columns and "Total_Sales" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="Customer Name", y="Total_Sales", kind="barh", ax=ax, legend=False)
            ax.set_title("Top 10 Customers by Sales")
            ax.set_xlabel("Total Sales")
            st.pyplot(fig)

        elif "Category" in result.columns and "Profit_Margin" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="Category", y="Profit_Margin", kind="bar", ax=ax, legend=False)
            ax.set_title("Profitability by Category")
            ax.set_ylabel("Profit Margin")
            st.pyplot(fig)

        elif "Year" in result.columns and "Total_Sales" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="Year", y="Total_Sales", kind="line", marker="o", ax=ax)
            ax.set_title("Yearly Sales Trend")
            ax.set_ylabel("Total Sales")
            st.pyplot(fig)

        elif "Year" in result.columns and "Total_Profit" in result.columns and "Region" in result.columns:
            fig, ax = plt.subplots()
            for region, data in result.groupby("Region"):
                ax.plot(data["Year"], data["Total_Profit"], marker="o", label=region)
            ax.set_title("Yearly Profit Trend by Region")
            ax.set_ylabel("Total Profit")
            ax.legend()
            st.pyplot(fig)

        elif "Discount" in result.columns and "Avg_Profit" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="Discount", y="Avg_Profit", kind="line", marker="o", ax=ax)
            ax.set_title("Impact of Discount on Profit")
            ax.set_ylabel("Average Profit")
            st.pyplot(fig)

        elif "Ship Mode" in result.columns:
            fig, ax = plt.subplots()
            result.set_index("Ship Mode")[["Total_Sales", "Total_Profit"]].plot(kind="bar", ax=ax)
            ax.set_title("Sales & Profit by Ship Mode")
            st.pyplot(fig)

        elif "Segment" in result.columns and "Total_Sales" in result.columns:
            fig, ax = plt.subplots()
            result.set_index("Segment")[["Total_Sales", "Total_Profit"]].plot(kind="bar", ax=ax)
            ax.set_title("Segment Performance")
            st.pyplot(fig)

        elif "Sub-Category" in result.columns and "Total_Profit" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="Sub-Category", y="Total_Profit", kind="barh", ax=ax, legend=False)
            ax.set_title("Top 10 Profitable Sub-Categories")
            ax.set_xlabel("Total Profit")
            st.pyplot(fig)

        elif "State" in result.columns and "Total_Sales" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="State", y="Total_Sales", kind="barh", ax=ax, legend=False)
            ax.set_title("Top States by Sales")
            ax.set_xlabel("Total Sales")
            st.pyplot(fig)

        elif "Month" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="Month", y="Total_Sales", kind="line", marker="o", ax=ax)
            ax.set_title("Monthly Sales Trend")
            st.pyplot(fig)

        elif "Avg_Shipping_Time" in result.columns:
            st.metric(label="Average Shipping Time (days)", value=round(result["Avg_Shipping_Time"].iloc[0], 2))

        elif "Product Name" in result.columns:
            fig, ax = plt.subplots()
            result.plot(x="Product Name", y="Total_Sales", kind="barh", ax=ax, legend=False)
            ax.set_title("Top 5 Products by Sales")
            st.pyplot(fig)

        elif "Segment" in result.columns and "Total_Profit" in result.columns:
            fig, ax = plt.subplots()
            result.set_index("Segment")["Total_Profit"].plot(kind="pie", autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")
            ax.set_title("Profit Share by Segment")
            st.pyplot(fig)
    else:
        st.error(result)
