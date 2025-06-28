import os
import cv2
import face_recognition
import numpy as np
import hashlib
import time
from ultralytics import YOLO
from constants import KNOWN_FACES_DIR, YOLO_MODEL_PATH

class VisionProcessor:
    def __init__(self, message_callback=None):
        self.message_callback = message_callback or print
        self.known_face_encodings = []
        self.known_face_names = []
        self.yolo = None
        self.last_detection_time = {}
        self.unknown_face_cooldown = {}
        self.load_models()
        self.load_known_faces()
    
    def load_models(self):
        try:
            self.yolo = YOLO(YOLO_MODEL_PATH)
            self.message_callback("✅ YOLO model loaded successfully!")
        except Exception as e:
            self.message_callback(f"❌ YOLO model failed to load: {str(e)}")
            try:
                self.yolo = YOLO("yolov8n.pt")
                self.message_callback("✅ YOLO model downloaded and loaded!")
            except Exception as e2:
                self.message_callback(f"❌ YOLO download failed: {str(e2)}")
    
    def load_known_faces(self):
        if not os.path.exists(KNOWN_FACES_DIR):
            os.makedirs(KNOWN_FACES_DIR)
            
        self.known_face_encodings = []
        self.known_face_names = []
        
        for filename in os.listdir(KNOWN_FACES_DIR):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                try:
                    image_path = os.path.join(KNOWN_FACES_DIR, filename)
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_names.append(os.path.splitext(filename)[0])
                        self.message_callback(f"✅ Loaded face: {os.path.splitext(filename)[0]}")
                except Exception as e:
                    self.message_callback(f"❌ Failed to load {filename}: {str(e)}")
    
    def process_frame(self, frame):
        try:
            display_frame = frame.copy()
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(
                rgb_small_frame, 
                model="hog",
                number_of_times_to_upsample=1
            )
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            current_time = time.time()
            face_count = 0
            
            for i, (face_encoding, (top, right, bottom, left)) in enumerate(zip(face_encodings, face_locations)):
                top = int(top * 2)
                right = int(right * 2)
                bottom = int(bottom * 2)
                left = int(left * 2)
                
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"
                color = (0, 0, 255)
                confidence = 0
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    color = (0, 255, 0)
                    
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    confidence = 1 - face_distances[first_match_index]
                
                cv2.rectangle(display_frame, (left, top), (right, bottom), color, 3)
                label = f"{name}"
                if confidence > 0:
                    label += f" ({confidence:.2f})"
                
                cv2.rectangle(display_frame, (left, bottom - 40), (right, bottom), color, cv2.FILLED)
                cv2.putText(display_frame, label, (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
                
                face_count += 1
            
            # Object detection with YOLO
            if self.yolo:
                try:
                    results = self.yolo(small_frame, verbose=False, conf=0.3)
                    if results and len(results) > 0:
                        boxes = results[0].boxes
                        if boxes is not None:
                            object_count = 0
                            for box in boxes:
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                conf = float(box.conf[0])
                                cls = int(box.cls[0])
                                
                                if conf > 0.3:
                                    x1, y1, x2, y2 = x1*2, y1*2, x2*2, y2*2
                                    label = f"{results[0].names[cls]} {conf:.2f}"
                                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), (255, 165, 0), 2)
                                    cv2.putText(display_frame, label, (x1, y1 - 10), 
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
                                    object_count += 1
                except Exception as e:
                    pass
            
            return display_frame, face_count
            
        except Exception as e:
            self.message_callback(f"❌ Processing error: {str(e)}")
            return frame, 0
    
    def generate_face_hash(self, face_img):
        try:
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (100, 100))
            face_hash = hashlib.sha256(resized.tobytes()).hexdigest()
            return face_hash
        except Exception as e:
            return hashlib.sha256(str(time.time()).encode()).hexdigest()
    
    def register_face(self, face_img, name):
        try:
            filename = f"{KNOWN_FACES_DIR}/{name}.jpg"
            cv2.imwrite(filename, face_img)
            self.load_known_faces()
            return True
        except Exception as e:
            self.message_callback(f"❌ Face registration failed: {str(e)}")
            return False
