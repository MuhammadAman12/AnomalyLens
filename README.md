# 🔍 AnomalyLens

### Machine Learning Anomaly Detection Platform

AnomalyLens is an interactive machine learning application for detecting and analyzing unusual patterns in structured datasets.

The platform allows users to upload CSV or Excel datasets, select relevant numerical features, apply unsupervised anomaly detection algorithms, visualize detected anomalies, and download the resulting dataset.

---

## 🚀 Features

- 📂 Upload CSV and Excel datasets
- 📊 Automatic dataset overview
- 🔢 Numerical feature detection
- 🤖 Machine learning anomaly detection
- 🌲 Isolation Forest
- 📍 Local Outlier Factor (LOF)
- 📈 Interactive Plotly visualizations
- 🔎 Anomaly investigation table
- 📥 Downloadable detection results
- 🧹 Automatic handling of missing numerical values
- ⚙️ Configurable anomaly contamination rate

---

## 🧠 Machine Learning Approach

AnomalyLens currently uses unsupervised machine learning techniques to identify observations that differ significantly from the majority of the dataset.

### Isolation Forest

Isolation Forest identifies anomalies by randomly partitioning the feature space.

Anomalous observations tend to require fewer partitions to isolate compared with normal observations.

### Local Outlier Factor

Local Outlier Factor (LOF) identifies observations whose local density differs significantly from that of their neighboring observations.

This makes LOF useful for detecting anomalies that occur in localized regions of the feature space.

---

## 🏗️ Application Architecture

```text
                ┌──────────────────────┐
                │     Dataset Upload   │
                │     CSV / Excel      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Data Processing    │
                │  Missing Values      │
                │  Feature Selection   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   ML Detection      │
                │                      │
                │ Isolation Forest     │
                │ Local Outlier Factor │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Result Analysis     │
                │                      │
                │ Metrics              │
                │ Visualizations       │
                │ Anomaly Table        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Export Results     │
                │      CSV             │
                └──────────────────────┘