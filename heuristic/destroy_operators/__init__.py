from typing import Callable, List

from numpy.random import RandomState

from heuristic.classes import Solution
from .cross_route import cross_route

D_OPERATORS: List[Callable[[Solution, RandomState], Solution]] = [
    random_customers,
]
