"""This module contains functions related to the Filliben test

##### List of functions (cte_alphabetical order) #####

## Functions WITH good TESTS ###


## Functions WITH some TESTS ###
- _critical_value(sample_size, alpha=0.05)
- _make_line_up_data(x_data)
- _normal_order_medians(mi)
- _p_value(statistic, sample_size)
- _statistic(x_data, zi)
- _uniform_order_medians(sample_size)
- citation(export=False)
- correlation_plot(axes, x_data)
- dist_plot(axes, test=None, alphas=[0.10, 0.05, 0.01])
- fi_test(x_data, alpha=0.05)
- line_up(x_data, seed=None, correct=False)

## Functions WITHOUT tests ###



##### List of CLASS (alphabetical order) #####

## WITH some TESTS ###
- Filliben(AlphaManagement, SafeManagement)
    - __init__(self, alpha=0.05, safe=True, **kwargs)
    - fit(self, x_data)
    - dist_plot(self, axes, alphas=[0.10, 0.05, 0.01])
    - correlation_plot(self, axes)
    - line_up(self, seed=None, correct=False)
    - citation(self, export=False)
    - __str__(self)
    - __repr__(self)

Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created : November 08, 2023

Last update: November 13, 2023
"""

##### IMPORTS #####

### Standard ###
from collections import namedtuple
from copy import deepcopy
import itertools

### Third part ###
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy import interpolate

# import seaborn as sns


### self made ###
from paramcheckup import parameters, types, numbers, numpy_arrays
from normtest import bibmaker
from .utils import critical_values, constants
from .utils.helpers import AlphaManagement, SafeManagement

##### DOCUMENTATION #####
from .utils import documentation as docs


#### CONSTANTS ####
Filliben1975 = "FILLIBEN, J. J. The Probability Plot Correlation Coefficient Test for Normality. Technometrics, v. 17, n. 1, p. 111-117, 1975."


##### FUNCTIONS #####


def citation(export=False):
    """This function returns the reference from Filliben's test, with the option to export the reference in `.bib` format.

    Parameters
    ----------
    export : bool
        Whether to export the reference as `Filliben1975.bib` file (`True`) or not (`False`, default);


    Returns
    -------
    reference : str
        The Filliben Test reference

    """
    reference = bibmaker.make_article(
        author="James J. Filliben",
        title="The Probability Plot Correlation Coefficient Test for Normality",
        journaltitle="Technometrics",
        year=1975,
        citekey="Filliben1975",
        date=None,
        volume="17",
        number="1",
        pages="111--117",
        doi="10.2307/1268008",
        month=2,
        export=export,
    )
    return reference


@docs.docstring_parameter(
    sample_size=docs.SAMPLE_SIZE["type"],
    samp_size_desc=docs.SAMPLE_SIZE["description"],
    mi=docs.MI["type"],
    mi_desc=docs.MI["description"],
    fi_ref=Filliben1975,
)
def _uniform_order_medians(sample_size):
    """This function estimates the uniform order statistic median (:math:`m_{{i}}`) used in the Filliben normality test [1]_.

    Parameters
    ----------
    {sample_size}
        {samp_size_desc}


    Returns
    -------
    {mi}
        {mi_desc}

    See Also
    --------
    fi_test


    Notes
    -----
    The uniform order statistic median is estimated using:

    .. math::

            m_{{i}} = \\begin{{cases}}1-0.5^{{1/n}} & i = 1\\\ \\frac{{i-0.3175}}{{n+0.365}} & i = 2, 3,  \\ldots , n-1 \\\ 0.5^{{1/n}}& i=n \\end{{cases}}

    where :math:`n` is the sample size and :math:`i` is the ith observation.


    References
    ----------
    .. [1] {fi_ref}



    Examples
    --------
    >>> from normtest import filliben
    >>> uniform_order = filliben._uniform_order_medians(7)
    >>> print(uniform_order)
    array([0.09427634, 0.22844535, 0.36422267, 0.5       , 0.63577733,
           0.77155465, 0.90572366])
    """

    i = np.arange(1, sample_size + 1)
    mi = (i - 0.3175) / (sample_size + 0.365)
    mi[0] = 1 - 0.5 ** (1 / sample_size)
    mi[-1] = 0.5 ** (1 / sample_size)

    return mi


