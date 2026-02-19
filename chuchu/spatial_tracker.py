import time

class SpatialTracker:
    def __init__(self):
        # Dictionary to track {bird_id: {"zone": X, "start_time": timestamp}}
        self.dwell_times = {}
        self.HPAI_THRESHOLD = 15 * 60  # 15 minutes in seconds

    def update_bird_position(self, bird_id, current_zone):
        """Logic to detect 'Prolonged Sitting'/Lethargy"""
        current_time = time.time()
        
        if bird_id not in self.dwell_times:
            self.dwell_times[bird_id] = {"zone": current_zone, "start_time": current_time}
            return False

        last_record = self.dwell_times[bird_id]
        
        # Check if bird has moved zones
        if last_record["zone"] == current_zone:
            duration = current_time - last_record["start_time"]
            if duration >= self.HPAI_THRESHOLD:
                print(f"ALERT: Bird {bird_id} stationary in {current_zone} for >15 mins.")
                return True # Suspected Symptom
        else:
            # Bird moved, reset timer
            self.dwell_times[bird_id] = {"zone": current_zone, "start_time": current_time}
            
        return False

    def get_zone(self, x, y, frame_w, frame_h):
        """Maps coordinates to Zones A-I (1-9)"""
        col = x // (frame_w // 3)
        row = y // (frame_h // 3)
        zone_index = row * 3 + col + 1
        return f"Zone_{zone_index}"