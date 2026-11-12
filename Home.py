import streamlit as st
from db import get_connection
from ui import apply_style

st.set_page_config(page_title="Store Ledger", page_icon="▦", layout="wide")
apply_style()
st.title("Store ledger")
st.caption("A clear view of what is on your shelves and what has moved.")
st.divider()
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(quantity), 0), COALESCE(SUM(quantity * unit_price), 0) FROM items")
    item_types, units, stock_value = cursor.fetchone()
    cursor.execute("SELECT COALESCE(SUM(quantity * unit_price), 0) FROM sales")
    sales_value = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    a, b, c, d = st.columns(4)
    a.metric("Item types", item_types)
    b.metric("Units on hand", units)
    c.metric("Stock value", f"₹{stock_value:,.2f}")
    d.metric("Sales recorded", f"₹{sales_value:,.2f}")
    st.divider()
    st.subheader("Start with a task")
    st.write("Add stock, record a sale, print a customer bill, or review what is available from the pages in the sidebar.")
except Exception as error:
    st.error(f"Database connection failed: {error}")
