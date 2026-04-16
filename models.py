"""
Machine Learning Models Module

WHAT: Implements hybrid ML approach (rule-based + Naive Bayes + Random Forest)
HOW: Custom rule-based logic combined with sklearn classifiers
WHY: Hybrid approach combines interpretable rules with data-driven patterns
WHY NOT: Not using cosine similarity (not a classifier) or unnecessary models
"""

import numpy as np
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from database import db_manager

# Create directories if they don't exist
OUTPUTS_DIR = "outputs"
MODELS_DIR = "models"
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


def load_data_from_mongodb():
    """
    Load dataset from MongoDB into pandas DataFrame.
    
    WHAT: Retrieve all documents from MongoDB
    HOW: Query collection and convert to DataFrame
    WHY: Pandas provides convenient data manipulation for ML
    """
    if not db_manager.connect():
        return None
    
    documents = db_manager.find()
    db_manager.disconnect()
    
    if not documents:
        print("❌ No documents found in database")
        return None
    
    # Flatten nested structure for ML
    flattened = []
    for doc in documents:
        flat_doc = {
            "clean_text": doc["clean_text"],
            "email_length": doc["features"]["email_length"],
            "word_count": doc["features"]["word_count"],
            "num_links": doc["features"]["num_links"],
            "urgency_score": doc["features"]["urgency_score"],
            "suspicious_score": doc["features"]["suspicious_score"],
            "is_free": doc["sender"]["is_free"],
            "has_typos": doc["sender"]["has_typos"],
            "has_suspicious_words": doc["sender"]["has_suspicious_words"],
            "label": doc["label"]
        }
        flattened.append(flat_doc)
    
    return pd.DataFrame(flattened)


# ============================================================================
# MODEL 1: Rule-Based Model (CUSTOM)
# ============================================================================

class RuleBasedModel:
    """
    Rule-based phishing detection model.
    
    WHAT: Threshold-based classification using urgency + suspicious + typos scores
    HOW: Sum scores and apply threshold
    WHY: Interpretable, fast, no training required, provides baseline
    """
    
    def __init__(self, threshold=2):
        """
        Initialize rule-based model.
        
        Args:
            threshold (int): Score threshold for phishing classification
        """
        self.threshold = threshold
    
    def predict(self, df):
        """
        Predict using rule-based logic.
        
        WHAT: Calculate score = urgency + suspicious + typos
        HOW: Sum scores and compare to threshold
        WHY: Combines multiple suspicious indicators
        
        Args:
            df (pd.DataFrame): DataFrame with features
            
        Returns:
            np.array: Predictions (0=legitimate, 1=phishing)
        """
        # Calculate composite score
        scores = (
            df["urgency_score"] +
            df["suspicious_score"] +
            df["has_typos"]
        )
        
        # Apply threshold
        predictions = (scores >= self.threshold).astype(int)
        return predictions
    
    def evaluate(self, y_true, y_pred):
        """
        Evaluate model performance.
        
        WHAT: Calculate accuracy and confusion matrix
        HOW: sklearn metrics
        WHY: Standard evaluation metrics
        """
        accuracy = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        
        print("\n📊 Rule-Based Model Evaluation")
        print("=" * 40)
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Threshold: {self.threshold}")
        print("\nConfusion Matrix:")
        print(cm)
        
        return accuracy, cm
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name):
        """
        Plot confusion matrix visualization.
        
        WHAT: Visualize confusion matrix
        HOW: seaborn heatmap
        WHY: Visual representation aids interpretation
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                   xticklabels=["Legitimate", "Phishing"],
                   yticklabels=["Legitimate", "Phishing"])
        plt.title(f"Confusion Matrix - {model_name}")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.savefig(f"{OUTPUTS_DIR}/confusion_matrix_{model_name.lower().replace(' ', '_')}.png", 
                   dpi=150, bbox_inches="tight")
        print(f"📈 Saved: {OUTPUTS_DIR}/confusion_matrix_{model_name.lower().replace(' ', '_')}.png")
        plt.close()


# ============================================================================
# MODEL 2: Naive Bayes Baseline (TF-IDF ONLY)
# ============================================================================

class NaiveBayesBaseline:
    """
    Naive Bayes baseline model using TF-IDF only.
    
    WHAT: Multinomial Naive Bayes with TF-IDF vectorization
    HOW: sklearn TfidfVectorizer + MultinomialNB
    WHY: Baseline for comparison, works well with text features
    """
    
    def __init__(self):
        """Initialize Naive Bayes model."""
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.model = MultinomialNB()
    
    def train(self, X_text, y):
        """
        Train model with TF-IDF features only.
        
        WHAT: Fit vectorizer and train classifier
        HOW: fit_transform on text, then fit classifier
        WHY: Establishes text-only baseline
        """
        X_tfidf = self.vectorizer.fit_transform(X_text)
        self.model.fit(X_tfidf, y)
        print("✅ Naive Bayes model trained with TF-IDF features")
    
    def predict(self, X_text):
        """
        Predict using TF-IDF features only.
        
        WHAT: Transform text and classify
        HOW: transform then predict
        WHY: Consistent with training approach
        """
        X_tfidf = self.vectorizer.transform(X_text)
        return self.model.predict(X_tfidf)
    
    def evaluate(self, y_true, y_pred):
        """
        Evaluate model performance.
        """
        accuracy = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        report = classification_report(y_true, y_pred)
        
        print("\n📊 Naive Bayes Baseline Evaluation")
        print("=" * 40)
        print(f"Accuracy: {accuracy:.4f}")
        print("\nConfusion Matrix:")
        print(cm)
        print("\nClassification Report:")
        print(report)
        
        return accuracy, cm, report
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name):
        """
        Plot confusion matrix visualization.
        
        WHAT: Visualize confusion matrix
        HOW: seaborn heatmap
        WHY: Visual representation aids interpretation
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                   xticklabels=["Legitimate", "Phishing"],
                   yticklabels=["Legitimate", "Phishing"])
        plt.title(f"Confusion Matrix - {model_name}")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.savefig(f"{OUTPUTS_DIR}/confusion_matrix_{model_name.lower().replace(' ', '_')}.png", 
                   dpi=150, bbox_inches="tight")
        print(f"📈 Saved: {OUTPUTS_DIR}/confusion_matrix_{model_name.lower().replace(' ', '_')}.png")
        plt.close()


