import pandas as pd

def validar_diametro(uploaded_file, otro=None):
    """
    Verifica que el archivo subido tenga una columna válida de diámetros.
    Se aceptan .csv o .xlsx con una columna llamada 'diametro' o 'dbh'.
    """

    if uploaded_file is None:
        return None, "No se cargó ningún archivo."

    # Determinar tipo
    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Formato no soportado. Sube un archivo .csv o .xlsx"
    except Exception as e:
        return None, f"Error leyendo el archivo: {e}"
    
    

    # Normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.strip()

    # Verificar que exista una columna de diámetro
    valid_cols = ["diametro", "d.bh", "dap"]
    if (otro is not None):
        valid_cols.append(otro.lower().strip())
    
    found = [c for c in valid_cols if c in df.columns]

    if not found:
        return None, (
            "El archivo debe contener una columna llamada: "
            "'diametro', 'd.bh' o 'dap' o el nombre personalizado que ingresaste."
        )

    # Renombrar a una columna estándar
    df = df.rename(columns={found[0]: "d.bh"})

    return df, None