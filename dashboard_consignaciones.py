# dashboard_consignaciones.py

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Consignaciones Eléctricas")

# Cargar archivo desde la interfaz o usar por defecto
uploaded_file = st.file_uploader("📂 Suba el archivo Excel generado (informe_consignaciones.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Consignaciones")
else:
    try:
        df = pd.read_excel("informe_consignaciones.xlsx", sheet_name="Consignaciones")
        st.info("Se cargó el archivo local por defecto.")
    except FileNotFoundError:
        st.warning("⚠️ No se encontró el archivo. Cargue uno manualmente para continuar.")
        st.stop()

# Filtros dinámicos
estado = st.multiselect("Filtrar por Estado", df["Estado actual"].unique(), default=df["Estado actual"].unique())
tipo = st.multiselect("Filtrar por Tipo de Unidad", df["Tipo de elemento"].unique(), default=df["Tipo de elemento"].unique())

df_filtered = df[
    df["Estado actual"].isin(estado) & 
    df["Tipo de elemento"].isin(tipo)
]

# Tabla
st.subheader("📋 Consignaciones filtradas")
st.dataframe(df_filtered, use_container_width=True)

# Gráfico de barras
st.subheader("📊 Distribución por tipo de unidad")
fig1 = px.histogram(df_filtered, x="Tipo de elemento", color="Estado actual", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de vencidas
st.subheader("⚠️ Proporción de consignaciones vencidas")
fig2 = px.pie(df_filtered, names="Vencida", title="Vencidas vs Activas")
st.plotly_chart(fig2, use_container_width=True)