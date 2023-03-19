from typing import List, Tuple
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
        flag = flag or constraint.direction() == Facing.RIGHT and constraint.value() > right
        
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


def solve_1d_linear_program_with_left_and_right_index(one_d_constraints: List[OneDConstraint], objective: bool) -> Tuple[float, int, int]:
    """
    Solves a one-dimensional linear programming problem with left and right indices.

    Args:
        one_d_constraints (List[OneDConstraint]): A list of one-dimensional constraints.
        objective (bool): A boolean value indicating the objective direction.
            If True, the objective is to maximize the value. Otherwise, it is to minimize.

    Returns:
        Tuple[float, int, int]: A tuple containing the solution to the problem and the left and right indices.
            If the problem is infeasible, the solution is None and the indices indicate the violating constraints.
    """
    left = float('-inf')
    right = float('inf')
    
    left_idx = -1
    right_idx = -1



    used_constraints = []
    for idx,constraint in enumerate(one_d_constraints):
        if constraint.direction() == Facing.LEFT and constraint.value() < left:
            right_idx = idx
            return None,right_idx,left_idx
        elif constraint.direction() == Facing.RIGHT and constraint.value() > right:
            left_idx = idx
            return None,right_idx,left_idx
        
        
        
        if (constraint.direction() == Facing.LEFT):
            if constraint.value() < right:
                right_idx = idx
                right = constraint.value()
        else:
            if constraint.value() > left:
                left_idx = idx
                left = constraint.value()

        used_constraints.append(constraint)
        
      
    return right if objective == POSITIVE else left  , right_idx, left_idx

