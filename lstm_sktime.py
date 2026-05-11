import numpy as np
from sktime.forecasting.compose import make_reduction
from sklearn.ensemble import RandomForestRegressor
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.datasets import load_airline
import json
from datetime import datetime

print("\n=== PRÉDICTION SÉQUENTIELLE (LSTM-like) ===\n")

# simuler des cybermenaces dans le temps
t = np.arange(0, 200)
y = 15 + 5 * np.sin(t / 20) + 0.05 * t + np.random.normal(0, 1, 200)

y_train, y_test = temporal_train_test_split(y, test_size=30)

regressor = RandomForestRegressor(n_estimators=50)
forecaster = make_reduction(regressor, window_length=10, strategy="recursive")
forecaster.fit(y_train)

y_pred = forecaster.predict(fh=np.arange(1, 31))

print("Prédictions (30 prochains pas) :", np.round(y_pred[:5], 2))

result = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "modele": "LSTM-like (sktime + RandomForest)",
    "prediction_sample": y_pred[:5].tolist()
}

with open("lstm_results.json", "w") as f:
    json.dump(result, f, indent=2)

print("\n✅ lstm_results.json sauvegardé")