from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)


tumor_model = YOLO("tumor_model.pt")   
type_model = YOLO("type_model.pt")     

@app.route('/')
def home():
    return "✅ Yolo Health Flask backend running with YOLO and chatbot!"


@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    tumor_results = tumor_model(img)
    type_results = type_model(img)

   
    tumor_detections = tumor_results[0].boxes.data.tolist()
    type_detections = type_results[0].boxes.data.tolist()

    tumor_msg = "Tumor detected" if len(tumor_detections) > 0 else "No tumor found"
    type_msg = "Type detected" if len(type_detections) > 0 else "No type found"

    return jsonify({
        "tumor_result": tumor_msg,
        "tumor_detections": len(tumor_detections),
        "type_result": type_msg,
        "type_detections": len(type_detections)
    })


@app.route('/chat', methods=['POST'])
def chatbot():
    user_message = request.json.get("message", "").lower()

    
    if "tumor" in user_message:
        reply = "Tumors are abnormal growths. Would you like to upload an MRI for analysis?"
    elif "hello" in user_message or "hi" in user_message:
        reply = "Hello! 👋 I’m Yulo Health AI. How can I assist you today?"
    elif "yolo" in user_message:
        reply = "YOLO is our model that detects tumors in MRI scans using deep learning."
    else:
        reply = "I’m not sure I understand that. Could you please rephrase?"

    return jsonify({"reply": reply})


