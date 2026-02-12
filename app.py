import cv2
import threading
import time
import numpy as np
import requests
from flask import Flask, Response

app = Flask(__name__)

# --- CONFIGURATION ---
VIDEO_SOURCE = 0 
API_URL = "http://localhost/chickenarium/api/get_monitoring.php" 

current_zone = None
current_status = ""

def fetch_db_status():
    global current_zone, current_status
    while True:
        try:
            # Kumukuha ng data sa PHP mo
            r = requests.get(API_URL, timeout=2)
            if r.status_code == 200:
                data = r.json()
                if data and len(data) > 0:
                    # Kinukuha ang pinaka-latest na record (Index 0)
                    current_zone = data[0].get('zone')
                    current_status = data[0].get('health_status')
        except Exception as e:
            print(f"Error fetching data: {e}")
        time.sleep(1)

def draw_grid_on_frame(frame):
    # Standardize size para saktong-sakto ang lines
    frame = cv2.resize(frame, (800, 450))
    h, w = 450, 800
    
    col_w = w // 3
    row_h = h // 3

    # 1. DRAW WHITE GRID LINES (Ito ang visual grid mo sa video)
    # Vertical lines
    cv2.line(frame, (col_w, 0), (col_w, h), (255, 255, 255), 2)
    cv2.line(frame, (2 * col_w, 0), (2 * col_w, h), (255, 255, 255), 2)
    # Horizontal lines
    cv2.line(frame, (0, row_h), (w, row_h), (255, 255, 255), 2)
    cv2.line(frame, (0, 2 * row_h), (w, 2 * row_h), (255, 255, 255), 2)

    # 2. RED BOX INDICATOR (Magpapakita lang kung may Problem/Warning)
    grid_map = {
        'A': (0,0), 'B': (1,0), 'C': (2,0),
        'D': (0,1), 'E': (1,1), 'F': (2,1),
        'G': (0,2), 'H': (1,2), 'I': (2,2)
    }

    # I-highlight ang zone kung ang status ay hindi "Healthy"
    if current_zone in grid_map and current_status in ["Critical", "Warning", "Problem Detected"]:
        c, r = grid_map[current_zone]
        x1, y1 = c * col_w, r * row_h
        x2, y2 = x1 + col_w, y1 + row_h
        
        # Gumawa ng pulang box na may konting transparency
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        # Solid red border para matalas tingnan
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
        
        # Optional: Maglagay ng text sa loob ng box
        cv2.putText(frame, f"ALARM: {current_zone}", (x1+10, y1+30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return frame

def gen_frames():
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Dito natin tinatawag ang drawing ng grid bago i-send sa browser
            frame = draw_grid_on_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the background thread for DB sync
    threading.Thread(target=fetch_db_status, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, threaded=True)