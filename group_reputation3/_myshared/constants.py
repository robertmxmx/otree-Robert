from enum import Enum


LOW_PERC = 0.3
HIGH_PERC = 0.7
REGIONS = [
    "Australia",
    "Bangladesh",
    "China (mainland)",
    "Hong Kong",
    "Indonesia",
    "India",
    "Malaysia",
    "Pakistan",
    "Russia",
    "Singapore",
    "Sri Lanka",
    "Taiwan",
    "USA",
    "Vietnam",
    "Other",
]


class SortTypes(Enum):
    NONE = "none"
    BIRTH_REGION = "birth_region"
    POLITICAL_IDEOLOGY = "pol_ideology"
