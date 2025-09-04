<div align="center">

# 🧠 Human Activity Detection

Action recognition from videos using 👣 Detectron2 keypoints + 🔁 LSTM — wrapped in a clean Flask web UI.

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)

[![Made with PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![Lightning](https://img.shields.io/badge/Lightning-%23B71CFF.svg?style=for-the-badge&logo=Lightning&logoColor=white)](https://lightning.ai/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

</div>

Real-time human action classification web app. It uses Detectron2 Keypoint R-CNN to extract body keypoints frame-by-frame and an LSTM classifier (PyTorch Lightning) to recognize actions such as JUMPING, JUMPING_JACKS, BOXING, WAVING_2HANDS, WAVING_1HAND, and CLAPPING_HANDS.

### ✨ Features
- **Web UI (Flask)**: upload an `.mp4` or try the bundled `sample_video.mp4`.
- **Pose estimation**: Detectron2 COCO Keypoints model (R-50-FPN 3x).
- **Sequence classification**: LSTM trained on sliding windows of 32 frames.
- **Live progress**: SSE updates progress and renders the annotated result video.

### 📁 Project Structure
```
app.py                         # Flask server and routes
templates/index.html           # Web UI for upload/progress/result
src/utils.py                   # Drawing and keypoint utilities
src/video_analyzer.py          # Inference loop, SSE progress, result writer
src/lstm.py                    # LSTM model and data module (training)
src/train.py                   # Training entrypoint (CLI)
models/saved_model.ckpt        # Trained LSTM checkpoint (required for inference)
images/val_acc.png, val_loss.png  # Training curves (optional)
sample_video.mp4               # Demo input video
```

### 📦 Requirements
- Python 3.8–3.10 recommended
- PyTorch with CUDA (optional but recommended for speed)
- OpenCV, Flask, PyTorch Lightning
- Detectron2 (matching your PyTorch/CUDA versions)

Install Python deps:
```bash
pip install -r requirements.txt
```

Install Detectron2 (choose a command that matches your CUDA/PyTorch):
```bash
# Example for CPU-only (slow):
pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Or visit Detectron2 install docs and pick the correct wheel:
# https://detectron2.readthedocs.io/en/latest/tutorials/install.html
```

Notes:
- The app auto-downloads Detectron2 weights from the model zoo at runtime.
- Ensure `models/saved_model.ckpt` exists. The app loads it via `ActionClassificationLSTM.load_from_checkpoint(...)`.

### 🚀 Running the Web App
```bash
python app.py
```
Then open `http://127.0.0.1:5000/`.

Usage:
- Upload an `.mp4` video, or click the sample option.
- The server will:
  - run Detectron2 keypoint inference per frame,
  - maintain a sliding window of 32 frames,
  - classify the action with the LSTM,
  - overlay the predicted action on frames,
  - write `res_<filename>.mp4` in the project root,
  - stream progress via SSE and display the result.

Result files:
- Download the annotated video from the link shown after processing, or find it as `res_<your_video>.mp4` in the project folder.

### 🏋️ Training the LSTM
Expected dataset format (see `src/lstm.py`):
- `X_train.txt`, `X_test.txt`: rows of comma-separated keypoint coordinates in OpenPose order; neck is filtered out and remapped to Detectron2 order internally.
- `Y_train.txt`, `Y_test.txt`: class labels (1-based integers) per frame.

Slice into windows of 32 frames is done in code. To train:
```bash
python -m src.train -d <path/to/data_dir/>
```
Arguments (defaults in `src/train.py`):
- `--batch_size` (default 512)
- `--epochs` (default 400)
- `--learning_rate` (default 1e-4)

Trained checkpoints are saved via PyTorch Lightning `ModelCheckpoint`. Rename or copy the best checkpoint to `models/saved_model.ckpt` for the web app.

### 🧩 Troubleshooting
- Detectron2 install issues: verify PyTorch and CUDA versions match the wheel. See Detectron2 install guide.
- CUDA not available: the app will still run on CPU but much slower.
- Missing checkpoint: ensure `models/saved_model.ckpt` exists, or update the path in `app.py`.
- OpenCV codec errors when writing files: install `opencv-python` (already in requirements) and ensure you have write permissions in the project directory.
- Large videos: increase performance by setting a higher `SKIP_FRAME_COUNT` in `src/video_analyzer.py` (trades accuracy for speed).

### 🙌 Acknowledgements
- Detectron2 by FAIR
- PyTorch and PyTorch Lightning

---

### 📬 Connect
- 🐙 **GitHub**: [@sunbyte16](https://github.com/sunbyte16)
- 💼 **LinkedIn**: [Sunil Kumar](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)

<p align="center">
  Created by <strong>❤️Sunil Sharma❤️</strong>
</p>



