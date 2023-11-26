"""This module contains functions related to the Ryan-Joiner test

##### List of functions (cte_alphabetical order) #####

## Functions WITH good TESTS ###
- _critical_value(sample_size, alpha=0.05, safe=False)
- _normal_order_statistic(x_data, weighted=False, cte_alpha="3/8", safe=False)
- _order_statistic(sample_size, cte_alpha="3/8", safe=False)
- _p_value(statistic, sample_size, safe=False)
- citation(export=False)
- rj_test(x_data, alpha=0.05, cte_alpha="3/8", weighted=False, safe=False)

## Functions WITH some TESTS ###
- _statistic(x_data, zi, safe=False)
- correlation_plot(axes, x_data, cte_alpha="3/8", weighted=False, safe=False)
- dist_plot(axes, x_data, cte_alpha="3/8", min=4, max=50, weighted=False, safe=False)
- _make_line_up_data(x_data, weighted, cte_alpha, safe)
- line_up(x_data, cte_alpha="3/8", weighted=False, seed=42, correct=False, safe=False)


## Functions WITHOUT tests ###



##### List of CLASS (alphabetical order) #####



Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created : November 02, 2023

Last update: November 13, 2023
"""

##### IMPORTS #####

### Standard ###
from collections import namedtuple


### Third part ###
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy import interpolate

# import seaborn as sns


### self made ###
from paramcheckup import parameters, types, numbers, numpy_arrays
from . import bibmaker
from .utils import constants
from .utils.helpers import AlphaManagement, SafeManagement

##### DOCUMENTATION #####
from .utils import documentation as docs

#### CONSTANTS ####
RyanJoiner1976 = "RYAN, T. A., JOINER, B. L. Normal Probability Plots and Tests for Normality, Technical Report, Statistics Department, The Pennsylvania State University, 1976. Available at `www.additive-net.de <https://www.additive-net.de/de/component/jdownloads/send/70-support/236-normal-probability-plots-and-tests-for-normality-thomas-a-ryan-jr-bryan-l-joiner>`_. Access on: 22 Jul. 2023."
Blom1958 = "BLOM, G. Statistical Estimates and Transformed Beta-Variables. New York: John Wiley and Sons, Inc, p. 71-72, 1958."


##### CLASS #####


##### FUNCTIONS #####


def citation(export=False):
    """This function returns the reference from Ryan Joiner's test, with the option to export the reference in `.bib` format.

    Parameters
    ----------
    export : bool
        Whether to export the reference as `ryan-joiner.bib` file (`True`) or not (`False`, default);


    Returns
    -------
    reference : str
        The Ryan Joiner Test reference

    """
    reference = bibmaker.make_techreport(
        citekey="RyanJoiner1976",
        author="Thomas A. Ryan and Brian L. Joiner",
        title="Normal Probability Plots and Tests for Normality",
        institution="The Pennsylvania State University, Statistics Department",
        year="1976",
        url="https://api.semanticscholar.org/CorpusID:9233652",
        export=export,
    )
    return reference


