import streamlit as st
import pandas as pd
from Code.procesamiento_datos import procesar_datos
from Code.verificacion_input import validar_diametro, cargar_archivo 


DEFAULT_DATASET_PATH = r"climate_data\baad_data.csv"


if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "inicio"

if "df_final" not in st.session_state:
    st.session_state["df_final"] = None
    

if "usar_default" not in st.session_state:
    st.session_state["usar_default"] = False

st.set_page_config(page_title="Estimación de Carbono", layout="wide")



def procesar_datosg(df_cargado, otro):
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
    
    # --- Control de Columna Personalizada ---
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

  
    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Carga tu archivo con los datos",
            type=["csv", "xlsx", "json"]
        )

    with col2:
        # Nuevo Botón para cargar el dataset por defecto
        st.write("---") # Espaciador
        if st.button(f"Usar Dataset por Defecto: {DEFAULT_DATASET_PATH}"):
            # Al hacer clic, forzamos el estado a usar el default y volvemos a ejecutar
            st.session_state["usar_default"] = True
            st.rerun() 
            
   

    df_cargado = None
    
    if uploaded_file is not None:
        st.session_state["usar_default"] = False # Desactivar la carga default si se sube un archivo
        
        df_cargado, error_carga = cargar_archivo(uploaded_file)
        
        if error_carga:
            st.error(error_carga)
            st.stop()
        
        # Procesar los datos cargados
        procesar_datosg(df_cargado, otro)


    elif st.session_state["usar_default"]:
        st.info(f"Procesando dataset por defecto: **{DEFAULT_DATASET_PATH}**. Esto puede tardar varios minutos...")
        
        try:
            df_final_procesado = procesar_datos()
            
            st.success("¡Procesamiento del dataset por defecto finalizado!")
            st.subheader("Vista previa del resultado:")
            st.dataframe(df_final_procesado.head())
            

            st.session_state["df_final"] = df_final_procesado
            
            if st.button("Ver Resultados Completos"):
                st.session_state["pantalla"] = "resultados"
                st.rerun()
            
        except FileNotFoundError:
            st.error(f"Error: No se encontró el archivo por defecto en la ruta: {DEFAULT_DATASET_PATH}")
            st.session_state["usar_default"] = False # Resetear
            
        except Exception as e:
            st.error(f"Error cargando el dataset por defecto: {e}")
            st.session_state["usar_default"] = False # Resetear
            
    # 3. Estado inicial: Ningún archivo o default cargado
    else:
        st.info("Esperando que cargues un archivo o uses el dataset por defecto.")
        # Asegurarse de que no haya resultados pendientes de una ejecución anterior fallida
        st.session_state["df_final"] = None



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
            st.session_state["usar_default"] = False # Resetear estado
            st.rerun()