@docs.docstring_parameter(
    mi=docs.MI["type"],
    mi_desc=docs.MI["description"],
    zi=docs.ZI["type"],
    zi_desc=docs.ZI["description"],
)
def _normal_order_medians(mi):
    """This function transforms the uniform order median to normal order median using the standard Normal distribution (:math:`z_{{i}}`).

    Parameters
    ----------
    {mi}
        {mi_desc}


    Returns
    -------
    {zi}
        {zi_desc}


    Notes
    -----
    The transformation to the standard Normal scale is done using the equation:

    .. math::

            z_{{i}} = \\phi^{{-1}} \\left(m_{{i}} \\right)

    where :math:`m_{{i}}` is the uniform statistical order and :math:`\\phi^{{-1}}` is the inverse of the standard Normal distribution. The transformation is performed using :doc:`stats.norm.ppf() <scipy:reference/generated/scipy.stats.norm>`.


    See Also
    --------
    fi_test


    Examples
    --------
    >>> from normtest import filliben
    >>> uniform_order = filliben._uniform_order_medians(7)
    >>> normal_order = filliben._normal_order_medians(uniform_order)
    >>> print(normal_order)
    [-1.31487275 -0.74397649 -0.3471943   0.          0.3471943   0.74397649
    1.31487275]


    """
    normal_ordered = stats.norm.ppf(mi)
    return normal_ordered


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    zi=docs.ZI["type"],
    zi_desc=docs.ZI["description"],
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    fi_ref=Filliben1975,
)
def _statistic(x_data, zi):
    """This function estimates the statistic of the Filliben normality test [1]_

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    {zi}
        {zi_desc}


    Returns
    -------
    statistic
        {statistic_desc}


    See Also
    --------
    fi_test


    Notes
    -----
    The test statistic (:math:`F_{{p}}`) is estimated through the correlation between the ordered data and the Normal statistical order:


    .. math::

            F_p = \\frac{{\\sum_{{i=1}}^n \\left(x_i - \\overline{{x}}\\right) \\left(z_i - \\overline{{z}}\\right)}}{{\\sqrt{{\\sum_{{i=1}}^n \\left( x_i - \\overline{{x}}\\right)^2 \\sum_{{i=1}}^n \\left( z_i - \\overline{{z}}\\right)^2}}}}

    where :math:`z_{{i}}` values are the z-score values of the corresponding experimental data (:math:`x_{{{{i}}}}`) value, and :math:`n` is the sample size.

    The correlation is estimated using :doc:`scipy.stats.pearsonr() <scipy:reference/generated/scipy.stats.pearsonr>`.

    References
    ----------
    .. [1] {fi_ref}


    Examples
    --------
    >>> from normtest import filliben
    >>> import numpy as np
    >>> x_data = np.array([6, 1, -4, 8, -2, 5, 0])
    >>> uniform_order = filliben._uniform_order_medians(x_data.size)
    >>> normal_order = filliben._normal_order_medians(uniform_order)
    >>> x_data = np.sort(x_data)
    >>> statistic = filliben._statistic(x_data, normal_order)
    >>> print(statistic)
    0.9854095718708367


    """
    correl = stats.pearsonr(x_data, zi)[0]
    return correl


@docs.docstring_parameter(
    sample_size=docs.SAMPLE_SIZE["type"],
    sample_size_desc=docs.SAMPLE_SIZE["description"],
    alpha=docs.ALPHA["type"],
    alpha_desc=docs.ALPHA["description"],
    critical=docs.CRITICAL["type"],
    critical_desc=docs.CRITICAL["description"],
    fi_ref=Filliben1975,
)
def _critical_value(sample_size, alpha=0.05):
    """This function calculates the critical value for the Filliben normality test [1]_.


    Parameters
    ----------
    {sample_size}
        {sample_size_desc}
    {alpha}
        {alpha_desc}


    Returns
    -------
    {critical}
        {critical_desc}


    References
    ----------
    .. [1] {fi_ref}


    Examples
    --------
    >>> from normtest import filliben
    >>> sample_size = 7
    >>> critical = filliben._critical_value(sample_size, alpha=0.05)
    >>> print(critical)
    0.899


    """
    # making a copy from original critical values
    critical = deepcopy(critical_values.FILLIBEN_CRITICAL)

    if sample_size not in critical["n"]:
        if sample_size < 100:
            constants.user_warning(
                "The Filliben critical value may not be accurate as it was obtained with linear interpolation."
            )
        else:
            constants.user_warning(
                "The Filliben critical value may not be accurate as it was obtained with linear *extrapolation*."
            )

    f = interpolate.interp1d(
        critical["n"][3:], critical[alpha][3:], fill_value="extrapolate"
    )

    return float(f(sample_size))


