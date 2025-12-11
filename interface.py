import streamlit as st
import pandas as pd
from Code.verificacion_input import validar_diametro, cargar_archivo


DEFAULT_DATASET_PATH = r"climate_data\baad_data.csv"


if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "inicio"

if "df_final" not in st.session_state:
    st.session_state["df_final"] = None

st.set_page_config(page_title="Estimación de Carbono", layout="wide")

if st.session_state["pantalla"] == "inicio":

    st.title("Sistema de estimación de carbono forestal")
    st.write("Sube un archivo con datos de diámetros de árboles (CSV, Excel o JSON).")
    st.write("Si no subes un archivo, se utilizará el dataset por defecto: **baad_data.csv**")

    # Pregunta al usuario
    otro_nombre = st.checkbox("¿Usaste un nombre diferente para la columna de diámetro?")
    otro = None

    if otro_nombre:
        otro = st.text_input("Escribe el nombre EXACTO de la columna personalizada:")

        if otro:
            if otro.isnumeric():
                st.error("El nombre de la columna no puede ser un número.")
                otro = None
            elif not isinstance(otro, str):
                st.error("El nombre debe ser texto válido.")
                otro = None

    # Subir archivo
    uploaded_file = st.file_uploader(
        "Carga el archivo con los datos",
        type=["csv", "xlsx", "json"]
    )

    
    if uploaded_file is None:
        st.info("No se subió ningún archivo. Usando dataset por defecto.")
        try:
            df_cargado = pd.read_csv(DEFAULT_DATASET_PATH)
            df_validado, error = validar_diametro(df_cargado, otro)
        except Exception as e:
            st.error(f"Error cargando el dataset por defecto: {e}")
            st.stop()
    else:
        
        df_cargado, error_carga = cargar_archivo(uploaded_file)

        if error_carga:
            st.error(error_carga)
            st.stop()

        df_validado, error = validar_diametro(df_cargado, otro)

    
    if error:
        st.error(error)
    else:
        st.success("Archivo validado correctamente.")
        st.subheader("Vista previa:")
        st.dataframe(df_validado.head())

        st.session_state["df_final"] = df_validado

        if st.button("Resultados"):
            st.session_state["pantalla"] = "resultados"
            st.rerun()


elif st.session_state["pantalla"] == "resultados":

    st.title("Resultados del análisis de carbono")

    df_final = st.session_state["df_final"]

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

        if st.button("Volver al inicio"):
            st.session_state["pantalla"] = "inicio"
            st.rerun()


