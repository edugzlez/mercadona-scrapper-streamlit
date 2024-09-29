from glob import glob

import pandas as pd
import plotly.express as px
import streamlit as st
from mdona_scrapper import MercadonaScrapper


def get_category(name):
    # Definir palabras clave para cada categoría
    categorias = {
        "Frutas y verduras": [
            "mandarina",
            "plátano",
            "zanahoria",
            "cebolla",
            "ajos",
            "aguacate",
            "manzana",
            "calabaza",
            "tomate",
            "pimiento",
            "patatas",
            "pepino",
            "pera",
            "fresas",
            "remolacha",
            "calabacín",
            "champiñón",
            "judías",
            "puerro",
            "espinaca",
            "verduras",
            "arandanos",
            "melocotones",
            "gazpacho",
            "melocotón",
            "uva blanca",
            "uva roja",
            "piña",
            "cereza",
            "albaricoque",
            "banana",
            "pomelos",
        ],
        "Carnes y embutidos": [
            "pollo",
            "vacuno",
            "cerdo",
            "lomo",
            "salchichón",
            "chorizo",
            "longaniza",
            "jamón",
            "pavo",
            "embuchado",
            "burger",
            "salchicha",
            "compango",
            "morcilla",
            "costilla",
            "bacon",
            "york",
            "chistorra",
            "fuet",
            "bacón",
            "ternera",
        ],
        "Pescados y mariscos": [
            "bacalao",
            "pota",
            "atún",
            "merluza",
            "berberecho",
            "mejillón",
            "calamar",
            "chipirón",
            "almejas",
            "caballa",
        ],
        "Lácteos y huevos": [
            "yogur",
            "nata",
            "queso",
            "huevos",
            "mantequilla",
            "margarina",
            "leche",
            "mozarella",
            "brie",
            "mozzarella",
        ],
        "Panadería y bollería": [
            "sobao",
            "magdalena",
            "pan",
            "barra",
            "molde",
            "torta",
            "empanadilla",
            "harina",
        ],
        "Cereales, pasta y legumbres": [
            "pasta",
            "macarrón",
            "spaghetti",
            "fusilli",
            "tortellini",
            "lenteja",
            "garbanzo",
            "arroz",
            "fideos",
            "nidos",
            "cereal",
            "copos",
            "granola",
            "alubia",
            "hélices",
            "tortiglioni",
            "penne",
            "hélices",
            "fideo",
            "nidos al huevo",
            "pajaritas vegetales",
            "gnocchi",
            "tallarín",
            "trottole",
            "cocktail",
        ],
        "Aceites y vinagres": [
            "aceite",
            "oliva",
            "girasol",
        ],
        "Salsas y condimentos": [
            "tomate",
            "curry",
            "mayonesa",
            "ketchup",
            "pesto",
            "sal",
            "pimienta",
            "cúrcuma",
            "ajo",
            "perejil",
            "comino",
            "colorante",
            "salsa",
            "vinagre",
            "mostaza",
            "alioli",
            "romero",
        ],
        "Bebidas": [
            "zumo",
            "bebida",
            "vino",
            "agua",
            "refresco",
            "café",
            "infusión",
            "té",
            "tinto",
        ],
        "Dulces y snacks": [
            "flan",
            "galletas",
            "chocolate",
            "turrón",
            "caramelo",
            "barritas",
            "mermelada",
            "helado",
            "cacahuete",
            "nuez",
            "anacardo",
            "picos",
            "regañá",
            "palomita",
            "almendra",
            "muesli crunchy",
            "golosinas",
            "chicle",
            "rosquillas",
            "nachos",
        ],
        "Productos de limpieza": [
            "lavavajillas",
            "detergente",
            "suavizante",
            "lejía",
            "limpiador",
            "estropajo",
            "bayeta",
            "friegasuelos",
            "ambientador",
            "limipiagafas",
        ],
        "Higiene personal": [
            "pañuelos",
            "desodorante",
            "dentífrico",
            "jabón",
            "maquinilla",
            "povidona",
            "gel de baño",
            "papel higiénico",
            "cápsulas",
            "bastoncillos",
            "esponja",
        ],
        "Productos de hogar": [
            "bolsa de basura",
            "papel de cocina",
            "pinzas",
            "colgador",
            "set antihumedad",
            "fregona",
            "recambio",
            "hielo",
            "plástico",
            "bosque verde",
            "papel cocina",
            "servilleta",
        ],
        "Edulcorantes": [
            "azúcar",
            "miel",
            "sacarina",
            "stevia",
            "panela",
            "edulcorante",
        ],
        "Enlatados y conservas": [
            "atún",
            "sardina",
            "tomate",
            "maíz",
            "guisante",
            "garbanzo",
            "lenteja",
            "pimiento",
            "aceituna",
            "alubia",
            "espárrago",
            "berberecho",
            "mejillón",
            "calamar",
            "chipirón",
            "almejas",
            "caballa",
            "pulpo",
            "callos",
            "fabada",
            "pisto",
            "gazpacho",
            "crema",
            "sopa",
            "conserva",
            "enlatado",
        ],
        "Platos preparados": [
            "pizza",
            "lasaña",
            "canelones",
            "sushi",
            "tabulé",
            "albóndigas",
            "patata para micro",
        ],
    }

    # Convertir el nombre del producto a minúsculas para evitar errores de capitalización
    name = name.lower()

    # Buscar la categoría correspondiente
    for categoria, keywords in categorias.items():
        if any(keyword in name for keyword in keywords):
            return categoria

    # Si no coincide con ninguna categoría, retornamos 'Desconocido'
    return "Otros"


