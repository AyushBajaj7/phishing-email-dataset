"""
Dataset Generator Module

WHAT: Creates initial balanced dataset with 50-100 diverse email samples
HOW: Hard-coded realistic phishing and legitimate email examples
WHY: Provides foundation for training and testing ML models
WHY NOT: Not using synthetic generation because realistic examples are needed for meaningful training
"""

from nlp_preprocessing import preprocess_text
from feature_engineering import (
    get_email_length, get_word_count, count_links,
    calculate_urgency_score, calculate_suspicious_score,
    extract_domain, is_free_email, has_suspicious_words_in_domain,
    has_typos_in_domain, get_domain_length
)


# Dataset: 100 phishing + 100 legitimate = 200 total (balanced)
# Includes: Phishing from legitimate-looking senders AND legitimate from suspicious-looking senders
PHISHING_EMAILS = [
    # Original 50 phishing emails from suspicious domains
    ("URGENT: Verify your bank account immediately", "support@amaz0n.com"),
    ("Your account will be suspended if not updated", "alert@secure-bank.com"),
    ("Click here to reset your password now", "security@paypa1.com"),
    ("Security alert: unauthorized login detected", "noreply@bank-update.com"),
    ("Update your payment details to continue", "verify@account-secure.com"),
    ("Your bank account needs verification", "alert@banking-secure.com"),
    ("Confirm your identity immediately", "support@secure-login.com"),
    ("Login now to avoid service interruption", "help@verification-center.com"),
    ("Your account has been compromised", "security@account-protect.com"),
    ("Reset your password using this link", "update@secure-mail.com"),
    ("You have won a prize, claim now", "reward@claim-prize.com"),
    ("Congratulations! Click to claim your reward", "offer@win-now.com"),
    ("Verify your email account urgently", "verify@secure-access.com"),
    ("Suspicious activity detected in your account", "alert@fraud-detection.com"),
    ("Immediate action required: update account", "support@urgent-update.com"),
    ("Your payment has failed, update details", "billing@payment-failed.com"),
    ("Click here to unlock your account", "unlock@account-access.com"),
    ("Confirm your banking details now", "verify@banking-alert.com"),
    ("Your account access is restricted", "support@account-restricted.com"),
    ("Update your profile information now", "update@profile-secure.com"),
    ("Your account will expire soon", "expire@account-warning.com"),
    ("Re-verify your credentials immediately", "verify@credential-check.com"),
    ("Your account needs urgent attention", "alert@account-attention.com"),
    ("Secure your account by logging in", "secure@login-alert.com"),
    ("Action required: verify your details", "action@required-now.com"),
    ("Click below to confirm your account", "confirm@account-access.com"),
    ("Your account is under review", "review@account-check.com"),
    ("Login to restore your access", "restore@login-now.com"),
    ("Update your security information", "update@security-alert.com"),
    ("Your session has expired, login again", "session@expired-login.com"),
    ("Verify your account to avoid blocking", "verify@blocking-alert.com"),
    ("Important: update your login credentials", "important@login-update.com"),
    ("Unauthorized access detected, act now", "alert@unauthorized.com"),
    ("Click here to secure your account", "secure@account-now.com"),
    ("Account alert: verify immediately", "alert@verify-now.com"),
    ("Your Apple ID was used to sign in", "support@appleid-security.com"),
    ("Confirm your PayPal account now", "service@paypal-verify.com"),
    ("Netflix account payment failed", "billing@netflix-update.com"),
    ("Your Microsoft account has been locked", "security@microsoft-alert.com"),
    ("Amazon order cancellation notice", "orders@amazon-notice.com"),
    ("Your Facebook account is at risk", "security@facebook-protect.com"),
    ("Google account security warning", "no-reply@google-security.com"),
    ("Your LinkedIn password needs reset", "security@linkedin-verify.com"),
    ("Instagram account verification required", "help@instagram-secure.com"),
    ("Your Twitter account has been suspended", "support@twitter-alert.com"),
    ("eBay account needs immediate attention", "security@ebay-protect.com"),
    ("Your PayPal account is limited", "service@paypal-alert.com"),
    ("Bank of America security alert", "alert@boa-security.com"),
    ("Chase account verification required", "verify@chase-secure.com"),
    ("Wells Fargo account notice", "notice@wells-fargo-alert.com"),
    ("Your credit card was declined", "billing@card-verify.com"),
    
    # NEW: 50 phishing emails from LEGITIMATE-looking senders (gmail, company domains)
    ("Urgent: Your account needs immediate verification", "noreply@gmail.com"),
    ("Verify your bank details now to avoid suspension", "alert@outlook.com"),
    ("Security warning: Click here to secure your account", "security@yahoo.com"),
    ("Your account will be locked in 24 hours, verify now", "support@hotmail.com"),
    ("Confirm your identity to restore access", "help@company.com"),
    ("Urgent action required: Update your password", "admin@organization.org"),
    ("Your payment method has expired, update now", "billing@corporation.net"),
    ("Verify your email to continue using our service", "verify@university.edu"),
    ("Security alert: Unauthorized access detected", "security@institution.gov"),
    ("Your account is suspended, verify to unlock", "support@startup.io"),
    ("Immediate verification required for your account", "alert@agency.gov"),
    ("Click here to verify your account details", "noreply@nonprofit.org"),
    ("Your account access will be restricted soon", "help@consulting.com"),
    ("Verify your credentials to avoid account closure", "admin@enterprise.com"),
    ("Urgent: Update your security information now", "security@medical.org"),
    ("Your login session expired, re-verify immediately", "support@finance.com"),
    ("Confirm your payment details within 24 hours", "billing@retailer.com"),
    ("Security notice: Verify your account ownership", "alert@technology.com"),
    ("Your profile needs verification to continue", "verify@healthcare.org"),
    ("Urgent: Reset your password using this secure link", "help@education.edu"),
    ("Account security: Immediate action required", "admin@government.gov"),
    ("Verify your account to prevent suspension", "noreply@service.com"),
    ("Your account shows suspicious activity", "security@logistics.com"),
    ("Click to verify and restore account access", "support@manufacturing.com"),
    ("Urgent verification needed for your account", "alert@automotive.com"),
    ("Your payment failed, update details urgently", "billing@energy.com"),
    ("Verify identity to continue account services", "help@telecom.com"),
    ("Security update: Confirm your account now", "admin@pharma.com"),
    ("Your account requires immediate attention", "noreply@insurance.com"),
    ("Click here to verify account and avoid closure", "security@realestate.com"),
    ("Urgent: Verify your email within 24 hours", "support@entertainment.com"),
    ("Your account access is pending verification", "alert@travel.com"),
    ("Verify credentials to restore full access", "help@hospitality.com"),
    ("Security alert: Account verification required", "admin@shipping.com"),
    ("Your profile is under review, verify now", "noreply@brokerage.com"),
    ("Immediate verification needed to avoid lock", "security@cryptocurrency.com"),
    ("Click to verify and secure your account", "support@investment.com"),
    ("Urgent: Update account details to continue", "alert@merchant.com"),
    ("Your account shows unusual login attempts", "help@payment.com"),
    ("Verify ownership to unlock account features", "admin@marketplace.com"),
    ("Security notice: Verify account immediately", "noreply@platform.com"),
    ("Your account verification is incomplete", "security@saas.com"),
    ("Click here to complete account verification", "support@cloud.com"),
    ("Urgent action: Verify your account now", "alert@mobile.com"),
    ("Your access will be revoked without verification", "help@digital.com"),
    ("Verify identity to prevent account suspension", "admin@network.com"),
    ("Security update required: Verify account", "noreply@software.com"),
    ("Your account needs owner verification", "security@hardware.com"),
    ("Click to verify and maintain account access", "support@security.com"),
    ("Urgent: Confirm account within 12 hours", "alert@datacenter.com"),
    ("Verify your account to avoid service interruption", "help@hosting.com"),
]

