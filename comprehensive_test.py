"""
Comprehensive Test Script - 100 Different Input Combinations

WHAT: Test prediction system with 100 different email/sender combinations
HOW: Generate test cases covering all possible scenarios
WHY: Verify prediction accuracy across edge cases and combinations
"""

from predict import PhishingPredictor


def generate_test_cases():
    """
    Generate 100 test cases covering different combinations.
    
    WHAT: Create diverse test scenarios
    HOW: Mix phishing/legitimate emails with phishing/legitimate senders
    WHY: Test model robustness across combinations
    """
    
    # Test data
    phishing_emails = [
        "URGENT: Verify your bank account immediately",
        "Your account will be suspended unless you click here",
        "Congratulations! You've won $1,000,000 - claim now",
        "Security alert: Unusual activity detected - verify identity",
        "Update your payment information to continue service",
        "Your password has been reset - click to confirm",
        "Limited time offer: 90% off - act now",
        "Confirm your email address to verify account",
        "Your package is delayed - click for details",
        "Suspicious login attempt - secure your account"
    ]
    
    legitimate_emails = [
        "Meeting scheduled at 10 AM tomorrow",
        "Your order has been shipped and will arrive Monday",
        "Thanks for your help with the project yesterday",
        "Please review the attached document when convenient",
        "Team lunch tomorrow at the cafeteria",
        "Your subscription has been renewed successfully",
        "The quarterly report is ready for review",
        "Happy birthday! Hope you have a great day",
        "Reminder: dentist appointment on Friday at 2 PM",
        "The project deadline has been extended to next week"
    ]
    
    phishing_senders = [
        "support@amaz0n.com",
        "security@paypa1.com",
        "admin@g0ogle.com",
        "verify@netfl1x.com",
        "update@apple-id.com",
        "alert@bank-security.com",
        "service@micros0ft.com",
        "info@amaz0n-support.com",
        "support@faceb00k.com",
        "verify@yaho0-security.com"
    ]
    
    legitimate_senders = [
        "manager@company.com",
        "hr@organization.org",
        "support@legitimate-business.com",
        "admin@university.edu",
        "service@corporation.net",
        "team@startup.io",
        "info@nonprofit.org",
        "contact@agency.gov",
        "support@established-firm.com",
        "admin@institution.edu"
    ]
    
    test_cases = []
    
    # Generate combinations
    # 25 phishing email + phishing sender
    for i in range(25):
        email = phishing_emails[i % len(phishing_emails)]
        sender = phishing_senders[i % len(phishing_senders)]
        test_cases.append({
            "raw_email": email,
            "sender_email": sender,
            "receiver_email": "user@gmail.com",
            "expected": "Phishing",
            "combination": "phishing_email + phishing_sender"
        })
    
    # 25 phishing email + legitimate sender
    for i in range(25):
        email = phishing_emails[i % len(phishing_emails)]
        sender = legitimate_senders[i % len(legitimate_senders)]
        test_cases.append({
            "raw_email": email,
            "sender_email": sender,
            "receiver_email": "user@gmail.com",
            "expected": "Phishing",
            "combination": "phishing_email + legitimate_sender"
        })
    
    # 25 legitimate email + phishing sender
    for i in range(25):
        email = legitimate_emails[i % len(legitimate_emails)]
        sender = phishing_senders[i % len(phishing_senders)]
        test_cases.append({
            "raw_email": email,
            "sender_email": sender,
            "receiver_email": "user@gmail.com",
            "expected": "Legitimate",
            "combination": "legitimate_email + phishing_sender"
        })
    
    # 25 legitimate email + legitimate sender
    for i in range(25):
        email = legitimate_emails[i % len(legitimate_emails)]
        sender = legitimate_senders[i % len(legitimate_senders)]
        test_cases.append({
            "raw_email": email,
            "sender_email": sender,
            "receiver_email": "user@gmail.com",
            "expected": "Legitimate",
            "combination": "legitimate_email + legitimate_sender"
        })
    
    return test_cases


def run_comprehensive_tests():
    """
    Run 100 test cases and analyze results.
    """
    print("🧪 Running Comprehensive Prediction Tests")
    print("=" * 60)
    
    predictor = PhishingPredictor()
    
    if predictor.model is None:
        print("\n❌ Cannot run tests. Model not loaded. Run models.py first.")
        return
    
    test_cases = generate_test_cases()
    
    results = {
        "total": len(test_cases),
        "correct": 0,
        "incorrect": 0,
        "by_combination": {}
    }
    
    for i, test in enumerate(test_cases):
        result = predictor.predict(
            test["raw_email"],
            test["sender_email"],
            test["receiver_email"]
        )
        
        prediction = result["prediction"]
        expected = test["expected"]
        combination = test["combination"]
        
        is_correct = prediction == expected
        
        if is_correct:
            results["correct"] += 1
        else:
            results["incorrect"] += 1
        
        # Track by combination
        if combination not in results["by_combination"]:
            results["by_combination"][combination] = {"correct": 0, "incorrect": 0}
        
        if is_correct:
            results["by_combination"][combination]["correct"] += 1
        else:
            results["by_combination"][combination]["incorrect"] += 1
        
        # Print first 10 results
        if i < 10:
            status = "✅" if is_correct else "❌"
            print(f"{status} Test {i+1}: {combination}")
            print(f"   Expected: {expected}, Got: {prediction}")
            print(f"   Confidence: {result['confidence']}")
            print()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Total tests: {results['total']}")
    print(f"Correct: {results['correct']} ({results['correct']/results['total']:.2%})")
    print(f"Incorrect: {results['incorrect']} ({results['incorrect']/results['total']:.2%})")
    
    print("\n📈 Results by Combination:")
    for combo, counts in results["by_combination"].items():
        total = counts["correct"] + counts["incorrect"]
        accuracy = counts["correct"] / total if total > 0 else 0
        print(f"{combo}:")
        print(f"   Correct: {counts['correct']}/{total} ({accuracy:.2%})")
    
    return results


if __name__ == "__main__":
    run_comprehensive_tests()
