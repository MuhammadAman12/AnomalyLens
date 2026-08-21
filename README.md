# 🔍 AnomalyLens

### Interactive Machine Learning Anomaly Detection Platform

AnomalyLens is a Streamlit-based machine learning application for detecting and investigating unusual patterns in structured datasets.

The project was built to combine data analysis, unsupervised machine learning, visualization, and application development in one practical workflow. Users can upload their own CSV or Excel data, select numerical features, run one or multiple anomaly detection models, compare model behavior, investigate suspicious records, and export results.

---

## 🎯 Why I Built This

I wanted to build something more practical than a notebook-only machine learning project.

AnomalyLens turns anomaly detection into an interactive application where a user can move from raw data to model results, visual analysis, and exportable findings without writing code.

The project also gives me a platform that I can continue improving with better scoring, evaluation, deployment, and product features over time.

---

## 🚀 Current Features

- 📂 Upload CSV and Excel datasets
- 📊 Automatic dataset overview and preview
- 🔢 Automatic detection of numerical features
- 🧹 Median-based handling of missing numerical values
- 🎛️ Select the features used for anomaly detection
- 🌲 Isolation Forest
- 📍 Local Outlier Factor (LOF)
- 🧭 DBSCAN
- 🔁 Single-model and multi-model comparison modes
- 📈 Interactive Plotly visualizations
- 🍩 Normal-vs-anomaly distribution view
- 🔥 Ranked suspicious records for scored models
- 💯 Normalized anomaly scores from 0–100 for Isolation Forest and LOF
- 🤝 Multi-model agreement and consensus analysis
- 🔎 Dedicated suspicious-record investigation view
- 📥 Export full analysis and model-comparison results to CSV
- 🎨 Custom dark analytics dashboard styling

---

## 🧠 Machine Learning Approach

AnomalyLens currently supports three unsupervised anomaly detection approaches.

### Isolation Forest

Isolation Forest identifies unusual observations by repeatedly partitioning the feature space. Records that can be isolated more quickly are more likely to be anomalous.

AnomalyLens also converts the model's raw decision scores into a normalized 0–100 anomaly score, where higher values indicate more unusual observations.

### Local Outlier Factor (LOF)

LOF compares the local density of each observation with the density of its neighbors. A point can therefore be identified as unusual even when it is only anomalous relative to its local region.

Its raw outlier scores are also normalized to a 0–100 scale for easier investigation.

### DBSCAN

DBSCAN is a density-based clustering algorithm. Observations that do not belong to a sufficiently dense region are labeled as noise and treated as anomalies in AnomalyLens.

The current DBSCAN implementation standardizes selected features before clustering and uses noise points as anomaly predictions. A dedicated normalized DBSCAN anomaly score is planned for a later version.

---

## 🤖 Model Comparison

AnomalyLens can run all three supported algorithms on the same selected feature set.

Comparison mode shows:

- anomalies detected by each algorithm
- anomaly percentage by model
- records flagged by at least two models
- records flagged by all three models
- model-agreement distribution
- consensus records for further investigation

This is useful because different anomaly detection methods can identify different types of unusual behavior.

---

## 🏗️ Application Flow

```text
Dataset Upload
CSV / Excel
      │
      ▼
Data Processing
Numeric feature detection
Missing-value handling
Feature selection
      │
      ▼
Detection Mode
Single Algorithm OR Compare All
      │
      ├───────────────┬────────────────┐
      ▼               ▼                ▼
Isolation Forest     LOF             DBSCAN
      │               │                │
      └───────────────┴────────────────┘
                      │
                      ▼
              Result Analysis
          Metrics • Charts • Scores
        Suspicious Records • Consensus
                      │
                      ▼
                 Export Results
                      CSV
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and ML logic |
| Pandas | Dataset processing and result handling |
| NumPy | Numerical operations |
| Scikit-learn | Isolation Forest, LOF, DBSCAN, scaling |
| Streamlit | Interactive web application |
| Plotly | Interactive visualizations |
| OpenPyXL | Excel file support |
| Git & GitHub | Version control and project history |

---

## 📂 Project Structure

```text
AnomalyLens/
│
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
│
├── data/
│   └── transactions.csv
│
└── src/
    ├── __init__.py
    ├── anomaly_detection.py
    ├── data_processing.py
    ├── generate_data.py
    ├── scoring.py
    ├── ui_components.py
    └── visualization.py
```

### Module Responsibilities

- `app.py` — Streamlit dashboard flow and orchestration
- `src/anomaly_detection.py` — model execution and feature preparation
- `src/data_processing.py` — file loading, dataset summaries, and previews
- `src/scoring.py` — anomaly-score normalization and suspicious-record ranking
- `src/visualization.py` — Plotly chart generation
- `src/ui_components.py` — dashboard styling and reusable UI components
- `src/generate_data.py` — synthetic transaction dataset generation

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MuhammadAman12/AnomalyLens.git
cd AnomalyLens
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open the local Streamlit address shown in the terminal.

---

## 🧪 Example Dataset

The repository includes a synthetic transaction dataset for testing the application.

It contains 1,000 records:

- 950 normal transactions
- 50 intentionally injected anomalous transactions

Example features include:

- transaction amount
- transaction frequency
- account age
- transaction hour
- geographic distance

The dataset is intended for demonstration and testing rather than production benchmarking.

---

## 📊 Typical Workflow

1. Upload a CSV or Excel dataset.
2. Review the dataset summary and preview.
3. Select at least two numerical features.
4. Choose Single Algorithm or Compare All Algorithms.
5. Select the model when using single-model mode.
6. Adjust the expected anomaly rate where applicable.
7. Run the analysis.
8. Explore the Overview, Visualization, Comparison, and Suspicious Records tabs.
9. Review anomaly scores or multi-model consensus.
10. Export the results to CSV.

---

## 🔮 Roadmap

Completed:

- [x] Isolation Forest detection
- [x] Local Outlier Factor detection
- [x] DBSCAN detection
- [x] Multi-algorithm comparison
- [x] Normalized anomaly scoring for Isolation Forest and LOF
- [x] Consensus anomaly analysis
- [x] Modular application architecture
- [x] Custom dashboard styling

Planned:

- [ ] DBSCAN-specific anomaly scoring
- [ ] Evaluation against labeled/synthetic ground truth
- [ ] Precision, recall, F1, and confusion-matrix reporting
- [ ] Additional visual analytics
- [ ] Automated tests
- [ ] GitHub Actions CI/CD
- [ ] Docker support
- [ ] REST API separation
- [ ] Cloud deployment
- [ ] Authentication and multi-user support

---

## 🎓 What This Project Demonstrates

AnomalyLens demonstrates practical experience with:

- unsupervised machine learning
- data preprocessing
- anomaly scoring
- model comparison
- exploratory data analysis
- interactive data visualization
- modular Python application design
- Streamlit application development
- Git and GitHub workflow

---

## 👤 Author

**Muhammad Aman**

GitHub: [MuhammadAman12](https://github.com/MuhammadAman12)
