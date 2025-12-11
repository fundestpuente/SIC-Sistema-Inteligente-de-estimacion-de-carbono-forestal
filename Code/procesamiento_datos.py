import pandas as pd
import rasterio
import os
import numpy as np
from pathlib import Path

# ====================== CONFIGURACIÓN ======================
rdata = "../climate_data/baad_data.csv"
archivo_output = "data_entrenamiento.csv"

# RUTAS EXACTAS
TIF_TEMP = os.path.join("climate_data", "T_annual_mean.tif")
TIF_PREC = os.path.join("climate_data", "P_annual_mean.tif")


# ====================== FUNCIÓN CLIMA ======================
def obtener_clima(lat, lon):
    try:
        if not Path(TIF_TEMP).exists():
            raise FileNotFoundError(f"No encontrado: {TIF_TEMP}")
        if not Path(TIF_PREC).exists():
            raise FileNotFoundError(f"No encontrado: {TIF_PREC}")

        with rasterio.open(TIF_TEMP) as src:
            val_t = next(src.sample([(lon, lat)]))[0]
        with rasterio.open(TIF_PREC) as src:
            val_p = next(src.sample([(lon, lat)]))[0]

        # Limpieza de NoData
        if val_t in [-9999, -3.4e+38, 65535, None] or np.isnan(val_t):
            val_t = np.nan
        if val_p in [-9999, -3.4e+38, 65535, None] or np.isnan(val_p):
            val_p = np.nan

        return float(val_t), float(val_p)

    except Exception as e:
        print(f"Error clima ({lat:.2f}, {lon:.2f}): {e}")
        return np.nan, np.nan


# ====================== PROCESAMIENTO ======================
def procesar_datos(ruta):
    print("Cargando BAAD...")

    cols = [
        "latitude", "longitude",
        "d.bh", "h.t", "m.so", "m.st", "r.st",
        "speciesMatched", "vegetation"
    ]

    df = pd.read_csv(ruta, usecols=cols)

    df = df.rename(columns={
        "latitude": "latitud",
        "longitude": "longitud",
        "d.bh": "DAP",
        "h.t": "altura",
        "m.so": "biomasa",
        "m.st": "m_st",
        "speciesMatched": "especie",
        "vegetation": "tipo_bosque",
        "r.st": "densidad"
    })


    print(f"Tamaño original: {len(df)} filas")

    # ========= LIMPIEZA =========
    df_limpio = df.dropna()
    df_limpio = df_limpio[(df_limpio["DAP"] > 0) & (df_limpio["altura"] > 0)]

    df["captura_carbono"] = 0.5 * (df["biomasa"]) # Se asume como factor 0.5

    print(f"Tras limpieza DAP/altura: {len(df_limpio)} filas")
    print(f"Filas con m.st (biomasa tronco): {df_limpio['m_st'].notna().sum()}")

    # ========= AÑADIR CLIMA =========
    print("Extrayendo datos climáticos (puede tardar 3-10 minutos)...")
    temps = []
    precs = []
    for idx, row in df_limpio.iterrows():
        if idx % 1000 == 0:
            print(f"   → Procesado {idx}/{len(df_limpio)}")
        t, p = obtener_clima(row["latitud"], row["longitud"])
        temps.append(t)
        precs.append(p)

    df_limpio = df_limpio.copy()
    df_limpio["temperatura"] = temps
    df_limpio["precipitacion"] = precs

    # Filtrar valores climáticos válidos
    antes = len(df_limpio)
    df_limpio = df_limpio.dropna(subset=["temperatura", "precipitacion"])
    df_limpio = df_limpio[(df_limpio["temperatura"] > -50) & (df_limpio["precipitacion"] >= 0)]
    print(f"Datos climáticos válidos: {len(df_limpio)} filas (eliminados: {antes - len(df_limpio)})")

    # ========= GUARDAR =========
    df_limpio.to_csv(archivo_output, index=False)
    print(f"\n¡ÉXITO TOTAL! Archivo generado:")
    print(f"→ {os.path.abspath(archivo_output)}")
    print(f"→ Filas finales: {len(df_limpio)}")
    print("\nPrimeras filas del resultado:")
    print(df_limpio.head())

    return df_limpio


# ====================== EJECUCIÓN ======================
if __name__ == "__main__":
    procesar_datos(rdata)