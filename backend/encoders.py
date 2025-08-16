from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

# Fonction pour appliquer le LabelEncoder sur un DataFrame
def apply_label_encoder(X):
    # Forcer la conversion en DataFrame si ce n’est pas déjà
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)

    label_encoder = LabelEncoder()
    return X.apply(lambda col: label_encoder.fit_transform(col.astype(str)))

def to_lower(x):
        # Appliquer la transformation sur chaque valeur si c’est un array
        return pd.DataFrame(x).applymap(lambda val: val.lower() if isinstance(val, str) else val)

    # Fonction pour marquer les âges invalides comme NaN
def mark_invalid_ages_as_nan(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    if 'age' in X.columns:
        # Convertir en numérique, les valeurs non convertibles deviennent NaN
        X['age'] = pd.to_numeric(X['age'], errors='coerce')
        # Remplacer les âges < 0 ou > 120 par NaN
        X['age'] = X['age'].apply(lambda x: np.nan if (pd.notna(x) and (x < 0 or x > 120)) else x)
    return X


# Classe pour appliquer le LabelEncoder sur une colonne spécifique
class CustomLabelEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.label_encoders = {}

    def fit(self, X, y=None):
        for col in X.columns:
            le = LabelEncoder()
            if X[col].dtype == 'object' or pd.api.types.is_bool_dtype(X[col]):
                le.fit(X[col])
                self.label_encoders[col] = le
        return self
    
    def transform(self, X):
        X_copy = X.copy()
        for col, le in self.label_encoders.items():
            if col in X.columns:  # Vérifier si la colonne est présente dans X
                X_copy[col] = le.transform(X[col])
        return X_copy