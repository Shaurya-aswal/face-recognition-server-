# Configure CORS for your specific Vercel domain
CORS(app, origins=[
    'https://face-recogn-live-mu.vercel.app',  # ✅ Your current domain 
    'http://localhost:3000',  # for local development
    'https://localhost:3000'
], supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'])

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB limit

# Load model artifacts on startup
try:
    util.load_saved_artifacts()
    print("✅ Model artifacts loaded successfully")
except Exception as e:
    print(f"❌ Error loading artifacts: {e}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask server is running for Sports Celebrity Classifier!",
        "status": "healthy",
        "endpoints": {
            "classify": "/classify_image",
            "health": "/health"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "healthy",
        "model_loaded": util.__model is not None if hasattr(util, '__model') else False
    }), 200

@app.route("/classify_image", methods=["POST", "OPTIONS"])
def classify_image():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200
    
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
        print(f"❌ Classification error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)