@docs.docstring_parameter(
    sample_size=docs.SAMPLE_SIZE["type"],
    samp_size_desc=docs.SAMPLE_SIZE["description"],
    alpha=docs.ALPHA["type"],
    alpha_desc=docs.ALPHA["description"],
    critical=docs.CRITICAL["type"],
    critical_desc=docs.CRITICAL["description"],
    rj_ref=RyanJoiner1976,
)
def _critical_value(sample_size, alpha=0.05):
    """This function calculates the critical value of the Ryan-Joiner test [1]_.

    Parameters
    ----------
    {sample_size}
        {samp_size_desc}
    {alpha}
        {alpha_desc}


    Returns
    -------
    {critical}
        {critical_desc}


    See Also
    --------
    rj_test


    Notes
    -----
    The critical values are calculated using [1]_ the following equations:

    .. math::

            R_{{p;\\alpha=0.10}}^{{'}} = 1.0071 - \\frac{{0.1371}}{{\\sqrt{{n}}}} - \\frac{{0.3682}}{{n}} + \\frac{{0.7780}}{{n^{{2}}}}

            R_{{p;\\alpha=0.05}}^{{'}} = 1.0063 - \\frac{{0.1288}}{{\\sqrt{{n}}}} - \\frac{{0.6118}}{{n}} + \\frac{{1.3505}}{{n^{{2}}}}

            R_{{p;\\alpha=0.01}}^{{'}} = 0.9963 - \\frac{{0.0211}}{{\\sqrt{{n}}}} - \\frac{{1.4106}}{{n}} + \\frac{{3.1791}}{{n^{{2}}}}

    where :math:`n` is the sample size.


    References
    ----------
    .. [1] {rj_ref}


    Examples
    --------
    >>> from normtest import ryan_joiner
    >>> critical = ryan_joiner._critical_value(10, alpha=0.05)
    >>> print(critical)
    0.9178948637370312

    """

    if alpha == 0.1:
        return (
            1.0071
            - (0.1371 / np.sqrt(sample_size))
            - (0.3682 / sample_size)
            + (0.7780 / sample_size**2)
        )
    elif alpha == 0.05:
        return (
            1.0063
            - (0.1288 / np.sqrt(sample_size))
            - (0.6118 / sample_size)
            + (1.3505 / sample_size**2)
        )
    else:  # alpha == 0.01:
        return (
            0.9963
            - (0.0211 / np.sqrt(sample_size))
            - (1.4106 / sample_size)
            + (3.1791 / sample_size**2)
        )


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    weighted=docs.WEIGHTED["type"],
    weighted_desc=docs.WEIGHTED["description"],
    cte_alpha=docs.CTE_ALPHA["type"],
    cte_alpha_desc=docs.CTE_ALPHA["description"],
    zi=docs.ZI["type"],
    zi_desc=docs.ZI["description"],
)
def _normal_order_statistic(x_data, weighted=False, cte_alpha="3/8"):
    """This function transforms the statistical order to the standard Normal distribution scale (:math:`z_{{i}}`).

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    {cte_alpha}
        {cte_alpha_desc}

    {weighted}
        {weighted_desc}


    Returns
    -------
    {zi}
        {zi_desc}


    Notes
    -----
    The transformation to the standard Normal scale is done using the equation:

    .. math::

            z_{{i}} = \\phi^{{-1}} \\left(p_{{i}} \\right)

    where :math:`p_{{i}}` is the normal statistical order and :math:`\\phi^{{-1}}` is the inverse of the standard Normal distribution. The transformation is performed using :doc:`stats.norm.ppf() <scipy:reference/generated/scipy.stats.norm>`.

    The statistical order (:math:`p_{{i}}`) is estimated using :func:`_order_statistic` function. See this function for details on parameter `cte_alpha`.


    See Also
    --------
    rj_test


    Examples
    --------
    The first example uses `weighted=False`:

    >>> import numpy as np
    >>> from normtest import ryan_joiner
    >>> data = np.array([148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210])
    >>> result = ryan_joiner._normal_order_statistic(data, weighted=False)
    >>> print(result)
    [-1.67293739 -1.16188294 -0.84837993 -0.6020065  -0.38786869 -0.19032227
    0.          0.19032227  0.38786869  0.6020065   0.84837993  1.16188294
    1.67293739]

    The second example uses `weighted=True`, with the same data set:

    >>> result = ryan_joiner._normal_order_statistic(data, weighted=True)
    >>> print(result)
    [-1.37281032 -1.37281032 -0.84837993 -0.4921101  -0.4921101  -0.19032227
    0.          0.19032227  0.38786869  0.6020065   0.84837993  1.16188294
    1.67293739]


    Note that the results are only different for positions where we have repeated values. Using `weighted=True`, the normal statistical order is obtained with the average of the order statistic values.

    The results will be identical if the data set does not contain repeated values.

    """

    # ordering
    x_data = np.sort(x_data)
    if weighted:
        df = pd.DataFrame({"x_data": x_data})
        # getting mi values
        df["Rank"] = np.arange(1, df.shape[0] + 1)
        df["Ui"] = _order_statistic(
            sample_size=x_data.size,
            cte_alpha=cte_alpha,
        )
        df["Mi"] = df.groupby(["x_data"])["Ui"].transform("mean")
        normal_ordered = stats.norm.ppf(df["Mi"])
    else:
        ordered = _order_statistic(
            sample_size=x_data.size,
            cte_alpha=cte_alpha,
        )
        normal_ordered = stats.norm.ppf(ordered)

    return normal_ordered


@docs.docstring_parameter(
    samp_size=docs.SAMPLE_SIZE["type"],
    samp_size_desc=docs.SAMPLE_SIZE["description"],
    cte_alpha=docs.CTE_ALPHA["type"],
    cte_alpha_desc=docs.CTE_ALPHA["description"],
    blom_ref=Blom1958,
    rj_ref=RyanJoiner1976,
)
def _order_statistic(sample_size, cte_alpha="3/8"):
    """This function estimates the normal statistical order (:math:`p_{{i}}`) using approximations [1]_.

    Parameters
    ----------
    {samp_size}
        {samp_size_desc}
    {cte_alpha}
        A `str` with the `cte_alpha` value that should be adopted (see details in the Notes section). The options are:

        * `"0"`;
        * `"3/8"` (default);
        * `"1/2"`;



    Returns
    -------
    pi : :doc:`numpy array <numpy:reference/generated/numpy.array>`
        The estimated statistical order (:math:`p_{{i}}`)


    See Also
    --------
    ryan_joiner


    Notes
    -----

    The `cte_alpha` (:math:`\\alpha_{{cte}}`) parameter corresponds to the values studied by [1]_, which adopts the following equation to estimate the statistical order:

    .. math::

            p_{{i}} = \\frac{{i - \\alpha_{{cte}}}}{{n - 2 \\times \\alpha_{{cte}} + 1}}

    where :math:`n` is the sample size and :math:`i` is the ith observation.


    .. admonition:: Info

        `cte_alpha="3/8"` is adopted in the implementations of the Ryan-Joiner test in Minitab and Statext software. This option is also cited as an alternative by [2]_.


    References
    ----------
    .. [1] {blom_ref}

    .. [2] {rj_ref}


    Examples
    --------
    >>> from normtest import ryan_joiner
    >>> size = 10
    >>> pi = ryan_joiner._order_statistic(size)
    >>> print(pi)
    [0.06097561 0.15853659 0.25609756 0.35365854 0.45121951 0.54878049
    0.64634146 0.74390244 0.84146341 0.93902439]

    """

    i = np.arange(1, sample_size + 1)
    if cte_alpha == "1/2":
        cte_alpha = 0.5
    elif cte_alpha == "0":
        cte_alpha = 0
    else:
        cte_alpha = 3 / 8

    return (i - cte_alpha) / (sample_size - 2 * cte_alpha + 1)


