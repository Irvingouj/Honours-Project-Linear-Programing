from typing import List
from linear_programming.utils.exceptions import NoSolutionException
from .oneDConstraint import Facing, OneDConstraint

POSITIVE = True
NEGATIVE = False


# debugging purpose, will be removed
def sol_1d_linear_program_with_os(one_d_constraints: List[OneDConstraint], objective: bool) -> float:
    from linear_programming.classes.osToolSolver import OsToolSolver
    return OsToolSolver().solve_one_dimension(one_d_constraints=one_d_constraints, objective=objective)
    


def solve_1d_linear_program(one_d_constraints: List[OneDConstraint], objective: bool) -> float:

    left = float('-inf')
    right = float('inf')

    def raise_for_violation(constraint: OneDConstraint):
        flag = constraint.direction() == Facing.LEFT and constraint.value() < left
        flag = constraint.direction() == Facing.RIGHT and constraint.value() > right
        
        # debugging purpose, I only need add 1 breakpoint here
        if flag:
            raise NoSolutionException(
                "No solution as one dimension linear program is infeasible")

    used_constraints = []
    for constraint in one_d_constraints:
        raise_for_violation(constraint)
        if (constraint.direction() == Facing.LEFT):
            right = min(right, constraint.value())
        else:
            left = max(left, constraint.value())

        used_constraints.append(constraint)
      
    return right if objective == POSITIVE else left  

