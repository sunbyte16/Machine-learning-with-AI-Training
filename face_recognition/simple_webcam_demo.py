import cv2
import numpy as np
import os

def simple_webcam_demo():
    """Simple webcam face detection demo"""
    print("🎥 Simple Webcam Face Detection Demo")
    print("=" * 40)
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        print("Please check:")
        print("1. Camera is connected")
        print("2. No other app is using camera")
        print("3. Camera permissions are enabled")
        return
    
    print("✅ Camera opened successfully!")
    print("Press 'q' to quit, 's' to save frame")
    
    # Load face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        print("❌ Error: Could not load face detection model")
        return
    
    print("✅ Face detection model loaded!")
    
    frame_count = 0
    faces_detected = 0
    
    try:
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            frame_count += 1
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Face Detected', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                faces_detected += 1
            
            # Add info text
            cv2.putText(frame, f"Frames: {frame_count} | Faces: {len(faces)}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit, 's' to save", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('Webcam Face Detection', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("👋 Quitting...")
                break
            elif key == ord('s'):
                # Save current frame
                filename = f"webcam_capture_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Saved: {filename}")
    
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n📊 Summary:")
        print(f"Total frames processed: {frame_count}")
        print(f"Total faces detected: {faces_detected}")
        print("✅ Webcam demo completed!")

def test_camera_only():
    """Test if camera works without face detection"""
    print("🔍 Testing Camera Only...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Camera test failed!")
        return False
    
    print("✅ Camera test successful!")
    
    # Try to read one frame
    ret, frame = cap.read()
    if ret:
        print(f"✅ Frame captured: {frame.shape}")
        cap.release()
        return True
    else:
        print("❌ Could not capture frame")
        cap.release()
        return False

def main():
    print("🎭 Webcam Testing System")
    print("=" * 30)
    
    # Test camera first
    if not test_camera_only():
        print("\n❌ Camera is not working properly.")
        print("Please check your camera setup and try again.")
        return
    
    print("\n🎥 Starting webcam face detection demo...")
    simple_webcam_demo()

if __name__ == "__main__":
    main()
