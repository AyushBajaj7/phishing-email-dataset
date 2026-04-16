"""
Feature Engineering Module

WHAT: Extracts relevant features from email text and sender information
HOW: Manual implementation of domain-specific feature extraction
WHY: Domain knowledge (urgency words, suspicious patterns, sender analysis) provides signal beyond raw text
WHY NOT: Not using automated feature extraction because phishing detection requires specific, interpretable features
"""

import re


# Text Feature Extraction Functions
def get_email_length(clean_text):
    """
    Calculate length of cleaned email text.
    
    WHAT: Character count of preprocessed text
    HOW: len() function on string
    WHY: Phishing emails often have different length patterns than legitimate emails
    """
    return len(clean_text)


def get_word_count(clean_text):
    """
    Calculate word count of cleaned email text.
    
    WHAT: Number of words in preprocessed text
    HOW: Split string and count tokens
    WHY: Phishing emails may use different word counts to convey urgency
    """
    return len(clean_text.split())


def count_links(raw_email):
    """
    Count number of links in email.
    
    WHAT: Count of http/https/www references
    HOW: String count for "http" and "www"
    WHY: Phishing emails often contain multiple suspicious links
    """
    return raw_email.count("http") + raw_email.count("www")


def calculate_urgency_score(clean_text):
    """
    Calculate urgency score based on urgency-indicating words.
    
    WHAT: Count of urgency words in text
    HOW: Check for presence of urgency keywords
    WHY: Phishing emails frequently use urgency to pressure victims
    """
    urgency_words = ["urgent", "now", "verify", "update", "immediately", "action", "required"]
    return sum(1 for word in urgency_words if word in clean_text.lower())


def calculate_suspicious_score(clean_text):
    """
    Calculate suspicious score based on phishing-indicating words.
    
    WHAT: Count of suspicious words in text
    HOW: Check for presence of phishing keywords
    WHY: Certain words (click, login, bank, password) are strongly associated with phishing
    """
    suspicious_words = ["click", "login", "bank", "password", "account", "secure", "confirm"]
    return sum(1 for word in suspicious_words if word in clean_text.lower())


# Sender Feature Extraction Functions
def extract_domain(sender_email):
    """
    Extract domain from sender email address.
    
    WHAT: Domain part of email (e.g., gmail.com from user@gmail.com)
    HOW: Split on '@' and take second part
    WHY: Domain analysis is critical for detecting spoofed/fake domains
    """
    return sender_email.split("@")[-1]


def is_free_email(domain):
    """
    Check if domain is a free email provider.
    
    WHAT: Binary indicator (1 if free provider, 0 otherwise)
    HOW: Check against list of known free email providers
    WHY: Legitimate business emails typically use custom domains, phishing often uses free providers
    """
    free_providers = [
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
        "aol.com", "protonmail.com", "icloud.com", "live.com"
    ]
    return int(domain in free_providers)


def has_suspicious_words_in_domain(domain):
    """
    Check if domain contains suspicious words.
    
    WHAT: Binary indicator (1 if suspicious words present, 0 otherwise)
    HOW: Check for phishing-related keywords in domain
    WHY: Phishing domains often contain words like "secure", "verify", "update" to appear legitimate
    """
    suspicious_keywords = ["secure", "verify", "update", "account", "login", "bank", "confirm"]
    return int(any(keyword in domain.lower() for keyword in suspicious_keywords))


def has_typos_in_domain(domain):
    """
    Check if domain contains typos or homoglyphs.
    
    WHAT: Binary indicator (1 if typos detected, 0 otherwise)
    HOW: Check for common typo patterns (0 for o, 1 for i, rn for m, etc.)
    WHY: Phishing domains use typos to mimic legitimate domains (e.g., amaz0n.com)
    """
    # Common homoglyph and typo patterns used in phishing
    typo_patterns = ["0", "1", "rn", "@", "!", "_", "ww", "vv", "vv", "rn"]
    return int(any(pattern in domain.lower() for pattern in typo_patterns))


def get_domain_length(domain):
    """
    Calculate domain length.
    
    WHAT: Character count of domain
    HOW: len() function
    WHY: Unusually long or short domains can indicate phishing attempts
    """
    return len(domain)
