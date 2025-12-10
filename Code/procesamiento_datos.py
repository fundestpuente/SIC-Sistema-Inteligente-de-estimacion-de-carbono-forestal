import pandas as pd
import rasterio
import os
import numpy as np

#Definir nombres
rdata = "baad_data.csv"
carpeta_clima = "climate_data" 
archivo_output = "data_entrenamiento.csv"

def obtener_clima(lat,lon):
  """
  Función para extraer temperatura y precipitación 
  de los mapas .tif a partir de coordenadas.
  """
  try:
    #Rutas relativas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_temp = os.path.join(base_dir, carpeta_clima, "T__annual_mean")
    path_prec = os.path.join(base_dir, carpeta_clima, "P__annual_mean")

    #Extraer temperatura
    with rasterio.open(path_temp) as src:
     val_t = list(src.sample([(lon, lat)]))[0][0]
      
    #Extraer precipitación
    with rasterio.open(path_prec) as src:
      val_p = list(src.sample([(lon, lat)]))[0][0]
    return val_t, val_p
  except:
    return np.nan, np.nan #Si falla (e.g coordenadas en el mar), devuelve nan

def procesar_datos():
  print("Cargando base de datos BAAD")
  #Cargar solo las columnas útiles
  #Todas las unidades son kg; kg/m**3, m 
  cols = [
    "latitude", 
    "longitude",
    "d.bh",           #Diámetro a la altura del pecho (DAP)
    "h.t",            #Altura desde el suelo hasta la hoja más alta
    "m.so",           #Toda la Biomasa sobre el nivel de tierra (AGB)
    "d.st",           #densidad de la madera
    "speciesMatched", #Especies corregidas 
    "vegetation"      #Tipo de bosque
  ]
  
  df = pd.read_csv(rdata, usecols=cols)
  #Renombrar columnas
  df = df.rename(columns={
    "Latitude": "latitud",
    "Longitude": "longitud",
    "d.bh": "DAP",
    "h.t": "altura",
    "m.so": "biomasa_",
    "d.st": "densidad_madera",
    "speciesMatched": "especie",
    "vegetation": "tipo_bosque"
  })
  
  print("Tamaño original del dataset: ", df.size)
  print("Limpieza inicial")
  df_limpio = df_limpio.dropna(subset=["DAP", "altura"])

  #filtrar valores ilógicos (negativos o ceros)
  df_limpio = df_limpio[(df_limpio["altura"] > 0) & (df_limpio["DAP"] > 0)]

  con_densidad = df["densidad_madera"].notna().sum()
  print("Filas con densidad disponible: {con_densidad} de {len(df)}")
  print("Datos tras limpieza: {len(df)} filas")
  print("Añadir datos climáticos (Worldclim)")

  temperatura = []
  precipitacion = []

  for index, row in df.iterrows():
    t, p = obtener_clima(row["latitud"], row["longitud"])
    temperatura.append(t)
    precipitacion.append(p)

  df_limpio["temperatura"] = temperatura
  df_limpio["precipitacion"] = precipitacion

  #Eliminar filas sin clima
  df_limpio = df_limpio[(df_limpio["temperatura"] > -100) & (df_limpio["precipitacion"] >= 0)]
  df_limpio = df_limpio.dropna(subset=["temperatura", "precipitaciones"])
  
  print("Datos restantes", len(df))
  df.to_csv(archivo_output, index=False)
  print("Archivo final generado. ", archivo_output)
  print(df.head())

  if __name__ == "__main__":
    procesar_datos()
        