@docs.docstring_parameter(
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    samp_size=docs.SAMPLE_SIZE["type"],
    samp_size_desc=docs.SAMPLE_SIZE["description"],
    p_value=docs.P_VALUE["type"],
    p_value_desc=docs.P_VALUE["description"],
    rj_ref=RyanJoiner1976,
)
def _p_value(statistic, sample_size):
    """This function estimates the probability associated with the Ryan-Joiner Normality test [1]_.


    Parameters
    ----------
    {statistic}
        {statistic_desc}
    {samp_size}
        {samp_size_desc}


    Returns
    -------
    {p_value}
        {p_value_desc}


    See Also
    --------
    rj_test


    Notes
    -----
    The test probability is estimated through linear interpolation of the test statistic with critical values from the Ryan-Joiner test [1]_. The Interpolation is performed using the :doc:`scipy.interpolate.interp1d() <scipy:reference/generated/scipy.interpolate.interp1d>` function.

    * If the test statistic is greater than the critical value for :math:`\\alpha=0.10`, the result is always *"p > 0.100"*.
    * If the test statistic is lower than the critical value for :math:`\\alpha=0.01`, the result is always *"p < 0.010"*.


    .. warning:: The estimated :math:`p_{{value}}` may not be accurate as it is calculated using linear interpolation


    References
    ----------
    .. [1] {rj_ref}


    Examples
    --------
    >>> from normtest import ryan_joiner
    >>> p_value = ryan_joiner._p_value(0.90, 10)
    >>> print(p_value)
    0.030930589077996555

    """

    alphas = np.array([0.10, 0.05, 0.01])
    criticals = np.array(
        [
            _critical_value(sample_size=sample_size, alpha=alphas[0]),
            _critical_value(sample_size=sample_size, alpha=alphas[1]),
            _critical_value(sample_size=sample_size, alpha=alphas[2]),
        ]
    )
    f = interpolate.interp1d(criticals, alphas)
    if statistic > max(criticals):
        return "p > 0.100"
    elif statistic < min(criticals):
        return "p < 0.010"
    else:
        p_value = float(f(statistic))
        return p_value


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    zi=docs.ZI["type"],
    zi_desc=docs.ZI["description"],
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    rj_ref=RyanJoiner1976,
)
def _statistic(x_data, zi):
    """This function estimates the Ryan-Joiner test statistic [1]_.

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    {zi}
        {zi_desc}


    Returns
    -------
    {statistic}
        {statistic_desc}


    Notes
    -----
    The test statistic (:math:`R_{{p}}`) is estimated through the correlation between the ordered data and the Normal statistical order:

    .. math::

            R_{{p}}=\\dfrac{{\\sum_{{i=1}}^{{n}}x_{{(i)}}z_{{(i)}}}}{{\\sqrt{{s^{{2}}(n-1)\\sum_{{i=1}}^{{n}}z_{{(i)}}^2}}}}

    where :math:`z_{{(i)}}` values are the z-score values of the corresponding experimental data (:math:`x_{{({{i)}}}}`) value, :math:`n` is the sample size and :math:`s^{{2}}` is the sample variance.

    The correlation is estimated using :doc:`scipy.stats.pearsonr() <scipy:reference/generated/scipy.stats.pearsonr>`.


    References
    ----------
    .. [1] {rj_ref}


    Examples
    --------
    >>> from normtest import ryan_joiner
    >>> import numpy as np
    >>> x_data = np.array([148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210])
    >>> x_data = np.sort(x_data)
    >>> normal_order = ryan_joiner._normal_order_statistic(x_data)
    >>> result = ryan_joiner._statistic(x_data, normal_order)
    >>> print(result)
    0.9225156050800545

    """
    return stats.pearsonr(zi, x_data)[0]


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    alpha=docs.ALPHA["type"],
    alpha_desc=docs.ALPHA["description"],
    cte_alpha=docs.CTE_ALPHA["type"],
    cte_alpha_desc=docs.CTE_ALPHA["description"],
    weighted=docs.WEIGHTED["type"],
    weighted_desc=docs.WEIGHTED["description"],
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    critical=docs.CRITICAL["type"],
    critical_desc=docs.CRITICAL["description"],
    p_value=docs.P_VALUE["type"],
    p_value_desc=docs.P_VALUE["description"],
    rj_ref=RyanJoiner1976,
)
def rj_test(x_data, alpha=0.05, cte_alpha="3/8", weighted=False):
    """This function applies the Ryan-Joiner Normality test [1]_.

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    {alpha}
        {alpha_desc}
    {cte_alpha}
        {cte_alpha_desc}
    {weighted}
        {weighted_desc}


    Returns
    -------
    result : tuple with
        {statistic}
            {statistic_desc}
        critical
            {critical_desc}
        {p_value}
            {p_value_desc}
        conclusion : str
            The test conclusion (e.g, Normal/Not Normal).


    See Also
    --------
    correlation_plot
    dist_plot


    Notes
    -----
    The test statistic (:math:`R_{{p}}`) is estimated through the correlation between the ordered data and the Normal statistical order:

    .. math::

            R_{{p}}=\\dfrac{{\\sum_{{i=1}}^{{n}}x_{{(i)}}z_{{(i)}}}}{{\\sqrt{{s^{{2}}(n-1)\\sum_{{i=1}}^{{n}}z_{{(i)}}^2}}}}

    where :math:`z_{{(i)}}` values are the z-score values of the corresponding experimental data (:math:`x_{{({{i)}}}}`) value and :math:`s^{{2}}` is the sample variance.

    The correlation is estimated using :func:`_statistic`.

    The Normality test has the following assumptions:

    .. admonition:: \u2615

       :math:`H_0:` Data was sampled from a Normal distribution.

       :math:`H_1:` The data was sampled from a distribution other than the Normal distribution.


    The conclusion of the test is based on the comparison between the `critical` value (at :math:`\\alpha` significance level) and `statistic` of the test:

    .. admonition:: \u2615

       if critical :math:`\\leq` statistic:
           Fail to reject :math:`H_0:` (e.g., data is Normal)
       else:
           Reject :math:`H_0:` (e.g., data is not Normal)

    The critical values are obtained using :func:`_critical_value`.


    .. warning:: The estimated :math:`p_{{value}}` may not be accurate as it is calculated using linear interpolation.

    References
    ----------
    .. [1] {rj_ref}


    Examples
    --------
    >>> from normtest import ryan_joiner
    >>> from scipy import stats
    >>> data = stats.norm.rvs(loc=0, scale=1, size=30, random_state=42)
    >>> result = ryan_joiner.rj_test(data)
    >>> print(result)
    RyanJoiner(statistic=0.990439558451558, critical=0.963891667086667, p_value='p > 0.100', conclusion='Fail to reject H₀')

    """
    # ordering
    x_data = np.sort(x_data)

    # zi
    zi = _normal_order_statistic(
        x_data=x_data,
        weighted=weighted,
        cte_alpha=cte_alpha,
    )

    # calculating the stats
    statistic = _statistic(x_data=x_data, zi=zi)

    # getting the critical values
    critical_value = _critical_value(sample_size=x_data.size, alpha=alpha)

    # conclusion
    if statistic < critical_value:
        conclusion = constants.REJECTION
    else:
        conclusion = constants.ACCEPTATION

    # pvalue
    p_value = _p_value(statistic=statistic, sample_size=x_data.size)

    result = namedtuple(
        "RyanJoiner", ("statistic", "critical", "p_value", "conclusion")
    )
    return result(statistic, critical_value, p_value, conclusion)


