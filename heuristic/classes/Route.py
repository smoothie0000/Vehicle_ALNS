import operator
from copy import deepcopy
from itertools import islice, takewhile, tee
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from heuristic.constants import DEPOT
from .Problem import Problem


class Route:
    __slots__ = ['customers', 'plan', '_route_cost', '_handling_cost']

    customers: List[int]  # visited customers
    schedule: List[float]
    load: List[int]
    plan: List[list]
    vehicle_id: int # vehicle ID

    # 0 -> 1 -> 2 -> 0
    _route_cost: Optional[float]  # cached results

    def __init__(self, customers: List[int], schedule: List[float],
                 load: List[int], plan: List[list], vehicle_id: int):
        self.customers = customers
        self.schedule = schedule
        self.load = load
        self.plan = plan
        self.vehicle_id = vehicle_id

        self._route_cost = None

        if not self.can_insert():
            raise Exception('Invalid solution for the route.')

    def cost(self) -> float:
        """
        Returns the cost (objective) value of this route, based on the
        distance and handling costs.
        """
        return self.routing_cost()

    def routing_cost(self) -> float:
        """
        Determines the route cost connecting this route's customers, and the
        DEPOT. O(1).
        """
        _distance = 0
        problem = Problem()

        if self._route_cost is None:
            route = self.customers
            _distance = Route.distance(route)

        self._route_cost = problem.veh_km_cost[self.vehicle_id] * _distance
        return self._route_cost

    def distance(self, customers: List[int]) -> float:
        """
        Computes the distance for the passed-in list of visited customer nodes.
        Does not assume this list forms a tour. O(|customers|).
        """
        problem = Problem()

        # Constructs two iterators from the passed-in customers. This is fairly
        # efficient, as it avoids copying.
        from_custs, to_custs = tee(customers)
        next(to_custs, None)

        return sum(problem.distances[first + 1, second + 1]
                   for first, second in zip(from_custs, to_custs))

    def insert_customer(self, customer: int, at: int, plan: list):
        ##########self.customers.insert(at, customer)
        ##########self.plan.insert(at, plan)

        self._update_schedule()
        self._update_load()

        return self.can_insert()

    def remove_customer(self, customer: int, at: int):
        #########self.customers.insert(at, customer)
        #########self.plan.insert(at, plan)

        self._update_schedule()
        self._update_load()

        return self.can_insert()

    def _update_schedule(self):
        problem = Problem()

        self.schedule = [self.schedule[0]]

        for index in range(len(self.customers)):
            customer = self.customers[index]

            loads_to_handle = self.plan[customer][0] + self.plan[customer][1]
            service_time = problem.SERVICE_TIME * loads_to_handle

            arrival_time = self.schedule[customer]
            leave_time = arrival_time + service_time

            # calculate next arrival time
            if index < len(self.customers) - 1:
                next_customer = self.customers[index + 1]
                distance = problem.distances[customer, next_customer]
                vehicle_speed = problem.VEH_SPEED[self.vehicle_id]
                drive_time = distance / vehicle_speed
                next_arrival_time = leave_time + drive_time
                next_open_time = problem.CUST_OPEN_TIME[next_customer]

                if next_arrival_time < next_open_time:
                    next_arrival_time = next_open_time
                self.schedule.append(next_arrival_time)

    def _update_load(self):
        self.load = [self.load[0]]
        for index in range(len(self.plan)):
            plan = self.plan[index]
            delivery = plan[0]
            pickup = plan[1]

            new_load = self.load[index] - delivery + pickup
            self.load.append(new_load)

    def can_insert(self):
        result = True
        result = result and self._validate_customers()
        result = result and self._validate_schedule()
        result = result and self._validate_load()
        result = result and self._validate_plan()
        return result

    def _validate_customers(self):
        if self.customers[0] == DEPOT and self.customers[-1] == DEPOT:
            return True
        return False

    def _validate_schedule(self):
        problem = Problem()

        result = True
        for index in range(len(self.customers)):
            customer = self.customers[index]

            arrival_time = self.schedule[customer]
            loads_to_handle = self.plan[customer][0] + self.plan[customer][1]
            service_time = problem.SERVICE_TIME * loads_to_handle
            leave_time = arrival_time + service_time

            open_time = problem.CUST_OPEN_TIME[customer]
            close_time = problem.CUST_CLOSE_TIME[customer]

            if open_time > arrival_time or close_time < leave_time:
                result = False
                break

            # validate next arrival time
            if index < len(self.customers) - 1:
                next_customer = self.customers[index + 1]
                distance = problem.distances[customer, next_customer]
                vehicle_speed = problem.VEH_SPEED[self.vehicle_id]
                drive_time = distance / vehicle_speed
                next_arrival_time = leave_time + drive_time
                next_customer_arrival_time = self.schedule[index + 1]

                if leave_time + drive_time > next_customer_arrival_time:
                    result = False
                    break

        return result

    def _validate_load(self):
        result = True

        for index in range(len(self.plan)):
            plan = self.plan[index]
            delivery = plan[0]
            pickup = plan[1]

            if self.load[index] - delivery + pickup != self.load[index + 1]:
                result = False
                break

        return result

    def _validate_plan(self):
        problem = Problem()

        delivery_demand = problem.CUST_DELIVERY_DEMAND
        pickup_demand = problem.CUST_PICKUP_DEMAND

        result = True
        for plan in self.plan:
            if plan[0] > delivery_demand or plan[1] > pickup_demand:
                result = False
                break

        return result
