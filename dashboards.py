import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",", parse_dates=["Date"])
df.sort_values("Date", inplace=True)
df["Month"] = df["Date"].apply(lambda x: f"{x.year}-{x.month}")

st.set_page_config(layout="wide")
st.title("Relatórios")
st.sidebar.title("Filtros")

month = st.sidebar.selectbox("Mês", df["Month"].unique())
# TODO start this multiselect with all options selected
city = st.sidebar.multiselect("City", df["City"].unique(), df["City"].unique())
payment = st.sidebar.multiselect("Payment", df["Payment"].unique(), df["Payment"].unique())
gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), df["Gender"].unique())

df_filtered = df
if month: df_filtered = df_filtered[df_filtered["Month"] == month]
if city: df_filtered = df_filtered[df_filtered["City"].isin(city)]
if payment: df_filtered = df_filtered[df_filtered["Payment"].isin(payment)]
if gender: df_filtered = df_filtered[df_filtered["Gender"].isin(gender)]

city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
fig_prod = px.bar(df_filtered, x="Date", y="Product line", color="City", title="Faturamento por tipo de produto", orientation="h")
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por filial")
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
fig_rating = px.bar(df_filtered, y="Rating", x="City", title="Avaliação")

col1.plotly_chart(fig_date, use_container_width=True)
col2.plotly_chart(fig_prod, use_container_width=True)
col3.plotly_chart(fig_city, use_container_width=True)
col4.plotly_chart(fig_kind, use_container_width=True)
col5.plotly_chart(fig_rating, use_container_width=True)

df_filtered.sort_values("Total", ascending=False, inplace=True)
# todo add a title to the table to show the top 5 totals
st.dataframe(df_filtered.head(5), title="Top 5 Faturamentos")
