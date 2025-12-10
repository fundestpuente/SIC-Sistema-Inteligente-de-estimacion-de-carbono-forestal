import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

# crear variables para el entrenamiento, no es mi parte lol
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