# ============================================================================
# MODEL 3: Hybrid Random Forest (TF-IDF + Engineered Features)
# ============================================================================

class HybridRandomForest:
    """
    Hybrid Random Forest model combining TF-IDF and engineered features.
    
    WHAT: Random Forest with TF-IDF + numerical features
    HOW: Concatenate TF-IDF and engineered features, train Random Forest
    WHY: Combines text patterns with domain knowledge for better performance
    """
    
    def __init__(self, n_estimators=100):
        """
        Initialize hybrid model.
        
        Args:
            n_estimators (int): Number of trees in Random Forest
        """
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        self.feature_names = None
    
    def train(self, X_text, X_features, y):
        """
        Train the hybrid model.
        
        WHAT: Fit TF-IDF vectorizer on text, train Random Forest on combined features
        HOW: Vectorize text, combine with engineered features, fit classifier
        """
        # Fit TF-IDF on training text
        self.vectorizer.fit(X_text)
        X_tfidf = self.vectorizer.transform(X_text).toarray()
        
        # Combine features (X_features is already numpy array from scaling)
        X_combined = np.hstack([X_tfidf, X_features])
        
        # Train Random Forest
        self.model.fit(X_combined, y)
        
        # Store feature names for importance
        tfidf_feature_names = [f"tfidf_{i}" for i in range(X_tfidf.shape[1])]
        engineered_feature_names = ["email_length", "word_count", "num_links", "urgency_score", "suspicious_score", "is_free", "has_typos", "has_suspicious_words"]
        self.feature_names = tfidf_feature_names + engineered_feature_names
        
        print("✅ Hybrid Random Forest model trained with TF-IDF + engineered features")
    
    def predict(self, X_text, X_features):
        """
        Predict using combined features.
        
        WHAT: Transform text, combine with features, classify
        HOW: Consistent with training approach
        """
        X_tfidf = self.vectorizer.transform(X_text).toarray()
        X_combined = np.hstack([X_tfidf, X_features])
        return self.model.predict(X_combined)
    
    def evaluate(self, y_true, y_pred):
        """
        Evaluate model performance with feature importance.
        """
        accuracy = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        report = classification_report(y_true, y_pred)
        
        print("\n📊 Hybrid Random Forest Evaluation")
        print("=" * 40)
        print(f"Accuracy: {accuracy:.4f}")
        print("\nConfusion Matrix:")
        print(cm)
        print("\nClassification Report:")
        print(report)
        
        # Feature importance
        if self.feature_names:
            importances = self.model.feature_importances_
            indices = np.argsort(importances)[::-1][:10]  # Top 10
            
            print("\nTop 10 Feature Importances:")
            for i in indices:
                print(f"  {self.feature_names[i]}: {importances[i]:.4f}")
            
            # Visualize feature importance
            plt.figure(figsize=(10, 6))
            plt.title("Top 10 Feature Importances")
            plt.bar(range(len(indices)), importances[indices])
            plt.xticks(range(len(indices)), [self.feature_names[i] for i in indices], rotation=45)
            plt.tight_layout()
            plt.savefig(f"{OUTPUTS_DIR}/feature_importance.png", dpi=150, bbox_inches="tight")
            print(f"📈 Saved: {OUTPUTS_DIR}/feature_importance.png")
            plt.close()
        
        return accuracy, cm, report
    
    def save_model(self, scaler):
        """
        Save trained model and preprocessing objects for real-time predictions.
        
        WHAT: Save model, vectorizer, and scaler to disk
        HOW: Using pickle serialization
        WHY: Enables predict.py to load and use trained model without retraining
        """
        with open(f'{MODELS_DIR}/hybrid_rf_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(f'{MODELS_DIR}/tfidf_vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        with open(f'{MODELS_DIR}/feature_scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        
        print("✅ Model artifacts saved for real-time predictions")
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name):
        """
        Plot confusion matrix visualization.
        
        WHAT: Visualize confusion matrix
        HOW: seaborn heatmap
        WHY: Visual representation aids interpretation
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                   xticklabels=["Legitimate", "Phishing"],
                   yticklabels=["Legitimate", "Phishing"])
        plt.title(f"Confusion Matrix - {model_name}")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.savefig(f"{OUTPUTS_DIR}/confusion_matrix_{model_name.lower().replace(' ', '_')}.png", 
                   dpi=150, bbox_inches="tight")
        print(f"📈 Saved: {OUTPUTS_DIR}/confusion_matrix_{model_name.lower().replace(' ', '_')}.png")
        plt.close()


def main():
    """
    Train and evaluate all three models.
    """
    print("🤖 Machine Learning Pipeline")
    print("=" * 40)
    
    # Load data
    df = load_data_from_mongodb()
    if df is None:
        return
    
    print(f"✅ Loaded {len(df)} samples from MongoDB")
    
    # Split data
    X_train, X_test = train_test_split(df, test_size=0.3, random_state=42, stratify=df["label"])
    
    # Prepare features
    engineered_features = [
        "email_length", "word_count", "num_links",
        "urgency_score", "suspicious_score",
        "is_free", "has_typos", "has_suspicious_words"
    ]
    
    X_train_features = X_train[engineered_features]
    X_test_features = X_test[engineered_features]
    
    # Scale engineered features with feature names to avoid warnings
    scaler = StandardScaler()
    X_train_features_scaled = scaler.fit_transform(X_train_features)
    X_test_features_scaled = scaler.transform(X_test_features)
    
    y_train = X_train["label"]
    y_test = X_test["label"]
    
    # ============================================================================
    # MODEL 1: Rule-Based
    # ============================================================================
    print("\n" + "=" * 40)
    print("MODEL 1: Rule-Based (Custom)")
    print("=" * 40)
    
    rule_model = RuleBasedModel(threshold=2)
    y_pred_rule = rule_model.predict(X_test)
    rule_model.evaluate(y_test, y_pred_rule)
    rule_model.plot_confusion_matrix(y_test, y_pred_rule, "Rule-Based")
    
    # ============================================================================
    # MODEL 2: Naive Bayes Baseline
    # ============================================================================
    print("\n" + "=" * 40)
    print("MODEL 2: Naive Bayes Baseline (TF-IDF Only)")
    print("=" * 40)
    
    nb_model = NaiveBayesBaseline()
    nb_model.train(X_train["clean_text"], y_train)
    y_pred_nb = nb_model.predict(X_test["clean_text"])
    nb_model.evaluate(y_test, y_pred_nb)
    nb_model.plot_confusion_matrix(y_test, y_pred_nb, "Naive Bayes")
    
    # ============================================================================
    # MODEL 3: Hybrid Random Forest (Final System)
    # ============================================================================
    print("\n" + "=" * 40)
    print("MODEL 3: Hybrid Random Forest (TF-IDF + Engineered)")
    print("=" * 40)
    
    hybrid_model = HybridRandomForest(n_estimators=100)
    hybrid_model.train(X_train["clean_text"], X_train_features_scaled, y_train)
    y_pred_hybrid = hybrid_model.predict(X_test["clean_text"], X_test_features_scaled)
    hybrid_model.evaluate(y_test, y_pred_hybrid)
    hybrid_model.plot_confusion_matrix(y_test, y_pred_hybrid, "Hybrid Random Forest")
    
    # Save model for real-time predictions
    hybrid_model.save_model(scaler)
    
    # ============================================================================
    # Model Comparison
    # ============================================================================
    print("\n" + "=" * 40)
    print("MODEL COMPARISON")
    print("=" * 40)
    
    rule_acc = accuracy_score(y_test, y_pred_rule)
    nb_acc = accuracy_score(y_test, y_pred_nb)
    hybrid_acc = accuracy_score(y_test, y_pred_hybrid)
    
    comparison = pd.DataFrame({
        "Model": ["Rule-Based", "Naive Bayes", "Hybrid Random Forest"],
        "Accuracy": [rule_acc, nb_acc, hybrid_acc],
        "Features": ["Engineered Only", "TF-IDF Only", "TF-IDF + Engineered"]
    })
    
    print(comparison.to_string(index=False))
    
    # Visualize comparison
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Model", y="Accuracy", data=comparison, palette="Set2", hue="Model", legend=False)
    plt.title("Model Accuracy Comparison")
    plt.ylim(0, 1)
    plt.savefig(f"{OUTPUTS_DIR}/model_comparison.png", dpi=150, bbox_inches="tight")
    print(f"📈 Saved: {OUTPUTS_DIR}/model_comparison.png")
    plt.close()
    
    print("\n✅ ML pipeline complete")
    print("📈 Generated visualizations:")
    print("   - confusion_matrix_rule_based.png")
    print("   - confusion_matrix_naive_bayes.png")
    print("   - confusion_matrix_hybrid_random_forest.png")
    print("   - feature_importance.png")
    print("   - model_comparison.png")


if __name__ == "__main__":
    main()
