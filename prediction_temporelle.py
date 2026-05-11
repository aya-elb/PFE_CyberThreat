import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

print("\n=== MODELE TEMPOREL ===\n")

dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
n_jours = len(dates)

np.random.seed(42)
tendance = np.linspace(5, 20, n_jours)
saisonnalite = 5 * np.sin(np.linspace(0, 4*np.pi, n_jours))
bruit = np.random.normal(0, 3, n_jours)

menaces_par_jour = tendance + saisonnalite + bruit
menaces_par_jour = np.maximum(0, menaces_par_jour)

df = pd.DataFrame({
    'date': dates,
    'nb_menaces': menaces_par_jour
})

print(f"Donnees generees : du {dates[0].strftime('%Y-%m-%d')} au {dates[-1].strftime('%Y-%m-%d')}")
print(f"Total : {n_jours} jours")
print(f"Moyenne : {menaces_par_jour.mean():.1f} menaces/jour")

df['jour_index'] = range(len(df))
df['mois'] = df['date'].dt.month
df['jour_semaine'] = df['date'].dt.dayofweek

train_size = int(0.8 * len(df))
train = df[:train_size]
test = df[train_size:]

X_train = train[['jour_index', 'mois', 'jour_semaine']].values
y_train = train['nb_menaces'].values
X_test = test[['jour_index', 'mois', 'jour_semaine']].values
y_test = test['nb_menaces'].values

print(f"Entrainement : {len(train)} jours")
print(f"Test : {len(test)} jours")

modele = LinearRegression()
modele.fit(X_train, y_train)

y_pred = modele.predict(X_test)
erreur_moyenne = np.mean(np.abs(y_test - y_pred))
print(f"Modele entraine")
print(f"Erreur moyenne : {erreur_moyenne:.2f} menaces/jour")

dernier_jour = df['date'].iloc[-1]
jours_futurs = 30
dates_futures = [dernier_jour + timedelta(days=i+1) for i in range(jours_futurs)]

futur_jour_index = np.arange(len(df), len(df) + jours_futurs)
futur_mois = [d.month for d in dates_futures]
futur_jour_semaine = [d.dayofweek for d in dates_futures]

X_futur = np.array([futur_jour_index, futur_mois, futur_jour_semaine]).T
predictions_futur = modele.predict(X_futur)

plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['nb_menaces'], 'b-', alpha=0.7, label='Historique')
plt.plot(test['date'], y_pred, 'r--', alpha=0.7, label='Prediction sur test')
plt.plot(dates_futures, predictions_futur, 'g-', linewidth=2, label='Prediction future (30j)')

plt.xlabel('Date')
plt.ylabel('Nombre de menaces par jour')
plt.title('Prediction temporelle des cybermenaces')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.savefig('prediction_menaces.png', dpi=100, bbox_inches='tight')
print("Graphique sauvegarde : prediction_menaces.png")

resultats = {
    "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "modele": "Regression Lineaire",
    "erreur_moyenne": round(erreur_moyenne, 2),
    "predictions_futur": []
}

for i, (date, pred) in enumerate(zip(dates_futures, predictions_futur)):
    resultats["predictions_futur"].append({
        "jour": i+1,
        "date": date.strftime("%Y-%m-%d"),
        "nb_menaces_predites": round(pred, 1)
    })

with open("prediction_temporelle_resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print("\nRESUME DE LA PREDICTION")
print("="*50)
print(f"Prediction sur 30 jours :")
print(f"   Moyenne : {np.mean(predictions_futur):.1f} menaces/jour")
print(f"   Maximum : {np.max(predictions_futur):.1f} menaces")
print(f"   Minimum : {np.min(predictions_futur):.1f} menaces")

if np.max(predictions_futur) > 25:
    print(f"\nPic d'activite prevu le {dates_futures[np.argmax(predictions_futur)].strftime('%Y-%m-%d')}")

print("\n=== FIN MODELE TEMPOREL ===")