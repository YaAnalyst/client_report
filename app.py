import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="client_report", layout="wide")

st.title("aduniverse_c032")

# Введення client_id
client_id = st.text_input("Введіть ваш Client ID:", "C032")

if client_id:
    try:
        # Параметри підключення
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="agency_db",     # ← заміни на назву твоєї бази
            user="aduniverse",       # ← заміни на ім’я користувача
            password="your_password"  # ← заміни на свій пароль
        )

        query = """
            SELECT * FROM AdUniverse_C032
            WHERE client_id = %s
            ORDER BY transaction_date DESC;
        """

        df = pd.read_sql(query, conn, params=[client_id])
        conn.close()

        if not df.empty:
            st.success(f"Показуємо дані для: {client_id}")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Даних не знайдено для цього клієнта.")
    except Exception as e:
        st.error(f"Помилка підключення або запиту: {e}")
else:
    st.info("Введіть ваш Client ID, щоб побачити дані.")
