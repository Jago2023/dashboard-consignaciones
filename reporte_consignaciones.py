# reporte_consignaciones.py

import pandas as pd
from datetime import datetime

# Ruta del archivo (ajústala según tu caso)
archivo_excel = "tabular.xlsx"

# Leer archivo Excel
df = pd.read_excel(archivo_excel, sheet_name="Tabular")

# Normalizar columnas clave
df["Estado actual"] = df["Estado actual"].astype(str).str.strip()
df["Tipo de elemento"] = df["Tipo de elemento"].astype(str).str.strip()

# Filtrar estados y tipos requeridos
estados_validos = ["En Ejecución", "Aprobada", "Ejecutadas"]
tipos_validos = ["UnidadHidraulica", "UnidadSolar", "UnidadTermica"]

df_filtrado = df[
    df["Estado actual"].isin(estados_validos) &
    df["Tipo de elemento"].isin(tipos_validos)
].copy()

# Calcular si está vencida
hoy = pd.Timestamp.today()
df_filtrado["Vencida"] = pd.to_datetime(df_filtrado["Fecha final real"], errors='coerce') < hoy

# Guardar reporte Excel
with pd.ExcelWriter("informe_consignaciones.xlsx", engine="openpyxl") as writer:
    df_filtrado.to_excel(writer, sheet_name="Consignaciones", index=False)

    resumen = df_filtrado.groupby(["Estado actual", "Tipo de elemento", "Vencida"]).size().unstack(fill_value=0)
    resumen.to_excel(writer, sheet_name="Resumen")

print("✅ Informe generado correctamente: informe_consignaciones.xlsx")