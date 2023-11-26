"""This module contains helpers functions and classes

##### List of functions (cte_alphabetical order) #####

## Functions WITH good TESTS ###

## Functions WITH some TESTS ###

## Functions WITHOUT tests ###



##### List of CLASS (alphabetical order) #####
## Functions WITH good TESTS ###

## Functions WITH some TESTS ###

## Functions WITHOUT tests ###


Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created : November 12, 2023

Last update: November 12, 2023
"""

##### IMPORTS #####

### Standard ###


### Third part ###

### self made ###
from paramcheckup import types, numbers

##### DOCUMENTATION #####
from normtest.utils import documentation as docs


#### CONSTANTS ####


##### CLASS #####


class SafeManagement:
    """Instanciates a class for `safe` management. It is primarily for internal use.


    Parameters
    ----------
    safe : bool, optional
        Whether to check the inputs before performing the calculations (`True`, default) or not (`False`). Useful for beginners to identify problems in data entry (may reduce algorithm execution time);


    """

    def __init__(self, safe=True, **kwargs):
        super().__init__(**kwargs)
        """Constructs the parameter `safe`


        Parameters
        ----------
        safe : bool, optional
            Whether to check the inputs before performing the calculations (`True`, default) or not (`False`). Useful for beginners to identify problems in data entry (may reduce algorithm execution time);


        """
        self.class_name = "SafeManagement"

        if safe is not True:
            types.is_bool(
                value=safe,
                param_name="safe",
                kind="class",
                kind_name=self.class_name,
                stacklevel=4,
                error=True,
            )
        self.safe = safe

    @docs.docstring_parameter(
        safe=docs.SAFE["type"],
        safe_desc=docs.SAFE["description"],
    )
    def get_safe(self):
        """Returns the current status of parameter `safe`


        Returns
        -------
        {safe}
            {safe_desc}


        """
        return self.safe

    @docs.docstring_parameter(
        safe=docs.SAFE["type"],
        safe_desc=docs.SAFE["description"],
    )
    def set_safe(self, safe):
        """Changes the current status of parameter `safe`


        Parameters
        ----------
        {safe}
            {safe_desc}


        """
        if safe is not True:
            types.is_bool(
                value=safe,
                param_name="safe",
                kind="class",
                kind_name=self.class_name,
                stacklevel=4,
                error=True,
            )
        self.safe = safe

    def __repr__(self):
        return self.safe

    def __str__(self):
        return f"The current state of parameter `safe` is '{self.safe}'"


class AlphaManagement:
    """Instanciates a class for `alpha` management. It is primarily for internal use.


    Parameters
    ----------
    alpha : float, optional
        The significance level (default is ``0.05``);


    Notes
    -----
    This method only allows input of type `float` and between ``0.0`` and ``1.0``.


    """

    def __init__(self, alpha=0.05, **kwargs):
        super().__init__(**kwargs)
        """Constructs the significance level value

        Parameters
        ----------
        alpha : float
            The significance level (default is ``0.05``);

        Notes
        -----
        This method only allows input of type `float` and between ``0.0`` and ``1.0``.

        """
        self.class_name = "AlphaManagement"

        if alpha != 0.05:
            types.is_float(
                value=alpha,
                param_name="alpha",
                kind="class",
                kind_name=self.class_name,
                stacklevel=4,
                error=True,
            )
            numbers.is_between_a_and_b(
                number=alpha,
                lower=0,
                upper=1,
                param_name="alpha",
                kind="class",
                kind_name=self.class_name,
                inclusive=False,
                stacklevel=4,
                error=True,
            )
        self.alpha = alpha

    def get_alpha(self):
        """Returns the current `alpha` value


        Returns
        -------
        alpha : float
            The level of significance (:math:`\\alpha`).

        """
        return self.alpha

    def set_alpha(self, alpha):
        """Changes the `alpha` value

        Parameters
        ----------
        alpha : float
            The level of significance (:math:`\\alpha`).

        Notes
        -----
        This method only allows input of type `float` and between ``0.0`` and ``1.0``.

        """
        types.is_float(
            value=alpha,
            param_name="alpha",
            kind="class",
            kind_name=self.class_name,
            stacklevel=4,
            error=True,
        )
        numbers.is_between_a_and_b(
            number=alpha,
            lower=0,
            upper=1,
            param_name="alpha",
            kind="class",
            kind_name=self.class_name,
            inclusive=False,
            stacklevel=4,
            error=True,
        )
        self.alpha = alpha

    def __repr__(self):
        return self.alpha

    def __str__(self):
        return f"The current significance level is '{self.alpha}'"


##### FUNCTIONS #####
