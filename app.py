import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Звіт клієнта", layout="wide")

st.title("📊 Звіт по замовленнях клієнта")

# Підключення до бази
engine = create_engine(st.secrets["database"]["url"])

# Фільтри
with st.sidebar:
    st.header("Фільтри")
    date_from = st.date_input("Дата від", pd.Timestamp("2024-01-01"))
    date_to = st.date_input("Дата до", pd.Timestamp.today())
    client = st.text_input("Ім’я клієнта (необов’язково)")

# Побудова SQL-запиту
query = text("""
    SELECT * FROM orders
    WHERE order_date BETWEEN :start AND :end
    AND (:client = '' OR client_name ILIKE :client_pattern)
    ORDER BY order_date DESC
""")

params = {
    "start": date_from,
    "end": date_to,
    "client": client,
    "client_pattern": f"%{client}%"
}

# Отримання даних
with engine.connect() as conn:
    df = pd.read_sql(query, conn, params=params)

# Виведення
st.write(f"Знайдено записів: {len(df)}")
st.dataframe(df)

# (опційно) Графік
if not df.empty:
    df["order_date"] = pd.to_datetime(df["order_date"])
    chart = df.groupby("order_date").size()
    st.line_chart(chart)
