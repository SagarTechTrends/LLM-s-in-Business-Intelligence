# =========================
# Streamlit UI
# =========================
st.title("🧠 LLMs in Business Intelligence")
st.write("Ask natural language queries on the **Superstore dataset** and see results with SQL + charts.")

# Example questions
example_queries = [
    "Show total sales and profit by region.",
    "List the top 10 customers by total sales.",
    "Show profitability (profit margin) by product category.",
    "Show yearly sales totals from 2014 to 2017.",
    "Analyze how discount levels impact average profit."
]

# Let user pick from dropdown or type their own
selected_query = st.selectbox("Choose an example question:", ["-- Type your own --"] + example_queries)
custom_query = st.text_input("Or enter your own question:")

# Final query
if selected_query != "-- Type your own --":
    user_query = selected_query
else:
    user_query = custom_query

if st.button("Run Query") and user_query:
    sql, latency = hf_nl_to_sql(user_query)
    st.markdown(f"**Generated SQL:** `{sql}`")
    st.markdown(f"⏱️ Latency: {round(latency, 2)} seconds")

    result = run_sql(sql)

    if isinstance(result, pd.DataFrame):
        st.dataframe(result)

        # Simple chart logic
        if "Region" in result.columns and "Total_Sales" in result.columns:
            st.bar_chart(result.set_index("Region")[["Total_Sales", "Total_Profit"]])
        elif "Year" in result.columns and "Total_Sales" in result.columns:
            st.line_chart(result.set_index("Year")["Total_Sales"])
    else:
        st.error(result)
