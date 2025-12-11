import os

import streamlit as st
import pandas as pd

from Code.verificacion_input import validar_diametro
from Code.procesamiento_datos import procesar_datos
from Code.model import modelo

DEFAULT_DATASET_PATH = r"climate_data\baad_data.csv"


if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "inicio"

if "df_final" not in st.session_state:
    st.session_state["df_final"] = None

if "usar_default" not in st.session_state:
    st.session_state["usar_default"] = False

if "archivo" not in st.session_state:
    st.session_state["archivo"] = ""

st.set_page_config(page_title="Estimación de Carbono", layout="wide")


def cargar_datos(df_cargado, otro):
    """Encapsula la validación y el manejo de errores."""
    df_validado, error = validar_diametro(df_cargado, otro)

    if error:
        st.error(error)
        # Opcional: limpiar el estado para evitar resultados erróneos
        st.session_state["df_final"] = None 
    else:
        st.success("Archivo validado correctamente.")
        st.subheader("Vista previa:")
        st.dataframe(df_validado.head())

        st.session_state["df_final"] = df_validado

        if st.button("Resultados"):
            st.session_state["pantalla"] = "resultados"
            st.rerun()

if st.session_state["pantalla"] == "inicio":

    st.title("Sistema de estimación de carbono forestal")
    st.write("Sube un archivo con datos de diámetros de árboles (CSV, Excel o JSON).")
    st.code("datos que debe tener el dataset")

    existing_files = [f for f in os.listdir("climate_data") if f.endswith((".csv", ".xlsx"))]
    if existing_files:
        st.subheader("📁 Archivos actuales en el sistema:")
        selected_file = st.selectbox("Selecciona un archivo existente:", existing_files)
        st.session_state["archivo"] =  os.path.join("climate_data", selected_file)

        if st.button("🗑️ Eliminar archivo seleccionado"):
            os.remove(os.path.join("climate_data", selected_file))
            st.success(f"Archivo '{selected_file}' eliminado correctamente.")
            st.session_state["archivo"] = ""
            st.experimental_rerun()

    st.divider()

    uploaded_file = st.file_uploader("Selecciona un nuevo archivo", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine="openpyxl")
                print(df)

            st.success(f"✅ Archivo '{uploaded_file.name}' cargado correctamente")
            st.subheader("Vista previa:")
            st.dataframe(df.head())

            save_path = os.path.join("climate_data", uploaded_file.name)
            df.to_csv(save_path.replace(".xlsx", ".csv"), index=False)
            st.success(f"Archivo guardado en: `{save_path.replace('.xlsx', '.csv')}`")

        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {e}")

    if st.button("Ver Resultados Completos"):
        st.session_state["pantalla"] = "resultados"
        st.rerun()

elif st.session_state["pantalla"] == "resultados":

    st.title("Resultados del análisis de carbono")

    df_final = procesar_datos(st.session_state["archivo"])
    st.session_state["df_final"] = df_final

    if df_final is None:
        st.error("No hay datos procesados. Regresa a la pantalla de carga.")
        if st.button("Volver"):
            st.session_state["pantalla"] = "inicio"
            st.rerun()
    else:
        st.success("Aquí puedes descargar los resultados del procesamiento.")
        st.subheader("Vista previa del dataset final:")
        st.dataframe(df_final.head())

        csv_data = df_final.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar dataset procesado (CSV)",
            data=csv_data,
            file_name="carbono_procesado.csv",
            mime="text/csv"
        )

        if st.button("Crear modelo de predicción"):
            st.session_state["pantalla"] = "prediccion"
            st.rerun()

        if st.button("Volver al inicio"):
            st.session_state["pantalla"] = "inicio"
            st.session_state["usar_default"] = False # Resetear estado
            st.rerun()


elif st.session_state["pantalla"] == "prediccion":
    st.title("Modelo de predicción de captura de carbono")
    r2_rf, mae_rf, importances, rf = modelo(st.session_state["df_final"])

    col1, col2, col3 = st.columns(3)

    with col1:
        # min_value=0.0 asegura que sean positivos
        dap = st.number_input("DAP (cm)", min_value=0.0, format="%.2f", value=10.0)

    with col2:
        altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f", value=5.0)

    with col3:
        m_st = st.number_input("m_st", min_value=0.0, format="%.4f", value=0.5)

    if st.button("Calcular Predicción", type="primary"):
        if dap > 0 and altura > 0 and m_st > 0:
            resultado = rf.predict([[dap, altura, m_st]]) * 0.5
            st.success(f"La captura de carbono predicha es: **{float(resultado[0]):.4f}**")
        else:
            st.warning("Por favor, ingrese valores mayores a 0 para todas las variables.")

    st.header("Evaluación del Modelo Random Forest")

    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="R² Score (Ajuste)", value=f"{r2_rf:.3f}")
    with m_col2:
        st.metric(label="MAE (Error Medio Absoluto)", value=f"{mae_rf:.3f}", delta_color="inverse")

    st.subheader("Importancia de las Variables")
    st.bar_chart(importances.set_index("Variable"))

    # Opción alternativa: Mostrar la tabla de datos
    with st.expander("Ver datos exactos de importancia"):
        st.dataframe(importances)