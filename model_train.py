import joblib
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def train_model():
    print("Loading MNIST dataset... (this may take a minute)")
    # Fetching a smaller subset to speed up training for the demo
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='liac-arff')
    
    # Use a subset of 10,000 samples for faster training
    X = X[:10000]
    y = y[:10000]
    
    # Preprocessing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    print("Training SGD Classifier...")
    # SGD is fast and efficient for larger datasets
    model = SGDClassifier(max_iter=1000, tol=1e-3, random_state=42)
    model.fit(X_train, y_train)
    
    # Print accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model Training Complete. Accuracy: {accuracy * 100:.2f}%")
    
    # Save model and scaler
    # We save as a dictionary to bundle the scaler too
    model_data = {
        'model': model,
        'scaler': scaler
    }
    
    joblib.dump(model_data, 'model.pkl')
    print("Model saved to model.pkl")

if __name__ == "__main__":
    train_model()
