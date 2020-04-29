import operator
from copy import deepcopy
from itertools import islice, takewhile, tee
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from heuristic.constants import DEPOT
from .Item import Item
from .Problem import Problem
from .SetList import SetList
from .Stacks import Stacks


class Route:
    __slots__ = ['customers', 'plan', '_route_cost', '_handling_cost']

    customers: SetList[int]  # visited customers
    schedule: SetList[float]
    load: SetList[int]
    vehicle_id: int # vehicle ID

    # 0 -> 1 -> 2 -> 0
    _route_cost: Optional[float]  # cached results

    def __init__(self,
                 customers: Union[List[int], SetList[int]],
                 schedule: Union[List[float], SetList[float]],
                 vehicle_id: int):
        self.customers = SetList(customers)
        self.schedule = SetList(schedule)
        self.vehicle_id = vehicle_id

        self._route_cost = None

    def __contains__(self, customer: int) -> bool:
        return customer in self.customers

    def __len__(self):
        return len(self.customers)

    def __iter__(self):
        yield from self.customers

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
        if self._route_cost is None:
            route = [DEPOT] + self.customers.to_list() + [DEPOT]
            self._route_cost = Route.distance(route)

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

        return sum(problem.veh_km_cost[self.vehicle_id] * problem.distances[first + 1, second + 1]
                   for first, second in zip(from_custs, to_custs))

        '''
          Solution:
          1. delivery should satisfy the customer demands
          2. pickup should satisfy the customer demands
          3. each customer should be visited at least once

          Route:
          1. the tour must be consecutive
          2. each tour should start and end in the depot
          3. start time and end time for one tour should be within the same shift interval
          4. vehicle capacity can never be exceeded
        '''

    def insert_customer(self, customer: int, at: int):
        """
        Inserts customer in route at index at. Inserts customer delivery and
        pickup items into the appropriate parts of the loading plan. Assumes it
        is feasible to do so.
        """
        problem = Problem()

        self.customers.insert(at, customer)
        self.plan.insert(at + 1, deepcopy(self.plan[at]))

        # Inserts customer delivery item into the loading plan. The stack to
        # insert into is the shortest stack at the depot (since the delivery
        # item is carried from the depot to the customer).
        stack_idx = self.plan[0].shortest_stack().index
        delivery = problem.demands[customer]

        for plan in self.plan[:at + 1]:
            plan[stack_idx].push_rear(delivery)

        pickup = problem.pickups[customer]
        stack = self.plan[at + 1].shortest_stack()

        # Pickups in the front (these are never moved, so we might want to
        # insert our pick-up item just after them, nearer to the rear).
        front = list(takewhile(lambda item: item.is_pickup(), reversed(stack)))

        # The pickup item will have to be moved for each delivery item that's
        # currently in the stack, if we insert it in the rear.
        volume = stack.deliveries_in_stack() * pickup.volume

        # Tests if placing the pick-up item near the front is cheaper than
        # inserting it in the rear. The former incurs costs *now*, whereas for
        # the latter the item might have to move at later points in the tour.
        if stack.volume() - sum(item.volume for item in front) < volume:
            # It is also best to move any pickup items that are not already
            # near the front, as those are to be moved now anyway.
            pickups = [item for item in islice(stack, len(stack) - len(front))
                       if item.is_pickup()]

            for plan in self.plan[at + 1:]:
                for item in pickups:
                    plan[stack.index].remove(item)
                    plan[stack.index].push(-len(front), item)

                plan[stack.index].push(-len(front), pickup)
        else:
            for plan in self.plan[at + 1:]:
                plan[stack.index].push_rear(pickup)

        self._update_routing_cost(customer, at, "insert")

    def remove_customer(self, customer: int):
        """
        Removes the passed-in customer from this route, and updates the
        loading plan to reflect this change. O(n * m), where n is the tour
        length, and m the length of the longest stack (in number of items).
        """
        problem = Problem()

        delivery = problem.demands[customer]
        pickup = problem.pickups[customer]

        idx = self.customers.index(customer)

        self._update_routing_cost(customer, idx, "remove")

        for stacks in self.plan[:idx + 1]:
            stacks.find_stack(delivery).remove(delivery)

        for stacks in self.plan[idx + 1:]:
            stacks.find_stack(pickup).remove(pickup)

        del self.customers[idx]
        del self.plan[idx + 1]

    def __str__(self):
        customers = np.array([DEPOT] + self.customers.to_list() + [DEPOT])
        customers += 1

        return f"{customers}, {self.plan}"

    def __repr__(self):
        return f"Route({self})"
