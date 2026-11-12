import streamlit as st
from html import escape

def apply_style():
    st.markdown("""
    <style>
    .stApp { background: #f6f4ee; color: #242a26; }
    [data-testid="stSidebar"] { background: #eae7de; border-right: 1px solid #d3d0c7; }
    [data-testid="stSidebar"] * { color: #242a26; }
    .block-container { max-width: 1180px; padding-top: 2.4rem; padding-bottom: 3rem; }
    h1, h2, h3 { font-family: Georgia, serif !important; color: #202722; letter-spacing: -0.035em; }
    h1 { font-size: 2.65rem !important; font-weight: 500 !important; }
    h2 { font-size: 1.8rem !important; font-weight: 500 !important; }
    p, label, input, button, [data-testid="stMetricLabel"] { font-family: Arial, sans-serif; }
    [data-testid="stMetric"] { background: transparent; border-top: 2px solid #343d36; padding: 0.8rem 0 0.4rem; }
    [data-testid="stMetricValue"] { font-family: Georgia, serif; font-size: 1.8rem; }
    div.stButton > button, div.stFormSubmitButton > button { border-radius: 2px; border: 1px solid #28332d; background: #28332d; color: #fffdf7; padding: 0.55rem 1.1rem; min-height: 2.6rem; }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover { border-color: #a64c34; background: #a64c34; color: white; }
    [data-baseweb="input"] input, [data-baseweb="select"] > div, [data-baseweb="textarea"] textarea { border-radius: 2px !important; background: #fffefa; }
    [data-testid="stDataFrame"], [data-testid="stTable"] { border-top: 1px solid #cbc8bf; }
    hr { border-color: #d3d0c7; }
    </style>
    """, unsafe_allow_html=True)

def receipt_html(bill):
    rows = "".join(f"<tr><td>{escape(line['name'])}</td><td>{line['quantity']}</td><td>₹{line['unit_price']:,.2f}</td><td>₹{line['amount']:,.2f}</td></tr>" for line in bill["items"])
    return f"""<html><head><style>body {{ font: 14px Arial,sans-serif; color:#222; padding:24px; }} .receipt {{ max-width:700px; margin:auto; }} h1 {{ font:28px Georgia,serif; }} .muted {{ color:#666; font-size:12px; }} table {{ width:100%; border-collapse:collapse; margin-top:24px; }} th,td {{ text-align:left; padding:10px 5px; border-bottom:1px solid #ddd; }} th {{ font-size:11px; text-transform:uppercase; }} .total {{ text-align:right; font-size:20px; font-weight:bold; margin-top:20px; }} @media print {{ body {{ padding:0; }} }}</style></head><body><main class="receipt"><h1>Store receipt</h1><div class="muted">{bill['number']} · {bill['created']}</div><table><thead><tr><th>Item</th><th>Qty</th><th>Price</th><th>Amount</th></tr></thead><tbody>{rows}</tbody></table><div class="total">Total: ₹{bill['total']:,.2f}</div><p class="muted">Thank you for shopping with us.</p></main><script>window.onload = () => window.print();</script></body></html>"""
