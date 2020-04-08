from classes import Literal, Clause
from typing import List, Mapping
from copy import deepcopy
from util import get_variables, purge_clauses_with_literal


def get_variable_purity(target: int, formula: List[Clause]) -> bool:
    """
    If variable has only one polarity throughout formula, returns the polarity of `literal`. Otherwise, returns None.
    """
    polarity = None

    for clause in formula:
        for literal in clause.literals:
            if target == literal.name:
                if polarity is None:
                    polarity = literal.sign
                else:
                    if not polarity == literal.sign:
                        return None

    return polarity


if __name__ == "__main__":
    # (!x)
    assert(get_variable_purity(1, [Clause("foo", [Literal(1, False)])]) is False)

    # (x or !z) AND (!z or x)
    everything_pure = [
        Clause("foo", [Literal(1, True), Literal(3, False)]),
        Clause("bar", [Literal(3, False), Literal(1, True)])
    ]
    assert(get_variable_purity(1, everything_pure))
    assert(get_variable_purity(3, everything_pure) is False)

    # (x or y) AND (!x or !y). Ensure global purity, not clausal purity.
    global_purity_check = [
        Clause("foo", [Literal(1, True), Literal(2, True)]),
        Clause("bar", [Literal(1, False), Literal(2, False)])
    ]
    assert(get_variable_purity(1, global_purity_check) is None)
    assert (get_variable_purity(2, global_purity_check) is None)


def do_pure_literal_elimination(formula: List[Clause]) -> (List[Clause], Mapping[int, bool]):
    known_mapping: Mapping[int, bool] = {}
    new_formula = deepcopy(formula)

    variables = get_variables(formula)
    for variable in variables:
        # Check variable purity on original formula because variables might get removed during purging. Purity does not
        # change across purges, so we're safe to use the original formula.
        variable_purity = get_variable_purity(variable, formula)
        if variable_purity is not None:
            new_formula = purge_clauses_with_literal(Literal(variable, variable_purity), new_formula)
            known_mapping[variable] = variable_purity

    return new_formula, known_mapping


if __name__ == "__main__":
    # (x) and (x)
    two_same = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, True)])
    ]
    two_same_new_formula = []
    two_same_mapping = {1: True}
    assert(do_pure_literal_elimination(two_same) == (two_same_new_formula, two_same_mapping))

    # (x) and (!x)
    two_opposite = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, False)])
    ]
    assert(do_pure_literal_elimination(two_opposite) == (two_opposite, {}))

    # (x) and (x or y) and (z) and (!z)
    three_vars_one_pure = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, True), Literal(2, True)]),
        Clause("baz", [Literal(3, True)]),
        Clause("buzz", [Literal(3, False)])
    ]
    tvop_new_formula = [
        Clause("baz", [Literal(3, True)]),
        Clause("buzz", [Literal(3, False)])
    ]
    tvop_mapping = {1: True, 2: True}
    assert(do_pure_literal_elimination(three_vars_one_pure) == (tvop_new_formula, tvop_mapping))