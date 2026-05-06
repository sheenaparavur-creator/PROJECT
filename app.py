from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os
from model_train import train_model

# Initialize FastAPI app
app = FastAPI(title="MNIST Digit Classifier API")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to hold the model and scaler
model_assets = None

# Model loading/training on startup
@app.on_event("startup")
async def load_model_on_startup():
    global model_assets
    model_path = "model.pkl"
    
    if not os.path.exists(model_path):
        print("Model file not found. Auto-training started...")
        train_model()
    
    print("Loading model assets...")
    try:
        model_assets = joblib.load(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")

# Input schema
class PredictionRequest(BaseModel):
    image: list[float]  # Expecting 784 pixels (28x28 flattened)

@app.get("/health")
async def root():
    return {"message": "MNIST Classifier API is running"}

@app.post("/predict")
async def predict(request: PredictionRequest):
    global model_assets
    
    if model_assets is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please wait for training to complete.")
    
    try:
        # Validate input size
        if len(request.image) != 784:
            raise HTTPException(status_code=400, detail=f"Expected 784 pixels, got {len(request.image)}")
        
        # Convert to numpy array and reshape
        img_array = np.array(request.image).reshape(1, -1)
        
        # Scale the features using the saved scaler
        scaler = model_assets['scaler']
        model = model_assets['model']
        
        img_scaled = scaler.transform(img_array)
        
        # Make prediction
        prediction = model.predict(img_scaled)[0]
        
        # Get confidence score (decision_function for SGD)
        # Simple softmax to get a "confidence"
        scores = model.decision_function(img_scaled)[0]
        exp_scores = np.exp(scores - np.max(scores))
        probabilities = exp_scores / exp_scores.sum()
        confidence = float(np.max(probabilities))
        
        return {
            "prediction": int(prediction),
            "confidence": confidence
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve React static files if they exist (for standalone deployment)
if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")

@app.exception_handler(404)
async def custom_404_handler(request, __):
    # Fallback to index.html for SPA routing
    if os.path.exists("dist/index.html"):
        return FileResponse("dist/index.html")
    return {"error": "Not Found"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
