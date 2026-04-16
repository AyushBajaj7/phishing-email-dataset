"""
Main Processing Module - Single Source of Truth

WHAT: Core email processing pipeline combining NLP preprocessing and feature engineering
HOW: Orchestrates preprocessing and feature extraction through process_email() function
WHY: Single source of truth ensures consistency across dataset generation, updates, and prediction
WHY NOT: Not duplicating logic because that would cause inconsistencies between training and inference
"""

from nlp_preprocessing import preprocess_text
from feature_engineering import (
    get_email_length, get_word_count, count_links,
    calculate_urgency_score, calculate_suspicious_score,
    extract_domain, is_free_email, has_suspicious_words_in_domain,
    has_typos_in_domain, get_domain_length
)


def process_email(raw_email, sender_email, receiver_email, label):
    """
    SINGLE SOURCE OF TRUTH for email processing.
    
    WHAT: Complete pipeline from raw email to structured document
    HOW: Applies NLP preprocessing and feature engineering in sequence
    WHY: Ensures identical processing for all emails (dataset generation, updates, predictions)
    
    Args:
        raw_email (str): Raw email content
        sender_email (str): Sender's email address
        receiver_email (str): Receiver's email address
        label (int): 0 for legitimate, 1 for phishing
    
    Returns:
        dict: Structured document matching MongoDB schema
    """
    # NLP Preprocessing
    clean_text = preprocess_text(raw_email)
    
    # Feature Engineering - Sender Information
    domain = extract_domain(sender_email)
    
    # Feature Engineering - Text Features
    text_features = {
        "email_length": get_email_length(clean_text),
        "word_count": get_word_count(clean_text),
        "num_links": count_links(raw_email),
        "urgency_score": calculate_urgency_score(clean_text),
        "suspicious_score": calculate_suspicious_score(clean_text)
    }
    
    # Feature Engineering - Sender Features
    sender_info = {
        "email": sender_email,
        "domain": domain,
        "is_free": is_free_email(domain),
        "has_typos": has_typos_in_domain(domain),
        "has_suspicious_words": has_suspicious_words_in_domain(domain)
    }
    
    # Construct final document matching MongoDB schema
    document = {
        "raw_email": raw_email,
        "clean_text": clean_text,
        "sender": sender_info,
        "features": text_features,
        "label": label
    }
    
    return document


def main():
    """
    Demonstrate the processing pipeline with sample data.
    """
    # Sample phishing email
    sample_phishing = process_email(
        raw_email="URGENT: Verify your bank account immediately",
        sender_email="support@amaz0n.com",
        receiver_email="user@gmail.com",
        label=1
    )
    
    # Sample legitimate email
    sample_legit = process_email(
        raw_email="Meeting scheduled at 10 AM tomorrow",
        sender_email="manager@company.com",
        receiver_email="user@gmail.com",
        label=0
    )
    
    print("✅ Processing pipeline demonstration")
    print("\n📧 Phishing Email Sample:")
    print(sample_phishing)
    print("\n📧 Legitimate Email Sample:")
    print(sample_legit)
    
    return sample_phishing, sample_legit


if __name__ == "__main__":
    main()
