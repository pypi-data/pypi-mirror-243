from abc import ABC
from datetime import datetime

from rhino_health.lib.metrics import Count
from rhino_health.lib.metrics.base_metric import AggregatableMetric, BaseMetric, DataFilter
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class TimeRangeBasedMetric(AggregatableMetric, ABC):
    """
    Abstract class for metrics that are based on a time range
    """

    variable: FilterVariableTypeOrColumnName
    detected_column_name: FilterVariableTypeOrColumnName
    time_column_name: FilterVariableTypeOrColumnName
    start_time: str
    end_time: str

    @property
    def supports_custom_aggregation(self):
        return False


class Prevalence(TimeRangeBasedMetric):
    """
    Returns the prevalence of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "prevalence"


class Incidence(TimeRangeBasedMetric):
    """
    Returns the incidence of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "incidence"
