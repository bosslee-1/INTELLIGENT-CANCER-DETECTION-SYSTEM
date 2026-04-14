import joblib
import numpy as np
import os
from flask import jsonify

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL = joblib.load(os.path.join(MODELS_DIR, "cancer_model.pkl"))
ENCODER = joblib.load(os.path.join(MODELS_DIR, "label_encoder.pkl"))
FEATURES = joblib.load(os.path.join(MODELS_DIR, "symptom_list.pkl"))

def predict(data):
    try:
        symptoms = data.get("symptoms", [])

        vector = []
        for f in FEATURES:
            vector.append(1 if any(s.lower() in f.lower() for s in symptoms) else 0)

        X = np.array([vector])
        probs = MODEL.predict_proba(X)[0]

        results = {}
        for i, p in enumerate(probs):
            label = ENCODER.inverse_transform([i])[0]
            if label != "none":
                results[label] = round(p * 100, 2)

        return jsonify({"success": True, "predictions": results}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500