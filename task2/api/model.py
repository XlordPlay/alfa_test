from fastapi import FastAPI, HTTPException
import onnxruntime as ort
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from fastapi.responses import FileResponse
from schemas import InputData


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
features_path = os.path.join(root_dir, "src", "onnx", "selected_features.json")
html_file_path_for_mount = os.path.join(root_dir, "src", "front_end")
MODEL_PATH = os.path.join(root_dir, "src", "onnx", "RandomForest.onnx")
html_file_path = os.path.join(root_dir, "src", "front_end", "content.html") 



with open(features_path, "r") as f:
    FEATURES = json.load(f)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(html_file_path_for_mount, StaticFiles(directory=html_file_path_for_mount), name="static")


@app.post("/predict")
def predict(data: InputData, threshold: float = 0.27):  
    try:
        
        print("Received features:", data.features)

        
        if not all(feature in data.features for feature in FEATURES):
            raise HTTPException(status_code=400, detail="INCORRECT DATA...")
        
        
        X = np.array([[data.features[f] for f in FEATURES]], dtype=np.float32)
        session = ort.InferenceSession(MODEL_PATH)
        input_name = session.get_inputs()[0].name
        
        print("Input array for prediction:", X)

        
        pred = session.run(None, {input_name: X})[0]
        
        print("Raw prediction result:", pred[0])

        
        prediction_class = 1 if pred[0] >= threshold else 0
        
        return {"prediction": prediction_class}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    




with open(html_file_path, 'r') as file:
    html_content = file.read()


@app.get("/")
def root():
    return FileResponse(html_file_path)