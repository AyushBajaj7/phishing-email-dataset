"""
NLP Preprocessing Module

WHAT: Clean and normalize email text for ML processing
HOW: Lowercasing, special character removal, tokenization, stopword removal, lemmatization
WHY: Reduces noise and improves model performance
WHY NOT: Not implementing from scratch because NLTK provides battle-tested implementations
"""

import re
import ssl
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Bypass SSL verification for NLTK downloads (fixes SSL certificate errors)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def ensure_nltk_resources():
    """
    Download required NLTK resources if not already present.
    This ensures the module works without manual intervention.
    """
    resources = {
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4",
    }
    for path, name in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


# Initialize resources
ensure_nltk_resources()
STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def preprocess_text(text):
    """
    Apply NLP preprocessing pipeline to text.
    
    STEPS:
    1. Lowercasing - Normalizes case for consistent processing
    2. Remove special characters - Removes noise while preserving alphanumeric content
    3. Tokenization - Splits text into individual words
    4. Stopword removal - Removes common words that carry little semantic meaning
    5. Lemmatization - Reduces words to base form for better generalization
    
    Args:
        text (str): Raw email text
        
    Returns:
        str: Preprocessed clean text
    """
    # Step 1: Lowercasing
    text = text.lower()
    
    # Step 2: Remove special characters (keep only alphanumeric and spaces)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    
    # Step 3: Tokenization (simple split)
    tokens = text.split()
    
    # Step 4: Stopword removal
    tokens = [word for word in tokens if word not in STOP_WORDS]
    
    # Step 5: Lemmatization
    tokens = [LEMMATIZER.lemmatize(word) for word in tokens]
    
    return " ".join(tokens)
