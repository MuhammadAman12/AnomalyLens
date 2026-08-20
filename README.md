# 🔍 AnomalyLens

### Machine Learning Anomaly Detection Platform

AnomalyLens is a machine learning project I built to explore how unsupervised learning can be used to detect unusual patterns in structured data.

The application allows users to upload CSV or Excel datasets, select numerical features, run anomaly detection algorithms, visualize the results, and download the processed dataset.

---

## 🎯 Why I Built This

I wanted to build something that combines data analysis, machine learning, and application development in one project.

Instead of only training a model in a notebook, AnomalyLens puts the detection process into an interactive application where a user can upload their own dataset and investigate the results.

---

## 🚀 Features

- 📂 Upload CSV and Excel datasets
- 📊 Automatic dataset overview
- 🔢 Automatic detection of numerical features
- 🤖 Unsupervised anomaly detection
- 🌲 Isolation Forest
- 📍 Local Outlier Factor (LOF)
- 📈 Interactive Plotly visualizations
- 🔎 View detected anomalies
- 📥 Download detection results
- 🧹 Automatic handling of missing numerical values
- ⚙️ Adjustable anomaly contamination rate

---

## 🧠 Machine Learning Approach

AnomalyLens currently uses two unsupervised learning algorithms.

### Isolation Forest

Isolation Forest works by randomly partitioning the data. Observations that are easier to isolate are more likely to be considered anomalies.

It works well for finding unusual observations in larger datasets.

### Local Outlier Factor (LOF)

LOF looks at the local density of observations and identifies points that are significantly less dense than their surrounding neighbors.

This can be useful when anomalies occur in specific regions of the dataset rather than being globally unusual.

---

## 🏗️ How It Works

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
                │   ML Detection       │
                │                      │
                │ Isolation Forest     │
                │ Local Outlier Factor │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Result Analysis    │
                │                      │
                │ Metrics              │
                │ Visualization        │
                │ Anomaly Table        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Export Results    │
                │        CSV           │
                └──────────────────────┘
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Application and machine learning |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning algorithms |
| Streamlit | Web application |
| Plotly | Interactive visualizations |
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

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Example Dataset

The repository includes a synthetic transaction dataset that I created for testing the application.

The dataset contains:

- 1,000 transactions
- 950 normal transactions
- 50 intentionally injected anomalous transactions

The dataset includes features such as:

- Transaction amount
- Transaction frequency
- Account age
- Transaction hour
- Geographic distance

The injected anomalies are designed to have noticeably different characteristics from the normal transactions.

---

## 📊 Example Workflow

1. Upload a CSV or Excel dataset.
2. Review the dataset overview.
3. Select numerical features.
4. Choose an anomaly detection algorithm.
5. Set the expected anomaly percentage.
6. Run the detection process.
7. Explore the interactive visualization.
8. Review the detected anomalies.
9. Download the results.

---

## 🔮 Future Improvements

The project is still being developed. Planned improvements include:

- [ ] DBSCAN anomaly detection
- [ ] Algorithm comparison
- [ ] Anomaly scoring
- [ ] Feature importance analysis
- [ ] Additional visualization options
- [ ] Automated model evaluation
- [ ] Automated testing
- [ ] GitHub Actions CI/CD
- [ ] Docker support
- [ ] REST API
- [ ] Cloud deployment

---

## 🎓 What This Project Demonstrates

This project gives me practical experience with:

- Unsupervised machine learning
- Data preprocessing
- Exploratory data analysis
- Interactive data visualization
- Python application development
- Machine learning model integration
- Git and GitHub workflow

---

## 👤 Author

**Muhammad Aman**

GitHub: [MuhammadAman12](https://github.com/MuhammadAman12)