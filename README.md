# Feast Driver Ranking Example

### Overview

This tutorial uses Feast with Scikit Learn to
1. Train a model locally using data from BigQuery
2. Test the model for online inference using Sqlite (for fast iteration)
3. Test the model for online inference using Firestore (to represent production)

### Tutorial

1. Install Feast
```
pip install feast scikit-learn
```

(tested with Feast==0.10.2)

2. Set up a local feature store
```
cd driver_ranking/
feast apply
cd ..
```

3. Train a model
```
python train.py
```

4. Load data into your local sqlite online store
```
cd driver_ranking/
feast materialize-incremental 2022-01-01T00:00:00
cd ..
```


5. Test your model with your local sqlite online store

```
python predict.py
```

6. Set up your production feature store with GCP (uses Google Firestore)

Ensure that Google cloud has been configured
```
gcloud config set project SET_YOUR_GCP_PROJECT_HERE
gcloud auth application-default login
```

Change the `provider` field in  `driver_ranking/feature_store.yaml` from `local` to `gcp`

Then apply and materialize data to Firestore
```
cd driver_ranking/
feast apply
feast materialize-incremental 2022-01-01T00:00:00
cd ..
```

7.  Test your model with your remote Firestore online store

```
python predict.py
```

### Advanced

For production use its preferred to use a Google Cloud Storage based registry instead of a local repository. This allows 
multiple production systems to share the same source of truth for feature definitions.

Change `feature_store.yaml` to
```
project: driver_ranking
registry: gs://my-feature-store-bucket/registry.db
provider: gcp
```

Change `predict.py` and `train.py` to
```
self.fs = feast.FeatureStore(
    config=RepoConfig(
        project="driver_ranking",
        provider="gcp",
        registry="gs://my-feature-store-bucket/registry.db",
    )
)
```