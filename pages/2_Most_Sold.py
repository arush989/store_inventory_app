import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

st.title("Most Sold Items")
conn = get_connection()
query = "SELECT i.name AS item, SUM(s.quantity) AS units_sold FROM sales s JOIN items i ON i.id = s.item_id GROUP BY i.id, i.name ORDER BY units_sold DESC"
df = pd.read_sql(query, conn)
conn.close()
if df.empty:
    st.info("No sales recorded yet.")
else:
    st.plotly_chart(px.bar(df, x="item", y="units_sold", title="Units sold by item", labels={"item": "Item", "units_sold": "Units sold"}), use_container_width=True)
    