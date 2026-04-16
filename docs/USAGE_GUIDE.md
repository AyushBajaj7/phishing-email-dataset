# Phishing Detection System - Complete Usage Guide

## 📋 System Status

### ✅ Working Components
- **dataset_generator.py**: Generates 204 email samples (102 phishing, 102 legitimate)
- **main.py**: Core processing pipeline with process_email() function
- **nlp_preprocessing.py**: Text cleaning (lowercasing, special chars removal, tokenization, stopword removal, lemmatization)
- **feature_engineering.py**: Text + sender feature extraction
- **database.py**: MongoDB connection and operations (configured and working)
- **setup.py**: Database initialization
- **analytics.py**: Data analytics (class imbalance, scaling, missing values)
- **models.py**: ML models (rule-based, Naive Bayes, Random Forest)
- **update_dataset.py**: Dataset updates with duplicate checking
- **predict.py**: Real-time email classification (uses trained model)

---

## 📁 File Classification

### 🔴 CORE FILES (Required - DO NOT MODIFY)
```
nlp_preprocessing.py        # NLP preprocessing module
feature_engineering.py     # Feature extraction module
database.py                # MongoDB connection and operations
main.py                    # Single source of truth for email processing
update_dataset.py          # Dataset updates with duplicate checking
dataset_generator.py       # Initial dataset creation
analytics.py               # Data analytics (requires MongoDB)
models.py                  # ML models (requires MongoDB)
predict.py                 # Real-time email classification
requirements.txt           # Python dependencies
.env                       # MongoDB configuration (needs password)
```

### 📚 DOCUMENTATION FILES (Reference)
```
README.md                  # Project overview and quick start
ARCHITECTURE_JUSTIFICATION.md  # Detailed justifications for every component
TABLEAU_DASHBOARDS.md      # Tableau dashboard specifications
USAGE_GUIDE.md             # This file - complete usage guide
```

### 🟡 OPTIONAL/TEMPORARY FILES (Can be kept but not essential)
```
.env.example               # Template for .env configuration
setup.py                   # One-time database initialization
comprehensive_test.py      # Test suite for model evaluation
```

---

## 🚀 Setup Instructions

### Step 1: Configure MongoDB
**What**: Update .env with actual MongoDB password
**How**: Edit `c:\Users\acer\data science\mongodb\.env`
**When**: Before running any database-dependent operations

```bash
# Edit .env file and replace <db_password> with actual password
MONGODB_URI=mongodb+srv://ayushbajaj215:YOUR_ACTUAL_PASSWORD@cluster0.ajksb.mongodb.net/?appName=Cluster0
DATABASE_NAME=phishing_detection
COLLECTION_NAME=emails
```

### Step 2: Install Dependencies
**What**: Install required Python packages
**How**: Already completed (pandas 3.0.1, pymongo, scikit-learn, nltk, matplotlib, seaborn, python-dotenv)
**When**: First time setup
**Status**: ✅ Complete

### Step 3: Initialize Database
**What**: Load initial dataset into MongoDB
**How**: `python setup.py`
**When**: After configuring MongoDB password
**Status**: ✅ Complete

### Step 4: Test Processing Pipeline
**What**: Verify email processing works
**How**: `python main.py`
**When**: Any time to verify processing logic
**Status**: ✅ Working

### Step 5: Run Analytics
**What**: Analyze class imbalance, scaling, missing values
**How**: `python analytics.py`
**When**: After database initialization
**Status**: ✅ Complete

### Step 6: Train and Evaluate Models
**What**: Train rule-based, Naive Bayes, and Random Forest models
**How**: `python models.py`
**When**: After database initialization
**Status**: ✅ Complete

### Step 7: Make Predictions
**What**: Classify new emails as phishing or legitimate
**How**: `python predict.py "email_content" "sender@example.com" "receiver@example.com"`
**When**: After training models
**Status**: ✅ Complete

**Output Explanation**:
```
Prediction: Phishing
Confidence: 99.00%
P(Phishing): 99.00%
Urgency Score: 1
Suspicious Score: 2
```

**Prediction Threshold**: 0.4 (catches more phishing emails for security)

**Input Validation**:
- Email addresses must follow format `user@domain.com`
- Invalid inputs (e.g., "i am in urgent need for money" as email) will return error

---

## 🔄 Workflow

