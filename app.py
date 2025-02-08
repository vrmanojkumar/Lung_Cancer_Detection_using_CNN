import os
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Path to the pre-trained model
MODEL_PATH = r'C:\Users\manoj\OneDrive\Desktop\mini project\lung_cancer_model.h5'

# Load the model
model = load_model(MODEL_PATH)

def preprocess_image(image_file):
    """Preprocess the uploaded image for model prediction."""
    img = Image.open(image_file).convert('RGB')  # Ensure image is in RGB format
    img = img.resize((256, 256))  # Resize to match model input
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_cancer():
    try:
        # Get form data
        patient_name = request.form.get('patient_name')
        patient_age = request.form.get('patient_age')
        patient_gender = request.form.get('patient_gender')
        patient_contact = request.form.get('patient_contact')
        patient_address = request.form.get('patient_address')
        medical_history = request.form.get('medical_history')

        # Get uploaded image
        ct_scan = request.files.get('ct_scan')

        # Validate inputs
        if not all([patient_name, patient_age, patient_contact, ct_scan]):
            return jsonify({
                'error': 'Please fill in all required fields and upload a CT scan image.'
            }), 400

        # Preprocess image
        img_array = preprocess_image(ct_scan)

        # Make prediction
        prediction = model.predict(img_array)
        cancer_probability = prediction[0][0]

        # Determine result
        if cancer_probability > 0.5:
            result = "⚠️ POTENTIAL CANCER DETECTED"
            recommendation = "Urgent Follow-up Required"
            result_class = "danger"
        else:
            result = "✅ NO CANCER DETECTED"
            recommendation = "Regular Health Monitoring"
            result_class = "success"

        # Generate report
        report = {
            'patient_name': patient_name,
            'patient_age': patient_age,
            'patient_gender': patient_gender,
            'patient_contact': patient_contact,
            'patient_address': patient_address,
            'medical_history': medical_history,
            'result': result,
            'recommendation': recommendation,
            'result_class': result_class,
            'probability': float(cancer_probability)
        }

        return jsonify(report)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
