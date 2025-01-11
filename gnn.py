from flask import Flask, request, jsonify
import os
import cv2
import torch
from some_deepfake_model import load_model, predict_deepfake  # Replace with actual model

app = Flask(__name__)

# Load the lightweight deepfake detection model
model = load_model("path_to_model_weights")  # Replace with actual model loading

@app.route('/detect_deepfake', methods=['POST'])
def detect_deepfake():
    try:
        # Check if video file is in the request
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        video_file = request.files['video']
        
        # Save the video file temporarily for processing
        video_path = os.path.join('uploads', video_file.filename)
        video_file.save(video_path)

        # Process the video file
        is_deepfake = process_video(video_path)

        # Return the result as JSON
        result = {
            "is_deepfake": is_deepfake
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Extract 10 seconds of the video (assuming 30fps -> 300 frames)
    frames = []
    frame_count = 0
    while cap.isOpened() and frame_count < 300:  # Process 10 seconds (300 frames at 30fps)
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        frame_count += 1
    
    cap.release()

    # Convert frames to a format suitable for the model
    frames_tensor = torch.tensor(frames).float()  # Convert frames to tensor (adjust for model input)
    
    # Predict whether the video is a deepfake
    result = predict_deepfake(model, frames_tensor)

    # Return whether the video is a deepfake (0: Real
