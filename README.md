# 🤖 Hand Gesture Recognition with MediaPipe

A real-time hand gesture recognition system that detects hand gestures from your webcam and overlays corresponding images on the screen. Perfect for interactive applications, virtual controls, and gesture-based interfaces.

## ✨ Features

### 🎯 Real-time Hand Tracking
- **MediaPipe Integration**: Leverages Google's MediaPipe framework for robust hand landmark detection
- **Single Hand Detection**: Optimized for tracking one hand at a time with high accuracy
- **60+ FPS Performance**: Efficient processing for smooth real-time experience

### 👆 Gesture Recognition
- **Multiple Gesture Support**: Detects four distinct hand gestures:
  - ✊ **Closed Fist** (`close.png`)
  - 🖐️ **Open Hand** (`open.png`)
  - ☝️ **One Finger** (`one.png`)
  - ✌️ **Two Fingers** (`two.png`)
- **Intelligent Finger Counting**: Sophisticated algorithm that analyzes finger positions to determine gestures

### 🖼️ Smart Image Overlay
- **Transparent PNG Support**: Seamlessly overlays images with alpha transparency
- **Dynamic Positioning**: Images follow your wrist movement in real-time
- **Auto-resizing**: All overlay images are automatically resized to optimal dimensions

### 🛡️ Robust Error Handling
- **Comprehensive Image Validation**: Checks for missing files and proper transparency channels
- **Graceful Error Recovery**: Provides clear error messages and prevents crashes
- **Bounds Checking**: Ensures overlays never go outside camera view

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Webcam
- Required gesture images (see below)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hand-gesture-tracker.git
   cd hand-gesture-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install opencv-python mediapipe numpy
   ```

3. **Prepare gesture images**
   - Download or create these transparent PNG files in the project directory:
     - `close.png` - ✊ Closed fist gesture
     - `open.png` - 🖐️ Open hand gesture  
     - `one.png` - ☝️ One finger pointing
     - `two.png` - ✌️ Two fingers (peace sign)
   - **Important**: Images must have **4 channels (RGBA)** with transparency

4. **Run the application**
   ```bash
   python hand_tracker.py
   ```

## 🎮 How to Use

1. **Start the program** - Camera feed will open automatically
2. **Show your hand** - Position your hand in front of the camera
3. **Make gestures**:
   - ✊ **Closed fist** → Displays `close.png`
   - 🖐️ **Open hand** → Displays `open.png`
   - ☝️ **One finger** → Displays `one.png`
   - ✌️ **Two fingers** → Displays `two.png`
4. **Move your hand** - The overlay image follows your wrist movement
5. **Press 'Q'** - To exit the application

## 🛠️ Configuration

Easy customization through the `CONFIGURATION` section:

```python
# Folder containing gesture images (current directory by default)
IMAGE_FOLDER = "."

# Size of overlay images in pixels (width, height)
OVERLAY_SIZE = (150, 150)

# MediaPipe detection sensitivity (0.0 to 1.0)
min_detection_confidence=0.7
min_tracking_confidence=0.5
```

## 📁 Project Structure

```
hand-gesture-tracker/
├── hand_tracker.py          # Main application file
├── close.png               # Closed fist gesture image
├── open.png                # Open hand gesture image  
├── one.png                 # One finger gesture image
├── two.png                 # Two fingers gesture image
└── README.md              # This file
```

## 🔧 Technical Details

### Core Components

- **`HandTracker` Class**: Main controller class
- **`load_images()`**: Robust image loader with validation
- **`overlay_image()`**: Advanced alpha blending for transparent overlays
- **`count_fingers()`**: Gesture recognition algorithm
- **`run()`**: Main video processing loop

### Algorithm Overview

1. **Hand Landmark Detection**: MediaPipe identifies 21 hand keypoints
2. **Finger State Analysis**: Compares fingertip positions with knuckle positions
3. **Gesture Classification**: Maps finger counts to specific gestures
4. **Visual Feedback**: Overlays corresponding images anchored to wrist position

## 🐛 Troubleshooting

### Common Issues

**❌ "Could not load [image].png"**
- Solution: Ensure all four PNG files exist in the project directory

**❌ "WARNING: [image] has X channels (expected 4)"**  
- Solution: Convert images to RGBA format with transparency channel

**❌ "Error reading frame from webcam"**
- Solution: Check camera permissions and ensure no other app is using the camera

**❌ Poor gesture detection**
- Solution: Improve lighting, ensure hand is clearly visible, adjust confidence thresholds

## 🎯 Potential Enhancements

- [ ] Multi-hand support
- [ ] Custom gesture training
- [ ] Gesture-based controls for applications
- [ ] Mobile device compatibility
- [ ] Additional gesture types
- [ ] Recording and playback functionality
---

**⭐ Star this repo if you found it helpful!**

**🐛 Found an issue?** Please open an issue or submit a pull request.
