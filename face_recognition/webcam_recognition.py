import cv2
import numpy as np
import os
import json
from datetime import datetime

class WebcamFaceRecognition:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = {}
        self.face_encodings = {}
        self.attendance_file = 'attendance.json'
        self.reference_folder = 'reference_faces'
        
        # Load existing reference faces
        self.load_reference_faces()
        self.load_attendance()
    
    def load_reference_faces(self):
        """Load reference faces from folder"""
        if not os.path.exists(self.reference_folder):
            return
        
        for filename in os.listdir(self.reference_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                person_name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.reference_folder, filename)
                
                image = cv2.imread(image_path)
                if image is not None:
                    # Extract face features
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    if len(faces) > 0:
                        x, y, w, h = faces[0]
                        face_roi = gray[y:y+h, x:x+w]
                        face_roi = cv2.resize(face_roi, (100, 100))
                        
                        self.face_encodings[person_name] = face_roi
                        self.known_faces[person_name] = image
                        print(f"✅ Loaded reference: {person_name}")
    
    def load_attendance(self):
        """Load attendance data"""
        if os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'r') as f:
                self.attendance_data = json.load(f)
        else:
            self.attendance_data = {}
    
    def save_attendance(self):
        """Save attendance data"""
        with open(self.attendance_file, 'w') as f:
            json.dump(self.attendance_data, f, indent=2)
    
    def compare_faces(self, face1, face2):
        """Compare two face encodings"""
        try:
            result = cv2.matchTemplate(face1, face2, cv2.TM_CCOEFF_NORMED)
            similarity = np.max(result)
            return similarity
        except:
            return 0
    
    def recognize_face(self, face_roi):
        """Recognize face from ROI"""
        if len(self.face_encodings) == 0:
            return "Unknown", 0
        
        best_match = None
        best_similarity = 0
        
        for name, ref_encoding in self.face_encodings.items():
            similarity = self.compare_faces(face_roi, ref_encoding)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = name
        
        if best_similarity > 0.6:  # Recognition threshold
            return best_match, best_similarity
        else:
            return "Unknown", best_similarity
    
    def mark_attendance(self, person_name):
        """Mark attendance for recognized person"""
        today = datetime.now().strftime('%Y-%m-%d')
        time_now = datetime.now().strftime('%H:%M:%S')
        
        if today not in self.attendance_data:
            self.attendance_data[today] = {}
        
        if person_name not in self.attendance_data[today]:
            self.attendance_data[today][person_name] = time_now
            self.save_attendance()
            return True, f"Attendance marked for {person_name} at {time_now}"
        else:
            return False, f"{person_name} already marked attendance today"
    
    def run_recognition(self):
        """Run real-time face recognition"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open camera")
            return
        
        print("🎥 Starting webcam face recognition...")
        print("Press 'q' to quit, 's' to save current frame")
        
        frame_count = 0
        last_attendance_check = {}
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Process each detected face
            for (x, y, w, h) in faces:
                # Extract face region
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                
                # Recognize face
                name, confidence = self.recognize_face(face_roi)
                
                # Draw rectangle and label
                if name != "Unknown":
                    color = (0, 255, 0)  # Green for recognized
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
                    cv2.putText(frame, f"{name} ({confidence:.2f})", 
                              (x+6, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    # Check attendance (once per 30 frames to avoid spam)
                    if frame_count % 30 == 0:
                        if name not in last_attendance_check or frame_count - last_attendance_check[name] > 300:
                            success, message = self.mark_attendance(name)
                            if success:
                                print(f"✅ {message}")
                            last_attendance_check[name] = frame_count
                else:
                    color = (0, 0, 255)  # Red for unknown
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
                    cv2.putText(frame, f"Unknown ({confidence:.2f})", 
                              (x+6, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add info text
            cv2.putText(frame, f"Faces: {len(faces)} | Known: {len(self.known_faces)}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit, 's' to save", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('Face Recognition', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save current frame
                filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Saved: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()
        print("👋 Webcam recognition stopped")

def main():
    print("🎭 Webcam Face Recognition System")
    print("=" * 40)
    
    # Check if reference faces exist
    if not os.path.exists('reference_faces') or len(os.listdir('reference_faces')) == 0:
        print("⚠️  No reference faces found!")
        print("Please add reference images to 'reference_faces' folder first.")
        print("You can use the main system to upload reference images.")
        return
    
    wr = WebcamFaceRecognition()
    
    if len(wr.known_faces) == 0:
        print("❌ No valid reference faces loaded!")
        return
    
    print(f"✅ Loaded {len(wr.known_faces)} reference faces:")
    for name in wr.known_faces.keys():
        print(f"  - {name}")
    
    print("\n🎥 Starting webcam recognition...")
    wr.run_recognition()

if __name__ == "__main__":
    main()
