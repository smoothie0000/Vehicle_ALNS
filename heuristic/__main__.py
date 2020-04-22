import sys

from alns import ALNS
from numpy.random import default_rng

from .classes import Problem


def main():
    if len(sys.argv) < 2:
        raise ValueError(f"{sys.argv[0]}: expected file location.")

    problem = Problem.from_file(sys.argv[1])

    alns = ALNS(default_rng(problem.instance))

'''
    for op in D_OPERATORS:
        alns.add_destroy_operator(op)

    for op in R_OPERATORS:
        alns.add_repair_operator(op)
'''


if __name__ == "__main__":
    main()
