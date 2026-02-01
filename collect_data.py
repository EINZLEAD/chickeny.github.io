import sounddevice as sd
import numpy as np
import librosa
import scipy.io.wavfile as wav
import os

FS = 44100
DURATION = 1.0  # 1 second per sample

LABEL = input("Enter zone label (FAR / MID / NEAR): ").strip().upper()
os.makedirs(f"dataset/{LABEL}", exist_ok=True)

count = 0
print("Recording... Press Ctrl+C to stop")

try:
    while True:
        audio = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
        sd.wait()

        filename = f"dataset/{LABEL}/{LABEL}_{count}.wav"
        wav.write(filename, FS, audio)

        print("Saved:", filename)
        count += 1

except KeyboardInterrupt:
    print("Done collecting data.")