st.title("Mercadona Scrapper")


macro_data_frame = pd.DataFrame()

docs = st.file_uploader("Upload a file", type=["pdf"], accept_multiple_files=True)


for doc in docs:
    try:
        invoice = MercadonaScrapper.get_invoice(doc)
        macro_data_frame = pd.concat(
            [macro_data_frame, invoice.dataframe], ignore_index=True
        )
    except Exception as e:
        st.warning(f"Error processing file {doc.name}: {e}")

if len(macro_data_frame) > 0:
    macro_data_frame["category"] = macro_data_frame["name"].apply(get_category)

    st.subheader("Tabla total")

    st.dataframe(macro_data_frame)

    (col1, col2) = st.columns(2)

    with col1:
        st.subheader("Productos más comprados")

        df_most_bought = (
            macro_data_frame.groupby("name")["quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        df_most_bought = pd.DataFrame(df_most_bought).rename(
            columns={"name": "Producto", "quantity": "Cantidad"}
        )

        st.dataframe(df_most_bought)

    with col2:
        st.subheader("Productos con más gasto")
        df_most_expensive = (
            macro_data_frame.groupby("name")["total_price"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        df_most_expensive = pd.DataFrame(df_most_expensive).rename(
            columns={"name": "Producto", "total_price": "Gasto"}
        )

        st.dataframe(df_most_expensive)

    (col1, col2) = st.columns(2)
    with col1:
        st.subheader("Categorías más comprados")

        df_most_bought = (
            macro_data_frame.groupby("category")["quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        df_most_bought = pd.DataFrame(df_most_bought).rename(
            columns={"name": "Producto", 0: "Cantidad"}
        )

        st.dataframe(df_most_bought)

    with col2:
        st.subheader("Categorías con más gasto")
        df_most_expensive = (
            macro_data_frame.groupby("category")["total_price"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        df_most_expensive = pd.DataFrame(df_most_expensive).rename(
            columns={"name": "Categoría", "total_price": "Euros"}
        )

        st.dataframe(df_most_expensive)

    st.plotly_chart(
        px.pie(
            macro_data_frame,
            names="category",
            values="total_price",
            title="Gastos por categoría",
        )
    )

    st.plotly_chart(
        px.bar(
            macro_data_frame.groupby("payment_date")["total_price"].sum().reset_index(),
            x="payment_date",
            y="total_price",
            title="Histórico de gasto",
        )
    )

    # Histórico gasto por categoría

    st.plotly_chart(
        px.bar(
            macro_data_frame.groupby(["payment_date", "category"])["total_price"]
            .sum()
            .reset_index(),
            x="payment_date",
            y="total_price",
            color="category",
            title="Histórico de gasto por categoría",
        )
    )

    unique_products = macro_data_frame["name"].unique()

    st.subheader("Histórico de precios de productos")

    selected_product = st.selectbox("Select a product", unique_products)

    # Histórico de precios

    st.plotly_chart(
        px.bar(
            macro_data_frame[macro_data_frame["name"] == selected_product],
            x="payment_date",
            y="unit_price",
            title=f"Histórico de precios de {selected_product}",
        )
    )

    (col1, col2) = st.columns(2)

    with col1:
        # tabla de gastos totales por producto

        st.subheader("Gastos totales por producto")

        df_total_expense = (
            macro_data_frame.groupby("name")["total_price"]
            .sum()
            .sort_values(ascending=False)
        )

        df_total_expense = pd.DataFrame(df_total_expense).rename(
            columns={"name": "Producto", "total_price": "Gasto"}
        )

        st.dataframe(df_total_expense)
