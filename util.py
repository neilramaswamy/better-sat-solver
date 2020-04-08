from classes import Literal, Clause
from typing import List, Set, Mapping
from copy import deepcopy
from collections import Counter

# A series of Clause/Literal manipulators and accessors.


def purge_literal(literal: Literal, formula: List[Clause]) -> List[Clause]:
    """
    Removes all instance of `literal` from all Clauses in `formula`
    """
    for clause in formula:
        clause.remove_literal(literal)

    return formula


if __name__ == "__main__":
    # (x) -x-> ()
    assert(purge_literal(Literal(1, True), [Clause("foo", [Literal(1, True)])]) == [Clause("foo", [])])

    # (x or !x) -x-> (!x)
    assert (purge_literal(Literal(1, True), [Clause("foo", [
        Literal(1, True), Literal(1, False)])]) == [Clause("foo", [Literal(1, False)])])

    # (x or y) -z-> (x or y)
    assert (purge_literal(Literal(3, True), [Clause("foo", [
        Literal(1, True), Literal(2, True)
    ])]) == [Clause("foo", [Literal(1, True), Literal(2, True)])])


def purge_clauses_with_literal(literal: Literal, formula: List[Clause]) -> List[Clause]:
    """
    Removes all clauses that contain `literal` from `formula` and returns the new formula. Should be used to simplify
    a formula after making a guess.
    """
    return [clause for clause in formula if literal not in clause.literals]


if __name__ == "__main__":
    # (x or y) AND (x or !y) -y-> (x or !y)
    # (x or y) AND (x or !y) -!y-> (x or y)
    test_1 = [
        Clause("foo", [Literal(1, True), Literal(2, True)]),
        Clause("bar", [Literal(1, True), Literal(2, False)])
    ]
    assert(purge_clauses_with_literal(Literal(2, True), test_1) == [Clause("bar", [Literal(1, True), Literal(2, False)])])
    assert(purge_clauses_with_literal(Literal(2, False), test_1) == [Clause("foo", [Literal(1, True), Literal(2, True)])])


def purge_non_unit_clauses_with_literal(literal: Literal, formula: List[Clause]) -> List[Clause]:
    """
    Removes all non-unit clauses that contain `literal` from `formula`, and returns the new formula. Should be used
    during unit elimination.
    """
    new_formula = []
    for clause in formula:
        is_unit = len(clause.literals) == 1
        not_contains_literal = literal not in clause.literals

        if is_unit or not_contains_literal:
            new_formula.append(clause)

    return new_formula


if __name__ == "__main__":
    # (x) and (x or y) and (z) -x> (x) and (z)
    test_1 = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, True), Literal(2, True)]),
        Clause("baz", [Literal(3, True)])
    ]
    result_1 = [
        Clause("foo", [Literal(1, True)]),
        Clause("baz", [Literal(3, True)])
    ]
    assert(purge_non_unit_clauses_with_literal(Literal(1, True), test_1) == result_1)

    # (x) and (!x or y) and (!x) -!x-> (x) and (!x)
    test_2 = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, False), Literal(2, True)]),
        Clause("baz", [Literal(1, False)])
    ]
    result_2 = [
        Clause("foo", [Literal(1, True)]),
        Clause("baz", [Literal(1, False)])
    ]
    assert(purge_non_unit_clauses_with_literal(Literal(1, False), test_2) == result_2)


def get_variables(formula: List[Clause]) -> List[int]:
    acc: Set[int] = set()

    for clause in formula:
        for literal in clause.literals:
            acc.add(literal.name)

    return list(acc)


if __name__ == "__main__":
    formula_1 = [
        Clause("foo", [Literal(1, True), Literal(1, False)]),
        Clause("bar", [Literal(2, False)]),
        Clause("baz", [Literal(3, True)])
    ]
    assert(Counter(get_variables(formula_1)) == Counter([1, 2, 3]))


def has_empty_clause(formula: List[Clause]) -> bool:
    """
    Returns whether there exists a clause in formula that has no literals
    """
    for clause in formula:
        if len(clause.literals) == 0:
            return True

    return False


def has_no_clauses(formula: List[Clause]) -> bool:
    """
    Returns whether there are no clauses in formula
    """
    return len(formula) == 0


def propagate_known_value(literal: Literal, formula: List[Clause]) -> List[Clause]:
    """
    Simplifies `formula` based on `literal`. If literal is +x, then any clauses containing +x can be removed and all
    -x literals can be removed. The simplified formula is returned.
    """
    clauses_purged = purge_clauses_with_literal(literal, deepcopy(formula))

    flipped_literal = Literal(literal.name, not literal.sign)
    both_purged = purge_literal(flipped_literal, clauses_purged)

    return both_purged


if __name__ == "__main__":
    # Testing propagation

    # (x)
    only_x = [Clause("foo", [Literal(1, True)])]
    assert(propagate_known_value(Literal(1, True), only_x) == [])

    # (x) and (x or y) and (z or !x)
    true_three = [
        Clause("foo", [Literal(1, True)]),
        Clause("bar", [Literal(1, True), Literal(2, True)]),
        Clause("baz", [Literal(3, True), Literal(1, False)])
    ]
    true_three_formula = [
        Clause("baz", [Literal(3, True)])
    ]
    assert(propagate_known_value(Literal(1, True), true_three) == true_three_formula)


def pick_var(var_assignment: Mapping[int, bool], formula: List[Clause]):
    """
    Returns a literal name from formula that is not already in `var_assignment`. Used in the solver when it needs to
    find a variable on which to branch.
    """
    for clause in formula:
        for literal in clause.literals:
            if var_assignment.get(literal.name) is None:
                return literal.name

    raise ValueError("Could not find new variable in formula")


def create_total_assignment(variables: List[str], partial_assignment: Mapping[int, bool]):
    """
    Creates a total variable assignment starting with the partial assignment `partial_assignment`. Variables that are
    not already assigned are assigned to True. If no partial assignment exists, that means that nothing could be
    inferred by DPLL, and the original formula is UNSAT.

    Function is needed because the DPLL algorithm provided gives partial instances, and modifying the algorithm wasn't
    ideal; as such, DPLL operates as something that returns a partial instance, and this function "fixes" it (i.e. makes
    it total).
    """
    if partial_assignment is None:
        return None
    for variable in variables:
        if partial_assignment.get(variable) is None:
            partial_assignment[variable] = True

    return partial_assignment


if __name__ == "__main__":
    # Verify nothing is added for UNSAT cases
    unsat_vars = ['1', '2', '3']
    assert(create_total_assignment(unsat_vars, None) == None)

    # Don't reassign
    one_var = ['1']
    one_var_partial = {'1': True}
    assert(create_total_assignment(one_var, one_var_partial) == one_var_partial)

    # Assign only variables that aren't already assigned
    all_vars = ['1', '2', '3', '4']
    all_partial = {'1': True, '4': False}
    all_total = {'1': True, '4': False, '2': True, '3': True}
    assert(create_total_assignment(all_vars, all_partial) == all_total)