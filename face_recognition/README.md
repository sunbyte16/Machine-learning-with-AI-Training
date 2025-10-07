# 🎭 Advanced Face Recognition System

A comprehensive face recognition system with image upload, recognition, and attendance tracking capabilities.

## ✨ Features

- 📤 **Image Upload**: Upload reference images for face recognition
- 🔍 **Face Recognition**: Recognize faces in uploaded images
- 🎥 **Real-time Webcam**: Live face recognition with webcam
- 📊 **Attendance Tracking**: Automatic attendance marking
- 📈 **Attendance Reports**: View attendance by date
- 👥 **Reference Management**: Add/delete reference faces
- 💾 **Data Persistence**: JSON-based attendance storage

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install opencv-python numpy
```

### 2. Run the System
```bash
python face_recognition_system.py
```

### 3. Webcam Recognition
```bash
python webcam_recognition.py
```

## 📁 Project Structure

```
face_recognition/
├── face_recognition_system.py    # Main system with menu interface
├── webcam_recognition.py         # Real-time webcam recognition
├── face_detection_demo.py        # Basic face detection demo
├── quick_start.py               # System test and setup
├── requirements_simple.txt      # Dependencies
├── reference_faces/             # Reference images (auto-created)
├── uploads/                     # Uploaded images (auto-created)
├── detection_results/           # Detection results (auto-created)
├── attendance.json              # Attendance data (auto-created)
└── README.md                    # This file
```

## 🎯 How to Use

### Main System (`face_recognition_system.py`)

1. **Upload Reference Image**
   - Choose option 1
   - Enter image path (e.g., `C:\path\to\photo.jpg`)
   - Enter person name

2. **Recognize Faces in Image**
   - Choose option 2
   - Enter image path to analyze
   - View recognition results and attendance marking

3. **View Attendance Report**
   - Choose option 3
   - Enter date or press Enter for today

4. **Manage Reference Faces**
   - Choose option 4 to list faces
   - Choose option 5 to delete faces

### Webcam Recognition (`webcam_recognition.py`)

- Automatically loads reference faces
- Real-time face detection and recognition
- Automatic attendance marking
- Press 'q' to quit, 's' to save frame

## 📸 Image Requirements

### Reference Images
- Clear, front-facing photos
- Single face per image
- Good lighting
- JPG/PNG format
- File naming: `PersonName.jpg`

### Recognition Images
- Can contain multiple faces
- Any image format supported by OpenCV
- Will be automatically processed

## 🔧 Technical Details

- **Face Detection**: OpenCV Haar Cascade
- **Face Recognition**: Template matching with similarity threshold
- **Storage**: JSON format for attendance data
- **Performance**: Optimized for real-time processing

## 📊 Attendance System

- Automatic attendance marking for recognized faces
- Prevents duplicate entries per day
- JSON-based storage with date tracking
- View reports by specific dates

## 🎮 Controls

### Main System
- Menu-driven interface
- File path input for images
- Interactive options

### Webcam System
- `q` - Quit application
- `s` - Save current frame
- Real-time face detection display

## 🛠️ Troubleshooting

### Common Issues

1. **Camera not working**
   - Check camera permissions
   - Ensure no other app is using camera

2. **No faces detected**
   - Check image quality
   - Ensure good lighting
   - Verify single face in reference images

3. **Low recognition accuracy**
   - Use clearer reference images
   - Ensure similar lighting conditions
   - Check face orientation

### Performance Tips

- Use smaller images for faster processing
- Good lighting improves accuracy
- Front-facing photos work best
- Regular reference image updates

## 📈 Future Enhancements

- [ ] Deep learning-based recognition
- [ ] Multiple face encodings per person
- [ ] Database integration
- [ ] Web interface
- [ ] Mobile app support
- [ ] Advanced analytics

## 🤝 Contributing

Feel free to improve the system by:
- Adding new features
- Optimizing performance
- Improving accuracy
- Enhancing UI/UX

## 📄 License

This project is open source and available under the MIT License.
