from argparse import ArgumentParser
import argparse
import re
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
        help='generate linear program ', dest='command')

    gen_parser = subparsers.add_parser('generate')

    gen_parser.add_argument('-n', '--num_constrains', type=int)
    gen_parser.add_argument('-t', '--type', type=str,choices=['bounded','infeasible','unbounded'])
    gen_parser.add_argument('-d', '--dimension', type=int,default=2)

    solve_parser = subparsers.add_parser('solve')
    solve_parser.add_argument('-f', '--file_name', type=str)
    solve_parser.add_argument('-d', '--dimension', type=int,default=2)
    solve_parser.add_argument('-t', '--type', type=str,choices=['Convex','OrTool'])
    
    test_parser = subparsers.add_parser('test')
    test_parser.add_argument('-s', '--start', type=int,default=10)
    test_parser.add_argument('-e', '--end', type=int,default=3000)
    test_parser.add_argument('-p', '--step', type=int,default=100)
    test_parser.add_argument('-t', '--type', type=str,choices=['bounded','infeasible','unbounded'])
    test_parser.add_argument('-n', '--name', type=str,default="result.txt")
    test_parser.add_argument('-d', '--dimension', type=int,default=2)
    

    def range_type(arg_value, pat=re.compile(r"^\d+,\d+,\d+$")):
        if not pat.match(arg_value):
            raise argparse.ArgumentTypeError("invalid value")
        return arg_value
    solve_parser.add_argument('-r', '--range', type=range_type)

    args = parser.parse_args()

    if args.command == 'generate':
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
        
        path = writer.save_to_file(args.type,program[0],program[1])

        print(f"Generated file: {path}")

    elif args.command == 'solve':
        obj,cons = reader.read(args.file_name,args.dimension)
        if args.type == 'Convex' and args.dimension == 2:
            res = solvers.ConvexSolver.solve_with_convex(obj,cons)
        if args.type == 'OrTool' and args.dimension == 2:
            res = solvers.or_tool_solver
            
        
        
    
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
            compare_time.test_with_time(type_para,range(start,end,step),args.name)
        elif args.dimension == 3:
            compare_time.test_with_time_3d(type_para,range(start,end,step),args.name)
        
