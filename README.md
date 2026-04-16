# Phishing Email Detection System - Production Implementation

## System Architecture Overview

This is a production-quality phishing detection pipeline implementing:
- Document-based NoSQL storage (MongoDB Atlas)
- Modular architecture with single source of truth
- Hybrid ML approach (Rule-based + Naive Bayes + Random Forest)
- Comprehensive NLP preprocessing and feature engineering
- Data analytics and visualization

## Project Structure

```
mongodb/
├── main.py                    # Core processing (preprocessing, feature extraction, process_email)
├── update_dataset.py          # Dataset updates with duplicate checking
├── database.py               # MongoDB connection and operations
├── nlp_preprocessing.py      # NLP preprocessing module
├── feature_engineering.py    # Feature extraction module
├── models.py                 # Hybrid ML models (rule-based, Naive Bayes, Random Forest)
├── analytics.py              # Data analytics (imbalance, scaling, missing values)
├── dataset_generator.py      # Initial dataset creation (50-100 balanced samples)
├── requirements.txt
├── .env.example
└── ARCHITECTURE_JUSTIFICATION.md  # Detailed justifications for every component
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and add your MongoDB Atlas connection string.

## Usage

1. **Generate initial dataset:**
   ```bash
   python dataset_generator.py
   ```

2. **Process emails (core module):**
   ```bash
   python main.py
   ```

3. **Update dataset with new emails:**
   ```bash
   python update_dataset.py
   ```

4. **Run data analytics:**
   ```bash
   python analytics.py
   ```

5. **Train and evaluate models:**
   ```bash
   python models.py
   ```

## MongoDB Document Structure

Each email is stored as:
```json
{
  "raw_email": "...",
  "clean_text": "...",
  "sender": {
    "email": "...",
    "domain": "...",
    "is_free": 0,
    "has_typos": 1,
    "has_suspicious_words": 1
  },
  "features": {
    "email_length": 120,
    "word_count": 18,
    "num_links": 2,
    "urgency_score": 1,
    "suspicious_score": 2
  },
  "label": 1
}
```

## ML Models

1. **Rule-Based Model**: Threshold-based classification using urgency + suspicious + typos scores (79.03% accuracy)
2. **Naive Bayes (Baseline)**: TF-IDF only for comparison (91.94% accuracy)
3. **Hybrid Random Forest**: TF-IDF + engineered features (final system, 91.94% accuracy)

## Dataset Statistics

- **Total samples**: 204 (102 phishing, 102 legitimate)
- **Balance**: Perfectly balanced (50% phishing, 50% legitimate)
- **Test split**: 30% (62 samples)
- **Composition**:
  - Phishing: 50 from suspicious domains + 52 from legitimate-looking domains
  - Legitimate: 50 from genuine domains + 52 from suspicious-looking typo domains

## Evaluation Metrics

- Accuracy
- Confusion Matrix
- Classification Report
- Feature Importance

## Model Performance Summary

| Model | Accuracy | Features |
|-------|----------|----------|
| Rule-Based | 79.03% | Engineered Only |
| Naive Bayes | 91.94% | TF-IDF Only |
| Hybrid Random Forest | 91.94% | TF-IDF + Engineered |

**Top Feature Importances** (Hybrid Model):
1. tfidf_2 (12.85%)
2. suspicious_score (12.84%)
3. email_length (9.89%)
4. urgency_score (9.67%)
5. has_suspicious_words (5.11%)

## Tableau Visualization

See `ARCHITECTURE_JUSTIFICATION.md` for dashboard specifications including:
- Class distribution with filters
- Missing values heatmap
- Feature distribution with interactivity
