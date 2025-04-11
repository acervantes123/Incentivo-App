import streamlit as st
import pandas as pd

# Custom CSS for better styling
st.markdown("""
<style>
    .stSelectbox div[data-baseweb="select"] {
        margin-bottom: 15px;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stSuccess {
        font-size: 18px !important;
        text-align: center;
    }
    .stWarning {
        font-size: 18px !important;
        text-align: center;
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

# App layout
st.title("🚗 Calculadora de Incentivos para Renovación Vehicular")
st.markdown("""
**Selecciona las características de tu vehículo actual para conocer el incentivo disponible 
para renovarlo por uno más ecológico.**
""")

# Create columns for better organization
col1, col2 = st.columns(2)
with col1:
    categoria = st.selectbox(
        "Categoría del Vehículo", 
        sorted(data["Categoria"].unique()),
        help="Selecciona la categoría de tu vehículo actual"
    )
    
    comb_actual = st.selectbox(
        "Combustible Actual", 
        sorted(data["Combustible_actual"].unique()),
        help="Tipo de combustible que usa tu vehículo actual"
    )

with col2:
    comb_reemplazo = st.selectbox(
        "Combustible de Reemplazo", 
        sorted(data["Combustible_reemplazo"].unique()),
        help="Tipo de combustible del vehículo nuevo que deseas adquirir"
    )
    
    # Sort years with custom order
    available_years = data["Año_fabricacion"].unique().tolist()
    year_order = ["Antes del 2000", "2000-2002", "2003-2006", "2007-2017"]
    sorted_years = [y for y in year_order if y in available_years]
    
    anio_fabricacion = st.selectbox(
        "Año de Fabricación",
        sorted_years,
        help="Año de fabricación de tu vehículo actual"
    )

# Calculate button with improved layout
st.markdown("---")
if st.button("📊 Calcular Incentivo", type="primary"):
    with st.spinner("Buscando el mejor incentivo para ti..."):
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
            st.balloons()
            st.success(f"### 💰 Incentivo disponible: **${valor:,.2f}**")
            
            # Show additional information
            with st.expander("📝 Información Adicional"):
                st.markdown(f"""
                - **Vehículo actual:** {categoria} ({comb_actual})
                - **Vehículo nuevo:** {comb_reemplazo}
                - **Año de fabricación:** {anio_fabricacion}
                """)
        else:
            st.warning("""
            ### ⚠️ No se encontró un incentivo para esta combinación
            
            Por favor verifica que:
            1. La combinación de combustible actual y de reemplazo sea válida
            2. El año de fabricación corresponda a tu vehículo
            """)

# Add footer
st.markdown("---")
st.caption("© 2023 Programa de Renovación Vehicular - Todos los derechos reservados")
