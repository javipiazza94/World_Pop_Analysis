import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_population_data
from simulation import PopulationSimulator

# Configuración de la página
st.set_page_config(page_title="Simulación de Población Mundial (2025-2125)", layout="wide")

# Título y Descripción
st.title("🌍 Simulación de Población Mundial (2025-2125)")
st.markdown("""
Esta aplicación simula el crecimiento de la población utilizando un **Método de Componentes** ($P_{t+1} = P_t + Nacimientos - Muertes$).
*   **Tasa de Natalidad**: Se asume constante.
*   **Tasa de Mortalidad**: Aumenta con el tiempo para simular el **envejecimiento de la población**, especialmente en países con una edad media alta.
""")

# Cargar Datos
@st.cache_data
def get_data():
    return load_population_data()

try:
    df = get_data()
except FileNotFoundError:
    st.error("Archivo de datos no encontrado. Por favor asegúrese de que 'population_2025.csv' existe.")
    st.stop()

# Controles de la Barra Lateral
st.sidebar.header("Configuración de la Simulación")

# Selección de Países
all_countries = df['Country'].unique().tolist()
default_countries = ["India", "China", "USA", "Nigeria", "Japan"]
selected_countries = st.sidebar.multiselect(
    "Seleccionar Países para Visualizar", 
    all_countries, 
    default=[c for c in default_countries if c in all_countries]
)

# Rango de Simulación
years_range = st.sidebar.slider("Rango de Simulación (Años)", 2025, 2125, (2025, 2125))
start_year, end_year = years_range

# Ejecutar Simulación
if selected_countries:
    # Filtrar datos para países seleccionados
    filtered_df = df[df['Country'].isin(selected_countries)]
    
    # Inicializar Simulador
    sim = PopulationSimulator(filtered_df)
    
    # Ejecutar Simulación
    sim_results = sim.simulate(start_year=start_year, end_year=end_year)
    
    # --- Visualización ---
    
    # 1. Gráfico de Línea de Población
    st.subheader("📈 Proyecciones de Población")
    fig_pop = px.line(
        sim_results, 
        x="Year", 
        y="Population", 
        color="Country", 
        title="Crecimiento de Población Proyectado",
        labels={"Population": "Población", "Year": "Año", "Country": "País"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_pop, use_container_width=True)
    
    # 2. Análisis de Nacimientos vs Muertes
    st.subheader("⚰️ Análisis de Nacimientos vs. Muertes")
    st.markdown("Observe cómo las **Muertes** (rojo) podrían superar a los **Nacimientos** (verde) a medida que la población envejece.")
    
    # Crear una pestaña para cada país seleccionado
    tabs = st.tabs(selected_countries)
    
    for i, country in enumerate(selected_countries):
        with tabs[i]:
            country_data = sim_results[sim_results['Country'] == country]
            
            fig_bd = go.Figure()
            fig_bd.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Births'],
                                mode='lines', name='Nacimientos', line=dict(color='green')))
            fig_bd.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Deaths'],
                                mode='lines', name='Muertes', line=dict(color='red')))
            
            fig_bd.update_layout(
                title=f"{country}: Nacimientos vs Muertes",
                xaxis_title="Año",
                yaxis_title="Cantidad",
                template="plotly_dark",
                hovermode="x unified"
            )
            st.plotly_chart(fig_bd, use_container_width=True)
            
            # Mostrar estadísticas actuales
            curr_stats = filtered_df[filtered_df['Country'] == country].iloc[0]
            st.caption(f"**Estadísticas Iniciales (2025)**: Edad Media: {curr_stats['Median_Age']} | Tasa Natalidad: {curr_stats['Birth_Rate']}‰ | Tasa Mortalidad: {curr_stats['Death_Rate']}‰")

    # 3. Tabla de Datos
    st.subheader("📊 Datos de la Simulación")
    with st.expander("Ver Datos Crudos"):
        st.dataframe(sim_results)
        
    # 4. Insights del Modelo Predictivo
    st.subheader("🤖 Insights del Modelo Predictivo (Scikit-learn)")
    
    cols = st.columns(len(selected_countries))
    
    for i, country in enumerate(selected_countries):
        trend = sim.predict_trend(country, sim_results)
        if trend:
            with cols[i % 3]: 
                st.info(f"**{country}**")
                st.write(f"Puntuación R²: `{trend['r2_score']:.4f}`")
                
                # Interpretación
                if trend['coefficient'] > 0:
                    st.success("Tendencia Ascendente 🚀")
                else:
                    st.warning("Tendencia Descendente 📉")

else:
    st.info("Por favor seleccione al menos un país en la barra lateral para comenzar la simulación.")

# Pie de página
st.markdown("---")
st.markdown("Fuente de Datos: Proyecciones 2025 (Simulado basado en tendencias ONU/Worldometers). 'Efecto de Envejecimiento' modelado algorítmicamente.")
