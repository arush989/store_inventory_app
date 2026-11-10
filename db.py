import streamlit as st
import mysql.connector

def get_connection():
    config = st.secrets["mysql"]
    return mysql.connector.connect(
        host=config["host"],
        port=config.get("port", 3306),
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )
