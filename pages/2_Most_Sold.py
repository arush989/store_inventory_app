import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection
from ui import apply_style

apply_style()
st.title("Sales report")
st.caption("Items ranked by the number of units sold.")
conn = get_connection()
df = pd.read_sql("SELECT item_id, MAX(items.name) AS item, SUM(sales.quantity) AS units_sold FROM sales JOIN items ON items.id = sales.item_id GROUP BY item_id ORDER BY units_sold DESC", conn)
conn.close()
if df.empty:
    st.info("No completed bills yet.")
else:
    st.plotly_chart(px.bar(df, x="item", y="units_sold", labels={"item": "Item", "units_sold": "Units sold"}, color_discrete_sequence=["#a64c34"]), use_container_width=True)
    st.dataframe(df[["item", "units_sold"]], use_container_width=True, hide_index=True)