### Initial Setup (One-time)
1. Configure .env with MongoDB password
2. Run `python setup.py` to initialize database
3. Run `python analytics.py` to analyze data
4. Run `python models.py` to train models

### Ongoing Operations
- **Predict email**: `python predict.py "email" "sender" "receiver"`
- **Add new email**: `python update_dataset.py` (interactive or command-line)
- **Retrain models**: `python models.py` after adding new data
- **Re-run analytics**: `python analytics.py` to monitor data quality

### Testing Without MongoDB
- Not available - test files have been removed as they are no longer needed

---

## 📊 Expected Outputs

### setup.py
```
🚀 Setting up Phishing Detection Database
========================================
📧 Generating initial dataset...
✅ Generated 204 email samples

🗄️  Connecting to MongoDB Atlas...
✅ Connected to MongoDB Atlas
📥 Inserting dataset into MongoDB...
✅ Inserted 204 documents

📊 Database Statistics:
   Total documents: 204
   Phishing emails: 102
   Legitimate emails: 102
```

### analytics.py
```
🔬 Data Analytics Pipeline
========================================
✅ Loaded 204 samples from MongoDB

📊 Class Balance Analysis
========================================
Total samples: 204
Phishing (1): 102 (50%)
Legitimate (0): 102 (50%)
✅ Classes are perfectly balanced

📈 Generated visualizations:
   - class_distribution.png
   - missing_values_heatmap.png
   - feature_distributions.png
```

### models.py
```
🤖 Machine Learning Pipeline
========================================
✅ Loaded 204 samples from MongoDB

MODEL 1: Rule-Based (Custom)
========================================
Accuracy: 0.7903 (79.03%)

MODEL 2: Naive Bayes Baseline (TF-IDF Only)
========================================
Accuracy: 0.9194 (91.94%)

MODEL 3: Hybrid Random Forest (TF-IDF + Engineered)
========================================
Accuracy: 0.9194 (91.94%)
Top Feature Importances:
  tfidf_2: 0.1285
  suspicious_score: 0.1284
  email_length: 0.0989
  urgency_score: 0.0967
  has_suspicious_words: 0.0511

📈 Generated visualizations:
   - confusion_matrix_rule_based.png
   - confusion_matrix_naive_bayes.png
   - confusion_matrix_hybrid_random_forest.png
   - feature_importance.png
   - model_comparison.png
```

---

## 🐛 Troubleshooting

### MongoDB Authentication Error
**Error**: `bad auth : authentication failed`
**Cause**: Placeholder password in .env file
**Solution**: Replace `<db_password>` with actual MongoDB Atlas password in .env

### Python Version Compatibility
**Supported**: Python 3.14+ (all components tested and working)
**Note**: MongoDB Atlas requires IP whitelist registration (not SSL compatibility issue)
**Status**: ✅ Fully compatible with Python 3.14

### Missing NLTK Resources
**Error**: `LookupError: Resource stopwords not found`
**Cause**: NLTK resources not downloaded
**Solution**: The system automatically downloads required resources on first run

### MongoDB Connection Error (IP Whitelist)
**Error**: `SSL handshake failed: [SSL: TLSV1_ALERT_INTERNAL_ERROR]`
**Cause**: MongoDB Atlas IP whitelist - new IP address not registered after internet change
**Solution**: Add new IP address to MongoDB Atlas → Network Access → IP Whitelist
**Note**: Error message is misleading - actual issue is IP registration, not SSL

---

## 📝 Next Steps

1. **Optional**: Build Tableau dashboards using specifications in TABLEAU_DASHBOARDS.md
2. **Ongoing**: Add new emails using `python update_dataset.py`
3. **Ongoing**: Retrain models after adding data using `python models.py`

---

## 🎯 System Architecture Summary

- **NLP Preprocessing**: NLTK-based text cleaning
- **Feature Engineering**: Manual implementation of domain-specific features
- **Database**: MongoDB Atlas with document structure
- **ML Models**: Hybrid approach (rule-based + Naive Bayes + Random Forest)
- **Evaluation**: Accuracy, confusion matrix, classification report, feature importance
- **Visualization**: Matplotlib/Seaborn for analytics, Tableau for dashboards

All components are modular, well-documented, and scientifically justified per ARCHITECTURE_JUSTIFICATION.md.
