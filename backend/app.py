import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import T5ForConditionalGeneration, T5TokenizerFast
import torch
import os

# Set a fallback directory for the model if the expected one is missing
MODEL_DIR = "./models/vehicle_chatbot_model_base"

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for communication with the React frontend

# Load the T5 model and tokenizer
def load_model():
    """Load the fine-tuned T5 model and tokenizer."""
    try:
        if not os.path.exists(MODEL_DIR):
            raise FileNotFoundError(f"Model directory not found at '{MODEL_DIR}'.")
            
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = T5TokenizerFast.from_pretrained(MODEL_DIR)
        model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR).to(device)
        print("Model and tokenizer loaded successfully!")
        return tokenizer, model, device
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        return None, None, None

tokenizer, model, device = load_model()

if not all([tokenizer, model, device]):
    print("Chatbot model failed to load. The Flask application will not be able to process requests.", file=sys.stderr)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Processes a user question and returns a diagnostic answer."""
    if not all([tokenizer, model, device]):
        return jsonify({"error": "Chatbot model is not loaded."}), 503

    # Check if the request contains JSON data
    if not request.is_json:
        print("Request does not contain JSON data.", file=sys.stderr)
        return jsonify({"error": "Request must be JSON."}), 400

    try:
        data = request.get_json()
        print(f"Received JSON data: {data}")

        if 'question' not in data or not isinstance(data['question'], str) or not data['question'].strip():
            print("Missing or invalid 'question' field in JSON data.", file=sys.stderr)
            return jsonify({"error": "Missing or empty 'question' in request body."}), 400

        user_question = data['question']
        
        prompt = f"diagnose: {user_question.strip()}"
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(device)
        
        output_sequences = model.generate(
            **inputs,
            max_length=128,
            num_beams=4,
            do_sample=True,
            temperature=0.4,
            early_stopping=True,
        )
        
        answer = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
        answer = answer.replace("diagnose:", "").strip().strip('",')

        return jsonify({"answer": answer})

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
