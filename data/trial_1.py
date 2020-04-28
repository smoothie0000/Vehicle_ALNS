# Instance index
INSTANCE_INDEX = 1

# Vehicle information
VEH_NUM = 2                               # Maximum number of vehicles
VEH_CAPACITY = 100                        # Vehicle capacity
VEH_SPEED = [55, 55]                      # Average speed of vehicles
VEH_KM_COST = [0.5, 0.5]                  # Cost of vehicle per kilometer

VEH_TOUR_NUM = 3                          # Maximum number of tours. For example: following trip has 2 tours 0-1-2-0-3-4-5-0 whereas this tour has 3 tours 0-1-0-2-3-0-3-4-5-0.
VEH_TOUR_COST = [[500, 1, 1],
                 [500, 1, 1]]             # Fixed cost of vehicle for tour r

VEH_SHIFT_NUM = 3                         # Number of shifts
VEH_SHIFT_START = [0, 76.667, 153.33]     # Shift start time
VEH_SHIFT_END = [76.6669, 153.3299, 230]  # Shift end time
VEH_SHIFT_COST = [[1500, 2000, 2500],
                  [1500, 2000, 2500]]     # Fixed cost of vehicle for shift s (per hour)


# Customer information
CUST_NUM = 5                                    # Number of customers

CUST_OPEN_TIME = [34, 149, 116, 161, 50]        # Customer opening time
CUST_CLOSE_TIME = [44, 159, 126, 171, 60]       # Customer closing time

SERVICE_TIME = 0.14                             # Service time of loading or unloading per item. It is same for both vehicles.
CUST_PICKUP_DEMAND = [38, 12, 13, 5, 6]         # Pickup demand of the customers
CUST_DELIVERY_DEMAND = [26, 19, 13, 10, 7]      # Delivery demand of the customers

# Distance between nodes i and j (Node 0 is the depot)
#                 Depot      Node1       Node2     Node3       Node4       Node5
CUST_DISTANCES = [0,         20.62,      25,       22.36,      15.23,      18,            # Depot
                  20.62,     0,          41.23,    42.72,      32.2,       23.85,         # Node1
                  25,        41.23,      0,        25,         32.2,       20.22,         # Node2
                  22.36,     42.72,      25,       0,          14.56,      34.41,         # Node3
                  15.23,     32.2,       32.2,     14.56,      0,          32.56,         # Node4
                  18,        23.85,      20.22,    34.41,      32.56,      0]             # Node5
