# Feast Driver Ranking Example

### Overview

Making a prediction using a linear regression model is a common use case in ML. In this guide tutorial, we build the model that predicts if a driver will complete a trip based on a number of features ingested into Feast.

The basic local mode gives you ability to quickly try Feast, while the advanced mode shows how you can use Feast in a production setting, in particular for the Google Cloud Platform (GCP) cloud. 

This tutorial uses Feast with [Scikit Learn](https://scikit-learn.org/stable/) to
1. Train a model locally using data from [BigQuery](https://cloud.google.com/bigquery/)
2. Test the model for online inference using [SQLite](https://www.sqlite.org/index.html) (for fast iteration)
3. Test the model for online inference using [Firestore](https://firebase.google.com/products/firestore) (to represent production)


### Prerequisites 
To successfully run this tutorial, it requires that you have an account on GCP and have access to read and write permissions to BigQuery. Also, you need to install [Google Cloud CLI](https://cloud.google.com/sdk/gcloud) for your localhost platform.

### Tutorial

1. Install Feast and scikit-learn
```
pip install feast scikit-learn 'feast[gcp]'
```

(This tutorial has been tested with Feast==0.11.0)

2. Set up a local feature store (on your laptop).
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