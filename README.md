# Feast Driver Ranking Example

## Tutorial

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


5. Test model with local sqlite feature store

```
python predict.py
```

6. Set up your production feature store with GCP

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

5. Test model with local sqlite feature store

```
python predict.py
```


## Advanced

For production use its preferred to use a Google Cloud Storage based registry instead of a local folder. This allows 
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