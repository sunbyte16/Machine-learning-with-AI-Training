import cv2
import numpy as np
import os
import shutil
from datetime import datetime
import json

class FaceRecognitionSystem:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = {}
        self.face_encodings = {}
        self.attendance_file = 'attendance.json'
        self.upload_folder = 'uploads'
        self.reference_folder = 'reference_faces'
        
        # Create necessary folders
        self.create_folders()
        self.load_attendance()
    
    def create_folders(self):
        """Create necessary folders"""
        folders = [self.upload_folder, self.reference_folder, 'detection_results']
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"✅ Created folder: {folder}")
    
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
    
    def upload_reference_image(self, image_path, person_name):
        """Upload and process reference image"""
        try:
            # Copy image to reference folder
            filename = f"{person_name}.jpg"
            reference_path = os.path.join(self.reference_folder, filename)
            shutil.copy2(image_path, reference_path)
            
            # Process the image
            image = cv2.imread(reference_path)
            if image is None:
                return False, "Could not load image"
            
            # Detect face
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                os.remove(reference_path)
                return False, "No face detected in image"
            
            if len(faces) > 1:
                os.remove(reference_path)
                return False, "Multiple faces detected. Please use image with single face"
            
            # Extract face features
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (100, 100))
            
            # Store face encoding
            self.face_encodings[person_name] = face_roi
            self.known_faces[person_name] = image
            
            print(f"✅ Successfully uploaded reference for: {person_name}")
            return True, f"Reference image uploaded for {person_name}"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def upload_image_for_recognition(self, image_path):
        """Upload image for face recognition"""
        try:
            # Copy to upload folder
            filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            upload_path = os.path.join(self.upload_folder, filename)
            shutil.copy2(image_path, upload_path)
            
            return upload_path
            
        except Exception as e:
            return None
    
    def recognize_faces_in_image(self, image_path):
        """Recognize faces in uploaded image"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None, "Could not load image"
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return [], "No faces detected in image"
            
            recognized_faces = []
            
            for (x, y, w, h) in faces:
                # Extract face region
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                
                # Compare with known faces
                best_match = None
                best_similarity = 0
                
                for name, ref_encoding in self.face_encodings.items():
                    similarity = self.compare_faces(face_roi, ref_encoding)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = name
                
                # Determine if recognized
                if best_similarity > 0.6:  # Threshold for recognition
                    recognized_faces.append({
                        'name': best_match,
                        'confidence': best_similarity,
                        'location': (x, y, w, h)
                    })
                else:
                    recognized_faces.append({
                        'name': 'Unknown',
                        'confidence': best_similarity,
                        'location': (x, y, w, h)
                    })
            
            return recognized_faces, "Recognition completed"
            
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def compare_faces(self, face1, face2):
        """Compare two face encodings"""
        try:
            result = cv2.matchTemplate(face1, face2, cv2.TM_CCOEFF_NORMED)
            similarity = np.max(result)
            return similarity
        except:
            return 0
    
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
    
    def get_attendance_report(self, date=None):
        """Get attendance report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if date in self.attendance_data:
            return self.attendance_data[date]
        else:
            return {}
    
    def list_reference_faces(self):
        """List all reference faces"""
        return list(self.known_faces.keys())
    
    def delete_reference_face(self, person_name):
        """Delete reference face"""
        try:
            # Remove from memory
            if person_name in self.known_faces:
                del self.known_faces[person_name]
            if person_name in self.face_encodings:
                del self.face_encodings[person_name]
            
            # Remove file
            file_path = os.path.join(self.reference_folder, f"{person_name}.jpg")
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return True, f"Deleted reference for {person_name}"
        except Exception as e:
            return False, f"Error: {str(e)}"

def main():
    print("🎭 Advanced Face Recognition System")
    print("=" * 40)
    
    fr = FaceRecognitionSystem()
    
    while True:
        print("\n📋 Menu:")
        print("1. Upload reference image")
        print("2. Recognize faces in image")
        print("3. View attendance report")
        print("4. List reference faces")
        print("5. Delete reference face")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            print("\n📤 Upload Reference Image")
            image_path = input("Enter image path: ").strip('"')
            person_name = input("Enter person name: ")
            
            if os.path.exists(image_path):
                success, message = fr.upload_reference_image(image_path, person_name)
                print(f"Result: {message}")
            else:
                print("❌ Image file not found!")
        
        elif choice == '2':
            print("\n🔍 Recognize Faces in Image")
            image_path = input("Enter image path: ").strip('"')
            
            if os.path.exists(image_path):
                # Upload image
                upload_path = fr.upload_image_for_recognition(image_path)
                if upload_path:
                    # Recognize faces
                    faces, message = fr.recognize_faces_in_image(upload_path)
                    
                    if faces is not None:
                        print(f"\nRecognition Results: {message}")
                        for i, face in enumerate(faces):
                            print(f"Face {i+1}: {face['name']} (Confidence: {face['confidence']:.2f})")
                            
                            # Mark attendance if recognized
                            if face['name'] != 'Unknown':
                                success, att_msg = fr.mark_attendance(face['name'])
                                print(f"  {att_msg}")
                    else:
                        print(f"❌ Error: {message}")
                else:
                    print("❌ Failed to upload image")
            else:
                print("❌ Image file not found!")
        
        elif choice == '3':
            print("\n📊 Attendance Report")
            date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
            if not date:
                date = None
            
            report = fr.get_attendance_report(date)
            if report:
                print(f"\nAttendance for {date or 'today'}:")
                for person, time in report.items():
                    print(f"  {person}: {time}")
            else:
                print("No attendance records found")
        
        elif choice == '4':
            print("\n👥 Reference Faces:")
            faces = fr.list_reference_faces()
            if faces:
                for face in faces:
                    print(f"  - {face}")
            else:
                print("No reference faces found")
        
        elif choice == '5':
            print("\n🗑️ Delete Reference Face")
            faces = fr.list_reference_faces()
            if faces:
                print("Available faces:")
                for i, face in enumerate(faces):
                    print(f"  {i+1}. {face}")
                
                try:
                    idx = int(input("Enter number to delete: ")) - 1
                    if 0 <= idx < len(faces):
                        person_name = faces[idx]
                        success, message = fr.delete_reference_face(person_name)
                        print(f"Result: {message}")
                    else:
                        print("❌ Invalid selection")
                except ValueError:
                    print("❌ Please enter a valid number")
            else:
                print("No reference faces to delete")
        
        elif choice == '6':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
