from typing import List, Mapping
from classes import Literal, Clause
from util import purge_non_unit_clauses_with_literal, purge_literal
from copy import deepcopy


def get_unit_clauses(formula: List[Clause]) -> List[Clause]:
    """
    Returns a list of the unit clauses in `formula`
    """
    return [clause for clause in formula if len(clause.literals) == 1]


if __name__ == "__main__":
    # (x or x) is not valid, so we won't test clauses that have repetitive Literals.

    # (x or !x) is valid, however.
    plus_or_minus = [Clause("foo", [Literal(1, True), Literal(1, False)])]
    assert (get_unit_clauses(plus_or_minus) == [])

    # (x) and (!x or y) and (z)
    three_clauses = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, False), Literal(2, True)]),
        Clause("baz", [Literal(3, True)])
    ]
    unit_clauses = [Clause("foo", [Literal(1, True)]), Clause("baz", [Literal(3, True)])]
    assert (get_unit_clauses(three_clauses) == unit_clauses)


def do_unit_elimination(formula: List[Clause]) -> (List[Clause], Mapping[bool, int]):
    """
    For every unit clause with variable {+/-x} in formula, removes non-unit clauses containing {+/-x}, all literals that
    are {-/+x} (flipped sign!), and assigns x a boolean value according to its polarity. Returns a tuple with the
    modified formula and the mapping that was created.
    """
    known_values = {}
    unit_clauses = get_unit_clauses(formula)
    new_formula = deepcopy(formula)

    for unit in unit_clauses:
        unit_literal = unit.literals[0]
        flipped_literal = Literal(unit_literal.name, not unit_literal.sign)

        new_formula = purge_non_unit_clauses_with_literal(unit_literal, new_formula)
        new_formula = purge_literal(flipped_literal, new_formula)

        known_values[unit_literal.name] = unit_literal.sign

    return new_formula, known_values


if __name__ == "__main__":
    # (x) and (!x) -> () and ()
    opposite_two = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, False)])
    ]
    opposite_two_formula = [Clause("foo", []), Clause("bar", [])]
    assert(do_unit_elimination(opposite_two) == (opposite_two_formula, {1: False}))

    # (x) and (x or y) and (z or !x)
    true_three = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, True), Literal(2, True)]),
        Clause("baz", [Literal(3, True), Literal(1, False)])
    ]
    true_three_new_formula = [Clause("foo", [Literal(1, True)]), Clause("baz", [Literal(3, True)])]
    true_three_mapping = {1: True}
    assert(do_unit_elimination(true_three) == (true_three_new_formula, true_three_mapping))

    # Multiple unit clauses
    # (!x) and (!x or x) and (x or y) and (y)
    two_units = [
        Clause("foo", [Literal(1, False)]),
        Clause("bar", [Literal(1, False), Literal(1, True)]),
        Clause("baz", [Literal(1, True), Literal(2, True)]),
        Clause("buzz", [Literal(2, True)])
    ]
    two_units_new_formula = [
        Clause("foo", [Literal(1, False)]),
        Clause("baz", [Literal(2, True)]),
        Clause("buzz", [Literal(2, True)])
    ]
    two_units_mapping = {1: False, 2: True}
    assert(do_unit_elimination(two_units) == (two_units_new_formula, two_units_mapping))
