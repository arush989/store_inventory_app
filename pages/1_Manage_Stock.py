import streamlit as st
from db import get_connection
from ui import apply_style

apply_style()
st.title("Stock movements")
mode = st.radio("Choose an action", ["Add stock", "Remove stock", "Sell item"], horizontal=True)
conn = get_connection()
cursor = conn.cursor()
if mode == "Add stock":
    with st.form("add_stock"):
        name = st.text_input("Item name")
        quantity = st.number_input("Quantity to add", min_value=1, step=1)
        price = st.number_input("Unit price (₹)", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add stock")
    if submitted and name.strip():
        cursor.execute("INSERT INTO items (name, quantity, unit_price) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity), unit_price = VALUES(unit_price)", (name.strip(), quantity, price))
        conn.commit()
        st.success("Stock updated.")
elif mode in ["Remove stock", "Sell item"]:
    cursor.execute("SELECT id, name, quantity, unit_price FROM items WHERE quantity > 0 ORDER BY name")
    items = cursor.fetchall()
    if items:
        chosen = st.selectbox("Choose item", items, format_func=lambda x: f"{x[1]} · {x[2]} available")
        qty = st.number_input("Quantity", min_value=1, max_value=int(chosen[2]), step=1)
        if st.button("Add to bill" if mode == "Sell item" else "Remove stock"):
            if mode == "Sell item":
                cart = st.session_state.setdefault("cart", {})
                line = cart.get(chosen[0], {"name": chosen[1], "quantity": 0, "unit_price": str(chosen[3])})
                if line["quantity"] + qty > chosen[2]:
                    st.error("The bill quantity is greater than available stock.")
                else:
                    line["quantity"] += qty
                    cart[chosen[0]] = line
                    st.switch_page("pages/4_Bill_Generator.py")
            else:
                cursor.execute("UPDATE items SET quantity = quantity - %s WHERE id = %s AND quantity >= %s", (qty, chosen[0], qty))
                conn.commit()
                st.success("Stock removed.")
    else:
        st.info("No stock available.")
cursor.close()
conn.close()
