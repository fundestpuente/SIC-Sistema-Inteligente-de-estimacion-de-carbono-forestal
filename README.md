# TreeVal
# 📌 <SIC-Sistema-Inteligente-de-Estimacion-de-Carbono-Forestal>

**Curso:** Samsung Innovation Campus – Módulo de Python (Ecuador 2025)  
**Seccion:** 'ecuador03'
**Carpeta:** `/<ecuador03>/<SIC-Sistema-Inteligente-de-Estimacion-de-Carbono-Forestal>`

---

## 👥 Integrantes del Grupo
- Ayman El Salous
- Krister Figueroa
- Steve Robinson
- Diego Campos

## Resumen

El sistema propuesto busca implementar una mejora en los estudios de captura de carbono forestal al aplicar un modelo de machine learning para estimar la
biomasa aérea de árboles, y reemplazar las ecuaciones alométricas comúnmente empleadas en este tipo de estudios.


## Planteamiento del problema
Para saber cuánto carbono captura un bosque, tradicionalmente se requieren mediciones complejas, como determinar la altura exacta de cada árbol o aplicar fórmulas alométricas rígidas que no siempre se ajustan a las características biológicas de cada ecosistema.  
Este proceso es lento, costoso y susceptible a errores humanos, especialmente cuando existen datos incompletos provenientes del trabajo de campo.

---

## Objetivos del proyecto
- **Validar la viabilidad técnica** de un modelo de Machine Learning para estimar carbono forestal, demostrando que puede igualar o superar la precisión de métodos alométricos tradicionales.  
- **Reducir los tiempos de entrega** de proyectos relacionados con la estimación de carbono, aumentando la eficiencia, competitividad y la posibilidad de desarrollar nuevas iniciativas ambientales basadas en análisis rápidos y flexibles.

---

## Herramientas utilizadas
- **Python** como lenguaje principal.  
- **Streamlit**, para construir una interfaz gráfica interactiva y accesible.  
- **Random Forest**, como modelo de Machine Learning para la estimación de variables forestales.  
- **Pandas y NumPy**, para manipulación, limpieza y análisis de datos.  

---

## Resultado del proyecto
El proyecto logró integrar un sistema capaz de recibir datos de inventarios forestales, validar y procesar la información ingresada por el usuario, y aplicar un modelo predictivo basado en Random Forest para estimar variables clave relacionadas al carbono forestal.  
La herramienta demuestra que es posible automatizar parte del proceso técnico involucrado en estudios de captura de carbono, facilitando el análisis incluso cuando existen datos faltantes (como la altura). Esto abre la puerta a procesos más ágiles, accesibles y confiables para la evaluación del recurso forestal utilizando inteligencia artificial.

## Estructura del Código 
```
SIC-Sistema-Inteligente-de-estimacion-de-carbono-forestal/
├── Code
│   ├── _init_.py
│   ├── model.py
│   ├── procesamiento_datos.py
│   └── verificacion_input.py
├── Prueba_archivos.py
├── README.md
├── climate_data
│   ├── P_annual_mean.tif
│   ├── T_annual_mean.tif
│   └── baad_data.csv
├── data_entrenamiento.csv
└── interface.py
```

## ⚙️ Instrucciones de Instalación y Ejecución

### Requisitos
- Python 3.9+ (recomendado)
- Git

### Pasos
1. Clonar el repositorio (o asegurarse de estar en la carpeta del proyecto):
   ```bash
   git clone <https://github.com/fundestpuente/SIC-Sistema-Inteligente-de-Estimacion-de-Carbono-Forestal>
   cd SIC-Sistema-Inteligente-de-Estimacion-de-Carbono-Forestal  
   ```

2. Actualizar pip e instalar dependencias:
   ```bash
   pip install --upgrade pip
   pip install streamlit
   ```

3. Ejecutar la aplicación (ejemplo):
   ```bash
   streamlit run interface.py

---


La data se consiguió en el [siguiente repositorio](https://github.com/dfalster/baad/blob/master/data/Garber2005/data.csv)



