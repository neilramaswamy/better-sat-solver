from classes import Literal, Clause
from typing import Mapping


def read_input(cnfFile: str):
    variableSet = []
    clauseSet = []
    nextCID = 0
    with open(cnfFile, "r") as f:
        for line in f.readlines():
            tokens = line.strip().split()
            if tokens and tokens[0] != "p" and tokens[0] != "c":
                literals = []
                for lit in tokens[:-1]:
                    sign = lit[0] != "-"
                    variable = lit.strip("-")

                    literals.append(Literal(variable, sign))
                    if variable not in variableSet:
                        variableSet.append(variable)

                clauseSet.append(Clause(nextCID, literals))
                nextCID += 1

    return variableSet, clauseSet


# Print the result in DIMACS format
def print_output(assignment: Mapping[int, bool]):
    result = ""
    isSat = (assignment is not None)
    if isSat:
        for var in assignment:
            result += " " + ("" if assignment[var] else "-") + str(var)

    print(f"s {'SATISFIABLE' if isSat else 'UNSATISFIABLE'}")
    if isSat:
        print(f"v{result} 0")


def comment(cmt: str) -> None:
    """
    Prints the comment `cmt` to standard output in accordance to the DIMACS format
    """
    print(f"c {cmt}")