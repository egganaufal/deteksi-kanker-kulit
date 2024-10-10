# Skin Cancer Detection System

This project is a web application for detecting skin cancer using object detection techniques. It leverages the YOLOv8 model to identify various types of skin cancer from uploaded images or videos, as well as through live webcam feeds.

## Features

- **Image and Video Upload**: Users can upload images or videos for skin cancer detection.
- **Live Webcam Detection**: Real-time detection using a webcam.
- **Detection of Multiple Skin Cancer Types**: The application can detect seven types of skin cancer:
  - Melanocytic Nevi (nv)
  - Melanoma (mel)
  - Benign Keratosis-like Lesions (bkl)
  - Basal Cell Carcinoma (bcc)
  - Actinic Keratoses (akiec)
  - Vascular Lesions (vasc)
  - Dermatofibroma (df)
- **User-Friendly Interface**: Easy-to-use interface with clear instructions and feedback.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/egganaufal/skin-cancer-detection.git
   cd skin-cancer-detection
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Download the YOLOv8 model**:
   - Ensure you have the trained YOLOv8 model file (`terdebest.pt`) in the `models` directory.

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Access the application**:
   - Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- **Home Page**: Upload an image or video file for detection or use the webcam for live detection.
- **About Page**: Learn more about the application and the types of skin cancer it can detect.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [YOLOv8](https://github.com/ultralytics/yolov8) for the object detection model.
- [SweetAlert2](https://sweetalert2.github.io/) for beautiful alerts.
