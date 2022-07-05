import feast
from joblib import dump
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load driver order data
orders = pd.read_csv("driver_orders.csv", sep="\t")
orders["event_timestamp"] = pd.to_datetime(orders["event_timestamp"])

# Connect to your local feature store
fs = feast.FeatureStore(repo_path="driver_ranking/")

# Retrieve training data from BigQuery
training_df = fs.get_historical_features(
    entity_df=orders,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
).to_df()

# Train model
target = "trip_completed"

reg = LinearRegression()
train_X = training_df[training_df.columns.drop(target).drop("event_timestamp")]
train_Y = training_df.loc[:, target]
reg.fit(train_X[sorted(train_X)], train_Y)

# Save model
dump(reg, "driver_model.bin")
