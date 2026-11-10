import streamlit as st
from db import get_connection

st.set_page_config(page_title="Store Manager", page_icon="📦", layout="centered")
st.title("Store Manager")
st.subheader("A simple inventory and sales dashboard.")
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBcCpG2JN8Ljzv7wltsEiD39K2kcCB-mVuUiKsumi_xg&s=10")
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(quantity), 0) FROM items")
    item_types, units = cursor.fetchone()
    cursor.execute("SELECT COALESCE(SUM(quantity * unit_price), 0) FROM items")
    stock_value = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    a, b, c = st.columns(3)
    a.metric("Item types", item_types)
    b.metric("Units in stock", units)
    c.metric("Inventory value", f"₹{stock_value:,.2f}")
except Exception as e:
    st.error(f"Database connection failed: {e}")
