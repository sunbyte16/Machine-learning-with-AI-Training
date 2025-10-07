import cv2
import numpy as np
import os
import json
from datetime import datetime
import time

class WebcamRecognitionNoDisplay:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = {}
        self.face_encodings = {}
        self.attendance_file = 'attendance.json'
        self.reference_folder = 'reference_faces'
        
        # Create results folder
        if not os.path.exists('webcam_results'):
            os.makedirs('webcam_results')
        
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
    
    def run_recognition(self, duration=30):
        """Run face recognition for specified duration (seconds)"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open camera")
            return
        
        print(f"🎥 Starting webcam recognition for {duration} seconds...")
        print("Press Ctrl+C to stop early")
        
        start_time = time.time()
        frame_count = 0
        faces_detected = 0
        recognitions = 0
        last_attendance_check = {}
        
        try:
            while (time.time() - start_time) < duration:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Error: Could not read frame")
                    break
                
                frame_count += 1
                
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                frame_recognitions = []
                
                # Process each detected face
                for (x, y, w, h) in faces:
                    faces_detected += 1
                    
                    # Extract face region
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (100, 100))
                    
                    # Recognize face
                    name, confidence = self.recognize_face(face_roi)
                    
                    # Draw rectangle and label on frame
                    if name != "Unknown":
                        color = (0, 255, 0)  # Green for recognized
                        recognitions += 1
                        frame_recognitions.append(f"{name} ({confidence:.2f})")
                        
                        # Check attendance (once per 30 frames to avoid spam)
                        if frame_count % 30 == 0:
                            if name not in last_attendance_check or frame_count - last_attendance_check[name] > 300:
                                success, message = self.mark_attendance(name)
                                if success:
                                    print(f"✅ {message}")
                                last_attendance_check[name] = frame_count
                    else:
                        color = (0, 0, 255)  # Red for unknown
                        frame_recognitions.append(f"Unknown ({confidence:.2f})")
                    
                    # Draw rectangle
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
                    cv2.putText(frame, f"{name} ({confidence:.2f})", 
                               (x+6, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Add info text
                elapsed = time.time() - start_time
                remaining = duration - elapsed
                cv2.putText(frame, f"Time: {remaining:.1f}s | Faces: {len(faces)} | Known: {len(self.known_faces)}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Save frame if faces detected
                if len(faces) > 0:
                    filename = f"webcam_results/frame_{frame_count:04d}_{len(faces)}faces.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"📸 Frame {frame_count}: {len(faces)} face(s) - {', '.join(frame_recognitions)}")
                
                # Progress update every 5 seconds
                if frame_count % 150 == 0:  # Assuming 30 FPS
                    print(f"⏱️  Progress: {elapsed:.1f}s / {duration}s - {frame_count} frames processed")
        
        except KeyboardInterrupt:
            print("\n👋 Stopped by user")
        
        finally:
            cap.release()
            
            # Save final summary
            summary = {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': time.time() - start_time,
                'total_frames': frame_count,
                'faces_detected': faces_detected,
                'recognitions': recognitions,
                'reference_faces': len(self.known_faces)
            }
            
            with open('webcam_results/session_summary.json', 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f"\n📊 Session Summary:")
            print(f"Duration: {summary['duration_seconds']:.1f} seconds")
            print(f"Frames processed: {frame_count}")
            print(f"Faces detected: {faces_detected}")
            print(f"Successful recognitions: {recognitions}")
            print(f"Reference faces loaded: {len(self.known_faces)}")
            print(f"Results saved in: webcam_results/")

def main():
    print("🎭 Webcam Recognition (No Display)")
    print("=" * 40)
    
    # Check if reference faces exist
    if not os.path.exists('reference_faces') or len(os.listdir('reference_faces')) == 0:
        print("⚠️  No reference faces found!")
        print("This will run in face detection mode only (no recognition)")
        print("Add reference images to 'reference_faces' folder for recognition")
    
    wr = WebcamRecognitionNoDisplay()
    
    if len(wr.known_faces) > 0:
        print(f"✅ Loaded {len(wr.known_faces)} reference faces:")
        for name in wr.known_faces.keys():
            print(f"  - {name}")
    else:
        print("ℹ️  Running in face detection mode only")
    
    # Get duration from user
    try:
        duration = int(input("\nEnter duration in seconds (default 30): ") or "30")
    except ValueError:
        duration = 30
    
    print(f"\n🎥 Starting {duration}-second session...")
    wr.run_recognition(duration)

if __name__ == "__main__":
    main()
