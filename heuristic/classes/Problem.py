from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import List

import numpy as np
import importlib.util

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
    def veh_num(self) -> int:
        return self._veh_num

    @property
    def veh_capacity(self) -> float:
        return self._veh_capacity

    @property
    def veh_spd(self) -> np.ndarray:
        return self._veh_spd

    @property
    def veh_km_cost(self) -> np.ndarray:
        return self._veh_km_cost

    @property
    def veh_tour_num(self) -> int:
        return self._veh_tour_num

    @property
    def veh_tour_cost(self) -> np.ndarray:
        return self._veh_tour_cost

    @property
    def veh_shift_num(self) -> int:
        return self._veh_shift_num

    @property
    def veh_shift_start(self) -> np.ndarray:
        return self._veh_shift_start

    @property
    def veh_shift_end(self) -> np.ndarray:
        return self._veh_shift_end

    @property
    def veh_shift_cost(self) -> np.ndarray:
        return self._veh_shift_cost

    @property
    def cust_num(self) -> int:
        return self._cust_num

    @property
    def cust_open_time(self) -> np.ndarray:
        return self._cust_open_time

    @property
    def cust_close_time(self) -> np.ndarray:
        return self._cust_close_time

    @property
    def cust_pickup_demand(self) -> np.ndarray:
        return self._cust_pickup_demand

    @property
    def cust_deliver_demand(self) -> np.ndarray:
        return self._cust_deliver_demand

    @property
    def cust_distances(self) -> np.ndarray:
        return self._cust_distances

    @property
    def service_time(self) -> float:
        return self._service_time

    @property
    def distances(self) -> np.ndarray:
        return self._distances

    @classmethod
    def from_file(cls, location: str) -> Problem:
        cls.clear()

        spec = importlib.util.spec_from_file_location('data', location)
        data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data)

        problem = cls()

        problem._instance = int(data.INSTANCE_INDEX)

        problem._veh_num = int(data.VEH_NUM)
        problem._veh_capacity = int(data.VEH_CAPACITY)
        problem._veh_spd = data.VEH_SPEED
        problem._veh_km_cost = data.VEH_KM_COST

        problem._veh_tour_num = int(data.VEH_TOUR_NUM)
        problem._veh_tour_cost = data.VEH_TOUR_COST

        problem._veh_shift_num = int(data.VEH_SHIFT_NUM)
        problem._veh_shift_start = data.VEH_SHIFT_START
        problem._veh_shift_end = data.VEH_SHIFT_END
        problem._veh_shift_cost = data.VEH_SHIFT_COST

        problem._cust_num = int(data.CUST_NUM)

        problem._cust_open_time = data.CUST_OPEN_TIME
        problem._cust_close_time = data.CUST_CLOSE_TIME

        problem._cust_pickup_demand = data.CUST_PICKUP_DEMAND
        problem._cust_delivery_demand = data.CUST_DELIVERY_DEMAND

        problem._cust_distances = data.CUST_DISTANCES

        problem._service_time = float(data.SERVICE_TIME)
