from ortools.linear_solver import pywraplp

def solve_with_os_tool(file):
    pass

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return
    
    x = solver.NumVar(0, solver.infinity(), 'x')
    y = solver.NumVar(0, solver.infinity(), 'y')
    # Constraint 0: x + 2y <= 14.
    # Constraint 0: x + 2y <= 14.

    solver.Add(eval("x + 2 * y <= 14.0"))

    # Constraint 1: 3x - y >= 0.
    solver.Add(3 * x - y >= 0.0)

    # Constraint 2: x - y <= 2.
    solver.Add(x - y <= 2.0)

    solver.Maximize(3 * x + 4 * y)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('x =', x.solution_value())
        print('y =', y.solution_value())
    else:
        print('The problem does not have an optimal solution.')

    print('Number of constraints =', solver.NumConstraints())

    print('Number of variables =', solver.NumVariables())

if __name__ == "__main__":
    main()