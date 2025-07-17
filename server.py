from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import os

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB limit

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running for Sports Celebrity Classifier!"

@app.route("/classify_image", methods=["POST"])
def classify_image():
    try:
        # Check if request has JSON data
        if not request.json:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Check if image_data exists in the request
        if "image_data" not in request.json:
            return jsonify({"error": "Missing 'image_data' field in request"}), 400
        
        image_data = request.json.get("image_data")
        
        # Check if image_data is not empty
        if not image_data:
            return jsonify({"error": "Empty image_data provided"}), 400
            
        result = util.classify_image(image_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_saved_artifacts()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