@docs.docstring_parameter(
    axes=docs.AXES["type"],
    axes_desc=docs.AXES["description"],
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    cte_alpha=docs.CTE_ALPHA["type"],
    cte_alpha_desc=docs.CTE_ALPHA["description"],
    weighted=docs.WEIGHTED["type"],
    weighted_desc=docs.WEIGHTED["description"],
    rj_ref=RyanJoiner1976,
)
def correlation_plot(axes, x_data, cte_alpha="3/8", weighted=False):
    """This function creates an `axis` with the Ryan-Joiner test [1]_ correlation graph.

    Parameters
    ----------
    {axes}
        {axes_desc}
    {x_data}
        {x_data_desc}
    {cte_alpha}
        {cte_alpha_desc}

    {weighted}
        {weighted_desc}



    Returns
    -------
    {axes}
        {axes_desc}


    See Also
    --------
    rj_test
    dist_plot


    References
    ----------
    .. [1] {rj_ref}


    Examples
    --------
    >>> from normtest import ryan_joiner
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>> data = stats.norm.rvs(loc=0, scale=1, size=30, random_state=42)
    >>> fig, ax = plt.subplots(figsize=(6, 4))
    >>> ryan_joiner.correlation_plot(axes=ax, x_data=data)
    >>> #plt.savefig("correlation_plot.png")
    >>> plt.show()

    .. image:: img/correlation_plot.png
        :alt: Correlation chart for Ryan-Joiner test Normality test
        :align: center

    """

    constants.warning_plot()

    # ordering the sample
    zi = _normal_order_statistic(
        x_data=x_data,
        weighted=weighted,
        cte_alpha=cte_alpha,
    )
    x_data = np.sort(x_data)

    # performing regression
    reg = stats.linregress(zi, x_data)
    # pred data
    y_pred = zi * reg.slope + reg.intercept

    ## making the plot

    # adding the data
    axes.scatter(zi, x_data, fc="none", ec="k")

    # adding the trend line
    axes.plot(zi, y_pred, c="r")

    # adding the statistic
    text = "$R_{p}=" + str(round(reg.rvalue, 4)) + "$"
    axes.text(0.1, 0.9, text, ha="left", va="center", transform=axes.transAxes)

    # perfuming
    axes.set_xlabel("Normal statistical order")
    axes.set_ylabel("Ordered data")

    return axes


