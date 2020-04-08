from typing import List, Mapping


class Literal:
    def __init__(self, name: int, sign: bool):
        self.name = name  # integer
        self.sign = sign  # boolean

    def __repr__(self):
        return ("-" if not self.sign else "") + str(self.name)

    def __eq__(self, other):
        if type(other) != Literal:
            return False
        return self.name == other.name and self.sign == other.sign

    def __hash__(self):
        return hash((self.name, self.sign))


class Clause:
    def __init__(self, id, literals: List[Literal]):
        self.id = id
        self.literals = literals

    def __repr__(self):
        return f"{self.id}: {str(self.literals)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return self.id == other.id

    def remove_literal(self, literal: Literal):
        self.literals = [l for l in self.literals if not l == literal]

    def eval(self, assignments: Mapping[int, bool]) -> bool:
        result = False
        for literal in self.literals:
            value = assignments.get(literal.name)
            if value is None:
                raise ValueError(f"No assignment for clause literal {literal.name}")
            else:
                evaluation = not (literal.sign ^ value)
                result = result or evaluation

        return result


if __name__ == "__main__":
    two_vars_one_expr = Clause("first", [Literal(1, False), Literal(2, True)])

    mapping_one = {1: True, 2: True}
    mapping_two = {1: True, 2: False}
    mapping_four = {1: False, 2: False}

    assert(two_vars_one_expr.eval(mapping_one))
    assert (not two_vars_one_expr.eval(mapping_two))
    assert(two_vars_one_expr.eval(mapping_four))
