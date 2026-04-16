# Architecture Justification - Phishing Email Detection System

## Table of Contents
1. [Dataset Design](#dataset-design)
2. [NLP Preprocessing](#nlp-preprocessing)
3. [Feature Engineering](#feature-engineering)
4. [Database Design](#database-design)
5. [Modular Architecture](#modular-architecture)
6. [Data Analytics](#data-analytics)
7. [Machine Learning Models](#machine-learning-models)
8. [Visualization Strategy](#visualization-strategy)

---

## Dataset Design

### What
A balanced dataset of 100 email samples (50 phishing, 50 legitimate) with fields: raw_email, clean_text, sender_email, receiver_email, sender_domain, and label.

### How
Hard-coded realistic email examples representing common phishing patterns (urgency, account verification, payment updates) and legitimate communications (meetings, deliveries, personal messages).

### Why
- **Balanced dataset**: Prevents model bias toward majority class
- **100 samples**: Sufficient for initial training while maintaining quality control
- **Realistic examples**: Ensures model learns actual phishing patterns, not synthetic artifacts
- **No duplicates**: Prevents data leakage and overfitting

### Why Not Alternatives
- **Synthetic generation**: Would produce unrealistic patterns that don't generalize
- **Web scraping**: Would introduce noise, legal issues, and quality control problems
- **Larger unbalanced dataset**: Would bias model without providing additional value

---

## NLP Preprocessing

### What
Text cleaning pipeline: lowercasing → remove special characters → tokenization → stopword removal → lemmatization.

### How
Using NLTK library:
- `lower()`: Case normalization
- `re.sub()`: Remove non-alphanumeric characters
- `split()`: Simple tokenization
- `nltk.corpus.stopwords`: Stopword removal
- `WordNetLemmatizer`: Lemmatization

### Why
- **Lowercasing**: Normalizes case for consistent processing (e.g., "URGENT" = "urgent")
- **Remove special characters**: Eliminates noise while preserving semantic content
- **Tokenization**: Enables word-level analysis
- **Stopword removal**: Removes common words (the, is, at) that carry little semantic meaning
- **Lemmatization**: Reduces words to base form (running → run) for better generalization

### Why Not Alternatives
- **Implement from scratch**: NLTK provides battle-tested, optimized implementations
- **Stemming instead of lemmatization**: Lemmatization produces actual dictionary words, better for interpretability
- **No preprocessing**: Raw text contains too much noise for effective ML

---

## Feature Engineering

### What
Extraction of domain-specific features from email text and sender information.

### Text Features
- **email_length**: Character count of cleaned text
- **word_count**: Number of words in cleaned text
- **num_links**: Count of http/www references
- **urgency_score**: Count of urgency-indicating words (urgent, now, verify, update, immediately)
- **suspicious_score**: Count of phishing-indicating words (click, login, bank, password, account)

### Sender Features
- **is_free_email**: Binary indicator for free email providers (gmail, yahoo, etc.)
- **has_suspicious_words**: Binary indicator for suspicious words in domain
- **has_typos**: Binary indicator for homoglyphs/typos in domain (0 for o, 1 for i, etc.)
- **domain_length**: Character count of domain

### How
Manual implementation using string operations and keyword matching.

### Why
- **Domain knowledge**: Phishing has specific patterns not captured by raw text alone
- **Interpretability**: Each feature has clear meaning (unlike black-box embeddings)
- **Efficiency**: Fast computation, suitable for real-time detection
- **Complementary**: Works alongside text-based features (TF-IDF)

### Why Not Alternatives
- **Automated feature extraction**: Would miss domain-specific phishing patterns
- **Only text features**: Would miss sender analysis which is critical for phishing detection
- **Deep learning embeddings**: Would be overkill, less interpretable, and require more data

---

## Database Design

### What
MongoDB Atlas document-based NoSQL database with nested document structure.

### Document Structure
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

### Operations
- `insert_many()`: Bulk insertion for initial dataset
- `find()`: Query and retrieval
- `count_documents()`: Analytics and validation
- `update_one()`: Modify existing records
- `delete_one()`: Remove records

### How
Using pymongo driver with connection string from environment variables.

### Why
- **Semi-structured data**: Email data has nested structure (sender info, features) that doesn't fit rigid SQL tables
- **Flexible schema**: Easy to add new features without schema migrations
- **Document model**: Natural representation of email as a single document
- **Scalability**: MongoDB Atlas provides horizontal scaling for large datasets
- **Better than alternatives**:
  - **Wide-column (Cassandra)**: Overkill, less flexible for nested structures
  - **Graph (Neo4j)**: Relationships are not primary concern (sender-recipient links are simple)

### Why Not Alternatives
- **SQL (PostgreSQL/MySQL)**: Requires complex joins for nested data, schema migrations for new features
- **CSV files**: No concurrent access, no querying capabilities, not production-ready
- **Wide-column DBs**: Designed for time-series or key-value patterns, not document storage

---

## Modular Architecture

### What
Separation of concerns across multiple modules with single source of truth for email processing.

### Module Structure
- **main.py**: Core processing (preprocessing, feature extraction, process_email)
- **update_dataset.py**: Dataset updates with duplicate checking
- **database.py**: MongoDB connection and operations
- **nlp_preprocessing.py**: NLP preprocessing module
- **feature_engineering.py**: Feature extraction module
- **models.py**: Hybrid ML models (rule-based, Naive Bayes, Random Forest)
- **analytics.py**: Data analytics (imbalance, scaling, missing values)
- **dataset_generator.py**: Initial dataset creation

### How
Each module has single responsibility and imports from others as needed. `process_email()` in main.py is the single source of truth for all email processing.

### Why
- **Single source of truth**: `process_email()` ensures consistent processing across dataset generation, updates, and prediction
- **Maintainability**: Each module can be modified independently
- **Testability**: Individual modules can be unit tested
- **Reusability**: Modules can be used in other projects
- **No duplicate logic**: Prevents inconsistencies between training and inference

### Why Not Alternatives
- **Monolithic script**: Would be unmaintainable, hard to test, and prone to errors
- **Duplicate logic**: Would cause inconsistencies (e.g., different preprocessing for training vs prediction)
- **Tight coupling**: Would make changes difficult and risky

---

## Data Analytics

### What
Analysis of class imbalance, feature scaling needs, and missing values.

### Components
1. **Class imbalance visualization**: Bar plot showing phishing vs legitimate distribution
2. **Scaling**: StandardScaler applied to numerical features
3. **Missing values**: Heatmap showing missing value patterns with percentage calculation

### How
Using pandas for data manipulation, sklearn for scaling, matplotlib/seaborn for visualization.

### Why
- **Class imbalance**: Imbalanced datasets bias ML models; visualization informs resampling decisions
- **Scaling**: Features on different scales bias distance-based algorithms; StandardScaler normalizes to zero mean, unit variance
- **Missing values**: Missing data degrades model performance; analysis identifies data quality issues

### Why Not Alternatives
- **No analytics**: Would miss critical data quality issues that impact model performance
- **Excessive analysis**: Would waste time on irrelevant insights (e.g., correlation matrix for small dataset)
- **PCA for model input**: Would reduce interpretability without clear benefit for this use case

---

## Machine Learning Models

### Model 1: Rule-Based (Custom)

#### What
Threshold-based classification: score = urgency + suspicious + typos, classify as phishing if score ≥ threshold.

#### How
Manual implementation summing scores and applying threshold.

#### Why
- **Interpretability**: Clear logic that can be explained to stakeholders
- **No training required**: Immediate deployment
- **Baseline performance**: Provides comparison point for ML models
- **Fast**: Minimal computation, suitable for real-time detection

#### Why Not Alternatives
- **Complex rules**: Would be overfitting to specific patterns
- **ML-only**: Would lose explainability

---

### Model 2: Naive Bayes (Baseline)

#### What
Multinomial Naive Bayes using TF-IDF features only.

#### How
sklearn TfidfVectorizer + MultinomialNB classifier.

#### Why
- **Baseline for comparison**: Establishes text-only performance
- **Fast training**: Efficient for large datasets
- **Works well with text**: Naive Bayes is effective for text classification
- **Probabilistic**: Provides confidence scores

#### Why Not Alternatives
- **SVM/Logistic Regression**: Would be more complex without clear benefit for baseline
- **Deep learning**: Would require more data and computational resources

---

### Model 3: Hybrid Random Forest (Final System)

#### What
Random Forest classifier combining TF-IDF text features with engineered features.

#### How
Concatenate TF-IDF vectors with engineered features, train sklearn RandomForestClassifier.

#### Why
- **Combines strengths**: Text patterns (TF-IDF) + domain knowledge (engineered features)
- **Non-linear**: Captures complex interactions between features
- **Feature importance**: Provides interpretability through feature importance scores
- **Robust**: Less prone to overfitting than individual decision trees
- **Ensemble**: Multiple trees reduce variance

#### Why Not Alternatives
- **TF-IDF only**: Would miss domain-specific sender analysis
- **Engineered only**: Would miss text patterns
- **Cosine similarity**: Not a classifier, cannot make predictions
- **SVM**: Less interpretable, doesn't provide feature importance
- **Neural networks**: Overkill for this dataset size, less interpretable

---

### Evaluation Metrics

#### What
Accuracy, confusion matrix, classification report, feature importance.

#### How
sklearn metrics functions and matplotlib/seaborn for visualization.

#### Why
- **Accuracy**: Overall performance measure
- **Confusion matrix**: Shows false positives/negatives (critical for security applications)
- **Classification report**: Precision, recall, F1-score for detailed analysis
- **Feature importance**: Model interpretability and validation

#### Why Not Alternatives
- **ROC/AUC**: Less intuitive for binary classification with balanced dataset
- **Only accuracy**: Would miss false positive/negative rates critical for security

---

## Visualization Strategy

### What
Tableau dashboards for class distribution, missing values, feature distribution, model comparison, and feature importance.

### How
Export data from MongoDB to CSV, connect Tableau, build dashboards with filters and interactivity.

### Why
- **Stakeholder communication**: Visual summaries are easier to understand than raw numbers
- **Monitoring**: Track dataset quality and model performance over time
- **Interactivity**: Filters allow exploration of specific subsets
- **Professional**: Tableau is industry-standard for business intelligence

### Why Not Alternatives
- **Python plots**: Less interactive, harder to share with non-technical stakeholders
- **No visualization**: Would miss insights from visual patterns
- **Excel charts**: Limited interactivity and scalability

---

## System Properties

### Modular
Each component has single responsibility and clear interfaces.

### Duplicate-Safe
Single source of truth (`process_email()`) ensures consistency.

### Scalable
MongoDB Atlas provides horizontal scaling; modular design allows component-level scaling.

### Interpretable
Rule-based model provides clear logic; feature importance explains ML decisions.

### Scientifically Justified
Every component has explicit justification based on requirements, not arbitrary choices.

---

## Conclusion

This architecture follows strict requirements:
- Document-based NoSQL (MongoDB Atlas) for semi-structured email data
- Modular design with single source of truth
- Hybrid ML approach (rule-based + Naive Bayes + Random Forest)
- Comprehensive NLP preprocessing and feature engineering
- Data analytics and visualization for monitoring
- Clear justifications for every design decision

The system is production-ready, maintainable, and scientifically justified.