@docs.docstring_parameter(
    axes=docs.AXES["type"],
    axes_desc=docs.AXES["description"],
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    sample_size=docs.SAMPLE_SIZE["type"],
    sample_size_desc=docs.AXES["description"],
    rj_ref=RyanJoiner1976,
)
def dist_plot(
    axes,
    critical_range=(4, 50),
    test=None,
):
    """This function generates axis with critical data from the Ryan-Joiner Normality test [1]_.

    Parameters
    ----------
    {axes}
        {axes_desc}
    critical_range : tuple (optional), with two elements:
        x_min : int, optional
            The lower range of the number of observations for the critical values (default is ``4``).
        x_max : int, optional
            The upper range of the number of observations for the critical values (default is ``50``).
    test : tuple (optional), with two elements:
        {statistic}
            {statistic_desc}
        {sample_size}
            {sample_size_desc}


    Returns
    -------
    {axes}
        {axes_desc}


    See Also
    --------
    rj_test
    correlation_plot


    References
    ----------
    .. [1] {rj_ref}


    Examples
    --------
    >>> from normtest import ryan_joiner
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>> data = stats.norm.rvs(loc=0, scale=1, size=30, random_state=42)


    Apply the Ryan Joiner test


    >>> result = ryan_joiner.rj_test(data)


    Create the distribution graph using the test result


    >>> fig, ax = plt.subplots(figsize=(6, 4))
    >>> ryan_joiner.dist_plot(axes=ax, test=(result.statistic, data.size))
    >>> # plt.savefig("rj_dist_plot.png")
    >>> plt.show()


    .. image:: img/dist_plot.png
        :alt: Critical chart for Ryan-Joiner test Normality test
        :align: center

    """
    constants.warning_plot()

    n_samples = np.arange(critical_range[0], critical_range[1] + 1)
    alphas = [0.10, 0.05, 0.01]
    alphas_label = ["$10\\%$", "$5\\%$", "$1\\%$"]
    colors = [
        (0.2980392156862745, 0.4470588235294118, 0.6901960784313725),
        (0.8666666666666667, 0.5176470588235295, 0.3215686274509804),
        (0.3333333333333333, 0.6588235294117647, 0.40784313725490196),
    ]

    # main test
    if test is not None:
        if test[1] > critical_range[1]:
            constants.user_warning(
                f"The graphical visualization is best suited if the sample size ({test[1]}) is smaller than the max value ({critical_range[1]})."
            )
        if test[1] < critical_range[0]:
            constants.user_warning(
                f"The graphical visualization is best suited if the sample size ({test[1]}) is greater than the min value ({critical_range[0]})."
            )

        axes.scatter(test[1], test[0], color="r", label="$R_{p}$", marker="^")

    # adding critical values
    for alp, color, alp_label in zip(alphas, colors, alphas_label):
        criticals = []
        for sample in n_samples:
            criticals.append(_critical_value(sample_size=sample, alpha=alp))
        axes.scatter(n_samples, criticals, label=alp_label, color=color, s=10)

    axes.set_title("Ryan-Joiner")

    # adding details
    axes.legend(loc=4)
    axes.set_xlabel("Sample size")
    axes.set_ylabel("Critical value")

    return axes


