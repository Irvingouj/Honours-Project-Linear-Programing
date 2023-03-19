from argparse import ArgumentParser
import argparse
import re
import linear_programming.utils.linear_program_generator as gen
import linear_programming.utils.compare_time as compare_time


def main():
    parser = ArgumentParser(prog='linear_programming',
                            description='Honours Project for Irving Ou')

    subparsers = parser.add_subparsers(
        help='generate linear program ', dest='command')

    gen_parser = subparsers.add_parser('generate')

    gen_parser.add_argument('-n', '--num_constrains', type=int)
    gen_parser.add_argument('-t', '--type', type=str,choices=['bounded','infeasible','unbounded'])

    solve_parser = subparsers.add_parser('solve')
    solve_parser.add_argument('-f', '--file_name', type=str)
    
    solve_parser = subparsers.add_parser('test')
    solve_parser.add_argument('-s', '--start', type=int,default=10)
    solve_parser.add_argument('-e', '--end', type=int,default=3000)
    solve_parser.add_argument('-t', '--step', type=int,default=100)
    

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
        
        path = gen.save_to_file(args.type,program[0],program[1])

        print(f"Generated file: {path}")

    elif args.command == 'solve':
        raise NotImplementedError()
    
    elif args.command == 'test':
        start = args.start
        end = args.end
        step = args.step
        compare_time.test_data_feasible(range(start,end,step))
        
