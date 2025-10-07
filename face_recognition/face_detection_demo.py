import cv2
import numpy as np
import os

def detect_faces_in_image(image_path):
    """Detect faces in a single image"""
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image {image_path}")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    print(f"Found {len(faces)} face(s) in {os.path.basename(image_path)}")
    
    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(image, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    
    # Save result
    output_path = f"output_{os.path.basename(image_path)}"
    cv2.imwrite(output_path, image)
    print(f"Result saved as: {output_path}")
    
    return len(faces)

def simple_webcam_detection():
    """Simple webcam face detection without display"""
    print("Starting webcam face detection...")
    print("Press Ctrl+C to stop")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every 10th frame to reduce CPU usage
            if frame_count % 10 == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    print(f"Frame {frame_count}: Detected {len(faces)} face(s)")
                
                # Save frame with faces detected
                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    output_path = f"webcam_detection_{frame_count}.jpg"
                    cv2.imwrite(output_path, frame)
                    print(f"Saved detection: {output_path}")
    
    except KeyboardInterrupt:
        print("\nStopping webcam detection...")
    
    cap.release()
    print("Webcam detection stopped")

def main():
    print("🎭 Face Detection Demo")
    print("=" * 30)
    
    # Check for images in ImagesBasic folder
    basic_folder = "ImagesBasic"
    if os.path.exists(basic_folder):
        images = [f for f in os.listdir(basic_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if images:
            print(f"Found {len(images)} image(s) in {basic_folder}/")
            for img in images:
                img_path = os.path.join(basic_folder, img)
                detect_faces_in_image(img_path)
        else:
            print(f"No images found in {basic_folder}/")
    else:
        print(f"Folder {basic_folder}/ not found")
    
    print("\nOptions:")
    print("1. Add images to ImagesBasic/ folder and run again")
    print("2. Run webcam detection (Ctrl+C to stop)")
    
    choice = input("\nRun webcam detection? (y/n): ").lower()
    if choice == 'y':
        simple_webcam_detection()

if __name__ == "__main__":
    main()
