from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import List

import numpy as np

from heuristic.constants import DEPOT
from .Singleton import Singleton

class Problem(metaclass=Singleton):
    _instance: int

    _veh_num: int
    _veh_capacity: float
    _veh_spd: np.ndarray
    _veh_km_cost: np.ndarray
    
    _veh_tour_num: int
    _veh_tour_cost: np.ndarray
    
    _veh_shift_num: int
    _veh_shift_start: np.ndarray
    _veh_shift_end: np.ndarray
    _veh_shift_cost: np.ndarray
    
    _cust_num: int
    _cust_open_time: np.ndarray
    _cust_close_time: np.ndarray
    _cust_pickup_demand: np.ndarray
    _cust_deliver_demand: np.ndarray
    _cust_distances: np.ndarray
    
    _service_time: float

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

    @classmethod
    def from_file(cls, location: str) -> Problem:
        cls.clear()

        data = np.genfromtxt(location)

        problem = cls()

        problem._idx = int(data[0])


