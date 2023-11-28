from rhino_health.lib.metrics.base_metric import (
    AggregatableMetric,
    BaseMetric,
    KaplanMeierMetricResponse,
)
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class ChiSquare(AggregatableMetric):
    """
    A metric that calculates the Chi-Square test for multiple cohort.
    """

    variable: FilterVariableTypeOrColumnName  # Used as an identifier for the count calculation
    variable_1: FilterVariableTypeOrColumnName  # TODO: better names
    variable_2: FilterVariableTypeOrColumnName

    @classmethod
    def metric_name(cls):
        return "chi_square"

    @property
    def supports_custom_aggregation(self):
        return False


class TTest(AggregatableMetric):
    """
    A metric that calculates the T test for multiple cohort.
    """

    numeric_variable: FilterVariableTypeOrColumnName  # Used as an identifier for the count calculation
    categorical_variable: FilterVariableTypeOrColumnName  # TODO: better names

    @classmethod
    def metric_name(cls):
        return "t_test"

    @property
    def supports_custom_aggregation(self):
        return False
