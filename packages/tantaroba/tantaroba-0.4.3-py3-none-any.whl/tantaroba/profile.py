from typing import Callable
from time import time
from datetime import timedelta
import logging


def simple_profile(function: Callable):
    """
    Decorator function that logs the execution time of the decorated function.

    Microseconds precision.

    Args:
        function (Callable): funtion to profile
    """

    def simple_profile_wrapper(*args, **kwargs):
        start = time()
        function(*args, **kwargs)
        end = time()
        execution_time = end - start
        logging.info(
            f"Function '{function.__name__}', execution time: {timedelta(microseconds=int(execution_time * 1000000))}"
        )

    return simple_profile_wrapper
