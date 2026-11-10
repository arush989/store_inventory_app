import streamlit as st
from db import get_connection
st.title("Add / Remove / Sell")
mode = st.radio(
    "Action",
    ["Add item", "Remove stock", "Sell item"],
    horizontal=True
)
conn = get_connection()
cursor = conn.cursor()
if mode == "Add item":
    with st.form("add"):
        name = st.text_input("Item name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Unit price (₹)", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add to inventory")
    if submitted:
        if name.strip():
            cursor.execute(
                """INSERT INTO items (name, quantity, unit_price)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                quantity = quantity + VALUES(quantity),
                unit_price = VALUES(unit_price)""",
                (name.strip(), quantity, price)
            )
            conn.commit()
            st.success("Stock added successfully.")
        else:
            st.warning("Please enter an item name.")
elif mode in ["Remove stock", "Sell item"]:
    cursor.execute("SELECT id, name, quantity FROM items ORDER BY name")
    items = cursor.fetchall()
    if items:
        chosen = st.selectbox(
            "Item",
            items,
            format_func=lambda x: f"{x[1]} ({x[2]} available)"
        )
        available_stock = int(chosen[2])
        if available_stock <= 0:
            st.warning("This item is out of stock. No stock can be removed or sold.")
        else:
            qty = st.number_input(
                "Quantity",
                min_value=1,
                max_value=available_stock,
                value=1,
                step=1
            )
            if st.button(mode):
                cursor.execute(
                    "UPDATE items SET quantity = quantity - %s WHERE id = %s AND quantity >= %s",
                    (qty, chosen[0], qty)
                )
                if cursor.rowcount > 0:
                    if mode == "Sell item":
                        cursor.execute(
                            """INSERT INTO sales (item_id, quantity, unit_price)
                            SELECT id, %s, unit_price
                            FROM items WHERE id = %s""",
                            (qty, chosen[0])
                        )
                    conn.commit()
                    if mode == "Sell item":
                        st.success("Sale recorded successfully.")
                    else:
                        st.success("Stock removed successfully.")
                    st.rerun()
                else:
                    conn.rollback()
                    st.error("Insufficient stock or inventory was updated. Please try again.")
    else:
        st.info("No items in inventory yet.")
cursor.close()
conn.close()