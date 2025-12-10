import pandas as pd
import json

def validar_diametro(uploaded_file, otro=None):
    #verifica la existencia de la columna diametro

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

def cargar_archivo(uploaded):
    file_type = uploaded.name.split(".")[-1].lower()
    #verifica el tipo de archivo
    try:
        if file_type == "csv":
            return pd.read_csv(uploaded), None

        elif file_type == "xlsx":
            return pd.read_excel(uploaded), None

        elif file_type == "json":

            # Intentar leer JSON como lista de objetos
            try:
                data = json.load(uploaded)
                if isinstance(data, dict):
                    # Si es un dict con una lista dentro
                    key = list(data.keys())[0]
                    data = data[key]
                df = pd.DataFrame(data)
                return df, None

            except Exception as e:
                return None, f"Error al leer el archivo JSON: {e}"

        else:
            return None, "Formato de archivo no soportado."

    except Exception as e:
        return None, f"Error procesando archivo: {e}"