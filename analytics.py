"""
Data Analytics Module

WHAT: Analyzes dataset for class imbalance, scaling needs, and missing values
HOW: Uses pandas, sklearn, matplotlib, and seaborn for analysis
WHY: Understanding data distribution and quality is essential for effective ML
WHY NOT: Not including excessive analysis because only relevant insights are needed
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from database import db_manager

# Create outputs directory if it doesn't exist
OUTPUTS_DIR = "outputs"
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def load_data_from_mongodb():
    """
    Load dataset from MongoDB into pandas DataFrame.
    
    WHAT: Retrieve all documents from MongoDB
    HOW: Query collection and convert to DataFrame
    WHY: Pandas provides convenient data manipulation for analysis
    """
    if not db_manager.connect():
        return None
    
    documents = db_manager.find()
    db_manager.disconnect()
    
    if not documents:
        print("❌ No documents found in database")
        return None
    
    # Flatten nested structure for analysis
    flattened = []
    for doc in documents:
        flat_doc = {
            "raw_email": doc["raw_email"],
            "clean_text": doc["clean_text"],
            "sender_email": doc["sender"]["email"],
            "sender_domain": doc["sender"]["domain"],
            "is_free": doc["sender"]["is_free"],
            "has_typos": doc["sender"]["has_typos"],
            "has_suspicious_words": doc["sender"]["has_suspicious_words"],
            "email_length": doc["features"]["email_length"],
            "word_count": doc["features"]["word_count"],
            "num_links": doc["features"]["num_links"],
            "urgency_score": doc["features"]["urgency_score"],
            "suspicious_score": doc["features"]["suspicious_score"],
            "label": doc["label"]
        }
        flattened.append(flat_doc)
    
    return pd.DataFrame(flattened)


def analyze_class_balance(df):
    """
    Analyze class distribution and handle imbalance.
    
    WHAT: Check for class imbalance and visualize distribution
    HOW: Count labels, calculate ratio, create bar plot
    WHY: Imbalanced datasets bias ML models toward majority class
    
    Returns:
        dict: Class balance statistics
    """
    print("\n📊 Class Balance Analysis")
    print("=" * 40)
    
    label_counts = df["label"].value_counts()
    total = len(df)
    phishing_count = label_counts.get(1, 0)
    legit_count = label_counts.get(0, 0)
    
    print(f"Total samples: {total}")
    print(f"Phishing (1): {phishing_count} ({phishing_count/total*100:.1f}%)")
    print(f"Legitimate (0): {legit_count} ({legit_count/total*100:.1f}%)")
    
    # Check imbalance
    ratio = max(phishing_count, legit_count) / min(phishing_count, legit_count)
    if ratio > 1.5:
        print(f"⚠️  Class imbalance detected (ratio: {ratio:.2f})")
        print("   Consider resampling techniques (SMOTE, random undersampling)")
    else:
        print("✅ Classes are balanced")
    
    # Visualization
    plt.figure(figsize=(8, 5))
    sns.countplot(x="label", data=df, palette="Set2", hue="label", legend=False)
    plt.title("Class Distribution")
    plt.xlabel("Label (0=Legitimate, 1=Phishing)")
    plt.ylabel("Count")
    plt.savefig(f"{OUTPUTS_DIR}/class_distribution.png", dpi=150, bbox_inches="tight")
    print(f"📈 Saved: {OUTPUTS_DIR}/class_distribution.png")
    plt.close()
    
    return {
        "total": total,
        "phishing": phishing_count,
        "legitimate": legit_count,
        "ratio": ratio
    }


def analyze_missing_values(df):
    """
    Analyze missing values in dataset.
    
    WHAT: Check for missing/null values and visualize
    HOW: Calculate missing percentage, create heatmap
    WHY: Missing values can degrade model performance
    
    Returns:
        dict: Missing value statistics
    """
    print("\n🔍 Missing Values Analysis")
    print("=" * 40)
    
    missing = df.isnull().sum()
    missing_percentage = (missing / len(df)) * 100
    
    print("Missing values per column:")
    for col in df.columns:
        if missing[col] > 0:
            print(f"  {col}: {missing[col]} ({missing_percentage[col]:.1f}%)")
    
    if missing.sum() == 0:
        print("✅ No missing values detected")
    else:
        print(f"⚠️  Total missing values: {missing.sum()}")
    
    # Heatmap visualization
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
    plt.title("Missing Values Heatmap")
    plt.savefig(f"{OUTPUTS_DIR}/missing_values_heatmap.png", dpi=150, bbox_inches="tight")
    print(f"📈 Saved: {OUTPUTS_DIR}/missing_values_heatmap.png")
    plt.close()
    
    return {
        "total_missing": int(missing.sum()),
        "columns_with_missing": int((missing > 0).sum())
    }


def apply_feature_scaling(df):
    """
    Apply StandardScaler to numerical features.
    
    WHAT: Scale numerical features to zero mean and unit variance
    HOW: sklearn StandardScaler
    WHY: Features on different scales can bias distance-based algorithms
    """
    print("\n📏 Feature Scaling")
    print("=" * 40)
    
    numerical_features = [
        "email_length", "word_count", "num_links",
        "urgency_score", "suspicious_score"
    ]
    
    # Check if features exist
    available_features = [f for f in numerical_features if f in df.columns]
    
    if not available_features:
        print("❌ No numerical features found for scaling")
        return None
    
    print(f"Scaling features: {available_features}")
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[available_features])
    
    # Create scaled feature names
    scaled_feature_names = [f"{f}_scaled" for f in available_features]
    
    # Add scaled features to DataFrame
    for i, feature_name in enumerate(scaled_feature_names):
        df[feature_name] = scaled_features[:, i]
    
    print("✅ Features scaled successfully")
    print("   Mean: ~0, Std Dev: ~1")
    
    return scaler


def analyze_feature_distributions(df):
    """
    Analyze distribution of numerical features.
    
    WHAT: Visualize feature distributions by class
    HOW: Box plots and histograms
    WHY: Understanding feature distributions helps identify discriminative power
    """
    print("\n📊 Feature Distribution Analysis")
    print("=" * 40)
    
    numerical_features = [
        "email_length", "word_count", "num_links",
        "urgency_score", "suspicious_score"
    ]
    
    available_features = [f for f in numerical_features if f in df.columns]
    
    # Box plots by class
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, feature in enumerate(available_features):
        if i < len(axes):
            sns.boxplot(x="label", y=feature, data=df, ax=axes[i], palette="Set2", hue="label", legend=False)
            axes[i].set_title(f"{feature} by Class")
            axes[i].set_xlabel("Label (0=Legitimate, 1=Phishing)")
    
    # Remove empty subplot
    if len(available_features) < len(axes):
        for i in range(len(available_features), len(axes)):
            fig.delaxes(axes[i])
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUTS_DIR}/feature_distributions.png", dpi=150, bbox_inches="tight")
    print(f"📈 Saved: {OUTPUTS_DIR}/feature_distributions.png")
    plt.close()


def main():
    """
    Run complete analytics pipeline.
    """
    print("🔬 Data Analytics Pipeline")
    print("=" * 40)
    
    # Load data
    df = load_data_from_mongodb()
    if df is None:
        return
    
    print(f"✅ Loaded {len(df)} samples from MongoDB")
    
    # Run analyses
    class_stats = analyze_class_balance(df)
    missing_stats = analyze_missing_values(df)
    scaler = apply_feature_scaling(df)
    analyze_feature_distributions(df)
    
    print("\n✅ Analytics complete")
    print("📈 Generated visualizations:")
    print("   - class_distribution.png")
    print("   - missing_values_heatmap.png")
    print("   - feature_distributions.png")


if __name__ == "__main__":
    main()