# this function does not have documentation on purpose (private)
@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    cte_alpha=docs.CTE_ALPHA["type"],
    cte_alpha_desc=docs.CTE_ALPHA["description"],
    weighted=docs.WEIGHTED["type"],
    weighted_desc=docs.WEIGHTED["description"],
    zi=docs.ZI["type"],
    zi_desc=docs.ZI["description"],
)
def _make_line_up_data(x_data, weighted, cte_alpha):
    """Tthis function prepares the data for the Ryan Joiner test `line_up` function.

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    {weighted}
        {weighted_desc}
    {cte_alpha}
        {cte_alpha_desc}


    Returns
    -------
    {x_data}
        The input data *ordered*
    {zi}
        {zi_desc}
    y_pred : :doc:`numpy array <numpy:reference/generated/numpy.array>`
        The predicted values for the linear regression between `x_data` and `zi`;

    """
    # ordering the sample
    x_data = np.sort(x_data)
    zi = _normal_order_statistic(
        x_data=x_data,
        weighted=weighted,
        cte_alpha=cte_alpha,
    )

    # performing regression
    reg = stats.linregress(zi, x_data)
    # pred data
    y_pred = zi * reg.slope + reg.intercept

    return x_data, zi, y_pred


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    cte_alpha=docs.CTE_ALPHA["type"],
    cte_alpha_desc=docs.CTE_ALPHA["description"],
    weighted=docs.WEIGHTED["type"],
    weighted_desc=docs.WEIGHTED["description"],
    zi=docs.ZI["type"],
    zi_desc=docs.ZI["description"],
)
def line_up(
    x_data,
    cte_alpha="3/8",
    weighted=False,
    seed=42,
    correct=False,
):
    """This function exports the figure with the correlation graphs for the line up method [1]_.

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    {cte_alpha}
        {cte_alpha_desc}

    {weighted}
        {weighted_desc}
    seed : int, optional
        A numerical value that generates a new set or repeats pseudo-random numbers. Use a positive integer value to be able to repeat results. Default is ``42``;
    correct : bool, optional
        Whether the `x_data` is to be drawn in red (`False`) or black (`True`, default);


    Returns
    -------
    fig : matplotlib.figure.Figure
        A figure with the generated graphics;


    Notes
    -----
    This function is based on the line up method, where ``20`` correlation graphs are generated. One of these graphs contains the graph obtained with the true data (`x_data`). The other `19` graphs are drawn from pseudo-random data obtained from the Normal distribution with a mean and standard deviation similar to `x_data`.

    The objective is to observe the 20 graphs at the same time and discover *which graph is the *least similar* to the behavior expected for the Normal distribution*.

    * If the identified graph corresponds to the true data, it can be concluded that the data set is not similar to a Normal distribution (with 95% confidence);
    * If the identified graph does not correspond to that obtained with real data, it can be concluded that the data set is similar to a Normal distribution (with 95% confidence);


    See Also
    --------
    rj_test
    dist_plot


    References
    ----------
    .. [1] BUJA, A. et al. Statistical inference for exploratory data analysis and model diagnostics. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, v. 367, n. 1906, p. 4361–4383, 13 nov. 2009


    Examples
    --------
    The line-up method must be conducted in two steps. The first step involves generating a figure with 20 graphs from the data, without indicating which graph is the true one.


    >>> from normtest import ryan_joiner
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> x_exp = np.array([5.1, 4.9, 4.7, 4.6, 5, 5.4, 4.6, 5, 4.4, 4.9, 5.4])
    >>> fig = ryan_joiner.line_up(x_exp, seed=42, correct=False)
    >>> fig.tight_layout()
    >>> # plt.savefig("line_up.png", bbox_inches="tight")
    >>> plt.show()


    .. image:: img/line_up.png
        :alt: Line-up method chart for Ryan-Joiner test Normality test
        :align: center

    The researcher must identify which of the 20 graphs deviates most significantly from what is expected for a Normal distribution. For instance, the graph located in the first row and second column.

    The second step involves determining which graph corresponds to the true data set. This can be accomplished by simply changing parameter `correct` from `False` to `True`:


    >>> fig = ryan_joiner.line_up(x_exp, seed=42, correct=True)
    >>> fig.tight_layout()
    >>> # plt.savefig("line_up_true.png", bbox_inches="tight")
    >>> plt.show()


    .. dropdown:: click to reveal output
        :animate: fade-in

        .. image:: img/line_up_true.png
            :alt: Line-up method chart for Ryan-Joiner test Normality test
            :align: center


        Given that the true data corresponds to the graph in the second row and first column, which was not identified as deviating from the others, we can conclude that the data set follows the Normal distribution, at least approximately.


    """
    constants.warning_plot()

    # getting a properly seed
    if seed is None:
        seed = int(np.random.rand() * (2**32 - 1))

    # creating a list of 20 integers and shuffling
    position = np.arange(20)
    rng = np.random.default_rng(seed)
    # sampling one to be the true position
    real_data_position = rng.choice(position)

    # preparing a list of 1000 seeds to generate Normal data
    seeds = np.arange(1000)
    seeds = rng.choice(seeds, 20)

    # making the synthetic data and grouping it with the real data at the random position
    data = []
    mean = x_data.mean()
    std = x_data.std(ddof=1)
    size = x_data.size

    for pos, sed in zip(position, seeds):
        if pos == real_data_position:
            data.append(x_data)
        else:
            data.append(
                stats.norm.rvs(loc=mean, scale=std, size=size, random_state=sed)
            )

    # creating the figure with the 20 axes

    rows = 5
    cols = 4
    fig, ax = plt.subplots(cols, rows, figsize=(10, 7))

    i = 0
    if correct:
        color = "r"
    else:
        color = "k"
    for row in range(rows):
        for col in range(cols):
            if i == real_data_position:
                x, zi, y_pred = _make_line_up_data(
                    x_data=data[i],
                    weighted=weighted,
                    cte_alpha=cte_alpha,
                )
                ax[col, row].scatter(zi, x, c=color)
                ax[col, row].plot(zi, y_pred, ls="--", c=color)

            else:
                x, zi, y_pred = _make_line_up_data(
                    x_data=data[i],
                    weighted=weighted,
                    cte_alpha=cte_alpha,
                )
                ax[col, row].scatter(zi, x, c="k")
                ax[col, row].plot(zi, y_pred, ls="--", c="k")

            i += 1
            ax[col, row].tick_params(axis="both", which="major", labelsize=5)

    fig.text(0.5, 0.0, f"Normal statistical order (seed={seed})", ha="center")
    fig.text(0.0, 0.5, "Ordered data", va="center", rotation="vertical")
    fig.patch.set_facecolor("white")

    return fig


