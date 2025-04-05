import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv("shopping_trends_updated.csv")

#Título da página
st.title("Análise das Trends de mercado Norte Americano🛒")

# Criação das Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Vendas por Gênero", "Vendas por Categoria", "Vendas por Região",
    "Vendas por Temporada", "Envios e Cupons", "Satisfação do Cliente"
])

# Vendas por Gênero
with tab1:
    #Filtro de gênero
    gender_filter = st.multiselect("Selecione o(s) gênero(s):", options=df["Gender"].unique(), default=df["Gender"].unique())
    df_gender = df[df["Gender"].isin(gender_filter)]

    st.subheader("Compras por Gênero")
    fig1 = px.histogram(df_gender, x="Gender", color="Gender", title="Número de Compras por Gênero")
    st.plotly_chart(fig1)

    #Define os valores mínimos e máximos de idade dentro do DataFrame
    min_age, max_age = int(df_gender["Age"].min()), int(df_gender["Age"].max())
    #Permite a seleção da idade mínima e máxima dentro do definido no slider
    idade_range = st.slider("Selecione a faixa etária:", min_value=min_age, max_value=max_age, value=(min_age, max_age))

    # Filtro de idade
    df_filtered_age = df_gender[(df_gender["Age"] >= idade_range[0]) & (df_gender["Age"] <= idade_range[1])]

    st.subheader("Gasto por Idade e Gênero")
    fig2 = px.scatter(df_filtered_age, x="Age", y="Purchase Amount (USD)", color="Gender",
                  title="Distribuição do Gasto por Idade (filtrado)")
    st.plotly_chart(fig2)

# Vendas por Categoria
with tab2:
    #Filtro de categoria
    category_filter = st.multiselect("Selecione categoria(s):", df['Category'].unique(), default=df['Category'].unique())
    df_category = df[df["Category"].isin(category_filter)]

    st.subheader("Número de compras por categoria")
    fig3 = px.histogram(df_category, x="Category")
    st.plotly_chart(fig3)

    st.subheader("Avaliação média por categoria")
    fig4 = px.bar(df_category, x="Category", y="Review Rating")
    st.plotly_chart(fig4)

with tab3:
    #Filtro por região
    location_filter = st.multiselect("Filtrar por localização:", df["Location"].unique(), default=df["Location"].unique()[:3])
    df_loc = df[df["Location"].isin(location_filter)]

    st.subheader("Compras por Estado")
    #Criação de um DataFrame auxiliar para salvar somente os valores utilizados
    location_counts = df_loc["Location"].value_counts().reset_index()
    location_counts.columns = ["Localização", "Compras"]
    
    #Gráfico
    fig5 = px.bar(location_counts, x="Localização", y="Compras")
    st.plotly_chart(fig5)

    st.subheader("Métodos de Pagamento por Região")
    fig6 = px.histogram(df_loc, x="Payment Method", color="Location", barmode="group")
    st.plotly_chart(fig6)

with tab4:
    #Filtro por temporada
    season_filter = st.multiselect("Filtrar por temporada: ", df["Season"].unique(), default=df["Season"].unique()[:2])
    df_season = df[df["Season"].isin(season_filter)]

    st.subheader("Compras por temporada: ")
    #Assim como o anterior, criação de um DataFrame auxiliar
    season_count = df_season["Season"].value_counts().reset_index()
    season_count.columns = ["Temporada", "Compras"]

    fig7 = px.bar(season_count, x="Temporada", y="Compras")
    st.plotly_chart(fig7)

    st.subheader("Gasto Médio por Temporada")
    #Outro DataFrame auxiliar
    avg_spending = df_season.groupby("Season")["Purchase Amount (USD)"].mean().reset_index()
    avg_spending.columns = ["Temporada", "Gasto Médio"]

    fig8 = px.bar(avg_spending, x="Temporada", y="Gasto Médio")
    st.plotly_chart(fig8)

with tab5:
    #Filtro por tipo de envio
    shipping_filter = st.multiselect("Tipo de envio:", df["Shipping Type"].unique(), default=df["Shipping Type"].unique()[:3])
    df_ship = df[df["Shipping Type"].isin(shipping_filter)]

    st.subheader("Uso de Cupom por Tipo de Envio")

    df_cupom_envio = df_ship.groupby(["Shipping Type", "Promo Code Used"]).size().reset_index(name="Count")

    fig9 = px.bar(df_cupom_envio, x="Shipping Type", y="Count", color="Promo Code Used", labels={"Promo Code Used": "Usou Cupom?"})
    st.plotly_chart(fig9)

    st.subheader("Gasto Médio por Tipo de Envio")

    df_gasto_envio = df_ship.groupby("Shipping Type")["Purchase Amount (USD)"].mean().reset_index()

    fig10 = px.bar(df_gasto_envio, x="Shipping Type", y="Purchase Amount (USD)", labels={"Purchase Amount (USD)": "Gasto Médio (USD)"})
    st.plotly_chart(fig10)

with tab6:
    #Filtro com slider para tipo de avaliação
    rating_selected = st.slider("Escolha uma avaliação (1 a 5 estrelas):", 1, 5, 5)

    df_rating = df[df["Review Rating"] == rating_selected]

    st.subheader("Compras por Categoria")
    #DataFrame auxiliar
    cat_rating = df_rating["Category"].value_counts().reset_index()
    cat_rating.columns = ["Categoria", "Compras"]

    fig1 = px.bar(cat_rating, x="Categoria", y="Compras", title=f"Categorias para Avaliação {rating_selected}⭐")
    st.plotly_chart(fig1)

    st.subheader("Gasto Médio por Tipo de Envio")
    #DataFrame auxiliar
    envio_rating = df_rating.groupby("Shipping Type")["Purchase Amount (USD)"].mean().reset_index()

    fig2 = px.bar(envio_rating, x="Shipping Type", y="Purchase Amount (USD)", title=f"Gasto Médio por Tipo de Envio ({rating_selected}⭐)", labels={"Purchase Amount (USD)": "Gasto Médio (USD)"})
    st.plotly_chart(fig2)