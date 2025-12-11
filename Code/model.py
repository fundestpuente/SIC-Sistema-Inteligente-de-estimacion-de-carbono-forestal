import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

from sklearn.model_selection import train_test_split

def modelo(df):

    target = "biomasa"
    features = ["DAP", "altura", "m_st"]

    X = df[features]
    y = df[target]

    # crear variables para el entrenamiento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Crear el modelo
    rf = RandomForestRegressor(
        n_estimators=200,       # número de árboles
        max_depth=None,         # sin límite de profundidad
        min_samples_split=2,    # criterio de división
        random_state=42,        # reproducibilidad
        n_jobs=-1               # usa todos los núcleos del procesador
    )

    # Entrenamiento
    rf.fit(X_train, y_train)

    # Predicciones
    y_pred_rf = rf.predict(X_test)

    # Métricas
    r2_rf = r2_score(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)

    importances = pd.DataFrame({
        'Variable': features,
        'Importancia': rf.feature_importances_
    }).sort_values(by='Importancia', ascending=False)

    print("R2 = ", r2_rf)
    print("Mean absolute error =", mae_rf)
    print(importances)

    return r2_rf, mae_rf, importances, rf