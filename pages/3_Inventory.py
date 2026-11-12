import streamlit as st
import pandas as pd
from db import get_connection
from ui import apply_style

apply_style()
st.title("Inventory")
st.caption("Current stock, item prices, and stock value.")
conn = get_connection()
df = pd.read_sql("SELECT name AS Item, quantity AS Quantity, unit_price AS `Unit price (₹)`, quantity * unit_price AS `Stock value (₹)` FROM items ORDER BY name", conn)
conn.close()
if df.empty:
    st.info("Inventory is empty.")
else:
    st.metric("Total units", int(df["Quantity"].sum()))
    st.dataframe(df, use_container_width=True, hide_index=True)
