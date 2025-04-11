import streamlit as st
import pandas as pd

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        background-color: #F5F5F5;
    }
    .stSelectbox div[data-baseweb="select"] {
        margin-bottom: 15px;
        background-color: white;
    }
    .stButton button {
        width: 100%;
        background-color: #0068c9;
        color: white;
        font-weight: bold;
        border-radius: 4px;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .stSuccess {
        background-color: #e6f7ee;
        border-left: 5px solid #00a651;
        padding: 1rem;
        font-size: 18px;
    }
    .stWarning {
        background-color: #fff3e6;
        border-left: 5px solid #ff9900;
        padding: 1rem;
        font-size: 18px;
    }
    .header {
        color: #0068c9;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Incentivos de renovacion.xlsx", sheet_name="Hoja1")
        df.iloc[:, 0:3] = df.iloc[:, 0:3].fillna(method='ffill')
        df.columns = [
            "Categoria", "Combustible_actual", "Combustible_reemplazo",
            "<2000", "2000-2002", "2003-2006", "2007-2017"
        ]
        df = df[df["Categoria"] != "Categoria"]
        df_melted = df.melt(
            id_vars=["Categoria", "Combustible_actual", "Combustible_reemplazo"],
            var_name="Año_fabricacion",
            value_name="Valor_incentivo"
        ).dropna()
        df_melted["Año_fabricacion"] = df_melted["Año_fabricacion"].replace("<2000", "Antes del 2000")
        return df_melted
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load data
data = load_data()

# App header
st.markdown('<h1 class="header">Calculadora de Incentivos para Chatarreo</h1>', unsafe_allow_html=True)
st.markdown("Selecciona los datos del vehículo para conocer el incentivo de chatarreo disponible.")

# Create columns for better organization
col1, col2 = st.columns(2)
with col1:
    categoria = st.selectbox(
        "Categoría del Vehículo", 
        sorted(data["Categoria"].unique()),
        help="Selecciona la categoría de tu vehículo actual"
    )
    
    comb_actual = st.selectbox(
        "Combustible de vehículo actual", 
        sorted(data["Combustible_actual"].unique()),
        help="Tipo de combustible que usa tu vehículo actual"
    )

with col2:
    # Sort years with custom order
    available_years = data["Año_fabricacion"].unique().tolist()
    year_order = ["Antes del 2000", "2000-2002", "2003-2006", "2007-2017"]
    sorted_years = [y for y in year_order if y in available_years]
    
    anio_fabricacion = st.selectbox(
        "Año de Fabricación",
        sorted_years,
        help="Año de fabricación de tu vehículo actual"
    )
    
    comb_reemplazo = st.selectbox(
        "Combustible de vehículo nuevo", 
        sorted(data["Combustible_reemplazo"].unique()),
        help="Tipo de combustible del vehículo nuevo que deseas adquirir"
    )

# Calculate button
st.markdown("---")
if st.button("Calcular"):
    with st.spinner("Calculando incentivo..."):
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
            st.success(f"Incentivo disponible: **${valor:,.2f}**")
            
            # Show additional information
            with st.expander("Ver detalles del cálculo"):
                st.markdown(f"""
                - **Vehículo actual:** {categoria} ({comb_actual})
                - **Vehículo nuevo:** {comb_reemplazo}
                - **Año de fabricación:** {anio_fabricacion}
                """)
        else:
            st.warning("""
            No se encontró un incentivo para esta combinación
            
            Por favor verifica que:
            1. La combinación de combustible actual y de reemplazo sea válida
            2. El año de fabricación corresponda a tu vehículo
            """)

# Add footer
st.markdown("---")
st.caption("© 2023 Programa de Renovación Vehicular - Todos los derechos reservados")
