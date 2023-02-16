from Classes.OneDConstraint import OneDConstraint;
from Classes import OneDLinearProgram;

c4 = OneDConstraint(1,5)
c5 = OneDConstraint(-1,2)

lists=[c4,c5]

solution = OneDLinearProgram.solve_1d_linear_program(lists, True)
print(solution)

lists.append(OneDConstraint(1,3))
solution = OneDLinearProgram.solve_1d_linear_program(lists, True)
print(solution)

lists = [OneDConstraint(-1,-5),OneDConstraint(1,3)]
solution = OneDLinearProgram.solve_1d_linear_program(lists, True)
print(solution)
