"""

We don't bundle pandas with our SDK, but we can still provide some pandas-specific
functions for users who have pandas installed and wish to seamlessly interoperate
Bauplan with Pandas workflows.

Note: if you add a function here, you must also wrap it with the pandas_import_checker
decorator to make sure we gracefully handle the case where pandas is not installed.

"""

from functools import wraps
from typing import Any

import pyarrow

from .query import query

#### Utility decorator ####


class MissingPandasError(Exception):
    def __init__(self):
        super().__init__('Pandas is not installed. Please do `pip3 install pandas` to resolve this error.')


def pandas_import_checker(f):
    """
    Decorator checks if pandas is installed before running the function.

    The user may have already pandas installed, so we don't bundle it
    with our SDK - however, if they don't have it, we should let them know
    that conversion to pandas object will not work!
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        # try import pandas first
        try:
            import pandas  # noqa
        except ModuleNotFoundError:
            raise MissingPandasError() from None
        # if pandas can be imported, run the function
        r = f(*args, **kwargs)
        return r
    return wrapped

#### Pandas-specific functions ####


@pandas_import_checker
def query_to_pandas(*args: Any, **kwargs: Any) -> Any:
    """
    This will return all the rows as a pandas DataFrame object to the client.
    """
    reader: pyarrow.flight.FlightStreamReader = query(*args, **kwargs)
    if reader is None:
        raise ValueError('No results found')
    return reader.read_pandas()
