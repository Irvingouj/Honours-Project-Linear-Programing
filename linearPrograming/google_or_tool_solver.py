from ortools.linear_solver import pywraplp

def solve_with_os_tool(file):
    pass

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return
    
    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')
    # Constraint 0: x + 2y <= 14.
    # Constraint 0: x + 2y <= 14.

    solver.Add(6*x-2*y<=-10)

    # Constraint 1: 3x - y >= 0.
    solver.Add(12*x + 9*y >=10)

    # Constraint 2: x - y <= 2.
    solver.Add(-3*x + 6*y <=100)

    solver.Minimize(5*x-3*y)

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