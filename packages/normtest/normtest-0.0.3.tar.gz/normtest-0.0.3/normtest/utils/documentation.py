### FUNCTIONS ###


def docstring_parameter(*args, **kwargs):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj

    return dec


### CONSTANTS ###


ALPHA = {
    "type": "alpha : float, optional",
    "description": "The level of significance (:math:`\\alpha`). Default is ``0.05``;",
}

AXES = {
    "type": "axes : matplotlib.axes.SubplotBase",
    "description": "The axis of the graph;",
}

CONCLUSION = {
    "type": "conclusion : str",
    "description": "The test conclusion (e.g, Normal/Not Normal).",
}


CRITICAL = {
    "type": "critical : float",
    "description": "The critical value of the test;",
}


CTE_ALPHA = {
    "type": "cte_alpha : str, optional",
    "description": """A `str` with the `cte_alpha` value that should be adopted. The options are:

        * `"0"`;
        * `"3/8"` (default);
        * `"1/2"`;""",
}


MI = {
    "type": "mi : :doc:`numpy array <numpy:reference/generated/numpy.array>`",
    "description": "The estimated the uniform order statistic median (:math:`m_{{i}}`)",
}


P_VALUE = {
    "type": "p_value : float or str",
    "description": "The probability of the test;",
}


SAFE = {
    "type": "safe : bool, optional",
    "description": "Whether to check the inputs before performing the calculations (`True`, default) or not (`False`). Useful for beginners to identify problems in data entry (may reduce algorithm execution time);",
}


SAMPLE_SIZE = {
    "type": "sample_size : int",
    "description": "The sample size. Must be equal or greater than ``4``;",
}


STATISTIC = {
    "type": "statistic : float (positive)",
    "description": "The test statistic;",
}


X_DATA = {
    "type": "x_data : :doc:`numpy array <numpy:reference/generated/numpy.array>`",
    "description": "One dimension :doc:`numpy array <numpy:reference/generated/numpy.array>` with at least ``4`` observations.",
}


WEIGHTED = {
    "type": "weighted : bool, optional",
    "description": "Whether to estimate the Normal order considering the repeats as its average (`True`) or not (`False`, default). Only has an effect if the dataset contains repeated values;",
}


ZI = {
    "type": "zi : :doc:`numpy array <numpy:reference/generated/numpy.array>`",
    "description": "The statistical order in the standard Normal distribution scale.",
}


# PARAM = {
#     "type":
#     "description":
# }
