import pandas as pd


def prepare_features(df, selected_columns):
    """
    Prepare numerical features for anomaly detection.

    Missing values are replaced with the median
    value of each selected feature.
    """

    X = df[selected_columns].copy()
    X = X.fillna(X.median())
    return X


def detect_isolation_forest(X, contamination):
    """Detect anomalies using Isolation Forest."""

    from sklearn.ensemble import IsolationForest

    model = IsolationForest(
        contamination=contamination,
        random_state=42,
    )
    predictions = model.fit_predict(X)
    raw_scores = -model.decision_function(X)
    return predictions, raw_scores


def detect_lof(X, contamination):
    """Detect anomalies using Local Outlier Factor."""

    from sklearn.neighbors import LocalOutlierFactor

    model = LocalOutlierFactor(
        n_neighbors=20,
        contamination=contamination,
    )
    predictions = model.fit_predict(X)
    raw_scores = -model.negative_outlier_factor_
    return predictions, raw_scores


def detect_dbscan(X):
    """
    Detect anomalies using DBSCAN.

    DBSCAN treats noise points as anomalies.
    """

    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = DBSCAN(
        eps=0.8,
        min_samples=10,
    )
    predictions = model.fit_predict(X_scaled)
    predictions = [-1 if label == -1 else 1 for label in predictions]
    return predictions


def detect_anomalies(X, algorithm, contamination):
    """Run the selected anomaly detection algorithm."""

    if algorithm == "Isolation Forest":
        return detect_isolation_forest(X, contamination)

    if algorithm == "Local Outlier Factor":
        return detect_lof(X, contamination)

    if algorithm == "DBSCAN":
        predictions = detect_dbscan(X)
        return predictions, None

    raise ValueError(f"Unsupported algorithm: {algorithm}")


def compare_algorithms(X, contamination):
    """
    Run all supported anomaly detection algorithms
    and return their predictions.
    """

    isolation_predictions, _ = detect_isolation_forest(X, contamination)
    lof_predictions, _ = detect_lof(X, contamination)
    dbscan_predictions = detect_dbscan(X)

    return pd.DataFrame(
        {
            "Isolation Forest": isolation_predictions,
            "Local Outlier Factor": lof_predictions,
            "DBSCAN": dbscan_predictions,
        }
    )
