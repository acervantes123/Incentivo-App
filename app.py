import streamlit as st
import pandas as pd

# Load the data (replace with your actual file path if running locally)
@st.cache_data
def load_data():
    df = pd.read_excel("Incentivos de renovacion.xlsx", sheet_name="Hoja1")
    df.iloc[:, 0:3] = df.iloc[:, 0:3].fillna(method='ffill')
    df.columns = [
        "Categoria", "Combustible_actual", "Combustible_reemplazo",
        "Año_fabricacion", "<2000", "2000-2002", "2003-2006", "2007-2017"
    ]
    df = df[df["Categoria"] != "Categoria"]
    df_melted = df.melt(
        id_vars=["Categoria", "Combustible_actual", "Combustible_reemplazo"],
        var_name="Año_fabricacion",
        value_name="Valor_incentivo"
    ).dropna()
    df_melted["Año_fabricacion"] = df_melted["Año_fabricacion"].replace("<2000", "Antes del 2000")
    return df_melted

# Load and cache data
data = load_data()

st.title("Incentivos por Renovación de Vehículos")
st.write("Selecciona los datos del vehículo para conocer el incentivo disponible.")

# UI filters
categoria = st.selectbox("Categoría", sorted(data["Categoria"].unique()))
comb_actual = st.selectbox("Combustible actual", sorted(data["Combustible_actual"].unique()))
comb_reemplazo = st.selectbox("Combustible de reemplazo", sorted(data["Combustible_reemplazo"].unique()))
anio_fabricacion = st.selectbox("Año de fabricación", sorted(data["Año_fabricacion"].unique()))

# Button to calculate
if st.button("Calcular incentivo"):
    # Filter data
    df_filtered = data[
        (data["Categoria"] == categoria) &
        (data["Combustible_actual"] == comb_actual) &
        (data["Combustible_reemplazo"] == comb_reemplazo) &
        (data["Año_fabricacion"] == anio_fabricacion)
    ]

    # Show result
    if not df_filtered.empty:
        valor = df_filtered.iloc[0]["Valor_incentivo"]
        st.success(f"Incentivo disponible: **{valor:.2f}**")
    else:
        st.warning("No se encontró un incentivo para esta combinación.")


