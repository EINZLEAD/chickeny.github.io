import sounddevice as sd
import numpy as np
import librosa
import joblib
from scipy.signal import butter, lfilter

FS = 44100
DURATION = 0.5

model = joblib.load("sonar_zone_model.pkl")

LOW, HIGH = 1000, 4000

def bandpass(data):
    b, a = butter(4, [LOW/(FS/2), HIGH/(FS/2)], btype='band')
    return lfilter(b, a, data)

def extract_features(audio):
    mfcc = librosa.feature.mfcc(y=audio, sr=FS, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    rms = np.mean(librosa.feature.rms(y=audio))
    return np.hstack([mfcc_mean, rms])

print("🔊 Sonar detection running...")

while True:
    audio = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
    sd.wait()

    audio = bandpass(audio[:,0])
    features = extract_features(audio).reshape(1, -1)

    zone = model.predict(features)[0]
    confidence = max(model.predict_proba(features)[0])

    if confidence > 0.6:
        print(f"🐔 Sound from {zone} zone (confidence {confidence:.2f})")