@docs.docstring_parameter(
    axes=docs.AXES["type"],
    axes_desc=docs.AXES["description"],
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    sample_size=docs.SAMPLE_SIZE["type"],
    sample_size_desc=docs.SAMPLE_SIZE["description"],
    fi_ref=Filliben1975,
)
def dist_plot(axes, test=None, alphas=[0.10, 0.05, 0.01]):
    """This function generates axis with critical data from the Filliben Normality test [1]_.

    Parameters
    ----------
    {axes}
        {axes_desc}
    test : tuple (optional), with two elements:
        {statistic}
            {statistic_desc}
        {sample_size}
            {sample_size_desc}
    alphas : list of floats, optional
        The significance level (:math:`\\alpha`) to draw the critical lines. Default is `[0.10, 0.05, 0.01]`. It can be a combination of:

        * ``0.005``;
        * ``0.01``;
        * ``0.025``;
        * ``0.05``;
        * ``0.10``;
        * ``0.25``;
        * ``0.50``;
        * ``0.75``;
        * ``0.90``;
        * ``0.95``;
        * ``0.975``;
        * ``0.99``;
        * ``0.995``;



    Returns
    -------
    {axes}
        {axes_desc}


    References
    ----------
    .. [1] {fi_ref}


    Examples
    --------
    >>> from normtest import filliben
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots(figsize=(6, 4))
    >>> filliben.dist_plot(axes=ax, test=(0.98538, 7))
    >>> # plt.savefig("filliben_paper.png")
    >>> plt.show()


    .. image:: img/filliben_paper.png
        :alt: Default critical chart for Filliben Normality test
        :align: center


    """
    # making a copy from original critical values
    critical = deepcopy(critical_values.FILLIBEN_CRITICAL)

    if test is not None:
        axes.scatter(test[1], test[0], c="r", label="statistic", marker="^")

    palette = itertools.cycle(constants.seaborn_colors["deep"])

    for alpha, color in zip(alphas, palette):
        axes.scatter(
            critical["n"],
            critical[alpha],
            label=f"{round(alpha*100)}%",
            s=20,
            color=color,
        )
    axes.set_xlabel("Sample size")
    axes.set_ylabel("Filliben critical values")
    axes.legend(loc=4)

    return axes


@docs.docstring_parameter(
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    samp_size=docs.SAMPLE_SIZE["type"],
    samp_size_desc=docs.SAMPLE_SIZE["description"],
    p_value=docs.P_VALUE["type"],
    p_value_desc=docs.P_VALUE["description"],
    fi_ref=Filliben1975,
)
def _p_value(statistic, sample_size):
    """This function estimates the probability associated with the Filliben Normality test [1]_.


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
    fi_test


    Notes
    -----
    The test probability is estimated through linear interpolation of the test statistic with critical values from the Filliben test [1]_. The Interpolation is performed using the :doc:`scipy.interpolate.interp1d() <scipy:reference/generated/scipy.interpolate.interp1d>` function.

    * If the test statistic is greater than the critical value for :math:`\\alpha=0.995`, the result is always *"p > 0.995"*.
    * If the test statistic is lower than the critical value for :math:`\\alpha=0.005`, the result is always *"p < 0.005"*.


    .. warning:: The estimated :math:`p_{{value}}` may not be accurate as it is calculated using linear interpolation.

    References
    ----------
    .. [1] {fi_ref}


    Examples
    --------
    >>> from normtest import filliben
    >>> p_value = filliben._p_value(0.98538, 7)
    >>> print(p_value)
    0.8883750000000009

    """
    alphas = [
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        0.75,
        0.9,
        0.95,
        0.975,
        0.99,
        0.995,
    ]
    criticals = []
    for alpha in alphas:
        criticals.append(
            _critical_value(sample_size=sample_size, alpha=alpha),
        )
    f = interpolate.interp1d(criticals, alphas)
    if statistic > max(criticals):
        return "p > 0.995"
    elif statistic < min(criticals):
        return "p < 0.005"
    else:
        p_value = float(f(statistic))
        return p_value


