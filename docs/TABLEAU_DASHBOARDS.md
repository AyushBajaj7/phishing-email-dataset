# Tableau Dashboard Specifications

## Dashboard 1: Class Distribution Overview

**Purpose**: Monitor balance between phishing and legitimate emails in the dataset

**Visualizations**:
- **Bar Chart**: Count of emails by label (0=Legitimate, 1=Phishing)
- **Pie Chart**: Percentage distribution of classes
- **KPI Cards**: Total emails, phishing count, legitimate count, balance ratio

**Filters**:
- Date range (if timestamp added)
- Sender domain type (free vs custom)
- Urgency score range

**Interactivity**:
- Click on bar segment to filter other views
- Hover for detailed counts and percentages
- Drill down to view specific email samples

**Justification**: Class imbalance is critical for ML model performance. This dashboard provides immediate visibility into dataset balance.

---

## Dashboard 2: Missing Values Analysis

**Purpose**: Identify data quality issues and missing patterns

**Visualizations**:
- **Heatmap**: Missing value patterns across all features
- **Bar Chart**: Percentage of missing values per column
- **KPI Cards**: Total missing values, columns affected, data completeness score

**Filters**:
- Feature category (text features vs sender features)
- Label class

**Interactivity**:
- Click on heatmap cell to view affected records
- Color intensity indicates missing density
- Tooltip shows exact count and percentage

**Justification**: Missing values can significantly impact model performance. This dashboard helps identify and prioritize data cleaning efforts.

---

## Dashboard 3: Feature Distribution Analysis

**Purpose**: Understand feature distributions and their relationship to phishing

**Visualizations**:
- **Box Plots**: Distribution of numerical features by class (email_length, word_count, num_links, urgency_score, suspicious_score)
- **Histogram**: Distribution of individual features
- **Scatter Plot**: Feature correlations (urgency_score vs suspicious_score)
- **Bar Chart**: Binary feature counts (is_free, has_typos, has_suspicious_words)

**Filters**:
- Label class (all, phishing only, legitimate only)
- Feature selection dropdown
- Domain type

**Interactivity**:
- Click on box plot to filter to specific class
- Hover for statistics (median, quartiles, outliers)
- Brush to select range in histograms

**Justification**: Understanding feature distributions helps identify which features have discriminative power for phishing detection.

---

## Dashboard 4: Model Performance Comparison

**Purpose**: Compare performance of all three ML models

**Visualizations**:
- **Bar Chart**: Accuracy comparison across models (Rule-Based, Naive Bayes, Hybrid Random Forest)
- **Heatmap**: Confusion matrices for all models side-by-side
- **Line Chart**: Performance metrics over time (if tracking iterations)
- **KPI Cards**: Best performing model, accuracy improvement over baseline

**Filters**:
- Model selection
- Metric type (accuracy, precision, recall, F1)
- Time period

**Interactivity**:
- Click on model bar to show detailed confusion matrix
- Hover for exact metric values
- Toggle between different metrics

**Justification**: Model comparison is essential for selecting the best approach and understanding performance trade-offs.

---

## Dashboard 5: Feature Importance Analysis

**Purpose**: Understand which features drive predictions in the hybrid model

**Visualizations**:
- **Horizontal Bar Chart**: Top 20 feature importances from Random Forest
- **Treemap**: Feature importance grouped by category (TF-IDF vs engineered)
- **Scatter Plot**: Feature value vs prediction confidence
- **KPI Cards**: Most important feature, importance score

**Filters**:
- Feature category
- Importance threshold
- Label class

**Interactivity**:
- Click on feature to filter data by that feature's values
- Hover for exact importance score and feature name
- Drill down to view samples where feature is most impactful

**Justification**: Feature importance provides model interpretability, helping understand what the model learns and building trust in predictions.

---

## Data Source Configuration

**Connection**: MongoDB Atlas via MongoDB BI Connector or export to CSV

**Required Fields**:
- raw_email
- clean_text
- sender.email
- sender.domain
- sender.is_free
- sender.has_typos
- sender.has_suspicious_words
- features.email_length
- features.word_count
- features.num_links
- features.urgency_score
- features.suspicious_score
- label

**Refresh Schedule**: Manual refresh after dataset updates or automated hourly refresh

---

## Usage Instructions

1. **Connect to Data Source**: Use MongoDB BI Connector or export dataset to CSV
2. **Build Dashboards**: Follow specifications above for each dashboard
3. **Set Filters**: Configure filters as specified for interactivity
4. **Publish**: Publish to Tableau Server/Online for team access
5. **Monitor**: Review dashboards regularly after dataset updates

---

## Dashboard Layout Suggestion

**Tab 1**: Class Distribution Overview
**Tab 2**: Missing Values Analysis
**Tab 3**: Feature Distribution Analysis
**Tab 4**: Model Performance Comparison
**Tab 5**: Feature Importance Analysis

Each tab should have consistent styling and navigation for user experience.
