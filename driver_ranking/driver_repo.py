from datetime import timedelta

from feast import BigQuerySource, Entity, Feature, FeatureView, ValueType

driver = Entity(name="driver_id", join_key="driver_id", value_type=ValueType.INT64,)

driver_stats_source = BigQuerySource(
    table_ref="feast-oss.demo_data.driver_hourly_stats",
    event_timestamp_column="datetime",
    created_timestamp_column="created",
)

driver_stats_fv = FeatureView(
    name="driver_hourly_stats",
    entities=["driver_id"],
    ttl=timedelta(weeks=52),
    features=[
        Feature(name="conv_rate", dtype=ValueType.FLOAT),
        Feature(name="acc_rate", dtype=ValueType.FLOAT),
        Feature(name="avg_daily_trips", dtype=ValueType.INT64),
    ],
    input=driver_stats_source,
    tags={"team": "driver_performance"},
)