@docs.docstring_parameter(
    axes=docs.AXES["type"],
    axes_desc=docs.AXES["description"],
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    fi_ref=Filliben1975,
)
def correlation_plot(axes, x_data):
    """This function creates an `axis` with the Filliben test [1]_ correlation graph.

    Parameters
    ----------
    {axes}
        {axes_desc}
    {x_data}
        {x_data_desc}


    Returns
    -------
    {axes}
        {axes_desc}


    See Also
    --------
    fi_test
    dist_plot


    References
    ----------
    .. [1] {fi_ref}


    Examples
    --------
    >>> from normtest import filliben
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> x_data = np.array([6, 1, -4, 8, -2, 5, 0])
    >>> fig, ax = plt.subplots()
    >>> ax = filliben.correlation_plot(ax, x_data)
    >>> # plt.savefig("correlation_plot.png")
    >>> plt.show()


    .. image:: img/correlation_plot.png
        :alt: Correlation chart for Filliben Normality test
        :align: center


    """

    constants.warning_plot()
    uniform_order = _uniform_order_medians(x_data.size)
    zi = _normal_order_medians(uniform_order)

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
    axes.set_xlabel("Normal order statistical medians")
    axes.set_ylabel("Ordered data")

    return axes


# this function does not have documentation on purpose (private)
@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    zi=docs.ZI["type"],
    zi_desc=docs.ZI["description"],
)
def _make_line_up_data(x_data):
    """Tthis function prepares the data for the Filliben test `line_up` function.

    Parameters
    ----------
    {x_data}
        {x_data_desc}


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
    uniform_order = _uniform_order_medians(x_data.size)
    zi = _normal_order_medians(uniform_order)

    # performing regression
    reg = stats.linregress(zi, x_data)
    # pred data
    y_pred = zi * reg.slope + reg.intercept

    return x_data, zi, y_pred


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
)
def line_up(x_data, seed=None, correct=False):
    """This function exports the figure with the correlation graphs for the line up method [1]_.

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    seed : int or None, optional
        A numerical value that generates a new set or repeats pseudo-random numbers. Use a positive integer value to be able to repeat results. Default is ``None`` what generates a random seed;
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
    fi_test
    dist_plot


    References
    ----------
    .. [1] BUJA, A. et al. Statistical inference for exploratory data analysis and model diagnostics. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, v. 367, n. 1906, p. 4361-4383, 13 nov. 2009


    Examples
    --------
    The line-up method must be conducted in two steps. The first step involves generating a figure with 20 graphs from the data, without indicating which graph is the true one.


    >>> from normtest import filliben
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> x_exp = np.array([5.1, 4.9, 4.7, 4.6, 5, 5.4, 4.6, 5, 4.4, 4.9, 5.4])
    >>> fig = filliben.line_up(x_exp, seed=42, correct=False)
    >>> fig.tight_layout()
    >>> # plt.savefig("line_up.png", bbox_inches="tight")
    >>> plt.show()


    .. image:: img/line_up.png
        :alt: Line-up method chart for Filliben Normality test
        :align: center

    The researcher must identify which of the 20 graphs deviates most significantly from what is expected for a Normal distribution. For instance, the graph located in the first row and second column.

    The second step involves determining which graph corresponds to the true data set. This can be accomplished by simply changing parameter `correct` from `False` to `True`:


    >>> fig = filliben.line_up(x_exp, seed=42, correct=True)
    >>> fig.tight_layout()
    >>> # plt.savefig("line_up.png", bbox_inches="tight")
    >>> plt.show()


    .. dropdown:: Click to reveal output
        :animate: fade-in

        .. image:: img/line_up_true.png
            :alt: Line-up method chart for Ryan-Joiner test Normality test
            :align: center


        Given that the true data corresponds to the graph in the second row and first column, which was not identified as deviating from the others, we can conclude that the data set follows the Normal distribution, at least approximately.



    .. admonition:: \u2615

        Note that the same seed must be used in both steps


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
                )
                ax[col, row].scatter(zi, x, c=color)
                ax[col, row].plot(zi, y_pred, ls="--", c=color)

            else:
                x, zi, y_pred = _make_line_up_data(
                    x_data=data[i],
                )
                ax[col, row].scatter(zi, x, c="k")
                ax[col, row].plot(zi, y_pred, ls="--", c="k")

            i += 1
            ax[col, row].tick_params(axis="both", which="major", labelsize=5)

    fig.text(0.5, 0.0, f"Normal order statistical medians (seed={seed})", ha="center")
    fig.text(0.0, 0.5, "Ordered data", va="center", rotation="vertical")
    fig.patch.set_facecolor("white")

    return fig


