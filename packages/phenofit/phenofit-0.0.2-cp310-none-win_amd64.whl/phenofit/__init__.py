import numpy as np
from .func_single_api import calculate_preseason_single
from .func_parallel_api import calculate_preseason_parallel


def calculate_preseason(y:np.ndarray, x:np.ndarray, **kwargs):
    """
    Calculate the optimal pre-season length for specified variables.

    Parameters:
    - y: np.ndarray, shape (years, 1)
      Target variable data over the years. such as phenological data at an annual scale.

    - x: np.ndarray, shape (months, vars)
      Explanatory variables data at a monthly scale, covering one more year than y data (months = 12 * (years + 1)).

    Keyword Arguments (kwargs):
    - max_month: int, default 6
      Maximum pre-season length calculated forward from the current month.

    - target_vars: list, default None
      variable names for calculating optimal pre-season length. Default --> x.columns.to_list().

    Returns:
    - result: pd.DataFrame
      Columns: ['n', 'r', 'CI95%', 'p-val', 'ops', 'var', 'index'], where ops is the optimal pre-season length.
    """
    
    
    return calculate_preseason_single(y, x, **kwargs)

