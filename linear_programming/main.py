from argparse import ArgumentParser
import linear_programming.utils.linear_program_generator as gen
import linear_programming.utils.problem_writer as writer
import linear_programming.utils.problem_reader as reader
import linear_programming.solvers as solvers
import linear_programming.utils.compare_time as compare_time
from linear_programming.utils.problem_reader import ProblemType



def main():
    parser = ArgumentParser(prog='linear_programming',
                            description='Honours Project for Irving Ou')

    subparsers = parser.add_subparsers(
        help=r'user {positional argument} -h for further help ', dest='command')

    gen_parser = subparsers.add_parser('generate', help='Generate a linear program')

    gen_parser.add_argument('-n', '--num_constrains', type=int)
    gen_parser.add_argument('-t', '--type', type=str,choices=['bounded','infeasible','unbounded'])
    gen_parser.add_argument('-d', '--dimension', type=int,default=2)
    gen_parser.add_argument('-f', '--file_path', type=str, default="program.txt")

    solve_parser = subparsers.add_parser('solve', help='Solve a linear program')
    solve_parser.add_argument('-f', '--file_path', type=str)
    solve_parser.add_argument('-s', '--solver', type=str,choices=['Convex','OrTool'],default='Convex')
    
    test_parser = subparsers.add_parser('test', help='Test randomly generated linear programs for n in range, default range is 10 to 3000 with step 100')
    test_parser.add_argument('-s', '--start', type=int,default=10)
    test_parser.add_argument('-e', '--end', type=int,default=3000)
    test_parser.add_argument('-p', '--step', type=int,default=100)
    test_parser.add_argument('-t', '--type', type=str,choices=['bounded','infeasible','unbounded'])
    test_parser.add_argument('-o', '--output_path', type=str,default="result.txt")
    test_parser.add_argument('-d', '--dimension', type=int,default=2)
    

    args = parser.parse_args()

    if args.command == 'generate' and args.dimension == 2:
        program = None
        if args.type == 'unbounded':
            program = gen.gen_random_2d_unbounded(args.num_constrains)
        elif args.type == 'infeasible':
            program = gen.gen_random_2d_infeasible(args.num_constrains)
        elif args.type == 'bounded':
            # feasible not necessarily bounded, need to fix :TODO
            program = gen.gen_random_2d_feasible(args.num_constrains)
        else:
            raise ValueError('invalid type')
        
        path = writer.write(args.file_path,(program[0],program[1]))

        print(f"Generated file: {path}")
    elif args.command == 'generate' and args.dimension == 3:
        program = None
        if args.type == 'unbounded':
            program = gen.gen_random_3d_unbounded(args.num_constrains)
        elif args.type == 'infeasible':
            program = gen.gen_random_3d_infeasible(args.num_constrains)
        elif args.type == 'bounded':
            program = gen.gen_random_3d_feasible(args.num_constrains)
        else:
            raise ValueError('invalid type')
        path = writer.write(args.file_path,(program[0],program[1]))
        print(f"Generated file: {path}")

    elif args.command == 'solve':
        dimension = reader.determine_dimension(args.file_path)
        obj,cons = reader.read(args.file_path,dimension)
        if args.solver == 'Convex' and dimension == 2:
            res = solvers.ConvexSolver.solve_with_convex(obj,cons)
        elif args.solver == 'OrTool' and dimension == 2:
            res = solvers.OrToolSolver.solve_with_or_2d(obj,cons)
        elif args.solver == 'OrTool' and dimension == 3:
            res = solvers.OrToolSolver.solve_with_or_3d(obj,cons)
        elif args.solver == 'Convex' and dimension == 3:
            res = solvers.Convex3DSolver.solve_with_convex(obj,cons)
        else:
            raise ValueError('invalid type or dimension')

        print(f"Result: {res}, dimension: {dimension},solver: {args.solver}")
        
        
    
    elif args.command == 'test':
        start = args.start
        end = args.end
        step = args.step
        type_para = None
        if args.type == 'bounded':
            type_para = ProblemType.BOUNDED
        elif args.type == 'infeasible':
            type_para = ProblemType.INFEASIBLE
        elif args.type == 'unbounded':
            type_para = ProblemType.UNBOUNDED
            
        if args.dimension == 2:
            res = compare_time.test_with_time(type_para,range(start,end,step),args.output_path)
        elif args.dimension == 3:
            res = compare_time.test_with_time_3d(type_para,range(start,end,step),args.output_path)
        else:
            raise ValueError('invalid dimension')
        
        print(f"Result: {res}")
        