@docs.docstring_parameter(
    x_data=docs.X_DATA["type"],
    x_data_desc=docs.X_DATA["description"],
    alpha=docs.ALPHA["type"],
    alpha_desc=docs.ALPHA["description"],
    statistic=docs.STATISTIC["type"],
    statistic_desc=docs.STATISTIC["description"],
    critical=docs.CRITICAL["type"],
    critical_desc=docs.CRITICAL["description"],
    p_value=docs.P_VALUE["type"],
    p_value_desc=docs.P_VALUE["description"],
    conclusion=docs.CONCLUSION["type"],
    conclusion_desc=docs.CONCLUSION["description"],
    fi_ref=Filliben1975,
)
def fi_test(x_data, alpha=0.05):
    """This function applies the Filliben Normality test [1]_.

    Parameters
    ----------
    {x_data}
        {x_data_desc}
    {alpha}
        {alpha_desc}


    Returns
    -------
    result : tuple with
        {statistic}
            {statistic_desc}
        {critical}
            {critical_desc}
        {p_value}
            {p_value_desc}
        {conclusion}
            {conclusion_desc}


    Notes
    -----
    The test statistic (:math:`F_{{p}}`) is estimated through the correlation between the ordered data and the Normal statistical order:


    .. math::

            F_p = \\frac{{\\sum_{{i=1}}^n \\left(x_i - \\overline{{x}}\\right) \\left(z_i - \\overline{{z}}\\right)}}{{\\sqrt{{\\sum_{{i=1}}^n \\left( x_i - \\overline{{x}}\\right)^2 \\sum_{{i=1}}^n \\left( z_i - \\overline{{z}}\\right)^2}}}}

    where :math:`z_{{i}}` values are the z-score values of the corresponding experimental data (:math:`x_{{{{i}}}}`) value, and :math:`n` is the sample size.

    The correlation is estimated using :doc:`scipy.stats.pearsonr() <scipy:reference/generated/scipy.stats.pearsonr>`.

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
    .. [1] {fi_ref}


    Examples
    --------
    >>> from normtest import filliben
    >>> from scipy import stats
    >>> data = stats.norm.rvs(loc=0, scale=1, size=30, random_state=42)
    >>> result = filliben.fi_test(data)
    >>> print(result)
    Filliben(statistic=0.9905837698603658, critical=0.964, p_value=0.7791884930182895, conclusion='Fail to reject H₀')


    """

    uniform_order = _uniform_order_medians(x_data.size)
    zi = _normal_order_medians(uniform_order)
    x_data = np.sort(x_data)
    statistic = _statistic(x_data=x_data, zi=zi)
    critical_value = _critical_value(sample_size=x_data.size, alpha=alpha)
    p_value = _p_value(statistic=statistic, sample_size=x_data.size)

    # conclusion
    if statistic < critical_value:
        conclusion = constants.REJECTION
    else:
        conclusion = constants.ACCEPTATION

    result = namedtuple("Filliben", ("statistic", "critical", "p_value", "conclusion"))
    return result(statistic, critical_value, p_value, conclusion)


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
    fi_ref=Filliben1975,
)
class Filliben(AlphaManagement, SafeManagement):
    """This class instantiates an object to perform the Filliben Normality test [1]_.


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
        Applies the Filliben Normality test;
    dist_plot(axes, alphas=[0.10, 0.05, 0.01]):
        Generates `axis` with critical data from the Filliben Normality test;
    correlation_plot(axes)
        Generates an `axis` with the Filliben test correlation graph;
    line_up(seed=None, correct=False)
        Generates a `Figure` with the correlation graphs for the line up method;
    citation(export=False)
        Returns the Filliben's test reference;

    References
    ----------
    .. [1] {fi_ref}


    Examples
    --------
    >>> from normtest import Filliben
    >>> import numpy as np
    >>> x = np.array([6, 1, -4, 8, -2, 5, 0])
    >>> test = Filliben()
    >>> test.fit(x)
    >>> print(test.normality)
    Filliben(statistic=0.9854095718708367, critical=0.899, p_value=0.8889294725781878, conclusion='Fail to reject H₀')

    """

    def __init__(self, alpha=0.05, safe=True, **kwargs):
        """Initiates Filliben `class` inheriting the `AlphaManagement` and `SafeManagement` classes

        Attributes
        ----------
        class_name : "Filliben"
        conclusion : None
            This attribute is used to check whether the fit method was applied or not
        alpha : float
        safe : bool


        """
        super().__init__(alpha=alpha, safe=safe, **kwargs)
        self.class_name = "Filliben"
        self.conclusion = None  # for cheking if the fit was applied
        if safe:
            if alpha != 0.05:
                types.is_float(
                    value=alpha,
                    param_name="alpha",
                    kind="class",
                    kind_name=self.class_name,
                    stacklevel=4,
                    error=True,
                )
                critical = deepcopy(critical_values.FILLIBEN_CRITICAL)

                parameters.param_options(
                    alpha,
                    list(critical.keys())[1:],
                    param_name="alpha",
                    kind="class",
                    kind_name=self.class_name,
                    stacklevel=4,
                    error=True,
                )

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
    def fit(self, x_data):
        """This method applies the Filliben test.

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
        fi_test


        """
        method_name = "fit"
        if self.safe:
            types.is_numpy(
                value=x_data,
                param_name="x_data",
                kind="method",
                kind_name=method_name,
                stacklevel=4,
                error=True,
            )
            numpy_arrays.n_dimensions(
                array=x_data,
                param_name="x_data",
                ndim=1,
                kind="method",
                kind_name=method_name,
                stacklevel=4,
                error=True,
            )
            numpy_arrays.size_is_greater_than_lower(
                array=x_data,
                param_name="x_data",
                kind="method",
                kind_name=method_name,
                lower=4,
                inclusive=True,
                stacklevel=4,
                error=True,
            )

        result = fi_test(x_data=x_data, alpha=self.alpha)
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
    def dist_plot(self, axes, alphas=[0.10, 0.05, 0.01]):
        """This method generates an `axis` with critical data from the Filliben Normality test.

        Parameters
        ----------
        {axes}
            {axes_desc}
        alphas : list of floats, optional
            The significance level (:math:`\\alpha`) to draw the critical lines. Default is `[0.10, 0.05, 0.01]`;


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
            return "The Filliben Normality test was not performed yet.\nUse the 'fit' method to perform the test."
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
                # making a copy from original critical values
                critical = deepcopy(critical_values.FILLIBEN_CRITICAL)
                for alpha in alphas:
                    parameters.param_options(
                        option=alpha,
                        options=list(critical.keys())[1:],
                        param_name="alphas",
                        kind="method",
                        kind_name=method_name,
                        stacklevel=4,
                        error=True,
                    )

            return dist_plot(
                axes,
                test=(self.statistic, self.x_data.size),
                alphas=alphas,
            )

    @docs.docstring_parameter(
        axes=docs.AXES["type"],
        axes_desc=docs.AXES["description"],
    )
    def correlation_plot(self, axes):
        """This method creates an `axis` with the Filliben test correlation graph.

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
        if self.conclusion is None:
            return "The Filliben Normality test was not performed yet.\nUse the 'fit' method to perform the test."
        else:
            if self.safe:
                types.is_subplots(
                    value=axes,
                    param_name="axes",
                    kind="method",
                    kind_name="correlation_plot",
                    stacklevel=4,
                    error=True,
                )
            return correlation_plot(axes, self.x_data)

    def line_up(self, seed=None, correct=False):
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
            return "The Filliben Normality test was not performed yet.\nUse the 'fit' method to perform the test."
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

            return line_up(self.x_data, seed=seed, correct=correct)

    def citation(self, export=False):
        """This method returns the reference from Filliben's test, with the option to export the reference in `.bib` format.

        Parameters
        ----------
        export : bool
            Whether to export the reference as `Filliben1975.bib` file (`True`) or not (`False`, default);


        Returns
        -------
        reference : str
            The Filliben Test reference

        """
        return citation(export=export)

    def __str__(self):
        if self.conclusion is None:
            text = "The Filliben Normality test was not performed yet.\nUse the 'fit' method to perform the test."
            return text
        else:
            return self.conclusion

    def __repr__(self):
        return "Filliben Normality test"
