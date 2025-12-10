# TreeVal

## SIC-Sistema-Inteligente-de-Estimacion-de-Carbono-Forestal

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


La data se consiguió en el [siguiente repositorio](https://github.com/dfalster/baad/blob/master/data/Garber2005/data.csv)