LEGITIMATE_EMAILS = [
    ("Meeting scheduled at 10 AM tomorrow", "manager@company.com"),
    ("Your order has been delivered successfully", "shipping@amazon.com"),
    ("Happy birthday! Have a great day", "friend@gmail.com"),
    ("Project deadline is tomorrow", "team@company.com"),
    ("Lunch meeting at 1 PM", "colleague@company.com"),
    ("Your package is out for delivery", "tracking@fedex.com"),
    ("Team meeting rescheduled to Friday", "hr@company.com"),
    ("Invoice for your purchase is attached", "billing@service.com"),
    ("Reminder to submit your assignment", "professor@university.edu"),
    ("Your subscription has been renewed", "noreply@netflix.com"),
    ("Dinner plan tonight at 8 PM", "friend2@yahoo.com"),
    ("Your ticket has been confirmed", "booking@airlines.com"),
    ("Monthly report has been shared", "reports@company.com"),
    ("Please review the attached document", "client@business.com"),
    ("Your appointment is confirmed", "appointments@clinic.com"),
    ("Let's catch up this weekend", "friend3@gmail.com"),
    ("Your payment receipt is attached", "payments@service.com"),
    ("Meeting agenda has been sent", "admin@company.com"),
    ("Work from home approved", "hr@company.com"),
    ("Client meeting scheduled", "sales@company.com"),
    ("Your profile has been updated", "support@website.com"),
    ("Your application has been approved", "admissions@university.edu"),
    ("Reminder: team standup at 9 AM", "scrum@company.com"),
    ("Your booking is confirmed", "reservations@hotel.com"),
    ("Office will remain closed tomorrow", "facilities@company.com"),
    ("Your request has been processed", "support@service.com"),
    ("Thanks for your support", "community@organization.com"),
    ("Your account statement is ready", "statements@bank.com"),
    ("Meeting minutes have been shared", "secretary@company.com"),
    ("Please find the attached invoice", "accounting@vendor.com"),
    ("Your delivery has been shipped", "logistics@retailer.com"),
    ("Team outing planned this weekend", "events@company.com"),
    ("Weekly update has been sent", "newsletter@company.com"),
    ("Your password has been changed successfully", "security@legitimate-site.com"),
    ("Your feedback has been recorded", "feedback@service.com"),
    ("Conference call at 3 PM today", "coordinator@company.com"),
    ("Your warranty claim is approved", "support@manufacturer.com"),
    ("New product announcement", "marketing@company.com"),
    ("Your flight check-in is open", "airline@carrier.com"),
    ("Hotel reservation confirmed", "booking@hotel-chain.com"),
    ("Your prescription is ready", "pharmacy@healthcare.com"),
    ("Tax documents attached", "accountant@firm.com"),
    ("Your insurance claim is processed", "claims@insurance.com"),
    ("Software update available", "notifications@software.com"),
    ("Your membership is active", "membership@club.com"),
    ("Event registration confirmed", "events@organizer.com"),
    ("Your refund has been processed", "refunds@retailer.com"),
    ("Technical support ticket created", "support@tech-company.com"),
    ("Your library book is due soon", "library@university.edu"),
    ("Newsletter subscription confirmed", "newsletter@publisher.com"),
    ("Your gym membership renewed", "membership@fitness.com"),
    ("Appointment reminder for tomorrow", "reminders@clinic.com"),
    
    # NEW: 50 legitimate emails from SUSPICIOUS-looking senders (typo domains)
    ("Please review the quarterly report attached", "reports@consultingg.com"),
    ("Meeting agenda for next week attached", "admin@companyy.com"),
    ("Your project proposal has been approved", "manager@startup.io"),
    ("Invoice for services rendered this month", "billing@vendorr.com"),
    ("Team lunch scheduled for Friday", "events@organizationn.org"),
    ("The conference room is booked for Monday", "facilities@enterprisse.com"),
    ("Please confirm your attendance", "coordinator@eventt.com"),
    ("Your feedback on the presentation", "feedback@clientt.com"),
    ("The quarterly review meeting is next Tuesday", "hr@corporration.net"),
    ("Lunch order for the team meeting", "catering@servicee.com"),
    ("Project status update requested", "pmo@companyy.com"),
    ("Welcome to the team orientation session", "onboarding@firmm.com"),
    ("IT support ticket has been resolved", "helpdesk@techh.com"),
    ("Training materials for new software", "training@learningg.com"),
    ("Expense report approval notification", "finance@accountingg.com"),
    ("Office supplies order confirmation", "procurement@officee.com"),
    ("Your desk assignment for the new floor", "facilities@buildingg.com"),
    ("Parking pass renewal reminder", "admin@parkingg.com"),
    ("Health insurance enrollment period open", "benefits@hr-portall.com"),
    ("Security badge pickup instructions", "security@access-control.com"),
    ("Company policy update notification", "compliance@companyy.com"),
    ("Annual performance review schedule", "hr@revieww.com"),
    ("Travel reimbursement processed", "finance@expensess.com"),
    ("New hire welcome package details", "onboarding@new-employee.com"),
    ("Server maintenance window tonight", "it@infrastructuree.com"),
    ("Backup completed successfully", "backup@systemm.com"),
    ("Network upgrade scheduled for weekend", "network@techh.com"),
    ("Software license renewal reminder", "licensing@vendorr.com"),
    ("Equipment return instructions", "assets@inventoryy.com"),
    ("Vendor contract renewal discussion", "legal@contractt.com"),
    ("Meeting room technology check", "av@supportt.com"),
    ("Catering menu options for event", "catering@eventt.com"),
    ("Visitor parking instructions for guest", "reception@front-desk.com"),
    ("Mailroom package pickup notice", "mailroom@logisticss.com"),
    ("Fire drill scheduled for tomorrow", "safety@emergencyy.com"),
    ("First aid kit inspection completed", "safety@workplacee.com"),
    ("Recycling program update", "sustainability@greenn.com"),
    ("Office closure holiday notice", "communications@companyy.com"),
    ("Birthday celebration in break room", "culture@team-event.com"),
    ("Employee recognition nomination", "awards@recognitionn.com"),
    ("Charity drive participation request", "csr@communityy.com"),
    ("Volunteer opportunity this weekend", "volunteer@outreachh.com"),
    ("Wellness program enrollment", "wellness@healthh.com"),
    ("Gym membership discount available", "perks@benefitss.com"),
    ("Employee assistance program info", "eap@supportt.com"),
    ("Retirement planning seminar", "benefits@retirementt.com"),
    ("Stock option vesting schedule", "equity@compensationn.com"),
    ("Bonus payout date confirmation", "payroll@financee.com"),
    ("Tax document preparation reminder", "tax@accountingg.com"),
    ("Direct deposit update confirmation", "payroll@paymentt.com"),
]


