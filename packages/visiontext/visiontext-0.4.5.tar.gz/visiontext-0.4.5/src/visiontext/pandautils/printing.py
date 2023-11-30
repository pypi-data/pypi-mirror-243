import pandas as pd
from contextlib import contextmanager


@contextmanager
def full_pandas_display(max_rows=None, max_columns=None, max_colwidth=None, width=None, expand_frame_repr=False):
    """
    A context manager for setting various pandas display options to their
    maximum values so that the output is not truncated when printed.
    """
    with pd.option_context(
        "display.max_rows",
        max_rows,
        "display.max_columns",
        max_columns,
        "display.max_colwidth",
        max_colwidth,
        "display.width",
        width,
        "display.expand_frame_repr",
        expand_frame_repr,
    ):
        yield


@contextmanager
def pandas_float_format(fmt="{:.2f}"):
    with pd.option_context("display.float_format", fmt.format):
        yield
