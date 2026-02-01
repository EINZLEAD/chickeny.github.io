import librosa
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

X = []
y = []

def extract_features(file):
    audio, sr = librosa.load(file, sr=44100)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    rms = np.mean(librosa.feature.rms(y=audio))
    return np.hstack([mfcc_mean, rms])

for label in ["FAR", "MID", "NEAR"]:
    folder = f"dataset/{label}"
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            features = extract_features(os.path.join(folder, file))
            X.append(features)
            y.append(label)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, "sonar_zone_model.pkl")
print("✅ Model saved as sonar_zone_model.pkl")
