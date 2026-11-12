import streamlit as st
import mysql.connector
from decimal import Decimal
from datetime import datetime

def get_connection():
    config = st.secrets["mysql"]
    return mysql.connector.connect(host=config["host"], port=config.get("port", 3306), user=config["user"], password=config["password"], database=config["database"])

def complete_bill(cart):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        checked = []
        total = Decimal("0.00")
        for item_id, line in cart.items():
            cursor.execute("SELECT name, quantity FROM items WHERE id = %s FOR UPDATE", (item_id,))
            item = cursor.fetchone()
            quantity = int(line["quantity"])
            if not item or item[1] < quantity:
                raise ValueError(f"Not enough stock for {line['name']}. Available: {item[1] if item else 0}.")
            price = Decimal(str(line["unit_price"]))
            amount = price * quantity
            total += amount
            checked.append({"item_id": item_id, "name": line["name"], "quantity": quantity, "unit_price": price, "amount": amount})
        cursor.execute("INSERT INTO bills (total) VALUES (%s)", (total,))
        bill_id = cursor.lastrowid
        for line in checked:
            cursor.execute("INSERT INTO bill_items (bill_id, item_id, item_name, quantity, unit_price) VALUES (%s, %s, %s, %s, %s)", (bill_id, line["item_id"], line["name"], line["quantity"], line["unit_price"]))
            cursor.execute("INSERT INTO sales (item_id, quantity, unit_price) VALUES (%s, %s, %s)", (line["item_id"], line["quantity"], line["unit_price"]))
            cursor.execute("UPDATE items SET quantity = quantity - %s WHERE id = %s", (line["quantity"], line["item_id"]))
        conn.commit()
        return {"id": bill_id, "number": f"INV-{bill_id:06d}", "created": datetime.now().strftime("%d %b %Y, %I:%M %p"), "items": checked, "total": total}
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
