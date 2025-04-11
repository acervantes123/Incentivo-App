import streamlit as st
import pandas as pd

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        background-color: #F5F5F5;
    }
    .title {
        text-align: center;
        color: #0068c9;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .stSelectbox div[data-baseweb="select"] {
        margin-bottom: 15px;
        background-color: white;
    }
    .stButton button {
        width: 50%;
        background-color: #0068c9;
        color: white;
        font-weight: bold;
        border-radius: 8px;  /* Made less round (from 20px to 8px) */
        padding: 0.5rem;
        margin: 0 auto;
        display: block;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .incentive-container {
        background-color: #e6f7ee;
        border-left: 5px solid #00a651;
        padding: 1rem;
        text-align: center;
        border-radius: 4px;
        margin-top: 1rem;
    }
    .incentive-value {
        font-size: 28px;
        font-weight: bold;
        color: #00a651;
        margin: 0;
    }
    .stWarning {
        background-color: #fff3e6;
        border-left: 5px solid #ff9900;
        padding: 1rem;
        font-size: 18px;
    }
    .description {
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

# App header - Centered title with left-aligned description
st.markdown('<h1 class="title">Calculadora de Incentivos para Chatarreo</h1>', unsafe_allow_html=True)
st.markdown('<div class="description">Selecciona los datos del vehículo para conocer el incentivo de chatarreo disponible.</div>', unsafe_allow_html=True)

# Create columns for better organization
col1, col2 = st.columns(2)
with col1:
    categoria = st.selectbox(
        "Categoría del Vehículo", 
        sorted(data["Categoria"].unique())
    )
    
    comb_actual = st.selectbox(
        "Combustible de vehículo actual", 
        sorted(data["Combustible_actual"].unique())
    )

with col2:
    # Sort years with custom order
    available_years = data["Año_fabricacion"].unique().tolist()
    year_order = ["Antes del 2000", "2000-2002", "2003-2006", "2007-2017"]
    sorted_years = [y for y in year_order if y in available_years]
    
    anio_fabricacion = st.selectbox(
        "Año de Fabricación",
        sorted_years
    )
    
    comb_reemplazo = st.selectbox(
        "Combustible de vehículo nuevo", 
        sorted(data["Combustible_reemplazo"].unique())
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
            st.markdown(
                f"""
                <div class="incentive-container">
                    <p>Incentivo disponible:</p>
                    <p class="incentive-value">${valor:,.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
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
