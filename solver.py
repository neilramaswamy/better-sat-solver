import sys
from sat_io import read_input, print_output, comment
from time import time
from pure_elimination import do_pure_literal_elimination
from unit_elimination import do_unit_elimination
from util import has_empty_clause, has_no_clauses, propagate_known_value, pick_var, create_total_assignment
from classes import *


def partial_solve(known_values: Mapping[int, bool], formula: List[Clause]) -> Mapping[int, bool]:
    """
    Using the DPLL algorithm (unit elimination, pure literal elimination, and branching), creates a partial instance
    of boolean assignments that satisfies `formula`. If no such assignment exists (`formula` is UNSAT), then it returns
    None.
    """
    new_formula, unit_knowns = do_unit_elimination(formula)
    curr_formula, pure_knowns = do_pure_literal_elimination(new_formula)
    curr_values = {**known_values, **unit_knowns, **pure_knowns}

    if has_empty_clause(curr_formula):
        return None
    if has_no_clauses(curr_formula):
        return curr_values

    new_var = pick_var(curr_values, curr_formula)
    new_var_true_solution = partial_solve(curr_values, propagate_known_value(Literal(new_var, True), curr_formula))

    if new_var_true_solution is not None:
        return {**curr_values, **{new_var: True}}
    else:
        return partial_solve({**curr_values, **{new_var: False}}, propagate_known_value(Literal(new_var, False), curr_formula))


def solve(variables: List[str], formula: List[Clause]) -> Mapping[int, bool]:
    """
    Solves the `formula` by generating a partial instance with the DPLL algorithm and adjusting the output to be total.
    `variables` parameter is used to know which variables need to be assigned to create a total assignment.
    """
    partial_assignment = partial_solve({}, formula)
    return create_total_assignment(variables, partial_assignment)


def do_dpll(path: str) -> None:
    """
    Runs the DPLL algorithm on a valid CNF file (pointed to by `path`) and prints out relevant information, including
    the satisfiability, to standard output.
    """
    start = time()
    comment(f"solving {path}")

    variables, formula = read_input(path)

    answer = solve(variables, formula)
    print_output(answer)

    elapsed = round(time() - start, 3)
    comment(f"Finished in {elapsed}s")


if __name__ == "__main__":
    # do_dpll(sys.argv[1])
    do_dpll("/Users/neilramaswamy/PycharmProjects/sat-solver/tests/sat/sat2.cnf")
