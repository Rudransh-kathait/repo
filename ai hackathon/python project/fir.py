import os
import csv
import cv2
import torch
import streamlit as st
import tempfile
from ultralytics import YOLO
import google.generativeai as genai
from PIL import Image
import numpy as np


# ============================================================
# 🧠 AIHealthSystem Class (Backend)
# ============================================================
class AIHealthSystem:
    def _init_(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pixel_spacing = [0.4688, 0.4688]  # mm/pixel
        self.API_KEY = "AIzaSyDPBmSKT9uOpWmRUOQcWUhEbGAcay8tVAk"

        # BMT data files
        self.DONOR_CSV = "donors.csv"
        self.PATIENT_CSV = "patients.csv"
        self.DONOR_FIELDS = ["Name", "Age", "Phone", "Blood Group", "HLA"]
        self.PATIENT_FIELDS = ["Name", "Age", "Disease", "HLA"]
        self.initialize_csv_files()

    # ============================== BMT FUNCTIONS ==============================
    def initialize_csv_files(self):
        for path, fields in [
            (self.DONOR_CSV, self.DONOR_FIELDS),
            (self.PATIENT_CSV, self.PATIENT_FIELDS),
        ]:
            if not os.path.exists(path):
                with open(path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)

    def load_data(self):
        donors, patients = [], []
        if os.path.exists(self.DONOR_CSV):
            with open(self.DONOR_CSV, "r") as f:
                donors = list(csv.DictReader(f))
        if os.path.exists(self.PATIENT_CSV):
            with open(self.PATIENT_CSV, "r") as f:
                patients = list(csv.DictReader(f))
        return donors, patients

    def add_donor(self, name, age, phone, blood_group, hla):
        donors, _ = self.load_data()
        donors.append(
            {"Name": name, "Age": str(age), "Phone": phone, "Blood Group": blood_group, "HLA": hla}
        )
        with open(self.DONOR_CSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.DONOR_FIELDS)
            writer.writeheader()
            writer.writerows(donors)
        return True, "✅ Donor added successfully."

    def add_patient(self, name, age, disease, hla):
        _, patients = self.load_data()
        patients.append({"Name": name, "Age": str(age), "Disease": disease, "HLA": hla})
        with open(self.PATIENT_CSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.PATIENT_FIELDS)
            writer.writeheader()
            writer.writerows(patients)
        return True, "✅ Patient added successfully."

    def find_donor_match(self, patient_hla):
        donors, _ = self.load_data()
        matches = [d for d in donors if d["HLA"].lower() == patient_hla.lower()]
        return matches if matches else None

    # ============================== YOLO DETECTION ==============================
    def brain_tumor_detection_single(self, image_path):
        """Run YOLOv8 detection on one MRI image (inline)."""
        model = YOLO(r"brain_mri_detection/best.pt")
        results = model.predict(
            source=image_path, conf=0.5, device=self.device, verbose=False, show=False
        )

        annotated_images = []
        for result in results:
            img = result.orig_img.copy()
            boxes = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else []
            label = "No tumor detected"

            for box in boxes:
                x_min, y_min, x_max, y_max = map(int, box[:4])
                width_px = x_max - x_min
                height_px = y_max - y_min
                real_width_mm = width_px * self.pixel_spacing[0]
                real_height_mm = height_px * self.pixel_spacing[1]
                label = f"Tumor: {real_width_mm:.1f}mm x {real_height_mm:.1f}mm"
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            cv2.rectangle(img, (10, 10), (430, 55), (0, 0, 0), -1)
            cv2.putText(img, label, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            annotated_images.append(img)
        return annotated_images
    def brain_tumor_detection_from_val_folder(self):
        """Detects tumors on all MRI images in val folder using YOLOv8."""
        model = YOLO(r"brain_mri_detection/best.pt")
        results = model.predict(
            source=r"brain_mri_detection/val",
            show=False,
            save=False,
            conf=0.5,
            device=self.device,
            stream=False,
            verbose=False
        )

        print("\n🧠 Running tumor detection on validation folder...")
        print("Press ESC in the window to close.\n")

        # Clear any previous OpenCV windows
        cv2.destroyAllWindows()
        cv2.waitKey(1)

        for i, result in enumerate(results, start=1):
            # Always use original image — not result.plot() — to avoid extra window
            img = result.orig_img.copy()
            boxes = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else []

            # Draw boxes + tumor size info
            label = "No tumor detected"
            for box in boxes:
                x_min, y_min, x_max, y_max = map(int, box[:4])
                width_px = x_max - x_min
                height_px = y_max - y_min
                real_width_mm = width_px * self.pixel_spacing[0]
                real_height_mm = height_px * self.pixel_spacing[1]
                label = f"Tumor: {real_width_mm:.1f}mm x {real_height_mm:.1f}mm"
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Add top-left label box
            cv2.rectangle(img, (10, 10), (430, 55), (0, 0, 0), -1)
            cv2.putText(img, label, (20, 45), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2, cv2.LINE_AA)

            # Single clean window (no duplicates)
            win = "🧠 Brain Tumor Detection (Press ESC to Close)"
            cv2.namedWindow(win, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(win, cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow(win, img)

            # Hold each image for 0.3 seconds (300 ms)
            key = cv2.waitKey(300) & 0xFF
            if key == 27:  # ESC to stop early
                break


        cv2.destroyAllWindows()
        cv2.waitKey(1)
        print("\n✅ Detection completed. All windows closed.\n")


# ============================================================
# 💻 STREAMLIT UI
# ============================================================
app = AIHealthSystem()
st.set_page_config(page_title="AI Health System 🏥", layout="wide")
st.title("🏥 AI Health System - Brain Tumor, Chatbot & BMT")

tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "🧠 Brain Tumor Detection", "🧬 Bone Marrow Transplant"])
# ============================== CHATBOT TAB ==============================
with tab1:
    # Green Title
    st.markdown(
        """
        <h2 style='text-align:center; color:#2e7d32; font-family:Trebuchet MS;'>
            💬 Zeptar AI HealthCareSystem Chatbot
        </h2>
        """,
        unsafe_allow_html=True
    )

    # Intro Box
    st.markdown(
        """
        <div style='background-color:#f0f0f0; border-radius:12px; padding:15px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);'>
            <p style='font-size:16px; color:#000000; text-align:center;'>
            🤖 <b>Ask Zeptar</b> anything related to health, diseases, or wellness!<br>
            Zeptar is powered by Google's Gemini model to give accurate and friendly answers.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Input box
    user_input = st.text_input(
        "🧠 Ask Zeptar AIHealthCareSystem:",
        "",
        placeholder="e.g., What are the symptoms of a brain tumor?"
    )

    # Styled button
    ask_button = st.button("✨ Ask Zeptar")

    if ask_button:
        if user_input.strip():
            try:
                genai.configure(api_key=app.API_KEY)
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(user_input)

                # Answer Box - black background, white text
                st.markdown(
                    f"""
                    <div style='background-color:#000000; border-left:6px solid #2e7d32;
                                padding:15px; border-radius:8px; margin-top:15px;
                                box-shadow: 0px 2px 8px rgba(0,0,0,0.08);'>
                        <h4 style='color:#2e7d32; font-family:Trebuchet MS;'>🩺 Zeptar says:</h4>
                        <p style='font-size:16px; color:#ffffff;'>{response.text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"⚠ Zeptar ran into an error: {e}")
        else:
            st.warning("Please type your question first 🧠.")


# ============================== BRAIN TUMOR DETECTION ==============================
with tab2:
    st.header("🧠 Brain Tumor Detection using YOLOv8")

    col1, col2 = st.columns(2)

    # ---- Single Image Upload ----
    with col1:
        st.subheader("📤 Detect from Single MRI Image")
        uploaded_file = st.file_uploader("Upload MRI Image:", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_file.write(uploaded_file.read())
            st.image(uploaded_file, caption="Uploaded MRI Image", use_column_width=True)

            if st.button("🔍 Detect Tumor in Uploaded Image"):
                st.info("Running YOLOv8 model... Please wait ⏳")
                images = app.brain_tumor_detection_single(temp_file.name)
                for img in images:
                    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Detection Result")

    # ---- Val Folder Detection (Popup) ----
    with col2:
        st.subheader("🧩 Detect from Validation Folder (Popup Window)")
        st.write("Runs detection on all MRI images in brain_mri_detection/val.")
        if st.button("▶ Run on Val Folder (Popup)"):
            st.warning("👉 A separate window will open. Press ESC to stop early.")
            app.brain_tumor_detection_from_val_folder()
            st.success("✅ Detection completed (check console for details).")

# ============================== BMT SYSTEM ==============================
with tab3:
    st.header("🧬 Bone Marrow Transplant Management")
    choice = st.radio("Select Action", ["Add Donor", "Add Patient", "Find Donor Match", "View All Data"])

    if choice == "Add Donor":
        st.subheader("➕ Add Donor Details")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        phone = st.text_input("Phone")
        blood_group = st.text_input("Blood Group")
        hla = st.text_input("HLA")
        if st.button("Save Donor"):
            if name and phone and blood_group and hla:
                _, msg = app.add_donor(name, age, phone, blood_group, hla)
                st.success(msg)
            else:
                st.warning("Please fill all donor details.")

    elif choice == "Add Patient":
        st.subheader("➕ Add Patient Details")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        disease = st.text_input("Disease")
        hla = st.text_input("HLA")
        if st.button("Save Patient"):
            if name and disease and hla:
                _, msg = app.add_patient(name, age, disease, hla)
                st.success(msg)
            else:
                st.warning("Please fill all patient details.")

    elif choice == "Find Donor Match":
        st.subheader("🔍 Find Matching Donors")
        patient_hla = st.text_input("Enter Patient HLA to Search:")
        if st.button("Find Match"):
            matches = app.find_donor_match(patient_hla)
            if matches:
                st.success(f"Found {len(matches)} matching donor(s):")
                st.table(matches)
            else:
                st.error("❌ No matching donor found.")

    elif choice == "View All Data":
        donors, patients = app.load_data()
        st.subheader("👨‍🔬 Donors")
        st.table(donors)
        st.subheader("🧫 Patients")
        st.table(patients)

# ============================== FOOTER ==============================
st.markdown("---")
st.markdown("👩‍💻 Developed by *Zeptar* | Hackathon Project 🚀")