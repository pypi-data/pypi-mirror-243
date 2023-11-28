from rhino_health.lib.metrics.base_metric import AggregatableMetric, BaseMetric
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class Count(AggregatableMetric):
    """
    Returns the count of entries for a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    @classmethod
    def metric_name(cls):
        return "count"


class Mean(AggregatableMetric):
    """
    Returns the mean value of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    @classmethod
    def metric_name(cls):
        return "mean"


class StandardDeviation(AggregatableMetric):
    """
    Returns the standard deviation of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    @classmethod
    def metric_name(cls):
        return "stddev"


class Sum(AggregatableMetric):
    """
    Returns the sum of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    @classmethod
    def metric_name(cls):
        return "sum"


COMMON_METRICS = [Count, Mean, StandardDeviation, Sum]
