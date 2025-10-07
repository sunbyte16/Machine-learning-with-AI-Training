import cv2
import os

def test_system():
    """Test if the system is working"""
    print("🔍 Testing Face Recognition System...")
    
    # Test OpenCV
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if face_cascade.empty():
            print("❌ Error: Could not load face cascade")
            return False
        print("✅ OpenCV face detection working")
    except Exception as e:
        print(f"❌ OpenCV error: {e}")
        return False
    
    # Test camera
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not open camera")
            return False
        print("✅ Camera working")
        cap.release()
    except Exception as e:
        print(f"❌ Camera error: {e}")
        return False
    
    # Check directories
    if not os.path.exists('ImagesAttendance'):
        os.makedirs('ImagesAttendance')
        print("✅ Created ImagesAttendance folder")
    else:
        print("✅ ImagesAttendance folder exists")
    
    if not os.path.exists('ImagesBasic'):
        os.makedirs('ImagesBasic')
        print("✅ Created ImagesBasic folder")
    else:
        print("✅ ImagesBasic folder exists")
    
    return True

def show_instructions():
    """Show setup instructions"""
    print("\n" + "="*50)
    print("🚀 FACE RECOGNITION PROJECT - READY!")
    print("="*50)
    
    print("\n📁 Project Structure:")
    print("├── simple_basics.py      (Basic face detection demo)")
    print("├── simple_face_recognition.py (Attendance system)")
    print("├── ImagesAttendance/     (Add reference images here)")
    print("├── ImagesBasic/          (Add test images here)")
    print("└── Attendance.csv        (Attendance log)")
    
    print("\n🎯 Quick Start:")
    print("1. Add photos to ImagesAttendance/ folder (format: PersonName.jpg)")
    print("2. Run: python simple_face_recognition.py")
    print("3. Or test basic detection: python simple_basics.py")
    
    print("\n📸 Image Requirements:")
    print("- Clear face photos")
    print("- Good lighting")
    print("- Front-facing")
    print("- JPG/PNG format")
    
    print("\n⚡ Commands:")
    print("- python simple_basics.py     (Basic demo)")
    print("- python simple_face_recognition.py (Attendance system)")
    print("- Press 'q' to quit any program")

def main():
    print("🎭 Face Recognition Project Setup")
    print("="*40)
    
    if test_system():
        show_instructions()
        
        # Check for existing images
        attendance_images = [f for f in os.listdir('ImagesAttendance') if f.endswith(('.jpg', '.jpeg', '.png'))]
        basic_images = [f for f in os.listdir('ImagesBasic') if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if attendance_images:
            print(f"\n✅ Found {len(attendance_images)} reference images in ImagesAttendance/")
        else:
            print("\n⚠️  No reference images found in ImagesAttendance/")
            print("   Add photos to enable attendance system")
        
        if basic_images:
            print(f"✅ Found {len(basic_images)} test images in ImagesBasic/")
        else:
            print("⚠️  No test images found in ImagesBasic/")
            print("   Add photos to enable basic demo")
        
        print("\n🎉 System is ready to use!")
        
    else:
        print("\n❌ System test failed. Please check your setup.")

if __name__ == "__main__":
    main()
