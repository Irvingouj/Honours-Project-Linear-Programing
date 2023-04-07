from scipy.optimize import linprog

# Objective function coefficients
c = [-6.855287318328901e-17, -2.789539993132946e-16, -7.132699348773927]

# Constraint coefficients
A = [
    [-2.13, 14.22, -2.12],
    [-8.50, 4.36, -3.83],
    [1.39, -3.43, -14.27],
    [5.56, -3.67, -7.24]
]

# Constraint values
b = [-123.49, -315.39, -895.61, 684.44]

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b)

# Print the result
print(result)
