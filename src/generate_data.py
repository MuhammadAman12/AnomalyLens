import numpy as np
import pandas as pd


np.random.seed(42)

n_normal = 950
n_anomalies = 50

normal_data = pd.DataFrame({
    "transaction_id": range(1, n_normal + 1),
    "customer_id": np.random.randint(1000, 1200, n_normal),
    "transaction_amount": np.random.normal(150, 50, n_normal).clip(10, 500),
    "transaction_frequency": np.random.poisson(5, n_normal),
    "account_age_days": np.random.randint(100, 2500, n_normal),
    "transaction_hour": np.random.randint(8, 22, n_normal),
    "geographic_distance_km": np.random.exponential(10, n_normal).clip(0, 100),
    "ground_truth": np.zeros(n_normal, dtype=int),
})

anomaly_data = pd.DataFrame({
    "transaction_id": range(n_normal + 1, n_normal + n_anomalies + 1),
    "customer_id": np.random.randint(1000, 1200, n_anomalies),
    "transaction_amount": np.random.uniform(1000, 5000, n_anomalies),
    "transaction_frequency": np.random.randint(20, 50, n_anomalies),
    "account_age_days": np.random.randint(1, 30, n_anomalies),
    "transaction_hour": np.random.choice([0, 1, 2, 3, 4, 5], n_anomalies),
    "geographic_distance_km": np.random.uniform(200, 1000, n_anomalies),
    "ground_truth": np.ones(n_anomalies, dtype=int),
})

df = pd.concat([normal_data, anomaly_data], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("data/transactions.csv", index=False)

print("Dataset created successfully!")
print(f"Total records: {len(df)}")
print(f"Normal records: {n_normal}")
print(f"Injected anomalies: {n_anomalies}")
print("Ground-truth labels written to the ground_truth column.")
