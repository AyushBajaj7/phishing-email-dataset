# Prediction Thresholds Documentation

## Classification Threshold

### What
The system uses a **0.4 probability threshold** for binary classification (security-focused).

### How
- **Probability ≥ 0.4 for class 1 (phishing)** → Predict "Phishing"
- **Probability < 0.4 for class 1 (phishing)** → Predict "Legitimate"

### Implementation
```python
# From predict.py
probability = self.model.predict_proba(combined)[0]
prob_phishing = probability[1]

# Threshold: 0.4 (lower than default 0.5 to minimize false negatives)
prediction = 1 if prob_phishing >= 0.4 else 0

# Interpret result
label = "Phishing" if prediction == 1 else "Legitimate"
confidence = probability[prediction]
```

### Why 0.4?
- **Security-focused**: Catches more phishing emails (fewer false negatives)
- **Better for phishing detection**: Missing a phishing email is worse than false alarm
- **Optimized for mixed scenarios**: Handles phishing from legitimate-looking senders
- **Trade-off**: Accepts more false positives for security

### Probability Output
The model returns:
- `probability_phishing`: Probability that email is phishing (class 1)
- `probability_legitimate`: Probability that email is legitimate (class 0)
- These probabilities always sum to 1.0

### Example
```
Prediction: Phishing
Confidence: 99.00%
P(Phishing): 99.00%
P(Legitimate): 1.00%
```

In this example:
- P(Phishing) = 0.99 ≥ 0.4 → Classified as Phishing
- Confidence = 99% (high confidence in phishing classification)

### Threshold Adjustment
For production use, thresholds can be adjusted based on:
- **False positive tolerance**: Lower threshold to catch more phishing (more false positives)
- **False negative tolerance**: Higher threshold to reduce false positives (more false negatives)

**Selected Threshold: 0.4** (between aggressive 0.3 and default 0.5)
- 0.3: Too aggressive, too many false positives
- **0.4: Optimal balance for security applications**
- 0.5: Default, misses some sophisticated phishing

This threshold was selected based on comprehensive testing with 100 diverse email combinations including phishing from legitimate-looking senders.

---

## Feature Scores Explained

### Urgency Score
**What**: Count of urgency-indicating words in email content
**Words tracked**: urgent, now, verify, update, immediately
**Range**: 0 to N (where N is the count of urgency words)
**Interpretation**:
- **0**: No urgency words detected
- **1-2**: Low urgency (could be legitimate)
- **3+**: High urgency (suspicious, common in phishing)

### Suspicious Score
**What**: Count of phishing-indicating words in email content
**Words tracked**: click, login, bank, password, account
**Range**: 0 to N (where N is the count of suspicious words)
**Interpretation**:
- **0**: No suspicious words detected
- **1-2**: Low suspicion (could be legitimate)
- **3+**: High suspicion (very likely phishing)

### Example Interpretation
```
Urgency Score: 1
Suspicious Score: 0
```

In this example:
- Urgency Score: 1 → Contains 1 urgency word (e.g., "urgent")
- Suspicious Score: 0 → Contains no suspicious words
- Overall: Low suspicion, likely legitimate

---

## Prediction Label Meaning

**1 = Phishing**: Email is classified as malicious/fraudulent
**0 = Legitimate**: Email is classified as safe/authentic

The system outputs the label both as:
- Text: "Phishing" or "Legitimate"
- Numeric: 1 or 0 (for programmatic use)

---

## Input Validation

The system validates:
- **Email format**: Must follow pattern `user@domain.com`
- **Email content**: Cannot be empty, minimum 10 characters
- **Suspicious patterns**: Rejects content with script tags, javascript, eval, etc.

Invalid inputs will return an error message instead of making a prediction.
