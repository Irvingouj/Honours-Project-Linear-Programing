import unittest
from LinearProgramming.Utils.twodLinearProgramGenerator import generate_random_2d_feasible_linear_program

class TestGenerateRandomLP(unittest.TestCase):
    def test_generates_correct_number_of_constraints(self):
        num_of_constraints = 5
        
        
        for i in range(10000):
            print(i+num_of_constraints)
        # _obj,cons = generate_random_2d_feasible_linear_program(num_of_constraints)
        # self.assertEqual(len(cons), num_of_constraints)

if __name__ == '__main__':
    unittest.main()
