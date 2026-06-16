import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Визуализации данных")

if "df_clean" not in st.session_state:
    st.warning("Сначала загрузите CSV-файл на главной странице.")
else:
    df = st.session_state["df_clean"]

    # 1. Barplot — выручка по категориям
    st.subheader("Выручка по категориям товаров")

    revenue_by_category = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()

    sns.barplot(
        x=revenue_by_category.index,
        y=revenue_by_category.values,
        hue=revenue_by_category.index,
        palette="mako",
        legend=False,
        ax=ax
    )

    ax.set_title("Выручка по категориям товаров")
    ax.set_xlabel("Категория")
    ax.set_ylabel("Выручка")
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)

    st.write("Наибольшую выручку принесла категория Electronics.")


    # 2. Lineplot — динамика продаж по месяцам
    st.subheader("Динамика продаж по месяцам")

    monthly_sales_sorted = (
        df.groupby("month")["revenue"]
        .sum()
        .sort_index()
    )

    fig, ax = plt.subplots()

    sns.lineplot(
        x=monthly_sales_sorted.index,
        y=monthly_sales_sorted.values,
        ax=ax
    )

    ax.set_title("Динамика продаж по месяцам")
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Продажи")
    ax.tick_params(axis="x", rotation=90)

    st.pyplot(fig)

    st.write("Наибольшая выручка была в августе 2025 года.")


    # 3. Histogram — распределение выручки от заказов
    st.subheader("Распределение выручки от заказов")

    fig, ax = plt.subplots()

    sns.histplot(
        df["revenue"],
        bins=20,
        kde=True,
        ax=ax
    )

    ax.set_title("Распределение выручки от заказов")
    ax.set_xlabel("Выручка")
    ax.set_ylabel("Количество заказов")

    st.pyplot(fig)

    st.write("Большинство заказов имеют низкую или среднюю выручку, а дорогие заказы встречаются реже.")


    # 4. Pie chart — распределение методов оплаты
    st.subheader("Распределение методов оплаты")

    payment_count = df["payment_method"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        payment_count.values,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=1.15
    )

    ax.set_title("Распределение методов оплаты")
    ax.legend(payment_count.index, title="Метод оплаты", loc="best")

    st.pyplot(fig)

    st.write("График показывает распределение способов оплаты. Доля Unknown небольшая.")


    # 5. Barplot — самые популярные товары
    st.subheader("Самые популярные товары")

    top_products = (
        df.groupby("product_name")["quantity"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()

    sns.barplot(
        x=top_products.index,
        y=top_products.values,
        hue=top_products.index,
        palette="viridis",
        legend=False,
        ax=ax
    )

    ax.set_title("Самые популярные товары")
    ax.set_xlabel("Товары")
    ax.set_ylabel("Количество продано")
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)

    st.write("Самым популярным товаром оказался Keyboard.")