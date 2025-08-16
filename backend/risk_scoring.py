import joblib
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from encoders import mark_invalid_ages_as_nan, to_lower, CustomLabelEncoder


try:
    risk_pipeline = joblib.load("models/risk_pipeline.pkl")
    print("Pipeline chargé avec succès !")
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du pipeline: {str(e)}")

EXPECTED_FEATURES = [
    'age', 'nationality', 'gender', 'Activites_label', 'Produits', 
    'Relation', 'Pays', 'isPEP', 'famCode', 'VoieDeDistribution'
]

def predict_risk_coefficient_with_proba(feature_dict: Dict) -> Tuple[str, Dict[str, float]]:
    risk_mapping = {'00': 'RE', '01': 'RF', '10': 'RM'}

    missing_features = [f for f in EXPECTED_FEATURES if f not in feature_dict]
    if missing_features:
        raise ValueError(f"Features manquantes: {missing_features}")

    input_df = pd.DataFrame([feature_dict])[EXPECTED_FEATURES]

    input_df = mark_invalid_ages_as_nan(input_df)

    pred_probas = risk_pipeline.predict_proba(input_df)[0]
    model_classes = risk_pipeline.classes_.astype(str)

    predicted_class_code = model_classes[np.argmax(pred_probas)]
    predicted_risk = risk_mapping.get(predicted_class_code, "Inconnu")

    risk_percentages = {
        risk_mapping.get(cls, cls): prob * 100
        for cls, prob in zip(model_classes, pred_probas)
    }

    print(f"La classe prédite est: {predicted_risk}")
    print("Probabilités pour chaque classe:")
    for label, proba in risk_percentages.items():
        print(f"{label}: {proba:.2f}%")
    print(f"Score global : {risk_percentages[predicted_risk]:.2f}%")

    return predicted_risk, risk_percentages
