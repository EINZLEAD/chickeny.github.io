from flask import Flask, Response, jsonify
import cv2
import time
import threading

app = Flask(__name__)

# CAMERA
camera = cv2.VideoCapture(0)  # USB cam / CCTV capture device

# EVENTS STORAGE
events = []

def generate_video():
    while True:
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/events')
def get_events():
    return jsonify(events[-10:])

def add_event(zone):
    events.append({
        "time": time.strftime("%H:%M:%S"),
        "zone": zone,
        "status": "Suspected",
        "remark": "Abnormal cough detected"
    })

# 🔊 AUDIO DETECTION THREAD (SHOTGUN MIC)
def audio_loop():
    import sounddevice as sd
    import numpy as np
    from scipy.signal import butter, lfilter

    FS = 44100
    LOW, HIGH = 1000, 4000

    def bandpass(data):
        b, a = butter(4, [LOW/(FS/2), HIGH/(FS/2)], btype='band')
        return lfilter(b, a, data)

    while True:
        audio = sd.rec(int(0.05 * FS), samplerate=FS, channels=1)
        sd.wait()
        filtered = bandpass(audio[:,0])
        energy = np.sqrt(np.mean(filtered**2))

        if energy > 0.04:
            if energy > 0.07:
                zone = "G-H-I"
            elif energy > 0.05:
                zone = "D-E-F"
            else:
                zone = "A-B-C"

            add_event(zone)
            time.sleep(1)

threading.Thread(target=audio_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
