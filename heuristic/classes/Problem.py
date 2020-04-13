from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import List

import numpy as np

from heuristic.constants import DEPOT
from .Singleton import Singleton

class Problem(metaclass=Singleton):
    _instance: int

    _capacity: float
    _handling_cost: float

    _num_customers: int
    _num_stacks: int

    _distances: np.ndarray
    _demands: np.ndarray
    _pickups: np.ndarray

    @property
    def instance(self) -> int:
        return self._instance

    @property
    def capacity(self) -> float:
        return self._capacity

    @property
    def handling_cost(self) -> float:
        return self._handling_cost

    @property
    def num_customers(self) -> int:
        return self._num_customers

    @property
    def num_stacks(self) -> int:
        return self._num_stacks

    @property
    def distances(self) -> np.ndarray:
        return self._distances

    @property
    @lru_cache(1)
    def stack_capacity(self) -> float:
        return self.capacity / self.num_stacks

    @property
    @lru_cache(1)
    def nearest_customers(self) -> np.ndarray:
        """
        Returns the customers nearest to each other customer, as a matrix. Each
        row gives a customer, all columns values the nearest customers in
        increasing order.

        Note: first column is the customer itself, as the distance to self is
        zero.
        """
        return np.argsort(self.distances[1:, 1:], axis=1)

    @property
    @lru_cache(1)
    def smallest_quantity_customers(self) -> np.ndarray:
        """
        Returns the customers sorted by the smallest quantities of demand and
        pickup (summed), ascending.
        """
        return np.argsort(self._demands + self._pickups)

    @classmethod
    def from_file(cls, location: str, **kwargs) -> Problem:
        """
        Sets-up a problem instance from the passed-in data file location. Any
        additional arguments are passed to ``numpy.genfromtxt``. For the assumed
        file format, see the data in `/data` - in particular the text file.

        Parameters
        ----------
        location
            Data file location.
        kwargs
            Additional arguments.

        Returns
        -------
        Problem
            Problem instance for the data file.
        """
        cls.clear()

        data = np.genfromtxt(location, **kwargs)

        problem = cls()

        problem._instance = int(data[0])

        problem._capacity = data[1]
        problem._handling_cost = data[3]

        problem._num_customers = int(data[2])
        problem._num_stacks = int(data[4])

        # Distances include depot, so customers + 1
        distances = data[5:5 + (problem.num_customers + 1) ** 2]
        problem._distances = distances.reshape((problem.num_customers + 1,
                                                problem.num_customers + 1))