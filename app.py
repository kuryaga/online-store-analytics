import streamlit as st
import pandas as pd

st.title("Аналитический дашборд интернет-магазина")

uploaded_file = st.file_uploader("Загрузите CSV-файл", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Исходные данные")
    st.dataframe(df.head())

    st.subheader("Информация о данных")
    st.write("Размер таблицы:", df.shape)

    st.subheader("Пропущенные значения до обработки")
    st.write(df.isna().sum())

   
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"])

    
    df["city"] = df["city"].fillna("Unknown")
    df["payment_method"] = df["payment_method"].fillna("Unknown")

    df["quantity"] = df["quantity"].fillna(df["quantity"].median())
    df["price_per_unit"] = df["price_per_unit"].fillna(df["price_per_unit"].median())
    df["discount_percent"] = df["discount_percent"].fillna(0)


    df["revenue"] = df["quantity"] * df["price_per_unit"] * (1 - df["discount_percent"] / 100)


    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    st.session_state["df_clean"] = df

    st.subheader("Пропущенные значения после обработки")
    st.write(df.isna().sum())

    st.subheader("Очищенные данные")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    
    st.download_button(
    label="Скачать очищенные данные",
    data=csv,
    file_name="cleaned_data.csv",
    mime="text/csv"
)

    st.subheader("Основные показатели")

    total_revenue = round(df["revenue"].sum(), 2)
    total_orders = df["order_id"].nunique()
    average_order_value = round(df["revenue"].mean(), 2)
    total_customers = df.groupby(["customer_name", "city"]).ngroups

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Общая выручка", total_revenue)
    col2.metric("Количество заказов", total_orders)
    col3.metric("Средний чек", average_order_value)
    col4.metric("Количество клиентов", total_customers)

    st.subheader("Результаты анализа")
    popular_products = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
)
    revenue_by_category = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
    monthly_sales = (
    df.groupby("month")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
    top_customers = (
    df.groupby(["customer_name", "city"])["order_id"]
    .count()
    .sort_values(ascending=False)
)

    st.write("Самые популярные товары:")
    st.dataframe(popular_products)

    st.write("Выручка по категориям:")
    st.dataframe(revenue_by_category)

    st.write("Месяцы с наибольшей выручкой:")
    st.dataframe(monthly_sales)

    st.write("Клиенты с наибольшим количеством заказов:")
    st.dataframe(top_customers)


