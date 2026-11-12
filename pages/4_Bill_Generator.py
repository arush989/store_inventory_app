import streamlit as st
import pandas as pd
from db import complete_bill
from ui import apply_style, receipt_html

apply_style()
st.title("Bill generator")
cart = st.session_state.setdefault("cart", {})
saved = st.session_state.get("generated_bill")
if saved:
    st.caption(f"{saved['number']} · {saved['created']}")
    st.dataframe(pd.DataFrame([{"Item": x["name"], "Qty": x["quantity"], "Unit price": float(x["unit_price"]), "Amount": float(x["amount"])} for x in saved["items"]]), use_container_width=True, hide_index=True)
    st.metric("Bill total", f"₹{saved['total']:,.2f}")
    if st.button("Print bill & start next bill", type="primary"):
        st.components.v1.html(receipt_html(saved), height=720, scrolling=True)
        st.session_state.generated_bill = None
        st.session_state.cart = {}
        st.success("Bill printed. The current bill has been cleared.")
elif not cart:
    st.info("Your bill is empty. Choose Sell item from Stock movements to add products.")
else:
    lines = [{"Item": v["name"], "Qty": v["quantity"], "Unit price": float(v["unit_price"]), "Amount": v["quantity"] * float(v["unit_price"])} for v in cart.values()]
    st.dataframe(pd.DataFrame(lines), use_container_width=True, hide_index=True)
    st.metric("Current total", f"₹{sum(x['Amount'] for x in lines):,.2f}")
    if st.button("Generate bill", type="primary"):
        try:
            st.session_state.generated_bill = complete_bill(cart)
            st.session_state.cart = {}
            st.rerun()
        except Exception as error:
            st.error(f"Could not generate bill: {error}")
    if st.button("Clear current bill"):
        st.session_state.cart = {}
        st.rerun()
