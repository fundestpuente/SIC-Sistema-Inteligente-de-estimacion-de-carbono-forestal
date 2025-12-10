#Se añaden variables climáticas para completar el dataset y se hace limpieza de datos
#Probando datos cargados 
import rasterio
import os

path_temp = "climate_data/P_annual_mean.tif" #Cambiar por ruta en computador

if os.path.exist(path_temp):
  print("archivo encontrado:", path_temp)
  try:
    src = rasterio.open(path_temp)
    print("Abierto correctamente")
    
    #Coords de prueba (Quito)
    lat = -0.18
    lon = -78.46

    #Obtener valor
    vals = src.sample([(lon,lat)])
    temp_leida = list(vals)[0][0]
    
    print(f"En Quito ({lat}, {lon}) la temperatura media del mapa es {temp_leida}")
  
  except Exception as e:
    print("Error al leer el mapa {e}")
else:
    print("No se encuentra el archivo en: {path_temp}")
    print("Verificar nombre de carpetas y archivos")

    


    