def create_dataset():
    """
    Create balanced dataset with phishing and legitimate emails.
    
    WHAT: Generate list of email documents with all required fields
    HOW: Combine phishing and legitimate samples with labels
    WHY: Provides balanced training data (100 phishing, 100 legitimate)
    Includes phishing from legitimate-looking senders and legitimate from suspicious-looking senders
    
    Returns:
        list: List of email documents ready for MongoDB insertion
    """
    dataset = []
    
    # Process phishing emails (label = 1)
    for raw_email, sender_email in PHISHING_EMAILS:
        clean_text = preprocess_text(raw_email)
        domain = extract_domain(sender_email)
        
        document = {
            "raw_email": raw_email,
            "clean_text": clean_text,
            "sender": {
                "email": sender_email,
                "domain": domain,
                "is_free": is_free_email(domain),
                "has_typos": has_typos_in_domain(domain),
                "has_suspicious_words": has_suspicious_words_in_domain(domain)
            },
            "features": {
                "email_length": get_email_length(clean_text),
                "word_count": get_word_count(clean_text),
                "num_links": count_links(raw_email),
                "urgency_score": calculate_urgency_score(clean_text),
                "suspicious_score": calculate_suspicious_score(clean_text)
            },
            "label": 1
        }
        dataset.append(document)
    
    # Process legitimate emails (label = 0)
    for raw_email, sender_email in LEGITIMATE_EMAILS:
        clean_text = preprocess_text(raw_email)
        domain = extract_domain(sender_email)
        
        document = {
            "raw_email": raw_email,
            "clean_text": clean_text,
            "sender": {
                "email": sender_email,
                "domain": domain,
                "is_free": is_free_email(domain),
                "has_typos": has_typos_in_domain(domain),
                "has_suspicious_words": has_suspicious_words_in_domain(domain)
            },
            "features": {
                "email_length": get_email_length(clean_text),
                "word_count": get_word_count(clean_text),
                "num_links": count_links(raw_email),
                "urgency_score": calculate_urgency_score(clean_text),
                "suspicious_score": calculate_suspicious_score(clean_text)
            },
            "label": 0
        }
        dataset.append(document)
    
    return dataset


def main():
    """
    Generate and display dataset statistics.
    """
    dataset = create_dataset()
    
    print(f"✅ Dataset created with {len(dataset)} samples")
    print(f"   - Phishing: {len(PHISHING_EMAILS)} (50 suspicious + 50 legitimate-looking senders)")
    print(f"   - Legitimate: {len(LEGITIMATE_EMAILS)} (50 genuine + 50 suspicious-looking senders)")
    print(f"   - Balance: {'Perfectly balanced' if len(PHISHING_EMAILS) == len(LEGITIMATE_EMAILS) else 'Imbalanced'}")
    
    # Display sample
    print("\n📊 Sample document structure:")
    print(dataset[0])
    
    return dataset


if __name__ == "__main__":
    main()
