from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from ml_model import detector

detection_bp = Blueprint('detection', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """
    Check if the file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@detection_bp.route('/api/detect', methods=['POST'])
def detect_image():
    """
    Detect if an uploaded image is AI generated or original
    """
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file part in the request"
        }), 400
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({
            "status": "error",
            "message": "No selected file"
        }), 400
    
    # Check if the file is allowed
    if not allowed_file(file.filename):
        return jsonify({
            "status": "error",
            "message": "Image Not Found/Unsupported File Type (Only JPG/PNG accepted)."
        }), 400
    
    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    
    try:
        # Process the image with our ML model
        result = detector.predict(filepath)
        
        # Remove the temporary file
        os.remove(filepath)
        
        if result is None:
            return jsonify({
                "status": "error",
                "message": "Failed to process the image"
            }), 500
        
        return jsonify({
            "status": "success",
            "result": result
        }), 200
        
    except Exception as e:
        # Clean up the file if there was an error
        if os.path.exists(filepath):
            os.remove(filepath)
            
        return jsonify({
            "status": "error",
            "message": f"Error processing image: {str(e)}"
        }), 500