##### CLASS #####


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    critical=docs.CRITICAL["type"],
    critical_desc=docs.CRITICAL["description"],
    p_value=docs.P_VALUE["type"],
    p_value_desc=docs.P_VALUE["description"],
    conclusion=docs.CONCLUSION["type"],
    conclusion_desc=docs.CONCLUSION["description"],
    alpha=docs.ALPHA["type"],
    alpha_desc=docs.ALPHA["description"],
    safe=docs.SAFE["type"],
    safe_desc=docs.SAFE["description"],
    rj_ref=RyanJoiner1976,
)
class RyanJoiner(AlphaManagement, SafeManagement):
    """This class instantiates an object to perform the Ryan-Joiner Normality test [1]_.


    Attributes
    ----------
    {statistic}
        {statistic_desc}
    {critical}
        {critical_desc}
    {p_value}
        {p_value_desc}
    {conclusion}
        {conclusion_desc}
    {alpha}
        {alpha_desc}
    normality : named tuple
        A tuple with the main test results summarized
    normality_hypothesis : str
        Description of the Normality test
    {safe}
        {safe_desc}

    Methods
    -------
    fit(x_data)
        Applies the Ryan-Joiner Normality test;
    dist_plot(axes, alphas=[0.10, 0.05, 0.01]):
        Generates `axis` with critical data from the Ryan-Joiner Normality test;
    correlation_plot(axes)
        Generates an `axis` with the Ryan-Joiner test correlation graph;
    line_up(seed=None, correct=False)
        Generates a `Figure` with the correlation graphs for the line up method;
    citation(export=False)
        Returns the Ryan-Joiner's test reference;

    References
    ----------
    .. [1] {rj_ref}


    Examples
    --------
    >>> from normtest import RyanJoiner
    >>> import numpy as np
    >>> x = np.array([6, 1, -4, 8, -2, 5, 0])
    >>> test = RyanJoiner()
    >>> test.fit(x)
    >>> print(test.normality)
    RyanJoiner(statistic=0.9844829186140105, critical=0.8977794003662074, p_value='p > 0.100', conclusion='Fail to reject H₀')

    """

    def __init__(
        self, alpha=0.05, safe=True, cte_alpha="3/8", weighted=False, **kwargs
    ):
        """Initiates RyanJoiner `class` inheriting the `AlphaManagement` and `SafeManagement` classes

        Attributes
        ----------
        class_name : "RyanJoiner"
        conclusion : None
            This attribute is used to check whether the fit method was applied or not
        alpha : float
        safe : bool
        cte_alpha : str
        weighted : bool


        """
        super().__init__(alpha=alpha, safe=safe, **kwargs)
        self.class_name = "RyanJoiner"
        self.conclusion = None  # for checking if the fit was applied
        if safe:
            parameters.param_options(
                option=alpha,
                options=[0.01, 0.05, 0.10],
                param_name="alpha",
                kind="class",
                kind_name=self.class_name,
                stacklevel=4,
                error=True,
            )
            parameters.param_options(
                option=cte_alpha,
                options=["0", "3/8", "1/2"],
                param_name="cte_alpha",
                kind="class",
                kind_name=self.class_name,
                stacklevel=4,
                error=True,
            )

            types.is_bool(
                value=weighted,
                param_name="weighted",
                kind="class",
                kind_name=self.class_name,
                stacklevel=4,
                error=True,
            )
        self.cte_alpha = cte_alpha
        self.weighted = weighted
        self.set_safe(safe=safe)
        self.alpha = alpha
        self.normality_hypothesis = constants.HYPOTESES

    @docs.docstring_parameter(
        x_data=docs.X_DATA["type"],
        x_data_desc=docs.X_DATA["description"],
        statistic=docs.STATISTIC["type"],
        statistic_desc=docs.STATISTIC["description"],
        critical=docs.CRITICAL["type"],
        critical_desc=docs.CRITICAL["description"],
        p_value=docs.P_VALUE["type"],
        p_value_desc=docs.P_VALUE["description"],
        conclusion=docs.CONCLUSION["type"],
        conclusion_desc=docs.CONCLUSION["description"],
    )
    def fit(
        self,
        x_data,
    ):
        """This method applies the Ryan-Joiner test.

        Parameters
        ----------
        {x_data}
            {x_data_desc}


        Returns
        -------
        {x_data}
            {x_data_desc}
        {statistic}
            {statistic_desc}
        {critical}
            {critical_desc}
        {p_value}
            {p_value_desc}
        {conclusion}
            {conclusion_desc}
        normality : named tuple
            A tuple with the main test results summarized


        See Also
        --------
        rj_test


        """
        func_name = "fit"

        if self.safe:
            types.is_numpy(
                value=x_data,
                param_name="x_data",
                kind="method",
                kind_name=func_name,
                stacklevel=4,
                error=True,
            )
            numpy_arrays.n_dimensions(
                array=x_data,
                param_name="x_data",
                ndim=1,
                kind="method",
                kind_name=func_name,
                stacklevel=4,
                error=True,
            )
            numpy_arrays.size_is_greater_than_lower(
                array=x_data,
                param_name="x_data",
                kind="method",
                kind_name=func_name,
                lower=4,
                inclusive=True,
                stacklevel=4,
                error=True,
            )

        result = rj_test(
            x_data=x_data,
            alpha=self.alpha,
            cte_alpha=self.cte_alpha,
            weighted=self.weighted,
        )
        self.x_data = x_data
        self.statistic = result.statistic
        self.critical = result.critical
        self.p_value = result.p_value
        self.conclusion = result.conclusion
        self.normality = result

    @docs.docstring_parameter(
        axes=docs.AXES["type"],
        axes_desc=docs.AXES["description"],
    )
    def dist_plot(self, axes, critical_range=(4, 50)):
        """This method generates an `axis` with the critical data from the Ryan-Joiner Normality test.

        Parameters
        ----------
        {axes}
            {axes_desc}
        critical_range : tuple (optional), with two elements:
            x_min : int, optional
                The lower range of the number of observations for the critical values (default is ``4``).
            x_max : int, optional
                The upper range of the number of observations for the critical values (default is ``50``).


        Returns
        -------
        {axes}
            {axes_desc}


        See Also
        --------
        dist_plot


        """
        method_name = "dist_plot"
        if self.conclusion is None:
            return "The Ryan Joiner Normality test was not performed yet.\nUse the 'fit' method to perform the test."
        else:
            if self.safe:
                types.is_subplots(
                    value=axes,
                    param_name="axes",
                    kind="method",
                    kind_name=method_name,
                    stacklevel=4,
                    error=True,
                )
                types.is_tuple(
                    value=critical_range,
                    param_name="critical_range",
                    kind="method",
                    kind_name=method_name,
                    stacklevel=4,
                    error=True,
                )
                types.is_int(
                    value=critical_range[0],
                    param_name="x_min",
                    kind="method",
                    kind_name=method_name,
                    stacklevel=4,
                    error=True,
                )
                types.is_int(
                    value=critical_range[1],
                    param_name="x_max",
                    kind="method",
                    kind_name=method_name,
                    stacklevel=4,
                    error=True,
                )
                numbers.is_greater_than(
                    number=critical_range[0],
                    lower=4,
                    param_name="x_min",
                    kind="method",
                    kind_name=method_name,
                    inclusive=True,
                    stacklevel=4,
                    error=True,
                )

            return dist_plot(
                axes=axes,
                critical_range=critical_range,
                test=(self.statistic, self.x_data.size),
            )

    @docs.docstring_parameter(
        axes=docs.AXES["type"],
        axes_desc=docs.AXES["description"],
    )
    def correlation_plot(
        self,
        axes,
    ):
        """This method generates an axis with the correlation plotfor the Ryan-Joiner Normality test.

        Parameters
        ----------
        {axes}
            {axes_desc}


        Returns
        -------
        {axes}
            {axes_desc}


        See Also
        --------
        correlation_plot


        """
        method_name = "correlation_plot"
        if self.conclusion is None:
            return "The Ryan Joiner Normality test was not performed yet.\nUse the 'fit' method to perform the test."
        else:
            if self.safe:
                types.is_subplots(
                    value=axes,
                    param_name="axes",
                    kind="method",
                    kind_name=method_name,
                    stacklevel=4,
                    error=True,
                )

            return correlation_plot(
                axes=axes,
                x_data=self.x_data,
                cte_alpha=self.cte_alpha,
                weighted=self.weighted,
            )

    def line_up(
        self,
        seed=None,
        correct=False,
    ):
        """This method generates a `Figure` with the correlation graphs for the line up method.

        Parameters
        ----------
        seed : int or None, optional
            A numerical value that generates a new set or repeats pseudo-random numbers. Use a positive integer value to be able to repeat results. Default is ``None`` what generates a random seed;
        correct : bool, optional
            Whether the `x_data` is to be drawn in red (`False`) or black (`True`, default);


        Returns
        -------
        fig : matplotlib.figure.Figure
            A figure with the generated graphics;


        See Also
        --------
        line_up



        """
        method_name = "line_up"
        if self.conclusion is None:
            return "The Ryan Joiner Normality test was not performed yet.\nUse the 'fit' method to perform the test."
        else:
            if self.safe:
                types.is_bool(
                    value=correct,
                    param_name="correct",
                    kind="method",
                    kind_name=method_name,
                    stacklevel=4,
                    error=True,
                )
                if seed is not None:
                    types.is_int(
                        value=seed,
                        param_name="seed",
                        kind="method",
                        kind_name=method_name,
                        stacklevel=4,
                        error=True,
                    )
                    numbers.is_positive(
                        number=seed,
                        param_name="seed",
                        kind="method",
                        kind_name=method_name,
                        stacklevel=4,
                        error=True,
                    )

            return line_up(
                x_data=self.x_data,
                cte_alpha=self.cte_alpha,
                weighted=self.weighted,
                seed=seed,
                correct=correct,
            )

    def citation(self, export=False):
        """This method returns the reference from Ryan-Joiner's test, with the option to export the reference in `.bib` format.

        Parameters
        ----------
        export : bool
            Whether to export the reference as `RyanJoiner1976.bib` file (`True`) or not (`False`, default);


        Returns
        -------
        reference : str
            The Ryan-Joiner Test reference;

        """
        return citation(export=export)

    def __str__(self):
        if self.conclusion is None:
            text = "The Ryan-Joiner Normality test was not performed yet.\nUse the 'fit' method to perform the test."
            return text
        else:
            return self.conclusion

    def __repr__(self):
        return "Ryan-Joiner Normality test"
