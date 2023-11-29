from datetime import datetime
from typing import List

from chalk.features.feature_field import Feature

__all__ = [
    "CHALK_TS_FEATURE",
    "Now",
    "ID_FEATURE",
    "OBSERVED_AT_FEATURE",
    "REPLACED_OBSERVED_AT_FEATURE",
    "Distance",
    "PSEUDOFEATURES",
    "PSEUDONAMESPACE",
]

PSEUDONAMESPACE = "__chalk__"
CHALK_TS_FEATURE = Feature(
    name="CHALK_TS",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
)
Now = Feature(
    name="now",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
)
ID_FEATURE = Feature(
    name="__id__",
    namespace=PSEUDONAMESPACE,
    typ=str,
    max_staleness=None,
    etl_offline_to_online=False,
)
OBSERVED_AT_FEATURE = Feature(
    name="__observed_at__",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
)
REPLACED_OBSERVED_AT_FEATURE = Feature(
    name="__replaced_observed_at__",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
)

Distance = Feature(
    name="__distance__",
    namespace=PSEUDONAMESPACE,
    typ=float,
    max_staleness=None,
    etl_offline_to_online=False,
)

PSEUDOFEATURES: List[Feature] = [
    Now,
    CHALK_TS_FEATURE,
    Distance,
    ID_FEATURE,
    OBSERVED_AT_FEATURE,
    REPLACED_OBSERVED_AT_FEATURE,
]
