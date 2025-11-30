# Simulación de Población Mundial (2025-2125)

Este proyecto es una herramienta interactiva en Python para simular y visualizar la evolución de la población mundial durante el próximo siglo. Utiliza datos demográficos reales de 2025 y un modelo de simulación basado en componentes que tiene en cuenta el envejecimiento de la población.

## 📋 Características

*   **Simulación Demográfica**: Proyección año a año basada en tasas de natalidad y mortalidad.
*   **Lógica de Envejecimiento**: La tasa de mortalidad aumenta dinámicamente en función de la edad media del país, simulando el envejecimiento poblacional.
*   **Visualización Interactiva**: Gráficos dinámicos con **Plotly** y **Streamlit**.
*   **Análisis Comparativo**: Visualización de "Nacimientos vs Muertes" para identificar cuándo la mortalidad supera a la natalidad.
*   **Modelo Predictivo**: Regresión lineal con **Scikit-learn** para calcular tendencias de crecimiento.

## 📂 Estructura del Proyecto

*   `app.py`: Aplicación principal (Frontend en Streamlit).
*   `simulation.py`: Motor lógico de la simulación (Clase `PopulationSimulator`).
*   `data_loader.py`: Script para cargar y limpiar los datos.
*   `data/population_2025.csv`: Dataset con datos de población, tasas de natalidad/mortalidad y edad media.
*   `utils/requirements.txt`: Lista de dependencias necesarias.

## 🚀 Instalación y Ejecución

### 1. Prerrequisitos
Asegúrate de tener Python instalado. Se recomienda usar un entorno virtual.

### 2. Instalar Dependencias
Ejecuta el siguiente comando en tu terminal para instalar las librerías necesarias:

```bash
pip install -r utils/requirements.txt
```

### 3. Ejecutar la Aplicación
Para iniciar la interfaz interactiva, ejecuta:

```bash
streamlit run app.py
```

Una vez ejecutado, se abrirá automáticamente una pestaña en tu navegador con la simulación.

## 📊 Datos
Los datos base (`population_2025.csv`) incluyen proyecciones para 2025 obtenidas de fuentes demográficas (ONU, Worldometers), incluyendo:
*   Población Total
*   Tasa de Natalidad (por 1000 hab.)
*   Tasa de Mortalidad (por 1000 hab.)
*   Edad Media (Median Age)
