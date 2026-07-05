import streamlit as st
import cv2
import numpy as np
from PIL import Image
import torch
from ultralytics import YOLO
import io

# Page configuration
st.set_page_config(
    page_title="Skin Cancer Detection",
    page_icon="🔬",
    layout="wide"
)

# Title and description
st.title("🔬 Skin Cancer Detection System")
st.markdown("""
Upload an image of a skin lesion to detect potential skin cancer regions using YOLO object detection.
This tool uses deep learning to identify and classify skin abnormalities.
""")

# Sidebar for model configuration
st.sidebar.header("⚙️ Configuration")
confidence_threshold = st.sidebar.slider(
    "Confidence Threshold", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.25,
    step=0.05
)

# Class names for skin cancer types (common categories)
CLASS_NAMES = {
    0: "Melanoma",
    1: "Basal Cell Carcinoma", 
    2: "Squamous Cell Carcinoma",
    3: "Benign Keratosis",
    4: "Nevus",
    5: "Actinic Keratosis",
    6: "Dermatofibroma"
}

@st.cache_resource
def load_model():
    """Load YOLO model - replace with your trained model path"""
    try:
        # Replace 'yolov8n.pt' with your trained skin cancer model
        model = YOLO('yolov8n.pt')  # You'll need to use your trained weights
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.info("Using placeholder model. Please provide your trained YOLO weights.")
        return None

def process_image(image, model, conf_threshold):
    """Process image and run inference"""
    if model is None:
        return None, None
    
    # Convert PIL to numpy array
    img_array = np.array(image)
    
    # Run inference
    results = model.predict(
        source=img_array,
        conf=conf_threshold,
        save=False,
        verbose=False
    )
    
    # Get annotated image
    annotated_img = results[0].plot()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    
    return results[0], annotated_img

def display_results(results):
    """Display detection results in a formatted way"""
    if results.boxes is None or len(results.boxes) == 0:
        st.warning("No skin lesions detected in the image.")
        return
    
    st.success(f"✅ Detected {len(results.boxes)} potential lesion(s)")
    
    # Create columns for each detection
    for idx, box in enumerate(results.boxes):
        with st.expander(f"Detection #{idx + 1}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            # Get class and confidence
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            
            # Display info
            with col1:
                st.metric("Class", CLASS_NAMES.get(cls, f"Class {cls}"))
            with col2:
                st.metric("Confidence", f"{conf:.2%}")
            with col3:
                # Bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                st.metric("Size", f"{int(x2-x1)}x{int(y2-y1)}px")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a skin lesion image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the skin lesion"
    )
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Add analyze button
        analyze_button = st.button("🔍 Analyze Image", type="primary", use_container_width=True)
    else:
        analyze_button = False
        st.info("👆 Please upload an image to begin analysis")

with col2:
    st.subheader("📊 Detection Results")
    
    if uploaded_file is not None and analyze_button:
        with st.spinner("Analyzing image..."):
            # Load model
            model = load_model()
            
            if model is not None:
                # Process image
                results, annotated_img = process_image(image, model, confidence_threshold)
                
                if annotated_img is not None:
                    # Display annotated image
                    st.image(annotated_img, caption="Detected Lesions", use_container_width=True)
                    
                    # Display detection details
                    st.markdown("---")
                    display_results(results)
            else:
                st.error("Model not loaded. Please check the model path.")
    else:
        st.info("Analysis results will appear here")

# Footer with disclaimers
st.markdown("---")
st.markdown("""
### ⚠️ Medical Disclaimer
This tool is for educational and research purposes only. It should NOT be used as a substitute for 
professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare 
provider for any medical concerns.

### 📋 How to Use
1. Upload a clear image of a skin lesion
2. Adjust the confidence threshold in the sidebar if needed
3. Click "Analyze Image" to run detection
4. Review the results and detected regions

### 🔧 Setup Instructions
To use this app with your trained model:
1. Train a YOLO model on skin cancer dataset
2. Replace `'yolov8n.pt'` with your model weights path
3. Update `CLASS_NAMES` dictionary with your classes
4. Install requirements: `pip install streamlit ultralytics opencv-python pillow`
5. Run: `streamlit run app.py`
""")
