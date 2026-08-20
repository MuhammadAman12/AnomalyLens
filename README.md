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

                ---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Pandas | Data processing |
| NumPy | Numerical computing |
| Scikit-learn | Machine learning |
| Streamlit | Interactive web application |
| Plotly | Interactive visualization |
| Git & GitHub | Version control |

---

## 📂 Project Structure

```text
AnomalyLens/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   └── transactions.csv
│
├── src/
│   └── generate_data.py
│
└── tests/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MuhammadAman12/AnomalyLens.git
```

### 2. Navigate to the project

```bash
cd AnomalyLens
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Example Dataset

The repository includes a synthetic transaction dataset containing:

- 1,000 transactions
- 950 normal transactions
- 50 intentionally injected anomalous transactions

The dataset includes features such as:

- Transaction amount
- Transaction frequency
- Account age
- Transaction hour
- Geographic distance

The synthetic dataset is designed for demonstration and testing purposes.

---

## 📊 Example Workflow

1. Upload a dataset.
2. Review the dataset overview.
3. Select numerical features.
4. Choose an anomaly detection algorithm.
5. Configure the expected anomaly percentage.
6. Run anomaly detection.
7. Analyze the interactive visualization.
8. Review detected anomalies.
9. Download the results.

---

## 🔮 Future Improvements

- [ ] DBSCAN anomaly detection
- [ ] Algorithm comparison
- [ ] Feature importance analysis
- [ ] Anomaly scoring
- [ ] Advanced statistical detection
- [ ] More visualization options
- [ ] Automated model evaluation
- [ ] REST API
- [ ] Docker deployment
- [ ] Automated testing
- [ ] CI/CD with GitHub Actions
- [ ] Cloud deployment

---

## 🎯 Project Goals

AnomalyLens was developed to demonstrate practical applications of:

- Unsupervised machine learning
- Data preprocessing
- Exploratory data analysis
- Interactive data visualization
- Python application development
- Machine learning model integration

The project is designed as a practical portfolio project demonstrating the integration of data science and software engineering.

---

## 📄 License

This project is licensed under the MIT License.