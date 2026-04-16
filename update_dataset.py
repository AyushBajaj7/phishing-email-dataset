"""
Dataset Update Module

WHAT: Handles adding new emails to the dataset with duplicate prevention and input validation
HOW: Calls process_email() from main.py, checks MongoDB for duplicates, validates user input
WHY: Allows incremental dataset growth without introducing bias from duplicates or invalid data
WHY NOT: Not duplicating processing logic because main.py.process_email() is the single source of truth
"""

import sys
import re
from main import process_email
from database import db_manager


def validate_email_format(email):
    """
    Validate email format.
    
    WHAT: Check if email follows standard format
    HOW: Regex pattern matching
    WHY: Prevents invalid email addresses from entering database
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_email_content(raw_email):
    """
    Validate email content.
    
    WHAT: Check if email content is reasonable
    HOW: Check length, not empty, contains valid characters
    WHY: Prevents empty or malicious content from entering database
    
    Args:
        raw_email (str): Email content to validate
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not raw_email or not raw_email.strip():
        return False, "Email content cannot be empty"
    
    if len(raw_email) < 10:
        return False, "Email content too short (minimum 10 characters)"
    
    if len(raw_email) > 10000:
        return False, "Email content too long (maximum 10000 characters)"
    
    # Check for suspicious patterns that might indicate injection attempts
    suspicious_patterns = [
        r'<script', r'javascript:', r'on\w+\s*=', r'eval\(',
        r'exec\(', r'\$\(', r'__import__'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, raw_email, re.IGNORECASE):
            return False, f"Suspicious pattern detected: {pattern}"
    
    return True, ""


def validate_label(label):
    """
    Validate label value.
    
    WHAT: Check if label is 0 or 1
    HOW: Type and value checking
    WHY: Ensures binary classification
    
    Args:
        label: Label value to validate
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        label_int = int(label)
        if label_int not in [0, 1]:
            return False, "Label must be 0 (legitimate) or 1 (phishing)"
        return True, ""
    except (ValueError, TypeError):
        return False, "Label must be an integer (0 or 1)"


def add_email_to_dataset(raw_email, sender_email, receiver_email, label):
    """
    Add a new email to the dataset with comprehensive validation and duplicate checking.
    
    WHAT: Validate input, check for duplicates, insert new email into MongoDB
    HOW: Validate format/content, check duplicates, process and insert
    WHY: Prevents invalid data and duplicates from entering database
    
    Args:
        raw_email (str): Raw email content
        sender_email (str): Sender's email address
        receiver_email (str): Receiver's email address
        label (int): 0 for legitimate, 1 for phishing
    
    Returns:
        bool: True if added, False if validation failed, duplicate, or error
    """
    # Validate email content
    content_valid, content_error = validate_email_content(raw_email)
    if not content_valid:
        print(f"❌ Content validation failed: {content_error}")
        return False
    
    # Validate sender email format
    if not validate_email_format(sender_email):
        print(f"❌ Invalid sender email format: {sender_email}")
        return False
    
    # Validate receiver email format
    if not validate_email_format(receiver_email):
        print(f"❌ Invalid receiver email format: {receiver_email}")
        return False
    
    # Validate label
    label_valid, label_error = validate_label(label)
    if not label_valid:
        print(f"❌ Label validation failed: {label_error}")
        return False
    
    # Connect to database
    if not db_manager.connect():
        return False
    
    # Check for duplicates
    if db_manager.check_duplicate(raw_email, sender_email):
        print("⚠️  Duplicate email detected - not added")
        db_manager.disconnect()
        return False
    
    # Process email using single source of truth
    document = process_email(raw_email, sender_email, receiver_email, int(label))
    
    # Insert into database
    try:
        db_manager.insert_many([document])
        print("✅ Email added to dataset successfully")
        db_manager.disconnect()
        return True
    except Exception as e:
        print(f"❌ Error adding email: {e}")
        db_manager.disconnect()
        return False


def interactive_mode():
    """
    Interactive CLI for adding emails to dataset with validation.
    """
    print("📧 Add New Email to Dataset")
    print("=" * 40)
    
    raw_email = input("Enter email content: ").strip()
    sender_email = input("Enter sender email: ").strip()
    receiver_email = input("Enter receiver email (optional, press Enter to skip): ").strip()
    if not receiver_email:
        receiver_email = "user@gmail.com"
    
    label_input = input("Enter label (0=legitimate, 1=phishing): ").strip()
    
    # Validation will happen in add_email_to_dataset
    success = add_email_to_dataset(raw_email, sender_email, receiver_email, label_input)
    
    if success:
        print("\n📊 Current dataset statistics:")
        if db_manager.connect():
            total = db_manager.count_documents()
            phishing = db_manager.count_documents({"label": 1})
            legit = db_manager.count_documents({"label": 0})
            print(f"   Total emails: {total}")
            print(f"   Phishing: {phishing}")
            print(f"   Legitimate: {legit}")
            db_manager.disconnect()


def main():
    """
    Main entry point for dataset updates.
    """
    if len(sys.argv) > 1:
        # Command line mode
        if len(sys.argv) != 5:
            print("Usage: python update_dataset.py <raw_email> <sender_email> <receiver_email> <label>")
            print("Or run without arguments for interactive mode")
            return
        
        raw_email = sys.argv[1]
        sender_email = sys.argv[2]
        receiver_email = sys.argv[3]
        try:
            label = int(sys.argv[4])
        except ValueError:
            print("❌ Label must be 0 or 1")
            return
        
        add_email_to_dataset(raw_email, sender_email, receiver_email, label)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
