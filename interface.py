import streamlit as st
from Code.verificacion_input import validar_diametro, cargar_archivo

if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "inicio"   # inicio -> resultados

if "df_final" not in st.session_state:
    st.session_state["df_final"] = None

st.set_page_config(page_title="Estimación de Carbono", layout="wide")

if st.session_state["pantalla"] == "inicio":

    st.title("Sistema de estimación de carbono forestal")

    st.write("Sube un archivo con datos de diámetros de árboles (CSV o Excel).")

# Pregunta de verdadero o falso
    otro_nombre = st.checkbox("¿Usaste un nombre diferente para la columna de diámetro?")

    otro = None

    if otro_nombre:
        otro = st.text_input("Escribe el nombre EXACTO de la columna personalizada:")

    # Validaciones
        if otro:
            if otro.isnumeric():
                st.error("El nombre de la columna no puede ser un número.")
                otro = None
            elif not isinstance(otro, str):
                st.error("El nombre debe ser texto válido.")
                otro = None

    # Subir archivo después de responder la pregunta
    uploaded_file = st.file_uploader(
        "Carga el archivo con los datos", 
        type=["csv", "xlsx", "json"]
    )


    if uploaded_file:
        df_cargado, error_carga = cargar_archivo(uploaded_file)

        if error_carga:
            st.error(error_carga)
        else:
            df_validado, error = validar_diametro(df_cargado, otro)

            if error:
                st.error(error)
            else:
                st.success("Archivo validado correctamente.")
                st.subheader("Vista previa:")
                st.dataframe(df_validado.head())

                # Por ahora solo guardamos df_validado
                st.session_state["df_final"] = df_validado
                # funcion para uso de modelo (df_cargado)
                # Mostrar botón de ir a resultados
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
        # ya lo que se ha procesado se muestra
        #Ejemplo:
        # archivo_modificado = generar_dataset_modificado(df_final)
        # archivo_reporte = generar_reporte(df_final)
        #
        # Incluirás gráficos, estadísticas, etc

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

