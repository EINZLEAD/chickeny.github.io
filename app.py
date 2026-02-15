import cv2
import threading
import time
import requests
import numpy as np 
from flask import Flask, Response

app = Flask(__name__)

# --- CONFIGURATION ---
VIDEO_SOURCE = "rtsp://Chicken:chicken123@192.168.100.88:554/stream1" 
API_URL = "http://localhost/chickenarium/api/get_monitoring.php" 

# Global alerts dictionary
active_alerts = {}

def fetch_db_status():
    global active_alerts
    while True:
        try:
            r = requests.get(API_URL, timeout=1)
            if r.status_code == 200:
                data = r.json()
                new_alerts = {}
                if data:
                    for item in data:
                        zone = item.get('zone')
                        status = item.get('health_status')
                        if zone and status in ["Critical", "Warning", "Problem Detected"]:
                            if zone not in new_alerts:
                                new_alerts[zone] = status
                            elif status == "Critical":
                                new_alerts[zone] = status
                active_alerts = new_alerts
        except:
            pass
        time.sleep(1)

# Helper function para sa math ng lines
def get_point_on_line(p1, p2, t):
    x = int(p1[0] + (p2[0] - p1[0]) * t)
    y = int(p1[1] + (p2[1] - p1[1]) * t)
    return (x, y)

def draw_grid_on_frame(frame):
    if frame is None: return frame
    
    # Resize frame (Standard 800x450)
    frame = cv2.resize(frame, (800, 450))
    h, w = 450, 800

    # --- DITO NATIN IBINABA ANG GRID (FLOOR ADJUSTMENT) ---
    # Binabaan ko ang Y value ng Top-Left at Top-Right para lumapat sa sahig.
    
    # Format: (X, Y) -> Y: 0 is top, 450 is bottom
    
    # Top-Left:  (X=100, Y=250) -> Nasa gitnang-ibaba na siya nagsisimula
    tl = (100, 250)   
    
    # Top-Right: (X=700, Y=250) 
    tr = (700, 250)   
    
    # Bottom-Left: (Sagad sa baba)
    bl = (0, 450)    
    
    # Bottom-Right: (Sagad sa baba)
    br = (800, 450)  

    # --- CALCULATE GRID POINTS ---
    # Interpolate para sa 3x3 Grid
    
    # 1. Compute Horizontal Cuts (Rows)
    # Kukunin natin ang points sa Left Edge at Right Edge
    left_edge_points = [get_point_on_line(tl, bl, i/3) for i in range(4)]
    right_edge_points = [get_point_on_line(tr, br, i/3) for i in range(4)]

    # 2. Compute Vertical Cuts (Columns)
    # Kukunin natin ang points sa Top Edge at Bottom Edge
    top_edge_points = [get_point_on_line(tl, tr, i/3) for i in range(4)]
    bottom_edge_points = [get_point_on_line(bl, br, i/3) for i in range(4)]

    # --- DRAW GRID LINES (Green) ---
    
    # Horizontal Lines
    for i in range(4):
        cv2.line(frame, left_edge_points[i], right_edge_points[i], (0, 255, 0), 2)

    # Vertical Lines (Perspective)
    for i in range(4):
        cv2.line(frame, top_edge_points[i], bottom_edge_points[i], (0, 255, 0), 2)

    # --- DRAW ACTIVE ZONES (Trapezoids) ---
    grid_map = {
        'A': (0,0), 'B': (1,0), 'C': (2,0),
        'D': (0,1), 'E': (1,1), 'F': (2,1),
        'G': (0,2), 'H': (1,2), 'I': (2,2)
    }

    current_alerts = active_alerts.copy()

    for zone, status in current_alerts.items():
        if zone in grid_map:
            c, r = grid_map[zone] # c=col, r=row

            # Hanapin ang 4 na kanto ng specific cell na ito
            # Row Top & Bottom
            row_top_l = left_edge_points[r]
            row_top_r = right_edge_points[r]
            row_bot_l = left_edge_points[r+1]
            row_bot_r = right_edge_points[r+1]

            # Ngayon, hanapin ang exact corners ng cell gamit ang Columns logic
            # Top-Left & Top-Right ng Cell
            cell_tl = get_point_on_line(row_top_l, row_top_r, c/3)
            cell_tr = get_point_on_line(row_top_l, row_top_r, (c+1)/3)
            
            # Bottom-Left & Bottom-Right ng Cell
            cell_bl = get_point_on_line(row_bot_l, row_bot_r, c/3)
            cell_br = get_point_on_line(row_bot_l, row_bot_r, (c+1)/3)

            # Buuin ang Polygon points
            pts = np.array([cell_tl, cell_tr, cell_br, cell_bl], np.int32)
            pts = pts.reshape((-1, 1, 2))

            # Color Coding
            if status == "Critical":
                color = (0, 0, 255)   # Red
                text_label = f"CRIT: {zone}"
            else:
                color = (0, 165, 255) # Orange
                text_label = f"WARN: {zone}"

            # Fill & Border
            overlay = frame.copy()
            cv2.fillPoly(overlay, [pts], color)
            cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
            cv2.polylines(frame, [pts], True, color, 3)

            # Center Text
            center_x = (cell_tl[0] + cell_br[0]) // 2
            center_y = (cell_tl[1] + cell_br[1]) // 2
            cv2.putText(frame, text_label, (center_x - 30, center_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame

def gen_frames():
    while True:
        cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not cap.isOpened():
            print("--- Waiting for Camera... ---")
            time.sleep(3)
            continue
        
        print("--- Floor Grid Active! ---")
        while True:
            success, frame = cap.read()
            if not success: break
            try:
                frame = draw_grid_on_frame(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret: continue
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            except Exception as e:
                break
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    threading.Thread(target=fetch_db_status, daemon=True).start()
    app.run(host='0.0.0.0', port=5001, threaded=True)