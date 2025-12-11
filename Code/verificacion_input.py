import pandas as pd
import json

def validar_diametro(df, otro=None):
    

    # 1. Normalizar nombres de columnas del DataFrame (no del archivo subido)
    df.columns = df.columns.str.lower().str.strip()

    # 2. Definir nombres válidos
    valid_cols = ["diametro", "d.bh", "dap"]
    
    # 3. Incluir el nombre personalizado si fue proporcionado
    if otro:
        # Normalizar el nombre personalizado para la búsqueda
        valid_cols.append(otro.lower().strip())

    # 4. Buscar la columna
    found = [c for c in valid_cols if c in df.columns]

    if not found:
        return None, (
            "El archivo debe contener una columna llamada: "
            "'diametro', 'd.bh', 'dap' o el nombre personalizado ingresado."
        )

    col_name = found[0]
    columna_diametro = df[col_name]

    # 5. Validación de tipo de datos (Añadido para robustez)
    if not pd.api.types.is_numeric_dtype(columna_diametro):
        # Intentar forzar la conversión si hay cadenas que parecen números (ej: "10.5")
        try:
            df[col_name] = pd.to_numeric(columna_diametro, errors='coerce')
            # Eliminar filas donde la conversión falló y se convirtió en NaN
            df.dropna(subset=[col_name], inplace=True) 
        except Exception:
             return None, f"La columna '{col_name}' no contiene valores numéricos válidos."


    # 6. Renombrar a una columna estándar 'DAP'
    df = df.rename(columns={col_name: "DAP"})

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