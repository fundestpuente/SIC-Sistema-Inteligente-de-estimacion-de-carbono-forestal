import streamlit as st
from Code.verificacion_input import validar_diametro


st.set_page_config(page_title="Estimación de Carbono", layout="wide")

st.title("Sistema de estimación de carbono forestal")

st.write("Sube un archivo con datos de diámetros de árboles (CSV o Excel).")

# Pregunta de verdadero o falso
otro_nombre_bool = st.checkbox("¿Usaste un nombre diferente para la columna de diámetro?")

otro = None

if otro_nombre_bool:
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
    type=["csv", "xlsx"]
)

if uploaded_file:
    df, error = validar_diametro(uploaded_file, otro)

    if error:
        st.error(error)
    else:
        st.success("Archivo validado correctamente.")
        st.subheader("Vista previa:")
        st.dataframe(df.head())


