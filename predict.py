"""
Prediction Module - Real-time Email Classification

WHAT: Take user input email and predict if it's phishing or legitimate
HOW: Load trained model, process email, return prediction with confidence
WHY: Enables real-time classification for new emails
"""

import pickle
import numpy as np
import os
import re
import warnings
from main import process_email
from sklearn.feature_extraction.text import TfidfVectorizer

# Suppress sklearn UserWarnings about feature names
warnings.filterwarnings("ignore", category=UserWarning)

# Define models directory
MODELS_DIR = "models"


def validate_email_format(email):
    """
    Validate email format.
    
    WHAT: Check if email follows standard format
    HOW: Regex pattern matching
    WHY: Prevents invalid email addresses from being processed
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not email.strip():
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


class PhishingPredictor:
    """
    Real-time phishing email predictor.
    
    Uses the trained Hybrid Random Forest model for predictions.
    """
    
    def __init__(self):
        """
        Initialize predictor with trained model and vectorizer.
        """
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """
        Load trained model and preprocessing objects from disk.
        
        WHAT: Load model artifacts
        HOW: Load pickle files saved during training
        WHY: Avoid retraining for every prediction
        """
        try:
            # Load trained model
            with open(f'{MODELS_DIR}/hybrid_rf_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            
            # Load TF-IDF vectorizer
            with open(f'{MODELS_DIR}/tfidf_vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # Load scaler
            with open(f'{MODELS_DIR}/feature_scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            
            print("✅ Model loaded successfully")
        except FileNotFoundError:
            print("⚠️  Model files not found. Run models.py to train and save models first.")
            self.model = None
            self.vectorizer = None
            self.scaler = None
    
    def predict(self, raw_email, sender_email, receiver_email):
        """
        Predict if email is phishing or legitimate.
        
        WHAT: Classify email using trained model
        HOW: Process email, extract features, run prediction
        WHY: Real-time classification for new emails
        
        Args:
            raw_email (str): Email content
            sender_email (str): Sender's email address
            receiver_email (str): Receiver's email address
        
        Returns:
            dict: Prediction results with label and confidence
        """
        if self.model is None:
            return {"error": "Model not loaded. Run models.py first."}
        
        # Validate email formats
        if not validate_email_format(sender_email):
            return {"error": f"Invalid sender email format: {sender_email}"}
        if not validate_email_format(receiver_email):
            return {"error": f"Invalid receiver email format: {receiver_email}"}
        
        # Process email using single source of truth
        processed = process_email(raw_email, sender_email, receiver_email, label=0)
        
        # Extract features
        clean_text = processed["clean_text"]
        text_features = processed["features"]
        sender_features = processed["sender"]
        
        # TF-IDF transformation
        tfidf_features = self.vectorizer.transform([clean_text]).toarray()
        
        # Engineered features (exact 8 features used in training)
        engineered = np.array([[
            text_features["email_length"],
            text_features["word_count"],
            text_features["num_links"],
            text_features["urgency_score"],
            text_features["suspicious_score"],
            sender_features["is_free"],
            sender_features["has_typos"],
            sender_features["has_suspicious_words"]
        ]])
        
        # Scale engineered features
        engineered_scaled = self.scaler.transform(engineered)
        
        # Combine features
        combined = np.hstack([tfidf_features, engineered_scaled])
        
        # Predict with custom threshold (0.4 for security - catch more phishing)
        probability = self.model.predict_proba(combined)[0]
        prob_phishing = probability[1]
        
        # Threshold: 0.4 (lower than default 0.5 to minimize false negatives)
        prediction = 1 if prob_phishing >= 0.4 else 0
        
        # Interpret result
        label = "Phishing" if prediction == 1 else "Legitimate"
        confidence = probability[prediction]
        
        return {
            "prediction": label,
            "confidence": f"{confidence:.2%}",
            "probability_phishing": f"{prob_phishing:.2%}",
            "probability_legitimate": f"{probability[0]:.2%}",
            "urgency_score": text_features["urgency_score"],
            "suspicious_score": text_features["suspicious_score"]
        }


def interactive_prediction():
    """
    Interactive prediction from user input.
    """
    print("\n🔬 Phishing Email Prediction")
    print("=" * 40)
    
    predictor = PhishingPredictor()
    
    if predictor.model is None:
        print("\n❌ Cannot make predictions. Please run models.py first to train and save models.")
        return
    
    print("\nEnter email details:")
    raw_email = input("Email content: ")
    sender_email = input("Sender email: ")
    receiver_email = input("Receiver email: ")
    
    result = predictor.predict(raw_email, sender_email, receiver_email)
    
    if "error" in result:
        print(f"\n❌ {result['error']}")
    else:
        print("\n📊 Prediction Results:")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   P(Phishing): {result['probability_phishing']}")
        print(f"   Urgency Score: {result['urgency_score']}")
        print(f"   Suspicious Score: {result['suspicious_score']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 4:
        # Programmatic mode: python predict.py "email_content" "sender@example.com" "receiver@example.com"
        raw_email = sys.argv[1]
        sender_email = sys.argv[2]
        receiver_email = sys.argv[3]
        
        predictor = PhishingPredictor()
        result = predictor.predict(raw_email, sender_email, receiver_email)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']}")
            print(f"P(Phishing): {result['probability_phishing']}")
            print(f"Urgency Score: {result['urgency_score']}")
            print(f"Suspicious Score: {result['suspicious_score']}")
    else:
        # Interactive mode
        interactive_prediction()
