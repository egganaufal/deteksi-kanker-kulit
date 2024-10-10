from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from ultralytics import YOLO
import os
import cv2
import base64
import numpy as np
import logging
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
camera = cv2.VideoCapture(0)  # Inisialisasi di luar fungsi untuk menghindari multiple initialization
camera_running = True  # Flag untuk mengontrol loop camera

# Memuat model YOLOv8
model = YOLO('../models/terdebest.pt')  # Pastikan Anda memiliki model YOLOv8 yang telah dilatih

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            file_type = file.content_type.split('/')[0]
            if file_type == 'image':
                # Melakukan deteksi pada gambar
                results = model(filepath)
                detections = []
                for result in results:
                    if hasattr(result, 'boxes'):
                        boxes = result.boxes.numpy()  # Mengonversi boxes ke array numpy
                        for i, box in enumerate(boxes.xyxy):
                            class_id = int(boxes.cls[i])  # Mendapatkan label kelas
                            class_name = result.names[class_id] if class_id in result.names else "Unknown"
                            bbox = {
                                "x1": float(box[0]),  # Mengonversi numpy.float32 ke float
                                "y1": float(box[1]),
                                "x2": float(box[2]),
                                "y2": float(box[3]),
                                "confidence": float(boxes.conf[i]),  # Mengonversi numpy.float32 ke float
                                "class_id": class_id,
                                "class_name": class_name
                        }
                        detections.append(bbox)

                if detections:
                    last_prediction['prediction'] = detections[0]['class_name']
                    classDescriptions = {
                        'nv': 'Melanocytic Nevi',
                        'mel': 'Melanoma',
                        'bcc': 'Basal Cell Carcinoma',
                        'akiec': 'Actinic Keratoses',
                        'bkl': 'Benign Keratosis-like Lesions',
                        'df': 'Dermatofibroma',
                        'vasc': 'Vascular Lesions'
                    } 
                    last_prediction['prediction'] = classDescriptions[last_prediction['prediction']]
                else:
                    last_prediction['prediction'] = 'Unknown'
                result_image = results[0].plot()  # Menggunakan metode .plot() untuk mendapatkan gambar dengan deteksi

                # Menyimpan gambar hasil dengan nama file yang sama
                result_image_path = os.path.join(app.config['RESULT_FOLDER'], filename)
                cv2.imwrite(result_image_path, result_image)

                return render_template('index.html', result_image_path=f'results/{filename}', is_image=True)

            elif file_type == 'video':
                # Melakukan deteksi pada video
                return process_video(filepath, filename)
    
    return render_template('index.html')

def process_video(filepath, filename):
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        return "Error: Could not open video file."

    # Mengubah codec ke 'avc1' (H.264)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out_path = os.path.join(app.config['RESULT_FOLDER'], filename)
    out = cv2.VideoWriter(out_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = []
        for result in results:
            if hasattr(result, 'boxes'):
                boxes = result.boxes.numpy()  # Mengonversi boxes ke array numpy
                for i, box in enumerate(boxes.xyxy):
                    class_id = int(boxes.cls[i])  # Mendapatkan label kelas
                    class_name = result.names[class_id] if class_id in result.names else "Unknown"
                    bbox = {
                            "x1": float(box[0]),  # Mengonversi numpy.float32 ke float
                            "y1": float(box[1]),
                            "x2": float(box[2]),
                            "y2": float(box[3]),
                            "confidence": float(boxes.conf[i]),  # Mengonversi numpy.float32 ke float
                            "class_id": class_id,
                            "class_name": class_name
                        }
                    detections.append(bbox)

                if detections:
                    last_prediction['prediction'] = detections[0]['class_name']
                    classDescriptions = {
                        'nv': 'Melanocytic Nevi',
                        'mel': 'Melanoma',
                        'bcc': 'Basal Cell Carcinoma',
                        'akiec': 'Actinic Keratoses',
                        'bkl': 'Benign Keratosis-like Lesions',
                        'df': 'Dermatofibroma',
                        'vasc': 'Vascular Lesions'
                    } 
                    last_prediction['prediction'] = classDescriptions[last_prediction['prediction']]
                else:
                    last_prediction['prediction'] = 'Unknown'
        result_frame = results[0].plot()  # Menggunakan metode .plot() untuk mendapatkan frame dengan deteksi
        out.write(result_frame)

    cap.release()
    out.release()

    return render_template('index.html', result_video_path=f'results/{filename}', is_image=False)

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

last_prediction = {
    'prediction': None,
}

@app.route('/get_prediction_label', methods=['GET'])
def get_prediction_label():
    try:
        app.logger.debug(f"Last prediction: {last_prediction}")  # Menambahkan logging untuk memeriksa prediksi terakhir
        return jsonify(last_prediction)
    except Exception as e:
        app.logger.error(f"Error in /get_prediction_label: {str(e)}")
        return jsonify({'error': str(e), 'prediction': 'Unknown'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']
    image_data = base64.b64decode(data.split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Perform prediction using your model
    results = model(img)

    # Manually construct JSON from results
    detections = []
    for result in results:
        if hasattr(result, 'boxes'):
            boxes = result.boxes.numpy()  # Convert boxes to numpy array
            for i, box in enumerate(boxes.xyxy):
                class_id = int(boxes.cls[i])  # Get class label
                class_name = result.names[class_id] if class_id in result.names else "Unknown"
                bbox = {
                    "x1": float(box[0]),  # Convert numpy.float32 to float
                    "y1": float(box[1]),
                    "x2": float(box[2]),
                    "y2": float(box[3]),
                    "confidence": float(boxes.conf[i]),  # Convert numpy.float32 to float
                    "class_id": class_id,
                    "class_name": class_name
                }
                detections.append(bbox)

    # Log the detections
    print("Detections:", detections)

    # Update last prediction
    if detections:
        last_prediction['prediction'] = detections[0]['class_name']
    else:
        last_prediction['prediction'] = 'Unknown'

    # Log the updated last prediction
    app.logger.debug(f"Updated last prediction: {last_prediction}")

    return jsonify({"detections": detections})

def generate_frames():  
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model(frame)
            # Iterate over each result in the list of results
            for result in results:
                if result.boxes:  # Check if there are any detections in this result
                    frame = result.plot()  # Use plot() to draw detections on the frame
                    break  # Assuming you only need to process the first set of detections

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Route ini mengembalikan response streaming
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
    app.run(debug=False, threaded=True)