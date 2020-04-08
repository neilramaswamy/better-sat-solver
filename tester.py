from solver import solve
from sat_io import read_input
from typing import List, Mapping
from classes import *
from os import listdir, path

UNSAT_TESTS_PATH = "./tests/unsat/"
SAT_TESTS_PATH = "./tests/sat/"

# Testing methodology: verify that every example in ./tests/sat is satisfiable and that the produced assignment results
# in the formula actually being true. It will also verify that every example in ./tests/unsat is UNSAT; however, it will
# not verify that this is the case, as that would require exhaustive checking. The logic here is that we can
# consistently classify (AND verify!) SAT cases and simply classify UNSAT cases, we probably have a working
# implementation.

# Some of the formulas in ./tests/sat/ were generated using the `cnfgen` Python library via the command line. These are
# pre-generated so that I didn't have to worry about giving pip instructions to you, the grader, or automating
# dependency installation on department machines.


def verify_unsat():
    for filename in listdir(UNSAT_TESTS_PATH):
        rel_path = path.join(UNSAT_TESTS_PATH, filename)
        variables, formula = read_input(rel_path)

        assignment = solve(variables, formula)
        if assignment is not None:
            raise ValueError(f"UNSAT file {filename} had a non-None assignment")

    print("UNSAT examples were all verified to be UNSAT")


def verify_sat():
    for filename in listdir(SAT_TESTS_PATH):
        rel_path = path.join(SAT_TESTS_PATH, filename)
        variables, formula = read_input(rel_path)

        assignment = solve(variables, formula)
        if assignment is None:
            raise ValueError(f"SAT file {filename} was said to be UNSAT")

        is_assignment_correct = verify_assignment(assignment, formula)
        if not is_assignment_correct:
            raise ValueError(f"Incorrect variable assignment produced for {filename}")

    print("SAT examples were verified and their assignments were correct")


def verify_assignment(assignments: Mapping[int, bool], formula: List[Clause]) -> bool:
    """
    Verifies that every clause in formula, using the assignments from `assignments`, is True. This should be used to
    check output from SAT scenarios.
    """
    for clause in formula:
        is_true = clause.eval(assignments)
        if not is_true:
            return False

    return True


if __name__ == "__main__":
    print("Starting verification of UNSAT instances...")
    verify_unsat()
    print("Starting verification of SAT instances...")
    verify_sat()