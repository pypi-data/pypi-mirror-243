<img src="https://raw.githubusercontent.com/puzzle-in-a-mug/normtest/main/docs/_static/favicon-180x180.png" align="right" />

# normtest



This package has a series of tests used to check whether a set of sample data follows, at least approximately, the Normal distribution.

## Available tests (25/11/2023)

- Filliben
- Ryan-Joiner
- Looney-Gulledge


## Install

```
pip install normtest
```

## Usage

Each test has its own class and can be imported as follows:

```python
from normtest import RyanJoiner
from normtest import Filliben
from normtest import LooneyGulledge
```

To perform the test, just instantiate the class and apply the ``fit`` method, passing the data set as a ``NumpyArray``. For example:

```python
import numpy as np
test = RyanJoiner()
x_data = np.array([6, 1, -4, 8, -2, 5, 0])
test.fit(x_data)
```


After the ``fit`` method is applied, the ``test`` ``object`` now has a series of attributes with the test results. The main attribute is ``test.normality``, which contains the summarized results:

```python
print(test.normality)
RyanJoiner(statistic=0.9844829186140105, critical=0.8977794003662074, p_value='p > 0.100', conclusion='Fail to reject H₀')
```

The ``test`` ``object`` also has methods for graphical visualization of results, such as the ``line_up`` method. See the [documentation](https://normtest.readthedocs.io/en/latest/source/ryan_joiner/RyanJoiner.html) for details.


Each test has its individual module, and functions can be accessed through the modules. To import the module that contains all the RyanJoiner test functions, for example, use:

```python
from normtest import ryan_joiner
```

This way, it is possible to generate graphs and obtain intermediate values from the test calculations. For example:

```python
size = 7
pi = ryan_joiner._order_statistic(size)
print(pi)
[0.0862069  0.22413793 0.36206897 0.5        0.63793103 0.77586207
 0.9137931 ]
```




## License

- [BSD 3-Clause License](https://github.com/puzzle-in-a-mug/normtest/blob/main/LICENSE)
